# C++ Programming — Chapter 1: Advanced Array Manipulation

> The slides show *what* arrays and vectors look like but skip *why* (fixed size vs. growing, what `begin()/end()` really are) and contain a few outright errors (`08` in an initializer, `end()` described like `back()`, an `int sum` that silently truncates). This note fills those gaps. All code below was compiled and run with g++ 13 (`-std=c++20`).

## 0. One-sentence overview

An **array** is a fixed-size row of same-type boxes reached by index; a **2-D array** is a table of them; a **`vector`** is an array that can grow and shrink and comes with helper functions.

| Section | Slides | Key idea |
|---|---|---|
| 1. 1-D arrays | 2–17 | index starts at 0, declare / initialise / loop |
| 2. 2-D arrays | 18–26 | `arr[row][col]`, row / column / whole-table loops |
| 3. `vector` | 27–34 | `push_back`, `erase`, `insert`, iterators |

---

## 1. One-dimensional arrays

**Analogy:** a row of numbered lockers. All lockers are the same size (same type), the row length is fixed when you build it, and locker numbers start from **0**.

```
int score[8];        index:  0    1    2    3    4    5    6    7
                            [ ? ][ ? ][ ? ][ ? ][ ? ][ ? ][ ? ][ ? ]
```

The `?` means "garbage": a local array is **not** cleared automatically (slide 5).

### 1.1 Initialising

