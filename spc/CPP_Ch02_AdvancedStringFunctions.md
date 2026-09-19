# C++ Programming — Chapter 2: Advanced String Functions

> The slides list eight tools but show almost no *why* and several outputs that the code does not actually produce (the `transform` example, `regex_replace`, and both `format` examples). Two of the slide code lines don't even compile (`{:.2f }`). This note explains each tool, corrects the slide outputs, and solves the exercise on slide 25. Everything was compiled and run with g++ 13 (`-std=c++20`).

## 0. One-sentence overview

Chapter 2 gives you eight ways to **convert, search, split, reshape, pattern-match and neatly print** strings.

| # | Tool | Header | Slides | Job |
|---|---|---|---|---|
| 1 | `to_string`, `stoi/stod/stof` | `<string>` | 3 | number ⇄ string |
| 2 | `find_first_of` family | `<string>` | 4 | find *any* char from a set |
| 3 | `stringstream` | `<sstream>` | 5–6 | split / convert using stream syntax |
| 4 | `transform` | `<algorithm>` | 7–9 | apply a function to every character |
| 5 | `regex` | `<regex>` | 10–16 | pattern matching |
| 6 | `format` | `<format>` | 17–24 | build formatted text (C++20) |

(The slide numbers them 1–8 because it counts `find_first_of` and `find_first_not_of` separately.)

---

## 1. Converting between numbers and strings (slide 3)

```cpp
string s = to_string(123);     // "123"
int    n = stoi("123");        // 123        stod → double, stof → float
```

Things the slide does not tell you (all verified):

- `stoi` reads digits **from the start and stops at the first non-digit**: `stoi("12abc")` gives **12**, no error.
- If it cannot read *any* number, `stoi("abc")` **throws `invalid_argument`**. Wrap user input in `try { … } catch (const invalid_argument&) { … }`.
- `to_string(123) + "!"` works because the result is a real `string`.

## 2. `find_first_of` and friends (slide 4)

`find("lo")` looks for the **exact substring** "lo". `find_first_of("lo")` looks for **any one character** that is `'l'` or `'o'`.

`"Hello world"`, index: `H0 e1 l2 l3 o4 ␣5 w6 o7 r8 l9 d10`

| Call | Meaning | Result |
|---|---|---|
| `find_first_of("aeiou")` | first vowel | **1** (`e`) |
| `find_last_of("aeiou")` | last vowel | 7 (`o` in *world*) |
| `find_first_not_of("Hel")` | first char **not** in {H,e,l} | 4 (`o`) |
| `find_first_of("xyz")` | nothing matches | `string::npos` |

⚠️ **When nothing is found** the functions return `string::npos` (a huge number), **not** −1 or 0. Always test `if (pos != string::npos)`. The slide stores the result in `int pos`, which works for the demo but is not the proper type (`size_t`).

**Analogy:** `find_first_of` is "which of these keys opens the first lock?", not "find this sentence".

## 3. `stringstream` (slides 5–6)

A `stringstream` lets you treat a string **like `cin`/`cout`**.

**Reading (splitting):** `>>` skips spaces and reads one value of the variable's type.

```cpp
string text = "10 25.78 Hello";
int n; float m; string word;
stringstream ss(text);
ss >> n >> m >> word;          // n=10  m=25.78  word="Hello"
```

