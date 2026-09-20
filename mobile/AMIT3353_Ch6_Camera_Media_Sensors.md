# AMIT3353 — Chapter 6: Specialized Instruments and Devices (Camera, Audio/Video, Sensors)
# 第 6 章：相机、音视频与传感器（中英双语）

> The slides give the camera decision chart but not the reasoning, mix `startActivity` with `onActivityResult`, say the accelerometer *excludes* gravity (it includes it), describe the thermometer two different ways, and cover sensors as a list of pictures with no code or numbers. This note explains each choice, adds real accelerometer/tilt numbers and bitmap-memory calculations (computed), corrects the slide errors and gives answers to the camera/sensor questions from both past papers.
> 中文：slide 给了相机流程图但没讲原因；代码里 `startActivity` 和 `onActivityResult` 对不上；加速度计写成「不含重力」（其实含重力）；传感器部分几乎只有图片。这里补上原因、算过的数字和考题模板。

---

## 0. One-sentence overview / 一句话总结

To use the phone's camera you either **pick from the gallery**, **launch the existing camera app with an Intent** (easy, no camera permission) or **write your own camera module** (CameraX/Camera2 + CAMERA permission); you play sound/video with **MediaPlayer** (and always `release()` it); and you read motion, environmental and position **sensors** to give apps context.
中文：相机 3 种做法（相册 / 调用系统相机 / 自己写）；MediaPlayer 用完要 release；传感器分运动、环境、位置三类。

| Topic | Slides | Exam relevance |
|---|---|---|
| Camera options, manifest declarations | 3–11 | Oct 2025 Q4b; Jan 2026 Q4a(i)(ii) |
| Camera uses, scaled bitmaps, barcode | 12–19 | Memory/OOM |
| Audio streams, MediaPlayer | 20–28 | Codec, WAKE_LOCK, release() |
| Sensors: motion, environmental, position | 29–46 | Jan 2026 Q4a(iii); Question 6.3 (5 marks) |

---

## 1. Camera: three ways / 相机的三种做法 (slides 3–6)

```
 Is a camera a must for the feature?
    No  -> get a photo from the GALLERY (no camera at all)
    Yes -> need special processing (filters, live analysis, custom UI)?
              No  -> use the EXISTING camera app via Intent   (simple)
              Yes -> write your OWN camera module (CameraX / Camera2)   (complex)
```
| | Gallery | Existing camera app (Intent) | Own camera module |
|---|---|---|---|
| Code | Very little (`GetContent` contract) | Little (Intent / `TakePicture` contract) | A lot (preview, capture, lifecycle) |
| CAMERA permission | No (system picker) | **No** (the camera app has it) | **Yes** — declare and ask at run time |
| Control over the image/preview | None | Little | Full |
| Best for | Choosing an existing photo | Simple capture (profile photo, receipt) | Live scanning, filters, AR |
Analogy / 类比: gallery = choose a photo from your album; camera Intent = borrow a professional photographer who hands you the photo; own module = you become the photographer with your own camera.

**Slide 4–5 (gallery):** `rememberLauncherForActivityResult(ActivityResultContracts.GetContent())` returns a `Uri`; `launcher.launch("image/*")` opens the picker; **Coil**'s `rememberAsyncImagePainter(uri)` shows it. ⚠️ The slide adds `READ_EXTERNAL_STORAGE`, but the system picker used by `GetContent` needs **no** storage permission (extra).

### 1.1 Manifest declarations (slides 8–9) — EXAM
| Declaration | What it does |
|---|---|
| `<uses-feature android:name="android.hardware.camera"/>` | Tells Google Play the app needs a camera → **prevents installation on devices without one** (`required="true"` by default; set `required="false"` and check at run time to allow them) |
| `<uses-permission android:name="android.permission.CAMERA"/>` | Needed **only if your own module opens the camera** (runtime permission on Android 6+) |
| `WRITE_EXTERNAL_STORAGE` (`maxSdkVersion="18"`) | Save photos to shared storage on very old Android |
| `RECORD_AUDIO` | Record video with sound |
| `ACCESS_FINE_LOCATION` | Geotag photos |
Only declare the extras you really use (least privilege).

