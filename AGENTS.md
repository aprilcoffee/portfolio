# 給 AI agent 的工作說明

這份是給接手的 AI agent（Claude、ChatGPT/Codex、Cursor…）看的：哪裡改什麼、哪些不能碰，特別是**翻譯**。
人看的說明在 `README.md`；`CLAUDE.md` 只是指到這裡。

## 先記住的規則

1. **不要手改產生出來的 HTML。** `index.html`、`works/`、`workshops/`、`about/`、`blog/`、`performance/` 與 `press/`（現在只是轉址）、`friends/`、`de/`、`zh/`、
   `impressum/`、`datenschutz/`、`sitemap.xml`、`robots.txt`、`llms.txt`、`blog/feed.xml`，還有根目錄那些舊 Wix 網址的
   轉址資料夾（`cv/`、`post/`、`sun/`、`fall/`、`beneath/`…）全部由 `scripts/build.py` 產生，下一次建置就會被覆蓋。
   要改就改來源（`data/`、`posts/`、`scripts/build.py`、`assets/`）。
2. **改完要重建。** `pip install markdown pillow fonttools brotli && python3 scripts/build.py`（沒有 Pillow 也能建，但圖片就不會有 `srcset` 小圖，頁面會跟著變）。產生的檔案可以一起 commit；
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
| 作品、表演紀錄、工作坊、CV、講座錄影與他人評論（`press`）、朋友、文章列表、網站名稱／描述／statement（SEO 用）／首頁大字 `home_text`／email／GA／對話框網址 | `data/site.json` |
| 文章內文（中文部落格，不翻譯） | `posts/<slug>.md` |
| 介面文字（選單、按鈕、頁面引言、對話框提示…） | `scripts/build.py` 的 `UI` 字典 |
| 頁面結構、HTML、SEO（title、canonical、hreflang、JSON-LD、sitemap） | `scripts/build.py` |
| Impressum、Datenschutz（只有德文） | `scripts/build.py` 裡 `page("impressum/"…)`、`page("datenschutz/"…)`、`CHAT_PRIVACY` |
| 字型 | `assets/fonts/`（都是 SIL OFL 開源字型，放在自己的伺服器；`fonts.css`、Minipax、粉圓由 `scripts/build-fonts.py` 產生，`fonts-google.css` 與芫荽的切片由 `scripts/fetch-google-fonts.py` 從 Google Fonts 下載一次，都不要手改；授權在 `assets/fonts/LICENSES/`，出處標示在 Impressum 的「Schriften」段落）。中文的分工：`--text` 內文（Minipax＋讀者裝置的系統黑體，跟臉書一樣：蘋果是蘋方、Windows 是微軟正黑體、Android 是 Noto Sans CJK；作品文字、About、工作坊、CV）；`--display` 標題、選單、卡片標題、首頁大字（Minipax Bold＋LTC Round／粉圓）；`--note` 中文小字與說明（Minipax＋芫荽 Iansui：卡片關鍵字、頁首引言、表演與講座說明、CV 跳轉列、圖說）；問答框用 `--mono`，中文落到芫荽。2026-10 試過內文用粉圓，無法閱讀，不要再用粉圓排內文；源起明體、仙人掌明體、思源宋體 Medium 都試過，作者不喜歡，內文改用系統黑體 |
| 樣式 | `assets/style.css`（全部用 rem；桌機 `html{font-size:80%}`，≤800px 回到 100%；斷點 1024px、800px） |
| 選單、語言切換等前端行為 | `assets/site.js` |
| p5.js 背景特效（首頁字元場、側欄訊號線） | `assets/effects.js` |
| 首頁問答框的前端（打字機效果、ASCII 顯卡風扇與溫度顏色） | `assets/chat.js`；ASCII 顯卡由 `build.py` 的 `_ask_gpu()` 產生，HTML 在 `ask_box()` |
| GA4 同意橫幅 | `assets/analytics.js` |
| 問答的 AI 規則、模型、連結工具 | `worker/src/index.js`（`RULES`、`suggest_links`、`localize()`），設定在 `worker/wrangler.toml` |
| 問答紀錄（每次提問與回答，存在 Cloudflare D1，不存 IP） | 寫入：`worker/src/index.js` 的 `save()`、主題分類 `TOPICS`；本機查看：`python3 worker/log-viewer.py`（說明在 `worker/README.md`）。改了存的內容要同步改 Datenschutz 的 `CHAT_PRIVACY` |
| 問答的知識（作品、經歷、說法） | `wiki/`（規則見 `wiki/CLAUDE.md`） |
| `llms.txt` 最後的彩蛋（ASCII 顯卡、給 agent 的話、藝術家介紹） | `data/llms-extra.md`（原樣接在後面） |
| 圖示、分享圖 | `favicon.ico`、`assets/favicon-32.png`、`assets/apple-touch-icon.png`、`assets/icon-192/512.png`、`site.webmanifest`、`images/og-latent-heat-2.jpg`（`site.og_image`，後台「預設分享縮圖」；換圖時用新檔名，臉書才會重新抓） |
| 圖片與影片檔 | `images/wix/`（新的 Wix 圖用 `scripts/download-images.sh` 下載） |
| 分享預覽（貼到臉書、LINE、IG 私訊等時出現的標題、小字與圖） | `build.py` 的 `layout()` 產生 `og:title`、`og:description`（就是頁面描述）、`og:image`（含寬高與替代文字）、`og:locale:alternate`；`og_image()` 把本機圖片轉成最長邊 1200px 的 JPEG 放在 `images/_og/`（因為 LINE 等不顯示 WebP），自動產生並一起 commit，不要手改。作品與工作坊的分享圖是自動做的卡片（`og_card()`：封面或 `share_image` 裁成 1200×630，下方深色漸層加 Minipax 標題與「Ting-Chun Liu · 年份」，存在 `images/_og/cards/<slug>-<雜湊>.jpg`，標題或圖換了就換檔名；需要 fonttools＋brotli 讀 Minipax）。網站小圖示（favicon、apple-touch-icon、icon-192/512）是 Latent Heat Generation 熱像中的一個顯示卡風扇。預覽小字的來源（都能在後台改）：首頁＝`site.description`；關於＝`about.bio`；每件作品＝`works[].summary`（留空用說明文字開頭）；每個工作坊＝`workshops[].summary`；作品列表、講座與工作坊、部落格、朋友頁＝`site.share_works`／`share_workshops`／`share_blog`／`share_friends`（+ `_de/_zh`，留空用 `UI` 的 `*_desc`，`build.py` 的 `share_text()`）。改了之後臉書要用 Sharing Debugger 重新抓才會更新；臉書新版貼文常只顯示圖、網域與標題，不一定顯示小字 |
| 作品頁圖片排版 | `works[].images` 第一張放大，其餘兩欄；某一行結尾加「 \| wide」（例如 `images/tokens/giraffe-hijack.webp | wide`）＝那張佔滿整寬，適合圖表與投影片，前後的圖照樣分組成兩欄（`build.py` 作品頁那段）。後台作品分頁的圖片欄也這樣寫 |
| 響應式小圖 | `images/_w/<寬度>/…webp`（480、960），由 `build.py` 的 `srcset()` 用 Pillow 自動產生並一起 commit，不要手改；原圖換了會自動重做 |
| GA 語言分組與問答事件 | `assets/analytics.js` 把頁面語言設成 `content_group`；`assets/chat.js` 的 `track()` 送 `chat_question`（不含問題文字）與 `chat_link`。改了要同步 Datenschutz 的 GA 段落 |
| 講座、工作坊與書寫頁（`/workshops/`，每個工作坊另有 `/workshops/<slug>/`；選單名稱 講座、工作坊與書寫／Talks, Workshops & Writing／Vorträge, Workshops & Texte） | `data/site.json` 的 `workshops[]`：`slug`、`title`、`summary`（卡片與頁首的一句話）、`text`（用 `# ` 分小標，`· ` 開頭的行當清單）、`with`、`held`（場次，每行一場，放在頁面最下方）、`images`（第一張是封面；可以是路徑字串，或 `{"src", "alt", "alt_de", "alt_zh"}`，後台一行寫成「路徑 | 說明 | DE | 中文」），除 `slug`／`with`／`images` 外都有 `_de/_zh`。這頁是在介紹「可以辦哪些工作坊」，辦在哪裡只放在 `held`。圖片放 `images/workshops/<slug>/`（見該資料夾 `README.md`）。頁面順序：引言 → 跳轉列 →「即將舉行」→「工作坊」卡片 → 講座錄影（`press[]` 的 `group: watch`）→「書寫」→「過往講座與工作坊」→ 聯絡。「即將舉行」與「近期場次」都來自 CV 的「Lectures, Talks & Workshops」區塊：CV 行的 `date`（YYYY-MM-DD，後台 CV 每行的第 6 欄）在建置日之後就算即將舉行，過往講座與工作坊是其餘最新 6 筆；「書寫」來自 CV 的「Publications & Writing」，是一欄的精簡列表（小預覽圖＋標題＋年份），預覽圖是 CV 行的 `thumb`（後台第 7 欄；留空時 `fetch-talk-thumbs.py` 在建置時抓該頁的 og:image）。頁首有跳轉列。工作坊、講座錄影、書寫都排成「小圖＋文字」的列，寬螢幕兩欄、窄螢幕一欄（`assets/style.css` 的 Talks, Workshops & Writing (3)），字級與卡片相同；手機上是小方圖，工作坊與講座的說明只顯示三行。所以場次與文章只在 CV 輸入一次。即將舉行的場次過期後，要等下一次重建才會移到近期（push 時會重建） |
| 講座錄影截圖 | `press[].thumb`；留空時 `build.yml` 會先跑 `scripts/fetch-talk-thumbs.py`，抓錄影頁的預覽圖（og:image）存到 `images/talks/` 並寫回 `site.json` |
| 圖片壓縮／轉檔 | `python3 scripts/compress-images.py [資料夾或檔案]`（預設 `images/workshops/`；需要 Pillow；長邊 2400px、JPEG 品質 82、移除 EXIF／GPS，PNG／HEIC 照片轉成 `.jpg`） |
| 後台 | `admin/index.html`、`admin/admin.js`；草稿預覽 `preview.html`（在瀏覽器用 Pyodide 跑同一個 `build.py`） |
| 自動化 | `.github/workflows/`：`build.yml`（重建網站）、`deploy-chat.yml`（部署問答 Worker）、`check-links.yml`（每月檢查連結）、`download-wix-images.yml` |

