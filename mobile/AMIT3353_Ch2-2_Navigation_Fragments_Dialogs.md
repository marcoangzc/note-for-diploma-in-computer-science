# AMIT3353 — Chapter 2.2: User Interface — Navigation, Fragments, Dialogs, Drawer, Tabs
# 第 2.2 章：导航、Fragment、对话框、抽屉菜单与标签页（中英双语）

> The slides say "Up and Back are identical" in principle 3 and then ask "why must they be different?" in the question on slide 11, and they mix the old XML Navigation Component with Compose navigation without saying which is current. This note resolves the contradiction with traces, explains what each navigation part does, and answers the unanswered slide questions.
> 中文：slide 原则 3 说 Up 和 Back「相同」，slide 11 又问「为什么要不同」，前后矛盾；还把旧 XML 导航和 Compose 导航混在一起。这里用步骤表把它讲清楚，并回答 slide 上没有答案的问题。

---

## 0. One-sentence overview / 一句话总结

Navigation is a **stack of screens** (back stack) with a fixed start; **Fragments** are reusable UI pieces inside an Activity (old way), **NavHost + NavController** move between destinations (both old and Compose versions), and **dialogs, navigation drawers and tabs** are the standard patterns for interrupting, top-level menus and same-level content.
中文：导航 = 一叠「屏幕」（back stack）；Fragment 是旧方式的界面模块；NavHost + NavController 负责跳转；Dialog、Drawer、Tabs 是三种常用界面模式。

| Topic | Slides | Exam relevance |
|---|---|---|
| 5 navigation principles, Up vs Back | 3–11 | "Why must Back and Up differ?" |
| Fragment | 12–20, 40 | "Fragment vs Activity" |
| Navigation Component (XML) | 21–31 | Parts of the component |
| Navigation in Compose | 32–39 | Code reading |
| Dialogs | 41–50 | Dialog vs Snackbar vs Notification |
| Drawer, Tabs | 51–57 | Compare and choose |

---

## 1. Navigation principles / 导航原则 (slides 3–11)

1. **Fixed start destination** — the app always begins at the same screen (A).
2. **Navigation state = a stack of destinations** — going forward pushes, going back pops.
3. **Up and Back are identical *within your app's task*.**
4. **Up never exits your app.**
5. **Deep linking simulates manual navigation.**

Stack picture (slide 6). Only the top item is visible:
```
 start A      go to B      go to C            Back / Up
 +---+        +---+        +---+ <- visible   pops C -> B visible
 | A |        | B |        | B |              pops B -> A visible
 +---+        | A |        | A |
              +---+        +---+
```

### Resolving the contradiction: Back vs Up (slide 11 question)
**English.** Inside your own app they do the same thing — go one screen back in the stack. They differ in two situations: (1) at the **start destination**, *Back* leaves the app (returns to the launcher / the previous app) but *Up* is not shown / never leaves your app; (2) when your screen was reached from **another app or a deep link**, *Back* returns to that other app (task history), but *Up* moves within your app's own hierarchy.
**中文：** App 内部两者一样；区别在于 ① 在起始页，Back 会退出 app，Up 不会；② 从别的 app（如邮件里的链接）直接进入某一页时，Back 回到那个 app，Up 只在自己 app 的层级里往上走。

| Situation | Press **Back** | Press **Up** (←) |
|---|---|---|
| Stack A→B→C, on C | goes to B | goes to B |
| On A (start destination) | **exits the app** | button not shown; never exits |
| User taps a link in Gmail that opens screen C of your app | returns to **Gmail** | goes to B (parent), then A |
| Deep link to C opened your app cold | (system stack) leaves app | Navigation *builds* A→B→C so Up works (principle 5) |

Analogy / 类比: Back = the browser's back button (history of everything you visited, even other sites); Up = the breadcrumb bar on the website (moves up the site's structure, never leaves the site).

**Exam answer (slide 11):** "They must differ because Back follows the user's history across tasks/apps and can exit the app, whereas Up follows the app's own screen hierarchy and never exits it, so users can always find the app's home even after arriving through a deep link."

---

