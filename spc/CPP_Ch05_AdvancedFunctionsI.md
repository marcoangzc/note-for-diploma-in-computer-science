# C++ Programming — Chapter 5: Advanced Functions I

> The slides show the three ways to pass data into a function but never say what the words *mean* underneath (copy, alias, address) and they leave all seven exercises unsolved. This note explains the difference with a tracing table, points out the one thing the slides get subtly wrong ("pass by address" is really a *copy of a pointer*), and solves every exercise. All code was compiled and run with g++ 13. (I did not open the structure-chart figure on slide 3.)

## 0. One-sentence overview

A function can receive its input as a **copy** (by value), as an **alias** for the caller's variable (by reference), or as the caller variable's **address** (by address); the last two let the function change the caller's data.

| Section | Slides | Key idea |
|---|---|---|
| 1. Recap of functions | 2–5 | declaration, call, definition |
| 2. Why parameters | 6–8 | avoid globals |
| 3. By value | 9–11 | copy, original safe |
| 4. By reference | 12–15 | `int &x`, alias |
| 5. By address | 16–19 | `int *x`, `&a`, `*x` |
| 6. Swap | 20–21 | classic reference vs address |
| 7. Flowchart | 23–24 | reading pseudocode |

---

## 1. Function recap (slides 2–5)

Three parts, always in this order of *thinking* (prototype can be skipped only if the definition comes first):

```cpp
void header();              // 1. declaration (prototype): promise to the compiler
int main() {
    header();               // 2. call
}
void header() { cout << "function"; }   // 3. definition: the actual code
```

Verified: calling `header()` **before** it is declared or defined gives `error: 'header' was not declared in this scope`. The prototype is what allows `main` to appear first.

⚠️ The slide writes `void main()`; g++ rejects it (`'::main' must return 'int'`). Visual Studio accepts it. Use `int main()`.

| Word | Meaning |
|---|---|
| **Actual parameter / argument** | the value in the call: `fun(a)` → `a` |
| **Formal parameter** | the variable in the definition: `void fun(int x)` → `x` |
| **void function** | returns nothing |
| **value-returning function** | ends with `return value;` |

**Why global variables are discouraged (slide 6):** any function can change them at any time, so when a value is wrong you cannot tell which function did it. Parameters make the data flow visible.

## 2. Pass by value (slides 9–11)

The function gets a **photocopy**. Changing the photocopy leaves the original alone.

```cpp
void fun(int x) { x = x + 3; }
int main() { int a = 5; fun(a); cout << a; }     // prints 5
```

```
main:  a [ 5 ]          (untouched)
fun:   x [ 5 ] -> [ 8 ]   (dies when fun ends)
```

Trade-off the slide doesn't mention: copying a big struct or array for every call is slow. That is one reason for references.

## 3. Pass by reference (slides 12–15)

`void fun(int &x)` — the `&` in the **parameter list** makes `x` another **name** for the caller's variable. No copy is made, and the call still looks normal: `fun(a);`

```
main:  a [ 5 ]  <== x is just a second name for this same box
fun:   x = x + 3   => a is now 8
```

Rules (verified errors):
- You must pass a real variable: `f(5)` where `f(int &x)` gives `cannot bind non-const lvalue reference of type 'int&' to an rvalue`.
- To promise not to change it, write `const int &x`; then `x = 3;` is `error: assignment of read-only reference`. (*Extra, not in slides:* `const &` is the usual way to pass big data cheaply and safely.)

## 4. Pass by address (slides 16–19)

The caller sends `&a` (address of a); the function receives a **pointer** `int *x` and must use `*x` to reach the value.

```cpp
void fun(int *x) { *x = *x + 3; }
int main() { int a = 5; fun(&a); cout << a; }     // prints 8
```

| | Call | Parameter | Inside function |
|---|---|---|---|
| value | `fun(a)` | `int x` | `x` |
| reference | `fun(a)` | `int &x` | `x` |
| address | `fun(&a)` | `int *x` | `*x` |