**Slide 19 answers:**
1. *"You must obtain permission to enable the camera feature"* — **only partly true**: not needed when you use the existing camera app through an Intent; **required** when you build your own camera with CameraX/Camera2.
2. Prevent install on devices without a camera → `<uses-feature android:name="android.hardware.camera"/>` (required).
3. Quickest way → the **camera Intent** (`MediaStore.ACTION_IMAGE_CAPTURE` / `ACTION_VIDEO_CAPTURE`, or the `TakePicture` contract).

### 1.2 Camera Intent — reading slides 10–11
Slide 10 says "execute with `startActivity()` and set up `onActivityResult()`" — mismatched; the old pair was `startActivityForResult()` + `onActivityResult()` (deprecated, Ch 3). Slide 11 shows the new one:
```
1  create temp file in cacheDir           photoFile = File.createTempFile("photo_", ".jpg", cacheDir)
2  make a content:// URI for it           FileProvider.getUriForFile(context, "${packageName}.fileprovider", photoFile)
3  register TakePicture launcher          rememberLauncherForActivityResult(TakePicture()) { success -> if (success) imageUri = photoUri }
4  launch it (not shown on slide)         cameraLauncher.launch(photoUri)
5  display imageUri                       Image / Coil
```
**Why FileProvider?** The camera app is a *different app*; it cannot write to your private files. A `content://` URI gives it **temporary** permission to write into your file. You must also declare the `<provider android:name="androidx.core.content.FileProvider" …>` in the manifest (not on the slide).

### 1.3 Beyond photos (slides 12–15, 18)
Document scan, text recognition/translate (**ML Kit**), cheque deposit, insurance claims, eye test, indoor navigation with visual positioning. **Barcode scanning (ML Kit)** runs **on the device**, works **without a network** and supports 2D codes such as **QR**.

