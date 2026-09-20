# AMIT3353 — Chapter 7: Mobile Application Packaging, Publication and Monetisation
# 第 7 章：应用打包、发布与变现（中英双语）

> The slides are mostly pictures and one-line bullets, and several facts are now out of date: **Google Play Instant was shut down in December 2025**, **Windows Subsystem for Android ended on 5 March 2025**, and the "150 MB + 2 GB expansion" size rule belongs to the old APK model (App Bundles have a 200 MB base-module limit and no expansion files). This note explains each step of the launch checklist, flags what is outdated (verified by web search), and gives model answers for the distribution and monetisation questions that appear in both past papers.
> 中文：这一章 slide 大多是图片和一句话要点，而且有几处已经过时：**Google Play Instant 已在 2025 年 12 月停用**，**Windows 的 Android 子系统 2025 年 3 月已终止**，「150 MB + 2 GB 扩展包」是旧 APK 时代的规则。这里逐步解释发布流程，标出过时内容，并给出两份历年试卷都考的「发布渠道」和「变现模式」答题模板。

---

## 0. One-sentence overview / 一句话总结

Before release you plan a **launch checklist** (policies, developer account, localisation, device compatibility, alpha/beta testing, store listing), **sign** the app with your own key, choose a **distribution channel and method** (marketplace, App Bundle, Android Go, …), and decide how the app earns money (**monetisation**).
中文：发布前要走清单（政策、开发者账号、本地化、兼容性、测试、商店页面）→ 用自己的密钥签名 → 选发布渠道/方式 → 决定赚钱模式。

| Topic | Slides | Exam relevance |
|---|---|---|
| Launch checklist | 3–24 | Localisation, testing terms |
| Preparing for release, signing | 25–28 | Signing steps, why the same key |
| Store listing, distribution channels | 29–32 | Oct 2025 Q4c(i) (channel, 5 marks) |
| Android Go, App Bundles, Play Instant, Chrome OS | 33–48 | Jan 2026 Q4b(i) (App Bundles, 4 marks); review questions |
| Monetisation | 50–60 | Oct 2025 Q4c(ii); Jan 2026 Q4b(ii) (5 marks each) |

---

## 1. Launch checklist / 发布检查清单 (slides 3–24)

### 1.1 Developer Program Policies (slides 3–4)
Rules of the store you publish on. Five areas: **restricted content, intellectual property, privacy and security, monetisation and ads, store listing and promotion.** Breaking them gets the app rejected or removed.

### 1.2 Developer account (slides 5–13)
A **developer account** is the publishing account issued by the platform provider; it lets you post, display, sell and distribute apps.
| Platform | Fee (slide 7) |
|---|---|
| Google Play | **USD 25, one-time** |
| Apple App Store | **USD 99 per year** |
| Huawei AppGallery, KaiOS, Tizen | Free of charge (FOC) per the slide |
**Google Play Console** (slides 8, 11–13): shows your apps, installs, ratings, last update and status; earn money with paid apps or in-app products; reports installs **by app version** and **by country** (slides 12–13 charts). (USD 25 and USD 99 are the well-known current fees; the free-of-charge stores are as stated on the slide.)

### 1.3 Localisation / 本地化 (slides 14–18)
**Localisation** = adapting an app to a language, culture or region so it looks as if it was made there. Slide examples:
| Slide | Example | Lesson |
|---|---|---|
| 16 | TED app in English vs German | German text is longer, so buttons/titles can be **truncated** ("Lassen Sie…") — design flexible layouts |
| 17 | Three pictures: person lying in the desert → drinking a cola → standing happy | Meaning depends on **reading direction**: read right-to-left (Arabic), the story reverses (drinks, then collapses) — adapt images |
| 18 | Job app in English vs Arabic | **Right-to-left (RTL)** layout: whole UI is mirrored |
Also localise date/currency formats, colours and symbols. (Technique = string resources and alternative resources, Ch 2.3.)