| Form | Result |
|---|---|
| `int a[3] = {2,3,1};` | full list |
| `int a[] = {2,3,1};` | compiler counts → size 3 (slide 8) |
| `int a[5] = {1,2};` | `1 2 0 0 0` — **missing values become 0** (slide doesn't say this) |
| `int a[5];` (local) | garbage |

Verified output of `int a[5]={1,2};` → `1 2 0 0 0`.

⚠️ **Slide 7 error:** `int score[8] = { 95,08,85,... }` **does not compile.** A number starting with `0` is **octal** in C++, and `8` is not an octal digit:

```
error: invalid digit "8" in octal constant
```

Even `010` compiles but means **8**, not 10. Write `8`, not `08`.

### 1.2 Processing a whole array

Use a `for` loop, because there is no "do this to all" shortcut. Standard patterns (slides 11–14):

```cpp
for (index = 0; index < 10; index++) cin >> sales[index];      // read
for (index = 0; index < 10; index++) cout << sales[index];     // print
largest = sales[0];                                            // start from element 0, not 0!
for (index = 1; index < 10; index++)
    if (largest < sales[index]) largest = sales[index];
```

**Why `largest = sales[0]`:** if you started with `largest = 0`, an array of all-negative numbers would wrongly report 0.

⚠️ **Slide 13 pitfall (sum/average):** slide 11 declares `double sum`, but slide 13 writes `int sum = 0;`.
1. Both in the same function → compile error `conflicting declaration 'int sum'`.
2. If `sum` really is `int`, every `sum += sales[i]` **truncates** the running total. Test with `{1.5, 2.5, …, 10.5}`:

| | `double sum` | `int sum` |
|---|---|---|
| total | 60 | 55 |
| average | 6 | 5.5 |

Keep `sum` as `double` when the array holds `double`.

### 1.3 No safety net

C++ does **not** check indexes. Writing `score[8]` on `int score[8]` compiles (g++ only warns: `iteration 8 invokes undefined behavior`) and corrupts whatever memory sits next to the array. Valid indexes are `0 … size-1`.

Also: you **cannot** copy arrays with `=` (`b = a;` → `error: invalid array assignment`). Copy element by element in a loop (slide 16 does this to build `SQUARE`).

**Array size trick:** `sizeof(arr) / sizeof(arr[0])` gives the element count (for `int arr[5]`: 20 / 4 = 5). It works only where `arr` is a real array, **not** inside a function that received it (see Chapter 6).

### 1.4 Index expressions (slide 17)

Any integer expression works as an index. With `int x[5]={1,2,3,8,7}; int i=2;`

| Expression | Element | Value |
|---|---|---|
| `x[i+1]` | `x[3]` | 8 |
| `x[2*i]` | `x[4]` | 7 |
| `x[0]` | | 1 |

The words "4th element" and "5th element" on the slide count from 1; the **index** is one less. This off-by-one is the #1 source of array bugs (see the hotel exercise below).

---

## 2. Two-dimensional arrays

**Analogy:** a spreadsheet. `ARR_2D[row][col]`. Declare with **rows first**: `int ARR_2D[3][4]` = 3 rows × 4 columns = 12 elements.

```
            col0 col1 col2 col3
   row 0  [  2    4    6    8 ]
   row 1  [  1    3    5    7 ]
   row 2  [  1    4    9   16 ]        ARR_2D[1][3] = 7 (row 1, col 3)
```

**In memory it is one long line, row after row** ("row-major"). Verified: `&m[1][0] - &m[0][0] = 4` (one row later = 4 ints later), and viewed flat it is `2 4 6 8 1 3 5 7 1 4 9 16`. This explains why the initialiser can be a flat list, and why Chapter 6 needs the column count when you pass a 2-D array to a function.

### 2.1 The three loop patterns (slides 21–24)

Fix one index, loop the other:

| Goal | Loop | Result on `ARR_2D` |
|---|---|---|
| Sum of row 2 (row index 1) | `for col: sum += A[1][col]` | 1+3+5+7 = **16** |
| Sum of column 4 (col index 3) | `for row: sum += A[row][3]` | 8+7+16 = **31** |
| Grand total | nested loops | 2+4+6+8+1+3+5+7+1+4+9+16 = **66** |

**Slides 23 vs 24:** "row by column" (outer = row) and "column by row" (outer = column) give the **same total**, verified 66 = 66. The difference is only the *order* of visiting. Row-by-column matches how memory is laid out, so it is generally the faster one on large arrays. (Extra, not in slides.)

### 2.2 Exercise (slides 25–26) — worked solution

The trap is **room numbers vs. indexes**. Room "23-9" is level 23, unit 9 → `hotel[22][8]`.

```cpp
#include <iostream>
using namespace std;
const int LEVELS = 25, ROOMS = 15;
int main() {
    int hotel[LEVELS][ROOMS] = {};              // (a) all 0 guests
    for (int level = 11; level <= 12; level++)   // (b) levels 11 and 12
        for (int room = 1; room <= ROOMS; room++) {
            cout << "Guests for room " << level << "-" << room << ": ";
            cin >> hotel[level - 1][room - 1];   // subtract 1 for the index
        }
    hotel[18 - 1][5 - 1] = 4;                    // (c) room 18-5 -> 4 guests
    int total = 0;                               // (d) total on levels 11 & 12
    for (int level = 11; level <= 12; level++)
        for (int room = 0; room < ROOMS; room++)
            total += hotel[level - 1][room];
    cout << "Total guests on levels 11 and 12: " << total << "\n";
}
```

Tested with 2 guests in every room of the two levels: total = **60** (30 rooms × 2); room 18-5 reads back as 4.

---

## 3. `vector` — an array that can grow

**Why it exists:** a normal array's size must be known when you write the program. A `vector` remembers its own size and resizes itself when you `push_back`. Needs `#include <vector>`.

```cpp
vector<int> num = {1,2,3,4,5};
```

### 3.1 The functions (slides 28–29), with what they really do

| Call | Effect | Note |
|---|---|---|
| `push_back(v)` / `pop_back()` | add / remove at the **end** | fast |
| `size()` / `empty()` / `clear()` | count / test / remove all | |
| `at(i)` | element `i`, **bounds-checked** | throws `out_of_range` |
| `v[i]` | element `i`, **no check** | out-of-range = undefined behaviour |
| `front()` / `back()` | **value** of first / last | |
| `insert(pos, val)` | insert **before** `pos` | `pos` is an iterator, e.g. `v.begin()+2` |
| `erase(pos)` | remove element at `pos` | later elements shift left |
| `resize(n)` | make size `n` | grow → new elements are 0; shrink → drops the tail |
| `swap(other)` | exchange contents | |

Verified: `v.at(10)` on a 5-element vector throws (`vector::_M_range_check: __n (which is 10) >= this->size() (which is 5)`). `resize(8)` on `{1,1,2,3,5}` gives `1 1 2 3 5 0 0 0`; `resize(3)` then leaves `1 1 2`.

### 3.2 `size()` vs `capacity()` (slide 30)

- `size()` = how many elements you have **now**.
- `capacity()` = how many the vector can hold **before it must find a bigger block of memory and copy everything over**.

```
capacity() = 8
[ 1 | 1 | 2 | 3 | 5 |   |   |   ]
  begin()        size() = 5  ^end()
```

Growth strategy is up to the compiler. On g++ it doubles: pushing 40 elements one by one showed capacity `1 2 4 8 16 32 64`. Other compilers may use a different factor (Visual Studio is commonly said to use ×1.5; I could not test that here), so **don't memorise exact numbers**. `resize(3)` does *not* shrink the capacity (it stayed 10 in my test).

### 3.3 Iterators, `begin()`, `end()` (slides 31–32) — where the slides mislead

An **iterator** is a "finger" pointing at an element; `*it` reads or changes the element it points to.

- `begin()` → iterator to the **first** element.
- `end()` → iterator to **one past the last** element (a marker meaning "stop"). **You must not dereference it.**
- `front()` / `back()` → the **values** of the first / last element.

⚠️ **Slide 32 says "`end()` and `back()` work similar like `begin()` and `front()`."** That is only half true. `begin()`↔`front()` correspond, but `end()` is **not** the last element; the last element is `*(end()-1)` = `back()`. The slide's own figure (slide 30) draws `end()` after the last box. Dereferencing `*v.end()` is undefined behaviour (on my machine it printed `0`; it could crash).

Useful identity (verified): `end() - begin() == size()`.

### 3.4 The slide 33–34 demo, traced

Slide 33 declares `void main()`. That is a Visual Studio habit; the C++ standard requires `int main()`, and g++ rejects `void main`. The output comments on the slides are correct — checked by running.

| Statement | `num` afterwards |
|---|---|
| `num = {1,2,3,4,5}` | 1 2 3 4 5 |
| `push_back(10); push_back(20);` | 1 2 3 4 5 10 20 |
| `pop_back();` | 1 2 3 4 5 10 |
| `erase(begin()+2)` (removes the 3) | 1 2 4 5 10 |
| `insert(begin()+1, 30)` | 1 30 2 4 5 10 |
| `front()+back()` | 1 + 10 = **11** |
| `it = begin()+1` → `*it` | 30 |
| `it = it + 3` → position 4, `*it = 999` | 1 30 2 4 **999** 10 |

Loop tip: `i < num.size()` compares `int` with an unsigned `size_t`; use `size_t i` to avoid a compiler warning.

⚠️ **Common confusion — erasing inside a loop.** Erasing shifts the remaining elements left, so a plain `for (i…; i++)` **skips** the element that moved into slot `i`. Removing evens from `{2,4,6,7,8}` by index left `4 7` (wrong); advancing `i` only when nothing was erased gives `7` (correct).

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Better understanding |
|---|---|---|
| 7 | `{ 95,08,85,… }` | Compile error (octal). Write `8`. |
| 13 | `int sum = 0;` after `double sum` | Redeclaration error; and int truncates `double` values. |
| 32 | "`end()` and `back()` work similar to `begin()` and `front()`" | `end()` is one **past** the last element; not dereferenceable. |
| 30 | "`capacity()` = maximum elements it can hold" | It is the current allocated room, and grows automatically. |
| 33–34 | `void main()` | Must be `int main()` in standard C++. |

**Exam strategy:** if a question quotes the slide, answer as the slide does, but never write `08` or `*v.end()` in your own code.

## Cheat sheet

| Topic | Rule |
|---|---|
| Array index | `0 … size-1`, unchecked |
| Array size | fixed at compile time; no `=` copy |
| Partial initialiser | remaining elements = 0 |
| 2-D array | `[rows][cols]`, stored row after row |
| Row sum / column sum | fix row (or col), loop the other |
| `at(i)` vs `[i]` | checked (throws) vs unchecked |
| `begin()` / `end()` | first / **one past** last |
| `front()` / `back()` | values, first / last |
| `insert(pos,v)` / `erase(pos)` | `pos` is an iterator (`v.begin()+k`) |
| `size()` / `capacity()` | used / allocated |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** After `int a[5] = {7, 8};` inside `main`, what is `a[2]`?
(a) garbage (b) 0 (c) 7 (d) compile error

**A2.** `int m[3][4];` How many elements does `m` have and which is the last valid element?
(a) 12, `m[3][4]` (b) 12, `m[2][3]` (c) 7, `m[2][3]` (d) 12, `m[12]`

**A3.** Which is true of `v.end()` for a non-empty vector?
(a) points to the last element (b) points one past the last element (c) returns the last value (d) same as `back()`

**A4.** What is the difference between `v[5]` and `v.at(5)` when `v` has 3 elements?
(a) none (b) `[]` throws, `at` doesn't (c) `at` throws, `[]` is undefined behaviour (d) both give 0

**A5.** `int s = 0; double d[3] = {1.5, 2.5, 3.5}; for (int i=0;i<3;i++) s += d[i];` What is `s`?
(a) 7.5 (b) 7 (c) 6 (d) 8

### B. Short answer

**B1.** Explain why `int score[8] = {95, 08, 85, 67, 70, 60, 78, 90};` fails to compile.
**B2.** State the difference between `size()` and `capacity()`.
**B3.** State the difference between `begin()` and `front()`.

### C. Calculation / trace

**C1.** `vector<int> v = {4,8,15,16,23,42};` then `v.erase(v.begin()+1); v.insert(v.begin()+3, 99); v.pop_back(); v.push_back(7);` Give the final contents and `v.front() + v.back()`.

**C2.** `int g[3][3] = {{1,2,3},{4,5,6},{7,8,9}};` Find (i) the sum of the main diagonal `g[0][0], g[1][1], g[2][2]`, (ii) the sum of the 3rd column, (iii) the sum of row index 1, (iv) `g[1][2] + g[2][1]`.

**C3.** `int x[5] = {1,2,3,8,7}; int i = 1;` Evaluate `x[i]`, `x[i+1]`, `x[i+2]`, `x[x[i]+2]`.

### D. Thinking

**D1.** The loop `for (int i = 0; i <= 8; i++) score[i] = 0;` on `int score[8]` compiles. Why is it still a bug, and what is the fix?
**D2.** You must remove all even numbers from a vector using an index loop. Explain why the obvious loop skips elements and give a correct version.

---

### Answers

**A1 → (b) 0.** Once at least one initialiser is given, the rest are zero-filled. (Only a completely uninitialised local array is garbage.)

**A2 → (b).** 3 × 4 = 12 elements; valid rows 0–2, columns 0–3.

**A3 → (b).** `end()` is a marker one past the last element; `back()` is the last value.

**A4 → (c).** `at(5)` throws `out_of_range`. `v[5]` performs no check, so the behaviour is undefined (not "0").

**A5 → (c) 6.** Every `s += d[i]` is computed in `double` and then truncated to `int`: 0+1.5 → 1; 1+2.5 = 3.5 → 3; 3+3.5 = 6.5 → 6. (Adding in `double` first would give 7.5.) Verified by running.

**B1.** A literal starting with `0` is octal in C++, and `8` is not a valid octal digit → `invalid digit "8" in octal constant`. Fix: `8`.

**B2.** `size()` = elements currently stored. `capacity()` = elements the currently allocated memory can hold before the vector must reallocate; always ≥ `size()`.

**B3.** `begin()` returns an **iterator** (a pointer-like position) to the first element, used for looping and with `insert`/`erase`. `front()` returns the **value** of the first element.

**C1.** `{4,8,15,16,23,42}` → erase index 1 → `{4,15,16,23,42}` → insert 99 before index 3 → `{4,15,16,99,23,42}` → pop_back → `{4,15,16,99,23}` → push_back(7) → **`{4,15,16,99,23,7}`**. `front()+back()` = 4 + 7 = **11**. (Verified.)

**C2.** (i) 1+5+9 = **15** (ii) 3+6+9 = **18** (iii) 4+5+6 = **15** (iv) 6+8 = **14**. (Verified.)

**C3.** `x[1]` = **2**; `x[2]` = **3**; `x[3]` = **8**; `x[x[1]+2]` = `x[4]` = **7**. (Verified.)

**D1.** Valid indexes are 0–7. `i <= 8` writes `score[8]`, one element past the end — undefined behaviour (g++ warns `iteration 8 invokes undefined behavior`). It may overwrite another variable or crash. Fix: `i < 8`.

**D2.** After `erase` at index `k`, the next element slides into `k`, but the loop then does `k++` and never examines it. For `{2,4,6,7,8}` the naive loop leaves `{4,7}` (verified). Correct version: only advance when you did **not** erase:
```cpp
for (size_t k = 0; k < w.size(); ) {
    if (w[k] % 2 == 0) w.erase(w.begin() + k);
    else k++;
}
```
Result `{7}` (verified).

---

## Links to other chapters

- **Ch 4 (Pointers):** an array name behaves like a pointer to its first element; iterators behave like pointers.
- **Ch 6 (Advanced Functions II):** passing arrays and 2-D arrays to functions (the column size must be given).
- **Ch 3 (Structures):** arrays can live inside structs and structs can live inside arrays.
