# AMCS2034 — Chapter 1: Basic Terminology (Elementary Data Organization)

> 这份 note 专门补 slide 讲得太简单 / 没解释的地方。
> 格式：**概念讲解 → Slide 容易误会的地方 → Cheat sheet → 练习（MCQ / Short / Trace / Thinking，全部有答案）**

---

## 0. 这章一句话总览

Chapter 1 其实只讲三件事：

1. **数据怎么分层描述**：Data → Field → Record → File
2. **Data structure 和 Algorithm 是什么**（两个不同的东西）
3. **怎么用 pseudo-code 写 algorithm**

---

## 1. 为什么要学 DSA？（Slide 4–6）

Slide 说有三个问题：Data Search、Processor Speed、Multiple Requests。翻译成人话：

| 问题 | 人话 |
|---|---|
| Data Search | 数据越多，一个一个找就越慢 |
| Processor Speed | CPU 再快，遇到 10 亿笔 data 也顶不住 |
| Multiple Requests | 很多用户同时搜，server 会被拖垮 |

**类比**：图书馆有 100 万本书。

- 书乱乱放 → 找一本要翻最多 **1,000,000** 本
- 书按类别 / 编号排好，再用"对半找"（后面 Ch5 的 binary search）→ 最多约 **20** 次（因为 2²⁰ ≈ 100 万）

Data structure = 把数据 **排好的方式**，让你不用每次都全部翻一遍。

---

## 2. Terminology：用一个例子全部串起来

Slide 给了 9 个词但没有例子，所以很难记。用一个 **学生 table** 就全部懂：

| StudentID | Name (First + Last) | CGPA |
|---|---|---|
| 2401 | Ali Ahmad | 3.50 |
| 2402 | Mei Ling | 3.80 |
| 2403 | Raj Kumar | 3.20 |

| 术语 | 定义（简化） | 在这个 table 里是 |
|---|---|---|
| **Data** | 值（values） | `2401`, `"Ali"`, `3.50` 这些 |
| **Data item** | 单一个值 | `3.50` |
| **Group item** | 可以再拆开的 data item | `Name`（可以拆成 First + Last） |
| **Elementary item** | 不能再拆的 data item | `StudentID`, `CGPA` |
| **Entity** | 一个有 attributes 的"东西" | 一位 student |
| **Attribute** | entity 的属性 | ID、Name、CGPA |
| **Entity set** | 同类 entity 的集合 | 所有 student |
| **Field** | 代表某个 attribute 的最小单位 | 某一格，例如 `CGPA` 那一栏的 `3.50` |
| **Record** | 一个 entity 的所有 field 值 | 一整行（2401, Ali Ahmad, 3.50） |
| **File** | 一个 entity set 的所有 records | 整个 table |

### 层级图（记这个就好）

```
File            = 整个 table（所有 student）
 └─ Record      = 一行（一个 student）
     └─ Field   = 一格（ID / Name / CGPA 其中一个）
         └─ Data item / value = 格子里面的值（3.50）
```

### ⚠️ 容易混淆的地方

- **Data vs Data item**：Data 是"很多个值"的统称，Data item 是"单一个值"。
- **Field vs Data item**：Field 强调这个值 **代表哪个 attribute**（属于哪一栏），Data item 只是一个值。
- **Group item vs Elementary item**：问自己"这个还可以再拆吗？" 可以 → Group；不可以 → Elementary。
- Slide 定义 Field 是 "single **elementary** unit"，所以严格来说 `Name`（group item）不是 field，`First name` 才是。但平常大家都会说 "Name field"，考试如果问定义就照 slide。

---

## 3. Primitive vs Non-primitive data types（Slide 11–12）

| | Primitive | Non-primitive |
|---|---|---|
| 是什么 | 语言 / 机器 **直接支持** 的最基本类型，一个变量存一个简单值 | 用 primitive **组合** 出来的类型，可以存很多个值 |
| Java 例子 | `int`, `double`, `float`, `char`, `boolean`（还有 `byte`, `short`, `long`） | Array, Class（例如 `String`, `Student`） |

### ⚠️ Slide 的说法有点怪

- Slide 说 non-primitive "do not allow any specific instructions to be performed directly"，这句很难懂。**实用的记法**：primitive = 一个简单的值；non-primitive = 由多个值 / 对象组成。
- Slide 列了 **Structures, Unions**，这是 **C / C++** 的名字。**Java 没有 struct / union**，用 class。
- 常见错误：`String` **不是** primitive，它是 class（所以是 non-primitive）。

---

## 4. Data structure vs Algorithm

| | Data structure | Algorithm |
|---|---|---|
| 是什么 | 数据在 memory / disk 里 **怎么排** | 对数据 **怎么处理** 的步骤 |
| 类比（厨房） | 架子、抽屉怎么放材料 | 食谱（做菜步骤） |
| 例子 | Array, Linked list, Stack, Queue, Tree, Hash table | Searching, Sorting |

两个是搭配的：**排得好（DS）+ 步骤好（Algo）= 程序快**。

### Linear vs Non-linear