⚠️ **What "by address" really is (extra insight).** In C++ the address itself is passed **by value**: the function gets a *copy of the pointer*. That copy points at the caller's variable, so `*x = …` changes the original, but if the function makes `x` point somewhere else, the caller's pointer is unaffected. Verified: after `reassign(ptr)` (which does `p = &other`), `ptr == &v` is still true and `v` is still 7.

### Side-by-side test (verified)

Starting from `a = 5`: `byValue(a)` → **5**; `byRef(a)` → **8**; `byAddr(&a)` → **11** (8 + 3).

### Swapping two variables (slides 20–21)

| Version | Result for `p=1, q=2` |
|---|---|
| swap by **value** | still `1,2` (only copies swapped) |
| swap by **reference** (`int &a, int &b`) | `2,1` |
| swap by **address** (`int *a, int *b`, body uses `*a`, `*b`) | swapped again |

The body uses a temporary: `temp = num1; num1 = num2; num2 = temp;` — without `temp` the first assignment would erase a value.

---

## 5. Exercises — worked solutions (all run and verified)

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

bool checkMark(int mark) { return mark >= 1 && mark <= 100; }                  // slide 11
void applyDiscount(double &price, double discountPercent)                      // slide 14
    { price -= price * discountPercent / 100; }
void updateSteps(int &todaySteps, int &weeklySteps, int &extraSteps)           // slide 15
    { todaySteps += extraSteps; weeklySteps += extraSteps; }
void topUpWallet(double topUpAmount, double *balance) { *balance += topUpAmount; }   // slide 18
void withdrawCash(double *balance, int *transCount, double withdrawAmt)        // slide 19
    { *balance -= withdrawAmt; (*transCount)++; }
void calculateFuelCost(double distance, double rate, double price,             // slide 22
                       double &cost, int *trips)
    { cost = distance * rate * price; (*trips)++; }
```

| Exercise | Test | Result |
|---|---|---|
| `checkMark` | 0, 1, 100, 101 | false, true, true, false |
| `applyDiscount` | price 100, 20 | 80.00 |
| `updateSteps` | 4700, 21350, extra 1500 | today **6200**, weekly **22850** |
| `topUpWallet` | RM3.50 + 20 | **23.50** |
| `withdrawCash` | 4000 − 500 | balance **3500**, transactions **1** |
| `calculateFuelCost` | 120 km × 0.08 L/km × RM2.05 | **19.68**, trips **1** |

Notes on the exercises:
- **Slide 14** doesn't say whether the discount is an amount or a percentage. I chose percent; for an amount use `price -= discount;`.
- **Slide 19:** `transCount` must be initialised to 0 in `main` (a local variable holds garbage otherwise).
- **Slide 22:** distances, rate and price are passed **by value** (inputs); `cost` by **reference** and `trips` by **address** (outputs) — a mix of all three methods.
- **Slide 15** wants all three parameters as references, as I wrote (the `extraSteps` reference is not required but follows the slide).
- A real ATM would also check `withdrawAmt <= *balance` first (extra).

## 6. Reading the flowchart / pseudocode (slides 23–24)

The program prints `Welcome to Addition`, reads two integers, and prints their sum (tested with 3 and 4 → `The result is 7`). The pseudocode on slide 24 is the same program in words: `main` calls `title()`, then `addition(a,b)`, and each function ends with `Return`. Flowchart shapes: rounded box = START/END, rectangle = process/call, parallelogram = input/output.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | More accurate |
|---|---|---|
| 4 | `void main()` | Must be `int main()` in standard C++ |
| 16 | pass by address is a third method "instead of copying the value" | The address is itself copied (a pointer passed by value) |
| 9 | by value is "the preferred passing technique" | Best for protection, but copying big data is slow; `const &` is common |
| 23 | `cout << “Enter 2 integers: “;` | Curly quotes will not compile; use straight `"` |
| 14, 15 | exercises unspecified (amount vs percent) | State your assumption |

**Exam strategy:** answer "by address = pass the address with `&`, receive a pointer, use `*`", as the slide does.

## Cheat sheet