`assets/` 的 CSS/JS 由 `versioned()` 自動加上 `?v=<hash>`，改了檔案瀏覽器就會重新抓，不用手動改版本號。
（`build.py` 裡另有一個舊的 `asset()` 函式處理圖片網址，兩個不要混用或重新命名。）

## 翻譯

網站有三種語言：英文在根目錄（`/`），德文在 `/de/`，繁體中文在 `/zh/`。
德文版第一次開啟時，右下角會出現一次提醒「部分德文由人工智慧翻譯，可能有錯誤」（`UI` 的 `mt_note`／`mt_ok`，`assets/site.js` 用 localStorage 的 `mt-note` 記住已看過）。要暫時隱藏某個語言，把它加進 `build.py` 的 `HIDDEN_LANGS`（該語言每一頁會轉址到英文版，並從語言切換、hreflang、sitemap、`llms.txt` 拿掉），同時把 `scripts/wiki-sitemap.py` 的 `LANGS` 對應那一行拿掉。程式裡的語言代碼是 `en`、`de`、`zh`
（`LANGS`、`LP` 路徑前綴、`HREFLANG` 的 `zh` 對應 `zh-Hant`、`LOCALE` 的 `zh_TW`，都在 `build.py` 開頭）。

### 1. 內容：`data/site.json` 的 `_de` / `_zh` 欄位