## 2. Fragments / 碎片 (slides 12–20)

**English.** A Fragment is a **reusable portion of UI (layout + code) that lives inside an Activity** and has its own lifecycle. It cannot exist alone and is not declared in the manifest. One Activity can host several Fragments, and the same Fragment can be reused in different Activities.
**中文：** Fragment = 放在 Activity 里面的、可重复使用的界面模块（自己的 layout + 代码 + 生命周期）。

Slides 14–18 example — list + details:
```
Landscape / tablet:   +-------------+---------------+     Portrait / phone:  screen 1: [ Fragment 1 list ]
 one Activity         | Fragment 1  | Fragment 2    |                        tap item ->
                      | Item 1      | Details of    |                        screen 2: [ Fragment 2 details ]
                      | Item 2      | the selected  |
                      | Item 3      | item          |
                      +-------------+---------------+
```
The Activity chooses one pane or two panes depending on screen size; the Fragments themselves are unchanged. That is *the reason Fragments exist.*

**How a Fragment gets its layout (slide 19):** (1) Fragment layout XML is loaded → (2) `onCreateView()` **inflates** it (turns XML into View objects) → (3) the Activity's layout has a **container** where the Fragment's view is placed.

### Slide 40 — Fragment vs Activity (with model answer)
| | Activity | Fragment |
|---|---|---|
| What | A screen / entry point | A part of a screen |
| Manifest | Must be declared | Not declared |
| Lives | Alone | Inside an Activity |
| Reuse | Hard | Easy (many Activities, many panes) |

**Advantages of Fragments:** reuse; multi-pane layouts for tablets/landscape; can be added/removed/replaced at run time; own lifecycle; managed by `FragmentManager` with its own back stack.

### Slide 20 — Fragments vs Compose
| Feature | Fragments (old) | Compose (new) |
|---|---|---|
| UI definition | XML + Kotlin | Composable functions |
| Navigation | FragmentManager + NavController | NavHost + navController |
| State | ViewModel + SavedStateHandle | `remember` + state |
| Lifecycle | Fragment lifecycle (onCreate, onStart…) | Simpler; composables enter/leave composition |
Note: the course outline still lists Fragments (older content); Compose replaces them in the slides.

---

## 3. Navigation Component (old XML approach) / 旧的 XML 导航 (slides 21–31)

Three parts — memorise with one image: **Nav graph = the map, NavHost = the window that shows the current place, NavController = the driver.**

| Part | What it is | Slide |
|---|---|---|
| Navigation Graph | XML resource listing all destinations and the `<action>`s (arrows) between them | 23–26 |
| NavHost | Empty container that displays the current destination | 27–29 |
| NavController | Object that performs `navigate()` inside a NavHost | 30–31 |

Reading slide 24: `startDestination="@+id/nav_home"` (fixed start); `<fragment>` = one destination with its class; `<action id=homeToGallery destination=nav_gallery>` = an arrow "Home → Gallery". Slide 28: `app:defaultNavHost="true"` makes the NavHost **intercept the system Back button** (only one NavHost may be the default). Slide 29: `app:navGraph` links the NavHost to the graph. Slide 31: get the controller with `findNavController(R.id.nav_host…)`, then `navController.navigate(R.id.action_nav_home_to_profileFragment)`.

---

## 4. Navigation in Jetpack Compose / Compose 导航 (slides 32–39)

Same three ideas, no XML: **NavController** (`rememberNavController()`), **NavHost** (declares start + routes), **`composable("route") { … }`** = one destination. Add the dependency `navigation-compose` in the module `build.gradle`.

```kotlin
NavHost(navController, startDestination = "home") {
    composable("home")    { HomeScreen(navController) }
    composable("details") { DetailScreen(navController) }
}
```
### Trace: back stack (not compiled here; standard behaviour)
| Action | Back stack (top on right) | Screen |
|---|---|---|
| App starts | [home] | Home |
| `navController.navigate("details")` | [home, details] | Details |
| `navController.popBackStack()` (Go Back button) | [home] | Home |
| `popBackStack()` again on home | [] (nothing left) | Activity finishes → app exits |