- **Linear**：数据排成一条线，每个 element 前面 / 后面最多接一个 → Array, Linked list, Stack, Queue
- **Non-linear**：数据是 **层级 / 网络** 的形状，一个 element 可以接很多个 → Tree, Graph

（Ch7 会详细讲）

### 六个 Data structure operations（Slide 22–23）

| Operation | 做什么 | 例子 |
|---|---|---|
| Traversing | 每个 element 访问 **一次** | 印出全部学生名字 |
| Searching | 找某个 element 的位置 | 找 ID = 2402 的学生 |
| Insertion | 加新 element | 新学生注册 |
| Deletion | 删除 element | 学生退学 |
| Sorting | 按顺序排（ascending / descending） | 按 CGPA 排名 |
| Merging | 把两个 structure 合并 | 合并 A 班和 B 班名单 |

---

## 5. Algorithm

**Algorithm = Input + Process + Output**

（一组有限的步骤，把 input 变成 output）

### Characteristics — 用人话解释（Slide 27）

| 特点 | 意思 | 反例 |
|---|---|---|
| Unambiguous | 每一步只有 **一种** 意思 | "把差不多大的数字拿出来"（差不多是多少？） |
| Input | **0 个或以上** 的 input | （产生随机数的 algorithm 可以 0 input） |
| Output | **至少 1 个** output | 没有 output 的话做了也没意义 |
| Finiteness | **一定会停** | `while (true) { ... }` 永远不停 → 不是 algorithm |
| Feasibility | 用现有资源做得到 | 需要 100 万年的计算 |
| Independent | 不依赖某个 programming language | 写成 "用 Java 的 `ArrayList`..." |

### Algorithm vs Program

- **Algorithm** = 想法 / 步骤（不依赖语言）
- **Program** = algorithm 用某个 language 写出来的 **实例**

### Good algorithm 的条件（Slide 28）

Correct、Finite、Terminate、Unambiguous、Space & Time efficient。

### 例子：找 a, b, c 最大值（Slide 29）

```
Let max = a
If b > max then max = b
If c > max then max = c
Display max
```

**Trace**（a, b, c）= (3, 9, 5)：

| 步骤 | max |
|---|---|
| max = a | 3 |
| b(9) > 3 ? yes → max = b | 9 |
| c(5) > 9 ? no | 9 |
| Display | **9** |

Slide 说 "Order is very important"：如果你把 `Let max = a` 放到最后，就会把前面找到的答案覆盖掉，结果是错的。

---

## 6. Pseudo-code

### 为什么要 pseudo-code？（Slide 31）

- Natural language（英文 / 中文）→ **太含糊**（ambiguous）
- Programming language → **太绑语言**，algorithm 应该 language independent
- Pseudo-code = 两者之间的 **平衡**：像代码一样清楚，但不用管语法

### 组件 + Slide 里那些没有答案的问题

**① Assignment：用 `←`，不是 `=`**

- `←` 是 assignment（相当于 Java 的 `=`）
- `=` 在 pseudo-code 里是 **比较相等**（相当于 Java 的 `==`）
- 这和 Java 刚好 **相反**，很容易写错。

```
Sum ← 0
Sum ← Sum + 5
```
Slide 问 final value of Sum? → **5**

**② Decision（if-then-else）**

```
if marks > 50 then
    print "Congratulation, you are passed!"
else
    print "Sorry, you are failed!"
end if
```
Slide 问 marks = 75？ → 75 > 50 成立 → **"Congratulation, you are passed!"**
（注意：marks = 50 时 `50 > 50` 不成立 → failed）

**③ Pre-condition loop：先检查条件，再执行**

```
while counter < 5 do
    print "Welcome to CS204!"
    counter ← counter + 1
end while
```
- counter = 0 → 印 **5 次**（counter 是 0,1,2,3,4 时都印）
- counter = 7 → 一开始 `7 < 5` 就是 false → **0 次**

```
for counter ← 0; counter < 5; counter ← counter + 2 do
    print "Welcome to CS204!"
end for
```
counter 依次是 0, 2, 4 → 印 **3 次**（下一个是 6，不满足）

**④ Post-condition loop（do-while）：先执行，再检查**

```
do
    print "Welcome to CS204!"
    counter ← counter + 1
while counter < 5
```
Slide 问 counter 一开始是 10？ → 先印 **1 次**，counter 变 11，`11 < 5` false 就停。

> **记法**：`while` 先问再做（可能 0 次）；`do-while` 先做再问（**至少 1 次**）。

**⑤ Method / return**

```
integer sum(integer num1, integer num2)
start
    result ← num1 + num2
    return result
end
```
Slide 40 的版本没有 `return`（少了这行就没把答案送回去），Slide 41 才补上。

**⑥ Array**：`A[i]` 是第 i 格，n 格的 array 是 `A[0]` 到 `A[n-1]`（和 Java 一样从 0 开始）。

### 写 algorithm 的两种风格（Slide 45–47）

