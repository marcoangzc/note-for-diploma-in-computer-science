# AMIT3353 — Chapter 3: Mobile Application Models (Activity, Intent, Lifecycle)
# 第 3 章：Activity、Intent 与生命周期（中英双语）

> The slides give the lifecycle diagram and code fragments but never trace a real scenario (Home button, rotation, opening a second screen), leave several questions unanswered, use Java/Kotlin mixed code that will not compile, and treat `LaunchedEffect` as if it were an Activity callback. This note adds traces, corrected code, matching rules for intent filters and answer templates for the two past-paper questions (lifecycle diagram; explicit vs implicit).
> 中文：slide 给了生命周期图，但没有用真实场景（按 Home、旋转屏幕、跳到第二个页面）逐步走一遍；代码有 Java/Kotlin 混用的错误；Compose 部分也讲得不准确。这里全部补上，并给出历年考题的答题模板。

---

## 0. One-sentence overview / 一句话总结

An **Activity** is one screen; Android keeps Activities on a **back stack**; an **Intent** asks the system to start one (explicit = by name, implicit = by action, matched to an **intent filter**); and every Activity moves through a **lifecycle** (`onCreate → onStart → onResume → onPause → onStop → onDestroy`) where you must save state.
中文：Activity = 一个屏幕；系统用 back stack 管理；Intent 启动别的 Activity（explicit 指名，implicit 指动作）；每个 Activity 都有生命周期，要在正确的回调里保存/释放东西。

| Topic | Slides | Exam relevance |
|---|---|---|
| Activity, manifest, back stack | 3–12 | Purpose, why declare, stack |
| Intent (explicit, implicit, parts) | 13–38 | Oct 2025 Q2c; Jan 2026 Q2c |
| Intent filter, results | 39–44 | Code reading |
| Lifecycle & callbacks | 45–59 | Jan 2026 Q2b (diagram, 9 marks) |
| Saving state, config change | 60–63 | Rotation, multi-window |

---

## 1. Activity, manifest and back stack / Activity 与返回栈 (slides 3–12)

**English.** An Activity = **one screen (UI)**. One is the *main* (launcher) Activity; others can be started by the same app or by other apps. It **must be declared** in the manifest (`<activity android:name=".ExampleActivity"/>`), otherwise the system does not know it exists. `finish()` closes the current Activity; `finishActivity()` closes another Activity you started earlier.
**中文：** 不在 manifest 里声明的 Activity，系统根本找不到，也就启动不了。

**Back stack (LIFO — last in, first out).** Starting a new Activity pushes it; the old one is *stopped but kept*; Back pops the top one and the previous one resumes.

| Step | Action | Stack (top on right) | Visible |
|---|---|---|---|
| 1 | Launch app | [A1 (Main)] | A1 |
| 2 | A1 starts A2 | [A1, A2] | A2 |
| 3 | A2 starts A3 | [A1, A2, A3] | A3 |
| 4 | Back | [A1, A2] (A3 destroyed) | A2 |
| 5 | Back | [A1] (A2 destroyed) | A1 |

### Slide 12 answers
1. **Purpose:** provides a window/screen for the UI and the entry point for user interaction.
2. **Why declare in manifest:** the system reads the manifest first; an undeclared Activity is invisible and cannot be started.
3. **Data structure:** a **stack** (the back stack, LIFO).
4. **User navigates away:** the Activity is **stopped** (`onPause` → `onStop`) but kept on the stack with its state; the system may destroy it later if memory is needed.

---

## 2. Intent / Intent 意图 (slides 13–38)

An Intent is a **message** asking Android to start a component (mainly an Activity). Two types:

| | **Explicit** | **Implicit** |
|---|---|---|
| Says | *Exactly which* component | *What to do* (an action) |
| Target | Your own app (usually) | Any app that can do it |
| Example | Home screen → Settings screen | Share text, open a map, send email |
| If nothing handles it | — | Crash (`ActivityNotFoundException`) unless you check |

**Five parts of an Intent (slide 14):**
| Part | Meaning | Example |
|---|---|---|
| Component name | Target class (explicit only; use for Services, for security) | `ComposeActivity::class.java` |
| Action | The verb; decides how data/extras are read | `ACTION_VIEW`, `ACTION_SEND` |
| Data | URI and/or MIME type of what to act on | `tel:031234567`, `geo:47.6,-122.3`, `text/plain` |
| Category | Extra info about who should handle it (optional) | `CATEGORY_LAUNCHER`, `CATEGORY_BROWSABLE` |
| Extra | Key-value pairs carried along | `putExtra("MSG", "hi")` |

