// Feeling Safe Studio — Cloudflare Worker.
// Keeps the Comfy Cloud API keys away from the browser and forwards four calls:
//   POST /upload            raw file body          -> { k, asset }
//   POST /voice             { k, ref, text, language }           -> { k, job }
//   POST /video             { k, image, audio, seconds, prompt, shape } -> { k, job }   shape: "portrait" | "landscape"
//   GET  /job/:id?k=        job status and outputs
//   GET  /file/:assetId?k=  download an output
//   POST /delete            { k, ids } remove uploads and outputs from Comfy
//   GET  /check             password test
// Secrets (set by the GitHub Action): COMFY_KEYS_A, COMFY_KEYS_B (comma-separated keys per group),
// CLASS_PASSWORD. Every request names its group in the header x-group: A or B.
// Comfy queues extra jobs per account (tested: 6 at once on one key all ran), so several
// students at the same time just wait in that group's queue.
// Vars (wrangler.toml): ALLOWED_ORIGINS, END_DATE, MAX_VIDEO_SECONDS.

import VIDEO_WORKFLOW from "./video_workflow.json";

const API = "https://cloud.comfy.org/api/v2";
const LANGUAGES = ["English", "German", "Chinese", "French", "Italian", "Spanish",
  "Portuguese", "Russian", "Japanese", "Korean"];
const MAX_UPLOAD = 15 * 1024 * 1024;
const MAX_TEXT = 1200;
const FPS = 25;
const DEFAULT_PROMPT = "A news anchor speaks calmly and clearly to the camera in a TV studio.";

const voiceWorkflow = (text, language, ref, seed) => ({
  "1": { class_type: "FB_Qwen3TTSVoiceClone", inputs: {
    target_text: text, model_choice: "0.6B", device: "auto", precision: "bf16",
    language, ref_audio: ["2", 0], seed, x_vector_only: true } },
  "2": { class_type: "LoadAudio", inputs: { audio: assetRef(ref) } },
  "3": { class_type: "SaveAudioMP3", inputs: { audio: ["1", 0], filename_prefix: "audio/voice", quality: "V0" } },
});

function videoWorkflow(image, audio, seconds, prompt, seed, landscape) {
  const g = structuredClone(VIDEO_WORKFLOW);
  // 384 x 672 portrait or 672 x 384 (≈16:9) landscape, e.g. an anchor at a news desk; same speed
  Object.assign(g["330:340"].inputs, landscape ? { width: 672, height: 384 } : { width: 384, height: 672 });
  g["284"].inputs.image = assetRef(image);
  g["125"].inputs.audio = assetRef(audio);
  g["330:337"].inputs.num_frames = Math.max(FPS, Math.ceil(seconds * FPS));
  g["330:332"].inputs.positive_prompt = prompt;
  g["330:333"].inputs.seed = seed;
  return g;
}

function assetRef(a) {
  if (!a || typeof a.id !== "string" || typeof a.hash !== "string") throw new HttpError(400, "Missing file. Please upload it again.");
  return { __type: "core/ASSET", info: { id: a.id, hash: a.hash, file_path: String(a.file_path || "input") } };
}

class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

const seed = () => Math.floor(Math.random() * 2 ** 31);

