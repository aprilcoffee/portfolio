# Safety Online 工作坊工具（Worker）

頁面：`https://liutingchun.com/workshops/safety-online/`（`workshops/safety-online/index.html`，手寫，不是 `build.py` 產生的）。
刻意隱藏：沒有任何頁面連到它，不在 `sitemap.xml`、HTML 網站地圖、`llms.txt`，頁面有 `noindex`；只有知道網址的人找得到。
`build.py` 重建時用 `KEEP` 保留這個資料夾。

這個 Worker（`feeling-safe-studio`）替頁面呼叫 Comfy Cloud，金鑰只在 Cloudflare：

- 聲音：錄音或上傳 10–30 秒 + 文字 → 用自己的聲音念出的 MP3（Qwen3-TTS 0.6B）
- 臉：照片 + MP3 → 對嘴影片 MP4（Wan2.1 InfiniteTalk，`video_workflow.json`）

## 部署

1. GitHub repo → Settings → Secrets and variables → Actions，新增：
   `COMFY_KEYS_A`、`COMFY_KEYS_B`（各組的 Comfy key，多把用逗號分開）、`CLASS_PASSWORD`（學生輸入的密碼）。
   `CLOUDFLARE_API_TOKEN` 問答 Worker 已經在用。
2. Actions → **Deploy studio worker** → Run workflow（之後改 `worker-studio/` 並 push 到 main 也會自動部署）。
3. 測試：
   `curl https://feeling-safe-studio.8765498-208.workers.dev/health`
   `curl -H 'x-class-password: …' https://feeling-safe-studio.8765498-208.workers.dev/check`
   再到頁面做一次聲音、一次短影片。

`wrangler.toml`：`ALLOWED_ORIGINS`（只接受 liutingchun.com）、`END_DATE`（2026-12-08 之後關閉）、`MAX_VIDEO_SECONDS`。

## 本機測試

`worker-studio/.dev.vars`（不進 git）：`COMFY_KEYS_A=…`、`COMFY_KEYS_B=…`、`CLASS_PASSWORD=…`、`ALLOWED_ORIGINS="*"`，
然後 `cd worker-studio && npm install && npx wrangler dev`，
開 `http://localhost:8000/workshops/safety-online/?api=http://127.0.0.1:8787`（另開 `python3 -m http.server 8000`）。

## 工作坊結束後

刪掉 Worker（Cloudflare → Workers）、刪掉 `workshops/safety-online/` 並把 `build.py` 的 `KEEP` 清掉，
到 platform.comfy.org **撤銷所有 Comfy key**（開發時金鑰曾貼在對話裡）。
不要在任何檔案寫入金鑰；不要記錄請求內容（學生的聲音與臉）。
