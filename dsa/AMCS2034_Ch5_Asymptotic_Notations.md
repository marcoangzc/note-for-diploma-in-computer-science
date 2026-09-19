# AMCS2034 — Chapter 5: Asymptotic Notations (Big-O, Ω, Θ)

> 这章最容易 "读了但没懂" 的地方：
> ① O / Ω / Θ 到底是什么意思？ ② 它们和 best / worst case 是同一回事吗？ ③ 那个 `f(n) ≤ c·g(n)` 的定义怎么用？
> 这份 note 用例子把三个问题都讲清楚。

---

## 0. 这章一句话总览

> **Asymptotic notation = 用一个简单的函数 g(n)，去描述 f(n) 在 n 很大时的"形状"。**

| 记号 | 白话 | 类比（考试分数） |
|---|---|---|
| **O**(g)  Big-O | **上界**：不会比 g 更差 | 分数不会超过 90 |
| **Ω**(g)  Big-Omega | **下界**：至少有 g 那么多 | 分数至少有 40 |
| **Θ**(g)  Big-Theta | **紧界**：上下都夹住 | 分数在 60 到 70 之间 |

---

## 1. 什么是 "Asymptotic"？（Slide 3–4）

给一个复杂的 f(n)，我们想找一个 **简单的 g(n)**，在 n 很大时和 f(n) 的形状差不多。

例：`f(n) = 2n² + 4n + 1`，n 很大时它的形状 ≈ `n²`。所以 g(n) = n² 就是 f(n) 的 **asymptotic curve**。

这就是为什么分析 algorithm 也叫 **asymptotic analysis**："n 趋近很大" 时的行为。

---

## 2. 三个记号的正式定义（Slide 9, 14, 15）

### 2.1 Big-O：f(n) = O(g(n))

> 存在正数 **c** 和 **N**，使得对所有 **n ≥ N**，都有 **f(n) ≤ c · g(n)**

白话：**"n 够大以后，f(n) 永远不会超过 g(n) 的某个倍数。"**

### 2.2 Big-Omega：f(n) = Ω(g(n))

> 存在正数 c 和 N，使得对所有 n ≥ N，都有 **f(n) ≥ c · g(n)**

白话：n 够大以后，f(n) **至少** 有 g(n) 的某个倍数那么大。

### 2.3 Big-Theta：f(n) = Θ(g(n))

> 存在正数 c₁, c₂ 和 N，使得对所有 n ≥ N，都有 **c₂·g(n) ≤ f(n) ≤ c₁·g(n)**

白话：**同时是 O(g) 和 Ω(g)**，被 g(n) 上下夹住。（Slide 15 用 c₁ 表示上界的倍数，c₂ 表示下界的倍数，别看反。）

### 2.4 用一个真实例子把定义走一遍

**f(n) = 2n² + 4n + 1，证明 f(n) = O(n²)**

要找 c 和 N。试 **c = 3**：

需要 `2n² + 4n + 1 ≤ 3n²`，也就是 `n² ≥ 4n + 1`。

| n | f(n) = 2n²+4n+1 | 3n² | f ≤ 3n² ? |
|---|---|---|---|
| 1 | 7 | 3 | ✗ |
| 2 | 17 | 12 | ✗ |
| 3 | 31 | 27 | ✗ |
| 4 | 49 | 48 | ✗（差一点） |
| **5** | 71 | 75 | ✅ |
| 6 | 97 | 108 | ✅ |

从 n = 5 开始一直成立 → **c = 3, N = 5** → f(n) = **O(n²)** ✅

**Ω 的部分**：`2n² + 4n + 1 ≥ 2n²` 对所有 n ≥ 1 都成立 → c = 2, N = 1 → **Ω(n²)**

**Θ 的部分**：n ≥ 5 时 `2n² ≤ f(n) ≤ 3n²` → **Θ(n²)**

