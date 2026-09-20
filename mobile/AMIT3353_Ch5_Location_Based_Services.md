# AMIT3353 — Chapter 5: Location-based Services
# 第 5 章：位置服务（中英双语）

> The slides list the location constants and permissions but never show how *accuracy, frequency and latency* trade off against battery with numbers, define geocoding backwards (slide 45), equate "last known location" with "current location", and still mention DDMS and a "connect in onStart()" step from the old API. This note explains each setting with worked numbers, corrects those points and gives model answers for the past-paper location questions.
> 中文：slide 只列出常量和权限，没有用数字讲清楚精度/频率/延迟与耗电的取舍；geocoding 的定义写反了；「last known location」不等于「当前位置」。这里逐项补充，并给出考试答题模板。

---

## 0. One-sentence overview / 一句话总结

An app gets the user's position from **GPS** (accurate, slow, power-hungry) or **Wi-Fi/cell towers** (rough, fast, cheap) through Google Play services' **Fused Location Provider**; you control battery use with **accuracy (priority), frequency (interval) and latency (max wait)**, ask for the right **permission** (fine / coarse / background), start updates in `onStart/onResume` and stop them in `onPause/onStop`.
中文：位置来源有 GPS 和 Wi-Fi/基站；用「优先级、间隔、最大等待时间」控制耗电；按需求申请 fine / coarse / background 权限；在合适的生命周期回调里开始和停止更新。

| Topic | Slides | Exam relevance |
|---|---|---|
| GPS vs Wi-Fi/cell | 4–6 | Jan 2026 Q3c (6 marks); MyChild GPS limitations |
| Accuracy / frequency / latency | 7–17 | Question 5.1 |
| Best practices | 20–24 | Removing updates, batching |
| Google Play services, permissions | 25–39 | Oct 2025 Q3c (foreground vs background) |
| Updates flow, permission dialog, mock | 40–44 | Testing |
| Geocoding | 45–47 | Oct 2025 Q4a (6 marks) |
| Review questions | 48–50 | Factors, real device, GPS limits |

---

## 1. Location strategies: GPS vs Wi-Fi/cell / 定位来源 (slides 4–6) — EXAM

| | **GPS** | **Wi-Fi / cell towers** |
|---|---|---|
| Accuracy 精度 | **High** (metres) | **Low** (tens to hundreds of metres or more) |
| Speed 速度 (time to first fix) | **Slow** | **Fast** |
| Power 耗电 | **High** | **Low** |
| Environment 环境 | Outdoors (needs sky view) | Indoors and outdoors |
**How each works:** GPS measures signals from satellites; Wi-Fi/cell positioning estimates position from known access points and towers around you (Google looks them up in a database).
**Exam template — Jan 2026 Q3c (6 marks):** three comparison points (accuracy, speed, power) × two sources = six statements, each with a short reason ("GPS is slow because the receiver must find and lock onto several satellites first").
Analogy / 类比: GPS = a surveyor with a precise instrument (accurate but slow to set up, tiring); Wi-Fi/cell = asking a neighbour "which street is this?" (quick, roughly right).

