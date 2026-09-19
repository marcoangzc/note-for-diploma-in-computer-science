# C++ Programming — Chapter 9: Recursion

> The slides are short and mostly right, but they contradict themselves (is recursion "easier to understand" or iteration?), say each recursive call has "its own code" (it doesn't), print a factorial trace with `+` instead of `*`, and praise Fibonacci as a "natural" recursion without mentioning it makes thousands of repeated calls. This note explains the call stack step by step and measures the costs. Everything was compiled and run with g++ 13.

## 0. One-sentence overview

**Recursion** solves a problem by calling the same function on a *smaller* version of the problem until it reaches a case simple enough to answer directly (the **base case**).

| Section | Slides | Key idea |
|---|---|---|
| 1. Recursion vs iteration | 3–5, 18 | trade-offs |
| 2. Rules & design | 6–10 | base case, general case, progress |
| 3. Activation frames | 11 | what each call stores |
| 4. Sum, factorial, Fibonacci | 12–17 | traces |

---

## 1. The idea in one picture

**Analogy:** Russian nesting dolls. To count the dolls, open one and ask "how many are inside?" (a smaller version of the same question). The smallest doll (no dolls inside) is the **base case**; then the answers come back out one by one.

```
Sum(3)  needs  Sum(2)  needs  Sum(1)
                              Sum(1) = 1          <- base case, no more calls
               Sum(2) = 2 + 1 = 3
Sum(3) = 3 + 3 = 6
```

## 2. The three rules (slides 6–10)

1. **Base case:** at least one input answered *without* recursing (`n == 1` → 1).
2. **General case:** each call reduces the problem and moves **toward** the base case (`Sum(n-1)`).
3. **Finite:** every valid input must eventually reach a base case.

Design order (slide 10): understand the problem → find the base case(s) → write the general case in terms of a smaller version.

⚠️ **What happens if rule 3 is broken:** `Sum(0)` never reaches `n == 1`, so the calls go on until the program runs out of stack memory and crashes. Verified: `Sum(0)` → *Segmentation fault* (exit code 139). Safer base case: `if (n <= 1) return 1;` (then `SumSafe(0)` and `SumSafe(-3)` give 1; verified).

## 3. Activation frames (slide 9 vs slide 11)

⚠️ **Slide 9 says "every call … has its own code".** That is **wrong**, and slide 11 shows why. There is **one copy of the code**; each call gets its own **activation frame** (a block on the call *stack*, "created on the whenever" is missing the word *stack*) holding:

| In the frame | Meaning |
|---|---|
| Return address | where to continue in the caller |
| Parameters | this call's `n` |
| Local variables | this call's own locals |
| Saved state | the caller's registers, stack pointer |

So "infinitely many copies of itself" is only a mental picture: the *code* is shared, the *data* is per call.

Frames are stacked like plates; the newest is on top and is removed first when it returns. Live trace of `Sum(3)` (printed by an instrumented version, verified):

```
Sum(3) calls Sum(2)
  Sum(2) calls Sum(1)
    Sum(1) returns 1
  Sum(2) returns 3
Sum(3) returns 6
```

Stack at the deepest point: `[Sum(3): n=3] [Sum(2): n=2] [Sum(1): n=1]` ← top.

**Stack size is limited.** At `-O0` (no optimisation), `Sum(1000)` and `Sum(100000)` worked but `Sum(1000000)` crashed with *Segmentation fault* (stack overflow). "Too deep" is a real limit of recursion.

## 4. The three examples

### 4.1 Sum 1..N (slides 12–13)

```cpp
int Sum(int n) { if (n == 1) return 1; else return n + Sum(n - 1); }
```

| Call | Waiting to compute | Returns |
|---|---|---|
| `Sum(3)` | `3 + Sum(2)` | 6 |
| `Sum(2)` | `2 + Sum(1)` | 3 |
| `Sum(1)` | base case | 1 |

`Sum(10)` = 55 (verified). ⚠️ For large `n` the sum overflows `int` before the stack does: `Sum(100000)` printed `705082704` instead of 5000050000.

### 4.2 Factorial (slides 14–15)

`n! = n × (n−1) × … × 1`, with `0! = 1` as the base case.

⚠️ **Slide 15's trace uses `+` where the code has `*`.** It shows `return (3 + Factorial(3-1))`. With `+`, `Factorial(3)` would be **7** (verified: `3 + (2 + (1 + 1))`), but the slide's result column (1, 2, 6) is correct for `*`. Read those boxes as `3 *`, `2 *`, and note the trace skips the last call `Factorial(0)` = 1.

| Call | Waiting | Returns |
|---|---|---|
| `Factorial(3)` | `3 * Factorial(2)` | 6 |
| `Factorial(2)` | `2 * Factorial(1)` | 2 |
| `Factorial(1)` | `1 * Factorial(0)` | 1 |
| `Factorial(0)` | base | 1 |

⚠️ **Overflow:** with `int`, `Factorial(12)` = 479001600 is fine but `Factorial(13)` gives **1932053504** (wrong; the true value is 6227020800). With `long long`, the largest that fits is `20! = 2432902008176640000` (verified).

### 4.3 Fibonacci (slides 16–17)

Each number is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55 (verified for n = 0…10).

`Fibonacci(3) = Fibonacci(2) + Fibonacci(1) = (Fibonacci(1) + Fibonacci(0)) + 1 = (1 + 0) + 1 = 2`. Slide 17 draws exactly this tree.

⚠️ **The slides never mention the cost.** The same subproblems are recomputed again and again. Counted calls (verified):

| n | fib(n) | number of calls |
|---|---|---|
| 3 | 2 | 5 |
| 5 | 5 | 15 |
| 10 | 55 | 177 |
| 20 | 6765 | 21 891 |
| 30 | 832 040 | 2 692 537 |

Roughly **×1.6 per step**, so it grows exponentially. Timing `fib(40)` (unoptimised): recursive **909 ms**, a simple loop **under a microsecond** for the same answer 102334155.

---

## 5. Recursion vs iteration (slides 3–4, 18)

⚠️ **Slide 4 contradicts itself.** Bullet 1: "an iterative solution is more obvious and easier to understand". Bullet 4: "coding for recursion is shorter, simpler and easier to understand". Both cannot be a general rule; **it depends on the problem**:

| Problem | Easier way |
|---|---|
| Sum 1..N, factorial | a loop is just as easy (and safer) |
| Fibonacci | loop is far faster; recursion only reads naturally |
| Divide-and-conquer (sorting, searching), trees | recursion is usually much clearer |

Slide 18's summary holds: recursion is often cleaner but uses more memory (one frame per call) and can be slower; iteration is faster and lighter but can be less readable. (*Extra:* some compilers turn simple recursion into a loop when optimising, so the cost isn't always there.)

