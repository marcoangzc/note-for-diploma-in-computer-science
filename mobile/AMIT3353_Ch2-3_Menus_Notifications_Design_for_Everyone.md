# AMIT3353 — Chapter 2.3: Menus, Notifications and Design for Everyone
# 第 2.3 章：菜单、通知、多语言/多屏幕适配与无障碍（中英双语）

> The slides never say when to choose Toast vs Snackbar vs Notification, mix dp with pixels ("48 × 48 pixel" is wrong), and the string-array code does not match its own XML. This note gives decision rules, verified dp/px and colour-contrast numbers, and exam-ready answers for "support different languages/devices" and "notify the user".
> 中文：slide 没讲 Toast / Snackbar / Notification 该怎么选，触控目标写成「48 像素」（应该是 48dp），string-array 代码也对不上。这里补上选择规则、验算过的数字和考试答题模板。

---

## 0. One-sentence overview / 一句话总结

Give users **actions** (toolbar/menus), **feedback** (Toast, Snackbar, Notification), and make the app work for **everyone** — any language, screen and Android version — and for people with disabilities (accessibility).
中文：工具栏给操作、三种消息给反馈；再用「外部化资源」适配语言/屏幕/系统版本，并照顾有障碍的用户。

| Topic | Slides | Exam relevance |
|---|---|---|
| Menus, Toolbar, Up button | 3–14 | Purpose of menus |
| Toast, Snackbar, Notification | 15–21 | Oct 2025 Q2b, Jan 2026 Q2a |
| Languages | 24–33 | Oct 2025 Q2a (apply TWO methods) |
| Screens, cutouts, bitmaps | 34–52 | Oct 2025 Q2a |
| API levels | 53–58 | min/target SDK |
| Accessibility | 59–77 | "What is accessibility?" |

---

## 1. Menus and the Toolbar / 菜单与工具栏 (slides 3–14)

**English.** The app bar (Toolbar) shows the **title**, an optional **drawer/Up icon**, **action buttons** for the most important actions, and an **overflow menu (⋮)** for the rest (slide 4 figure).
**Why menus?** (slide 5) They give a consistent, familiar place for actions, save screen space (overflow hides rare actions) and provide navigation (drawer, Up).
**FIT scheme (slide 6)** to decide what becomes an action button: **F**requent, **I**mportant, **T**ypical. Frequent/important actions → `showAsAction="ifRoom"`; rarely used (Settings) → `"never"` (always in overflow) — slide 8 XML: "Mark favourite" ifRoom, "Settings" never.
**中文：** 常用/重要的放工具栏按钮，不常用的放「⋮」溢出菜单。

**Context-sensitive menu (slide 7, no explanation on slide):** appears when the user **long-presses or selects items** (figure: "2 selected", with delete/label/star actions). It offers actions that only make sense for the selected items — the toolbar temporarily turns into an "action mode" bar.

### Compose version (slides 9–10, 13)
```kotlin
Scaffold(topBar = { MyAppBar() }) { innerPadding -> Content(Modifier.padding(innerPadding)) }
```
- `TopAppBar(title, navigationIcon, actions)`: `navigationIcon` = the ☰ drawer or ← Up icon; `actions` = action buttons (`IconButton` + `Icon`).
- **`TopAppBar` must be placed inside a `Scaffold`** (slide 10) so Compose reserves space and passes `innerPadding` to the content.
- Always give an `Icon` a `contentDescription` (used by screen readers — see section 6).

### Up button (slides 12–14)
It brings the user back to the parent screen. Old XML way: a child Activity declares its **parent in the manifest**; Compose way: `navController.navigateUp()` in the `navigationIcon` (slide 13). Purpose (slide 14.2): "helps users find their way back to the app's main/parent screen" — never leaves the app (Ch 2.2).

---

## 2. Toast, Snackbar, Notification / 三种反馈 (slides 15–21) — EXAM

| | **Toast** | **Snackbar** | **Notification** |
|---|---|---|---|
| Where shown | Small popup over the screen | Bottom of your app's screen | **Outside** the app: status bar, notification drawer, heads-up |
| Action button? | No | **Yes** (one, e.g. UNDO) | Yes (reply, archive…) |
| Disappears | Automatically (~2 s short, ~3.5 s long; extra) | Automatically (or swipe) | **Stays** until dismissed or the cause is resolved |
| Needs app open? | Meant for while app is used | Yes | **No** — works when app is closed |
| Priority | Very low | Low | Medium |
| Typical use | "Copied to clipboard" | "Message deleted — UNDO" | "New message", "Update available", "Storage low" |