**Navigate with data (slide 38):** route `"details/{itemId}"` declares a placeholder; `navigate("details/123")` fills it; `backStackEntry.arguments?.getString("itemId")` reads `"123"` (always a string in this style).
**Up button in Compose (Ch 2.3 slide 13):** `navController.navigateUp()`.

⚠️ **Where slide 39 needs care:** `BottomNavigation` is the Material 2 component (Material 3 name: `NavigationBar`). Calling `navigate("home")` on every tap pushes a *new* copy each time; real apps add `launchSingleTop = true` and `popUpTo(startDestination)` so the stack does not grow (extra, not in slides).

---

## 5. Dialogs / 对话框 (slides 41–50)

Use a dialog for **critical information, decisions, or a small self-contained task**; use sparingly because it **interrupts** the user.

| Component | Priority | User action | Behaviour |
|---|---|---|---|
| Snackbar | Low | Optional | Disappears automatically |
| Notification | Medium | Optional | Stays until dismissed or the cause is resolved |
| Dialog | High | **Required** | Blocks the app until the user chooses or exits |
(Slide 43 has a typo: "officiation" should be "notification".)

Types: **Alert**, **Simple** (list, tap = choose), **Confirmation** (choose then confirm), **Full-screen** (multi-step task; may open pickers). Avoid dialogs that open more dialogs or contain scrolling content (exception: full-screen).
AlertDialog anatomy: optional title, content area, **at most three** action buttons.

### Reading slide 48
`showDialog` is **state**: button sets it `true` → recompose → `AlertDialog` is drawn; `onDismissRequest` runs when the user taps outside/presses Back; `confirmButton` / `dismissButton` are the two actions. (In the slide both buttons just call `onDismiss()`; a real app would do the "OK" work first.)

### Slide 50 answers
1. **Dialog A ("CANCEL / DISCARD") is better** — button labels state exactly what will happen, so the user cannot misread them. Dialog B ("NO / YES") forces the user to reread the question ("Discard draft?" → what does *No* mean?).
2. **Full-screen dialog "New event"** — there is an **X** and a **CLOSE** text button that do the same thing, and no clear **SAVE** action. Improve: X (close) on the left, **SAVE** on the right, and confirm before discarding.

Pickers (slide 49): time picker and date picker are dialogs for choosing a time/date.

---

## 6. Navigation drawer and tabs / 抽屉菜单与标签页 (slides 51–57)

**Navigation drawer** — panel sliding from the left edge listing main destinations. Use when: **≥ 5 top-level destinations**, **≥ 2 levels** of navigation hierarchy, or quick jumps between **unrelated** destinations.
**Tabs** — organise **related content at the same level** of hierarchy; **fixed** tabs (few, equal width) or **scrollable** tabs (many).

| | Navigation drawer | Tabs |
|---|---|---|
| Destinations | Unrelated, many (≥5) | Related, same level, few |
| Hierarchy | 2+ levels | Flat |
| Hidden until opened? | Yes (hamburger ☰) | No (always visible) |
| Swipe between? | No | Often yes |

### Slide 57 — choose (with reasons)
| App | Choice | Why |
|---|---|---|
| a. News | **Tabs** (Top / World / Sports / Business) | Categories are the same kind of content at one level; swipe between them |
| b. Weather | **Tabs** (Today / Hourly / 10-day) — or no menu at all | Three views of the same data at the same level; a drawer would be overkill |
| c. Contacts | **Navigation drawer** (All contacts, Favourites, Labels/Groups, Settings, Trash) | Several unrelated top-level areas; groups add a second level |

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 4 vs 11 | Up and Back identical vs must differ | Identical only inside your app's task; differ at start destination and after deep link/other app |
| 43 | "officiation" | Typo for "notification" |
| 22 | "Old approach" for the XML Navigation Component | Correct — Compose uses NavHost + `composable()` |
| 20 | Fragment "slower" than Compose | Simplified comparison; both work |
| 39 | `BottomNavigation` + `navigate("home")` | Material 2 name; needs `launchSingleTop`/`popUpTo` |

