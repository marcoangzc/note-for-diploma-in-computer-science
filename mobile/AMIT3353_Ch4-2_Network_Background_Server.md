# AMIT3353 — Chapter 4.2: Network Operations, Background Operations and Mobile Server Options
# 第 4.2 章：网络操作、后台任务与服务器选择（中英双语）

> The slides tell you to use WorkManager/coroutines on one slide and AsyncTask on another, define SOAP as running over "TCP or UDP" (application layer), give the DevOps definition for BaaS, and show a flowchart that sends *every* network call to DownloadManager. This note keeps the slide's structure but corrects those points, explains what each background tool is for, and gives ready answers for the front-end/back-end diagram, UI-vs-background thread, and the H&H case study.
> 中文：slide 前后互相矛盾（一页说用 WorkManager/协程，另一页教 AsyncTask）、把 BaaS 写成 DevOps 的定义、流程图把所有网络请求都指向 DownloadManager。这里逐项纠正，并给出考试题模板。

---

## 0. One-sentence overview / 一句话总结

A mobile app is the **front-end** that talks to a **back-end** through an **API** (usually HTTP + JSON); slow work such as networking must run on a **background thread** (coroutines/WorkManager/…), and the back-end can be **built yourself (DIY)** or **rented (cloud/BaaS such as Firebase)**.
中文：手机 app（前端）通过 API 和后端沟通；网络等慢操作一定要放后台线程；后端可以自建（DIY）或租用（云 / BaaS）。

| Topic | Slides | Exam relevance |
|---|---|---|
| Mobile-to-server, REST/SOAP, JSON | 3–13 | Oct 2025 Q3a (define front/back end, diagram) |
| Main vs background thread, background tools | 14–18 | Jan 2026 Q3a (UI thread, background thread, 2 async tasks) |
| Network operations, AsyncTask, Volley | 19–43 | Questions 4.2.1 |
| MQTT | 44–47 | Question 4.2.2 |
| Mobile server options, BaaS | 48–68 | Question 4.2.3 (H&H) |

---

## 1. Mobile-to-server communication / 手机与服务器通信 (slides 3–13)

### 1.1 Front-end, API, back-end
- **Front-end** = the part the user sees and touches: the **mobile app** (UI + optional local database).
- **Back-end** = the server side: **API server**, application logic, **database server / cloud database**.
- **API** (Application Programming Interface) = the agreed "menu" of requests the app can send and replies it gets; the app never touches the database directly.
Analogy / 类比: restaurant — customer = mobile app, waiter = API, kitchen and pantry = back-end. The customer orders from the menu; the waiter carries requests; the kitchen never comes out to the table.

```
 FRONT-END                                   BACK-END
 +-----------+                +--------+   +--------+   +----------+   +----------+
 | Mobile    | <-- HTTP/S --> | Network|<->| API    |<->| Database |<->| Cloud    |
 | client    |    (JSON)      | (cloud)|   | server |   | server   |   | database |
 +-----+-----+                +--------+   +--------+   +----------+   +----------+
       |
   Local database (Room/SQLite: offline cache)
```
(Slide 5 figure; the exam asks you to **draw exactly this** — Oct 2025 Q3a(ii), 5 marks.)
**Exam definitions (Oct 2025 Q3a(i), 4 marks):** *Front end* — the client-side, user-facing part (the mobile app and its UI/local storage) that collects input and displays results. *Back end* — the server-side part (API server, business logic, databases) that processes requests, stores data and returns responses.

**Slide 6 "Do I even need a back-end?" (no content on slide; extra):** yes if data is shared between users/devices, you need login, payments, push notifications or heavy processing; no for a purely local app (calculator, offline notes) — then Room/DataStore is enough.

### 1.2 Protocols and data formats (slides 7–12)
HTTP is the most used protocol. Three styles: **REST**, **SOAP**, **XML-RPC**.
| | **REST** | **SOAP** |
|---|---|---|
| Idea | Resources identified by URLs; use HTTP methods | Messages in an XML **Envelope** (Header + Body) |
| Methods | `GET` read, `POST` create, `PUT` update, `DELETE` remove | Operations defined in the message/WSDL |
| Formats | HTML, XML, **JSON** | XML only |
| Weight | Light, simple, common for mobile | Heavy, strict, used in enterprise/legacy systems |
| Runs over | HTTP | Application-layer protocols such as HTTP, SMTP |
⚠️ Slide 9 lists "HTTP, SMTP, **TCP, UDP**" as application-layer protocols — TCP and UDP are **transport-layer**. Quote the slide if asked, but know the difference.

