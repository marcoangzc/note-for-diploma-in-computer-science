# AMIT3353 — Chapter 1: Introduction to Mobile Application Development
# 第 1 章：移动应用开发简介（中英双语）

> The slides list the four components and the manifest in one line each, never say *why* Android is built this way, and contain a few wrong or dated facts (Super Mario is not a Sega game, `sharedUserId` is deprecated, permissions are not all runtime). This note adds the reasons, small examples, and exam-ready answer templates.
> 中文：slide 只给了定义，没讲「为什么这样设计」，还有几处错误/过时的地方。这份笔记补上原因、例子和可直接用于考试的答题模板。技术名词全部保留英文。

---

## 0. One-sentence overview / 一句话总结

Android apps are built from four kinds of components (Activity, Service, Broadcast Receiver, Content Provider) that are started by **Intents**, declared in the **Manifest**, and run inside a per-app **security sandbox**; the chapter also surveys app types, OSes and the four hardware limits of phones.
中文：Android app = 4 种组件 + Intent 启动 + Manifest 声明 + 沙盒隔离；另外还介绍 app 类型、手机系统和手机的四大硬件限制。

| Topic 主题 | Slides | Exam relevance 考试相关 |
|---|---|---|
| Native / Web / Hybrid 三种 app | 5–7 | Compare table, choose for scenario |
| Languages & tools 语言与工具 | 8–12 | Names only |
| Mobile OS 手机操作系统 | 13–21 | Oct 2025 Q1a (choose 2 OS and justify) |
| Key challenges 四大挑战 | 22–25 | Jan 2026 Q1a(i) (4 challenges, 12 marks) |
| Beyond mobile apps 移动之外 | 26–31 | Jan 2026 Q1a(ii) (AI in the app) |
| Sandbox & permissions 沙盒与权限 | 32–42 | "Explain two ways Android protects data" |
| ABCS components 四大组件 | 43–51 | Scenario matching |
| Intent, Manifest, Resources | 52–60 | "Why is the manifest important?" |

---

## 1. Types of mobile apps / 三种 app 类型 (slides 5–7)

**English.** A *native* app is written for one OS with that OS's language and tools (Kotlin/Java for Android, Swift for iOS). A *mobile web* app is a website opened in the phone browser. A *hybrid* app is web content (HTML/CSS/JS) wrapped inside a thin native shell so it can be installed from a store.
**中文：** Native = 为某个系统专门写；Mobile web = 用浏览器打开的网站；Hybrid = 网页技术 + 原生外壳（能上架 app store）。

Analogy / 类比: native = a tailor-made suit (fits perfectly, costs more, one per person); mobile web = a rental suit shop that everyone can walk into (no store install needed, but limited fit); hybrid = a ready-made suit with a small tailor adjustment. *(The analogy stops at performance: hybrid is not "half as fast" — it is limited by the WebView.)*

| | Native | Hybrid | Mobile Web |
|---|---|---|---|
| Cost 成本 | High | Low | Low |
| Performance 性能 | Fast | Lower than native (runs in a WebView) | Lower; needs network |
| Distribution 发布 | App stores | App stores | None (just a URL) |
| Device features 硬件功能 | Wide | Limited (via plugins) | Very limited |
| Code maintenance 代码维护 | One codebase **per OS** | Single codebase | Single codebase |

### Worked example — slide 7 question (with reasoning) / 例题

| Entity | Best choice | Reason (write this in the exam) |
|---|---|---|
| a. Bernama (news agency) | **Mobile web** (or hybrid if push alerts in a store app are wanted) | Mostly text/images that change all day; wide reach on any device via a URL; cheap to update in one place |
| b. Super Mario Bros (game) | **Native** | Needs fast graphics, touch/tilt input and offline play; games are the classic native case |
| c. Setapak Central (shopping mall) | **Hybrid** | Mainly information (directory, promotions) so one codebase is enough, but the mall wants a store presence, push notifications and maybe camera/QR for coupons |