> 记住：**N 的意思是 "从这个点开始才成立"**。小 n 不成立没关系，我们只关心 n 很大的时候。

---

## 3. ⚠️ 最大的误会：O / Ω / Θ vs Best / Worst / Average

Slide 8 和 14 说：Big-O 是 "maximum time"，Ω 是 "best-case"。这是 **简化版**，容易让人以为：

> O = worst case，Ω = best case，Θ = average case ← ❌ 这样想会出错

**正确的想法：这是两个不同的维度。**

| 维度 | 问的是什么 | 选项 |
|---|---|---|
| ① **哪种 case** | 我要分析哪种 input | Best / Worst / Average |
| ② **哪种 bound** | 我怎么描述这个函数 | O / Ω / Θ |

先选 case 得到一个函数 T(n)，再用 O / Ω / Θ 描述它。

**Linear search 例子：**

| Case | T(n) | 可以写成 |
|---|---|---|
| Best（key 在第一个） | 1 | **Θ(1)** |
| Worst（key 在最后 / 不存在） | n | **Θ(n)** |
| Average | ≈ n/2 | **Θ(n)** |

所以：
- "Linear search 的 worst case 是 O(n)" ✅
- "Linear search 的 best case 是 Ω(1)" ✅
- "Linear search 是 O(1)" ❌（这句话只在 best case 才成立）

> 📝 **考试策略**：如果题目问 "Ω 代表什么"，按 slide 答（lower bound / best case）。但自己要明白上面的区别，遇到进阶题就不会被绕晕。

### 松 vs 紧

`f(n) = n` 是不是 O(n²)？**技术上是。**（因为 n ≤ n²，c=1, N=1。）但这个上界很 **松**。

- Big-O 只保证"不会比这个差"，**可以很松**
- **Θ 是紧的**，最精确

平常说 "algorithm 是 O(n)"，我们通常指的是最紧的那个上界。

---

## 4. 怎么化简成 Big-O？五条规则

| 规则 | 例子 |
|---|---|
| ① 丢掉常数倍 | `100n` → n |
| ② 丢掉低阶项 | `n² + n + 1` → n² |
| ③ 前后接着的两段 code：取 **较大** 的 | `O(n) + O(n²)` → O(n²) |
| ④ 嵌套的 loop：**相乘** | 外层 n 次 × 内层 n 次 → O(n²) |
| ⑤ 每次减半 / 加倍 → **log n** | `i = i * 2` 的 loop |

Slide 里的例子：

- `2n² + 4n + 1` → 主导项 n² → **O(n²)**
- `7 log n + 5` → 主导项 log n → **O(log n)**
- Algorithm A：`2n + 1` → 2n → n → **O(n)**
- Algorithm B：`n² + n + 1` → **O(n²)**

### Loop 分析例子

```java
// (1) O(n)
for (int i = 0; i < n; i++) { ... }

// (2) O(n²)：外层 n × 内层 n
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) { ... }

// (3) O(n²)：内层次数是 1+2+…+n = n(n+1)/2 → 还是 n²
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= i; j++) { ... }

// (4) O(log n)：i 每次 ×2
for (int i = 1; i < n; i *= 2) { ... }
```

(4) 为什么是 log n？n = 16 时，i = 1, 2, 4, 8 → 跑 4 次 = log₂16。

---

## 5. 七个最常见的函数（Slide 18–25）

### 5.1 log n 到底是什么？

**log₂ n = "n 要对半切几次才变成 1"**

| n | 1024 | 512 | 256 | … | 2 | 1 |
|---|---|---|---|---|---|---|
| 切几次 | | 1 | 2 | … | 9 | **10** |

所以 log₂ 1024 = 10。这也是 **binary search** 每次砍掉一半的原理，100 万笔 data 只要约 20 次（2²⁰ ≈ 100 万）。

Slide 20 说默认底数是 2（因为电脑用 binary）。在 Big-O 里，底数不同只差一个常数倍，所以底数其实不重要。

