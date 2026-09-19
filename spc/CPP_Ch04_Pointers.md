# C++ Programming — Chapter 4: Pointers

> The slides define pointers well but skip the two things students trip on most: `*` and `&` each mean *two different things*, and `new` without `delete` leaks memory (the slide-15 program leaks). They also assume `int` = 4 bytes and `long` = 4 bytes, which is only true on some systems, and one program contains a full-width Chinese comma that will not compile. Everything below was compiled and run with g++ 13 on 64-bit Linux.

## 0. One-sentence overview

A **pointer** is a variable that stores the **address** of another variable; you follow the address with `*`, and you can create nameless variables with `new`.

| Section | Slides | Key idea |
|---|---|---|
| 1. Address & pointer | 3–8 | `&x` = address, `int *p` = pointer |
| 2. Dereference | 9–13 | `*p` = the thing pointed at |
| 3. `new` | 14–15 | nameless variables, and `delete` |
| 4. Pointer arithmetic | 16–22 | `p+1` moves by one *element* |
| 5. References | 23–24 | an alias, not a pointer |

---

## 1. Addresses and pointer variables

**Analogy:** a variable is a **house**; its value is the person inside; its **address** is the street address on the letter. A pointer is a **piece of paper with a street address written on it** — not the house itself.

```
        x                    ptr
   ┌─────────┐          ┌──────────┐
   │   10    │ ◄─────── │  0x7ffe… │      ptr holds x's address
   └─────────┘          └──────────┘
   address 0x7ffe…
```

```cpp
int x = 10;
int *ptr = &x;      // ptr stores the address of x
```

### 1.1 The two meanings of `&` and `*` (not stated in the slides)

| Symbol | In a **declaration** | In an **expression** |
|---|---|---|
| `&` | `int &r = x;` → *r is a reference (alias)* | `&x` → *address of x* |
| `*` | `int *p;` → *p is a pointer* | `*p` → *the value p points to* |

Most pointer confusion is reading one meaning as the other.

### 1.2 Declaration rules (slides 5–6)

- The pointer's type must match what it points at: `int*` → `int`, `double*` → `double`.
- The `*` may touch the type or the name: `int *p; int* p; int * p;` are identical.
- ⚠️ **`int *p, q;` makes only `p` a pointer.** `q` is a plain `int`. Verified: `q = &x;` fails with `invalid conversion from 'int*' to 'int'`. Write `int *p, *q;` for two pointers.
- Declaring a pointer gives it **no target** (slide 7). Until you assign one, it contains garbage.

### 1.3 Assigning the address (slides 7–8)

```cpp
double a = 10;
double *number = &a;      // OK: declare + point in one line
number = &a;              // OK: point later
*number = &a;             // WRONG
```

Slide 8's crossed-out line fails to compile: `cannot convert 'double*' to 'double' in assignment`. `*number` is a `double` (the target), and you tried to put an address inside it.

### 1.4 Printing an address (slide 3)

`cout << &var1;` prints an address for an `int`. For a `char`, `cout` assumes a `char*` is a **text string** and would print characters until it finds `'\0'`. That is why slide 3 writes `(void *)&var2`: it tells `cout` "treat this as a plain address". Addresses differ each run.

---

## 2. Dereferencing and null (slides 9–13)

`*ptr` **is** the variable pointed at, so it works on both sides of `=`:

```cpp
int num = 10, *ptr = &num;
cout << *ptr;       // 10
*ptr = 20;          // num is now 20
```

Slide 10 shows three different things about `p = &a`:

| Expression | Meaning |
|---|---|
| `a` and `*p` | the same value (7, later 10) |
| `&a` and `p` | the same address |
| `&p` | the address of the pointer variable **itself** (a different address) |

### 2.1 Null pointers (slide 11)

`NULL` (or `0`) means "points to nothing". Modern C++ (C++11) prefers **`nullptr`**. Dereferencing a null pointer crashes: verified, `*p` with `p = nullptr` gives *Segmentation fault* (exit code 139). Check `if (p != nullptr)` before using it.