### 2.1 Explicit intent — worked trace (slides 20–27)
```kotlin
// In Activity A
val intent = Intent(this, DisplayMessageActivity::class.java).apply {
    putExtra(EXTRA_MESSAGE, "Hello")          // key-value pair
}
startActivity(intent)
// In Activity B
val message = intent.getStringExtra(EXTRA_MESSAGE)   // "Hello"
```
| Step | Who | What happens |
|---|---|---|
| 1 | Activity A | Creates an Intent naming `DisplayMessageActivity` and puts extra `MESSAGE = "Hello"` |
| 2 | Android system | Looks for that component in the app (found by name — no matching needed) |
| 3 | System | Starts B; A goes to `onPause/onStop` |
| 4 | Activity B | Reads `intent.getStringExtra(...)` → "Hello" |
Convention: key names are prefixed with the package (`"com.example.myfirstapp.MESSAGE"`) to avoid clashing with other apps.

### 2.2 Implicit intent — worked trace (slides 28–37)
1. Activity A creates an Intent with an **action** (+ data/type).
2. The system searches **all apps' intent filters** for a match.
3. One match → starts it. **Several matches → a chooser dialog** ("Complete action using…", slide 35). **No match → crash** (slide 30) — so check first:
```kotlin
if (sendIntent.resolveActivity(packageManager) != null) startActivity(sendIntent)
else { /* tell the user no app can handle this */ }
```
From **API 30**, package visibility rules mean you must also declare the intents you query in the manifest with `<queries>` (slide 37).

**Corrected Kotlin for the slide 33 email intent** (the slide mixes Java/Kotlin and uses an old constant):
```kotlin
val emailIntent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"                                        // not HTTP.PLAIN_TEXT_TYPE
    putExtra(Intent.EXTRA_EMAIL, arrayOf("jon@example.com"))    // EXTRA_EMAIL expects a String array
    putExtra(Intent.EXTRA_SUBJECT, "Email subject")
    putExtra(Intent.EXTRA_TEXT, "Email message text")
}
```
Slide 34: `ACTION_DIAL` opens the dialer with the number filled in (no permission needed); `ACTION_VIEW` with a `geo:` URI opens a map. (`ACTION_CALL` would place the call directly and needs `CALL_PHONE` permission — extra.)

### 2.3 Slide 38 answers
1. **Difference:** explicit names the exact component (usually inside your app); implicit only declares an action and lets the system choose any capable app.
2. a. Share a website URL → **implicit** (`ACTION_SEND`, `text/plain`) — the user picks any messaging/social app.
   b. Listen to an audio file downloaded from the Internet → **implicit** (`ACTION_VIEW` with an audio MIME type) so any installed player can open it (explicit only if you have your own player Activity).
   c. Change the app's sound profile to silent → **explicit** — you open your own Settings screen/component (if the question means the *phone's* profile, an implicit intent to system sound settings or `AudioManager` is used instead).

### 2.4 Worked example — Oct 2025 Q2c (explicit or implicit? 3 marks each)
| Task in MyGOV | Type | Justification |
|---|---|---|
| (i) Home screen → Settings screen | **Explicit** | Target is a known Activity inside the same app |
| (ii) Send an email to support | **Implicit** | `ACTION_SEND`/`mailto:`; any email app can handle it |
| (iii) Create a new driving-licence-renewal request | **Explicit** | Own request-form Activity/screen; carries extras such as the licence number |
| (iv) Open a map to the nearest UTC | **Implicit** | `ACTION_VIEW` + `geo:` URI; the Maps (or another map) app handles it |

### 2.5 Exam template — Jan 2026 Q2c "Explain TWO intent types with an example each in ELSA" (10 marks)
For each type: **definition → how it works (component name vs action + filter) → ELSA example → small code/extra**.
- *Explicit:* ELSA dashboard → "Financing Application" Activity, carrying `applicationId` with `putExtra`.
- *Implicit:* ELSA asks the system to open the ModalNiaga web page (`ACTION_VIEW` + `https://` URI) or share the diagnostic report (`ACTION_SEND`, `text/plain`); the system finds a browser/messaging app via intent filters.

---

## 3. Intent filter / Intent 过滤器 (slide 39)

