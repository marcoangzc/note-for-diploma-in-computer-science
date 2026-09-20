# AMIT3353 — Chapter 4.1: Saving Data
# 第 4.1 章：数据存储（SharedPreferences / DataStore / Files / Room / ViewModel / Coroutine）（中英双语）

> The slides list the storage options but never say **how to choose one**, contain broken snippets (`@Entity` without a comma, a file example that closes streams twice), say SharedPreferences can be "public", and promise "NoSQL – Firebase" with no Firebase content at all. This note gives the decision rules, real SQL output from a test database, an explanation of ViewModel/Repository/coroutines, and answers for the past-paper "choose the storage method" questions.
> 中文：slide 只列出各种存储方式，没有教你「怎么选」；代码有错；「Firebase」章节其实是空的。这里补上选择规则、实际跑过的 SQL 结果、ViewModel/Repository/Coroutine 的讲解和考题模板。

---

## 0. One-sentence overview / 一句话总结

Choose **SharedPreferences/DataStore** for small settings, **files** for big blobs like photos and documents, **SQLite via Room** for structured repeating records, and wrap them in **Repository + ViewModel + coroutines** so data survives rotation and never blocks the UI thread.
中文：小设置 → SharedPreferences/DataStore；大文件 → 文件；结构化多条记录 → Room(SQLite)；再用 Repository + ViewModel + Coroutine 组织，保证旋转不丢数据、不卡主线程。

| Topic | Slides | Exam relevance |
|---|---|---|
| SharedPreferences, DataStore | 3–11 | Jan 2026 Q3b(ii) "Preferred language" |
| Files: internal vs external | 12–21 | Oct 2025 Q3b (table, 6 marks); Jan 2026 Q3b(iii) |
| SQLite and Room | 22–35 | Jan 2026 Q3b(i) "Training progress" |
| ViewModel, Repository, LiveData | 36–57 | "Purpose of Activity/ViewModel/Repository" |
| Coroutines | 58–63 | Purpose; why not on main thread |
| NoSQL / Firebase | 64–65 | SQL vs NoSQL |

---

## 1. Which storage should I use? / 怎么选 (slide 3, question 4.1.3)

| Question about the data | Use |
|---|---|
| A few simple values (a setting, a flag, last screen) | **SharedPreferences** (or DataStore) — key-value |
| A large file (photo, PDF, audio, JSON download) | **Files** (internal or external storage) |
| Many similar records you search/sort/join (contacts, orders, progress per module) | **SQLite / Room** |
| Data shared by all devices or users | A server database / **Firebase** (Ch 4.2) |

Analogy / 类比: SharedPreferences = sticky notes on the fridge; Files = boxes in the store room; SQLite = a filing cabinet with an index.

### Exam template — Jan 2026 Q3b: pick the method for ELSA data (3 marks each)
| Data | Method | Justification |
|---|---|---|
| (i) Training progress | **SQLite (Room)** | Many structured, repeating records (module id, score, date) that must be queried and updated per module. *(If only "last completed module" is kept, SharedPreferences is acceptable — say which you assume.)* |
| (ii) Preferred language | **SharedPreferences** | One small key-value pair (`language = "ms"`), read at every start |
| (iii) Business registration documents | **Data files** | Large files (PDF/scan images), not key-value or table data; stored in app-private internal storage (or uploaded to the server) |

---

## 2. SharedPreferences and DataStore / 键值存储 (slides 4–11)

**English.** SharedPreferences stores **private primitive values** (boolean, float, int, long, String) as key-value pairs in an XML file. Values **persist across sessions**, even if the app is killed.
Two ways to get it (slide 5, figure slide 6):
| | `getSharedPreferences(name, mode)` | `getPreferences(mode)` |
|---|---|---|
| Called on | any `Context` | an `Activity` |
| Files | **Many**, chosen by name | **One** per Activity (named after the Activity) |
| Shared by | all Activities of the app | that Activity only |
```kotlin
val prefs = getSharedPreferences("settings", Context.MODE_PRIVATE)
prefs.edit().putString("language", "ms").apply()            // write (apply = asynchronous)
val lang = prefs.getString("language", "en")                 // read, "en" = default if missing
```
**Slide 11 answers:** 1) `getPreferences` = one file per Activity; `getSharedPreferences` = many named files usable from any Context. 2) A SharedPreferences file can be accessed by **a. multiple Activities — yes** (same file name); **b. multiple apps — no in modern Android**: slide 3's "Private or Public" is an old idea (`MODE_WORLD_READABLE/WRITEABLE` are deprecated and throw `SecurityException` on API 24+). Use a ContentProvider to share.