**JSON vs XML (slide 10):** same data — JSON is shorter (`{"username":"…"}`) than XML (`<username>…</username>` tags), so it is lighter to send and easier to parse; most Google APIs are JSON REST.

### 1.3 Parsing JSON on Android (slide 13) — verified with the slide's sample
Sample: `{"records":[{"id":"1","name":"Alice","contact":"012"}, … 5 items ]}`
```kotlin
val root = JSONObject(response)                       // whole text -> JSONObject
val arr  = root.getJSONArray("records")               // the array under key "records"
for (i in 0 until arr.length()) {                     // slide: 0..size-1
    val o = arr.getJSONObject(i)
    users.add(User(o.getString("id"), o.getString("name"), o.getString("contact")))
}
```
Parsed with Python's `json` to check: `length = 5`; rows `1 Alice 012`, `2 Calvin 013`, `3 Jane 123`, `4 Mark 035`, `5 Susan 05`. Note `contact` stays a **String** (`"05"`) — `getString`, not `getInt`, or the leading zero is lost. `getString` throws `JSONException` if a key is missing; `optString` returns a default.

---

## 2. Background operations / 后台操作 (slides 14–18)

**Main (UI) thread** = the one thread that draws the screen and handles touches. **Background thread** = any other thread used for long-running work (network, disk I/O, decoding a bitmap — slide 16 figure).
**Exam definitions (Jan 2026 Q3a(i), 4 marks):** *UI thread* — the main thread that handles user interaction and updates the screen; it must never be blocked. *Background thread* — a separate thread that runs long or blocking operations (network, disk, heavy computation) and hands results back to the UI thread.
Rule: **if you do network on the main thread, Android throws `NetworkOnMainThreadException`** — and even without it the UI would freeze (ANR).

### 2.1 Which background tool? (slide 17 flowchart, slide 18 table)
| Ask yourself | Use | Meaning |
|---|---|---|
| Is it a long HTTP **download**? | **DownloadManager** | System handles long downloads, retries, notification |
| Must it run **now** and finish (user-started)? | **Foreground Service** | Shows an ongoing notification; e.g. music, navigation, upload the user just started |
| Can it wait until conditions are right (Wi-Fi, charging)? | **WorkManager** | Deferrable, guaranteed work that survives app/device restart |
| Must it run at an **exact time**? | **AlarmManager** | Alarm/reminder at a set time |
| None of the above | **WorkManager** | Default for deferrable background work |

### Worked examples (with reasons)
| Task | Tool | Why |
|---|---|---|
| Download a 300 MB course video | DownloadManager | Long HTTP download |
| Upload receipts when on Wi-Fi and charging | WorkManager | Deferrable with constraints |
| Remind the user at 7:30 a.m. | AlarmManager | Exact time |
| Play music while the app is closed | Foreground Service | Must run now, user-visible |
| Sync application status every 15 minutes | WorkManager (periodic) | Repeating deferrable work |
| Load a JSON list for the screen | **Coroutine** (Kotlin, slide 20) | Short API call started by the UI |
⚠️ **Slide 17 simplification:** "Network I/O → DownloadManager" applies to *downloading files*. Normal API calls (JSON) use coroutines/Retrofit/Volley, not DownloadManager. Slide 20 says "Kotlin: use WorkManager – coroutine"; **SyncAdapter** ("regularly and efficiently") is legacy — Google now recommends WorkManager for new code.

### 2.2 Exam template — Jan 2026 Q3a(ii): "TWO asynchronous tasks in ELSA" (6 marks)
1. **Fetch AI diagnostic results** — the app sends the SME's data to the server and waits for analysis; done on a background thread/coroutine so the screen stays usable, then the result is posted to the UI thread.
2. **Upload financing documents / sync application status** — uploads can be large and slow; WorkManager retries them when the network returns and updates the status screen when finished.
Each: *what the task is → why it must be asynchronous → how the result reaches the UI*.

---

## 3. Network operations / 网络操作 (slides 19–43)