同一個欄位加後綴就是翻譯，`build.py` 用 `tr(obj, key, lang)` 讀取：有 `key_de`／`key_zh` 就用，**空的或沒有就顯示英文**。

| 位置 | 英文欄位 | 翻譯欄位 |
|---|---|---|
| `site` | `description`、`statement`、`job_title`、`home_text` | `description_de/_zh`、`statement_de/_zh`、`job_title_de/_zh`、`home_text_de/_zh` |

`home_text` 是首頁下方的大字，留空時只留白不顯示（不會退回英文或 statement）；`statement` 只用在 JSON-LD、分享與 llms.txt，不顯示在首頁。
| `works[]` | `text`、`type`、`materials`、`status`、`tags`（主題標籤，list） | `text_de/_zh`、`type_de/_zh`、`materials_de/_zh`、`status_de/_zh`、`tags_de/_zh` |
| `press[]`（講座錄影與他人評論） | `note` | `note_de/_zh` |
| `performances[]`（作品頁下方的表演紀錄） | `note`、`title`（只在需要區分時，例如 Imaginary Landscape（表演版）） | `note_de/_zh`、`title_de/_zh` |
| `workshops[]` | `title`、`summary`、`text`、`held` | `_de/_zh` |
| `about` | `bio`（短，也是頁面描述與 JSON-LD）、`text`（較長的介紹，顯示在 bio 下方，空一行分段） | `bio_de/_zh`、`text_de/_zh` |
| `about.sections[]`（CV 區塊，順序即頁面順序：教學、獎項與獎助、展覽、講座、出版、學歷、表演、新媒體專案；頁首有跳轉列，標題放在列表上方、條目佔滿寬度；相鄰的短區塊（5 筆以內，例如教學與獎項）並排成兩欄（`build.py` 的 `CV_SHORT`）；超過 10 筆的區塊只先顯示 8 筆，其餘收進「顯示全部」） | `title` | `title_de/_zh` |
| `about.sections[].items[]`（CV 每一行：`year`、`text`、`url`、選填 `date`） | `text` | `text_de/_zh`；後台每行寫「年份 \| 內容 \| 連結 \| 中文 \| DE \| 日期 \| 類型 \| 預覽圖」；`date` 可寫 `TBA`（日期待定，也算即將舉行）；`kind` 是 `talk` 或 `workshop`，在近期場次標成「演講」「工作坊」，舊版後台只有前三欄、存檔會弄掉翻譯，已修正 |

