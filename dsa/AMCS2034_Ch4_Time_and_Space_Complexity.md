# AMCS2034 — Chapter 4: Time and Space Complexity

> Ch3 讲"为什么要看 growth rate"，Ch4 讲 **怎么真的去算**：
> 数 primitive operations → 得到 f(n)。另外还讲 space（memory）和 space/time tradeoff。

---

## 0. 这章一句话总览

| Topic | 重点 |
|---|---|
| Empirical analysis | 真的跑 code 量时间（有很多缺点） |
| Theoretical analysis | 数 **primitive operations**，写成 f(n) |
| Space complexity | 用多少 memory（尤其是 data structure 本身） |
| Space/Time tradeoff | 用多一点 memory 换速度，或反过来 |

---

## 1. Time complexity vs Space complexity（Slide 3–5）

| | Time complexity | Space complexity |
|---|---|---|
| 量什么 | 执行要多久（数 elementary steps） | 用多少 **main memory** |
| 通常看哪个 case | **Worst case**（最大时间） | — |
| 用什么表示 | Big-O | Big-O |

### ⚠️ Slide 5 有一句会误导

Slide 说 "the number of instruction ... residing in the algorithm will decide the space complexity"。**这样理解会错。**

- Space complexity 主要是看 **数据占多少 memory**：变量、array、object、recursion 的 call stack。
- **不是** 看你的 code 有多长（code 行数多不代表 space 大）。

例子：

```java
int sum = 0;                      // 1 个变量 → O(1) 额外 space
int[] copy = new int[n];          // 一个 n 大小的 array → O(n) space
```

---

## 2. Empirical analysis（Slide 6–19）

### 2.1 做法

1. 写好 **两个** algorithm
2. 跑它们，记录时间
3. 多跑几次取平均
4. 比较

Java 量时间的写法（Slide 14–15）：

```java
long start = System.nanoTime();     // 开始前记时间
runAlgorithm();
long end = System.nanoTime();       // 结束后记时间
long elapsed = end - start;         // 相减 = 用了多久（nanoseconds）
```

`currentTimeMillis()` 是毫秒，`nanoTime()` 是纳秒，很快的操作要用 `nanoTime()`。

### 2.2 缺点（考试最爱问）

| 缺点 | 解释 |
|---|---|
| **Uncontrolled factors** | system load、programming language、compiler efficiency 都会影响时间 |
| **Programmer bias** | 两个 program 的实作水平不同，结果不公平 |
| **Code tuning** | 一个 program 被多优化了一点，时间就变了 |
| **只测有限的 input** | 没测到的 input 可能很重要 |
| **必须先完整 implement** | 还没写完就不能比较 |
| **必须同样的 hardware / software** | 不同电脑没办法直接比 |

### 2.3 Code tuning 想说什么？（Slide 10）

如果两个 program 的时间只差一个 **常数倍**（growth rate 一样），那么谁被 tune 得比较好，谁就赢，结果跟 algorithm 好不好没关系。

> 但如果 **growth rate 不同**（例如 O(n) vs O(n²)），n 够大时再怎么 tune 也追不上。所以我们才需要看 growth rate。

### 2.4 Simulation（Slide 11）

Simulation = 用 program **模拟** 一个真实问题，然后跑出结果。它的目的是分析 **很难或很大的问题**，和 "跑两个 program 比较时间" 的 empirical comparison 不一样。

### 2.5 我们想要的分析方法（Slide 19）

- 不受 hardware / software 影响
- 只看 algorithm 的 **高层描述**，不用先写完
- 考虑 **所有可能的 input**

这就是下面的 theoretical analysis。

---

## 3. Theoretical analysis：数 Primitive Operations（Slide 20–34）

### 3.1 什么是 primitive operation？（Slide 22）

一步就能完成的基本动作：

| Primitive operation | 例子 |
|---|---|
| Assign 值给变量 | `x = 5` |
| 跟随 object reference | `s.name` |
| Arithmetic 运算 | `a + b`、`a * b` |
| 比较两个数字 | `a < b` |
| 用 index 拿 array 元素 | `A[i]` |
| 调用 method | `foo()` |
| 从 method return | `return x` |

我们 **不去算每个 operation 到底几纳秒**，只数"做了几个 operation"，得到 t，t 会和真正的 running time 成正比（Slide 23）。