### 3.1 Permissions and safety (slide 21)
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>  <!-- to check connectivity -->
```
Best practice: send as little sensitive data as possible and **encrypt traffic** — slide says SSL; modern apps use **HTTPS (TLS, the successor of SSL)**.

### 3.2 Checking connectivity (slides 22–24, Compose)
`ConnectivityManager.NetworkCallback` reports changes; a `StateFlow<NetworkStatus>` (`Available, Unavailable, Losing, Lost`) publishes them:
| Callback | Sets status |
|---|---|
| `onAvailable` | Available |
| `onLosing(maxMsToLive)` | Losing (about to drop) |
| `onLost` | Lost |
| `onUnavailable` | Unavailable (could not connect) |
UI: `val status by observer.status.collectAsState()`; `LaunchedEffect(Unit){ observer.register() }` starts listening; `DisposableEffect(Unit){ onDispose { observer.unregister() } }` stops when the composable leaves (avoids leaks); a `when(status)` shows Online/Offline/Losing text.

### 3.3 AsyncTask (slides 25–28) — legacy
An `AsyncTask` ran work off the UI thread and published the result back:
| Step | Runs on | Method |
|---|---|---|
| 1 | UI thread | `onPreExecute()` (set up progress bar) |
| 2 | Background thread | `doInBackground(params)` (the network call) |
| 3 | UI thread | `onPostExecute(result)` (show the result) |
Slide 27 figure: MainActivity's `NetworkFragment` starts a `DownloadTask`; `DownloadCallback` returns the result to the UI.
⚠️ **Contradiction:** slide 20 says use coroutines/WorkManager, slides 25–28 teach AsyncTask. `AsyncTask` is **deprecated (API 30)**. Learn it for the exam (the concept "background work + publish on UI thread"), use **coroutines** in real code. Suitable only for short operations (slide 28).
**Q 4.2.1 answers:** (1) *Three components:* mobile app (front-end UI) sends requests through the **API** (the interface/contract, e.g. REST + JSON) to the **back-end** (server + database) which replies; the API is the only door between them. (2) Network delays are unpredictable; on the UI thread they freeze the app and cause `NetworkOnMainThreadException`/ANR. (3) AsyncTask performs the network operation in `doInBackground()` off the UI thread, then `onPostExecute()` publishes the result on the UI thread.

### 3.4 Volley (slides 30–43)
**Volley** = Google's HTTP library. **Good for:** populating UI with small data (search results, JSON); **benefits:** automatic request scheduling, several connections at once, request **prioritisation**, request **cancellation**; **not for** large downloads or streaming.
| Class | Returns |
|---|---|
| `StringRequest` | raw String |
| `JsonObjectRequest` | `JSONObject` |
| `JsonArrayRequest` | `JSONArray` |
**Reading the code (slide 35):** create `RequestQueue`; create `StringRequest(method, url, successListener, errorListener)`; `queue.add(request)`. Volley runs the request on its own threads and **delivers the callbacks on the main thread**, so you can update the UI directly.
- **RequestQueue** needs a **network** (`BasicNetwork(HurlStack())`) and a **cache** (`DiskBasedCache(cacheDir, 1024*1024)` = 1 MiB = 1,048,576 bytes) (slides 38–39).
- **Cancel** (slide 37): give requests a tag, call `queue.cancelAll(TAG)` in `onStop()` so leaving the screen stops needless requests. (In Kotlin the method should be `override fun onStop()`.)
- **Singleton** (slides 40–42): one `RequestQueue` for the whole app, created with `context.applicationContext` so you do not **leak** an Activity.
- **URL parts** (slide 36, checked with a parser): `https://www.bing.com/search?q=library` → scheme `https`, host `www.bing.com`, path `/search`, query `q=library`; the translate URL has query keys `sl=en, tl=zh-CN, text=android, op=translate`.
⚠️ Slide 35 uses `http://` — since Android 9 **cleartext HTTP is blocked** by default; use `https://`.