| Method | Prototype | Call | Original changes? |
|---|---|---|---|
| value | `void f(int x)` | `f(a)` | No |
| reference | `void f(int &x)` | `f(a)` | Yes |
| address | `void f(int *x)` | `f(&a)` | Yes (via `*x`) |
| read-only, no copy | `void f(const int &x)` | `f(a)` | Not allowed |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** `void f(int x){ x = x+3; }` called as `int a=5; f(a);` — `a` afterwards? (a) 5 (b) 8 (c) 3 (d) error
**A2.** Which call passes by address? (a) `f(a)` (b) `f(&a)` (c) `f(*a)` (d) `f(a&)`
**A3.** Why does `swap(int a, int b)` (by value) not swap the caller's variables? (a) it swaps copies (b) needs `return` (c) `temp` is wrong (d) it is a global
**A4.** `void f(int &x); f(5);` gives (a) works (b) compile error (c) x=5 (d) runtime error
**A5.** The *formal* parameter is (a) the value in the call (b) the variable in the function header (c) the return type (d) a global variable

### B. Short answer

**B1.** Name two problems with global variables (slide 6).
**B2.** Explain "the address is passed by value".
**B3.** Which of value/reference/address would you use to (i) test a mark, (ii) update a balance, (iii) return two results?

### C. Trace

**C1.** `int g(int x, int &y, int *z){ x++; y += x; *z = x + y; return x; }` with `A=1, B=2, C=0` and `int r = g(A, B, &C);` Give A, B, C, r.
**C2.** Compute `calculateFuelCost` for 120 km, 0.08 L/km, RM2.05 per litre, starting `trips = 0`.
**C3.** `int a=5;` call `byValue(a)` (adds 3 to its parameter), then `byRef(a)`, then `byAddr(&a)`. Give `a` after each.

### D. Thinking

**D1.** Why can a swap not be written with pass by value? Sketch the correct version by address.
**D2.** A function `void reset(int *p){ p = nullptr; }` is called as `reset(ptr)`. Is `ptr` null afterwards? Explain.

---

### Answers

**A1 → (a) 5.** Only the copy changed.
**A2 → (b) `f(&a)`.**
**A3 → (a).** It swaps its own copies, which vanish.
**A4 → (b).** A non-const reference needs a variable, not a literal (verified error).
**A5 → (b).**

**B1.** Anything can change them at any time (data protection is lost), which makes bugs hard to trace; functions that depend on globals are not self-contained, so they are harder to reuse and test.

**B2.** The caller sends `&a`; the function's pointer parameter is a **copy** of that address. Following it (`*x`) changes the original; re-pointing the copy (`x = &other`) doesn't affect the caller's pointer (verified: `ptr == &v` remained true).

**B3.** (i) value (input only). (ii) reference or address (must change the caller's balance). (iii) reference or address for the two outputs.

**C1.** Inside `g`: `x` (a copy of A) becomes 2; `y` is B, so B = 2 + 2 = **4**; `*z = 2 + 4 = 6`, so C = **6**; returns 2. Final **A = 1, B = 4, C = 6, r = 2**. Verified.

**C2.** cost = 120 × 0.08 × 2.05 = **19.68**; trips = **1**. Verified.

**C3.** After `byValue`: **5**; after `byRef`: **8**; after `byAddr`: **11**. Verified.

**D1.** By value swaps copies. Correct: `void swapAddr(int *a,int *b){ int t=*a; *a=*b; *b=t; }` called as `swapAddr(&p,&q);` (or reference version `int &a, int &b`). Verified: by value leaves `1,2`; the other two swap.

**D2.** **No.** `p` is a copy of `ptr`; setting the copy to `nullptr` leaves `ptr` alone. To change the caller's pointer you would need a pointer-to-pointer (`int **p`) or a reference to the pointer (`int *&p`).

---

## Links to other chapters

- **Ch 4:** `&`, `*` and references are used here.
- **Ch 6:** arrays and structs as parameters, storage classes and scope (where `x` and `a` live).
- **Ch 11:** by-value parameters = *data coupling* (best); globals = *common coupling* (worse).
