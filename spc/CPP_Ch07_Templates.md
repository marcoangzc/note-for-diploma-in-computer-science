# C++ Programming — Chapter 7: Templates

> The file name says "not yet ready" and it shows: the slides define templates in one paragraph, never explain how the compiler picks `T`, and two of the four examples contain mistakes (`cout << printPair(...)` on a `void` function, and a `bool` printed as `false` when C++ prints `0`). This note explains what actually happens, adds the two ways templates fail that students hit first, and solves both exercises. All code was compiled and run with g++ 13.

## 0. One-sentence overview

A **template** is a fill-in-the-blank function (or class): you write the logic once with a placeholder type `T`, and the compiler writes a real function for each type you use.

| Section | Slides | Key idea |
|---|---|---|
| 1. Why | 3–4 | one function, many types |
| 2. One type parameter | 5–7 | `template <typename T>` |
| 3. Two type parameters | 8–10 | `T1`, `T2` |
| 4. Exercises | 11–12 | solved below |

---

## 1. The idea

**Analogy:** a cookie cutter. The template is the cutter (the shape of the code); `int`, `double`, `char` are different doughs. Each time you use a new dough the compiler presses out a fresh cookie, called an **instantiation**. (Nothing happens at run time; it is all decided when the program is compiled.)

Without templates you would write `addInt`, `addDouble`, `addFloat`… with identical bodies.

## 2. One type parameter (slides 5–7)

```cpp
template <typename T>
T add(T a, T b) { return a + b; }
```

- `template <typename T>` says "the next function uses a placeholder type named `T`". (`class T` means the same; `T` is just a name.)
- Every `T` in the function is replaced by the real type.

Verified outputs of slides 6–7: `add(3,4)` → **7**, `add(2.5,6.8)` → **9.3**, `maximum(3,7)` → **7**, `maximum(3.5,2.1)` → **3.5**, `maximum('a','z')` → **z**.

### 2.1 How `T` is chosen (deduction) — the slides skip this

The compiler looks at the **arguments** and deduces `T` from them:

| Call | `T` becomes |
|---|---|
| `add(3, 4)` | `int` |
| `add(2.5, 6.8)` | `double` |
| `maximum('a', 'z')` | `char` |

⚠️ **Both arguments must give the *same* `T`.** `add(3, 4.5)` fails:

```
error: no matching function for call to 'add(int, double)'
note:  deduced conflicting types for parameter 'T' ('int' and 'double')
```

Two fixes (both verified): tell the compiler explicitly, `add<double>(3, 4.5)` → **7.5**; or use **two** parameters (next section).

### 2.2 "Works with any type" is not quite true (slide 3)

The body must only use operations the type supports.

| Call | Result |
|---|---|
| `add(string("con"), string("cat"))` | `concat` (`+` joins strings) |
| `maximum(string("apple"), string("banana"))` | `banana` (`>` compares text) |
| `maximum(P, P)` where `P` is your own struct | **compile error** `no match for 'operator>'` (P has no `>`) |

⚠️ **Trap with text literals:** `maximum("apple", "kiwi")` **compiles**, but `T` becomes `const char*`, so it compares the two *addresses in memory*, not the words. Use `string("apple")` instead.

⚠️ **Overflow is still your problem:** `add(2000000000, 2000000000)` with `int` gives `-294967296`; `add<long long>(2000000000, 2000000000)` gives **4000000000**.

### 2.3 What "type safety" (slide 4) really means

Mistakes such as `add(3, "x")` are caught by the compiler, not at run time. That is the benefit the slide is pointing at.

## 3. Two type parameters (slides 8–10)

When the arguments may have different types, use `T1` and `T2`:

```cpp
template <typename T1, typename T2>
void printPair(T1 a, T2 b) {
    cout << "First: "  << a << endl;
    cout << "Second: " << b << endl;
}
printPair(8, 42.5);        // T1 = int,         T2 = double
printPair("Hello", 2025);  // T1 = const char*, T2 = int
```

Verified output: `First: 8 / Second: 42.5 / First: Hello / Second: 2025`.

⚠️ **Slide 9's `main` does not compile.** It writes `cout << printPair(8, 42.5) << endl;`, but `printPair` is a **`void`** function; there is nothing to print:

```
error: no match for 'operator<<' (operand types are 'std::ostream' and 'void')
```

Just call `printPair(8, 42.5);`. (The slide also uses `’’` and curly `“ ”` quotes; type ordinary `"`.)

⚠️ **Slide 10 prints `0`, not `false`.** `compareValues(a,b)` returns a `bool`; `cout` prints `bool` as `1` or `0` unless you add `boolalpha`. Verified: the line prints `Are both values 69 & 96 equal? 0`. With `cout << boolalpha << …` it prints `false`.

Also note `T1` and `T2` are **independent**: `compareValues(69, 96.0)` compiles (int vs double); with `<typename T>` it would not.

---

## 4. Exercises — worked solutions

**Exercise 1 (slide 11) — `squareValue`:**

```cpp
template <typename T> T squareValue(T v) { return v * v; }
// int n; cin >> n; cout << squareValue(n);
```
`squareValue(12)` → 144; `squareValue(7)` → 49; `squareValue(2.5)` → 6.25.

**Exercise 2 (slide 12) — `swapValues` with two types:**

