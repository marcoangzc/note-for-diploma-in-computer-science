# AMCS2034 — Chapter 3: Efficiency of an Algorithm

> 这章是整个后半部分的地基。Slide 有很多句子看起来很抽象（asymptotic、rate of growth、dominant term…），
> 其实核心只有一个问题：**"数据变大以后，algorithm 会慢多少？"**

---

## 0. 这章一句话总览

- 我们 **不比较** "跑了几秒" 或 "写了几行"（因为会受电脑和写法影响）
- 我们比较 **"input 变大时，工作量怎么增长"** → 这就是 **rate of growth**
- 用 **best / worst / average case** 描述同一个 algorithm 在不同 input 下的表现

---

## 1. 为什么要分析 algorithm？（Slide 3–4）

**类比**：从 A 城到 B 城可以坐飞机、巴士、火车、脚车。选哪个看你在乎什么（快？便宜？方便？）。

同一个问题也有很多 algorithm（例如 sorting 有 insertion sort、quick sort…）。Algorithm analysis 帮我们比较：

| 比什么 | 意思 |
|---|---|
| Running time | 要多久 |
| Memory requirement | 用多少 memory |
| Developer effort | 写起来多难 |

---

## 2. 怎么比较？为什么不用"跑几秒"？（Slide 5–9）

### Input size（n）

Running time analysis = 看 **input size 增加时，时间怎么变**。Input size n 依问题而定：

| 问题 | n 是什么 |
|---|---|
| Array 相关 | array 的大小 |
| Matrix | element 数量 |
| Graph | vertices + edges 的数量 |
| 数字（binary） | bit 的位数 |

### 两个"看起来可行但不好"的方法

| 方法 | 为什么不好 |
|---|---|
| 量 execution time | 电脑不同、同时跑别的程序、input 不同，时间都会变（slide 8 提到 system load 和 specific input） |
| 数 statements | 不同 language、不同人的 coding style，行数会不一样 |

### 理想的方法

把 running time 写成 **input size 的函数 f(n)**，然后比较不同 algorithm 的 f(n)。这样与电脑、language、coding style 都无关。

---

## 3. Rate of Growth（Slide 10–16）

**Rate of growth = 当 n 变大时，running time 增加得多快。**

### 3.1 Car and Bicycle（Slide 12–13）

你去店里买一辆 car 和一辆 bicycle，朋友问你买什么，你说"买 car"。因为 car 的价钱远远大于 bicycle，bicycle 的价钱可以 **忽略**。

换成 algorithm：total cost = `n⁴ + 2n² + 100n + 500`。当 n 很大时，`n⁴` 那一项 **压倒其他所有项**，所以只看 `n⁴`（叫 **dominant term**，主导项）。

用数字看 `n⁴` 占多少：

| n | n⁴ | 2n² | 100n | 500 | 总和 | n⁴ 占的比例 |
|---|---|---|---|---|---|---|
| 10 | 10,000 | 200 | 1,000 | 500 | 11,700 | 85.5% |
| 100 | 100,000,000 | 20,000 | 10,000 | 500 | 100,030,500 | **99.97%** |
| 1000 | 10¹² | 2,000,000 | 100,000 | 500 | ≈ 10¹² | **99.9998%** |

**n 越大，其他项越不重要。** 所以 Big-O 才可以放心丢掉它们。

### 3.2 为什么常数也可以丢掉？

Slide 26 说 `O(n) = O(n/2) = O(100n)`。你可能会想："100n 明明比 n 慢 100 倍啊？"

关键：我们关心的是 **n 变大时"形状"怎么变**，不是具体倍数。比较 `100n`（linear）和 `n²`（quadratic）：

| n | 100n | n² | 谁大？ |
|---|---|---|---|
| 10 | 1,000 | 100 | 100n |
| 100 | 10,000 | 10,000 | 一样 |
| 1,000 | 100,000 | 1,000,000 | **n²** |
| 100,000 | 10,000,000 | 10,000,000,000 | **n² 大很多** |

不管 linear 前面乘多大的常数，**n 够大时 quadratic 一定会超过它**。所以只看"形状"（growth rate）就够了。

### 3.3 Linear search 的例子（Slide 14–15）

Linear search = 从头一个一个比较，直到找到或找完。

Array = `[7, 3, 9, 1]`，找 key = 9：比 7（不是）→ 比 3（不是）→ 比 9（找到）→ 3 次比较。

- **Array 大小加倍 → comparison 次数也大约加倍** → 成 **linear（线性）** 增长
- 所以说 "order of magnitude 是 n"，写成 **O(n)**，读作 "order of n"

---

## 4. Types of analysis：Best / Worst / Average（Slide 17–25）

同一个 algorithm，input 不同，时间会不同。

**类比**：上学的路程

- **Best case**：一路畅通，最快
- **Worst case**：塞车，最慢
- **Average case**：平均下来大概多久

### Linear search 三种 case（n 个 element）

| Case | 什么时候发生 | 比较次数 |
|---|---|---|
| **Best** | key 刚好在 **第一个** | 1 |
| **Worst** | key 在 **最后**，或 **根本不在** array | n |
| **Average** | key 在 array 里，位置随机 | 大约 n/2 |

> ⚠️ "average = n/2" 有前提：**key 一定在 array 里，而且每个位置的机会一样**。如果 key 不在 array，就是 n 次（Slide 14 说得很清楚）。

### 关系

```
Lower bound（best） ≤ Average ≤ Upper bound（worst）
```
（Slide 22）

### 为什么大家最常用 worst case？（Slide 24–25）

