# Ting-Chun Liu — portfolio

https://liutingchun.com 的原始碼：從 Wix 搬出來的個人網站，由 GitHub Pages 提供。內容只有兩個地方：

- `data/site.json`：作品、表演、CV、朋友、文章列表、網站設定
- `posts/<slug>.md`：每篇文章的內文（Markdown）

**這個 repo 是主要版本。** 舊網址 `aprilcoffee.github.io/liutingchun/` 已封存，所有頁面都轉到 liutingchun.com 對應的網址
（`aprilcoffee.github.io` 上的 `sun/`、`heat_as_image/` 不動）。

`scripts/build.py` 會把它們產生成每一頁一個資料夾的靜態 HTML（`works/sun/`、`blog/lift-off/`…），每頁都有自己的 title、description、canonical、Open Graph、JSON-LD，並產生 `sitemap.xml`、`robots.txt`（放在網域根目錄）與文章 RSS（`blog/feed.xml`）。

網站是三語：英文在根目錄，德文在 `de/`，繁體中文在 `zh/`（部落格文章不翻譯，只有一份在 `blog/<slug>/`）。舊的 `writing/…` 網址會自動轉到 `blog/…`。翻譯放在哪裡見下面〈翻譯〉。

> **用 AI agent 改網站之前，先讓它讀 [`AGENTS.md`](AGENTS.md)**：檔案地圖、翻譯規則、不能動的東西都在那裡（`CLAUDE.md` 會自動指過去）。

```
（repo 根目錄）
├── index.html, works/, performance/, about/, blog/, friends/, de/, zh/   ← 自動產生，不要手改
├── data/site.json
├── posts/*.md
├── images/wix/          圖片與影片
├── data/llms-extra.md   接在 llms.txt 後面的彩蛋
├── assets/style.css, site.js, effects.js, chat.js, analytics.js
├── preview.html         後台的草稿預覽（瀏覽器裡跑 build.py）
├── admin/               極簡後台
├── wiki/                LLM Wiki：給首頁對話框用的知識庫（見 wiki/CLAUDE.md）
├── worker/              首頁問答的 Cloudflare Worker
└── scripts/build.py, build-knowledge.py, wiki-sitemap.py, wiki-lint.py, download-images.sh, check-videos.py
```

網址：`https://liutingchun.com/`（repo 根目錄的 `CNAME` 檔）

## 更新內容

1. 打開 `/admin/`，修改後會自動存成本機草稿，「預覽草稿」可先看效果。
2. 「發佈」頁填入 fine-grained token（只給這個 repo 的 *Contents: Read and write*），按「發佈到 GitHub」。
3. GitHub Actions（`.github/workflows/build.yml`）會自動重跑 `build.py` 並 commit 產生的頁面，約 1–2 分鐘後上線。

直接在 GitHub 上改 `site.json` 或 `posts/*.md` 也一樣會觸發重建。

## 內容格式

- 作品說明：空一行＝分段；以 `# ` 開頭＝小標題；網址自動變連結。
- 文章：一般 Markdown。`![說明](圖片)` 會變成有圖說的圖片；單獨一行的 Vimeo / YouTube / mp4 網址會變成播放器。
- 舊網站 `liutingchun.com/...` 的連結會自動改指到新頁面（對照表在各作品的 `aliases`）。
- `hidden: true` 的作品或文章不會出現在網站。

## 翻譯

| 要翻譯的東西 | 寫在哪裡 |
|---|---|
| 作品說明、形式、媒材、表演說明、Bio、CV 標題與每一行、網站描述、Statement | `data/site.json` 同名欄位加 `_de` / `_zh`（如 `text_de`、`materials_zh`、`bio_de`）；留空＝顯示英文。後台每個欄位旁都有 DE／中文 輸入框 |
| 選單、按鈕、頁面引言、問答框的提示與錯誤訊息 | `scripts/build.py` 的 `UI` 字典（`en` / `de` / `zh` 三組，key 要一致） |
| 部落格文章 | 不翻譯，只有中文一份 |
| Impressum、Datenschutz | 只有德文 |
| `wiki/`（問答知識庫）、`llms.txt` | 只有英文；問答會用訪客的語言回答，推薦連結會換成訪客語言的頁面 |