**Writing (building):** `ss << 45;` then `ss.str()` returns `"45"`. (The slide's comment "read 45 into string" means "write into".)

**Splitting at a comma** — `>>` only splits at whitespace, so add `getline`:

```cpp
stringstream sp("apple,banana,cherry"); string tok;
while (getline(sp, tok, ',')) cout << "[" << tok << "]";   // [apple][banana][cherry]
```

⚠️ **Common confusion — a failed read.** If the text does not match the type, the stream enters a *fail* state and **all later reads do nothing**. Verified with `"10 abc Hello"`: `n = 10`, `f = 0`, and `word` is left untouched.

## 4. `transform` (slides 7–9)

Signature: `transform(begin, end, destination, function)` — for every character in `[begin, end)`, apply `function` and write the result starting at `destination`.

```cpp
string text1 = "Hello world!";
transform(text1.begin(), text1.end(), text1.begin(), ::toupper);        // HELLO WORLD!
transform(text1.begin()+6, text1.end(), text1.begin()+6, ::tolower);   // HELLO world!
```

Both lines (verified) work because the destination is the **same string**, so there is room. `::toupper` means "the global `toupper` function".

Iterator arithmetic recap: `begin()+6` = start at index 6.

⚠️ **Slide 9 is wrong.** It does

```cpp
string text1 = "Hello world!", text2 = " ";          // text2 has length 1
transform(text1.begin()+1, text1.end(), text2.begin(), ::tolower);
cout << text2;                                        // slide claims: ello
```

`transform` **writes into `text2` but never makes it longer**; it just runs off the end of a 1-character string. That is **undefined behaviour**. When I ran it, no crash happened, but the output was `e` (size still 1), **not `ello`** as the slide claims. (Even the "correct" text would be `ello world!`, since the range runs to `end()`.)

Two correct fixes (both verified to give `ello world!`):

```cpp
string a(text1.size()-1, ' ');                                        // 1) size the destination first
transform(text1.begin()+1, text1.end(), a.begin(), ::tolower);

string b;                                                             // 2) let it grow (needs <iterator>)
transform(text1.begin()+1, text1.end(), back_inserter(b), ::tolower);
```

**Rule:** the destination must already have room for every result, or use `back_inserter`.

## 5. `regex` (slides 10–16)

A **regular expression** is a mini-language that describes a *pattern* of text ("some digits", "letters then digits").

**Reading the pattern table (slide 12).** In a C++ string literal the backslash itself must be written `\\`, so the regex `\d` is written `"\\d"`. The slide's `\\d` column shows the C++ spelling.

| Pattern | Meaning |
|---|---|
| `\\d` | one digit |
| `\\w` | letter, digit or `_` |
| `.` | any character |
| `*` | 0 or more of the previous thing |
| `+` | 1 or more |
| `^` / `$` | start / end of the string |
| `( )` | capture group |
| `[a-z]` | any one lowercase letter |

### The three functions (slides 11, 13–15) — differences that decide exam answers

| Function | Question it answers | `"abc123xyz"` with `[a-z]+\\d+` |
|---|---|---|
| `regex_match` | does the **whole** string fit? | **false** (`xyz` is left over) |
| `regex_search` | does **any part** fit? | **true** |
| `regex_replace` | replace every matching part | |

(Verified: match = 0, search = 1.)

### Worked examples (all verified)

| Code | Result |
|---|---|
| `regex_search("My unit number is A-1-25", "\\d+")` | `Number found!` |
| `regex_match("abc123", "[a-z]+\\d+")` | `Full match!` |
| `regex_replace("A-1-25", regex("\\d+"), "#")` | `A-#-#` |

### Capture groups (slide 16)

```cpp
string text = "David is 18 years old";
regex twoPatterns("(\\w+) is (\\d+) years old");
smatch match;
if (regex_search(text, match, twoPatterns)) {
    cout << match[0];   // whole match:  David is 18 years old
    cout << match[1];   // 1st ( ):      David
    cout << match[2];   // 2nd ( ):      18
}
```

Each `( )` becomes `match[1]`, `match[2]`, …; `match[0]` is the whole match. `match.size()` is 3 here. To use the age as a number: `stoi(match[2])`.

⚠️ **Slide 15 output is not what the code prints.** The code prints `"Password entered"`, then `result`, then `"is correct!"` with **no spaces**. Real output:

```
Password entered***is correct!
```

(The slide shows `Password entered *** is correct!`.) The example is also odd logic: it replaces the *password itself* with `***` to hide it.

⚠️ **Validation trap:** `regex_search` without `^…$` accepts junk around a good value. With `\\d{3}-\\d{7}`, the text `"call 012-3456789 now"` gives search = **true** but match = **false** (and `^\\d{3}-\\d{7}$` with search = false). To validate a whole input, use `regex_match` or add anchors.

## 6. `format` (slides 17–24)

`format` (C++20, `#include <format>`) builds a string from a template where each `{}` is a slot, similar to `printf` but type-safe.

**Setup (slides 18–20):** the slides show Visual Studio → Project → Properties → set the C++ language standard to **ISO C++20**. With g++ use `-std=c++20`.

### Format specs — `{:` fill/align, width, precision, type `}`

| Spec | Meaning | Example (`68` / `3.14159`) | Result |
|---|---|---|---|
| `{}` | default | `format("{}", 68)` | `68` |
| `{:05}` | width 5, pad with zeros | | `00068` |
| `{:>6}` | width 6, right-aligned | | `    68` |
| `{:<6}` | width 6, left-aligned | | `68    ` |
| `{:^6}` | centred | | `  68  ` |
| `{:.2f}` | 2 decimals | `3.14159` | `3.14` |
| `{:8.3f}` | width 8, 3 decimals | `3.14159` | `   3.142` |
| `{:x}` | hexadecimal | `255` | `ff` |
| `{1} … {0}` | pick arguments by position | | |

⚠️ **Slide errors in this section:**

1. **Slide 22:** `format("{} x {:.2f } = {:.2f }", …)` **does not compile.** The space before `}` is part of the spec and is illegal: `error: call to non-'constexpr' function … __failed_to_parse_format_spec`. Write `{:.2f}`. Also the slide's expected output says `5 * 3.14` but the format text has `x`. Real output: `5 x 3.14 = 15.71`.
2. **Slide 21:** the output comment says `Hello Lionel ! Lionel is 20 years old`. The code has `"Hello, {} !"` and prints the two messages with no separator, so the real output is `Hello, Lionel !Lionel is 20 years old`.
3. **Slide 23:** the comments show `Zero padded : 00068` (extra space) while the code prints `Zero padded: 00068`, and the alignment padding is lost in the slide's plain text. Real output (brackets added by me): `[    68]` and `[68    ]`.

---

## Exercise (slide 25) — worked solution

Slide 26 is **blank** in the file you have (an empty exercise slide).

Task: two vectors (items, radius), compute the circle area (π = 3.14159) and print a table.

```cpp
#include <iostream>
#include <format>
#include <string>
#include <vector>
using namespace std;
int main(){
    const double PI = 3.14159;
    vector<string> items  = {"coin", "ring", "wheel"};
    vector<double> radius = {0.5, 0.7, 21.6};
    cout << format("{:<8}{:>8}{:>14}\n", "Items", "Radius", "Area");
    for (size_t i = 0; i < items.size(); i++) {
        double area = PI * radius[i] * radius[i];
        string areaText = format("{:.2f}cm^2", area);          // build the text first...
        cout << format("{:<8}{:>8}{:>14}\n", items[i], radius[i], areaText);   // ...then align it
    }
}
```

Output (matches the slide's 0.79 / 1.54 / 1465.74):

```
Items     Radius          Area
coin         0.5      0.79cm^2
ring         0.7      1.54cm^2
wheel       21.6   1465.74cm^2
```

Hand-check for wheel: 21.6² = 466.56; × 3.14159 = 1465.74.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | What really happens |
|---|---|---|
| 9 | `text2 = " "` receives the result; prints `ello` | Writes past the end of a 1-char string (undefined behaviour); printed `e` for me |
| 15 | Output `Password entered *** is correct!` | No spaces printed: `Password entered***is correct!` |
| 21 | Output `Hello Lionel ! Lionel is 20 years old` | `Hello, Lionel !Lionel is 20 years old` |
| 22 | `{:.2f }` and output `5 * 3.14 …` | Space makes it a compile error; text uses `x` |
| 4 | `int pos = find_first_of(...)` | Return type is `size_t`; "not found" is `string::npos` |
| 26 | exercise slide | Blank in this file |

**Exam strategy:** if a question quotes these outputs, answer as the slide does; write your own code the correct way.

## Cheat sheet

| Need | Use |
|---|---|
| number → string / string → number | `to_string`, `stoi`, `stod`, `stof` |
| first/last char from a set | `find_first_of`, `find_last_of` (`npos` if none) |
| first/last char **not** in a set | `find_first_not_of`, `find_last_not_of` |
| split by whitespace | `stringstream ss(text); ss >> a >> b;` |
| split by other separator | `getline(ss, tok, ',')` |
| change every char | `transform(b, e, dest, ::toupper)` (dest needs room) |
| whole string matches | `regex_match` |
| pattern appears somewhere | `regex_search` |
| replace by pattern | `regex_replace(s, re, "new")` |
| capture parts | `( )` + `smatch`; `match[1]`… |
| formatted text | `format("{:>8.2f}", x)` — no spaces inside `{ }` |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** `string s = "Hello world"; s.find_first_of("aeiou")` returns
(a) 1 (b) 4 (c) 2 (d) `npos`

**A2.** `stoi("12abc")` gives
(a) 12 (b) 0 (c) throws `invalid_argument` (d) 12.0

**A3.** Which function requires the **entire** string to match the pattern?
(a) `regex_search` (b) `regex_match` (c) `regex_replace` (d) `smatch`

**A4.** `format("{:05}", 68)` gives
(a) `68000` (b) `00068` (c) `   68` (d) `68`

**A5.** `regex_search("abc123xyz", regex("[a-z]+\\d+"))` and `regex_match` on the same string give
(a) true, true (b) false, false (c) true, false (d) false, true

### B. Short answer

**B1.** Slide 9 copies `text1.begin()+1 … end()` into `text2` where `text2 = " "`. Explain what is wrong and give two fixes.
**B2.** Explain how to split `"apple,banana,cherry"` into three strings using `stringstream`.
**B3.** Why does `format("{:.2f }", x)` fail, and when is the error reported?

### C. Calculation / trace

**C1.** `string s = "Hello, World";` Give `s.find_first_of("lo")`, `s.find_last_of("lo")`, `s.find_first_not_of("Hel")`.
**C2.** `string t = "Order 45: 3 items at RM12.50"; regex r("Order (\\d+): (\\d+) items");` After a successful `regex_search(t, m, r)` give `m[0]`, `m[1]`, `m[2]`. Then give `regex_replace("2024-09-19", regex("\\d+"), "N")`.
**C3.** What does `format("{:>8.2f}|{:<6}|{:06}", 3.14159, 42, 42)` produce? (Mark each space as `␣`.)

### D. Thinking

**D1.** A form field must contain a Malaysian-style phone number `012-3456789`. Why is `regex_search(input, regex("\\d{3}-\\d{7}"))` a poor validator, and what should you use?
**D2.** `stringstream ss("10 abc Hello"); int n; float f; string w; ss >> n >> f >> w;` What are `n`, `f`, `w`, and what should the program do about it?

---

### Answers

**A1 → (a) 1.** The first vowel is `e` at index 1.

**A2 → (a) 12.** It stops at the first non-digit and does not throw. It throws only if no digits are found at the start.

**A3 → (b).** `regex_match` needs the whole string; `regex_search` finds a match anywhere.

**A4 → (b) `00068`.** `0` = pad with zeros, `5` = total width.

**A5 → (c).** The pattern matches the part `abc123` (search = true) but `xyz` is left over (match = false). Verified.

**B1.** `transform` writes into `text2` but does not enlarge it; `text2` has size 1, so writing 11 characters goes past its end — undefined behaviour (it printed `e`, not `ello`). Fixes: (1) `string text2(text1.size()-1, ' ');` so it already has room; (2) `transform(..., back_inserter(text2), ::tolower)` after starting from an empty string.

**B2.** Put the text in the stream and call `getline` with a delimiter in a loop: `stringstream sp("apple,banana,cherry"); string tok; while (getline(sp, tok, ',')) { … }`. `>>` alone cannot do it because it only splits on whitespace.

**B3.** A space is not allowed inside the replacement field spec (`{:.2f }`), so the format string is invalid. In C++20 with a string literal it is caught at **compile time** (`__failed_to_parse_format_spec`).

**C1.** Indexes `H0 e1 l2 l3 o4 ,5 ␣6 W7 o8 r9 l10 d11`. `find_first_of("lo")` = **2**; `find_last_of("lo")` = **10**; `find_first_not_of("Hel")` = **4** (`o` is not one of H, e, l). Verified.

**C2.** `m[0]` = `Order 45: 3 items`; `m[1]` = `45`; `m[2]` = `3`. `regex_replace` → `N-N-N` (each run of digits becomes `N`). Verified.

**C3.** `{:>8.2f}` → `␣␣␣␣3.14` (width 8); `{:<6}` → `42␣␣␣␣`; `{:06}` → `000042`. Full output: `␣␣␣␣3.14|42␣␣␣␣|000042`. Verified.

**D1.** Because `regex_search` accepts the number anywhere in the input: `"call 012-3456789 now"` gives search = true (verified), match = false. Use `regex_match`, or anchor the pattern with `^…$`.

**D2.** `n` = 10, `f` = 0, `w` is unchanged (still whatever it was before). Reading `abc` into a `float` fails, the stream enters the fail state, and later reads are skipped (`ss.fail()` is true). The program should check `if (ss >> n >> f >> w)` (or `ss.fail()`) and report invalid input. Verified.

---

## Links to other chapters

- **Ch 1:** `vector` is used in the slide-25 exercise; iterators (`begin()+1`) are the same idea as in Ch 1.
- **Ch 3:** structs often hold `string` members; `strcpy` (C-style) vs `string =` is discussed there.
- **Ch 11:** good function design — a validation function using `regex_match` is a nicely *cohesive* module.
