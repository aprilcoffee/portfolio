# 給 AI agent 的工作說明

這份是給接手的 AI agent（Claude、ChatGPT/Codex、Cursor…）看的：哪裡改什麼、哪些不能碰，特別是**翻譯**。
人看的說明在 `README.md`；`CLAUDE.md` 只是指到這裡。

## 先記住的規則

1. **不要手改產生出來的 HTML。** `index.html`、`works/`、`performance/`、`about/`、`blog/`、`friends/`、`de/`、`zh/`、
   `impressum/`、`datenschutz/`、`sitemap.xml`、`robots.txt`、`llms.txt`、`blog/feed.xml`，還有根目錄那些舊 Wix 網址的
   轉址資料夾（`cv/`、`post/`、`sun/`、`fall/`、`beneath/`…）全部由 `scripts/build.py` 產生，下一次建置就會被覆蓋。
   要改就改來源（`data/`、`posts/`、`scripts/build.py`、`assets/`）。
2. **改完要重建。** `pip install markdown && python3 scripts/build.py`。產生的檔案可以一起 commit；
   就算沒有，push 到 main 之後 `.github/workflows/build.yml` 也會重建並自己 commit「Rebuild pages」。
3. **三種語言要一起改。** 新增或修改任何顯示在網頁上的文字，英文、德文、繁體中文都要處理（見下面〈翻譯〉）。
4. **另一個 repo 的東西不要動。** `aprilcoffee.github.io` 上的 `sun/` 和 `heat_as_image/` 是獨立作品，絕對不要改；
   那邊的 `liutingchun/` 已封存，只剩轉址到 liutingchun.com 的頁面（`liutingchun/assets/analytics.js` 要保留，sun 跟 heat 會載入它）。
   所有改動都在這個 repo（portfolio）。
5. **不放祕密。** API key、token 只放在 GitHub Secrets／Cloudflare，不寫進任何檔案。`wiki/raw/private/` 不進 git，
   wiki 裡不能有私人資料（地址、電話、健康、家人、財務）。
6. `data/site.json` 也是後台（`/admin/`）在改的檔案。改之前先 `git pull`，避免蓋掉作者剛從後台發佈的內容。

## 檔案地圖：要改什麼，去哪裡

| 想改的東西 | 檔案 |
|---|---|
| 作品、表演、CV、朋友、文章列表、網站名稱／描述／statement（SEO 用）／首頁大字 `home_text`／email／GA／對話框網址 | `data/site.json` |
| 文章內文（中文部落格，不翻譯） | `posts/<slug>.md` |
| 介面文字（選單、按鈕、頁面引言、對話框提示…） | `scripts/build.py` 的 `UI` 字典 |
| 頁面結構、HTML、SEO（title、canonical、hreflang、JSON-LD、sitemap） | `scripts/build.py` |
| Impressum、Datenschutz（只有德文） | `scripts/build.py` 裡 `page("impressum/"…)`、`page("datenschutz/"…)`、`CHAT_PRIVACY` |
| 樣式 | `assets/style.css`（全部用 rem；桌機 `html{font-size:80%}`，≤800px 回到 100%；斷點 1024px、800px） |
| 選單、語言切換等前端行為 | `assets/site.js` |
| p5.js 背景特效（首頁字元場、側欄訊號線） | `assets/effects.js` |
| 首頁問答框的前端（打字機效果、ASCII 顯卡風扇與溫度顏色） | `assets/chat.js`；ASCII 顯卡由 `build.py` 的 `_ask_gpu()` 產生，HTML 在 `ask_box()` |
| GA4 同意橫幅 | `assets/analytics.js` |
| 問答的 AI 規則、模型、連結工具 | `worker/src/index.js`（`RULES`、`suggest_links`、`localize()`），設定在 `worker/wrangler.toml` |
| 問答紀錄（每次提問與回答，存在 Cloudflare D1，不存 IP） | 寫入：`worker/src/index.js` 的 `save()`、主題分類 `TOPICS`；本機查看：`python3 worker/log-viewer.py`（說明在 `worker/README.md`）。改了存的內容要同步改 Datenschutz 的 `CHAT_PRIVACY` |
| 問答的知識（作品、經歷、說法） | `wiki/`（規則見 `wiki/CLAUDE.md`） |
| `llms.txt` 最後的彩蛋（ASCII 顯卡、給 agent 的話、藝術家介紹） | `data/llms-extra.md`（原樣接在後面） |
| 圖示、分享圖 | `favicon.ico`、`assets/favicon-32.png`、`assets/apple-touch-icon.png`、`assets/icon-192/512.png`、`site.webmanifest`、`images/og.jpg`（`site.og_image`） |
| 圖片與影片檔 | `images/wix/`（新的 Wix 圖用 `scripts/download-images.sh` 下載） |
| 後台 | `admin/index.html`、`admin/admin.js`；草稿預覽 `preview.html`（在瀏覽器用 Pyodide 跑同一個 `build.py`） |
| 自動化 | `.github/workflows/`：`build.yml`（重建網站）、`deploy-chat.yml`（部署問答 Worker）、`check-links.yml`（每月檢查連結）、`download-wix-images.yml` |