Analogy / 类比: Toast = a friend's quick nod; Snackbar = a waiter asking "Shall I undo that?" while you're still at the table; Notification = a letter through the door that waits until you read it.

**Code reading — Compose Snackbar (slide 18):** the Snackbar needs a `SnackbarHostState` shown by a `SnackbarHost` inside `Scaffold(snackbarHost = …)`. `showSnackbar()` is a **suspend function**, so it must be called inside a coroutine: `coroutineScope.launch { snackbarHostState.showSnackbar(message, actionLabel, duration) }` with `rememberCoroutineScope()`.
Toast (slide 16): `Toast.makeText(context, text, Toast.LENGTH_SHORT).show()` — needs a `Context`.
Notification (extra, not in slides): from Android 8 (API 26) a notification needs a **channel**, and from Android 13 (API 33) the user must grant the `POST_NOTIFICATIONS` runtime permission.

### Slide 21 answers
1. **Toast is better than a notification** when the message is short, immediate, only relevant while the user is in the app and needs no action or persistence (e.g. "Saved").
2. Notification or Snackbar?
   - a. Internal storage low → **Notification** (important, must persist, user must act, may happen when app closed).
   - b. A message has been deleted from Inbox → **Snackbar** (short, in-app, offers **UNDO**).
   - c. An update is available → **Notification** (timely info that can arrive while the app is closed).

### Exam templates
- **Oct 2025 Q2b "Demonstrate how MyGOV notifies users when a new update is available" (3 marks):** The app/server sends a **notification** (push message) that appears in the status bar/notification drawer with a short text ("MyGOV update available") and a tap action that opens the Play Store page; it stays until dismissed even when the app is closed.
- **Jan 2026 Q2a "TWO methods ELSA updates users after financing submission" (6 marks):** (1) **Snackbar/Toast** — immediate in-app confirmation "Application submitted" (Snackbar can add "VIEW STATUS"); (2) **Notification** — later status updates (approved / more documents needed) delivered even if the app is closed. (Optional third: a confirmation **dialog** or screen for critical confirmation.) Each method: what it looks like + why it suits this moment.

---

## 3. Design for Everyone (i): Languages / 多语言 (slides 22–33)

**Problem:** Android runs in many languages, screens and versions. **Technique:** *externalise resources* — keep strings, images, layouts, styles **outside the source code** so they can be swapped without touching code (slide 25).
```
res/
  values/strings.xml        <- default (English); also the fallback
  values-fr/strings.xml     <- French
  values-b+es+ES/...        <- Spanish (Spain), BCP 47 style
  mipmap/  mipmap-b+es+ES/  <- alternative image (e.g. a flag) per locale
```
Every file uses the **same string names** with different values (slide 30: `hello_world` → "Hello World!" / "Bonjour le monde !"). At run time Android uses the folder matching the device locale; if a string is missing there it falls back to the default `values/`.
Use it: `getString(R.string.hello)` (slide 32); in Compose `stringResource(R.string.hello)` (extra).
**中文：** 字符串写在 `strings.xml`，每种语言一个文件夹；系统按手机语言自动选；找不到就用默认文件夹。

Language codes (slide 31): `en`, `en_GB`, `en_US`, `zh`, `zh_CN`, `ms` = Bahasa Melayu. ⚠️ Slide says `in` = "Malay (Indonesia)": that is the legacy code for **Indonesian** (modern code `id`); Malay is `ms`.

⚠️ **Slide 33 does not match itself:** the XML defines `states_array` but the Kotlin uses `R.array.planets_array` and `Array` without a type, and the slide text says "R.string". Correct:
```xml
<string-array name="states_array"><item>Johor</item><item>Selangor</item></string-array>
```
```kotlin
val states: Array<String> = resources.getStringArray(R.array.states_array)  // R.array, not R.string
```
Beyond text (Ch 7 localisation): text length (German longer), right-to-left layouts (Arabic), images/colours with cultural meaning, date/currency formats.

---

## 4. Design for Everyone (ii): Screens / 多屏幕 (slides 34–52)

Android groups screens by **size** (small, normal, large, xlarge) and **density** (ldpi, mdpi, hdpi, xhdpi…). *Orientation is treated as a size variation* (slide 37).