- 第一种：`declare three integers a, b & c` 等，什么都写出来
- 第二种：`get values of a & b` → `c ← a + b` → `display c`
- Analysis of algorithm 通常用 **第二种**，因为更短、专注在重点，没有多余的 declaration。

---

## 7. Cheat sheet

| 题型 | 记这个 |
|---|---|
| Field / Record / File | 格 / 行 / 整个 table |
| Group vs Elementary | 可不可以再拆 |
| Linear vs Non-linear | 一条线 vs 层级 / 网络 |
| 6 operations | Traversing, Searching, Insertion, Deletion, Sorting, Merging |
| Algorithm 要求 | 0+ input, **1+ output**, finite, unambiguous, feasible, language independent |
| `←` vs `=` | assign vs compare（和 Java 相反的感觉） |
| `while` vs `do-while` | 可能 0 次 vs 至少 1 次 |

---

## 8. 练习

### A. MCQ

**A1.** 下面哪个是 **group item**？
a) CGPA　b) StudentID　c) Full Name（First + Last）　d) Age

**A2.** "一个 entity set 里所有 entity 的 records 的集合" 叫什么？
a) Field　b) Record　c) File　d) Attribute

**A3.** 下面哪个 **不是** algorithm 的必要特点？
a) Finiteness　b) 至少 1 个 output　c) Unambiguous　d) 必须用 Java 写

**A4.** 一个 do-while loop 的 body 最少会执行几次？
a) 0　b) 1　c) 2　d) 视条件而定

**A5.** 下面哪个是 non-linear data structure？
a) Stack　b) Queue　c) Tree　d) Linked list

**答案：**

- **A1: c**。Full Name 可以再拆成 First + Last。
- **A2: c**。File = records 的集合。
- **A3: d**。Algorithm 要 language independent，不一定用 Java。
- **A4: b**。先执行再检查条件。
- **A5: c**。Tree 是层级结构。

### B. Short answer

**B1.** 用一个例子解释 Field、Record、File 的关系。

**B2.** 为什么写 algorithm 用 pseudo-code，而不是 natural language 或 programming language？

**B3.** 什么是 data structure，和 algorithm 有什么不同？

**答案：**

**B1.** 以学生 table 为例：一个 student 的 CGPA（3.50）是一个 **Field** 的值；一整行（2401, Ali Ahmad, 3.50）是一个 **Record**；所有 student 的 records 合起来是一个 **File**。

**B2.** Natural language 太含糊（ambiguous），同一句话可以有不同意思。Programming language 太依赖某个语言的语法，algorithm 应该 language independent。Pseudo-code 两者兼顾：够清楚，又不绑定语言。

**B3.** Data structure 是数据在 memory / disk 里的排列方式（例如 array、linked list）；algorithm 是处理数据的步骤（例如 searching、sorting）。前者决定"数据放哪里"，后者决定"怎么处理这些数据"。

### C. Trace / Calculation

**C1.** 写出下面 pseudo-code 最后 `Sum` 的值，并列出每次 loop 的变化：

```
Sum ← 0
for i ← 1; i <= 4; i ← i + 1 do
    Sum ← Sum + i
end for
```

**C2.** 下面会印多少次 "Hi"？最后 counter 是多少？

```
counter ← 3
while counter < 10 do
    print "Hi"
    counter ← counter * 2
end while
```

**C3.** 写 pseudo-code：给一个有 n 个数字的 array `A`，找出最大的数字。

**答案：**

**C1.**

| i | Sum（loop 之后） |
|---|---|
| 1 | 1 |
| 2 | 3 |
| 3 | 6 |
| 4 | 10 |

最后 **Sum = 10**。

**C2.** counter 依次是 3 → 6 → 12。3 < 10 印一次，6 < 10 印一次，12 < 10 不成立停下。所以印 **2 次**，最后 **counter = 12**。

**C3.**
```
max ← A[0]
for i ← 1; i < n; i ← i + 1 do
    if A[i] > max then
        max ← A[i]
    end if
end for
return max
```
（这个 algorithm 会做 n − 1 次比较，Ch3 会用到。）

### D. Thinking

**D1.** 电脑越来越快，为什么我们还是要学 data structure / algorithm？

**D2.** 你手机的"联系人"app，哪个是 File、哪个是 Record、哪个是 Field？

**答案：**

**D1.** 因为数据量增长得比 CPU 快，而且 algorithm 好不好带来的差距很大：找 100 万笔数据，一个一个找最多要 100 万次比较，用排好序的结构 + binary search 大约只要 20 次。硬件快 2 倍，比不上 algorithm 从 100 万次变 20 次。

**D2.** 整个联系人列表 = **File**；一个联系人（名字 + 电话 + email）= **Record**；电话号码那一栏 = **Field**。

---

## 9. 和后面章节的连接

- Ch2 的 pseudo-code / algorithm 会用在 Dynamic Programming（Fibonacci）
- Ch3 & Ch4 的 "n − 1 次比较" 就是 C3 那个找最大值的 algorithm
- Ch7 会把 Linear / Non-linear 展开，讲 Array, Linked list, Stack, Queue, Tree, Graph