⚠️ An **uninitialised** pointer is worse: it holds a random address, so `*p = 5;` writes to a random place (undefined behaviour). Always initialise to `nullptr` or a real address.

### 2.2 Tracing slides 12–13 (values verified: `10/20` both)

Slide 13, step by step (`value1=5`, `value2=15`):

| Statement | value1 | value2 | p1 points to | p2 points to |
|---|---|---|---|---|
| `p1=&value1; p2=&value2;` | 5 | 15 | value1 | value2 |
| `*p1 = 10;` | 10 | 15 | value1 | value2 |
| `*p2 = *p1;` (copy **value**) | 10 | 10 | value1 | value2 |
| `p1 = p2;` (copy **address**) | 10 | 10 | value2 | value2 |
| `*p1 = 20;` | 10 | 20 | value2 | value2 |

**Key contrast:** `*p2 = *p1` copies the *values*; `p1 = p2` copies the *addresses* (now both point to the same variable).

⚠️ **Slide 13 does not compile as printed.** The declaration `int value1 = 5, value2 = 15， *p1, *p2;` contains a **full-width Chinese comma `，`** after `15`. g++ reports `stray '\' in program`. Replace it with an ordinary `,`.

---

## 3. Dynamic variables with `new` (slides 14–15)

`new int` asks the system for a **nameless** int on the **heap** and returns its address, so you can only reach it through a pointer.

Slide 15 (values verified):

| Statement | `*p1` | `*p2` |
|---|---|---|
| `p1 = new int; *p1 = 42; p2 = p1;` | 42 | 42 |
| `*p2 = 53;` | 53 | 53 |
| `p1 = new int; *p1 = 88;` (p1 now points to a **new** int) | 88 | 53 |

The last line is the important one: after `p1 = new int`, `p1` and `p2` point to **different** ints.

⚠️ **The slide never uses `delete`.** Memory from `new` is not returned automatically. Compiled with the leak checker, slide 15's program reports `8 byte(s) leaked in 2 allocation(s)`. For short programs the OS reclaims it at exit, but in a long-running program it is a *memory leak*.

The fix — **one `delete` for each `new`**:

```cpp
int *p1 = new int(42), *p2 = p1;
*p2 = 53;
delete p1;                 // frees the int (p1 and p2 both pointed to it: delete it ONCE)
p1 = nullptr; p2 = nullptr;        // both are now dangling, so clear them
int *arr = new int[3]{1,2,3};
delete[] arr;              // arrays from new[] need delete[]
```

Verified with the leak checker: no report. (*Extra, not in slides.*)

---

## 4. Pointer arithmetic (slides 16–22)

**Rule:** `p + 1` moves to the **next element of the pointer's type**, i.e. adds `sizeof(type)` bytes, not 1 byte.

Measured on this machine (64-bit Linux):

| Pointer type | Bytes moved by `p+1` |
|---|---|
| `char*` | 1 |
| `short*` | 2 |
| `int*` | 4 |
| `long*` | **8** |

⚠️ **Slides 17–19 assume `int` = 4 and `long` = 4** (the figure shows `3000 → 3004`). That is true on Windows (Visual Studio), but on 64-bit Linux `long` is 8 bytes, so `++mylong` would go `3000 → 3008`. The safe statement: **`p++` adds `sizeof(*p)` bytes.** For an exam that copies the slide, answer 3004.

### 4.1 Arrays and pointers (link to Chapter 1)

```cpp
int arr[5] = {10,20,30,40,50};  int *q = arr;    // arr means &arr[0] here
arr[2]  ==  *(q+2)  ==  q[2]     // all 30 (verified)
&arr[4] - &arr[1]  ==  3         // subtracting pointers gives a number of ELEMENTS
```

### 4.2 Slide 21 traced

`x = &c` (say address 1000); `p = x + 2` = 1008; `q = x - 2` = 992; `a = p - q` = (1008−992)/4 = **4 elements** (verified: 4). Note `x+2` and `x-2` point outside the variable `c`; the language only guarantees pointer arithmetic *inside an array*, so this is a demo, not a technique to copy.

