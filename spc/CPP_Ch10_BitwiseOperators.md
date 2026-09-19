# C++ Programming — Chapter 10: Bitwise Operators

> The slides give the truth tables (all correct) but leave both exercises unanswered, show bit patterns for "2" and "5" that are not the binary of 2 and 5, label the right-shift arrow "inserted on right" (it is the left), draw right shifts that only work for unsigned numbers, and never mention that C++ silently widens small types, which changes the answer to exercise 2. This note fixes those, gives you the standard flag-setting recipes, and solves everything. All results were computed with g++ 13 (`<bitset>`, `<cstdint>`).

## 0. One-sentence overview

Bitwise operators treat an integer as a **row of individual bits** (0/1) instead of one number, so you can switch single bits on/off, shift them, and combine them.

| Section | Slides | Key idea |
|---|---|---|
| 1. Bits and fixed sizes | 3–4 | bit rows, `int8_t`… |
| 2. `~` NOT | 5–6 | flip every bit |
| 3. Shifts `<<`, `>>` | 7–9 | slide the bits |
| 4. `&`, `\|`, `^` | 10–12 | combine two rows |
| 5. Exercises | 13–14 | solved below |
| 6. Applications | 15–17 | masks, XOR encryption |

---

## 1. Bits, and why sizes matter (slides 3–4)

A byte is 8 bits. Bit positions are numbered **from the right, starting at 0** (slide 15):

```
value  1  0  1  1  0  1  1  0
bit    7  6  5  4  3  2  1  0        <- bit 0 is the "least significant bit" (LSB)
```

Handy notation: `0b10110110` is a **binary literal**; `std::bitset<8>(x)` prints a number in binary.

**Fixed-size types (slide 3).** `int` and `long` differ between machines (Chapter 8). When you need an exact width use `#include <cstdint>`: `int8_t`, `int16_t`, `int32_t`, `int64_t` and unsigned `uint8_t`, `uint16_t`, … Verified sizes: 1, 2, 4, 8 bytes.

**Signed vs unsigned:** an *unsigned* type uses all bits for the magnitude. A *signed* type's top bit is the sign bit (1 = negative). Bit tricks are safest on **unsigned** types.

⚠️ **Slide 4's example is wrong.** It shows `2 → 11011011` and `5 → 01001110`. Those bit rows are **219** and **78**. The real 8-bit patterns are:

```
2 = 0000 0010        5 = 0000 0101
```

