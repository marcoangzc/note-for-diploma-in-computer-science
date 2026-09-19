# C++ Programming — Chapter 6: Advanced Functions II

> This chapter has the most slide problems so far. Several examples do not compile in standard C++ (`auto int`, `int x[][]`, calls before declaration, `void main()`), one prints different numbers from what the slide claims (`count++`), one indexes past the end of an array (`num[1][2]` on a 3×2 array), and "array name is a pointer" is not quite true. This note fixes those, explains *why* arrays change but ordinary variables don't, and solves every exercise. All code was compiled and run with g++ 13.

## 0. One-sentence overview

You can pass **arrays** and **structs** to functions, and every variable has a **scope** (where it can be seen), a **duration** (how long it lives) and a **storage class** (which rules it follows).

| Section | Slides | Key idea |
|---|---|---|
| 1. Arrays → functions | 4–15 | element = copy, whole array = original |
| 2. Structs → functions | 16–25 | by value, by address/reference, return |
| 3. Scope | 28–30 | where a name is visible |
| 4. Storage classes | 31–39 | `auto`, `static`, `register`, `extern` |
| 5. Duration | 40–43 | static / local / dynamic |

---

## 1. Passing arrays

### 1.1 One element → pass by value (slides 5–6)

`findLargest(list[i], largest)` sends a **copy** of one `int`. The function cannot change the array. Nothing new: it works like any `int` parameter.

⚠️ **Slide 6 quietly has a bug.** `#define SIZE 15` but only 11 values are given; the other 4 elements are `0`. The loop runs `i < SIZE`, so it also looks at those zeros. With positive data (max 68) you don't notice, but with the 11 negative numbers `-5 … -11` the slide's method returns **0**, while the correct answer is **−2** (verified). Pass the *real* number of elements.

### 1.2 The whole array (slides 8–11)

Write the parameter as `int x[]` (no `&`) and call with just the name: `findLargest(list)`.

**Why the function changes the original (slide 11):** the function does **not** get a copy. What is passed is the **address of the first element**, so `x[i]` in the function is the caller's `list[i]`. Slide 10's `multiply2(base, SIZE)` therefore doubles the caller's array: `3 7 1 5 8` → `6 14 2 10 16`.

**Analogy:** giving someone a photocopy of a page (one element / ordinary variable) versus giving them the *location of your notebook* (whole array).

⚠️ **"Array name is actually a pointer" (slide 11) is only half true.** An array and a pointer are different things: the array name is *converted* to a pointer to its first element when you pass it. Proof (verified):

| | Real array in `main` | Parameter `int x[]` |
|---|---|---|
| `sizeof(...)` for 15 ints | **60** | **8** (size of a pointer) |

Inside the function `x` is really `int *x`, so `sizeof(x)` gives 8 and the compiler warns `sizeof on array function parameter will return size of 'int*'`. That is why slide 8 says the written size is "ignored", and why you must **pass the size separately**:

```cpp
void multiply2(int x[], int size);     // slide 10 does this correctly
```

**Safer version:** if the function must not modify the array, write `const int x[]`.

### 1.3 Strings (slide 13)

A `char` array is passed the same way, so `fun2` changes the caller's string. Verified output `hate love love` (call ①②③). Needs `<cstring>` for `strcpy`, and `char str[5]` is exactly big enough for `"hate"` (4 letters + `'\0'`).

### 1.4 Two-dimensional arrays (slides 14–15) — two slide errors

⚠️ **Slide 14:** `int num[3][2]` has columns `0` and `1` only. `display(num[1][2])` is **outside the row**. It printed `55` (the memory just after the row, which is `num[2][0]`) and the undefined-behaviour checker reports `index 2 out of bounds for type 'int [2]'`. The intended element was probably `num[1][1]` = **44**.

⚠️ **Slide 15:** `void display(int x[][])` **does not compile**: `declaration of 'x' as multidimensional array must have bounds for all dimensions except the first`. The function needs the **column count** to compute where each row starts (recall from Chapter 1 that rows are stored one after another). Fixed and verified:

```cpp
const int COLS = 2;
void display(int x[][COLS], int rows) {
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < COLS; c++) cout << x[r][c] << " ";
        cout << "\n";
    }
}
// display(num, 3);  prints:  11 22 / 33 44 / 55 66
```

**Returning an array is not allowed** (slide 4): `int f()[3]` gives `'f' declared as function returning an array`. A *struct* can be returned even if it contains an array (verified), and so can a `vector`.

