# C++ Programming — Chapter 11: Program Design

> This chapter is almost all definitions (coupling and cohesion), so the risks are different: one slide puts a coupling idea under cohesion, the ordering of two cohesion levels differs from most textbooks, one code sample uses a member name that does not exist, and the "store components in separate files" idea on slide 3 is never shown. This note gives a memory aid for every level, backs the abstract ideas with small programs that were compiled and run (g++ 13), and answers the classification questions the slides leave to the lecturer.

## 0. One-sentence overview

Good design splits a program into **modules** (functions/files) that are **loosely coupled** (depend on each other as little as possible) and **highly cohesive** (each does one job).

| Section | Slides | Key idea |
|---|---|---|
| 1. Why and how to split | 2–5 | reuse, maintain, separate files |
| 2. Naming | 6 | readable names |
| 3. Coupling | 7–17, 33 | connection *between* modules |
| 4. Cohesion | 18–32 | focus *inside* a module |
| 5. Good habits | 34 | plan, pseudocode, desk check |

---

## 1. Why split a program? (slides 2–5)

The ATM example (slide 4) shows that Withdrawal, Deposit and Balance Inquiry all repeat *verify PIN, display menu, check balance, print receipt*. Write each **once**, reuse it three times: less code, one place to fix a bug.

### 1.1 How "separate files" really work (slides 3, 5: "include / import / copy") — the slides skip this

Split each component into a **header** (`.h`, the *declarations*: what exists) and a **source** file (`.cpp`, the *definitions*: how it works):

```cpp
// price.h
#ifndef PRICE_H            // include guard: skip this file if already included
#define PRICE_H
struct Item { double price; };
double calculateFinalPrice(double price, double taxRate);
#endif

// price.cpp
#include "price.h"
double calculateFinalPrice(double price, double taxRate) { return price + taxRate * price; }

// main.cpp
#include <iostream>
#include "price.h"
int main() { std::cout << "final = " << calculateFinalPrice(100.0, 0.06) << "\n"; }
```

Build: `g++ main.cpp price.cpp -o app` (or compile each `.cpp` separately then link). Verified: prints `final = 106`.

`#include` literally **copies** the header's text into the file (slide 5's word "copy" is the accurate one). Use `<…>` for library headers and `"…"` for your own.

Three things that go wrong (each verified):

| Mistake | What you see |
|---|---|
| No include guard and the header gets included twice | `error: redefinition of 'struct Item'` |
| Forgetting to compile/link `price.cpp` | `undefined reference to 'calculateFinalPrice(double, double)'` |
| Putting only the *declaration* in the header and no definition anywhere | same `undefined reference` |

## 2. Naming (slide 6)

Rules on the slide: meaningful (`student`, not `s`), pronounceable (`score`, not `xfqb`), suitable abbreviation (`stud`), avoid digits (`menu`, not `menu1`), separate words (`studName`), verbs for flags.

⚠️ The last row is a **house rule**: "approve" (good) vs "approval" (bad). Many style guides prefer names that read as a yes/no question (`isApproved`, `hasPermission`). Follow the slide in the exam; in projects follow your team's style.

---

## 3. Coupling (slides 7–17)

**Coupling = how strongly two modules depend on each other.** Goal: **loose** (few, simple connections). Tight coupling means a change in one module breaks another.

**Analogy:** two people sharing **one bank account** (tight: each spending affects the other) versus one **mailing the other a cheque for a stated amount** (loose: only the amount is exchanged).

### 3.1 The four levels (slide 12), best → worst

| Level | Meaning | Slide example |
|---|---|---|
| **Data** (best) | modules share data only through **parameters / return values** | `calculateFinalPrice(price, tax)` |
| **Control** | the caller passes a **code/flag that decides what the other module does** | `chooseAction(inputCode)` with a `CASE` |
| **External / common** | modules share **global variables or structures** | global `salesTax`, global `emp` struct |
| **Pathological** (worst) | one module **changes another module's data** | `calculateSalesTax` sets `amountDue` |