### 3.2 把 t 写成 n 的函数 f(n)（Slide 24）

Input 越大，operations 越多，所以用 **f(n)** 表示"input size 是 n 时，做了多少个 operations"。

### 3.3 为什么用 worst case？（Slide 25–26）

Average case 要定义 input 的概率分布，很难。Worst case 只要找出最坏的 input，比较容易；而且针对最坏情况去设计，通常会得到更好的 algorithm。

### 3.4 有用的公式（Slide 27）

```
1 + 2 + … + n       = n(n + 1) / 2
1 + 2 + … + (n − 1) = n(n − 1) / 2
```

**为什么？**（配对法）：把 1 到 n 头尾配对：`1+n`, `2+(n−1)`, … 每一对都是 n+1，一共有 n/2 对 → n(n+1)/2。

---

## 4. 三个算 1 + 2 + … + n 的 algorithm（Slide 28–33）

**问题**：给正整数 n，算 1 + 2 + … + n。

**Algorithm A — 一个 loop**
```
sum = 0
for i = 1 to n
    sum = sum + i
```

**Algorithm B — 两个 loop（nested）**
```
sum = 0
for i = 1 to n {
    for j = 1 to i
        sum = sum + 1
}
```

**Algorithm C — 直接用公式**
```
sum = n * (n + 1) / 2
```

### 4.1 数 operations（Slide 30–32，忽略 loop 本身的开销）

**Algorithm A**

- Assignments：1（`sum = 0`）+ n（每次 loop 的 `sum = ...`）
- Additions：n
- **Total = (1 + n) + n = 2n + 1**

**Algorithm B** — 关键是 inner loop 总共跑几次

| i | inner loop 跑几次（j = 1..i） |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| … | … |
| n | n |

Inner loop 总次数 = 1 + 2 + … + n = **n(n+1)/2**。每次 inner loop 做 1 个 assignment + 1 个 addition。

- Assignments = 1 + n(n+1)/2
- Additions = n(n+1)/2
- **Total = 1 + n(n+1) = n² + n + 1**

**Algorithm C**

- 1 个 assignment + 1 个 `*` + 1 个 `+` + 1 个 `/` = **4**（和 n 无关）

### 4.2 结果对比

| | f(n) | n = 10 | n = 100 | n = 1000 | Big-O |
|---|---|---|---|---|---|
| A | 2n + 1 | 21 | 201 | 2,001 | **O(n)** |
| B | n² + n + 1 | 111 | 10,101 | 1,001,001 | **O(n²)** |
| C | 4 | 4 | 4 | 4 | **O(1)** |

**n 加倍时会怎样？** A 的 operations 大约 ×2；B 大约 ×4；C 不变。

> Slide 33/34 的意思：不用知道每个 operation 多少秒，只要看"函数值随 n 增加多少倍"，就知道时间大概增加多少倍。

---

## 5. Space Complexity（Slide 35–39）

### 5.1 Time 和 Space 的分析对象不一样

| | 分析什么 |
|---|---|
| Time | 一个 algorithm 在 **某个 data structure 上** 操作要多久 |
| Space | 通常是 **data structure 本身** 要用多少 memory |

（Slide 37。分析方法（asymptotic）是一样的。）

### 5.2 Overhead

Data structure 的目的是"有效率地存和取 data"。为了 **快速找到 data**，常常需要多存一些额外信息，这些额外的东西叫 **overhead**。

**例子**：Linked list 的每个 node 除了存 data，还要存一个 **指向下一个 node 的 pointer（reference）**。

```
Array（存 4 个 int）:           [ 5 ][ 8 ][ 2 ][ 9 ]          只有 data

Linked list（存 4 个 int）:     [5|→] → [8|→] → [2|→] → [9|null]
                                  ↑ 每个 node 多了一个 pointer = overhead
```

- 理想：overhead **越小越好**，同时保持快速访问
- 要在 "省 memory" 和 "访问快" 之间取平衡，这就是 data structure 有趣的地方（Slide 39）

---

## 6. Space/Time Tradeoff（Slide 40–50）

> **原则：常常可以 "用多一点 space 换 time"，或者 "用多一点 time 换 space"。**

### 6.1 Packing / Unpacking