| Case | 有用吗？ |
|---|---|
| Best case | **不具代表性**（运气好才发生，不能拿来保证什么） |
| Average case | 理想，但 **很难算**（要知道 input 的概率分布） |
| **Worst case** | **最实用**：保证 algorithm "**最差也不会比这个慢**"，而且比较容易分析 |

### Slide 8 的例子：为什么"跑一次的时间"会误导？

Key 恰好在 list 第一个 → linear search 一步就找到，比 binary search 还快。但这只是 **特定 input** 的巧合，不代表 linear search 比较好。所以才要用 f(n) 和 worst case 来看。

---

## 5. 两个经典例子

### 5.1 找最大值（Slide 29–30）

n 个数字找最大的：要做 **n − 1 次比较**。

| n | 比较次数 |
|---|---|
| 2 | 1 |
| 3 | 2 |
| n | n − 1 |

n 很大时，`−1` 不重要，主导的是 `n` → **O(n)**。

### 5.2 Constant time（Slide 31）

如果时间 **不受 input size 影响**，就叫 constant time，写成 **O(1)**。

例子：`arr[5]` 直接拿第 5 格。array 有 10 格还是 1,000,000 格，都是"算一下地址、直接拿"，时间一样。

> ⚠️ O(1) **不是** "只花 1 步"，而是"步数不随 n 变"。

---

## 6. 常用 growth rate 一览（先预览，Ch5 详细讲）

从慢（好）到快（坏）：

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ)
```

---

## 7. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Rate of growth | n 变大时，running time 增长多快 |
| Dominant term | n 很大时压倒其他项的那一项 |
| Constants | 不影响 growth rate，`O(100n) = O(n)` |
| Best / Worst / Average | 最快 / 最慢 / 平均的 input |
| 为什么用 worst case | 保证上限，而且比 average 容易分析 |
| Linear search | best 1，worst n，average ≈ n/2，O(n) |
| Find max | n − 1 次比较，O(n) |
| O(1) | 时间不随 n 变 |

---

## 8. 练习

### A. MCQ

**A1.** 为什么不能直接用 "跑了几秒" 来比较两个 algorithm？
a) 秒数太小　b) 会受电脑、system load、input 影响　c) Java 不能量时间　d) 时间不重要

**A2.** `3n³ + 50n² + 1000` 的 dominant term 是？
a) 1000　b) 50n²　c) 3n³　d) 3

**A3.** 在 n 个 element 的 array 里 linear search，key **不在** array，需要几次比较？
a) 1　b) n/2　c) n　d) log n

**A4.** 找 n 个数字里的最大值，需要几次比较？
a) n　b) n − 1　c) n/2　d) n²

**A5.** 下面哪个是 O(1)？
a) 走过整个 array　b) 在 linked list 找第 n 个　c) 用 index 取 array 的元素　d) linear search

### B. Short answer

**B1.** 解释 dominant term，并用 car and bicycle 的类比说明。

**B2.** 为什么 worst-case analysis 比 average-case 常用？

**B3.** 为什么说 `O(n) = O(n/2) = O(100n)`？

### C. Calculation

**C1.** `f(n) = n⁴ + 2n² + 100n + 500`，n = 100 时总和是多少？`n⁴` 占多少百分比？

**C2.** Linear search，n = 1000。worst case 和 average case 各要多少次比较？如果 array 变成 2000，worst case 呢？

**C3.** 化简成 Big-O：(a) `5n + 20`　(b) `3n² + 7n`　(c) `n/2 + log n`

### D. Thinking

**D1.** 一个 algorithm 是 O(n²)，另一个是 O(n)。是不是 O(n) 的永远比较快？

**D2.** Linear search 的 best case 是 O(1)。能不能说 "linear search 是 O(1) algorithm"？

---

### 答案

**A1: b**　**A2: c**　**A3: c**　**A4: b**　**A5: c**

**B1.** Dominant term 是 n 很大时，对总和影响最大的那一项。买 car 和 bicycle，人们说"买 car"，因为 car 的价钱远大于 bicycle，bicycle 可以忽略。同理，`n⁴ + 2n² + 100n + 500` 当 n 很大时，只看 `n⁴`。

**B2.** Average case 需要知道所有 input 的出现概率，通常很难求；worst case 只需要找出最坏的 input，比较简单，而且能保证 algorithm 不会比这个更慢。

**B3.** Big-O 只看 growth rate（形状），不看乘上的常数。n/2 和 100n 都是 "n 加倍，时间也加倍"，属于同样的 linear 增长。

**C1.** 总和 = 100,000,000 + 20,000 + 10,000 + 500 = **100,030,500**。`n⁴` 占 100,000,000 / 100,030,500 ≈ **99.97%**。

**C2.** Worst = **1000**，average ≈ **500**（假设 key 存在且位置随机）。Array 变 2000 → worst = **2000**（加倍）。

**C3.** (a) **O(n)**　(b) **O(n²)**　(c) **O(n)**（n/2 比 log n 增长快，取 n；常数 1/2 丢掉）

**D1.** 不一定。O(n) 的 algorithm 可能常数很大（例如 100n），n 很小时（n < 100）可能比 n² 慢。但 **n 够大时** O(n) 一定赢。

**D2.** 不能。O(1) 只是 **best case**，不代表 algorithm 整体。一般说 algorithm 的复杂度用 **worst case**，所以 linear search 是 O(n)。

---

## 9. 和后面章节的连接

- Ch4：怎么 **数** operations 得到 f(n)（primitive operations）
- Ch5：把 "≤"、"≥"、"夹在中间" 变成正式记号：O、Ω、Θ