Exam strategy: for "Fragment vs Activity" answer from slide 40; for navigation code questions use Compose names (NavHost, NavController, composable).

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| Back stack | Stack of visited destinations; top = visible |
| Back | Pops history; may exit app or return to another app |
| Up | Moves up app hierarchy; never exits the app |
| Deep link | Opens an inner screen directly; back stack is synthesised |
| Fragment | Reusable UI module hosted by an Activity |
| NavGraph / NavHost / NavController | Map / container / driver |
| `composable("route")` | One Compose destination |
| Dialog | Modal interruption; action required |
| Snackbar / Notification | Auto-dismiss message / persistent message |
| Drawer / Tabs | ≥5 unrelated destinations / related same-level content |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which part of the Navigation Component actually performs `navigate()`? (a) NavGraph (b) NavHost (c) NavController (d) Fragment
2. The Up button… (a) always closes the app (b) never exits the app (c) is identical to the power button (d) only exists in dialogs
3. Which has the **highest** priority and blocks the app until answered? (a) Snackbar (b) Toast (c) Notification (d) Dialog
4. Tabs are best for… (a) unrelated top-level destinations (b) related content at the same level (c) 8 destinations with 2 levels (d) errors
5. A Fragment must be declared in… (a) the manifest (b) nothing — it is hosted by an Activity (c) strings.xml (d) build.gradle

### B. Short answer
1. Give two advantages of Fragments over using only Activities.
2. Why should a dialog be used sparingly?
3. Compare navigation drawer and tabs in two points.

### C. Trace
1. Compose app with routes home, list, details. Trace the back stack for: start → navigate("list") → navigate("details/7") → popBackStack() → popBackStack() → popBackStack(). What happens at the last step?
2. A user opens your app's `details` screen from a link in an email app. Table: what do Back and Up do, assuming the parent chain is home → list → details?
3. In slide 48's code, the state is `showDialog`. Trace what happens when the user taps "Show Dialog", then taps "Cancel".

### D. Thinking
1. Design the navigation for an e-commerce app with Home, Search, Cart, Orders, Wishlist, Profile, Settings, Help. Which pattern(s) and why?
2. A banking app shows a dialog for every success message. Critique and suggest alternatives.

### Answers
**A.** 1-c. 2-b. 3-d. 4-b. 5-b.

**B.**
1. Reuse the same UI module in several Activities/screens; multi-pane layout on tablets/landscape; add/remove at run time; own lifecycle.
2. It is modal: blocks the user until they act, so overuse frustrates; keep it for critical information or decisions.
3. Drawer: ≥5 unrelated destinations, ≥2 levels, hidden until opened. Tabs: related same-level content, always visible, swipeable.

**C.**
1. [home] → [home, list] → [home, list, details/7] → pop → [home, list] → pop → [home] → pop → [] : the Activity has no destination left, so the app exits (like pressing Back on the start screen).
2. Back: returns to the **email app** (previous task). Up: goes to `list` (the parent), then `home`; Up never leaves your app because Navigation builds the stack home → list → details (deep-link principle).
3. Initial `showDialog=false` → dialog absent. Tap "Show Dialog": `showDialog=true` → recompose → AlertDialog drawn, rest of screen blocked. Tap "Cancel": `onDismiss()` sets `showDialog=false` → recompose → dialog removed.

**D.**
1. Bottom navigation bar (3–5 top-level: Home, Search, Cart, Orders/Profile) for the frequent ones, and a navigation drawer or profile menu for the rest (Settings, Help, Wishlist). Tabs inside Orders (Active / Past). Top app bar with Up button on detail screens. Reason: 8 destinations exceed what fits in a bottom bar.
2. Dialogs are for critical/required decisions; a success message is low priority. Use a Snackbar (auto-dismiss, optionally with Undo) or a notification for later confirmation; keep dialogs for confirming a transfer.

---

## Links to other chapters / 与其他章节的联系
- Activity lifecycle and back stack of Activities → **Chapter 3**.
- App bar, Up button and Snackbar/Notification code → **Chapter 2.3**.
- State (`remember`) used for dialogs and `ViewModel` state → **Chapters 2.1 and 4.1**.
