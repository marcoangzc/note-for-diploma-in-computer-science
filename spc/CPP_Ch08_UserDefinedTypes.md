# C++ Programming — Chapter 8: User-defined Types

> Like Chapter 7, this file is labelled "not yet ready". It leaves every enum question unanswered (slides 15, 21–23, 25, 27), contains code that will not compile (`enum` with the same name twice, `cons int`), a `printPassenger` function whose output is one long line, and a size table (`long` = 4 bytes) that is true only on Windows. This note answers all of them and checks each answer by compiling. Everything was run with g++ 13 on 64-bit Linux.

## 0. One-sentence overview

You can give an existing type a **new name** (`typedef`) or define a **new type whose values are a list of names** (`enum`); structs (Chapter 3) are the third kind of user-defined type.

| Section | Slides | Key idea |
|---|---|---|
| 1. Simple types | 2–5 | primitive types and their sizes |
| 2. `typedef` | 6–12 | alias, not a new type |
| 3. `enum` | 13–27 | named integer constants as a type |

---

## 1. Simple and primitive types (slides 3–5)

A **simple type** holds one indivisible value (`int x = 9;`). An **array** (`int x[2] = {0,9}`) is **not** simple: it is a structured type made of several values. (That is the answer to the "Array ?" on slide 3.)

Sizes in bytes (slide 5 vs. this machine, verified):

| Type | Slide | Here (64-bit Linux, g++) |
|---|---|---|
| `bool`, `char` | 1 | 1 |
| `short` | 2 | 2 |
| `int` | 4 | 4 |
| `long` | 4 | **8** |
| `float` | 4 | 4 |
| `double` | 8 | 8 |
| `long long` (not on slide) | – | 8 |

⚠️ **Sizes are not fixed by the language.** The standard only guarantees minimum sizes and ordering (`short ≤ int ≤ long`). Visual Studio on Windows has `long` = 4 (as on the slide); 64-bit Linux/macOS has `long` = 8. Use `sizeof(type)` to find out. (Chapter 10 shows fixed-size types.)

## 2. `typedef` (slides 6–12)

`typedef ExistingType NewName;` gives an **alias**. It creates **no new type**: `Status` and `int` are interchangeable.

```cpp
typedef int Status;
const int GOOD = 1;
Status condition = GOOD;     // exactly the same as:  int condition = 1;
```