```cpp
template <typename T1, typename T2>
void swapValues(T1 &a, T2 &b) { T1 temp = a; a = b; b = temp; }
```
The parameters must be **references** (Chapter 5) or the caller's variables would not change.

⚠️ **The exercise has a hidden catch.** An `int` cannot hold `3.7` and a `float` variable can hold an int, so the swap is **lossy**. Verified: with `i = 5` and `f = 3.7`, after `swapValues(i, f)` we get **`i = 3, f = 5`**, not `3.7` and `5`. The variables keep their own types. In a report, say the values were "exchanged with conversion" (`int` truncates); a template swap is exact only when both variables have the *same* type (the standard library's `std::swap` requires that).

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Truth |
|---|---|---|
| 9 | `cout << printPair(8, 42.5)` | `printPair` returns `void`; won't compile |
| 10 | output `equal? false` | prints `0` without `boolalpha` |
| 3 | works with "any data type" | only types that support the operations used |
| 5–6 | (no mention) | both args must deduce the same `T` |
| 12 | swap values of different types | lossy: int truncates |

**Exam strategy:** answer with the slide's outputs if a question quotes them, but in your own programs call `printPair(...)` on its own line and use `boolalpha`.

## Cheat sheet

| Need | Write |
|---|---|
| one type | `template <typename T> T f(T a, T b)` |
| two types | `template <typename T1, typename T2> void f(T1 a, T2 b)` |
| force `T` | `f<double>(3, 4.5)` |
| change caller's variables | reference parameters `T &a` |
| print bool as text | `cout << boolalpha << x;` |
| comparing text | use `string`, not `"literals"` |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** `template <typename T> T add(T a, T b)` — what happens with `add(3, 4.5)`? (a) returns 7.5 (b) returns 7 (c) compile error (d) runtime error
**A2.** `compareValues(69, 96)` returns a `bool`; `cout << compareValues(69,96);` prints (a) `false` (b) `0` (c) `true` (d) `69`
**A3.** When is `T` decided? (a) while the program runs (b) at compile time (c) at link time only (d) when the user types
**A4.** `maximum("apple", "kiwi")` with `template <typename T> T maximum(T,T)` (a) compares alphabetically (b) compares pointer addresses (c) fails to compile (d) always returns "kiwi"
**A5.** Minimum number of template parameters to accept an `int` and a `float` in one function call? (a) 1 (b) 2 (c) 3 (d) 0

### B. Short answer

**B1.** Explain why slide 9's `cout << printPair(8, 42.5) << endl;` fails.
**B2.** When would you use `<typename T1, typename T2>` instead of `<typename T>`?
**B3.** Give two benefits of templates named on slide 4 and one limitation not on the slide.

### C. Calculation / trace

**C1.** `squareValue(7)`, `squareValue(1.5)`.
**C2.** `int i = 5; float f = 3.7f; swapValues(i, f);` — give `i` and `f` afterwards.
**C3.** `add<long long>(2000000000, 2000000000)` versus `add(2000000000, 2000000000)` (both `int`).

### D. Thinking

**D1.** Why does `maximum("apple","kiwi")` compile yet give unreliable results, and how do you fix it?
**D2.** You need `maximum` for your own struct `Student` (compare by `cgpa`). What must you provide?

---

### Answers

**A1 → (c).** `T` deduced as `int` and `double` conflict (verified).
**A2 → (b) `0`.** Unless `boolalpha` is used (verified).
**A3 → (b).** The compiler creates each instantiation.
**A4 → (b).** `T = const char*`, so addresses are compared.
**A5 → (b).** One `T` cannot be both `int` and `float`.

**B1.** `printPair` is a `void` function, so `printPair(...)` has no value that `<<` can print (`no match for operator<<` with `void`). Call it as a statement.

**B2.** When the two arguments may have different types (`printPair(8, 42.5)`, `compareValues(int, double)`). With one `T` both must be the same type.

**B3.** From slide 4: less duplicated code; one place to maintain (also reuse, compile-time type checking). Limitation: the type must support the operations in the body (e.g. `>` for `maximum`), otherwise compile error (verified for a struct).

**C1.** **49** and **2.25**. (Verified.)
**C2.** `i = 3`, `f = 5` (the float 3.7 is truncated when stored in `int`). Verified.
**C3.** **4000000000** versus **−294967296** (signed `int` overflow). Verified for the first; the second is an overflow (undefined behaviour in the language, wraps on this machine).

**D1.** With `const char*` arguments `T` is a pointer, so `>` compares memory addresses, which say nothing about spelling. Fix: pass `string("apple")` and `string("kiwi")` (verified `maximum(string,string)` gives `banana` correctly), or provide a specialised version for C strings.

**D2.** An `operator>` for `Student` (`bool operator>(const Student &a, const Student &b) { return a.cgpa > b.cgpa; }`), because the template body uses `>` and the compiler reports `no match for operator>` otherwise (verified with a struct `P`). (Operator overloading is beyond this chapter; alternatively pass a comparison function.)

---

## Links to other chapters

- **Ch 5:** references (`T &a`) are needed for swap; by-value templates just copy.
- **Ch 1:** `vector<int>` is a class template: `vector<T>`; the `<int>` is the same idea as `<double>` in `add<double>`.
- **Ch 8:** `typedef`/`enum` create user-defined types; templates can be applied to them if they support the operations.