### 5.2 七个函数和它们常出现的地方

| 函数 | 名称 | 什么时候出现 | 例子 |
|---|---|---|---|
| c | Constant | 做一个基本操作 | `arr[i]` |
| log n | Logarithmic | 每次把问题 **减半** | Binary search |
| n | Linear | 对 n 个 element 各做一次 | Linear search、找 max |
| n log n | n-log-n | 分治（D&C） | Merge sort 等有效率的 sort |
| n² | Quadratic | **嵌套 loop** | 简单的 sort（bubble / selection） |
| n³ | Cubic | 三层嵌套 loop | 简单的矩阵相乘 |
| 2ⁿ | Exponential | 每步 **翻倍** | Naive recursive fib、列出所有子集 |

### 5.3 谁快谁慢（Slide 26 的表）

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ)
 好 ────────────────────────────────────────────────► 坏
```

具体数值（log 是 base 2）：

| n | log n | n | n log n | n² | n³ | 2ⁿ |
|---|---|---|---|---|---|---|
| 4 | 2 | 4 | 8 | 16 | 64 | 16 |
| 8 | 3 | 8 | 24 | 64 | 512 | 256 |
| 16 | 4 | 16 | 64 | 256 | 4,096 | 65,536 |
| 32 | 5 | 32 | 160 | 1,024 | 32,768 | **4,294,967,296** |

看 2ⁿ：n 只是 16 → 32，就从 6 万变成 **43 亿**。这就是 exponential "爆炸"。

---

## 6. Picturing Efficiency（Slide 27–31）

### 6.1 n 加倍会怎样？（Slide 28）

| Big-O | n 变 2n，时间 … |
|---|---|
| O(1) | 不变 |
| O(log n) | 只 +1 步 |
| O(n) | ×2 |
| O(n log n) | 略多于 ×2 |
| O(n²) | **×4** |
| O(n³) | **×8** |
| O(2ⁿ) | 变成 **平方** |

### 6.2 处理 100 万笔 data，假设每秒 100 万个 operations（Slide 29）

| Big-O | operations | 时间 |
|---|---|---|
| O(log n) | ≈ 20 | 约 0.00002 秒 |
| O(n) | 10⁶ | **1 秒** |
| O(n log n) | ≈ 2 × 10⁷ | **约 20 秒** |
| O(n²) | 10¹² | **约 11.6 天** |
| O(n³) | 10¹⁸ | **约 3 万多年** |
| O(2ⁿ) | 天文数字 | 完全不可能 |

### 6.3 Slide 30 的意思

O(n²)、O(n³)、O(2ⁿ) **也可以用**，只要问题 **很小**（n 很小）。但只要 n 会变大，就一定要找更好的 algorithm。

### 6.4 Slide 16–17：怎么"评估" algorithm 的效率？

这两页是一个 checklist：分析 algorithm → 定 time / space complexity → 想 best / worst case → 跟别的 algorithm 比 → benchmark（实测）→ 需要的话优化 → 了解 tradeoff。

---

## 7. Cheat sheet

| 概念 | 一句话 |
|---|---|
| O | 上界：f ≤ c·g（n ≥ N） |
| Ω | 下界：f ≥ c·g |
| Θ | 上下夹住：c₂g ≤ f ≤ c₁g |
| O / Ω / Θ vs best / worst | **不同维度**：先选 case，再选 bound |
| 化简 | 丢常数、丢低阶、顺序取大、嵌套相乘、减半 = log |
| log₂ n | n 对半切几次到 1 |
| 顺序 | 1 < log n < n < n log n < n² < n³ < 2ⁿ |
| n 加倍 | n²→×4，n³→×8，2ⁿ→平方 |

---

## 8. 练习

### A. MCQ

**A1.** `4n³ + 2n + 9` 的 Big-O？
a) O(n)　b) O(n²)　c) O(n³)　d) O(9)

**A2.** 哪个 notation 表示 **紧界**（tight bound）？
a) O　b) Ω　c) Θ　d) 都不是

**A3.** 一个 O(n²) 的 algorithm，input 从 n 变成 2n，时间大约变成？
a) ×2　b) ×4　c) ×8　d) 不变

**A4.** `log₂ 1024` = ?
a) 2　b) 10　c) 32　d) 1024

**A5.** 下面哪个顺序（由慢增长到快增长）是对的？
a) n², n, log n　b) log n, n, n log n, n²　c) n log n, n, log n　d) 2ⁿ, n², n

### B. Short answer

**B1.** 解释 O、Ω、Θ 的分别。

**B2.** `f(n) = n` 是 O(n²) 吗？这句话有意义吗？

**B3.** 为什么 Big-O 可以丢掉常数和低阶项？

### C. Calculation

**C1.** 证明 `3n + 10 = O(n)`，找出 c 和 N。

**C2.** 分析下面三段 code 的 Big-O：
```java
// (a)
for (int i = 1; i < n; i *= 2) sum++;