Why use it? **Readability and one place to change**: if `Days` later needs to be `short`, edit one line. (The statement needs its `;`, which slide 7's syntax line omits.) *Extra:* modern C++ prefers `using Status = int;`, the same thing, easier to read (verified to compile).

### 2.1 Slide 9–10 (Days)

The answer is on slide 10 but has a typo: **`cons int SUN = 7;` must be `const int SUN = 7;`** (`error: 'cons' does not name a type; did you mean 'const'?`). With that fixed I confirmed `weekday[4]` = 5 and `restday[1]` = 7.

### 2.2 Slides 11–12 (Passenger)

```cpp
typedef struct { string name; int age; string seatNumber; } Passenger;
```

- In **C** you needed `typedef struct {…} Name;` to avoid writing `struct` everywhere. In **C++** `struct Passenger { … };` already lets you write `Passenger p;`, so the typedef is a C habit (it still works).
- ⚠️ **Output problem in `printPassenger`:** the loop prints `", Seat: " << p.seatNumber` with **no newline**, so all three passengers run together (verified):

```
Passenger List:
Name: Ah Chin, Age: 34, Seat: 12AName: Ah Lam, Age: 45, Seat: 12BName: Ah Wong, Age: 29, Seat: 13A
```
Add `<< endl` after `p.seatNumber`. Also pass the vector as `const vector<Passenger> &` to avoid copying the whole list. The code needs `<vector>` and `<string>`, and uses curly quotes on `“Ah Chin"`.

---

## 3. Enumeration types (slides 13–27)

**Analogy:** a **menu with numbered dishes**. You order by *name* (`BURGER`), the kitchen stores the *number* (1). The compiler stops you from ordering "dish number 7" that isn't on the menu (well, mostly; see 3.4).

```cpp
enum Days {MON, TUE, WED, THU, FRI, SAT, SUN};   // Days is a NEW type
```

- The names are called **enumerators**. Behind the scenes they are ints starting at **0**: `MON`=0 … `SUN`=6 (slide 18: "index").
- They must be **identifiers** (letters/digits/`_`, not starting with a digit), **not numbers or characters**.
- They must be **unique in the same scope**.

### 3.1 Slide 15 — which declarations are valid? (unanswered on the slide)

| # | Declaration | Valid? | Compiler message (verified) |
|---|---|---|---|
| 1 | `enum Vowel {'A','E','I','O','U'};` | **No** | `expected identifier before 'A'` (characters aren't identifiers) |
| 2 | `enum Prizes {1st, 2nd, 3rd};` | **No** | `expected identifier before numeric constant` (can't start with a digit) |
| 3 | `enum Animals {MOUSE, RABBIT, …}; enum Pets {CAT, …, RABBIT};` | **No** | `'RABBIT' conflicts with a previous declaration` |

Number 3 is the key idea: the enumerators of a plain `enum` are visible in the **enclosing scope**, so two enums in the same scope cannot share a name. Each enum on its own is fine (verified).

⚠️ **Slide 14 breaks its own rule:** `enum Program {RMM,RSD,RSF,RSD,REI,RIT};` has `RSD` **twice** → `error: redefinition of 'RSD'`.

*Extra (not in slides):* C++11's `enum class` fixes problem 3: `enum class Color {Red}; enum class Light {Red};` compiles (you write `Color::Red`), and it doesn't convert to `int` automatically (so `cout << Color::Red` is an error).

### 3.2 Using enum variables (slides 16–20)

```cpp
enum Weekdays {MON,TUE,WED,THU,FRI};
Weekdays workday = MON;
if (workday == MON) cout << "Monday Blue";
cout << workday;                    // prints the number: 0
```

**Invalid vs valid operations (verified):**

| Code | Result |
|---|---|
| `workday = 1;` | error: `invalid conversion from 'int' to 'Weekdays'` |
| `workday++;` | error: `no 'operator++(int)' declared` |
| `workday = workday + 1;` | error (`workday + 1` is an int) |
| `workday = Weekdays(1);` | OK → `TUE` |
| `workday = Weekdays(workday + 1);` | OK |

The rule: an **int cannot go into an enum without a cast**, but an enum turns into an int automatically.

⚠️ **The cast is unchecked (not on the slides).** `Weekdays(FRI + 1)` gave **5**, which is not any of the five names, and there is no wrap-around. Test the value yourself before advancing.

Comparisons work because enums behave like ints: `MON < FRI` is true, `int(THU)` = 3.

### 3.3 Slide 21 — trace

`workday = FRI` (value 4). `workday < WED`? 4 < 2 → no. `workday == WED`? no. So `mood = EXCITED`, which is the 4th name of `Emotion {SAD, HAPPY, ANGRY, EXCITED}` → index **3**. Output **`Mood = 3`** (verified). (`cout` prints the number, not the word.)

| `workday` | Branch taken | `mood` printed |
|---|---|---|
| MON, TUE (< WED) | first | 0 (SAD) |
| WED | second | 1 (HAPPY) |
| THU, FRI | else | 3 (EXCITED) |

### 3.4 Slides 22–23, 25 — the fast-food exercise, solved

```cpp
enum Fastfood  {FF, BG, PZ};
enum Friedfood {FFC, FFN, FFF};
enum Burger    {BGC, BGB, BGF};
enum Pizza     {PZC, PZV, PZT};

Fastfood ff = FF;  Friedfood fr = FFC;  Burger bg = BGC;  Pizza pz = PZC;   // first items
cout << ff << " " << fr << " " << bg << " " << pz;      // 0 0 0 0

int index;  cin >> index;                // user types 1
Fastfood chosen = Fastfood(index);       // cast required -> BG
```

Checked: with `index = 1`, `chosen == BG` is true. All twelve enumerator names are different, so no clash.

**Slide 25 (price with `switch`):**

```cpp
double price = 0;
switch (bg) {                  // bg is a Burger
    case BGC: price = 5.80; break;
    case BGB: price = 5.50; break;
    case BGF: price = 6.80; break;
}
```
`BGB` gives 5.50 (verified). Enumerators are constants, so they can be `case` labels (slide 24). Remember `break`, or execution falls through to the next case (slide 24 intentionally stacks `case HAPPY: case EXCITED:` to share one action). Slide 24's output for `ANGRY` is `Forgive, and you'll forget` (verified).

### 3.5 Slide 26 — returning an enum

`Weekday stringToDay(string)` compares the text with each name. ⚠️ The slide's `...` hides the ending: if the text matches none, **no `return` runs**, which is undefined behaviour (`warning: control reaches end of non-void function`). Always end with a default such as `return MON;` (verified version compiles and works).

### 3.6 Slide 27 fill-in-the-blank

Reading order on the slide is scrambled; visually: enum, prototype ①, `main` with ②, then the function with ③ and ④.

| Blank | Answer | Why |
|---|---|---|
| ① | `Mood getMood(int);` | prototype before `main` |
| ② | `Mood` | `ans` stores what `getMood` returns |
| ③ | `Mood` | return type |
| ④ | `int` | called with `getMood(1)`, and compared with `m == 0` |

Why not `Mood` for ④? `getMood(1)` passes an **int**, and an int does not convert to `Mood` (slide 19 rule); verified `invalid conversion from 'int' to 'Mood'`. With ④ = `int` the program prints `1` (HAPPY).

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Truth |
|---|---|---|
| 5 | `long` = 4 bytes | platform-dependent; 8 on 64-bit Linux/macOS |
| 10 | `cons int SUN = 7;` | typo: `const` |
| 12 | Passenger list output | no newline between passengers |
| 14 | `enum Program {…RSD,…,RSD…}` | duplicate enumerator → error |
| 15 | valid enum declarations? | all three are invalid (answers above) |
| 26 | `stringToDay` ends with `...` | needs a final `return` |
| 7 | `typedef ExistingType NewName` | needs `;`; "no new type" is correct |

**Exam strategy:** for slide 5, answer with the table on the slide (`long` = 4); for enum questions use the rules on slide 13.

## Cheat sheet

| Need | Code |
|---|---|
| alias | `typedef int Status;` or `using Status = int;` |
| enum | `enum Days {MON, TUE, …};` (values 0, 1, 2, …) |
| enum variable | `Days d = MON;` |
| enum → int | automatic (`cout << d` prints a number) |
| int → enum | `Days(1)` (unchecked) |
| loop/step | `d = Days(d + 1);` (check the range yourself) |
| `switch` on enum | `case MON:` … with `break` |
| unique names | per scope; use `enum class` to avoid clashes |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** Which is a valid enum? (a) `enum A {'x','y'};` (b) `enum B {1st, 2nd};` (c) `enum C {RED, GREEN};` (d) `enum D {RED, RED};`
**A2.** `enum Weekdays {MON,TUE,WED,THU,FRI}; cout << FRI;` prints (a) FRI (b) 4 (c) 5 (d) 0
**A3.** Which is invalid for `Weekdays workday = MON;`? (a) `workday = Weekdays(2);` (b) `workday++;` (c) `if (workday == MON)` (d) `cout << workday;`
**A4.** `typedef int Days;` creates (a) a new type (b) another name for `int` (c) an enum (d) a constant
**A5.** Slide 5 says `long` = 4 bytes. On 64-bit Linux it is (a) 2 (b) 4 (c) 8 (d) 16

### B. Short answer

**B1.** Explain why `enum Animals {MOUSE, RABBIT}; enum Pets {CAT, RABBIT};` is an error.
**B2.** Explain why `workday = 1;` is rejected and write the correct form.
**B3.** State two advantages of `enum` over `const int` constants plus a `typedef`.

### C. Calculation / trace

**C1.** `enum Weekdays {MON,TUE,WED,THU,FRI}; enum Emotion {SAD,HAPPY,ANGRY,EXCITED};` The slide-21 `if` chain (`< WED` → SAD, `== WED` → HAPPY, else EXCITED) is run with `workday = THU`. What is printed?
**C2.** `enum Time {MORNING,NOON,EVENING,NIGHT};` Give `int(EVENING)` and `Time(1)`.
**C3.** Using the burger prices (BGC 5.80, BGB 5.50, BGF 6.80), what is the total for one BGC and one BGB?

### D. Thinking

**D1.** `Weekdays d = FRI; d = Weekdays(d + 1);` — what is `d` afterwards, and what should the program do to be safe?
**D2.** Why is a `stringToDay` function that has no `return` after the `if … else if` chain dangerous?

---

### Answers

**A1 → (c).** (a) characters, (b) starts with digit, (d) duplicate.
**A2 → (b) 4.** MON=0, TUE=1, WED=2, THU=3, FRI=4. (Verified with `MON`=0; `THU`=3.)
**A3 → (b).** `++` isn't defined for a plain enum (verified).
**A4 → (b).** An alias only.
**A5 → (c) 8.** (Verified: `sizeof(long)` = 8 here.)

**B1.** The enumerators of a plain enum go into the enclosing scope, so `RABBIT` would be declared twice (`'RABBIT' conflicts with a previous declaration`). Rename one, or use `enum class`.

**B2.** An `int` does not convert to an enum implicitly (`invalid conversion from 'int' to 'Weekdays'`). Write `workday = Weekdays(1);` (a cast, giving TUE) or better `workday = TUE;`.

**B3.** (i) The compiler treats the enum as a *distinct type* (no accidental int assignment) so the variable is self-documenting. (ii) The list of names is defined in one statement, numbered automatically, usable directly in `switch`. With ints you must number and keep them in step yourself.

**C1.** `THU` (3) is not `< WED` and not `== WED`, so `mood = EXCITED` → output **`Mood = 3`**.

**C2.** `int(EVENING)` = **2**; `Time(1)` = **NOON**.

**C3.** 5.80 + 5.50 = **11.30**.

**D1.** `d` becomes the number **5**, which is not one of the named values (verified `FRI + 1 -> 5`, no wrap-around). Check the range first (`if (d < FRI)`) or wrap explicitly: `d = (d == FRI) ? MON : Weekdays(d + 1);`.

**D2.** If none of the strings match, control reaches the end of the function without returning a value — undefined behaviour (g++: `control reaches end of non-void function`). End with a fallback `return` (or handle the error).

---

## Links to other chapters

- **Ch 3:** `typedef struct {…} Name;` builds on structs.
- **Ch 5–6:** enums as parameters and return values (slide 26); `switch` on enum.
- **Ch 10:** fixed-size integer types and using bits as flags are the next step after `enum`.
