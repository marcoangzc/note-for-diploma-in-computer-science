# AMIT3353 — Chapter 2.1: User Interface — Layouts, Components and Events
# 第 2.1 章：界面布局、组件与事件（中英双语）

> The slides show Compose code but never explain `@Composable`, `remember`, `mutableStateOf` or *why* a TextField needs `onValueChange`; they also say a Column scrolls by itself (it does not) and mix old XML-View ideas with Compose. This note explains the mechanics, fixes the mix-ups and gives ready answers for the "optimise layout performance" exam question.
> 中文：slide 直接放代码，没有解释 state、recomposition，还把旧的 View/XML 概念和 Compose 混在一起。这里把机制讲清楚，并给出「优化布局性能」的标准答案。

---

## 0. One-sentence overview / 一句话总结

In Jetpack Compose you build a screen by **nesting small functions** (Row, Column, Box, Lazy lists, Button, TextField…), style them with **Modifier**, keep changing values in **state**, and apply a **theme** for consistent colours/fonts/dark mode.
中文：Compose = 用小函数嵌套拼出界面 + Modifier 调样式 + state 存会变的数据 + Theme 统一外观。

| Topic 主题 | Slides |
|---|---|
| Basic layouts: Row, Column, Box, Modifier | 3–4 |
| ConstraintLayout | 5–6 |
| Lazy list / grid, RecyclerView idea, Card | 7–8, 15–17 |
| Improving layout performance (3 methods) | 10–13 (exam!) |
| Components: Button, TextField, Checkbox, RadioButton, Spinner | 18–32 |
| Style & Theme, dark theme | 33–37 |

---

## 1. Composable functions, state and recomposition / 基本机制（slide 里没讲）

**English.** A *composable* is a Kotlin function marked `@Composable` that *describes* a piece of UI. Compose calls it to draw the UI. When some **state** it reads changes, Compose calls it again — only the parts that read that state — this is **recomposition**. State is created with `remember { mutableStateOf(initial) }`; `remember` keeps the value between recompositions, `mutableStateOf` makes Compose notice changes. `by` is Kotlin syntax that lets you write `isChecked` instead of `isChecked.value`.
**中文：** `@Composable` 函数「描述」界面；里面读到的 state 一变，Compose 就重新执行（recomposition，只重画受影响的部分）。`remember` = 重画时别把值丢掉；`mutableStateOf` = 值变了要通知 Compose。

Analogy / 类比: a composable is a recipe card; state is the ingredient list on the fridge. Whenever the list changes, the kitchen re-reads only the recipes that use those ingredients. *(Stops working for one thing: recomposition can run many times, so never put slow work directly inside a composable.)*

### Worked example — slide 26 Checkbox, traced
```kotlin
@Composable
fun SimpleCheckbox() {
    var isChecked by remember { mutableStateOf(false) }
    Row(verticalAlignment = Alignment.CenterVertically) {
        Checkbox(checked = isChecked, onCheckedChange = { isChecked = it })
        Text(text = if (isChecked) "Checked" else "Unchecked")
    }
}
```
| Step | Event | `isChecked` | What Compose does | Screen |
|---|---|---|---|---|
| 1 | First draw | false | Runs function, `remember` stores false | ☐ Unchecked |
| 2 | User taps box | — | Calls `onCheckedChange(true)` (`it` = new value) | — |
| 3 | Lambda runs | true | State changed → schedule recomposition | — |
| 4 | Recompose | true | Re-runs the function; `checked = true` | ☑ Checked |

⚠️ **Common confusion:** `onClick = { ... }` is a **lambda** (a block of code passed as a value) — this is "input event handling" in Compose. There is no `setOnClickListener`.

---

## 2. Basic layouts: Row, Column, Box, Modifier / 基础布局 (slides 3–4)

| Layout | Arranges children | Real-life picture |
|---|---|---|
| `Row` | left → right | items on a shelf |
| `Column` | top → bottom | a stack of plates |
| `Box` | on top of each other (layers) | photo with a caption on it |

**Modifier** sets size, padding, background, click, alignment. **Order matters** — modifiers are applied from the outside in (documented behaviour; not compiled here):
- `Modifier.padding(16.dp).background(Color.Red)` → red area is **inside** the 16 dp gap (gap is outside the red).
- `Modifier.background(Color.Red).padding(16.dp)` → red covers the whole box, **content** is inset by 16 dp.