### DataStore (Compose, slides 7–10)
DataStore replaces SharedPreferences: **asynchronous** (uses coroutines and `Flow`), so it never blocks the UI.
- `val Context.dataStore by preferencesDataStore(name = "settings")` — an **extension property** on Context (so `context.dataStore` works anywhere) created by a **property delegate** (`by`); declare it once at top level.
- **Write:** `context.dataStore.edit { prefs -> prefs[key] = value }` — `edit` is a **suspend function**, so call it inside a coroutine.
- **Read:** `context.dataStore.data.map { prefs -> prefs[key] ?: "Default Value" }` gives a `Flow<String>` (a stream that emits each time the value changes); `.first()` takes the current value once (slide 8).
Keys are typed: `stringPreferencesKey("example_key")`.

---

## 3. Files: internal vs external storage / 文件存储 (slides 12–21) — EXAM

| Characteristic | **Internal** | **External** |
|---|---|---|
| Removable | No | Possible (SD card) |
| Availability | Always | Not always (SD removed, USB mounted) |
| Accessibility | Only your app (private) | World-readable; user can modify |
| Permission | Not needed | Was needed (older Android) |
| After app uninstall | Deleted | Private area: deleted; public area (e.g. Pictures): stays |
This is exactly the **Oct 2025 Q3b(i)** table (removability, availability, accessibility). Write three rows, one line each.

- Internal: `File(context.filesDir, "report.txt")`; check `getFreeSpace()` / `getTotalSpace()` before writing to avoid I/O errors (slide 14).
- External: check the state first (`Environment.getExternalStorageState()` is `MEDIA_MOUNTED`, slide 18). Two kinds: **public** (all apps; stays after uninstall) and **private/app-specific** (`getExternalFilesDir()`; deleted with the app) — slides 17, 19.

**Storage guide (slide 20):**
| Type | Content | Other apps can access? | Removed on uninstall? |
|---|---|---|---|
| App-specific files | For your app only | No | Yes |
| Media | Photos, audio, video | Yes (with permission) | No |
| Documents & other files | Downloads, shareable docs | Yes | No |
| App preferences | Key-value | No | Yes |
| Database | Structured data | No | Yes |
Modern Android (10+) uses **scoped storage** (extra): apps read/write their own dirs freely, and use MediaStore / system pickers for shared files; `READ/WRITE_EXTERNAL_STORAGE` are being phased out.

⚠️ **Slide 15 code smell:** `file.bufferedWriter().use { out -> out.write(text); out.close() }` — `use` already closes the writer, so `out.close()` is redundant; and `file.bufferedReader().readText()` followed by `file.bufferedReader().close()` closes a *different, new* reader (the first is never closed). Simpler and correct: `file.writeText(text)` and `file.readText()` (they open and close for you).

### Slide 21 answers
1. Files the user should open on a computer → **external** storage (world-readable/visible over USB).
2. Built-in non-removable memory that a computer can access — is it "internal"? **No.** "Internal/external" in Android describes **access rules**, not hardware: that visible, shared partition counts as *external* (primary shared storage) even though it cannot be removed. Internal = private app area.

### Exam template — Oct 2025 Q3b(ii) "ONE local storage method for internal and external, with a MyGOV content example" (4 marks)
Internal → **Files (or SharedPreferences) in `filesDir`**: private cache of the user's profile/session data. External → **Files in the public Documents/Downloads area**: a PDF receipt of a paid fine that the user wants to open with a file manager or computer. Give method + example + one reason each.

---

## 4. SQLite and Room / 数据库 (slides 22–35)