`assets/` 的 CSS/JS 由 `versioned()` 自動加上 `?v=<hash>`，改了檔案瀏覽器就會重新抓，不用手動改版本號。
（`build.py` 裡另有一個舊的 `asset()` 函式處理圖片網址，兩個不要混用或重新命名。）

## 翻譯

網站有三種語言：英文在根目錄（`/`），德文在 `/de/`，繁體中文在 `/zh/`。程式裡的語言代碼是 `en`、`de`、`zh`
（`LANGS`、`LP` 路徑前綴、`HREFLANG` 的 `zh` 對應 `zh-Hant`、`LOCALE` 的 `zh_TW`，都在 `build.py` 開頭）。

### 1. 內容：`data/site.json` 的 `_de` / `_zh` 欄位

同一個欄位加後綴就是翻譯，`build.py` 用 `tr(obj, key, lang)` 讀取：有 `key_de`／`key_zh` 就用，**空的或沒有就顯示英文**。

| 位置 | 英文欄位 | 翻譯欄位 |
|---|---|---|
| `site` | `description`、`statement`、`job_title`、`home_text` | `description_de/_zh`、`statement_de/_zh`、`job_title_de/_zh`、`home_text_de/_zh` |

`home_text` 是首頁下方的大字，留空時只留白不顯示（不會退回英文或 statement）；`statement` 只用在 JSON-LD、分享與 llms.txt，不顯示在首頁。
| `works[]` | `text`、`type`、`materials` | `text_de/_zh`、`type_de/_zh`、`materials_de/_zh` |
| `performances[]` | `note` | `note_de/_zh` |
| `about` | `bio` | `bio_de/_zh` |
| `about.sections[]`（CV 區塊） | `title` | `title_de/_zh` |
| `about.sections[].items[]`（CV 每一行） | `text` | `text_de/_zh`（目前多數只有 `_zh`） |

注意：
- **作品標題不翻譯。** `works[].title` 各語言都一樣；`works[].title_zh` 不是翻譯，而是作品的中文名，三種語言的頁面都會顯示在英文標題旁。
  `site.name_zh`（劉庭均）也一樣。
- CV 行沒有翻譯時，`build.py` 會給那一行加 `lang="en"`，讓瀏覽器與搜尋引擎知道這段是英文。
- 表演影片標題、合作者（`collaborators`）、年份、網址不翻譯。
- 新增一個要翻譯的欄位時：在 `site.json` 加 `xxx_de`/`xxx_zh`，在 `build.py` 用 `tr(obj, "xxx", L)` 讀，
  並在 `admin/admin.js` 加對應的輸入框（照 `text_de`、`type_zh` 那幾行的寫法），作者才能在後台編輯。
- 翻譯風格：德文用 Sie、性別中立寫法（`Künstler*innen`）；中文用繁體、台灣用語、全形標點，作品名用《》。

### 2. 介面文字：`scripts/build.py` 的 `UI` 字典

`UI = {"en": {...}, "de": {...}, "zh": {...}}`，三個語言的 key 必須一樣。新增 key 時三個都要加，否則該語言的頁面建置時會出錯。
`%s`、`%d` 是程式填入的值（名字、年份、數量、網址），翻譯時要保留、數量相同。