(The slide's point, "an operand is a collection of bits", is right; the bit patterns are just arbitrary.)

## 2. Negation `~` (slides 5–6)

`~` flips **every** bit (also called *one's complement*): `0→1`, `1→0`. One operand.

```
A   1001 0110 0001 0001
~A  0110 1001 1110 1110      (slide 6 is correct; verified)
```

⚠️ **Promotion trap (not on the slides).** C++ converts `char`/`uint8_t` to `int` before doing arithmetic-style operations. So for `uint8_t x = 0b11000101;`, `~x` is **not** `0011 1010`: it is an `int` with all 32 bits flipped (`-198`), so `~x == 0b00111010` is **false**. Cast back: `(uint8_t)~x == 0b00111010` is **true** (both verified).

## 3. Shifts (slides 7–9)

`x << n` slides bits **left** by `n`, filling with zeros on the right; bits pushed off the left are **lost**. `x >> n` slides right; bits pushed off the right are lost.

**Useful meaning (verified):** `<< n` multiplies by 2ⁿ, `>> n` divides by 2ⁿ (dropping the remainder): `13 << 2 = 52`, `13 >> 2 = 3`, `1 << 4 = 16`.

Slide 9 (16-bit `A = 1001 0110 0001 0001`), verified:

```
A<<1  0010 1100 0010 0010    (leftmost 1 lost, a 0 enters on the right)
A>>3  0001 0010 1100 0010    (three 0s enter on the left)   -- for an UNSIGNED A
```

⚠️ **Two problems on these slides:**

1. **Slide 7's callout says "0 or 1 bits inserted on right".** For `>>`, new bits enter on the **left** (the "?" in the diagram) and the **rightmost** bit is discarded. Slide 8 (`<<`) is correct: zero inserted on the right.
2. **"0 or 1" depends on the type.** Unsigned values shift in **0s** ("logical shift"). Signed *negative* values normally shift in **copies of the sign bit** ("arithmetic shift") so the number stays negative. Verified: treating `A` as a signed 16-bit value (−27119), `A >> 3` gives `1111 0010 1100 0010`, not the slide's `0001 …`. Also `-8 >> 1` = **−4**. Slide 9's `000` fill is correct only for unsigned.

## 4. `&`, `|`, `^` (slides 10–12)

| a | b | `a & b` (AND) | `a \| b` (OR) | `a ^ b` (XOR) |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | **1** | 1 | **0** |

Words: **AND** = both are 1; **OR** = at least one is 1; **XOR** ("exclusive or") = exactly one is 1, i.e. *the bits differ*. (All three truth tables on slides 10–11 are correct.)

Slide 12 verified:

```
A    1001 0110 0001 0001
B    0001 1010 1101 1001
A&B  0001 0010 0001 0001
A|B  1001 1110 1101 1001
A^B  1000 1100 1100 1000
```

⚠️ **`&` is not `&&`.** `12 & 10` = **8** (bitwise), `12 && 10` = **1** (true/false); `12 | 10` = 14, `12 || 10` = 1 (verified). Also `n & 1 == 0` is parsed as `n & (1 == 0)` and gives 0 for `n = 6`; write `(n & 1) == 0` (gives 1). Always bracket bit expressions.

---

## 5. Exercises — worked solutions

### Exercise 1 (slide 13): M = 0011 1010, N = 1010 1101 (8-bit)

| | Working | Answer |
|---|---|---|
| 1. `~M` | flip each bit of 0011 1010 | **1100 0101** |
| 2. `M \| N` | 0011 1010 \| 1010 1101 | **1011 1111** |
| 3. `M ^ N` | 0011 1010 ^ 1010 1101 | **1001 0111** |
| 4. `~(N ^ M)` | `N^M` = 1001 0111, then flip | **0110 1000** |
| 5. `N & M` | 1010 1101 & 0011 1010 | **0010 1000** |
| 6. `N & ~M` | `~M` = 1100 0101; 1010 1101 & 1100 0101 | **1000 0101** |

All six verified. (Note 4 is simply the flip of 3. In C++ with `uint8_t`, expressions 1 and 4 give an `int`, so mask with `& 0xFF` or cast to `uint8_t` to see 8 bits.)

### Exercise 2 (slide 14): M = 1011 0110

The slide does not give the width. The intended model is an **8-bit register** where bits shifted off the left are lost after every operation.

| | Working | Answer |
|---|---|---|
| 1. `M >> 2` | 1011 0110 → 0010 1101 | **0010 1101** |
| 2. `M << 3` | 1011 0110 → (10110 lost) 1011 0000 | **1011 0000** |
| 3. `M >> 2 << 3` | 0010 1101 → 0110 1000 | **0110 1000** |
| 4. `M << 1 >> 4` | `M<<1` = 0110 1100 (top 1 lost), `>>4` | **0000 0110** |

Verified with each step stored back into a `uint8_t`.

⚠️ **What C++ does if you write it in one expression.** `M << 1 >> 4` is computed in an `int`, so the top bit is **not** lost between the two shifts: the result is `0001 0110`, not `0000 0110`. Likewise `M << 3` in an `int` is `0101 1011 0000` (12 bits) until you store it into a `uint8_t` (then `1011 0000`). For the exam use the 8-bit register answers; when coding, store intermediate results in the right type.

---

## 6. Applications (slides 15–17)

### 6.1 Masking (flags)

A **bit mask** is a number with 1s in the positions you care about. Recipes (verified on `flags = 0101 0001`):

| Goal | Code | Result for the running example |
|---|---|---|
| **set** bit 3 to 1 | `flags \|= (1 << 3);` | `0101 1001` |
| **clear** bit 0 | `flags &= ~(1 << 0);` | `0101 1000` |
| **toggle** bit 7 | `flags ^= (1 << 7);` | `1101 1000` |
| **test** bit 4 | `(flags & (1 << 4)) != 0` | true (bit 4 is 1); bit 1 → false |

Why they work: `|` with a 1 forces 1; `&` with a 0 forces 0 (so use `~mask`, which has a single 0); `^` with a 1 flips; `&` with a single 1 keeps only that bit, so the result is non-zero exactly when the bit is on.

**Uses:** file permissions (read/write/execute = 3 bits), option flags, network address masks, packing several yes/no settings into one byte.

### 6.2 XOR "encryption" (slides 16–17)

Key fact: `x ^ key ^ key = x` (XOR twice with the same key restores the value), because `k ^ k = 0` and `x ^ 0 = x`.

Slide 17, verified: data `0101 0000` (`'P'`) ^ key `0001 0010` = `0100 0010` (`'B'`); XOR again with the key gives `0101 0000` (`'P'`). Another check: `'H' ^ 0x2A` = `0x62` (`'b'`), and `0x62 ^ 0x2A` = `'H'`. A repeating-key version over a whole string `"PASS"` round-trips correctly.

⚠️ **This is an exercise, not real security (extra, not in slides).** If an attacker knows one plaintext byte and its encrypted byte, `plain ^ cipher` reveals the key: `'P' ^ 'B'` = `0001 0010`, exactly the slide's key. Short repeating keys are broken quickly. Real systems use vetted ciphers (e.g. AES), not hand-rolled XOR.

---

## ⚠️ Where the slides mislead

| Slide | Slide says | Truth |
|---|---|---|
| 4 | `2 → 11011011`, `5 → 01001110` | those are 219 and 78; real: `00000010`, `00000101` |
| 7 | right shift: "0 or 1 bits inserted on **right**" | inserted on the **left**; the right bit is discarded |
| 9 | `A>>3` fills with `000` | true only for unsigned; signed negatives copy the sign bit |
| 13–14 | exercises unanswered; width unspecified | 8-bit answers above; C++ promotes to `int` |
| 15 | "least significant bi" | typo: bit |

**Exam strategy:** use 8-bit register behaviour (bits shifted off are lost) and unsigned shifts, matching the slides' diagrams.

## Cheat sheet

| Operator | Meaning | Example (8-bit) |
|---|---|---|
| `~a` | flip all bits | `~0011 1010 = 1100 0101` |
| `a & b` | 1 if both 1 | keep / clear bits |
| `a \| b` | 1 if either 1 | set bits |
| `a ^ b` | 1 if different | toggle, encrypt |
| `a << n` | ×2ⁿ, zeros in on right | `13 << 2 = 52` |
| `a >> n` | ÷2ⁿ | `13 >> 2 = 3` |
| set / clear / toggle / test bit n | `\|= 1<<n` / `&= ~(1<<n)` / `^= 1<<n` / `& (1<<n)` | |
| `x ^ x` / `x ^ 0` | 0 / x | |

---

## Practice (answers after each part)

### A. Multiple choice

**A1.** `5 & 3` = (a) 1 (b) 7 (c) 6 (d) 2
**A2.** `6 ^ 3` = (a) 5 (b) 7 (c) 3 (d) 0
**A3.** `1 << 4` = (a) 4 (b) 8 (c) 16 (d) 32
**A4.** `x ^ x` = (a) x (b) 0 (c) 1 (d) `~x`
**A5.** Which correctly tests whether `n` is even? (a) `n & 1 == 0` (b) `(n & 1) == 0` (c) `n && 1 == 0` (d) `n ^ 1`

### B. Short answer

**B1.** Explain how to set, clear, toggle and test bit 3 of a flags byte.
**B2.** Explain why XORing with the same key twice restores the original.
**B3.** Explain the difference between `&` and `&&`.

### C. Calculation / trace

**C1.** 8-bit `A = 0110 1001`, `B = 0011 1100`. Find `A & B`, `A | B`, `A ^ B`.
**C2.** `flags = 0101 0001`. Apply in order: set bit 3, clear bit 0, toggle bit 7. Give the final value.
**C3.** Encrypt `'H'` (0x48) with key 0x2A, give the result in hex and as a character, then decrypt it.

### D. Thinking

**D1.** Exercise 2 part 4 (`M << 1 >> 4`) has two possible answers in C++. Explain why.
**D2.** Why is XOR with a short repeating key a poor way to protect data, even though it round-trips correctly?

---

### Answers

**A1 → (a) 1** (101 & 011 = 001). **A2 → (a) 5** (110 ^ 011 = 101). **A3 → (c) 16.** **A4 → (b) 0.** **A5 → (b).** `==` binds tighter than `&`, so (a) means `n & (1 == 0)` (verified 0 for n = 6).

**B1.** Set: `flags |= (1 << 3);` Clear: `flags &= ~(1 << 3);` Toggle: `flags ^= (1 << 3);` Test: `(flags & (1 << 3)) != 0`.

**B2.** `(x ^ key) ^ key = x ^ (key ^ key) = x ^ 0 = x`. Verified with 'P'→'B'→'P'.

**B3.** `&` works bit by bit on integers and returns a number (`12 & 10 = 8`); `&&` treats each operand as true/false and returns true/false (`12 && 10 = 1`), stopping early if the left side is false.

**C1.** `A & B` = **0010 1000**; `A | B` = **0111 1101**; `A ^ B` = **0101 0101**. Verified.

**C2.** `0101 0001` → set bit 3 → `0101 1001` → clear bit 0 → `0101 1000` → toggle bit 7 → **`1101 1000`** (0xD8). Verified.

**C3.** `0x48 ^ 0x2A` = **0x62 = 'b'**; `0x62 ^ 0x2A` = 0x48 = `'H'`. Verified.

**D1.** In an idealised 8-bit register the top bit is lost after `<< 1`, giving `0000 0110`. In C++ the value is promoted to a 32-bit `int` first, so nothing is lost between the shifts and the result is `0001 0110`. Both were verified. State your assumption.

**D2.** Knowing a single plaintext/ciphertext pair reveals the key (`'P' ^ 'B'` = `0001 0010`), and a short key repeats, so patterns leak. XOR alone is a teaching example, not real security.

---

## Links to other chapters

- **Ch 8:** sizes of `int`/`long` vary, motivating `<cstdint>`; `enum` values are often combined as bit flags.
- **Ch 1:** arrays of flags or bytes; `vector<bool>` is bit-packed.
- **Ch 11:** a good design keeps the "flag handling" in one cohesive module (set/clear/test functions).