### Exercises (slides 7 and 12) — solutions

```cpp
float toFahrenheit(float c) { return (c * 9.0 / 5.0) + 32; }      // slide 7
int countPassed(const int marks[], int n) {                        // slide 12
    int cnt = 0;
    for (int i = 0; i < n; i++) if (marks[i] >= 50) cnt++;
    return cnt;
}
```

Tests: `0,37,100,-40,25 °C` → `32.0, 98.6, 212.0, -40.0, 77.0 °F`. For 25 sample marks `countPassed` returned **16** (hand-counted the same). Use `9.0 / 5.0`, not `9 / 5` (which is 1).

---

## 2. Passing structs (slides 16–25)

| Method | Parameter | Original changes? | Slide |
|---|---|---|---|
| one member | `float cgpa` | No | 17 |
| whole struct by value | `Student s` | No | 18 |
| whole struct by address | `Student *s` → `s->cgpa` | Yes | 20 |
| whole struct by reference | `Student &s` → `s.cgpa` | Yes | 21 |

`s->cgpa` is shorthand for `(*s).cgpa`. Use `.` with an object or reference, `->` with a pointer.

**Answers to the fill-in-the-blanks:**

| Slide | Blank | Answer |
|---|---|---|
| 17 | (A) | `float cgpa`; outputs ① 4.0 ② 3.5 |
| 18 | (A) | `Student`; outputs ① 4.0 ② 3.5 (the copy changed, not `stud`) |
| 20 | (A) | `Student *` (or `Student &`); outputs ① 4.0 ② **4.0** |
| 21 | (A) `Student` (B) `s.name` (C) `s.cgpa` (D) `stud` | |

⚠️ Slide 20 has a garbled line, `(*s).cgpa = 4.0; cout << cgpa;`: `cgpa` alone is not a name that exists there; it must be `(*s).cgpa` or `s->cgpa`. Slide 21 has an extra `)` after `stud.cgpa`.

**Returning a struct (slide 24):** allowed, and the whole struct is copied back. `Student askRecord()` builds a local `stud` and returns it.

### Exercises (slides 19, 22–23, 25) — solutions

```cpp
struct Student { string name, id; float cgpa; };
void display(Student s) { cout << s.name << " " << s.id << " " << s.cgpa << "\n"; }   // slide 19

struct Car { string model; int km; double fuel; };                                    // slides 22-23
void serviceCar(Car &c) { c.km = 0; }                       // by reference
void refuel(Car *c, double liters) { c->fuel += liters; }   // by address
// main: Car car = {"X70", 56000, 18.5}; serviceCar(car); refuel(&car, 30.0);
//       -> X70 km=0 fuel=48.5

struct Time { int hour, minute; };                                                    // slide 25
Time askTime() { Time t; cout << "Hour: "; cin >> t.hour; cout << "Minute: "; cin >> t.minute; return t; }
```