`dp` = density-independent pixel (same physical size on any screen; at 320 dpi, 1 dp = 2 px; verified in section 5 of Ch 2.3). `sp` = same idea, used for text and follows the user's font-size setting.

⚠️ **Where slide 4 misleads:**
1. "Column … creates a scrollbar if the length exceeds the screen." In Compose a Column does **not** scroll by itself — add `Modifier.verticalScroll(rememberScrollState())`, or use `LazyColumn`. (The slide text comes from the old XML `ScrollView`.)
2. "Divider" (slide 3) is a **thin line**; empty space is added with `Spacer(Modifier.height(8.dp))` (slide 21 does this correctly).
3. The box titled "Constrain Layout" carries the old **RelativeLayout** description and a footnote "replaced by Constraint Layout". Read it as: *place children relative to each other → use ConstraintLayout*.

---

## 3. ConstraintLayout (slides 5–6)

**English.** ConstraintLayout positions each child relative to the parent or to other children, which lets you build complex screens with a **flat** hierarchy (no deep nesting of Rows/Columns).
**Rule (slide 6):** every view needs **at least one horizontal and one vertical constraint**; otherwise it does not know where to sit (in the Views editor it jumps to the top-left corner). Slide 6 figure: A is constrained left-to-parent and top-to-parent; C is constrained under A; B is right of A.
```kotlin
// compose version (needs androidx.constraintlayout:constraintlayout-compose; not compiled here)
ConstraintLayout(Modifier.fillMaxSize()) {
    val (a, b) = createRefs()
    Text("A", Modifier.constrainAs(a) { top.linkTo(parent.top); start.linkTo(parent.start) })
    Text("B", Modifier.constrainAs(b) { top.linkTo(a.bottom); start.linkTo(a.start) })  // B under A
}
```
中文：每个控件至少要有水平方向和垂直方向各一个约束。优点：层级扁平，性能好。

---

## 4. Dynamic content: Lazy lists and grids / 动态内容 (slides 7–9, 15–17)

**English.** A normal `Column` composes **every** child at once — 1,000 items means 1,000 composables. `LazyColumn` (vertical), `LazyRow` (horizontal) and `LazyVerticalGrid` compose **only the items visible on screen** (plus a few to prefetch) and drop items that scroll out. No adapter is needed.
```kotlin
val items = listOf("Apple", "Banana", "Cherry")
LazyColumn { items(items) { item -> Text(text = item) } }
```
### Worked example — how many items are composed? (calculated)
Screen list height 800 dp, each row 72 dp, 1,000 rows.
- Visible rows: 800 / 72 = 11.1 → at offset 0 the rows touched are 12; in the worst scroll offset 13.
- `Column`: 1,000 composed. `LazyColumn`: ≈ 12–13 (plus a small prefetch buffer). Roughly **80× fewer**.
中文：只 compose 屏幕上看得见的行，所以长列表不卡、不占内存。

⚠️ **Where slide 15/16 mislead:**
- Slide 15 says *ListView loads all records* and *LazyList uses ViewHolder*. Real picture: old `ListView` and `RecyclerView` **recycle** row views with the ViewHolder pattern; `LazyColumn` has **no ViewHolder** — it composes visible items on demand and disposes the others. The slide is a simplification to show "load visible only".
- Slide 16 (RecyclerView recycling) describes the **old View system**, not LazyColumn.

### Slide 9 question — which layout?
| App | Screen | Best layout |
|---|---|---|
| A: YouTube home | vertical feed of similar video rows | `LazyColumn` (+ `Card`/`Row` per item) |
| B: Google Play home | vertical list of sections, each a horizontal strip of app icons | `LazyColumn` containing `LazyRow`s (or `LazyVerticalGrid` for the "Top charts" grid) |

**Card-based layout (slide 17):** `Card { … }` groups related info in a raised, rounded block; gives a consistent look across platforms.

---

## 5. Improving layout performance in Jetpack Compose / 优化布局性能 (slides 10–13) — EXAM

Both past papers ask this in Q1b (Oct 2025: "Adapt THREE methods", 15 marks; Jan 2026: "Apply THREE methods", 9 marks). The slide pairs each *old* Android technique with its Compose replacement:

| # | Old View system technique | Compose method (what you write) | Why it is faster |
|---|---|---|---|
| 1 | Optimise the layout hierarchy | **Flat tree of composables + smart recomposition.** Avoid needless nesting, use `ConstraintLayout` for complex screens, keep state low so only changed parts recompose | No deep View tree to measure/inflate; only composables that read changed state re-run |
| 2 | Reuse layouts with `<include>` | **Break UI into small reusable composables** (e.g. `ProfileCard(user)`) | Reuse without XML inflation; each small function recomposes independently |
| 3 | Load views on demand (`ViewStub`) | **`LazyColumn`/`LazyRow`/`LazyVerticalGrid`** | Only visible items are composed and drawn |