⚠️ **Common confusion:** "hybrid = performance depends on network" (slide 6) is a simplification. A hybrid app ships its web files inside the app, so it can work offline; the real limit is WebView speed, not the network.

---

## 2. Programming languages and tools / 语言与工具 (slides 8–12)

| Kind | Languages | Tools |
|---|---|---|
| Native (Android) | Kotlin, Java, C/C++ | Android Studio |
| Native (iOS) | Swift | Xcode |
| Other native | — | Tizen Studio, Visual Studio, Huawei Quick App |
| Web / hybrid | HTML5, JavaScript, CSS3 | Ionic, PhoneGap, … |
| Cross-platform frameworks | Dart, JS, C# … | Flutter, React Native, Xamarin, NativeScript, … |

**English.** Kotlin Multiplatform lets you share *business logic* (networking, data) across Android and iOS while keeping each platform's own UI.
**中文：** KMM 的想法：共用「逻辑层」，UI 仍然各自原生。（Extra，不在 slide：JetBrains 已把 "KMM" 这个名字改成 **Kotlin Multiplatform (KMP)**。）

---

## 3. Mobile operating systems / 手机操作系统 (slides 13–21)

| OS | Kernel | Source | Notes 备注 |
|---|---|---|---|
| Android | Linux kernel | Open source (AOSP) | ~70% market share (slide 14 chart, Jan 2022–Jan 2023) |
| iOS | Unix-based (shared with macOS) | Closed | ~28–29% share; Apple devices only |
| Tizen | Linux kernel | Open source | Samsung watches/TVs |
| KaiOS | Linux-based | Open source | Feature phones |
| HarmonyOS | Microkernel | Open source (per slide) | Huawei |
| Fuchsia | Microkernel | Open source | Google; ran on Nest Hub |

The slide 14 chart shows two lines only: Android (top, ~70%) and iOS (~28%); every other OS is almost 0%.
中文：图上只有 Android 和 iOS 两条线，其余系统几乎贴着 0%。

### Exam template — "Examine TWO mobile OS that support the app" (Oct 2025 Q1a, 6+4 marks)
1. **Android** — Linux kernel, open source, huge market share, many device brands and price levels → the MyGOV app reaches the most Malaysians, including low-cost phones.
2. **iOS** — Unix-based, closed, tightly controlled hardware and updates → consistent performance and security on Apple devices; users update quickly so fewer versions to support.
*Justify:* together the two cover almost all smartphones, so one government service reaches nearly every citizen.
中文：写「OS 是什么 + 内核/开源 + 对这个 app 的好处」，最后一句说明两者合起来覆盖几乎所有用户。

---

## 4. Key mobile challenges / 四大挑战 (slides 22–25)

Four hardware/network limits: **processing power, memory & storage, battery, network.**
Slide 24 compares a flagship (octa-core, 12 GB RAM/256 GB, big battery, 4G/5G) with a basic phone (quad-core, 2 GB RAM/8 GB, small battery, 3G/4G). The point: **the same app must run on both.**
中文：同一个 app 要同时跑在旗舰机和入门机上，所以要为最差的设备优化。

### Slide 25 answer — apps for emerging markets / 新兴市场的做法

| Challenge | What goes wrong on a basic phone | What the developer does |
|---|---|---|
| Processing power | Laggy UI, dropped frames | Avoid heavy animation; do work off the main thread; simple layouts |
| Memory & storage | App killed (out of memory); no space to install | Small APK (Android Go targets < 40 MB), scaled images, cache limits, clean up resources |
| Battery | Drains fast, phone gets hot | Fewer location/network updates, batch background work, dark theme on OLED |
| Network | Slow/expensive/unstable data | Compress data, cache and work offline, retry, load only what is visible |

### Exam template — Jan 2026 Q1a(i) "Interpret FOUR key challenges in developing the ELSA app" (12 marks = 3 each)
For each challenge write *(1) what it is, (2) how it hurts this app, (3) what you do*. Example for one:
"**Battery** — phones have limited battery. ELSA runs AI diagnostics and syncs financing status, which drains battery, so users may uninstall it. The developer should batch network calls, avoid continuous location updates and support dark mode."
Repeat the same pattern for processing power, memory/storage and network. (3 marks ≈ 3 sentences.)