### 4.1 Pixels, density and dp — verified numbers
`px = dp × (dpi ÷ 160)`. (Calculated with Python.)

| Bucket | dpi | Scale | 48 dp = | 8 dp = |
|---|---|---|---|---|
| ldpi | 120 | 0.75 | 36 px | 6 px |
| mdpi | 160 | 1.0 | 48 px | 8 px |
| hdpi | 240 | 1.5 | 72 px | 12 px |
| xhdpi | 320 | 2.0 | 96 px | 16 px |
| xxhdpi | 480 | 3.0 | 144 px | 24 px |
| xxxhdpi | 640 | 4.0 | 192 px | 32 px |
(Slide 35 lists only four buckets; xxhdpi/xxxhdpi exist on modern phones.)

Resolution names (slide 36): HD 720×1280 = 921,600 px; FHD 1080×1920 = 2,073,600 px (**2.25×** HD); QHD 1440×2560 = 3,686,400 px (**4×** HD). More pixels ≠ bigger screen; that is why we use **dp**, not px.

### 4.2 Alternative layouts (slides 37–42)
Same **file name**, different **folder**, different content: `layout/main.xml` (default portrait), `layout-land/main.xml`, `layout-large/…`, `layout-large-land/…`. The system picks the folder that matches the device; code just calls `setContentView(R.layout.main)`.
⚠️ Extra: the `large/xlarge` qualifiers are old; modern XML apps use **smallest-width** folders such as `layout-sw600dp`.
**Compose way (slide 41):** `WindowSizeClass` — `Compact` (< 600 dp width, phones), `Medium` (600–839 dp, small tablets/foldables), `Expanded` (≥ 840 dp) → choose `PhoneLayout()`, `TabletLayout()` or `DesktopLayout()` with `when`. (Breakpoints are from the Android docs; checked with a small script: 360→Compact, 600/720→Medium, 840/1024→Expanded.)

### 4.3 Cutouts, foldables
Notches/punch-holes (slides 43–47): from **Android 9 (API 28)** set `android:windowLayoutInDisplayCutoutMode` = `default`, `shortEdges` (content may extend into the cutout along short edges) or `never`. Foldables/tablets (slide 48): use Window Manager and `FoldingFeature` to react to the hinge.

### 4.4 Alternative bitmaps (slides 50–52)
Slide 52 shows the same letter "a": a low-resolution image blows up into blocky pixels on a dense screen. Provide one image per density: `drawable-mdpi`, `-hdpi`, `-xhdpi`… at scale **3 : 4 : 6 : 8** (ldpi : mdpi : hdpi : xhdpi). Example (calculated): a 100×100 px mdpi icon → 75, 100, 150, 200 px.
**Slide 58.3 comment — "to be compatible with all screen sizes, make the image in the best quality possible":** *Partly wrong.* One huge image looks fine on a big screen but wastes memory on small ones: a 4000×3000 ARGB_8888 bitmap = **45.8 MiB** in memory, whereas scaled to ¼ (1000×750) it is **2.86 MiB** (16× less; calculated). Better: supply density-specific versions (or vector drawables) and decode/scale to the view size.

---

## 5. Design for Everyone (iii): Android versions / 系统版本 (slides 53–57)