問答框的字串也在這裡：
- `ask`（區塊的 aria-label）、`ask_ph`（輸入框提示：Ask me anything／Fragen Sie mich alles／問我任何事）、`ask_btn`
- `ask_note`：框下方的提醒。**只有德文版有 `· %s`**，會被換成 Datenschutz 的連結（`ask_more`）；英文、中文刻意沒有連結，不要加回去。
- `ask_q`：三個範例問題（list）
- `ask_err`（`%s` 會填 email）、`ask_busy`、`ask_refusal`：錯誤訊息，由 `chat.js` 顯示
- 介面用第一人稱（「問我」、「我的作品」），因為問答框代表藝術家本人。

### 3. 不翻譯、只有一種語言的部分

- **部落格文章**（`posts/*.md`）：只有一份，在 `/blog/<slug>/`，中文；外框用英文介面。德文、中文的部落格列表頁會連到同一份。
- **Impressum、Datenschutz**：只有德文（德國法律要求），三種語言的頁尾都連到同一頁。問答框的隱私說明在 `CHAT_PRIVACY`。
- **`wiki/`**：只用英文寫。問答會用訪客的語言回答（`chat.js` 送出 `document.documentElement.lang`）。
- **`llms.txt`、`data/llms-extra.md`**：英文。

### 4. 問答框推薦的連結

`wiki/pages/site-map.md` 由 `scripts/wiki-sitemap.py` 從 `site.json` 自動產生（不要手改），列出每頁的三種語言網址。
模型被要求給**英文網址**，Worker 的 `localize(url, lang)` 再依頁面語言改成 `/de/…` 或 `/zh/…`（只在 site-map 裡有那個語言版本時才換；
部落格、Impressum、Datenschutz 只有一份，外部連結也不改）。新增語言或改網址結構時，要同步改 `worker/src/index.js` 的 `PREFIX`。

### 5. 新增一種語言（例如日文）要改的地方

`build.py` 的 `LANGS`、`LP`、`HREFLANG`、`LOCALE`、`LANG_NAME`、`UI`；`site.json` 加 `_ja` 欄位；
`admin/admin.js` 的輸入框；`scripts/wiki-sitemap.py` 的 `LANGS`；`worker/src/index.js` 的 `PREFIX`。

## 常見工作

- **新增作品**：在 `site.json` 的 `works` 加一筆（`slug`、`title`、`title_zh`、`year`、`type`、`text`、圖片…，加上 `_de`/`_zh` 翻譯），
  重建。如果這件作品在 wiki 裡還沒有，順便在 `wiki/pages/works/` 新增一頁（照 `wiki/CLAUDE.md`）。
- **改問答的知識或語氣**：改 `wiki/`，跑 `python3 scripts/wiki-lint.py --index`，在 `wiki/log.md` 記一行。
  push 到 main 後 `deploy-chat.yml` 會用 `scripts/build-knowledge.py` 打包 wiki 並部署 Worker。語氣規則在 `wiki/CLAUDE.md` 的
  “The chat's voice” 與 `worker/src/index.js` 的 `RULES`。
- **改問答框外觀**：`assets/style.css`（`.ask…`）、`assets/chat.js`、`build.py` 的 `ask_box()`／`_ask_gpu()`。
- **本機預覽**：`python3 scripts/build.py && python3 -m http.server 8000`，開 http://localhost:8000/ 、/de/、/zh/ 三種語言都看一次。
- **問答 Worker 本機測試**：`cd worker && npm install && npx wrangler dev`（需要 `.dev.vars` 裡的 `OPENAI_API_KEY`，不要 commit）。

## 網域與部署（不用 agent 處理，但要知道）

- 網站由 GitHub Pages 從這個 repo 的 main 提供，網域 `liutingchun.com`（`CNAME`）。DNS 目前在 Wix，之後會搬到 Cloudflare；
  細節見 `README.md` 的〈網域〉。Google Search Console 的 TXT 記錄不要刪。
- 問答 Worker：`liutingchun-com-chat`（Cloudflare），網址存在 `site.chat_endpoint`，頁面裡以反轉＋base64 的 `data-e` 呈現。
  只接受 liutingchun.com 與 www 的來源，每位訪客每分鐘 5 次、全站 20 次。