注意：
- **作品標題不翻譯。** `works[].title` 各語言都一樣；`works[].title_zh` 不是翻譯，而是作品的中文名，三種語言的頁面都會顯示在英文標題旁。
  `site.name_zh`（劉庭均）也一樣。
- CV 行沒有翻譯時，`build.py` 會給那一行加 `lang="en"`，讓瀏覽器與搜尋引擎知道這段是英文。
- `works[].summary`（選填，+ `_de/_zh`）：搜尋結果與分享用的描述。只有作品文字開頭不適合當描述時才填（例如 Sixteen Tokens for a Cave 以 token 詩開頭）；沒填就用文字開頭。
- `works[].status`（例如 In development）顯示在作品卡與作品頁的「Status」列；留空就不顯示。
- `press[]` 的 `group` 只能是 `watch`（講座錄影，顯示在工作坊與講座頁）、`read`（他人引用或討論作品的文字，About 頁簡介下方、CV 之前的「引用與討論」／Cited and discussed，`#texts`）；展覽、活動、機構介紹頁不放；標題與來源不翻譯，沒有 `note_de/_zh` 時該語言顯示英文並標 `lang="en"`。
- 側邊欄：主選單只有 `NAV`（創作計畫、講座與工作坊、關於），部落格與朋友在側欄下方的小字（`FOOT`），都在 `build.py` 開頭。表演沒有獨立頁，是作品頁最下方深色的「表演紀錄」區塊（`#performances`），沒有引言；中文寫「音像演出」不寫「影音表演」。作品的 `type` 與卡片小字 `kw` 用同一套詞（兩者保持一致）；影像裝置中文寫「影像裝置」；舊的 `/performance/`、`/press/` 轉址到新位置。中文名稱在 `UI["zh"]["nav"]`；中文側邊欄用標題字體（`assets/style.css` 的 `html:lang(zh) .nav a`）。
- 聯絡信箱：邀約（工作坊、講座、合作、委託）一律給 Weimar 信箱：問答框（`worker/src/index.js` 的 `RULES`）、錯誤訊息 `ask_err`、`llms.txt`、wiki 都用 `site.email_alt`。`site.email`（側欄、Impressum、JSON-LD）維持 gmail；`site.email_alt`（Weimar 信箱）是 About 頁顯示的聯絡信箱（沒填就用 `site.email`）；`site.orcid`（只填 iD）有填才會在 About 頁出現，目前留空。`friends/` 頁刻意只有標題與卡片（沒有引言和主題）。頁尾沒有 HTML 網站地圖的連結（`/sitemap/` 仍在 `sitemap.xml` 裡）。
- **搜尋引擎（SEO）用語**：主要敘述是 “research-based media artist working with critical AI”（`site.description`、`statement`、About 的 bio 第一句）；看不到的地方（JSON-LD 的 `jobTitle`、`occupations`、`llms.txt`）用 “Critical AI Artist”；首頁 `<title>` 刻意只放名字。文字裡一律寫全名 Ting-Chun Liu。部落格文章的作者列寫 “Ting-Chun Liu, media artist”。
- 主題標籤：`works[].tags`（`_de/_zh` 沒填就顯示英文）顯示在作品頁的「Topics」列，也寫進 JSON-LD 的 `keywords`；各列表頁的標籤在 `build.py` 的 `UI[...]["tags"]`。
- `data/lastmod.json` 由 `build.py` 自動維護（每頁的內容雜湊與最後更新日），給 `sitemap.xml` 的 `<lastmod>` 用，不要手改。HTML 版網站地圖在 `/sitemap/`（`/de/sitemap/`、`/zh/sitemap/`），側欄頁尾有連結。
- **合作一律在最外層標出來**：作品卡片（`work_card()`，取 `collaborators` 分號前的部分）與工作坊卡片（`shop_card()`，`with`）都顯示「與 X 合作」，不只在內頁。新增合作作品或工作坊時一定要填 `collaborators`／`with`。
- 表演影片標題（除了上面說的區分用 `title_zh`）、合作者（`collaborators`）、年份、網址不翻譯。
- 新增一個要翻譯的欄位時：在 `site.json` 加 `xxx_de`/`xxx_zh`，在 `build.py` 用 `tr(obj, "xxx", L)` 讀，
  並在 `admin/admin.js` 加對應的輸入框（照 `text_de`、`type_zh` 那幾行的寫法），作者才能在後台編輯。