### 1.4 Device compatibility (slides 19–20)
Make sure the app runs well across devices of different hardware, software and OS versions: screen sizes/densities, min/target SDK, `uses-feature` filters. ⚠️ Slide 19 says "(Chapter 3)"; the material is in **Chapter 2.3** (design for everyone).

### 1.5 Quality test: alpha and beta (slides 21–23)
Quality test = techniques to prevent problems and make sure the app meets standards. Slide 23 shows three nested circles:
| Stage | Who tests | Purpose |
|---|---|---|
| Developers' testing | The team | Fix obvious bugs |
| **Alpha** | Small trusted group (staff/testers) | Early full-feature test, find major problems |
| **Beta** | Larger group of real outside users | Real-world use, devices, feedback before public launch |
(On Google Play these are the closed and open testing tracks — extra.)

### 1.6 Store listing (slide 29)
Title/description/screenshots plus: **distribution** (countries), **app size**, **platforms**, **free or paid**. ⚠️ The slide's "app size < 150 MB + expansion up to 2 GB" is the **old APK rule**: with **Android App Bundles the base module limit is 200 MB (compressed download size) and expansion (`.obb`) files are not supported** — large game assets use Play Asset Delivery (verified on Google's developer/support pages).

---

## 2. Preparing for release and signing / 签名 (slides 25–28)

A release build must be a **signed APK/bundle** so Android and the store can verify who made it and that it is unchanged.
**Minimum requirements (slide 26):** (1) cryptographic keys, (2) application icon, (3) End-User License Agreement (EULA), (4) promotional/marketing materials.
Analogy / 类比: your **private key = your personal seal**; the **signature = the seal impression** stamped on the app. Only the owner of the seal can make a valid impression, so users and Google can trust that an update really comes from you.
⚠️ Slide 26 says "cryptographic key: digital signature"; more exactly, the **private key creates the signature** and the certificate holds the matching public key.