作品標題不翻譯；`title_zh` 是作品的中文名，三種語言都會顯示。問答框下方的提醒只有德文版附 Datenschutz 連結。

## 網域

`site.json` 裡的 `site.base_url`（`https://liutingchun.com`）決定 canonical、分享連結與 sitemap。網站在網域根目錄，所以 `build.py` 也會為舊的 Wix 網址（`/cv`、`/post/...`、`/sun`…）產生轉址頁。

目前網域註冊與 DNS 都還在 Wix：`@` 四筆 A 紀錄指向 GitHub Pages（185.199.108–111.153），`www` 的 CNAME 指向 `aprilcoffee.github.io`，HTTPS 憑證由 GitHub（Let's Encrypt）自動續期。
另外有一筆 Google Search Console 驗證用的 TXT 記錄，**不要刪**。

之後轉到 Namecheap、DNS 改到 Cloudflare 時：先在 Cloudflare 建好同樣的記錄（4 筆 A、www CNAME、Search Console 的 TXT），都設成 DNS only（灰色雲朵），再改 NS，網站就不會中斷。

## 設計

- 版面依作品集設計系統：白底、左側資訊欄＋右側圖版（plates）、等寬字的中繼資料、極少量的紅色 `#E4032E`。
- 字型用系統字（Helvetica／Arial、蘋方／微軟正黑、等寬字），不從 Google 載入字型（德國法院曾對遠端 Google Fonts 判罰）。
- p5.js 特效在 `assets/effects.js`：首頁字元場（字元依〈Processing 蒙地卡羅演算法做文字動畫〉算出的密度排序）、側欄訊號線。p5.js 在頁面載入完成後才載入；使用者設定「減少動態」時只畫靜態一格。

## Google Analytics 與法律頁

- GA4（`site.ga_id`，目前 `G-5XL9T33VG0`，GA 裡的串流「liutingchun - GA4」，從 Wix 時期延續）由 `assets/analytics.js` 載入，每次瀏覽都會載入（沒有 cookie 同意視窗）；訪客可以在 Datenschutz 頁按按鈕關掉，選擇存在瀏覽器。`aprilcoffee.github.io` 上的 `sun/`、`heat_as_image/` 用另一個串流 `G-JX0CS0510W`（「heat_as_image」），寫在它們自己的 HTML 裡，不受這裡影響。
- `impressum/`、`datenschutz/` 會自動產生並連在側欄底部。**`site.address` 必須填入可送達的郵寄地址**（德國 § 5 DDG 規定），可在後台「網站設定」填寫。
- `llms.txt`（網域根目錄）以一般文字向 AI 助理說明你的身分與作品，並由 robots.txt 指向。

## 連結檢查

`.github/workflows/check-links.yml` 每月 1 號檢查所有外部連結，也可在 Actions 分頁手動執行，結果在該次執行的 Summary。

## 圖片

新加入、還連到 Wix 的圖片（`static.wixstatic.com`）或影片，在本機執行：

```bash
bash scripts/download-images.sh
```

會下載到 `images/wix/`、轉成 webp，並改寫 `site.json` 與 `posts/*.md` 的路徑，之後 commit。

## 本機預覽

```bash
pip install markdown
python3 scripts/build.py
python3 -m http.server 8000      # 在 repo 根目錄執行
# http://localhost:8000/
```

也可以在 GitHub 的 Actions 分頁手動執行「Download Wix images」，它會在雲端下載並 commit。

## 首頁問答（AI chat）

`worker/` 是一個小型 Cloudflare Worker：訪客在首頁提問，它把 `wiki/` 的內容當作知識庫交給 ChatGPT（OpenAI API）回答。
設定步驟見 `worker/README.md`。在 `data/site.json` 填入 `site.chat_endpoint` 之後，首頁才會出現問答框。

每次提問和回答都會存在 Cloudflare D1（不存 IP，永久保存，Datenschutz 第 7 節有寫）。在自己電腦上看：

```bash
CLOUDFLARE_API_TOKEN=<只有 D1 Read 權限的 token> python3 worker/log-viewer.py
# 自動打開 http://localhost:8790 ，可依主題、語言、日期篩選與搜尋
```