- 翻譯風格：德文用 Sie、性別中立寫法（`Künstler*innen`）；中文用繁體、台灣用語、全形標點，作品名用《》；中文裡能不用英文就不用：AI 一律寫「人工智慧」；技術詞用中文，長文裡第一次出現時括號附英文：回授（Feedback）、詞元（Token）、嵌入向量（Embedding）、強制登入頁面（captive portal），之後只寫中文。其他固定譯法：cybernetics 寫「模控論」、operational image 寫「操作性影像」、audiovisual performance 寫「音像演出」、prompt 寫「提示詞」。職稱、機構、活動保留原文括號，例如「講師暨藝術研究員（Künstlerischer Mitarbeiter）」「科隆媒體藝術學院（KHM）」「（39C3）」，但 TNUA 不加；博物館等不音譯，寫原文全名再括號附中文意思，例如 Rautenstrauch-Joest-Museum – Kulturen der Welt（科隆世界文化民族學博物館，RJM）。Storage Museum、Transformer 保留英文。保留英文的還有：作品與文章標題、人名、軟體與模型名稱（Stable Diffusion、CLIP、ChatGPT）、實驗裡實際輸入的英文字（giraffe、happy）。

### 2. 介面文字：`scripts/build.py` 的 `UI` 字典

`UI = {"en": {...}, "de": {...}, "zh": {...}}`，三個語言的 key 必須一樣。新增 key 時三個都要加，否則該語言的頁面建置時會出錯。
`%s`、`%d` 是程式填入的值（名字、年份、數量、網址），翻譯時要保留、數量相同。

問答框的字串也在這裡：
- `ask`（區塊的 aria-label）、`ask_ph`（輸入框提示：Ask me anything／Fragen Sie mich alles／問我任何事）、`ask_btn`
- `ask_note`：框下方的提醒。**只有德文版有 `· %s`**，會被換成 Datenschutz 的連結（`ask_more`）；英文、中文刻意沒有連結，不要加回去。
- `ask_ex`：範例問題（list，四個）；輸入框空著時，placeholder 會輪流顯示它們（`chat.js`），打字、focus 或在回答時暫停；減少動態效果時不輪播。區塊上方可見的標題用 `ask`
- `ask_err`（`%s` 會填 email）、`ask_busy`、`ask_refusal`：錯誤訊息，由 `chat.js` 顯示
- 介面用第一人稱（「問我」、「我的作品」），因為問答框代表藝術家本人。
- 問答框以外的中文介面文字與翻譯，少用第一人稱：寫「工作坊內容包含：……」，不寫「我開設的工作坊……」。
- 問答框的回答用「Ting-Chun」稱呼藝術家（中文用「庭均」或「劉庭均」），不要單獨用「Liu」；wiki 內文仍寫 Liu，規則在 `RULES`。不談個人隱私。

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