### 3.5 MQTT (slides 44–47)
**MQTT** (Message Queuing Telemetry Transport) = lightweight machine-to-machine **publish/subscribe** protocol on top of TCP/IP. Devices never talk to each other: they publish messages to a **topic** on a **broker**; subscribers of that topic receive them.
| Step (slide 45) | Who | What |
|---|---|---|
| 1 | Laptop and mobile | **subscribe** to topic `temperature` at the broker |
| 2 | Temperature sensor | **publishes** "21 °C" to topic `temperature` |
| 3 | Broker | forwards it to every subscriber |
**Q 4.2.2 — why MQTT for an IoT app:** very small headers and low bandwidth/battery use; works on slow or unreliable networks and keeps a persistent connection for real-time updates; publish/subscribe decouples the many sensors from the app; one broker serves many devices.

---

## 4. Mobile server options / 服务器选择 (slides 48–68)

A back-end has three core functions: **application server** (logic), **web server**, **database**. Popular technologies (slide 50): Ruby on Rails, Express/**Koa**/Sails (Node.js; slide says "Kia"), Django (Python), PHP MVC frameworks, Google Firebase.

Three options (slide 51):
| | **DIY** (build your own) | **Subscribe** (rent) | **Mix** (DIY + subscribe) |
|---|---|---|---|
| What | Own servers: API + DB | Cloud, container, virtualisation, **BaaS** | Sensitive parts DIY, others rented |
| Advantages | Complete control (hardware, software, network, services) | Cost efficiency, scalability, speed, integration, audit/compliance, business continuity | Balance of control and cost |
| Disadvantages | Complexity, customisation effort, security vulnerabilities, insufficient performance, poor reliability/functionality, technical debt, more monitoring/maintenance | Pay-for-use bills, security depends on the provider | More to manage |
(Slide 51 says "Mix and bang" — read it as "mix and match".)

**Definitions (slide 54):** *Cloud* — on-demand computing resources over the Internet, pay-for-use. *Container* — packages an app with what it needs so it runs the same in any environment. *Virtualisation* — running a virtual computer on shared hardware.
⚠️ **BaaS (Back-end as a Service) is mis-defined on slide 54.** The slide's sentence (tools that help the development and operations teams collaborate) describes **DevOps**. BaaS = a cloud service that gives ready-made back-end features through an SDK/API so you do not build servers: **storage, push notifications, usage analytics, dashboard, social integration, user administration/authentication, custom code** (slide 57). Examples: **Firebase** (Google), **Apple CloudKit**; cloud platforms: AWS, Azure, Alibaba Cloud, Huawei Cloud (slides 58–66).

### Q 4.2.3 answers
**1. Subscription vs DIY** — use the table: DIY = full control but high effort/security/maintenance risk; subscription = fast, scalable, cheaper to start, provider handles security updates, but recurring cost and dependence on the provider.
**2. H&H (500 salespersons; slow search; poor territory management; add push notifications + chatbot) — secure and cost-effective deployment:**
- **Push notifications:** Firebase Cloud Messaging (BaaS) — no server to build, free/cheap, encrypted transport, reaches all 500 devices.
- **Chatbot:** a managed chatbot/NLP service (e.g. Dialogflow, Azure Bot) called through the API — cheaper and safer than training and hosting your own.
- **Slow search:** keep the existing inventory DB, expose it through a **secured REST API over HTTPS** with authentication (tokens), add a search index/cache in the cloud and a local Room cache on the phone.
- **Territory management:** location + analytics dashboard from a cloud service.
- **Security/cost balance:** "mix" — keep the sensitive customer/inventory data in the company's controlled DB (or private cloud), rent the generic features (push, chatbot, analytics) on pay-as-you-use plans; encrypt in transit, role-based access.

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 9 | SOAP over HTTP, SMTP, TCP, UDP (application layer) | TCP/UDP are transport layer |
| 12 | JSON faster and easier than XML | Generally smaller/simpler; "faster" is a simplification |
| 17 | Network I/O → DownloadManager | Only long file downloads; API calls use coroutines/Retrofit/Volley |
| 20 vs 25 | WorkManager/coroutine vs AsyncTask | AsyncTask deprecated in API 30 |
| 20 | SyncAdapter | Legacy; WorkManager recommended |
| 21 | SSL | Use HTTPS/TLS |
| 35 | `http://` URL | Cleartext blocked from Android 9 |
| 37 | `protected fun onStop()` | `override fun onStop()` in an Activity |
| 50 | Kia | Koa |
| 54 | BaaS definition | That is DevOps; BaaS = ready-made back-end services |