**English.** An `<intent-filter>` in the manifest **advertises which implicit intents a component can receive**. Slide 39: `ShareActivity` accepts `ACTION_SEND` with `text/plain` and category `DEFAULT` (`startActivity` adds `DEFAULT` automatically, so a filter must include it to be found by implicit intents).
**Matching rule of thumb:** action must be listed; every category in the intent must be listed; data type/URI must match.

| Intent sent | Matches `ShareActivity` filter? | Result |
|---|---|---|
| `ACTION_SEND`, type `text/plain` | ✔ action, category, MIME | Starts ShareActivity |
| `ACTION_SEND`, type `image/jpeg` | ✘ MIME differs | Not this app (crash if nobody handles it) |
| `ACTION_VIEW`, `http://…` | ✘ action differs | Not this app |
Extra: on Android 12+ an Activity with an intent filter must set `android:exported`.

---

## 4. Getting a result back / 取得返回结果 (slides 40–44)

**English.** Sometimes A starts B *to get something back* (pick a contact, pick a photo). Old way: `startActivityForResult(intent, REQUEST_CODE)` and override `onActivityResult(requestCode, resultCode, data)` — the **request code** tells which request the answer belongs to; **result code** (`RESULT_OK`) says success; `data` carries the answer. It is **deprecated**. New way (slide 44): the **Activity Result API** — `registerForActivityResult(ActivityResultContracts.GetContent()) { uri -> … }` then `launch("image/*")`; no request codes.
Slide 43 detail: the `data` parameter of `onActivityResult` should be nullable (`Intent?`). Compose equivalent: `rememberLauncherForActivityResult` (Ch 6).

---

## 5. The Activity lifecycle / Activity 生命周期 (slides 45–59) — EXAM

**Why it exists:** the system creates, hides and destroys screens as the user moves around and as memory runs low; the callbacks let *you* start work, pause work and save data at the right moment.

```
        Launched
           |
       onCreate()  ---- one-time setup (UI, ViewModel, listeners)
           |
       onStart()   <----------------- onRestart() <-----------+
           |                                                   |
       onResume()  <------------- user returns ---+            |
           |                                       |            |
     [ RUNNING: visible + interactive ]           |            |
           | another activity in front             |            |
       onPause()  ---- (partly visible) ----------+            |
           | no longer visible                                   |
       onStop()   ------------ user returns -----------------+
           |
   finishing / system needs memory
           |
      onDestroy()  --> Activity shut down       (process may also be killed: onDestroy skipped)
```

| Callback | Called when | What to do | Don't |
|---|---|---|---|
| `onCreate` | Activity is created (once per instance) | Set content/UI, create ViewModel, register listeners, restore state | Heavy work that blocks the UI |
| `onStart` | Becomes **visible** | Register receivers that update the UI, lightweight UI data | — |
| `onResume` | In **foreground**, interactive (first time and after every pause) | Start camera preview, animations, sensors | Assume it runs only once |
| `onPause` | User is leaving; may still be partly visible (multi-window) | **Quickly** commit unsaved data, pause animations/media, release foreground-only sensors | Long or heavy operations (blocks the next screen) |
| `onStop` | No longer visible | Release almost everything, heavier saves (database) | — |
| `onDestroy` | `finish()` called, or system/config change destroys it | Release all resources | Rely on it: the system **may skip** it |

State table (slide 47): Resumed = visible + interactive; Paused = partly visible, not interactive; Stopped = not visible; Destroyed = gone.
⚠️ "Code execution: No" for Paused/Stopped is a simplification — your callbacks run, background threads and Services can keep running; what stops is *UI interaction*.

### Traces of real scenarios (standard documented order; not run on a device)
| Scenario | Callback sequence |
|---|---|
| Launch app | `onCreate → onStart → onResume` |
| Press **Home** | `onPause → onStop` |
| Return from Recents | `onRestart → onStart → onResume` |
| Press **Back** on the last screen (finish) | `onPause → onStop → onDestroy` |
| **A starts B** (full screen) | A: `onPause` → B: `onCreate → onStart → onResume` → A: `onStop` |
| **Back** from B to A | B: `onPause` → A: `onRestart → onStart → onResume` → B: `onStop → onDestroy` |
| Permission dialog / transparent overlay on top | only `onPause` (Activity still partly visible), then `onResume` |
| **Rotate** the phone (default) | `onPause → onStop → onSaveInstanceState* → onDestroy → onCreate → onStart → onRestoreInstanceState → onResume` |
\*On Android 9 (API 28)+ `onSaveInstanceState` is called **after** `onStop`; on older versions before it.
⚠️ **A starts B:** B is created *before* A is stopped — do not release something A and B both need in A's `onStop` and expect B to have it already.