## 6. More recursive functions to practise (extra, all verified)

```cpp
int power(int b, int e)   { if (e == 0) return 1; return b * power(b, e - 1); }   // power(2,10) = 1024
int gcd(int a, int b)     { if (b == 0) return a; return gcd(b, a % b); }          // gcd(48,18) = 6
int digitSum(int n)       { if (n == 0) return 0; return n % 10 + digitSum(n / 10); }   // 1234 -> 10
```

Pattern: **base case first, then a call on a smaller input**.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Truth |
|---|---|---|
| 9 | each call has "its own code" | one copy of code; each call has its own frame (data) |
| 4 | iteration "easier to understand" *and* recursion "easier to understand" | contradictory; depends on the problem |
| 15 | `3 + Factorial(3-1)` | should be `3 *` (results 1, 2, 6 are right) |
| 11 | "created on the whenever" | "on the **stack** whenever" |
| 12, 14 | no guard for bad input | `Sum(0)` crashes; negative factorial never ends |
| 16–17 | Fibonacci as a good example | correct but exponentially slow |
| 18 | "Iteraction" | typo: iteration |

**Exam strategy:** copy the slide's summary (recursion elegant/memory-heavy, iteration efficient) but be able to say why.

## Cheat sheet

| Term | Meaning |
|---|---|
| base case | answered directly, stops recursion |
| general case | calls itself on a smaller input |
| activation frame | per-call record: return address, parameters, locals, saved state |
| stack overflow | too many frames (e.g. missing base case) |
| `Sum(n)` | `n + Sum(n-1)`, base `n == 1` |
| `Factorial(n)` | `n * Factorial(n-1)`, base `n == 0` |
| `Fibonacci(n)` | `F(n-1) + F(n-2)`, bases `0`, `1` |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** Which is essential to every recursive function? (a) a loop (b) a base case (c) a global variable (d) two parameters
**A2.** `Sum(5)` with the slide's function returns (a) 5 (b) 10 (c) 15 (d) 120
**A3.** `Fibonacci(6)` (0, 1, 1, 2, …) returns (a) 5 (b) 8 (c) 13 (d) 6
**A4.** What happens when you call the slide's `Sum(0)`? (a) returns 0 (b) returns 1 (c) infinite recursion → crash (d) compile error
**A5.** Each recursive call has its own (a) copy of the code (b) parameters and local variables (c) global variables (d) source file