Exam strategy: answer with the slide's terms (AsyncTask, Volley, BaaS), then add "modern equivalent: coroutines / Retrofit / Firebase" if space permits.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| Front-end / back-end | Mobile app / server side (API server, DB) |
| API | Interface through which the app requests back-end services |
| REST verbs | GET read, POST create, PUT update, DELETE delete |
| JSON | Light text data format: `{"key":"value"}` |
| UI thread / background thread | Screen + touch / long-running work |
| `NetworkOnMainThreadException` | Thrown when network work runs on the UI thread |
| DownloadManager / WorkManager / AlarmManager / Foreground Service | Long download / deferrable / exact time / now, visible |
| AsyncTask | onPreExecute (UI) → doInBackground → onPostExecute (UI); deprecated |
| Volley | HTTP library: queue, cache, priority, cancel |
| MQTT | Publish/subscribe via broker, topics, light |
| DIY / Subscribe / BaaS | Own servers / rented / ready-made back-end services |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which HTTP method normally *creates* a resource in REST? (a) GET (b) POST (c) PUT (d) DELETE
2. Best tool for "run every 15 minutes, only on Wi-Fi"? (a) AlarmManager (b) DownloadManager (c) WorkManager (d) Toast
3. Which method of AsyncTask runs on a background thread? (a) onPreExecute (b) doInBackground (c) onPostExecute (d) all
4. MQTT devices communicate through… (a) each other directly (b) a broker using topics (c) SOAP envelopes (d) SMTP
5. Which is **not** a BaaS service? (a) push notifications (b) user authentication (c) file storage (d) compiling the Android app

### B. Short answer
1. Explain the relationship between mobile app, API and back-end.
2. Give two advantages and two disadvantages of DIY servers.
3. Why is a Volley `RequestQueue` made a singleton?

### C. Trace / classification
1. Parse `https://shop.example.com/api/orders?status=paid&page=2` into scheme, host, path, query.
2. Choose the background tool: (a) upload 50 photos when charging; (b) navigation voice guidance; (c) download an 80 MB PDF; (d) alarm at 6:00; (e) fetch a JSON list when a screen opens.
3. A `JSONArray` under key `records` has 5 objects. What does `arr.length()` return, and what is `arr.getJSONObject(4).getString("name")` for the sample in section 1.3?

### D. Thinking
1. Jan 2026 Q3a: define UI thread and background thread and give two asynchronous tasks in an SME-finance app.
2. Design the back-end for a small clinic's appointment app with one developer and a low budget.

### Answers
**A.** 1-b. 2-c. 3-b. 4-b. 5-d.

**B.**
1. The app (front-end) shows the UI and sends requests; the API is the defined interface/contract (e.g. REST + JSON over HTTPS); the back-end (server + database) processes them and returns responses. The app never accesses the database directly.
2. Advantages: complete control over hardware/software/network; can meet special requirements. Disadvantages: complexity and maintenance time; security vulnerabilities and reliability/performance risks; technical debt.
3. One shared queue schedules all requests efficiently, shares one cache, and using `applicationContext` prevents leaking an Activity.

**C.**
1. scheme `https`; host `shop.example.com`; path `/api/orders`; query `status=paid`, `page=2`.
2. (a) WorkManager (charging constraint); (b) Foreground Service; (c) DownloadManager; (d) AlarmManager; (e) coroutine (or Volley/Retrofit) — a short API call.
3. `length() = 5`; index 4 → `"Susan"` (verified by parsing the sample).

**D.**
1. Definitions from section 2; tasks: fetch AI analysis results; upload documents/sync status (see 2.2).
2. Subscribe: Firebase (Auth + Firestore + Cloud Messaging) as BaaS — no servers to run, pay-as-you-go, built-in security; use push reminders for appointments; keep patient data encrypted and follow privacy rules; upgrade to a mixed model if data must stay in a private system.

---

## Links to other chapters / 与其他章节的联系
- Threads, coroutines, Room and Repository → **Chapter 4.1**; Service/BroadcastReceiver basics → **Chapter 1**.
- Notifications triggered by push or alarms → **Chapter 2.3**; permissions in the manifest → **Chapters 1, 5, 6**.
- Cloud/BaaS choices and app cost → **Chapter 7 (monetisation)**.