**English.** SQLite is a small **embedded relational database**: the whole DB is one file inside the app, no server. Storage classes (slide 23): `NULL`, `INTEGER`, `REAL`, `TEXT`, `BLOB` (images/audio/other binary). Verified with a real SQLite: `typeof()` of `42, 3.14, 'hi', x'DEADBEEF', NULL` → `integer, real, text, blob, null`.
**Room** = a library on top of SQLite so you write Kotlin classes instead of raw SQL strings and get compile-time checks. Three components (slide 24):
| Component | What it is | Slide 27–30 code |
|---|---|---|
| **Entity** | A table (class = table, property = column) | `@Entity data class User(@PrimaryKey val uid: Int, …)` |
| **DAO** (Data Access Object) | Interface with the methods to read/write | `@Dao interface UserDao { @Query… @Insert… @Delete… }` |
| **Database** | The holder / access point | `@Database(entities=[User::class], version=1) abstract class AppDatabase : RoomDatabase() { abstract fun userDao(): UserDao }` |
Four steps: (1) Entity, (2) DAO, (3) AppDatabase abstract class, (4) `Room.databaseBuilder(applicationContext, AppDatabase::class.java, "database-name").build()`.

### Worked example — the slide-29 DAO queries, run on real SQLite
Table `user(uid, first_name, last_name)` with rows (1, Alice, Tan), (2, Calvin, Lee), (3, Jane, Ong), (4, Mark, NULL):
| DAO method | SQL | Result (actual output) |
|---|---|---|
| `getAll()` | `SELECT * FROM user` | 4 rows |
| `loadAllByIds(intArrayOf(1,3))` | `… WHERE uid IN (1,3)` | Alice Tan, Jane Ong |
| `findByName("Alice","Tan")` | `… first_name LIKE 'Alice' AND last_name LIKE 'Tan' LIMIT 1` | Alice Tan |
| `findByName("alice","tan")` | same, lower case | still Alice Tan (**LIKE ignores case for ASCII**) |
| `findByName("Bob","X")` | — | no row (Kotlin: return type must be nullable) |
| `delete(user2)` | `DELETE … WHERE uid = 2` | remaining uids: 1, 3, 4 |
Also verified: a **composite primary key** rejects a duplicate pair (`UNIQUE constraint failed`), and a **foreign key** insert with a non-existing parent fails with `FOREIGN KEY constraint failed` (foreign keys must be enabled in SQLite; Room enables them for `@ForeignKey`).

⚠️ **Slide 28 code is broken as printed:** `@Entity(tableName = "users" primaryKeys = …)` is missing a comma; the foreign-key snippet uses `parentColumns = "id"` although slide 27's key is named `uid`. Correct: `@Entity(tableName = "users", primaryKeys = ["firstName", "lastName"])`.
⚠️ **Threading:** DAO methods on slide 29 are plain functions; if called on the main thread Room throws an `IllegalStateException` (slide 32: "don't use Room on the UI thread"). Make them `suspend fun` or return `Flow` and call from a coroutine.
⚠️ Slide 25 shows old dependencies (`room 2.3.0`, `annotationProcessor`; Kotlin uses `kapt`/KSP) — treat as illustrative.
**Database Inspector** (slide 33): Android Studio tool to view, query and edit the app's database while it runs.

### Slide 34–35 answers
- **Entity** = one table; **DAO** = methods to access the database (query, insert, delete); **Room** = persistence library that wraps SQLite with these abstractions.
- **myhome.com.my — TWO techniques:** (1) **Data files** for uploaded media (photos/videos stored as files — external/media storage — then uploaded); (2) **SQLite via Room** for comments and property locations (repeating structured rows: property id, comment, latitude, longitude, time), synced to the server. Justify each with the data type.

---

## 5. ViewModel, Repository, LiveData/StateFlow / 架构组件 (slides 36–57)

**Problem (slides 38–40):** on rotation the Activity is destroyed and recreated, so UI data held in it is destroyed and reloaded.
**ViewModel (slides 37, 41–43):** holds UI data and **survives configuration changes** — the new Activity instance re-attaches to the *same* ViewModel.
```
 without ViewModel:   Activity(data) --rotate--> destroy Activity+data --> create new Activity, reload data
 with ViewModel:      Activity --rotate--> destroy Activity only --> new Activity attaches to same ViewModel (data still there)
```
**Repository (slide 45):** one clean API for saving/loading; hides *where* data comes from and decides e.g. "use the network or the cached DB copy?".
**Architecture (slides 44, 47–48):**
```
 UI (Activity/Compose)  ->  ViewModel  ->  Repository  ->  Room (DAO + Entity + SQLite)
                                                       \->  Network (API)
```
| Layer | Job (slide 49 answers) |
|---|---|
| Activity | Draw the UI and receive user interaction |
| ViewModel | Hold UI data; survive rotation |
| Repository | API for saving/loading app data from DB or network |
| Entity / DAO / SQLite | Table / methods / relational database (slide 46) |