- 把 data **压缩 / 编码**（packing）→ 省 space，但要用的时候要 **解码**（unpacking）→ 多花 time。
- 反过来：**预先存好结果** → 省 time，但多花 space。

### 6.2 Lookup Table（Slide 42–44）

**Lookup table = 把"一个函数的答案"预先算好存起来，要用时直接查。**

**例子：阶乘（factorial）**

- `12! = 479,001,600` 可以放进 32-bit `int`（max = 2,147,483,647）
- `13! = 6,227,020,800` **超过** int 的最大值 → 放不下

所以只需要存 **13 个值**（0! 到 12!）：

```java
static final int[] FACT = new int[13];
static {
    FACT[0] = 1;
    for (int i = 1; i <= 12; i++) FACT[i] = FACT[i - 1] * i;
}
// 需要 n! (n ≤ 12) 时：直接 FACT[n]   → O(1)，不用重新算
```

- **省了 time**（不用重算），**花了一点 space**（13 个 int）。

**Sine / Cosine**：也可以把每 1 度的答案存起来，用最接近的度数去查，得到近似值。

> ⚠️ **注意（Slide 44）**：建 table 本身要花时间。要 **常常用** 这个 table，才值得。如果只用一两次，反而亏。

### 6.3 "Binary sort" 例子（Slide 45–48）

**前提**：A 是 0 到 n−1 的一个 permutation（打乱顺序的 0, 1, 2, …, n−1）。

**版本 1：用两个 array（快，但多花 space）**

```java
for (i = 0; i < n; i++)
    B[A[i]] = A[i];
```

把每个 value 放到 B 里 "**位置 = 自己的值**" 的地方。

Trace：A = [2, 0, 1]

| i | A[i] | 动作 | B |
|---|---|---|---|
| 0 | 2 | B[2] = 2 | [_, _, 2] |
| 1 | 0 | B[0] = 0 | [0, _, 2] |
| 2 | 1 | B[1] = 1 | [0, 1, 2] ✅ |

需要 **两个** size n 的 array（A 和 B）。

**版本 2：in-place（只用一个 array，省 space，但花多点 time）**

```java
for (i = 0; i < n; i++)
    while (A[i] != i)              // 位置 i 上的数字不对
        swap(A, i, A[i]);          // 把它交换到它应该去的位置 A[i]
```

Trace：A = [2, 0, 3, 1]

| 步骤 | 动作 | A |
|---|---|---|
| i=0, A[0]=2 ≠ 0 | swap(A, 0, 2) | [3, 0, 2, 1] |
| A[0]=3 ≠ 0 | swap(A, 0, 3) | [1, 0, 2, 3] |
| A[0]=1 ≠ 0 | swap(A, 0, 1) | [0, 1, 2, 3] |
| A[0]=0 ✅ | i = 1, 2, 3 都已经正确 | **[0, 1, 2, 3]** |

**对比：**

| | 版本 1 | 版本 2 (in-place) |
|---|---|---|
| 额外 array | 需要 B（多 n 格） | **不需要** |
| Space | 两个 array | 一个 array（约一半） |
| Time | 比较快 | 大约慢 2 倍（Slide 48） |

> **In place** = 直接在原本的 array 里改，不需要额外的大 array。
> 两个版本的时间都还是 O(n)，只是常数不同（每次 swap 至少会放好一个 element）。

### 6.4 Disk-based tradeoff：几乎"反过来"（Slide 49–50）

**Main memory 的原则**：多用 space → 可能更快（例如 lookup table）。

**Disk 的原则**：**存储需求越小，program 反而越快。**

原因：**从 disk 读数据比 CPU 计算慢太多太多了**。就算要多花时间去解压缩，也比 "多读 disk" 便宜。

**类比**：从很远的仓库搬货。把货压缩打包成小箱子搬过来（路程慢，但只搬一趟），到了再拆开，比搬一大堆没压缩的货（要来回很多趟）快。

> Slide 也说了：这个原则 "不是 100% 都成立"，只是设计 disk-based program 时要记住的方向。

---