---

## 5. Beyond mobile apps / 移动应用之外 (slides 26–31)

Wearables, smart-home appliances, car dashboards (Android Auto), IoT, AR, AI, blockchain. The three photos on slides 29–31 are: Google Lens identifying a dog (**AI**), an AR thermal-monitoring overlay (**AR**), and a blockchain graphic.
**Exam use — Jan 2026 Q1a(ii) "how AI is implemented in ELSA" (4 marks):** give two applications, e.g. AI diagnostics that analyse SME data to find strengths and weaknesses, and AI-based recommendation of suitable training/financing plus auto-filling forms. Keep each linked to a benefit (faster, more accurate).

---

## 6. Android application fundamentals / Android 基础 (slides 32–42)

### 6.1 What is inside an APK? (slide 34, question 42.1)
APK (Android Package) = **Compiled code + Data + Resources**.
**English.** Code = the logic; Resources = layouts, images, strings that change per language/screen; Data = raw files bundled with the app. Keeping resources separate from code lets Android pick a different image or string for each phone (language, screen density) without changing any code.
**中文：** 代码、资源、数据分开，系统才能按语言/屏幕自动换资源而不改代码——这就是「为什么有三部分」的答案。（Extra：APK 里其实还有 AndroidManifest.xml 和签名信息。）

### 6.2 The sandbox / 沙盒 (slides 35–36)

```
              Phone CPU / Memory / Storage
   +----------------------+   +----------------------+
   | App 1  (UID 100)     |   | App 2  (UID 101)     |
   |  own Linux process   |   |  own Linux process   |
   |  own virtual machine |   |  own virtual machine |
   |  own private files   |   |  own private files   |
   +----------------------+   +----------------------+
        App 1 cannot read App 2's files (different UID)
```

Analogy / 类比: each app is a tenant in its own locked apartment; the OS is the building manager who only opens a door when the owner grants permission. *(Stops working for shared services — those are reached through permissions and intents, not by walking into other apartments.)*

**Principle of least privilege:** an app gets only the access it needs and nothing else (slide 37).

### 6.3 Sharing data / 共享数据 (slides 38–39)
Two apps signed with the **same certificate** can be given the **same UID**, so they can read each other's files and run in one process and VM.
⚠️ Slide is old: the `android:sharedUserId` mechanism is **deprecated since API 29**. Today apps share data through ContentProviders or Intents instead (extra).

### 6.4 Permissions (slides 40–41)
An app asks the user before touching contacts, SMS, storage, camera, Bluetooth, location…
- Android ≤ 5 (API < 23): all permissions granted **at install**.
- Android ≥ 6 (API 23+): "dangerous" permissions are asked **at runtime**.
⚠️ Not *all* permissions are runtime: "normal" ones such as `INTERNET` are granted automatically at install (extra).