- `minSdkVersion` = **lowest** API level your app supports (below it, Play will not install it).
- `targetSdkVersion` = **highest** API level you have designed and tested for; the OS then applies that version's behaviour.
- In `build.gradle`: `minSdkVersion 16` (support more devices), `targetSdkVersion 30` (use latest features) — slides 55–56.
**Slide 58.4 — why set min lowest and target latest?** Min as low as your code allows → reaches the **most devices/users**; target latest → gets the newest features, security and behaviour, and Google Play requires new apps to target a recent level (check the current requirement; extra).
**Runtime check (slide 57):** `if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) { use newer API } else { fallback }` — so one APK works on old and new phones. (The slide's HONEYCOMB example is very old; the idea is what matters.)

### Exam template — "Apply TWO methods to serve different races and the wide variety of devices" (Oct 2025 Q2a, 10 marks)
1. **Multi-language resources** (races/languages): keep all UI text in `res/values/strings.xml` plus `values-ms`, `values-zh`, `values-ta`; Android chooses by device locale, so one app serves Malay, Chinese, Tamil and English users; add locale-specific images/formats where needed.
2. **Alternative layouts/bitmaps and API-level handling** (devices): `layout-land`, `sw600dp` or `WindowSizeClass` for phones vs tablets; density-specific drawables; `minSdk` low and runtime `SDK_INT` checks so old phones still work.
Write: *what it is → how MyGOV uses it → benefit* for each (5 marks each).

---

## 6. Accessibility / 无障碍 (slides 59–77)

**Definition (slide 76.1):** design so that users, **regardless of ability**, can navigate, understand and use the app. **Why important:** inclusion (vision, hearing, motor, cognitive, age), legal/ethical duty, larger market, and it improves usability for *everyone* (e.g. big buttons help in a moving bus).
Three areas: **Navigation, Readability, Guidance & feedback.**

| Area | Rule | How |
|---|---|---|
| Navigation | Support screen readers | Label controls: `contentDescription` (XML `android:contentDescription`, Compose `contentDescription = "Share"`); group related items (`screenReaderFocusable`) |
| | Easy navigation | Support keyboard/gesture input; **nothing that fades out after a time**; flat structure (slide 62: one parent with 5 children beats a deep tree) |
| | Large touch targets | **48 dp × 48 dp**, at least **8 dp** between targets |
| Readability | Contrast; do not rely on colour alone | Add icon/text (✓ Going / ✗ Can't go, slide 69) |
| | Media | Pause/stop controls; captions/transcripts |
| Guidance | Clear controls | Text labels, tooltips, placeholder; consistent naming |

⚠️ **Slides 63–64 say "48 × 48 pixel".** The guideline is **48 dp**. Verified: 48 px on an xxhdpi phone (3×) is only **16 dp** (tiny), whereas 48 dp = 144 px there (table in 4.1).

### Colour contrast — worked examples (calculated with the WCAG formula)
Rule of thumb (WCAG, extra): ≥ **4.5 : 1** for normal text, ≥ **3 : 1** for large text.
| Text on background | Ratio | Normal text |
|---|---|---|
| Black on white | 21.00 : 1 | Pass |
| Grey #767676 on white | 4.54 : 1 | Pass (just) |
| Light grey #AAAAAA on white | 2.32 : 1 | **Fail** |
| White on green #4CAF50 | 2.78 : 1 | **Fail** |
| White on dark green #2E7D32 | 5.13 : 1 | Pass |
| Red #FF0000 on green #00FF00 | 2.91 : 1 | **Fail** (and unreadable for red-green colour blindness) |

Colour blindness (slides 70–72): **deuteranopia / protanopia** (red-green) confuse red and green; **tritanopia** (blue-yellow). Slide 72's "YES=green / NO=red" pair becomes yellow/brown for deutan/protan users → add text or icons.

### Touch zones and gestures (slides 65–68)
The thumb reaches the lower-middle of the screen easily (green), the top and far corners with effort (orange/red); bigger phones (slide 66, 4″→6″) have a bigger hard zone. → Put primary actions (bottom bar, FAB) in the easy zone; destructive/rare actions in the hard zone.
Gesture navigation (Android 10 / API 29): extend content **edge-to-edge** (transparent status/navigation bars, slide 68) and avoid **conflicting gestures** (e.g. a horizontal swipe in your UI vs the system Back swipe).

### Slide 76–77 answers
- **76.2 Desktop vs mobile navigation:** desktop has a large screen, mouse hover, keyboard, visible multi-level menus; mobile has a small touch screen, thumb reach, no hover, so it uses hidden menus (drawer/overflow), bottom navigation, gestures and flat hierarchies.
- **76.3 Role of colour:** identity/branding, visual hierarchy (draw attention), state and feedback (error/success), readability via contrast — but never the only way to convey information.
- **77 Identify space (Facebook screens):** top = status bar + search/title bar + top tab bar (navigation); middle = scrollable feed/photo grid (content); bottom = action row (Status / Photo / Check-in) and bottom navigation bar (navigation).

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 63–64 | Touch target 48×48 **pixel** | 48 **dp** (px depends on density) |
| 31 | `in` = Malay (Indonesia) | `in`/`id` = Indonesian; Malay = `ms` |
| 33 | `R.string.<name>` for arrays; names mismatch | `R.array.states_array`, typed `Array<String>` |
| 35 | four density buckets | also xxhdpi, xxxhdpi in real devices |
| 38–40 | `layout-large` | Old qualifier; modern: `sw600dp` |
| 57 | HONEYCOMB example | Old API; use current version constants |
| 11–13 | XML `showAsAction` + Compose mixed | Two systems for the same thing — know both terms |

Exam strategy: quote dp (not px) for touch targets; if a question uses the slide's "pixel", mention dp.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| FIT | Frequent, Important, Typical — decide toolbar actions |
| `showAsAction` | `ifRoom` / `never` (overflow) |
| Toast / Snackbar / Notification | quick popup / in-app bar with action / outside app, persistent |
| Externalise resources | Keep strings/images/layouts outside code |
| `values-xx/strings.xml` | String file per language; default is `values/` |
| `px = dp × dpi/160` | Density conversion |
| `minSdk` / `targetSdk` | Lowest supported / highest tested API |
| `SDK_INT` | Runtime API level check |
| Touch target | 48 dp, gap ≥ 8 dp |
| Contrast | ≥ 4.5:1 normal, ≥ 3:1 large text |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which message can carry an UNDO action and disappears automatically? (a) Toast (b) Snackbar (c) Notification (d) Dialog
2. Where is a French `hello_world` string stored? (a) `res/values/strings.xml` (b) `res/values-fr/strings.xml` (c) `res/fr/values.xml` (d) `assets/fr.txt`
3. 48 dp on a 320 dpi phone equals… (a) 48 px (b) 72 px (c) 96 px (d) 144 px
4. `targetSdkVersion` means… (a) lowest API supported (b) highest API you tested against (c) API of the emulator (d) screen size
5. Which colour combination fails the 4.5:1 rule? (a) black/white (b) white/#2E7D32 (c) white/#4CAF50 (d) #767676/white

### B. Short answer
1. Explain "externalise resources" and why it helps localisation.
2. Give two accessibility rules for touch targets/navigation.
3. When should you use a Notification rather than a Snackbar?

### C. Calculation / trace
1. A 24 dp icon: how many pixels on ldpi, mdpi, hdpi, xhdpi, xxhdpi?
2. A 2000×1500 photo is loaded ARGB_8888 (4 bytes/pixel) into a 500×375 view. Memory for full size vs `inSampleSize = 4`?
3. Device locale = Tamil, but the app only has `values/` and `values-ms/` folders. Which strings are shown? What if the `values-ms` file lacks `title`?

### D. Thinking
1. Write the 10-mark answer for "Apply TWO methods to serve different races and devices" for a banking app.
2. Evaluate: "A red 'No' button and green 'Yes' button are enough to show which is which."

### Answers
**A.** 1-b. 2-b. 3-c (48 × 320/160 = 96). 4-b. 5-c (2.78:1).

**B.**
1. Store text/images/layouts outside source code (`res/`), one copy per locale/screen; the system picks the right one at run time, so adding a language means adding a file, not editing code.
2. Touch targets ≥ 48 dp with ≥ 8 dp spacing; label all controls with `contentDescription`; do not use elements that disappear after a time.
3. When the message must be seen even if the app is closed, must persist, or is timely/important (update available, storage low).

**C.**
1. 24 × 0.75 = 18 px (ldpi); 24 (mdpi); 36 (hdpi); 48 (xhdpi); 72 (xxhdpi).
2. Full: 2000 × 1500 × 4 = 12,000,000 B ≈ 11.44 MiB. `inSampleSize = 4` → 500 × 375 × 4 = 750,000 B ≈ 0.72 MiB (16× smaller, matches the view size).
3. No Tamil folder → falls back to the **default `values/`** (English) — not Malay. A missing `title` in `values-ms` falls back to the default `values/` string for that key.

**D.**
1. Use the template in section 5: (1) multi-language string resources (`values-ms/zh/ta`) and locale-aware formats; (2) alternative layouts/bitmaps + `WindowSizeClass` + low `minSdk` with `SDK_INT` checks. Each: what → how in the banking app → benefit.
2. Not enough: red/green look alike to red-green colour-blind users (also 2.91:1 contrast). Add text ("Yes"/"No"), icons and sufficient contrast.

---

## Links to other chapters / 与其他章节的联系
- Layouts, themes, Material components → **Chapter 2.1**; Up button/back stack → **Chapter 2.2**.
- Notification via alarms/services → **Chapters 1 and 4.2**; localisation & distribution → **Chapter 7**.
- Scaled bitmap decoding → **Chapter 6**.