export default {
  async fetch(req, env) {
    const cors = corsHeaders(req, env);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    try {
      const url = new URL(req.url);
      if (url.pathname === "/health") return json({ ok: true, end: env.END_DATE || null }, cors);
      checkAccess(req, env);
      if (url.pathname === "/check") return json({ ok: true }, cors);
      const group = (req.headers.get("x-group") || "").toUpperCase();
      if (!["A", "B"].includes(group)) throw new HttpError(400, "Choose group A or B.");
      const keys = (env["COMFY_KEYS_" + group] || env.COMFY_KEYS || "").split(/[\s,]+/).filter(Boolean);
      if (!keys.length) throw new HttpError(500, `Group ${group} has no Comfy key yet.`);
      const pick = (k) => {
        const i = Number.isInteger(k) ? k : parseInt(k, 10);
        if (i >= 0 && i < keys.length) return i;
        return Math.floor(Math.random() * keys.length);
      };

      if (req.method === "POST" && url.pathname === "/upload") {
        const k = pick(req.headers.get("x-key-index"));
        const type = (req.headers.get("content-type") || "application/octet-stream").split(";")[0];
        if (!/^(audio|image|video)\//.test(type)) throw new HttpError(415, "Please upload an audio file or a photo.");
        const body = await req.arrayBuffer();
        if (body.byteLength > MAX_UPLOAD) throw new HttpError(413, "The file is too large (max. 15 MB).");
        const name = (req.headers.get("x-filename") || "upload").replace(/[^\w.\-]/g, "_").slice(0, 80);
        const fd = new FormData();
        fd.append("content_type", type);
        fd.append("file_path", name);
        fd.append("file", new Blob([body], { type }), name);
        const a = await comfy(keys[k], "/assets", { method: "POST", body: fd });
        return json({ k, asset: { id: a.id, hash: a.hash, file_path: name } }, cors);
      }

      if (req.method === "POST" && url.pathname === "/voice") {
        const b = await req.json();
        const k = pick(b.k);
        const text = String(b.text || "").trim();
        if (!text) throw new HttpError(400, "Please type a script.");
        if (text.length > MAX_TEXT) throw new HttpError(400, `The script is too long (max. ${MAX_TEXT} characters).`);
        if (!LANGUAGES.includes(b.language)) throw new HttpError(400, "Unknown language.");
        const job = await comfy(keys[k], "/jobs", { method: "POST", json: { workflow: voiceWorkflow(text, b.language, b.ref, seed()) } });
        return json({ k, job: job.id }, cors);
      }

      if (req.method === "POST" && url.pathname === "/video") {
        const b = await req.json();
        const k = pick(b.k);
        const max = Number(env.MAX_VIDEO_SECONDS || 45);
        const seconds = Number(b.seconds);
        if (!(seconds > 0)) throw new HttpError(400, "Could not read the length of the audio.");
        if (seconds > max) throw new HttpError(400, `The audio is ${seconds.toFixed(1)} s; the limit is ${max} s.`);
        const prompt = String(b.prompt || DEFAULT_PROMPT).slice(0, 400);
        const job = await comfy(keys[k], "/jobs", { method: "POST", json: { workflow: videoWorkflow(b.image, b.audio, seconds, prompt, seed(), b.shape === "landscape") } });
        return json({ k, job: job.id }, cors);
      }

      if (req.method === "POST" && url.pathname === "/delete") {
        const b = await req.json();
        const k = pick(b.k);
        const ids = (Array.isArray(b.ids) ? b.ids : []).filter((x) => /^[\w-]{8,64}$/.test(x)).slice(0, 6);
        await Promise.all(ids.map((id) => fetch(`${API}/assets/${id}`, { method: "DELETE", headers: auth(keys[k]) }).catch(() => {})));
        return json({ deleted: ids.length }, cors);
      }

      let m;
      if (req.method === "GET" && (m = url.pathname.match(/^\/job\/([\w-]{8,64})$/))) {
        const k = pick(url.searchParams.get("k"));
        const j = await comfy(keys[k], `/jobs/${m[1]}`);
        return json({
          status: j.status, queue_position: j.queue_position, progress: j.progress,
          error: j.error ? (j.error.message || String(j.error)) : null,
          outputs: (j.outputs || []).map((o) => ({ id: o.id, name: o.name, content_type: o.content_type, node: o.node_id })),
        }, cors);
      }

      if (req.method === "GET" && (m = url.pathname.match(/^\/file\/([\w-]{8,64})$/))) {
        const k = pick(url.searchParams.get("k"));
        const r = await fetch(`${API}/assets/${m[1]}/content`, { headers: auth(keys[k]), redirect: "manual" });
        const res = r.status >= 300 && r.status < 400 ? await fetch(r.headers.get("location")) : r;
        if (!res.ok) throw new HttpError(502, "Could not download the result.");
        const h = new Headers(cors);
        h.set("content-type", res.headers.get("content-type") || "application/octet-stream");
        if (res.headers.get("content-length")) h.set("content-length", res.headers.get("content-length"));
        return new Response(res.body, { headers: h });
      }

      throw new HttpError(404, "Not found.");
    } catch (e) {
      const status = e instanceof HttpError ? e.status : 500;
      return json({ error: e instanceof HttpError ? e.message : "Something went wrong. Please try again." }, cors, status);
    }
  },
};

function checkAccess(req, env) {
  if (env.END_DATE && new Date() > new Date(env.END_DATE + "T23:59:59")) throw new HttpError(403, "The studio is closed.");
  const pw = env.CLASS_PASSWORD;
  if (!pw || req.headers.get("x-class-password") !== pw) throw new HttpError(401, "Wrong class password.");
}

function corsHeaders(req, env) {
  const origin = req.headers.get("origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || "*").split(",").map((s) => s.trim());
  const ok = allowed.includes("*") || allowed.includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? (origin || "*") : allowed[0],
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, x-class-password, x-filename, x-key-index, x-group",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

const auth = (key) => ({ Authorization: `Bearer ${key}` });

async function comfy(key, path, { method = "GET", json: body, body: raw } = {}) {
  const headers = auth(key);
  let payload = raw;
  if (body !== undefined) { headers["content-type"] = "application/json"; payload = JSON.stringify(body); }
  let r = await fetch(API + path, { method, headers, body: payload });
  if (r.status === 429 && method === "POST" && body !== undefined) {   // busy: one retry for JSON submits
    await new Promise((ok) => setTimeout(ok, 2000));
    r = await fetch(API + path, { method, headers, body: payload });
  }
  const text = await r.text();
  let data = {};
  try { data = text ? JSON.parse(text) : {}; } catch { /* not JSON */ }
  if (r.status === 401 || r.status === 403) throw new HttpError(502, "The school's Comfy key was refused. Tell your teacher.");
  if (r.status === 429) throw new HttpError(429, "Too many requests right now. Please wait a minute.");
  if (!r.ok) throw new HttpError(502, `Comfy Cloud error ${r.status}: ${(data.message || data.error || text).toString().slice(0, 200)}`);
  return data;
}

function json(obj, cors, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { ...cors, "content-type": "application/json" } });
}