### Slide 42 question 2 — model answer: "Two ways Android protects app data and user security"
1. **Application sandbox** — each app has its own Linux UID, process and VM, so one app cannot read another's data.
2. **Permission system + least privilege** — an app can only use protected resources (camera, location…) if the user grants that permission.
(Extra third: apps are signed with the developer's certificate so updates can be verified.)

---

## 7. The four components: ABCS / 四大组件 (slides 43–51)

| Component | One line | Has UI? | Analogy (restaurant) | Example |
|---|---|---|---|---|
| **A**ctivity | One screen | Yes | The dining room the customer sees | Login screen |
| **B**roadcast Receiver | Listens for system/app announcements | No (may show a notification) | The PA system — you act only when an announcement matches your interest | "Battery low", "phone rebooted" |
| **C**ontent Provider | Shared data gatekeeper | No | The pantry counter: other people may take items, but only through the clerk and only with permission | Contacts, user dictionary |
| **S**ervice | Long-running background work | No | The kitchen working out of sight | Music playing in background, sync |

**No `main()`:** an Android app has no single entry point. Any component can be the entry — e.g. WhatsApp can ask Gallery's "pick photo" Activity to start (slide 54).

**Broadcast flow (slide 46):** (1) app registers for "reboot" → (2) phone reboots → (3) system broadcasts → (4) every registered receiver runs. ⚠️ Receiver ≠ Activity: it has no screen and must finish quickly.

### Slide 51 — matching components (with reasons)
| Task | Component | Why |
|---|---|---|
| a. Login screen | **Activity** | It is a screen the user interacts with |
| b. Sync data from app to server | **Service** (in modern Android: WorkManager/foreground service) | Long-running, no UI, must survive leaving the screen |
| c. Manage a shared set of app data in local storage | **Content Provider** | It exists to share structured data with other apps under permission control |
| d. Schedule an alarm to post a notification | **Broadcast Receiver** | The alarm fires later as a broadcast; the receiver wakes up and posts the notification |

⚠️ **Common confusion:** "Service" is not a thread and does not mean "on a different thread" — by default it runs on the main thread of your app (Ch 4.2).

---

## 8. Intent and Manifest / Intent 与 Manifest (slides 52–60)

### 8.1 Intent
**English.** An Intent is a *message* that asks Android to start a component. It is how one app can start another app's component without knowing where it is.
**中文：** Intent = 给系统的一封「请帮我启动某某组件」的信。
It activates **Activities, Services and Broadcast Receivers** (slide 55). ⚠️ A **Content Provider is *not* started by an Intent** — it is accessed through a `ContentResolver` request (extra).

Common uses (question slide 60.2): start another Activity in your app; share text/photo (`ACTION_SEND`); open a web page/dial/map (`ACTION_VIEW`, `ACTION_DIAL`); start a Service; send a broadcast. Details in Chapter 3.

### 8.2 Manifest (`AndroidManifest.xml`)
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
  <uses-permission android:name="android.permission.INTERNET"/>     <!-- permission -->
  <uses-feature android:name="android.hardware.camera"/>            <!-- hardware/software features -->
  <application android:label="MyApp">
    <activity android:name=".MainActivity" android:exported="true"> <!-- component -->
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>          <!-- this is the "main" activity -->
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
  </application>
</manifest>
```
It is the first file Android reads. It lists: permissions, minimum API level, hardware/software features, components, linked libraries.
**Why important (question 60.3):** (1) tells the system which components exist — an undeclared Activity/Service/Provider cannot run; (2) declares permissions so the user can be asked; (3) declares which devices/API levels are supported so Google Play only offers the app to compatible devices.
⚠️ Nuance: a Broadcast Receiver can also be registered **in code at runtime**, so "components not declared can NEVER run" is strictly true for Activities, Services and Providers.

### 8.3 App resources (slide 59)
Stored in `res/`: `layout/` (UI), `values/` (strings, colours, styles), `drawable/` & `mipmap/` (images/icons), `menu/`, animation. Chapter 2.3 shows how alternative folders (`values-fr/`, `layout-land/`) support other languages/screens.

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 7 | Super Mario Bros is "developed by Sega" | It is Nintendo's. (Sega = Sonic.) Answer the question anyway: native game |
| 6 | Hybrid performance "depends on network speed" | Hybrid bundles its web files; limit is the WebView, not the network |
| 12 | "KMM" | Now called Kotlin Multiplatform (KMP) — extra |
| 38 | Same UID to share data | `sharedUserId` deprecated (API 29+) |
| 40 | All permissions granted at install or runtime | Only *dangerous* permissions are runtime; normal ones auto-granted |
| 55 | Intent activates A/S/BR | Correct — but do not extend it to Content Providers |
| 56 | Undeclared components can NEVER run | True for Activity/Service/Provider; receivers can be registered dynamically |

**Exam strategy:** if a question quotes a slide statement, answer as the slide does; the table above is for your own understanding.

---

## Cheat sheet / 速查表

| Term | Definition |
|---|---|
| Native / Hybrid / Mobile web | OS-specific / web inside native shell / browser site |
| APK | Compiled code + data + resources |
| Sandbox | Own UID + own process + own VM per app |
| Least privilege | Only the access the app needs |
| Activity / Service / Receiver / Provider | Screen / background work / event listener / shared data |
| Intent | Message that starts Activity, Service or Receiver |
| Manifest | First file read; lists permissions, features, min API, components |
| 4 challenges | Processing power, memory & storage, battery, network |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which app type gives the widest access to device features but needs a separate codebase per OS? (a) Mobile web (b) Hybrid (c) Native (d) Progressive
2. Two apps have different UIDs. Which statement is true? (a) They share one process (b) App 1 cannot read App 2's private files (c) They share one VM (d) Both are granted all permissions
3. Which component has no UI and is best for playing music in the background? (a) Activity (b) Service (c) Content Provider (d) Intent
4. Which is **not** started by an Intent? (a) Activity (b) Service (c) Broadcast Receiver (d) Content Provider
5. What happens if you forget to declare a new Activity in the manifest? (a) It runs slower (b) It cannot be started (c) It runs without permissions (d) Nothing

### B. Short answer
1. Give two differences between native and hybrid apps.
2. Why does an APK keep resources separate from compiled code?
3. Explain the principle of least privilege with one example.

### C. Trace / classification
1. App A (UID 100) tries to read a private file of App B (UID 101). Trace what the OS does and what would allow it.
2. User taps "Share photo" in WhatsApp and chooses Gallery. List which components of which apps take part and what starts them.
3. Fill in the four challenges for a basic phone (2 GB RAM, 2150 mAh, 3G) and give one design action each.

### D. Thinking
1. Jan 2026 style: "Interpret FOUR key challenges of developing a government service app for all Malaysians." Write a 12-mark answer.
2. A startup has only one developer but wants Android and iOS. Recommend an approach and justify.

### Answers
**A.** 1-c (native: wide features, one codebase per OS). 2-b (different UID → private files protected). 3-b (Service runs without UI; in modern Android use a foreground service). 4-d (Content Providers use ContentResolver). 5-b (an undeclared Activity is invisible to the system).

**B.**
1. Native: written in Kotlin/Java, fastest, wide device features, one codebase per OS, high cost. Hybrid: web content in a native shell, slower (WebView), limited features, single codebase, low cost. 中文：性能/硬件功能/代码库/成本四个角度比较。
2. So Android can choose different images, strings, layouts per language and screen density at run time without changing code.
3. An app that only needs internet does not declare camera or contacts permissions, so even if compromised it cannot access them.

**C.**
1. Different UID → files owned by App B have Linux permissions that deny App A → access denied (SecurityException). It would work only if both apps were signed with the same certificate and share a user ID (deprecated), or if App B exposes the data through a ContentProvider / share Intent with permission.
2. WhatsApp Chat Activity creates an implicit Intent (`ACTION_GET_CONTENT`/pick). Android searches intent filters, starts Gallery's Activity (another app, own process). Gallery returns the chosen photo URI to WhatsApp's Activity; the photo is read through a ContentProvider/URI grant.
3. Processing: quad-core → avoid heavy animation, background threads. Memory/storage: 2 GB/8 GB → small APK, scaled images. Battery: 2150 mAh → batch work, few location updates. Network: 3G → compress, cache, offline mode.

**D.**
1. Use the template in section 4: processing power, memory & storage, battery, network — each with what/why it hurts/what you do (3 marks each).
2. Recommend hybrid or a cross-platform framework (Flutter/React Native/KMP) — one codebase, low cost, app-store distribution — unless the app needs very heavy graphics or deep hardware access, in which case build native for the main platform first.

---

## Links to other chapters / 与其他章节的联系
- Intent details, Activity lifecycle → **Chapter 3**.
- Resources/alternative folders, accessibility → **Chapter 2.3**.
- Service and background work (WorkManager, threads) → **Chapter 4.2**.
- Manifest permissions for location/camera → **Chapters 5 and 6**; signing → **Chapter 7**.