**Steps (slide 27):** create a **key store** (the file that holds keys) → create a **private key** → **build** the project → **sign** the app.
**Why the key matters (slide 28):**
| Consideration | Meaning |
|---|---|
| **Update** | A new version must be signed with the **same key** as the installed one, otherwise Android refuses the update |
| **Modularity** | Modules/apps signed with the same key can work together |
| **Code/data sharing** | Apps with the same signature can be allowed to share code/data (permissions by signature) |
Worked trace: v1.0 signed with key K1 (published) → v1.1 signed with K1 → installs as an update ✔ → v1.2 signed with a new key K2 → **rejected** (signatures don't match). **Lose the key = cannot update** the same app (Play App Signing lets Google keep the app-signing key — extra).

---

## 3. Distribution channels and methods / 发布渠道与方式 (slides 31–48)

### 3.1 Channels (slide 32)
| Channel | Description | Pros | Cons |
|---|---|---|---|
| **Marketplace** (Google Play, App Store, AppGallery…) | Official store | Trusted, security-scanned, discoverable, automatic updates, payments, analytics | Store fee/commission, policy review |
| **Email** | Send the APK file | Easy for a few testers | Insecure, user must allow "unknown sources", no updates |
| **Website/server** | Download link | Full control, no store fee | Users must trust the site, manual updates, harder to reach users |

**Exam template — Oct 2025 Q4c(i) "Analyse ONE distribution channel the government uses for MyGOV, with reasons" (5 marks):**
Channel: **marketplace (Google Play / App Store / AppGallery)**. Reasons: (1) **trust and security** — apps are checked and users know the app is the official one (important for a government app handling IDs and payments); (2) **wide reach** — almost every citizen already uses the store; (3) **easy updates** — the store pushes new versions automatically; (4) built-in analytics/ratings. Contrast briefly with email/website (unsafe, no auto-update). Write *what → why → benefit*.

### 3.2 Four distribution methods (slide 33)
| Method | What it is | Key facts (from the slides) |
|---|---|---|
| **Android Go** | Optimising for entry-level phones | Target Oreo (API 26); app size < 40 MB; RAM use < 50 MB (apps) / 150 MB (games); start in < 5 s |
| **App Bundles** | Publishing format for Google Play | Upload compiled code + resources; APK generation and signing are **deferred to Google Play**; **Dynamic Delivery** builds an APK for each user's device configuration |
| **Google Play Instant** | Run a native app without installing | Started from a URL; an upgrade to your existing app; Android 5.0 (API 21)+; supported by App Bundles; **Try** (in Play Store) and **Instant Play** (full game); size ≤ 15 MB; disadvantages: subset of APIs, size limit |
| **Chrome OS / PC / Mac** | Run mobile apps on other devices | Chrome OS supports Play Store apps; add `<uses-feature android:name="android.hardware.touchscreen" android:required="false"/>` so touchscreen-less Chromebooks can install; Windows and Apple-silicon Macs (slides 45–48) |

⚠️ **Outdated items (verified by web search, September 2026):**
- **Google Play Instant** — Google announced that from **December 2025 Instant Apps can no longer be published and the APIs stop working**; the slide's benefits/limits are historical. Answer exam questions as the slide does, but know the feature is discontinued.
- **Windows Subsystem for Android / Amazon Appstore on Windows** (slide 46) — Microsoft ended support on **5 March 2025**.
- **App size** — App Bundles: base module 200 MB compressed download size; no `.obb` expansion files (see 1.6).
- Android Go targets on the slide are as given by the lecturer; check Google's current Go requirements before quoting elsewhere (not verified).

### 3.3 App Bundles and Dynamic Delivery — explained
**English.** With an APK you ship *everything* (all screen densities, all languages, all CPU types) to *everyone*. With an **App Bundle** you upload one file; Google Play generates **optimised APKs** and each user downloads only the code and resources for **their** phone (their screen density, language, CPU architecture) — this is **Dynamic Delivery**.
中文：传统 APK = 把所有资源都塞给所有人；App Bundle = 你上传一份，Google Play 按每部手机的屏幕密度/语言/CPU 生成专属安装包，用户只下载自己需要的部分。

### Worked example — Review question 3 (5 marks): app > 100 MB because it carries normal *and* high-resolution art
Problem: one APK contains both art sets, so every phone downloads both. Illustrative sizes (chosen to add to 100 MB): code and shared resources 12 MB, normal art 38 MB, high-res art 50 MB.
| Delivery | Phone (normal screen) downloads | Tablet (high-res) downloads |
|---|---|---|
| Single APK | 12 + 38 + 50 = **100 MB** | **100 MB** |
| App Bundle (Dynamic Delivery) | 12 + 38 = **50 MB** | 12 + 50 = **62 MB** |
**Solution:** publish as an **Android App Bundle** so Google Play splits the resources by density; if some art is only needed later, use **feature modules / asset delivery** for on-demand parts. **Justify:** smaller downloads (faster installs, less mobile data, fewer abandoned installs), no extra maintenance (one upload), and the 100 MB APK problem disappears.

### Review questions 1–2
1. **Benefits of Instant App (slide's view):** try the app **without installing** (lower friction), launch from a URL or the Play Store "Try now" button, quick discovery and higher chance of converting to a full install, small and fast. (Now discontinued.)
2. **Main benefit of Dynamic Delivery:** each device gets only the code/resources it needs → **smaller download and install size**.

### Exam template — Jan 2026 Q4b(i) "Justify TWO reasons App Bundles suit distributing ELSA to SMEs" (4 marks)
1. **Smaller, device-specific downloads** — SME owners often use mid-range phones and limited mobile data; Dynamic Delivery sends only what their phone needs, so installation is faster and cheaper.
2. **Modular/on-demand delivery** — ELSA's training and learning modules can be delivered as optional feature modules, keeping the first install light while still offering rich content; also one upload covers all device types and Google Play handles signing and optimisation.
Each reason: *reason → how App Bundles do it → benefit for ELSA users*.

---

## 4. Monetisation / 变现模式 (slides 50–60) — EXAM

| Model | How the app earns | Best for | Examples |
|---|---|---|---|
| **Premium (paid)** | Pay once to download; may add in-app billing | Extensive features or a **narrow niche** with users who value it | Professional tools |
| **Freemium** | Free app; sells **digital goods** via in-app billing: **durable** (bought once, kept — e.g. remove ads, a skin) and **consumable** (used up — e.g. coins) | Games, apps with optional extras | PUBG Mobile |
| **Subscription** | Free trial, then a recurring fee through in-app billing | Ongoing content/service | Streaming, learning platforms |
| **Ads** | Free; shows ads via **AdMob + Google Mobile Ads SDK** | Large audiences, casual use | Free games, news |
| **E-commerce** | Free app selling goods/services (B2C); income from sales, **commissions + setup fees**; needs technology, logistics and payment solutions | Retail/marketplace | Shopping apps |
| **Rewarded products** | Users share content or do simple tasks (scan a QR, answer a survey) and get rewards; advertisers/researchers pay | Engagement-driven | 8coin, GigaGigs, Google Opinion Rewards |
| **Service** | Free app that is an **extension of a physical/online service** | Banks, telcos, government | Telco/bank apps |
| **Data collection / partnership / affiliate** | Free; provides customer service, promotion, giveaways, partners' offers | Brands and platforms | Partner-driven apps |

### Question 7.3 (slide 60) — suggested answers (justify each)
| App | Suitable model | Reason |
|---|---|---|
| a. PUBG Mobile | **Freemium** (+ ads) | Free download; earns from in-app purchases of skins (durable) and currency (consumable) |
| b. MyDigi (telco app) | **Service** | Free extension of the telco's online services (top-up, bills) |
| c. WhatsApp | **Data collection/partnership (business messaging) or service** | Free consumer app; revenue comes from business/partner services, not from users |
| d. Touch 'n Go eWallet | **Service + partnership/e-commerce** | Extension of a payment service; income from merchant fees/partner offers |
(Several answers can be correct — marks come from a clear justification.)

### Exam templates (5 marks each)
**Oct 2025 Q4c(ii) — MyGOV Malaysia:** **Service model** — a free extension of existing government services. Explain: citizens download free; the government benefits from cost savings (fewer counter visits, faster processing); any income comes from service/payment fees processed through FPX/Touch 'n Go, not from ads or upfront prices. Why not others: ads would reduce trust and clutter sensitive tasks; premium/paid would exclude citizens.
**Jan 2026 Q4b(ii) — ELSA:** **Freemium (with the bank's service revenue)** — free download with basic AI diagnostics and learning modules for all 10,000 SMEs; optional paid **premium** content (advanced reports, extra training, priority advice) via in-app billing or subscription; the bank also earns from financing applications made through ModalNiaga (service extension). Describe: how users pay, who pays, why it fits SMEs (low entry barrier, upsell when value is proven).
Structure: **name the model → how the money comes → why suitable for this app → one limitation.**

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 29 | App size < 150 MB + expansion up to 2 GB | App Bundle: base ≤ 200 MB, no expansion files |
| 38–42 | Google Play Instant benefits/limits | **Discontinued Dec 2025** |
| 46 | Microsoft Store hosts Android apps | Windows Subsystem for Android ended 5 Mar 2025 |
| 19 | Device compatibility "(Chapter 3)" | Covered in Chapter 2.3 |
| 26 | Cryptographic key = digital signature | Private key creates the signature |
| 34 | Android Go figures | As given; verify current Go requirements before quoting elsewhere |
| 30, 49, 59 | "Question 7.1/7.2/7.3" with only a picture/QR code | The QR code on slide 30 could not be decoded here; answers to 7.3 are in section 4 |

Exam strategy: if a question asks about Instant Apps or Windows apps, answer from the slide, but mention modern status only if the question asks for current trends.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| Developer account | Publishing account (Google USD 25 once; Apple USD 99/year) |
| Localisation | Adapt language, culture, layout direction, images, formats |
| Alpha / beta | Small trusted testers / larger real users |
| Key store / private key | File holding keys / secret used to sign |
| Same key | Required for updates and signature-based sharing |
| App Bundle / Dynamic Delivery | One upload; Play builds per-device APKs |
| Android Go | Lightweight apps for entry-level phones (< 40 MB, fast start) |
| Play Instant | Run without install (discontinued Dec 2025) |
| Premium / Freemium / Subscription / Ads | Pay first / free + purchases / recurring / advertising |
| Service, e-commerce, rewarded, data/partnership | Alternative models |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which fee structure is correct? (a) Google USD 99 once, Apple USD 25/year (b) Google USD 25 once, Apple USD 99/year (c) Both free (d) Both USD 25/year
2. Why must v2 of your app be signed with the same key as v1? (a) Faster build (b) Android accepts it as an update (c) Smaller size (d) Required for ads
3. What does Dynamic Delivery do? (a) Encrypts the app (b) Sends each device only the code/resources it needs (c) Speeds up the network (d) Adds ads
4. "Free download, then users buy coins" is… (a) Premium (b) Freemium (c) Subscription (d) Rewarded
5. Which is a valid benefit of publishing through a marketplace? (a) No review (b) Automatic updates and trust (c) No policies (d) Unlimited app size

### B. Short answer
1. Explain alpha and beta testing.
2. Give two reasons for localising an app.
3. Give two disadvantages of distributing an APK by email.

### C. Trace / calculation
1. A 90 MB app = 10 MB code + 30 MB normal art + 50 MB high-res art. Download size for a normal-screen phone with an App Bundle vs a single APK? By what percentage does it fall?
2. Signing trace: v1 signed with K1, v1.1 signed with K1, v1.2 signed with K2. Which updates install?
3. Match: (a) telco top-up app, (b) mobile racing game with paid cars, (c) meditation app with 7-day free trial, (d) newspaper app funded by banners.

### D. Thinking
1. Oct 2025 Q4c style: analyse ONE distribution channel for a government app and explain the monetisation model.
2. Should a language-learning app choose Premium, Freemium or Subscription? Justify.

### Answers
**A.** 1-b. 2-b. 3-b. 4-b. 5-b.

**B.**
1. Alpha: early test with a small trusted/internal group to find major bugs. Beta: broader test with real outside users on many devices to collect feedback before public release.
2. Reach and satisfy users in other languages/cultures; avoid truncated text/RTL problems and culturally wrong images; higher installs and ratings.
3. Insecure (users must allow unknown sources and may get tampered files) and no automatic updates/analytics.

**C.**
1. Bundle: 10 + 30 = **40 MB**; single APK: **90 MB**; reduction = 50/90 ≈ **55.6 %** (arithmetic checked).
2. v1.1 installs as an update (same key K1); v1.2 is rejected (different key K2).
3. (a) Service, (b) Freemium (consumable/durable items), (c) Subscription with free trial, (d) Ads.

**D.**
1. Use section 3.1 and 4 templates (marketplace + Service model).
2. Subscription (or Freemium with subscription): learning is ongoing and content updates regularly; a free trial lets users see value; a one-off Premium price would limit reach and give no income for new lessons.

---

## Links to other chapters / 与其他章节的联系
- Alternative resources, min/target SDK, localisation techniques → **Chapter 2.3**.
- Manifest features/permissions and signing basics → **Chapters 1, 5, 6**.
- Server, BaaS and cloud costs → **Chapter 4.2**; storage limits → **Chapter 4.1**.