## 7. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Time complexity | 数 elementary steps，通常看 worst case |
| Space complexity | 看数据占的 memory（不是 code 长度） |
| Empirical 缺点 | system load、language、compiler、programmer bias、code tuning、有限 input |
| Primitive operations | assign、arithmetic、compare、array access、method call、return… |
| 1+2+…+n | n(n+1)/2 |
| A / B / C | 2n+1 (O(n)) / n²+n+1 (O(n²)) / 4 (O(1)) |
| Overhead | 为了访问方便而额外存的信息（例如 linked list 的 pointer） |
| Space/Time tradeoff | 多 space ↔ 少 time |
| Lookup table | 预先存答案；要常用才值得；12! 是 int 的极限 |
| In-place | 不用额外大 array，省 space 但更慢 |
| Disk tradeoff | 存得越小越快（反过来） |

---

## 8. 练习

### A. MCQ

**A1.** 通常分析 time complexity 用哪个 case？
a) Best　b) Average　c) Worst　d) 随便

**A2.** 下面哪个 **不是** primitive operation？
a) `x = 5`　b) `A[i]`　c) `a + b`　d) 把整个 array 排序

**A3.** Algorithm C（`sum = n*(n+1)/2`）的 time complexity？
a) O(n)　b) O(n²)　c) O(1)　d) O(log n)

**A4.** 为什么 factorial 的 lookup table 只存到 12!？
a) 13! 是负数　b) 13! 超过 32-bit int 的范围　c) 数学上没有 13!　d) 12 是 slide 随便选的

**A5.** Disk-based space/time tradeoff 说什么？
a) 存得越大越快　b) 存得越小越快　c) 没关系　d) 只有 SSD 才适用

### B. Short answer

**B1.** 列出 empirical analysis 的 3 个缺点。

**B2.** 什么是 overhead？举一个 data structure 的例子。

**B3.** 用一个例子解释 space/time tradeoff。

### C. Calculation

**C1.** Algorithm B，n = 20 时 total operations 是多少？

**C2.** 数下面 code 的 operations（assignments + additions），写出 f(n) 和 Big-O，再算 n = 10：
```
sum = 0
for i = 1 to n
    for j = 1 to n
        sum = sum + 1
```

**C3.** 把 n 从 1000 加倍到 2000，Algorithm A、B、C 的 operations 大约各变成原来的几倍？

### D. Thinking

**D1.** 为什么 disk-based 的 tradeoff 和 memory-based 的几乎相反？

**D2.** Lookup table 什么情况下 **不值得** 用？

---

### 答案

**A1: c**　**A2: d**　**A3: c**　**A4: b**　**A5: b**

**B1.** 任选三个：(1) 受 system load / language / compiler 影响；(2) 有 programmer bias / code tuning；(3) 只能测有限的 input；(4) 必须先完整 implement；(5) 必须在同样的 hardware / software 才能比。

**B2.** Overhead = 除了实际 data 以外，为了方便访问而额外存的信息。例子：linked list 每个 node 要多存一个指向下一个 node 的 pointer。

**B3.** Factorial lookup table：预先算好 0! 到 12! 存进 array（多花 13 个 int 的 space），之后每次要 n! 直接查，O(1)，省了重复计算的时间。这是 **用 space 换 time**。（反过来，把 data 压缩存 = 省 space，但读的时候要解压 = 多花 time。）

**C1.** n² + n + 1 = 400 + 20 + 1 = **421**。

**C2.**
- Assignments = 1 + n²（inner loop 一共跑 n × n 次，每次 1 个 assignment）
- Additions = n²
- **f(n) = 2n² + 1**，**O(n²)**
- n = 10：2(100) + 1 = **201**

**C3.**
- A：2001 → 4001 ≈ **×2**
- B：1,001,001 → 4,002,001 ≈ **×4**
- C：4 → 4，**×1**（不变）

**D1.** 因为 disk 读写比 CPU 计算慢太多。数据越小，要读的 disk 越少；就算多花 CPU 时间解压缩，总时间还是比多读 disk 短。

**D2.** (1) 很少用到，建 table 的时间比省下来的还多；(2) table 太大，memory 放不下；(3) 函数很便宜，重算比查表还快。

---

## 9. 和后面章节的连接

- Ch5：把 "2n + 1 → O(n)"、"n² + n + 1 → O(n²)" 的"丢掉低阶项和常数"变成正式定义（O、Ω、Θ）
- Ch7：array vs linked list 就是 space/time tradeoff（array 省 overhead，linked list 灵活）
- Ch6：HashSet 的 load factor 也是 space/time tradeoff