### Slide 59 answers
1. **Why `onCreate` and `onPause` are important:** `onCreate` is where you build the UI and initialise the Activity — it runs once and is mandatory. `onPause` is the first (and often only guaranteed) warning that the user is leaving, so it is where unsaved data must be committed and CPU-hungry work paused.
2. **Scenario with no `onPause`/`onStop`:** the process is killed without warning (crash, force stop, battery dies), or `finish()` is called inside `onCreate()` — the system then goes straight to `onDestroy()`.
3. **Which callback?** a. *Play background music* — start in `onStart`/`onResume` and pause in `onPause` while the screen is used; music that must continue after leaving the app belongs in a **foreground Service** (Ch 4.2). b. *Save game level* — `onPause` (quick commit; heavier saves in `onStop`). c. *Connect to a server* — `onStart` (or `onResume`), and disconnect in `onStop`.
4. **Two callbacks to save data to a database:** `onPause` (small, quick commit of unsaved changes) and `onStop` (heavier database writes).

### Exam template — Jan 2026 Q2b "Use a diagram to explain the activity lifecycle" (9 marks)
Draw the diagram above (all 6 callbacks + `onRestart`, arrows for "another activity in front", "user returns", "process killed/finish"). Then 1 line per callback (marks ≈ diagram 3 + explanation 6). Mention the states Resumed/Paused/Stopped/Destroyed.

---

## 6. Configuration change and saving state / 配置变化与状态保存 (slides 54–55, 60–63)

