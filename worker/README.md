# Chat worker — "Ask about the work"

The homepage chat box sends questions here. This Cloudflare Worker adds the knowledge
base (the LLM wiki in `../wiki/`, bundled by `../scripts/build-knowledge.py`) and the
OpenAI API key, asks a ChatGPT model, and streams the answer back. Each exchange is kept in
a D1 database (see "Chat log" below).

## Set up (once)

1. OpenAI: create an API key at platform.openai.com/api-keys and set a monthly budget
   (Settings → Limits).
2. Cloudflare: My Profile → API Tokens → Create Token → "Edit Cloudflare Workers".
3. GitHub repo → Settings → Secrets and variables → Actions: add
   `CLOUDFLARE_API_TOKEN` and `OPENAI_API_KEY`.
4. Actions → "Deploy chat worker" → Run workflow. The log prints the Worker URL
   (`https://liutingchun-com-chat.<account>.workers.dev`).
5. Put that URL in `data/site.json` → `site.chat_endpoint`. The chat box appears on the
   homepage with the next build; leave it empty to hide it.

After that, every change to `wiki/` redeploys the Worker automatically.

## Settings (`wrangler.toml`)

- `MODEL`: which OpenAI model answers (`gpt-5.4-mini`; larger: `gpt-5.5`).
- `REASONING_EFFORT`: `none` (required with the `suggest_links` tool on gpt-5.4 models in the
  chat completions API); remove it for models without reasoning.
- `ALLOWED_ORIGINS`: pages allowed to use the Worker.
- Rate limits: 5 questions per minute per visitor, 20 per minute in total.
- Context: only the new question and the exchange before it are sent; answers are short.
- Links: the model may call the `suggest_links` tool; only URLs that appear in the wiki
  (see `wiki/pages/site-map.md`, generated from `data/site.json`) reach the visitor.

## Bot check (optional, recommended)

Cloudflare → Turnstile → Add widget (hostnames `liutingchun.com` and
`www.liutingchun.com`; mode "Invisible"). Put the **site key** in `data/site.json` →
`site.turnstile_sitekey`, and the **secret key** in the GitHub secret `TURNSTILE_SECRET`,
then run "Deploy chat worker". Requests without a valid check are refused.
- Logs (Cloudflare dashboard → Workers → liutingchun-com-chat → Logs) show token usage per
  answer, never the questions.

## Local test

    npm install
    printf 'OPENAI_API_KEY=sk-...\nALLOWED_ORIGINS=http://localhost:8000\n' > .dev.vars
    npx wrangler dev

## Chat log

Every exchange is stored in the Cloudflare D1 database `liutingchun-chat-log` (table `chats`):
time, page language, country, topic (the model sorts each question into one of `TOPICS` in
`src/index.js`), status (ok / refusal / error / aborted = the visitor left before the answer was finished / pending = the answer never arrived), question, answer, suggested links, the previous
question if it was a follow-up, model and tokens. No IP address. The question is saved the moment it arrives and completed when the answer ends, so a visitor who closes the page mid-answer still leaves an entry (status `aborted`). Kept without time limit; the
privacy page (Datenschutz, section 7) says so.

The deploy workflow finds the database by name or creates it on the first run (the Cloudflare
token needs **D1: Edit** besides Workers) and puts its id into `wrangler.toml` for that deploy;
the Worker creates the table itself.

To read it on your computer:

    CLOUDFLARE_API_TOKEN=<token with Account / D1 / Read> python3 worker/log-viewer.py

It opens http://localhost:8790 with filters for topic, language, status, country, dates and a
text search. `--local` reads the test database of `npx wrangler dev` instead.
Single entries can also be read or deleted in the Cloudflare dashboard: Storage & databases → D1
→ liutingchun-chat-log → Console (e.g. `DELETE FROM chats WHERE id = 42`).