### Limits of GPS and how to overcome them (slide 50, 6 + 4 marks)
Three limitations: (1) **poor indoors/underground/between tall buildings** (weak or reflected signals); (2) **slow time to first fix**, especially on a cold start; (3) **high battery drain** (a child's tracker would run flat). (Also: accuracy varies with weather/foliage/multipath.)
**Technique:** use the **Fused Location Provider** — it combines GPS + Wi-Fi + cell towers (+ sensors) and chooses the best source automatically, gives a fast rough fix first and a precise one later, and saves battery; add **batching** and a lower update rate when the child is stationary.

---

## 2. Battery drain: accuracy, frequency, latency / 三个耗电因素 (slides 7–17)

Three knobs of a `LocationRequest`:

### 2.1 Accuracy = priority (slides 8–12)
| Priority | Constant | Uses | Precision | Power |
|---|---|---|---|---|
| High accuracy | `PRIORITY_HIGH_ACCURACY` | GPS (+ Wi-Fi, cell) | Best possible | High |
| Balanced power | `PRIORITY_BALANCED_POWER_ACCURACY` | Mostly Wi-Fi/cell, may use GPS | City block, ~100 m | Less |
| Low power | `PRIORITY_LOW_POWER` | Mostly cell towers | City level, ~10 km | Lower |
| No power | `PRIORITY_NO_POWER` | Only receives locations other apps requested | Depends on others | Minimal |
Higher accuracy → higher battery drain.

### 2.2 Frequency (slides 13–14)
| Method | Meaning |
|---|---|
| `setInterval(ms)` | How often you **want** a fix. Use a **large** value for background use, a **small** value for foreground. The real rate may vary. |
| `setFastestInterval(ms)` | The **fastest** rate at which your app can handle updates (it may receive faster updates that other apps requested). Prevents UI flicker/data overflow. |
| `setPriority()` | Accuracy setting |

### 2.3 Latency (slide 15)
`setMaxWaitTime(ms)` = the longest the system may **hold** locations before delivering them. Set it several times larger than the interval → the system **batches** fixes and wakes your app once instead of many times.

### Worked example — slide 16 (numbers verified)
```kotlin
interval = 10000        // 10 000 ms = 10 s   (slide comment says "1000 ms = 1 second": that is not the value used)
fastestInterval = 5000  // 5 s: never handle updates faster than every 5 s
maxWaitTime = 60 * 1000 // 60 s
priority = PRIORITY_HIGH_ACCURACY
```
- Fixes are **computed** about every 10 s; with `maxWaitTime = 60 s` the system may deliver them in a batch of **60 ÷ 10 = 6 locations** each minute.
- Slide 23: interval 10 min, maxWait 60 min → **6 fixes per delivery, 24 deliveries per day instead of 144 wake-ups** (6× fewer).
- Slide 24 (passive): interval 15 min, fastestInterval 2 min → you accept locations other apps triggered but at most once every 2 minutes.
⚠️ `LocationRequest.create()` (slide 16) is deprecated in newer Play services; the current form is `LocationRequest.Builder(priority, intervalMillis)`. Same ideas, different syntax.

### Question 5.1 — choose a location model (accuracy / frequency / latency)
| Use case | Accuracy | Frequency | Latency (batching) | Reason |
|---|---|---|---|---|
| a. Mapping/navigation | High | Every 1–5 s | Low — no batching | Turn-by-turn needs precise, immediate positions |
| b. Weather | Low power (city-level) | Rarely (e.g. every 30–60 min) | High — batching fine | City-level is enough |
| c. Retailer proximity alert | Balanced (~100 m) | Every few minutes (or geofence) | Medium | Need "near the store", not exact spot; save battery |
| d. Fitness tracker | High | Every 1–5 s while exercising | Low–medium (a foreground service; batching if screen off) | Records the route accurately |
(The numbers are reasonable examples, not official values.)

---

## 3. Best practices / 最佳实践 (slides 20–24)

1. **Remove location updates** when not needed: `requestLocationUpdates()` in `onStart()/onResume()`, `removeLocationUpdates()` in `onPause()/onStop()` (slide 21).
2. **Set timeouts** (`setExpirationDuration`, `setExpirationTime`) so a request stops by itself.
3. **Batch** requests (non-foreground use): long interval + larger `maxWaitTime`.
4. **Passive** updates: reuse locations that a foreground app already requested.

### Slide 39 answers
- **Why start in `onStart()`/`onResume()`?** Updates are only useful while the screen is visible; starting there ensures they (re)start every time the user returns, and combined with stopping in `onPause/onStop` they never run when the user cannot see the result — saving battery. Starting only in `onCreate()` would not resume after a pause.
- **Which lifecycle method turns them off?** `onPause()` (or `onStop()`).

---

## 4. Google Play services and last known location / 获取位置 (slides 25–38)

Location APIs come from **Google Play services** (installed via SDK Manager and added as a library dependency). Your app calls the **Fused Location Provider** client; the service talks to the location hardware (slide 26).
```kotlin
private lateinit var fusedLocationClient: FusedLocationProviderClient
override fun onCreate(savedInstanceState: Bundle?) {
    fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
}
fusedLocationClient.lastLocation.addOnSuccessListener { location: Location? ->
    // location can be null (no fix yet, location off, etc.)
}
```
⚠️ **Slide 25 "Current location = last known location"** is a simplification: `lastLocation` returns the **most recent cached fix**, which can be old or `null`; for an up-to-date position request updates (`requestLocationUpdates`) or a current-location request.
⚠️ **Slide 38 "Connect to service in `onStart()`"** comes from the older `GoogleApiClient` API. With `FusedLocationProviderClient` there is no explicit connect step.

### Permissions (slides 27–30, 42–43)
| Permission | What it gives |
|---|---|
| `ACCESS_COARSE_LOCATION` | Approximate location (about a city block) |
| `ACCESS_FINE_LOCATION` | Precise location (GPS) |
| `ACCESS_BACKGROUND_LOCATION` | Location while the app is not visible (**Android 10 / API 29+**) |
- Android 6+ (API 23): ask **at run time** (dialog: *While using the app / Only this time / Deny*, slide 42).
- Android 11 (API 30)+: the user enables **background** location on a **settings page** (slide 43); you cannot get it from the same dialog.
- (Extra) Android 12+: the user can grant only "approximate" even if you ask for fine.
**Slide 39.1:** mapping app → **Fine** (precise turn-by-turn); weather app → **Coarse** (city-level is enough).

### Foreground vs background location (slides 31–36) — EXAM
| | **Foreground** | **Background** |
|---|---|---|
| Sharing | Once, or for a predefined period | **Constant** |
| UI | **Visible** | **Not visible** |
| Persistent notification | **Yes** (foreground service) | No |
| Examples | Turn-by-turn navigation; "share my location" in chat | Family location sharing; smart-home "turn off when I leave home" |
For a foreground service declare `android:foregroundServiceType="location"` in the manifest (Android 10+; slide 36).

**Exam template — Oct 2025 Q3c (3 marks each):**
| Use in MyGOV | Type | Explanation |
|---|---|---|
| (i) Directions to the nearest UTC | **Foreground** | The user is looking at the map; location is only needed while the feature is on screen (and a short-lived foreground service can keep navigating) |
| (ii) Alerts for nearby government events | **Background** | The app must detect proximity while its UI is not visible and keep checking over time |

---

## 5. Location update flow (slide 41)
```
START -> connect to location service -> make a location request
      -> [location changed?] --yes--> update UI --+
                  no ------------------------------+--> [pause?] --yes--> stop updates -> STOP
                                                           no -> back to "location changed?"
```
Trace: request made → fix arrives → UI updates → user leaves screen (`onPause`) → `removeLocationUpdates` → STOP.

---

## 6. Testing with mock locations / 测试 (slide 44, question 49.4)
The emulator's **Extended controls → Location** lets you enter latitude/longitude (slide 44 figure) or replay a GPX/KML route. ⚠️ Slide text says "DDMS" — that tool is obsolete; the figure shows the modern Extended controls.
**Slide 49.4 — "The best way to ensure accuracy is to test on a real device":** *Largely true.* Emulators only inject the coordinates you type; real devices show real GPS behaviour — slow first fix, drift indoors, signal loss, battery drain, sensor fusion and different phone hardware. Best practice: use mock locations for repeatable logic tests, real devices (moving, indoors and outdoors) for accuracy and battery.

---

## 7. Geocoding / 地理编码 (slides 45–47) — EXAM

⚠️ **Slide 45 defines geocoding backwards.**
| Term | Direction | Android call |
|---|---|---|
| **Geocoding** | **Address → coordinates** (latitude, longitude) | `Geocoder.getFromLocationName()` |
| **Reverse geocoding** | **Coordinates → address** | `Geocoder.getFromLocation()` |
Slide 45's sentence ("converting a geographic location to an address") is *reverse* geocoding, and slide 46 (coordinates verify a misspelled address; "street addresses can change; coordinates won't") describes normal geocoding. If asked to define it: give the standard meaning (address → coordinates) and mention the reverse direction.
Possible errors (slide 47): no location data provided; invalid latitude/longitude; no geocoder available on the device; no address found.

**Exam template — Oct 2025 Q4a "Relate the applications of geocoding to relevance and benefits for MyGOV users" (6 marks):** (1) Convert the user's typed address into coordinates to find and show the **nearest UTC**/office and its distance; (2) **Reverse-geocode** the phone's GPS position into a street address to **auto-fill** forms such as licence-renewal address; (3) **Validate** misspelled/ambiguous addresses so services (e.g. mail delivery, eligibility by district) use correct data. For each: application → relevance → benefit (faster, fewer errors, less typing).

---

## 8. Review questions (slides 48–50)

**5.3.1 Factors that affect accuracy:** location source (GPS vs Wi-Fi/cell), environment (indoors, tall buildings, weather, trees), number/strength of satellites and towers, device hardware quality, user movement/speed, the priority/interval you choose, permission level (coarse vs fine), battery-saver settings, mock locations.
**5.3.2 "It is important to create a model of best performance":** Agree — accuracy, frequency and latency all cost battery; a model chosen per use case (section 2, question 5.1) gives just enough accuracy, prevents battery drain and uninstalls, and can be tested and tuned.
**Question 5 (6 marks) — location awareness improving UX:** e.g. a **food-delivery app**: (1) shows restaurants near you; (2) auto-fills the delivery address by reverse geocoding; (3) tracks the rider live and gives an ETA; benefit each: relevance, less typing, transparency.
**Question 6:** see "Limits of GPS" in section 1.
**Emergency features (slides 18–19):** *Android Emergency Location Service* automatically sends the phone's location to emergency responders when you call an emergency number; *Earthquake Alerts System* uses phone sensors to detect shaking and warns nearby users.

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 45 | Geocoding = location → address | That is *reverse* geocoding; geocoding = address → coordinates |
| 25 | Current location = last known location | Last known = cached, possibly old/null |
| 38, 26 | Connect to the service in `onStart()` (Google API Client) | Not needed with `FusedLocationProviderClient` |
| 16 | `interval = 10000 // 1000 ms = 1 second`; `LocationRequest.create()` | Value is 10 s; `create()` deprecated → `Builder` |
| 13 | `setFastestInterval` = "interval for other apps" | Fastest rate your app handles; you may receive updates other apps triggered |
| 44 | DDMS | Use emulator Extended controls |
| 30 | Only coarse (+ background) shown | Precise use needs `ACCESS_FINE_LOCATION`; Android 12+ users may downgrade to approximate |

Exam strategy: use the slide's constants (`PRIORITY_HIGH_ACCURACY` …) and lifecycle rule (start `onStart/onResume`, stop `onPause/onStop`).

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| GPS | Accurate, slow, high power, outdoors |
| Wi-Fi/cell | Rough, fast, low power, indoors + outdoors |
| Priority | `HIGH_ACCURACY`, `BALANCED_POWER_ACCURACY`, `LOW_POWER`, `NO_POWER` |
| `setInterval` / `setFastestInterval` / `setMaxWaitTime` | Desired rate / fastest handled rate / batching delay |
| Fused Location Provider | Google Play services API combining sources |
| Fine / Coarse / Background | Precise / ~city block / when UI not visible |
| Foreground service type `location` | Needed for foreground location on Android 10+ |
| Geocoding / reverse | Address → coordinates / coordinates → address |
| Remove updates | `onPause`/`onStop` |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which source is fastest and least power-hungry? (a) GPS (b) Wi-Fi/cell towers (c) both equal (d) magnetometer
2. Which setting batches location fixes to save battery? (a) setInterval (b) setMaxWaitTime (c) setPriority (d) setExpirationTime
3. A weather app needs city-level position. Best permission? (a) Fine (b) Coarse (c) Background (d) none
4. Converting "1 Jalan Ampang" into latitude/longitude is… (a) reverse geocoding (b) geocoding (c) batching (d) mocking
5. Where should you call `removeLocationUpdates()`? (a) onCreate (b) onResume (c) onPause/onStop (d) onDestroy only

### B. Short answer
1. Compare GPS and Wi-Fi/cell in accuracy, speed and power.
2. Explain foreground vs background location with one example each.
3. Give three limitations of GPS and one technique to overcome them.

### C. Calculation / trace
1. `interval = 5 min`, `maxWaitTime = 30 min`. How many fixes per delivery? How many deliveries per day?
2. A store is at (3.1488, 101.7134) (hypothetical) with a 500 m geofence. User A at (3.1520, 101.7120), user B at (3.1579, 101.7116). Who is inside? (Use the haversine formula.)
3. Trace the update flow: the user opens the map, walks, then switches to another app.

### D. Thinking
1. Choose a full location model (priority, interval, maxWait, permission, lifecycle) for a delivery-rider tracking app.
2. Explain how a government app could use both geocoding and reverse geocoding.

### Answers
**A.** 1-b. 2-b. 3-b. 4-b. 5-c.

**B.**
1. GPS: high accuracy, slow first fix, high power, outdoors. Wi-Fi/cell: low accuracy, fast, low power, indoors and outdoors.
2. Foreground: user sees the feature, e.g. turn-by-turn directions (with a persistent notification/foreground service). Background: constant sharing while UI is hidden, e.g. family location sharing.
3. Limits: poor indoors/urban canyons; slow first fix; high battery use. Technique: Fused Location Provider (GPS + Wi-Fi + cell) with balanced/adaptive priority and batching.

**C.**
1. 30 ÷ 5 = **6** fixes per delivery; 24 h × 60 ÷ 30 = **48** deliveries per day (versus 288 wake-ups without batching).
2. Haversine (R = 6371 km): A ≈ **388 m** → inside; B ≈ **1,031 m** → outside (calculated with Python).
3. Connect/create client → `requestLocationUpdates` (in `onStart/onResume`) → each new fix updates the map → switching apps calls `onPause` → `removeLocationUpdates` → updates stop; on return `onResume` restarts them.

**D.**
1. Priority HIGH_ACCURACY; interval 5 s (foreground), maxWait ~15 s; permission Fine + a foreground service of type location (background if tracking continues when the screen is off); start on `onStart/onResume`, stop on `onPause/onStop` or when delivery ends; batch uploads to the server.
2. Geocode a typed home address → coordinates to find the nearest UTC; reverse-geocode the phone's position → address to auto-fill a form.

---

## Links to other chapters / 与其他章节的联系
- Lifecycle callbacks for start/stop → **Chapter 3**; foreground services and WorkManager → **Chapter 4.2**.
- Runtime permission concept → **Chapter 1**; sensors (accelerometer, barometer help location) → **Chapter 6**.
- Location-based apps in the store (Play policies for background location) → **Chapter 7**.