(The slide says "hour and time"; it means hour and **minute**. Slide 22's "duel" means **fuel**.) The refuel amount 30 is my test value.

---

## 3. Scope (slides 28–30)

**Scope** = the region where a name can be used. Rule (slide 28): **from the point of declaration to the end of its block `{ }`.**

Slide 29, with the line numbers from the figure:

| Variable | Scope (lines) | Comment |
|---|---|---|
| `a` (line 1, global) | 1–14 | but hidden in lines 5–7 |
| `b` (line 3, parameter) | 3–7 | |
| `a` (line 5, local) | 5–7 | **shadows** the global `a` |
| `d` (line 9) | 9–14 | |
| `e` (line 12) | 12–14 | |

Output of `show`: the `printf` on line 4 prints the **global** 10 (local `a` isn't declared yet), line 6 prints **20** — verified `10 20`. Careful: `a (line 1)` still has scope 1–14 even though a name hides it inside `show`. That is the difference between *scope* and *visibility*.

Slide 30 works the same way (answers on the slide: `x` line 1 = 1–12, `x` line 2 = 2–6, `a` line 4 = 4–6, `a` line 7 = 7–12, `x` line 10 = 10–12).

⚠️ Slide 28's code uses `#include <stdio.h>` but `cout`; use `<iostream>`.

---

## 4. Storage classes (slides 31–39)

The slides list four: `auto`, `static`, `register`, `extern`.

### 4.1 ⚠️ `auto` and `register` are out of date

| Slide code | Result (verified) |
|---|---|
| `auto int a = 100;` (slide 33) | OK in C++98; **error in C++11 and later**: `two or more data types in declaration of 'a'`. Since C++11 `auto` means "deduce the type" (`auto a = 100;`). |
| `register int d;` (slide 36) | g++ with `-std=c++17` warns: `ISO C++17 does not allow 'register' storage class specifier`. It has been useless since compilers ignore it. |

For the exam, know the textbook meaning: `auto` = normal local variable (stack, dies at `}`); in real code **just write `int a;`**.

### 4.2 The four classes

| Class | Lives | Value between calls | Notes |
|---|---|---|---|
| `auto` (default for locals and parameters) | created on entry, destroyed at `}` | lost | on the stack |
| `static` local | whole program | **kept** | initialised **once** |
| `register` | like `auto` | lost | "please keep in a CPU register", compilers ignore it; gone in modern C++ |
| `extern` | whole program | kept | **declares** a global defined elsewhere; no memory allocated by itself |

### 4.3 `static` — trace it (slides 34–35)

⚠️ **Slide 35's comments are wrong.**

```cpp
int counter() { static int count = 0; return count++; }
cout << counter();   // slide: "// 1"      real: 0
cout << counter();   // slide: "// 2"      real: 1
```

`count++` returns the **old** value and then increments, so the calls return **0, 1, 2** (verified: `012`). With `return ++count;` you get `1, 2, 3` (also verified). The slide's own explanation ("the second call uses count = 1") matches 0-then-1, not 1-then-2.

The initialiser runs **only once**: verified with a function whose initialiser prints `[init runs]`; it printed once, then values `7`, `8`. (Slide 34's phrase "allocated and initialised… at compile time" is a simplification: for a constant initialiser like `= 0` that is effectively true; for a runtime initialiser it happens the first time execution reaches the line.)

### 4.4 `extern` and global vs local (slides 37–38)

Two outputs on slide 38 (verified, no separators): **`105`** (`display` has its own local `b = 5` that hides the global) and **`1010`** (`extern int b;` inside `display` means "the global `b`").

⚠️ As printed, slide 38 calls `display()` from `main` **before it is declared** → `'display' was not declared in this scope`. Add `void display();` above `main`. Also `void main()` again.

`extern int p;` on its own allocates **no** memory: it linked fine unused, and using it with no definition anywhere gives `undefined reference to 'p'` (verified). That answers slide 42.

### 4.5 Exercise (slide 39) — solution

`A` global (static duration), `B` auto (`main`), `C` auto, `D` **static**, `E` auto (parameter).

| B | `f1(B)`: C = 2 + B + 20 | `f2(B)`: D (kept) |
|---|---|---|
| 0 | 22 | 2 + 0 + 20 = **22** |
| 1 | 23 | 22 + 1 + 20 = **43** |
| 2 | 24 | 43 + 2 + 20 = **65** |

Printed order (f1 then f2 each time): **`22 22 23 43 24 65`** (verified). `C` restarts from 2 each call; `D` accumulates.

---

## 5. Duration (slides 40–43)

| Duration | Which variables | Lives |
|---|---|---|
| Static | globals, `static` locals | whole program |
| Local (automatic) | ordinary locals, parameters | one function call |
| Dynamic | `new` variables | until `delete` (Chapter 4) |

Slide 41: `main` prints `num` (20), `display` prints its local `a` (10), `main` prints `num` again: real output **`20`, `10`, `20`** → `201020` (verified). The slide's comments read `20, 20, 10` in visual order; the true order is 20, 10, 20.

**Slide 42** (the tick marks are hidden animations in the file; answers derived): variables that **might not allocate memory** are **(d) `register`** (may live in a CPU register) and **(e) `extern`** (only a declaration).
**Slide 43** (same): deallocated when `fun()` ends are **a, b, d** (auto/register locals). `c` (static) and `e` (extern) stay.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Truth |
|---|---|---|
| 6, 9 | loops to `SIZE` with 11 values | zeros included; wrong for all-negative data |
| 11 | "Array name is actually a pointer" | converts to a pointer when passed; `sizeof` differs (60 vs 8) |
| 14 | `display(num[1][2])` on `num[3][2]` | out of bounds |
| 15 | `int x[][]` | compile error; give column count |
| 33 | `auto int a` | error since C++11 |
| 35 | outputs `1`, `2` | `0`, `1` |
| 36 | `register` | ignored/removed |
| 38 | call before declaration | needs a prototype |
| 41 | comments `20 20 10` | real order `20 10 20` |
| 13, 14, 17, 33, 35, 38 | `void main()` | must be `int main()` |

**Exam strategy:** answer with the slide's textbook meaning (`auto` = default local; array passed "by reference"), but never copy these examples into your own code.

## Cheat sheet

| Passing | Function header | Changes original? |
|---|---|---|
| array element | `int x` | No |
| whole array | `int x[], int n` | **Yes** |
| 2-D array | `int x[][COLS], int rows` | Yes |
| struct by value | `Student s` | No |
| struct by address | `Student *s` (`s->m`) | Yes |
| struct by reference | `Student &s` (`s.m`) | Yes |

| Storage | Scope | Duration |
|---|---|---|
| auto local | block | call |
| static local | block | program |
| global | file (`extern` for others) | program |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** `int counter(){ static int count = 0; return count++; }` — values of the first two calls? (a) 1, 2 (b) 0, 1 (c) 0, 0 (d) 1, 1
**A2.** Which are deallocated when `fun()` ends: `int a; auto int b; static int c; register int d; extern int e;`? (a) a,b,d (b) all (c) a,b (d) c,e
**A3.** Inside `void f(int x[])`, `sizeof(x)` on a 64-bit system is (a) size of the whole array (b) 8 (c) 4 (d) 1
**A4.** Which prototype is illegal? (a) `void f(int x[][5])` (b) `void f(int x[][])` (c) `void f(int x[5][5])` (d) `void f(int x[])`
**A5.** `int a=10;` global, and `void show(){ cout << a; int a = 20; cout << a; }` prints (a) `1020` (b) `2020` (c) `1010` (d) error

### B. Short answer

**B1.** Why does changing an array element inside a function change the caller's array, but changing an `int` parameter doesn't?
**B2.** Distinguish *scope* from *duration*.
**B3.** Why can a function return a struct but not an array?

### C. Trace

**C1.** Slide 39's program: give the output.
**C2.** Slide 41's program: give the output.
**C3.** `int list[15] = {-5,-2,-7,-8,-36,-4,-2,-68,-22,-34,-11};` and the slide-9 `findLargest` loop over 15 elements. What does it return, and what is the correct maximum of the 11 values?

### D. Thinking

**D1.** `int num[3][2]`; explain what `num[1][2]` really refers to and why it is a bug.
**D2.** For each, choose auto, static, or global: (i) a loop counter; (ii) the number of times a function has been called; (iii) a tax rate used by ten functions.

---

### Answers

**A1 → (b).** `count++` returns the old value. (Verified `012`.)
**A2 → (a).** a, b, d are automatic; static `c` and extern `e` survive.
**A3 → (b) 8.** The parameter is really a pointer.
**A4 → (b).** Only the first dimension may be omitted.
**A5 → (a) `1020`.** The first `a` is the global (10); after the local is declared, `a` is 20. (Verified `10 20`.)

**B1.** For an array the function receives the *address of the first element*, so it works on the caller's memory. An `int` parameter is a *copy*; only the copy changes.

**B2.** Scope = where in the code a name can be used. Duration = how long the memory exists at run time. They can differ: a `static` local has block scope but program duration.

**B3.** Arrays cannot be copied or returned by value (`declared as function returning an array`), but a struct can be copied whole, even if it holds an array (verified `123`).

**C1.** `22 22 23 43 24 65`. **C2.** `20`, `10`, `20`.
**C3.** The loop also compares the four zeros, so it returns **0**; the correct maximum is **−2**. Verified.

**D1.** Row 1 has columns 0 and 1 only. `num[1][2]` steps past the row; it happens to be `num[2][0]` in memory (55), but that is undefined behaviour (the checker reports `index 2 out of bounds`). The likely intention was `num[1][1]` = 44.

**D2.** (i) auto (normal local); (ii) `static` local (keeps its value between calls, hidden from other functions); (iii) a global — better a `const` global — since many functions share it (but prefer parameters, Chapter 11).

---

## Links to other chapters

- **Ch 1:** 2-D arrays are stored row after row, which is why the column size is needed.
- **Ch 3:** structs (`.` and members). **Ch 4:** pointers, `->`, addresses. **Ch 5:** by value / reference / address.
- **Ch 9:** each recursive call gets its own *automatic* variables.
- **Ch 11:** global variables lead to *common coupling*.