### 1.4 Decode a scaled image (slides 16–17) — with numbers
Problem: a full-size photo decoded into memory can exhaust RAM ("app runs out of memory"). Fix: decode a **smaller** version that matches the view size using `BitmapFactory.Options.inSampleSize` (a power of 2; first read only the size with `inJustDecodeBounds = true`).
Computed with Python (ARGB_8888 = 4 bytes/pixel; Android's `calculateInSampleSize` for a 600×600 target):
| Photo | inSampleSize | Full size in memory | Decoded size | Saving |
|---|---|---|---|---|
| 4000 × 3000 | **4** | 48,000,000 B = **45.78 MiB** | 1000 × 750 = 3,000,000 B = **2.86 MiB** | **16×** |
| 1920 × 1080 | 1 | 7.91 MiB | 7.91 MiB | none (already ≤ 2× target) |
| 600 × 600 | 1 | 1.37 MiB | 1.37 MiB | none |
Memory falls with the **square** of the sample size (÷4 in each direction → ÷16). Slide 17 calls `decodeScaledBitmapFromUri(...)` without showing it — it does exactly this.

---

## 2. Audio and video playback / 音频与视频 (slides 20–28)

Android keeps **separate audio streams** (music, alarms, notifications, ringer, system sounds, in-call volume…). Most are reserved for system events; apps use **`STREAM_MUSIC`** for music and sound effects. (Extra: newer code uses `AudioAttributes`; the slide's stream-type call is deprecated.)
- **MediaPlayer** plays sound and video, local files or **streams**; **AudioManager** manages audio sources/outputs.
- Codecs: it supports what the platform provides plus some device-specific ones → use the **core media formats** (audio `.3gp .mp3 .mp4 .mid .wav .ogg`; picture `.jpg .gif .png .bmp`; video `.3gp .mp4`) for compatibility.
- Manifest: `INTERNET` (streaming), `WAKE_LOCK` (keep the screen from dimming / the CPU from sleeping while playing).

MediaPlayer states (extra, from the Android docs): `Idle → Initialized (setDataSource) → Prepared (prepare) → Started ⇄ Paused → Stopped → released`.
**Slide 26 reading:** `MediaPlayer().apply { setDataSource(url); prepare() }`; button toggles `pause()` / `start()` and a Boolean `isPlaying` state. ⚠️ `prepare()` is **synchronous** — for network streams it blocks the UI thread; real code uses `prepareAsync()` with a listener (extra).
**Release (slide 27):** a MediaPlayer holds decoder/audio resources → always `release()`; in Compose call it in `DisposableEffect(Unit) { onDispose { mediaPlayer.release() } }` when the composable leaves.

**Slide 28 answers:**
1. *"Free to use any codec"* — **false**: MediaPlayer only supports codecs the platform/device provides; stick to core media formats.
2. `WAKE_LOCK` lets the app keep the **screen from dimming or the processor from sleeping** during playback.
3. **`release()`**.

---

## 3. Sensors / 传感器 (slides 29–46) — EXAM

Three categories (slide 29): **Motion**, **Environmental**, **Position**.

| Category | Sensor | Measures (unit) | Example use |
|---|---|---|---|
| Motion | **Accelerometer** | Acceleration force on x, y, z **including gravity** (m/s²) | Tilt steering in a racing game (slide 35), step counting, screen rotation |
| Motion | **Gravity sensor** | Direction and strength of gravity | Which way is "down" |
| Motion | **Gyroscope** | **Rate of rotation** around x, y, z (rad/s) | Smooth rotation/AR, motion controls |
| Motion | **Rotation vector** | Device **orientation** (fusion of sensors) | Games, AR, compass apps |
| Environmental | **Barometer** | Air pressure (hPa) | Altitude / floor detection; helps GPS with vertical position |
| Environmental | **Light sensor (photometer)** | Illuminance (lux) | Auto-brightness, auto dark mode |
| Environmental | **Thermometer** | Ambient air temperature (°C) | Weather apps |
| Position | **Magnetometer** | Magnetic field strength (µT) → heading | Compass |
| Position | **Orientation** | Angles relative to a coordinate frame | Legacy compass/level (API deprecated) |
| Position | **Proximity** (shown on slides 38–39, not explained) | Distance to a nearby object | Turn the screen off during a call |
Slide 36 (smartwatch) illustrates heart-rate/step sensors; slides 38–39 (Pixel 4 / iPhone X) show the front sensor cluster: ambient-light and proximity sensors, IR camera, dot projector, flood illuminator (face unlock), and Soli radar (motion sense).

### Worked example — what the accelerometer really reads (computed)
At rest it reads **gravity** (≈ 9.81 m/s²), which is why it "senses orientation".
| Phone position | (x, y, z) m/s² | \|a\| | Roll (atan2(y,z)) | Pitch |
|---|---|---|---|---|
| Flat on table, screen up | (0, 0, 9.81) | 9.81 | 0° | 0° |
| Upright, portrait | (0, 9.81, 0) | 9.81 | 90° | 0° |
| Landscape, left side down | (9.81, 0, 0) | 9.81 | 0° | −90° |
| Tilted 30° about x | (0, 4.90, 8.50) | 9.81 | 30° | 0° |
| Sample reading | (0.3, 0.5, 9.7) | 9.72 | 3.0° | −1.8° |
In **free fall** it reads ≈ (0, 0, 0). A sensor that excludes gravity is the separate **linear acceleration** sensor.
Barometer: from standard atmosphere, 1013.25 → 1000 hPa ≈ +111 m; about **0.36 hPa ≈ 3 m ≈ one floor**.

### Using a sensor in code (extra — not in the slides)
```kotlin
val sm = getSystemService(SENSOR_SERVICE) as SensorManager
val acc = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)         // null if the phone lacks it
override fun onResume() { super.onResume(); sm.registerListener(listener, acc, SensorManager.SENSOR_DELAY_NORMAL) }
override fun onPause()  { super.onPause();  sm.unregisterListener(listener) }   // save battery
// listener.onSensorChanged(event) -> event.values[0..2] = x, y, z
```
Register in `onResume`, unregister in `onPause` (same rule as location updates).

### Question 6.3 / Jan 2026 Q4a(iii) — how apps use sensors (model answers)
**Template (5–6 marks):** sensor → what it measures → how the app uses it → benefit.
- **Fitness app:** accelerometer counts steps and detects activity; barometer counts floors climbed; benefit — accurate activity summary without GPS battery cost.
- **ELSA (Jan 2026 Q4a(iii), choose TWO):** (1) **Ambient light sensor** — switches to dark mode/adjusts brightness so financial charts stay readable in bright shops or dim rooms (comfort, accessibility); (2) **Accelerometer/gyroscope** — detects orientation to re-layout dashboards or a "shake to refresh/undo" gesture (convenience). Other valid choices: proximity, magnetometer, GPS for nearby advisory centres, microphone for voice input.

---

## 4. Exam templates: camera / 相机答题模板

**Oct 2025 Q4b(i) "Describe TWO ways an app can handle a camera request" (6 marks)**
1. **Use the existing camera app via an Intent** — the app creates `ACTION_IMAGE_CAPTURE` (or the `TakePicture` contract), the system camera captures, and the photo URI returns; simple, no CAMERA permission.
2. **Build your own camera module (CameraX/Camera2)** — the app shows its own preview and controls; needs the CAMERA permission and more code; allows live processing.
*(A valid third: pick from the gallery when a new photo is not required.)*
**Q4b(ii) "Most suitable way for MyGOV, with justification" (3 marks):** the **existing camera app** — the app only needs to capture a document/photo to upload; no special processing, so the Intent method is quick to develop, needs no CAMERA permission (fewer privacy concerns for a government app) and works on all camera apps/devices.
**Jan 2026 Q4a(i) "Illustrate TWO manifest declarations for the ELSA camera" (6 marks):** (1) `<uses-feature android:name="android.hardware.camera"/>` — Play only offers ELSA to camera phones (or `required="false"` if the camera is optional); (2) `<uses-permission android:name="android.permission.CAMERA"/>` — needed if ELSA runs its own scanner (request at run time). Optional: `RECORD_AUDIO`, storage. Write the XML line, then what it does.
**Q4a(ii) "TWO scenarios ELSA uses the camera" (4 marks):** (1) photograph/scan **business registration documents** to auto-fill the financing application (document scan + text recognition); (2) scan a **QR code** (e.g. to link the ModalNiaga application) or take a profile/premises photo; also video consultation.

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 31 | Accelerometer excludes gravity | `TYPE_ACCELEROMETER` **includes** gravity; excluding it = linear acceleration |
| 33 | Gyroscope "helps the accelerometer" | Measures rotation **rate** (rad/s); used with the accelerometer in fusion |
| 34 | Rotational vector = "turning movements" | Gives device **orientation** |
| 37 vs 42 | Thermometer = ambient air temperature vs "temperature within the device" | Android's ambient sensor measures air; internal battery/CPU temperatures are separate |
| 45 | Magnetometer "determines your location" | Measures the magnetic field → **heading**, not location |
| 44 | Orientation sensor | Deprecated API; use rotation vector |
| 10 | `startActivity()` + `onActivityResult()` | `startActivityForResult()` (old) or the Activity Result API |
| 4 | `READ_EXTERNAL_STORAGE` for the gallery | Not needed for `GetContent` |
| 6 | Existing camera app: "no need permission" | True unless your own manifest declares/uses `CAMERA` |
| 26 | `prepare()` | Blocks UI for streams; use `prepareAsync()` |

Exam strategy: for "which sensor" questions give the slide's sensor and use case; add the correct measurement (e.g. "accelerometer — acceleration including gravity, so it also gives orientation").

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| Gallery / camera Intent / own camera | Pick / borrow / build |
| `uses-feature camera` | Restrict install to camera devices |
| `CAMERA` permission | Only for your own camera module |
| FileProvider | Gives the camera app a temporary `content://` URI to your file |
| `inSampleSize` | Decode ÷N in each dimension; memory ÷N² |
| MediaPlayer | Plays local/streamed audio & video; call `release()` |
| `WAKE_LOCK` | Keep screen/CPU awake during playback |
| Sensor categories | Motion, environmental, position |
| Accelerometer / gyroscope / light / barometer / magnetometer | Acceleration incl. gravity / rotation rate / lux / pressure / magnetic field |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which option needs **no** CAMERA permission? (a) CameraX preview (b) Camera2 API (c) `ACTION_IMAGE_CAPTURE` Intent (d) ML Kit live scanning with own preview
2. `<uses-feature android:name="android.hardware.camera"/>` mainly… (a) requests permission (b) filters devices in Google Play (c) starts the camera (d) records audio
3. An accelerometer at rest lying flat reads about… (a) (0,0,0) (b) (0,0,9.81) (c) (9.81,0,0) (d) (0,9.81,0)
4. What must you always call when finished with a MediaPlayer? (a) `start()` (b) `prepare()` (c) `release()` (d) `wait()`
5. Which sensor helps the GPS with altitude? (a) Light (b) Barometer (c) Gyroscope (d) Proximity

### B. Short answer
1. Name the three ways to obtain a photo in an app and state when each is best.
2. Why is a FileProvider needed for the camera Intent?
3. Why is `inSampleSize` used when loading photos?

### C. Calculation / trace
1. A 3024 × 4032 photo (ARGB_8888) is shown in a 500 × 500 view. Find `inSampleSize` (power of 2 with both dimensions still ≥ the target) and the memory before/after.
2. Accelerometer reads (0, 7.0, 6.87) m/s². Find |a| and the roll angle. What is the phone doing?
3. Order the MediaPlayer states from `MediaPlayer()` to being released, and say where `prepare()` fits.

### D. Thinking
1. Oct 2025 style: describe TWO ways to handle a camera request in a government app and choose the most suitable one.
2. Design a "step and floor counter" app: which sensors, when to register listeners, and how to save battery?

### Answers
**A.** 1-c. 2-b. 3-b. 4-c. 5-b.

**B.**
1. Gallery: no new photo needed. Camera Intent: simple capture without special processing. Own camera module: live preview, scanning or filters.
2. The camera app is another app and cannot write to your private storage; FileProvider gives it a temporary `content://` URI.
3. Decoding a full-size photo needs huge memory (e.g. 45.78 MiB for 4000×3000); decoding a scaled version (÷4 → 2.86 MiB) matches the view and avoids OutOfMemory.

**C.**
1. Sample size: 3024/2 = 1512 ≥ 500 and 4032/2 = 2016 ≥ 500 → try 4: 756/1008 ≥ 500 → 8: 378 < 500 stops → **inSampleSize = 4** (result 756 × 1008). Before: 3024 × 4032 × 4 = 48,771,072 B ≈ **46.5 MiB**; after: 756 × 1008 × 4 = 3,048,192 B ≈ **2.9 MiB** (16× less).
2. |a| = √(0² + 7.0² + 6.87²) = √96.2 ≈ **9.81** (gravity only). Roll = atan2(7.0, 6.87) ≈ **45.5°** — the phone is held still, tilted about 45° from flat.
3. Idle → `setDataSource` → Initialized → **`prepare()`** → Prepared → `start()` → Started ⇄ `pause()` Paused → `stop()` Stopped → `release()`.

**D.**
1. Use section 4 template (Intent and own module) and choose the Intent method with justification.
2. Accelerometer (steps), barometer (floors); register in `onResume` (or a foreground service when tracking continues), unregister in `onPause`; use a low sampling rate/batching; avoid keeping GPS on.

---

## Links to other chapters / 与其他章节的联系
- Intents and result APIs → **Chapters 1 and 3**; permissions and manifest → **Chapters 1 and 5**.
- Saving photos/files and Room → **Chapter 4.1**; background upload of photos → **Chapter 4.2**.
- Photo memory and image density → **Chapter 2.3**; store listing (uses-feature affects device filtering) → **Chapter 7**.