### B. Short answer

**B1.** Explain the contradiction on slide 4 and give a fair rule of thumb.
**B2.** Why is the recursive Fibonacci slow?
**B3.** List what an activation frame stores.

### C. Calculation / trace

**C1.** Trace `Factorial(4)`: list each call's waiting expression and the value it returns.
**C2.** How many calls are made (including the first) by the slide's `Fibonacci(5)`?
**C3.** Compute `power(2,10)`, `gcd(48,18)`, `digitSum(1234)`.

### D. Thinking

**D1.** For which of Sum, Factorial and Fibonacci is a loop clearly better, and why?
**D2.** Rewrite `Sum` so it never crashes for `n <= 0`.

---

### Answers

**A1 → (b).** **A2 → (c) 15** (5+4+3+2+1). **A3 → (b) 8** (0,1,1,2,3,5,8). **A4 → (c).** (Verified: segfault.) **A5 → (b).**

**B1.** Bullet 1 says iteration is easier to understand, bullet 4 says recursion is. Neither is always true: recursion is clearer for inherently recursive problems (trees, divide-and-conquer); loops are clearer for simple repetition like summing.

**B2.** It solves the same smaller problems repeatedly (fib(3) inside fib(5) and fib(4)…), so the number of calls grows exponentially: 15 calls for n=5, 2 692 537 calls for n=30. Fib(40) took 909 ms recursively vs. essentially nothing with a loop (verified).

**B3.** Return address, parameters (arguments), local variables, saved state (previous stack pointer, registers).

**C1.** `Factorial(4)` waits for `4*Factorial(3)`; `Factorial(3)` waits for `3*Factorial(2)`; `Factorial(2)` waits for `2*Factorial(1)`; `Factorial(1)` waits for `1*Factorial(0)`; `Factorial(0)` returns 1. Returns come back as 1 → 1 → 2 → 6 → **24**. Verified 24.

**C2.** **15** calls (verified). By the recurrence calls(n) = calls(n−1) + calls(n−2) + 1: calls(0)=calls(1)=1, calls(2)=3, calls(3)=5, calls(4)=9, calls(5)=15.

**C3.** **1024**, **6**, **10**. (Verified.)

**D1.** Fibonacci (repeated work, exponential calls). Sum and factorial are also better as loops in practice (no stack limit), but the gain is small; Fibonacci's cost difference is dramatic.

**D2.** Change the base case: `int Sum(int n) { if (n <= 1) return 1; return n + Sum(n - 1); }`. Verified `SumSafe(0)` = 1 and `SumSafe(-3)` = 1. (If you want `Sum(0)` to be 0, add `if (n <= 0) return 0;`.)

---

## Links to other chapters

- **Ch 5–6:** parameters and local (automatic) variables are what a frame stores.
- **Ch 4:** `new` memory lives on the heap, not in frames.
- **Ch 1 / later courses:** sorting and searching (mentioned on slide 4) are typical recursive algorithms.
