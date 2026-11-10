# Safety Online 工作坊工具（Worker）

頁面：`https://liutingchun.com/workshops/safety-online/`（`workshops/safety-online/index.html`，手寫，不是 `build.py` 產生的）。
刻意隱藏：沒有任何頁面連到它，不在 `sitemap.xml`、HTML 網站地圖、`llms.txt`，頁面有 `noindex`；只有知道網址的人找得到。
`build.py` 重建時用 `KEEP` 保留這個資料夾。

這個 Worker（`feeling-safe-studio`）替頁面呼叫 Comfy Cloud，金鑰只在 Cloudflare：

- 聲音：參考錄音（錄或上傳，長度不限、最多取前 2 分鐘，可以不給；越長通常越像）＋音色描述＋稿子 → MP3。沒有錄音時，先用 Qwen3 VoiceDesign（開源）依描述合成一段樣本聲音，再交給 ElevenLabs 複製。用自己的聲音念出的 MP3（ElevenLabs v4，經 Comfy 的夥伴節點；稿子裡可寫 `[happy]`、`[whispers]` 等情緒標籤）。
  費用從 Comfy 點數扣：複製聲音約 $0.15（同一段錄音會沿用快取），念稿每 1000 字元約 $0.11。學生的聲音會送到 ElevenLabs。
- 圖片：一段描述 → 一張手機直式 9:16 的圖（Z-Image Turbo，768×1344，約 15 秒），可直接當影片的臉
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

`wrangler.toml`：`VIDEO_FROM`（第 3 步影片從這天開放，威瑪時間；之前只能做聲音和圖片，Worker 也會擋下影片請求。改日期後 push 到 main 就會重新部署）、`ALLOWED_ORIGINS`（只接受 liutingchun.com）、`END_DATE`（2027-02-28 之後關閉）、`MAX_VIDEO_SECONDS`。

## 本機測試

`worker-studio/.dev.vars`（不進 git）：`COMFY_KEYS_A=…`、`COMFY_KEYS_B=…`、`CLASS_PASSWORD=…`、`ALLOWED_ORIGINS="*"`，
然後 `cd worker-studio && npm install && npx wrangler dev`，
開 `http://localhost:8000/workshops/safety-online/?api=http://127.0.0.1:8787`（另開 `python3 -m http.server 8000`）。

## 工作坊結束後

刪掉 Worker（Cloudflare → Workers）、刪掉 `workshops/safety-online/` 並把 `build.py` 的 `KEEP` 清掉，
到 platform.comfy.org **撤銷所有 Comfy key**（開發時金鑰曾貼在對話裡）。
不要在任何檔案寫入金鑰；不要記錄請求內容（學生的聲音與臉）。