### 4.3 The four `*` / `++` combinations (slide 22) — verified

`int a[4] = {10,20,30,40}; int *p = a;` (each line starts from `p = a`)

| Expression | Read as | Value | Afterwards |
|---|---|---|---|
| `*p++` | `*(p++)` | **10** | p → `a[1]`, `a[0]` unchanged |
| `*++p` | `*(++p)` | **20** | p → `a[1]` |
| `++*p` | `++(*p)` | **11** | p unchanged, `a[0]` = 11 |
| `(*p)++` | | **11** (old value) | p unchanged, `a[0]` = 12 |

Memory trick: `++` next to **`p`** moves the pointer; `++` next to **`*p`** changes the value. Post-increment gives the *old* value; pre-increment gives the *new* one.

---

## 5. References (slides 23–24)

A **reference** is a second name for an existing variable: `int &refNumber = number;`

Slide 24 output (verified): `88 88 99 99 55 55` — changing either name changes the same variable.

⚠️ **"A reference is similar to a pointer" hides three differences** (all verified):

| | Pointer | Reference |
|---|---|---|
| Must be set at creation? | No (may be null) | **Yes** (`int &r;` → `declared as reference but not initialized`) |
| Can it change target? | Yes (`p = &other;`) | **No.** `ref = other;` copies *`other`'s value into the original variable* (number became 1); `&ref == &number` stayed true |
| Need `*` to use? | Yes | No, use it like the variable |

---

## Exercises on slides 25–27 — solutions

**Slide 25:** `double *ptrNum; double num; ptrNum = &num; *ptrNum = 123;` (prints `num=123`).

**Slide 26** (`a` at 0x32AB, `b` at 0xE1F2):

| Statement | Effect | Output |
|---|---|---|
| `ptr2 = ptr3 = &a; ptr1 = &b;` | ptr2, ptr3 → a; ptr1 → b | |
| `cout << *ptr2 + b` | 10 + 20 | **30** |
| `cout << *&*ptr2` | `*ptr2` = a; `&` then `*` cancel | **10** |
| `ptr3 = &b; a += *ptr3 + *ptr1;` | a = 10 + 20 + 20 | (a = 50) |
| `ptr1 = ptr2;` | ptr1 → a | |
| `cout << a` | | **50** |
| `cout << *ptr3 + *ptr1` | b + a = 20 + 50 | **70** |
| `cout << ptr1` | address of a | **0x32AB** |
| `cout << ptr3` | address of b | **0xE1F2** |

Verified on real pointers: `30 10 50 70`, `ptr1==&a`, `ptr3==&b`.

**Slide 27:** `*aPtr = 12` → a = 12; `b = 13`; prints `a = 12`, `b = 13`; `c = 25` prints `c = 25`; `aPtr = &c; a = *aPtr - 2;` → a = 25 − 2 = **23**; `(*bPtr)++` → b = **14**. Final prints: `a = 23`, `b = 14`. Verified.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | More accurate |
|---|---|---|
| 13 | `15， *p1` | Full-width comma → compile error |
| 15 | `new` used, never freed | Leaks; add `delete` |
| 17–19 | `int++` = 4 bytes, `long++` = 4 bytes | It is `sizeof(type)`; `long` is 8 on 64-bit Linux/macOS |
| 21 | `x-2`, `x+2` around a lone variable | Only valid inside arrays; works in practice |
| 23 | "A reference is similar to a pointer" | Must be initialised; cannot be re-bound |
| 11 | null is `NULL` / `0` | Prefer `nullptr` (C++11) |
| 23 | "newNew" | typo for "newName" |

## Cheat sheet