**LiveData (slides 50–56):** an **observable, lifecycle-aware** data holder. Flow: (1) UI attaches an **Observer**; (2) new data arrives (`setValue`); (3) the observer runs and updates the UI — only while the UI is active (no crash/leak when it is gone). Pattern (slide 54): `private val _user = MutableLiveData<User>()` (writable, private) and `val user: LiveData<User> get() = _user` (read-only, public) — so only the ViewModel can change it.
**Compose: StateFlow (slide 57):** a stream that always holds the latest value; the recommended UI-state holder for Compose:
```kotlin
class UserVm : ViewModel() { private val _u = MutableStateFlow(User()); val u: StateFlow<User> = _u }
// in a composable:  val user by vm.u.collectAsState()
```
(not compiled here; standard pattern.) Slide 54 typos: `saveInstanceState` should be `savedInstanceState`.

---

## 6. Coroutines / 协程 (slides 58–63)

**English.** A coroutine is lightweight **asynchronous** code that can *suspend* (pause without blocking a thread) — used for long tasks (disk, network) so the **main (UI) thread** stays free and the app never freezes; it gives "main-safety" (you may call it from the main thread).
| | `launch` | `async` |
|---|---|---|
| Returns | a `Job` (no result) — "fire and forget" | `Deferred<T>`; get the result with `await()` |

**Scopes (slide 61):** `GlobalScope` — lives as long as the whole app process (discouraged: easy to leak); `lifecycleScope` — cancelled when the **Activity** is destroyed; `viewModelScope` — cancelled when the **ViewModel** is cleared. (The slide's "Resources High/Medium/Low" is a rough idea, not an official property.)

### Slide 62 trace (output verified with an equivalent Java daemon-thread program; the Kotlin compiler was not available)
```kotlin
GlobalScope.launch { delay(1000L); println("World!") }   // background
println("Hello,")                                       // main thread continues at once
Thread.sleep(2000L)                                     // keeps the JVM alive
```
| Time | Main thread | Coroutine |
|---|---|---|
| 0 s | starts coroutine, prints **Hello,** | suspended in `delay` (1 s) |
| 1 s | sleeping | prints **World!** |
| 2 s | wakes, `main` ends | — |
Output: `Hello,` then `World!`. **Without the `Thread.sleep(2000)`** the program ends at once and `World!` is never printed (verified: GlobalScope coroutines don't keep the process alive).
⚠️ "Demo that looks like a bug": `delay` is non-blocking; `Thread.sleep` blocks — the `sleep` is only a trick to keep the demo alive.

**Slide 63 answers:** 1) Coroutines run long-running work asynchronously without blocking the main thread, keeping the UI responsive. 2) Database (disk) access can be slow; on the main thread it freezes the UI (dropped frames or an ANR "Application Not Responding"), and Room refuses to run queries on the main thread by default.

---

## 7. SQL vs NoSQL and Firebase / NoSQL 与 Firebase (slides 64–65)

The deck's objective says "Using NoSQL – Firebase" but slide 64 is only a title and slide 65 a picture. What the picture shows:
| | SQL | NoSQL |
|---|---|---|
| Model | Tables with rows/columns, relations | Document, key-value, graph, wide-column |
| Schema | Fixed | Flexible |
| Example | SQLite/Room, MySQL | Firestore (documents), Realtime Database (JSON tree) |
**Extra (not in the slides):** Firebase is Google's Backend-as-a-Service (Ch 4.2): **Cloud Firestore** stores documents in collections and **Realtime Database** a JSON tree; both sync across devices and cache offline. Local Room ≠ cloud Firebase: one is on the phone, the other on a server.

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 3 | SharedPreferences "private or public" | Modern Android: private only (world-readable modes removed) |
| 15 | `use { … close() }`, second `bufferedReader().close()` | Redundant/incorrect closing; use `readText()`/`writeText()` |
| 17 | READ/WRITE_EXTERNAL_STORAGE with `maxSdkVersion 18` | Old; scoped storage on Android 10+ |
| 21 | Non-removable "device memory" | Still *external* storage (access rules, not hardware) |
| 25 | Room 2.3.0, `annotationProcessor` | Illustrative; newer versions use KSP/kapt |
| 28 | Missing comma; `id` vs `uid` | Fix syntax; match column names |
| 29 | Non-suspend DAO | Call off the main thread |
| 54 | `saveInstanceState`, `Observer` | `savedInstanceState`; typo only |
| 61 | Resource usage High/Medium/Low | Lifetimes differ; usage is not an official attribute |
| 64 | "Firebase" | Only a title — content is extra |