### Model answer template (per method, 3–5 marks each)
"**Method 1 — Use a flat composable hierarchy.** *What:* … *How to apply in the app:* … *Benefit:* …". Always finish with **how it is applied to the scenario app** (e.g. MyGOV's list of 100 services → LazyColumn; a repeated service tile → one reusable composable `ServiceCard`). Marks are for *apply/adapt*, not for copying the slide.
中文：每个方法写三步：是什么 → 在题目的 app 里怎么用 → 带来什么好处。

---

## 6. UI components / 常用组件 (slides 18–32)

| Component | Use | Key Compose parts |
|---|---|---|
| Button | trigger an action | `Button(onClick = {…}) { Text("…") }`; `colors = ButtonDefaults.buttonColors(…)` |
| Text field | type text | `TextField(value, onValueChange, label, keyboardOptions)` |
| Checkbox | choose **zero or more** options | `Checkbox(checked, onCheckedChange)` |
| RadioButton | choose **exactly one** of a visible set | `RadioButton(selected, onClick)` |
| Spinner (dropdown) | choose one from a long list without taking screen space | `ExposedDropdownMenuBox` + `ExposedDropdownMenu` |

**Button:** slide 19 "Button class: text and icon; ImageButton class: icon" is the XML world. In Compose, `Button` holds any content (`Icon`, `Spacer`, `Text` as in slide 21).

**Text field — why `onValueChange`?** A Compose TextField is **controlled**: it shows exactly what `value` says. If your `onValueChange` does not store the new text (`email = it`), nothing you type appears. Keyboard types (slide 24): `text`, `textEmailAddress`(@), `textUri`(/), `number`, `phone` ↔ `KeyboardType.Text/Email/Uri/Number/Phone`.

**Checkbox vs RadioButton:** Checkbox = "select any"; RadioButton group = "select one" (slide 29 keeps one `selectedOption` string, so choosing one automatically un-selects the others — trace: options = Male/Female/Other, selectedOption = "Male"; tap "Other" → selectedOption = "Other" → recompose → only "Other" is filled). ⚠️ The single radio of slide 28 toggles itself on/off, which real radio groups never allow — it is only a demo of `Modifier.clickable`.

**Spinner (slides 30–32) — reading the code:** `expanded` = is the menu open; `selectedOption` = current value; the read-only TextField shows the selection; `DropdownMenuItem.onClick` saves the choice and sets `expanded = false`. (`menuAnchor()` may show a deprecation warning in newer Material3 versions — extra.)

---

## 7. Style, Theme and Dark theme / 样式与主题 (slides 33–37)

- **Style** = a bundle of attributes for **one** view (XML). **Theme** = a style applied to a **whole activity/app**, so every view inherits colours and fonts (slide 35 figure).
- In Compose you wrap the UI in `MaterialTheme(colorScheme, typography, shapes) { … }`; children read `MaterialTheme.colorScheme.primary` etc.
- **Dark theme** (Android 10 / API 29+): saves power (especially OLED), reduces glare, easier in low light. Slide 37 shows the XML way (parent `Theme.MaterialComponents.DayNight`). Compose way (not compiled here):
```kotlin
val scheme = if (isSystemInDarkTheme()) darkColorScheme() else lightColorScheme()
MaterialTheme(colorScheme = scheme) { /* screens */ }
```

---

## ⚠️ Where the slides mislead / slide 需要小心的地方

| Slide | Says | More accurate |
|---|---|---|
| 4 | Column creates a scrollbar | Only with `verticalScroll` or `LazyColumn` |
| 3 | Divider "manages space" | Divider = line; `Spacer` = space |
| 4 | "Constrain Layout … replaced by Constraint Layout" | Description is RelativeLayout's |
| 5 | ConstraintLayout compatible with API 9 | About the View library; Compose itself needs minSdk 21 (extra) |
| 15 | LazyList uses ViewHolder | No ViewHolder in Lazy lists |
| 19 | ImageButton class | XML concept; Compose has `IconButton` |
| 28 | Radio button toggles | Real radios stay selected; use a group |

Exam strategy: for "Compose" questions use Compose terms (composable, state, Lazy list); if the question mentions ViewHolder/`<include>`, answer the slide way but mention the Compose equivalent.

---

## Cheat sheet / 速查表

| Term | Meaning |
|---|---|
| `@Composable` | Function that describes UI |
| Recomposition | Re-running composables that read changed state |
| `remember`, `mutableStateOf` | Keep value / notify changes |
| Row / Column / Box | Horizontal / vertical / layered |
| Modifier | Size, padding, background, click; order matters |
| LazyColumn/LazyRow/LazyVerticalGrid | Compose only visible items |
| ConstraintLayout | Relative placement; ≥1 horizontal + ≥1 vertical constraint |
| Checkbox / RadioButton | Any / exactly one |
| Theme | App-wide colours, type, shapes |
| 3 performance methods | Flat hierarchy + recomposition, small reusable composables, Lazy lists |

---

## Practice / 练习（答案紧跟题目）

### A. Multiple choice
1. Which layout would you use for a scrolling list of 5,000 chat messages? (a) Column (b) Row (c) LazyColumn (d) Box
2. `remember { mutableStateOf(false) }` is used to… (a) draw a checkbox (b) keep a value that changes and triggers recomposition (c) start a coroutine (d) navigate
3. In a controlled TextField, what happens if `onValueChange` does not update the state? (a) Text appears normally (b) Text does not change on screen (c) App crashes (d) Keyboard closes
4. Which control lets the user select several options at once? (a) RadioButton (b) Checkbox (c) Spinner (d) Button
5. Which is **not** a Compose way to reduce layout cost? (a) Lazy lists (b) Small reusable composables (c) Deeply nested Rows/Columns (d) Flat hierarchy

### B. Short answer
1. State the three methods to optimise layout performance in Compose.
2. Difference between a style and a theme.
3. Why must a ConstraintLayout child have both horizontal and vertical constraints?

### C. Trace / calculation
1. Trace the radio group of slide 29 when the user taps "Female" then "Other" (start "Male").
2. A `LazyColumn` shows rows of 56 dp on a list area of 672 dp. How many rows are visible at once, and how many compose calls for 200 rows in a `Column` vs `LazyColumn`?
3. `Button` with `Modifier.padding(16.dp).fillMaxWidth()` on a phone that is 360 dp wide: what is the button width? What is 16 dp in px on a 480 dpi phone?

### D. Thinking
1. Jan 2026 style: "Apply THREE methods to optimise layout performance of the ELSA app."
2. Why is a `LazyColumn` inside a `Column` that has `verticalScroll` a bad design?

### Answers
**A.** 1-c. 2-b. 3-b (controlled component). 4-b. 5-c.

**B.**
1. Flat composable hierarchy with smart recomposition; break UI into small reusable composables (instead of `<include>`); load on demand with LazyColumn/LazyRow.
2. Style = attributes for one view; theme = style applied to the whole app/activity so all views inherit it.
3. The system needs two coordinates (x and y); with only one axis constrained the view's position on the other axis is undefined.

**C.**
1. Start selected = Male. Tap Female → `selectedOption = "Female"` → recompose: Female filled, others empty. Tap Other → selected = "Other". Always exactly one filled.
2. 672 / 56 = 12 rows visible exactly. `Column`: 200 composed; `LazyColumn`: about 12–13 (+ prefetch). Verified: at offset 0 rows 0–11 = 12; at other offsets 13.
3. `fillMaxWidth` fills the parent, then padding takes 16 dp per side: button content width = 360 − 32 = 328 dp (the padding is outside the button because `padding` comes first). 16 dp × (480/160) = 48 px (matches the verified table in Ch 2.3).

**D.**
1. Use section 5 template and apply: e.g. (1) flat hierarchy — ELSA dashboard uses ConstraintLayout instead of nested Columns and reads state as low as possible; (2) reusable composables — one `AdviceCard`, `TrainingModuleItem` reused across screens; (3) LazyColumn for the training modules/financing list. Add one benefit per method.
2. Both try to control scrolling on the same axis with unbounded height: Compose throws an exception (infinite height constraint) and the Lazy list loses its lazy benefit if forced to measure everything. Use a single LazyColumn with different item types instead.

---

## Links to other chapters / 与其他章节的联系
- Same themes/resources are reused for languages and screen sizes → **Chapter 2.3**.
- Navigation between these screens, dialogs, tabs → **Chapter 2.2**.
- `remember`/state and lifecycle, `ViewModel` state survives rotation → **Chapters 3 and 4.1**.