// (b)
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= i; j++) sum++;

// (c)
for (int i = 0; i < n; i++) sum++;
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) sum++;
```

**C3.** 100 万笔 data，每秒 100 万 operations。O(n) 和 O(n²) 各需要多久？

### D. Thinking

**D1.** Algorithm A 是 O(n log n) 但常数很大（1000 · n log₂ n），B 是 O(n²)（常数 1）。n 大概要多大 A 才比 B 快？

**D2.** "Ω 就是 best case"，这句话哪里不严谨？

---

### 答案

**A1: c**　**A2: c**　**A3: b**　**A4: b**　**A5: b**

**B1.** O 是上界（增长不会超过 g）；Ω 是下界（增长至少有 g 那么多）；Θ 同时是上界和下界，即紧界（f 被 g 夹住）。

**B2.** 技术上是（n ≤ n²）。但这个上界很松，没什么信息量。要精确说 f(n) = n 应该说 Θ(n)。

**B3.** n 很大时，主导项决定了增长的"形状"，低阶项和常数占的比例越来越小。Big-O 关心的是 growth rate，不是精确的步数。

**C1.** `3n + 10 ≤ 4n` ⇔ `n ≥ 10`。所以 **c = 4, N = 10** → `3n + 10 = O(n)`。

**C2.**
- (a) i 每次 ×2 → 约 log₂ n 次 → **O(log n)**
- (b) 内层总次数 = 1 + 2 + … + n = n(n+1)/2 → **O(n²)**
- (c) O(n) + O(n²) = **O(n²)**（顺序取大）

**C3.**
- O(n)：10⁶ / 10⁶ = **1 秒**
- O(n²)：10¹² / 10⁶ = 10⁶ 秒 ≈ **11.6 天**

**D1.** 要 `1000 · n · log₂ n < n²`，即 `1000 · log₂ n < n`。试算：n = 13,700 时左边 ≈ 13,743 > 13,700（A 还不够快）；n = 14,000 时左边 ≈ 13,770 < 14,000 ✅。所以 **n 大约要超过 14,000**，A 才开始比 B 快。（这说明 "常数很大的低阶 algorithm" 在小数据时不一定赢。）

**D2.** 因为 Ω 只是"下界"的数学记号，best case 是"哪种 input"的分类。你可以对 **worst case** 的函数也取 Ω（例如 linear search 的 worst case 是 Ω(n)）。两个是不同维度，不能画等号。

---

## 9. 和后面章节的连接

- Ch6：HashSet 的 add / contains 平均 O(1)，TreeSet 是 O(log n)
- Ch7：Array 取值 O(1)、insert 中间 O(n)；Linked list 反过来
- Ch9：DFS / BFS 的 O(|V| + |E|)