Exam strategy: use the slide's names (Entity, DAO, Room, Repository, ViewModel); add that operations run on a background thread/coroutine.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| SharedPreferences / DataStore | Small private key-value / async, Flow-based replacement |
| Internal / external storage | Private, always there / world-readable, may vanish |
| SQLite | Embedded relational DB (NULL, INTEGER, REAL, TEXT, BLOB) |
| Entity / DAO / Room DB | Table / methods / access point |
| ViewModel | Holds UI data, survives rotation |
| Repository | Decides network vs local; single API |
| LiveData / StateFlow | Observable, lifecycle-aware / always-has-value stream |
| Coroutine | Lightweight async code; `launch` vs `async` |
| Scopes | Global (app), lifecycle (Activity), viewModel (ViewModel) |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Best place for "preferred theme = dark"? (a) SQLite (b) SharedPreferences/DataStore (c) External storage (d) Repository
2. Which is **not** a Room component? (a) Entity (b) DAO (c) Database (d) Adapter
3. Files in an app's internal storage are… (a) readable by any app (b) private to the app (c) kept after uninstall (d) on the SD card
4. What survives a screen rotation? (a) Activity fields (b) ViewModel data (c) local variables in `onCreate` (d) the Activity object
5. `async` differs from `launch` because it… (a) is slower (b) returns a result via `await()` (c) needs no scope (d) runs on the main thread only

### B. Short answer
1. Compare internal and external storage in removability, availability, accessibility.
2. State the roles of Activity, ViewModel and Repository.
3. Why is a database query on the main thread bad?

### C. Trace / calculation
1. Using the `user` table above, what does `SELECT * FROM user WHERE uid IN (2,4)` return, and what does `DELETE FROM user WHERE uid = 4` leave? 
2. Trace the coroutine: `launch { delay(500); println("B") }; println("A"); Thread.sleep(300); println("C"); Thread.sleep(400)` — order and timing of prints.
3. A `TEXT` value "05" is stored in a `TEXT` column and read back. What is the value? What if the column were `INTEGER`?

### D. Thinking
1. Jan 2026 Q3b: choose SharedPreferences, Data Files or SQLite for (i) training progress, (ii) preferred language, (iii) business registration documents, with a justification each.
2. Design the data layer of a to-do app that works offline and syncs to a server: which classes and where does each run?

### Answers
**A.** 1-b. 2-d. 3-b. 4-b. 5-b.

**B.**
1. Internal: not removable, always available, private to the app. External: possibly removable (SD), not always available (unmounted), world-readable/user-modifiable.
2. Activity draws the UI and takes input; ViewModel holds UI data and survives configuration changes; Repository is the single API that loads/saves from DB or network.
3. Disk I/O can take long and blocks the UI thread → frozen UI/ANR; Room throws by default.

**C.**
1. `IN (2,4)` → (2, Calvin, Lee) and (4, Mark, NULL). After deleting uid 4 the table holds uids 1, 2, 3 (before any other delete).
2. t=0 prints **A** (main), coroutine suspended until 500 ms; t=300 ms prints **C**; t=500 ms coroutine prints **B**; main ends at 700 ms. Order: A, C, B. (Assumes the coroutine runs on a background dispatcher and the JVM stays alive until 700 ms.)
3. `TEXT` keeps `'05'`. In an `INTEGER` column SQLite's type affinity would convert `'05'` to `5`, losing the leading zero — store phone numbers as TEXT (also seen in the JSON sample of Ch 4.2: `"contact":"05"`).

**D.**
1. Use the table in section 1.
2. UI (Compose) → ViewModel (StateFlow) → Repository → Room DAO (local, suspend functions in a coroutine on IO dispatcher) and Retrofit/Volley API (network). Repository reads from Room first, refreshes from the network in a background coroutine/WorkManager, and writes the result back to Room; the UI observes Room so it updates by itself.

---

## Links to other chapters / 与其他章节的联系
- Lifecycle, Bundle and rotation → **Chapter 3**; background work and networking → **Chapter 4.2**.
- Photos to files, MediaStore → **Chapter 6**; storage/signing and app size → **Chapter 7**.