*(Extra, not in slides: textbooks often list finer levels such as "stamp" and "content" coupling; if your lecturer follows the slide's four, answer with those.)*

**Memory aid:** *Data → Control → Common → Pathological* = "**D**on't **C**ouple **C**arelessly, **P**lease".

### 3.2 Why globals are dangerous — a run you can reproduce

Common-coupled version: two functions communicate through the global `gSalesTax`. Verified output:

```
global version, wrong call order: 100      <- amount due ignored the tax
global version, right call order: 106
data-coupled version: 106                  <- works whatever you do, tax is passed in
```

`calculateAmountDue` silently depends on **another function having already run**. With data coupling (`amountDue(total, salesTax(total))`) the dependency is visible in the parameters and cannot be forgotten.

### 3.3 Slide 16 (global structure) has two mistakes

```cpp
typedef struct { char name[31], id[11]; double salary; } Employee;
Employee emp;                      // global
... outfile << emp.ID << emp.name << emp.salary;
```

- ⚠️ The member is `id`, the code uses `emp.ID`. C++ is case-sensitive: `error: 'struct Employee' has no member named 'ID'; did you mean 'id'?` (verified).
- ⚠️ `while (!feof(fptr))` is a classic bug: the end-of-file flag is set only *after* a read fails, so the loop body runs **one extra time**. I demonstrated the C++ equivalent `while (!in.eof())` on a file containing `10 20`: it printed `10 20 20` (the last value twice); `while (in >> x)` printed the correct `10 20`. (The `feof` version has the same problem; I did not run it.)

### 3.4 Control coupling in practice

Passing a code like `inputCode` (slide 14) makes the caller *know how the callee works*. The fix is to give each action its own function (`readEmployeeRecord()`, `printPageHeading()`, …) and let the caller call the one it wants.

---

## 4. Cohesion (slides 18–32)

**Cohesion = how well the statements *inside one module* belong together.** Goal: **strong** (one purpose).

**Analogy (slide 20 cartoon):** one person doing laundry, cooking, sweeping, feeding a baby and dusting **at the same moment** = **weak cohesion**. A cook who only cooks = **functional** cohesion.

⚠️ **Slide 21 mixes up the two ideas.** Its second bullet under "When is the cohesion strong?" is "if modules can access the same variables". That is a *coupling* idea (slide 9 calls it *tight* coupling). Cohesion is about the statements *inside one module* all serving one purpose.

**"And" test (extra):** if the honest name of a function needs "and" (`readStudentRecords_And_TotalStudentAges`, slide 28), it probably has weak cohesion.

### 4.1 Seven levels (slides 22–32), best → worst

| # | Level | What the module does | Slide |
|---|---|---|---|
| 1 | **Functional** | one single task | 23 (`calculateSalesTax`) |
| 2 | **Sequential** | several tasks in order, output of one feeds the next, **same data** | 24 (`processPurchases`) |
| 3 | **Communicational** | several tasks, **same data**, order not important | 25 (validating one record) |
| 4 | **Temporal** | tasks that just happen **at the same time** (init, cleanup) | 26–27 (`initialization`) |
| 5 | **Procedural** | tasks in a **fixed order**, different data | 28 |
| 6 | **Logical** | tasks of a similar kind, **one chosen by a code** | 29 (`readAllFiles(code)`) |
| 7 | **Coincidental** | no relationship at all | 30 (`fileProcessing`) |

**Memory aid:** *"**F**or **S**ure **C**ohesive **T**eams **P**lan **L**ogically **C**arefully"*: (F)unctional, (S)equential, (C)ommunicational, (T)emporal, (P)rocedural, (L)ogical, (C)oincidental.

### 4.2 The decision table on slide 31 (this is how to classify)

```
Does the module perform ONE task?           yes -> FUNCTIONAL
  no -> Is the module tied together by DATA?
          yes -> sequence important? yes -> SEQUENTIAL    no -> COMMUNICATIONAL
        Is it tied together by LOGIC CONTROL (a code/decision)?
          yes -> sequence important? yes -> PROCEDURAL    no -> LOGICAL
        Neither data nor logic:
          related by TIME?          yes -> TEMPORAL       no -> COINCIDENTAL
```

### 4.3 ⚠️ Ordering note

Slides 22 and 32 rank **temporal above procedural**. Many textbooks and reference pages list them the other way round (from worst to best: coincidental, logical, temporal, procedural, communicational, sequential, functional), and at least one software-engineering text notes the levels "do not form a linear scale". *(This comes from a web check of common references, not from your slides.)* For the exam follow **your lecturer's order** (functional, sequential, communicational, temporal, procedural, logical, coincidental); when both appear in a question, say which order you use.

### 4.4 Refactoring example (verified)

The slide-24 function does three jobs. Split it:

```cpp
// before: sum + tax + total in one function (sequential cohesion)
double processPurchases(const vector<double>& p, double taxPercent) {
    double total = 0; for (double x : p) total += x;
    double tax = total * taxPercent;
    return total + tax;
}
// after: one job each (functional cohesion), connected by parameters (data coupling)
double sumPurchases(const vector<double>& p);
double salesTax(double total, double taxPercent);
double amountDue(double total, double tax);
```

For purchases `{10.0, 20.5, 5.5}` at 6%, before and after both give **38.16**. Same behaviour, but each piece can now be reused and tested alone.

**Coupling and cohesion move together:** strong cohesion usually gives loose coupling, and the reverse.

---

## 5. Good habits (slide 34)

1. **Plan before coding** with flowcharts or pseudocode.
2. **Desk check** = walk through your pseudocode by hand with sample values *before* writing code. Example for `calculateFinalPrice(price, tax)`: `(100, 0.06)` → 100 + 0.06×100 = **106** (matches the run); `(200, 0.1)` → **220**.
3. Design with **high cohesion and loose coupling**.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Better understanding |
|---|---|---|
| 21 | strong cohesion "if modules can access the same variables" | that is tight coupling; cohesion is *inside* one module |
| 22, 32 | temporal above procedural | many references reverse these two |
| 16 | `emp.ID` with member `id` | case mismatch; compile error |
| 16 | `while(!feof(fptr))` | reads the last record twice |
| 6 | flags should be verbs | house rule; `isApproved` style is common |
| 5 | "Include, Import, copy" | in C++ `#include` copies the text; headers + include guards |
| 19 | cohesion = "independence" | independence is closer to *coupling*; cohesion = single purpose |

**Exam strategy:** use the slide's four coupling levels and seven cohesion levels; classify with the slide-31 table.

## Cheat sheet

| Coupling (loose → tight) | Sign |
|---|---|
| Data | parameters/return values only |
| Control | passes a code that selects behaviour |
| External / common | shared global variable or struct |
| Pathological | modifies another module's data |

| Cohesion (strong → weak) | Sign |
|---|---|
| Functional | one task |
| Sequential | tasks in order, same data |
| Communicational | tasks on the same data |
| Temporal | happen at same time |
| Procedural | fixed order, different data |
| Logical | code picks one of several tasks |
| Coincidental | unrelated |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** A function `initialization()` that zeroes counters, opens two files, prints a title and reads the date has (a) functional (b) temporal (c) sequential (d) logical cohesion
**A2.** `double updatePrice(double price, double discount)` called with its inputs as parameters is an example of (a) data coupling (b) control coupling (c) common coupling (d) pathological coupling
**A3.** Two functions both read and write the global `salesTax`: (a) data (b) control (c) common (d) none
**A4.** The strongest cohesion is (a) coincidental (b) logical (c) functional (d) temporal
**A5.** `readAllFiles(fileCode)` uses a `CASE` on `fileCode` to read one of three unrelated files. Its cohesion is (a) logical (b) sequential (c) functional (d) temporal

### B. Short answer

**B1.** Define coupling and cohesion and say which you want high/low.
**B2.** Explain, with the 100 vs 106 example, why a global variable is a form of tight coupling.
**B3.** What are the header and the source file for, and what does the include guard prevent?

### C. Classification / calculation

**C1.** Classify the cohesion of: (i) `calculateSalesTax(price)`; (ii) a function that sums purchases, then computes tax, then the amount due on the same data; (iii) a function that prints an error message, resets a page counter and opens a file (no relation); (iv) `initialization()` as in A1.
**C2.** Desk-check `calculateFinalPrice(price, taxRate)` = `price + taxRate * price` for `(100, 0.06)` and `(200, 0.10)`.
**C3.** Put these in order from loosest to tightest coupling: common, data, pathological, control.

### D. Thinking

**D1.** Why is a function named `readStudentRecords_And_TotalStudentAges` a design smell, and how would you split it?
**D2.** Why do the two "wrong call order / right call order" outputs matter to a team of several programmers?

---

### Answers

**A1 → (b) temporal.** Tasks only related by *when* they run (setup time). **A2 → (a).** **A3 → (c).** **A4 → (c).** **A5 → (a) logical** (a code selects among unrelated tasks; the `fileCode` is also control coupling).

**B1.** Coupling = strength of connection *between* modules (want **low/loose**). Cohesion = how closely the statements *within* a module belong together (want **high/strong**).

**B2.** The function `calculateAmountDue` works only if `calculateSalesTax` already wrote the global. Called first it printed **100**, called second **106** (verified). Any module can change the global at any time, so the modules are secretly linked; with parameters the link is visible and safe.

**B3.** The header declares *what* exists (prototypes, structs); the source defines *how*. Other files `#include` the header. The include guard (`#ifndef … #define … #endif`) stops the header's contents being read twice in one compilation, which otherwise gives `redefinition of 'struct Item'` (verified).

**C1.** (i) **Functional**. (ii) **Sequential** (ordered steps, same data). (iii) **Coincidental**. (iv) **Temporal**.

**C2.** `(100, 0.06)` → 100 + 6 = **106** (verified). `(200, 0.10)` → 200 + 20 = **220**.

**C3.** **data, control, common, pathological.**

**D1.** The "And" in the name shows it does two jobs (reading and totalling), which the slide calls procedural cohesion. Split into `readStudentRecords()` returning the records, and `totalAges(records)`; the second takes the first's output as a parameter (data coupling). The same idea was verified in section 4.4.

**D2.** Because bugs would depend on call order and on who touched the global last; with several people editing, that is nearly impossible to track. Parameter-based (data-coupled) modules can be tested and changed independently.

---

## Links to other chapters

- **Ch 5:** by-value parameters and return values give **data coupling**; globals (slide 6) give common coupling.
- **Ch 6:** scope and storage class: globals are visible everywhere, which is why they couple modules.
- **Ch 2 / 3:** `regex_match` validation function = a nicely cohesive module; the global `Employee emp` is the slide-16 example.
- **Ch 9:** recursion is a function with one clear purpose and shows good functional cohesion.