**English.** A **configuration change** (rotation, language, keyboard/input device) makes the system **destroy and recreate** the Activity (`onPause → onStop → onDestroy → onCreate…`). Any UI data held only in the old instance (typed text, scroll position) is lost unless saved.
- **Instance state** = key-value pairs in a **Bundle**. Save in `onSaveInstanceState(outState)`, restore in `onCreate(savedInstanceState)` or `onRestoreInstanceState()`. The system already saves and restores standard views that have an id (e.g. an EditText's text) — call `super.onSaveInstanceState(outState)` to keep that (slide 62).
- Compose: `remember` state is **lost** on rotation; use `rememberSaveable` (survives rotation and process death) or a `ViewModel` (survives rotation, not process death — Ch 4.1). (Extra, not in slides.)
**Analogy:** rotating the phone is like moving a desk to another room — the desk is rebuilt from scratch; the Bundle is the box of papers you carried across.

### Slide 63 — multi-window / multitasking (model answer)
Save important data as early as possible: commit unsaved data in `onPause` (an Activity can be visible in multi-window but not focused), do heavier saves in `onStop`, keep UI state in a Bundle (`onSaveInstanceState`) or `ViewModel` so it survives recreation, restore it in `onCreate`/`onRestoreInstanceState`, and stop CPU/sensors in `onPause` while restarting them in `onResume`.

---

## 7. Compose and the Activity lifecycle / Compose 与生命周期 (slides 56–58)

A **composable has its own lifecycle**: it *enters* composition, may *recompose* many times, and *leaves*. It has no `onStart`/`onResume`. To run code when the composable appears use `LaunchedEffect(key)`; to react to **Activity** lifecycle events you observe the `LifecycleOwner`.
⚠️ Slide 49 shows `LaunchedEffect(Unit) { Log.d("onStart Equivalent") }` — this runs **once when the composable enters composition**, *not* when the Activity starts, so it is not an `onStart` equivalent. Slide 57 adds an observer inside `LaunchedEffect` and never removes it (a **leak**). Correct pattern (standard, not compiled here):
```kotlin
val owner = LocalLifecycleOwner.current
DisposableEffect(owner) {
    val obs = LifecycleEventObserver { _, e -> if (e == Lifecycle.Event.ON_RESUME) { /* … */ } }
    owner.lifecycle.addObserver(obs)
    onDispose { owner.lifecycle.removeObserver(obs) }      // clean up
}
```
Slide 58: `rememberCoroutineScope()` gives a scope to launch coroutines from event handlers (e.g. a button click).

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 47 | Paused/Stopped: code execution "No" | Callbacks run; background threads/services can continue; UI interaction stops |
| 47 | Instance state "Saved" for all but destroyed | After destroy/recreate the Bundle restores it; simplified |
| 49, 56, 57 | `LaunchedEffect` = lifecycle callback; observer in `LaunchedEffect` | Not equivalent; use `DisposableEffect` + remove observer |
| 33 | `HTTP.PLAIN_TEXT_TYPE`, mixed Java/Kotlin, `EXTRA_EMAIL` string | `type = "text/plain"`, `arrayOf(...)` |
| 40 | `startActivityForResult` | Deprecated; use Activity Result API (slide 44) |
| 43 | `data: Intent` | `data: Intent?` |
| 52 | "Commit changes in onPause" but "execution must be very brief" | Small commit in `onPause`; heavy work in `onStop` |
| 54 | `onDestroy` releases everything | May be skipped if the process is killed |

Exam strategy: if a question asks "which callback…", give the slide's callback and add a one-line reason.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| Activity | One screen; declared in manifest |
| Back stack | LIFO stack of Activities |
| Explicit / implicit intent | By component name / by action |
| Action, Data, Category, Extra | Verb, URI/MIME, extra info, key-value payload |
| Intent filter | Manifest entry that advertises which implicit intents a component accepts |
| `resolveActivity` | Check that something can handle the intent |
| Lifecycle | `onCreate → onStart → onResume → onPause → onStop → onDestroy` (+ `onRestart`) |
| Instance state | Bundle saved in `onSaveInstanceState` |
| `finish()` | Close this Activity |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which callback is called **every time** the Activity returns to the foreground? (a) onCreate (b) onResume (c) onDestroy (d) onRestart only
2. What happens when an implicit intent has no matching app and no check is made? (a) Nothing (b) A chooser opens (c) App crashes (d) The manifest is edited
3. What is the data structure for Activities? (a) Queue (b) Heap (c) Stack (d) Tree
4. Which extra is required for a filter to receive implicit intents from `startActivity()`? (a) category DEFAULT (b) category LAUNCHER (c) data scheme http (d) exported=false
5. On rotation (default), the Activity is… (a) paused only (b) destroyed and recreated (c) restarted with `onRestart` (d) unchanged

### B. Short answer
1. Explain the difference between `onPause` and `onStop`.
2. Why is `resolveActivity` used before `startActivity` for an implicit intent?
3. What is the Bundle in `onSaveInstanceState` and why is it needed?

### C. Trace
1. Write the callback sequence when Activity A starts Activity B and the user presses Back.
2. An intent has `ACTION_SEND`, type `image/png`. Filters: F1 = SEND + `text/plain`; F2 = SEND + `image/*`; F3 = VIEW + `image/*`. Which match?
3. Back stack trace: start Main (M), M→Details (D), D→Edit (E), Back, Back, Back.

### D. Thinking
1. Draw the lifecycle diagram and explain each callback (Jan 2026 Q2b style, 9 marks).
2. A game must not lose the current level when the phone rotates or when the user takes a call. Which callbacks and mechanisms do you use?

### Answers
**A.** 1-b. 2-c. 3-c. 4-a. 5-b.

**B.**
1. `onPause`: activity is leaving/partly visible; quick commit, pause animations/media. `onStop`: no longer visible; release most resources and do heavier saves.
2. If nothing can handle the intent `startActivity` throws and the app crashes; `resolveActivity(packageManager) != null` lets you show a message instead (from API 30 also declare `<queries>`).
3. A key-value store the system keeps for the Activity's UI state so it can be restored after destruction (rotation or process kill).

**C.**
1. A: `onPause` → B: `onCreate → onStart → onResume` → A: `onStop`. Back: B: `onPause` → A: `onRestart → onStart → onResume` → B: `onStop → onDestroy`.
2. F2 matches (`image/*` covers `image/png`). F1 no (text). F3 no (action VIEW ≠ SEND). → only F2.
3. [M] → [M, D] → [M, D, E] → Back [M, D] → Back [M] → Back [] (app exits).

**D.**
1. Use the diagram and callback table in section 5; add states (Resumed, Paused, Stopped, Destroyed).
2. Rotation: keep the level in a `ViewModel` or Bundle (`onSaveInstanceState` / `rememberSaveable`). Phone call: `onPause` is called → pause the game loop and commit the level (SharedPreferences/DataStore); resume in `onResume`. Heavier save in `onStop`.

---

## Links to other chapters / 与其他章节的联系
- Intents and components → **Chapter 1**; navigation stack in Compose → **Chapter 2.2**.
- `ViewModel`, SharedPreferences/DataStore for saving → **Chapter 4.1**; Service/WorkManager → **Chapter 4.2**.
- Location updates start in `onStart/onResume` and stop in `onPause/onStop` → **Chapter 5**; camera/media release in `onPause`/`onDispose` → **Chapter 6**.