| Want | Write |
|---|---|
| pointer to int | `int *p;` (each pointer needs its own `*`) |
| address of x | `&x` |
| value p points to | `*p` |
| nothing | `nullptr` |
| next element | `p + 1` (adds `sizeof(*p)` bytes) |
| elements between | `p2 - p1` |
| nameless variable / free it | `new int` / `delete p` |
| nameless array / free it | `new int[n]` / `delete[] p` |
| alias | `int &r = x;` |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** After `int *p, q;`, what type is `q`? (a) `int*` (b) `int` (c) `int&` (d) error
**A2.** With `int a[4]={10,20,30,40}; int *p=a;` what does `*p++` evaluate to, and where is `p` afterwards? (a) 20, at a[1] (b) 10, at a[1] (c) 11, at a[0] (d) 10, at a[0]
**A3.** If `int *p = (int*)1000;` on a system where `int` is 4 bytes, what is the address `p + 3`? (a) 1003 (b) 1012 (c) 1004 (d) 1000
**A4.** Which line is invalid? `double a=10; double *n;` (a) `n = &a;` (b) `*n = a;` (c) `*n = &a;` (d) `double *m = &a;`
**A5.** Which is true of a C++ reference? (a) may be null (b) can be re-bound later (c) must be initialised when declared (d) needs `*` to read

### B. Short answer

**B1.** State the two meanings of `*` and give an example of each.
**B2.** Why must every `new` be matched with a `delete`? What does slide 15's program do wrong?
**B3.** Give three differences between a pointer and a reference.

### C. Trace

**C1.** Do slide 26 (`a`=10, `b`=20 at 0x32AB, 0xE1F2) and list all six outputs.
**C2.** Do slide 27 and give the four printed values after `aPtr = &c`.
**C3.** With `int a[4]={10,20,30,40}; int *p=a;` and each expression starting fresh from `p = a`, give the value of `++*p` and then `a[0]`; and the value of `(*p)++` and then `a[0]`.

### D. Thinking

**D1.** `int *p; *p = 5;` — explain why this is dangerous even though it may compile.
**D2.** In slide 15, after `p1 = new int;` (the second one), the first int (value 53) is still reachable. What would make it unreachable, and what is the name of that bug?

---

### Answers

**A1 → (b) `int`.** `*` binds to `p` only.
**A2 → (b).** `*p++` = `*(p++)`: value 10, pointer moves to `a[1]`. (Verified.)
**A3 → (b) 1012.** `p+3` adds 3 × 4 = 12 bytes.
**A4 → (c).** `*n = &a` stores an address into a `double`.
**A5 → (c).** A reference must be initialised, cannot be null or re-bound, and needs no `*`.

**B1.** In a declaration `int *p;` says *p is a pointer to int*. In an expression `*p = 20;` (dereference) means *the variable p points to*.

**B2.** `new` takes heap memory that is never returned automatically; without `delete` it stays reserved until the program ends (memory leak). Slide 15 allocates two ints and frees neither (the leak checker reported 8 bytes in 2 allocations).

**B3.** (i) A reference must be initialised; a pointer need not be. (ii) A pointer can be re-pointed; a reference is permanently bound (`ref = other` copies the value). (iii) A pointer needs `*` to reach the target and can be null; a reference is used like the variable and cannot be null.

**C1.** `30`, `10`, `50`, `70`, `0x32AB`, `0xE1F2`. (Steps in the table above; verified.)

**C2.** `a = 23`, `b = 14` (after earlier prints `a = 12`, `b = 13`, `c = 25`). Verified.

**C3.** `++*p` → **11**, then `a[0]` = **11**. `(*p)++` → **11** (old value), then `a[0]` = **12**. Verified.

**D1.** `p` is uninitialised, so it holds a random address; `*p = 5` writes 5 to an unknown place (undefined behaviour): a crash, or silent corruption. Initialise `p` first (`&x`, `new int`, or `nullptr` and test before use).

**D2.** If `p2` were also re-pointed or went out of scope without a `delete`, nothing would hold the address of the 53 int and it can never be freed: a **memory leak**. Fix: `delete p2;` (or `delete p1` before reassigning) at the right time.

---

## Links to other chapters

- **Ch 1:** an array name acts like a pointer to its first element; vector iterators behave like pointers.
- **Ch 5:** pass-by-address uses `*` and `&`; pass-by-reference uses the reference syntax from section 5.
- **Ch 6:** passing arrays to functions really passes a pointer.
- **Ch 9:** each recursive call has its own stack frame; `new` memory lives on the heap instead.
