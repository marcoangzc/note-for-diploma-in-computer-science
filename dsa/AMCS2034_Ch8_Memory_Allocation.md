# AMCS2034 — Chapter 8: Static and Dynamic Memory Allocation

> 这章的 slide 有几处 **前后矛盾 / 不太准确**（尤其是 Slide 24、31、34、35），而且 Slide 12–15 的 "problem" 只有 A、B、C 三个格子，没讲结论。
> 这份 note 先讲 **正确的大图**，然后再对应回 slide，标出哪里会让人迷惑。

---

## 0. 这章一句话总览

> 程序里的变量，会被放在 memory 的 **三个地方** 之一：
> **Static 区**（一直都在）、**Stack**（method 用的，自动来自动走）、**Heap**（`new` 出来的，要靠 GC 清）。
> 放哪里，取决于 **"大小 / 存活多久" 能不能在 compile 时决定**。

| | Static | Stack | Heap |
|---|---|---|---|
| 放什么 | 全局变量、`static` 变量 | Method 的 local 变量、参数 | 用 `new` 创建的 object / array |
| 什么时候分配 | **程序开始前**（compile time 决定） | **Method 被调用时**（runtime） | **执行 `new` 时**（runtime） |
| 什么时候释放 | 程序结束 | **Method 结束时自动释放** | 没人用它时（Java：garbage collector） |
| 大小 | 固定 | 每个 frame 的大小在 compile time 已知 | 可以在 runtime 才决定，也能变 |

---

## 1. Memory 是什么？（Slide 4–5）

**类比**：Memory 是一张 **超大的方格纸**，每一格是 1 个 byte，每格都有 **地址（address）**（1, 2, 3, …）。

- 你写 `int var = 5;`，电脑找一块空的格子，在小本子上记下 "`var` = 这个地址"。
- 之后你写 `var`，电脑就去那个地址读 / 写。
- 电脑靠 **stack pointer** 记住"已用 memory 的尾巴在哪里"，下一块空的从那里开始（Slide 5）。

**重点**：程序里的代码 **不记得变量名字，只记得地址**。这个观念是理解下面 "Problem" 的关键。

---

## 2. Memory allocation 和 Binding（Slide 6–7, 16）

- **Memory management**：管理 memory 的分配（allocation）和释放（deallocation）。OS 的重要功能之一。
- **Memory binding**：把 "变量" 和 "memory 地址" **绑在一起**。
- **Binding time**：什么时候绑。

| 类型 | Binding 发生在 | 意思 |
|---|---|---|
| **Static** allocation | **Compile time**（编译时） | 地址 / 大小在程序跑之前就定了 |
| **Dynamic** allocation | **Runtime**（执行时） | 程序跑的时候才决定，可以建立和销毁 |

---

## 3. Slide 12–15 的 "Problem"：为什么大小要固定？

Slide 用 A、B、C 三个变量讲了一个故事，但没说结论。这里完整讲一遍。

**情况**：一个 function 有 3 个变量：A（1 byte）、B（**大小会变**）、C（1 byte）。B 声明在 A 和 C 中间。

```
地址:     1     2     3     4     5     6
        ┌─────┬─────┬─────┬─────┬─────┬─────┐
初始:   │  A  │  B  │  C  │     │     │     │
        └─────┴─────┴─────┴─────┴─────┴─────┘

B 变大成 4 bytes → C 被挤走，搬到地址 6：

        ┌─────┬─────┬─────┬─────┬─────┬─────┐
之后:   │  A  │  B  │  B  │  B  │  B  │  C  │
        └─────┴─────┴─────┴─────┴─────┴─────┘
```

**问题**：Compiled 好的 code 只记得 **"C 在地址 3"**。C 搬走后，code 下次写 C 时，还是去写地址 3 —— 那里现在是 **B 的一部分**，B 的数据就被 **覆盖** 了！

**Slide 15 的结论**：所以变量的 **大小必须固定，而且在 compile time 就知道**。

**那要放"大小会变"的东西（例如会变大的 list）怎么办？** 答案：**放到 Heap**，而 stack 上只放一个 **固定大小的 reference（地址）** 指向它：

```
Stack（固定大小的格子）           Heap（可以任意大小、可以变）
┌───────────────┐
│ list ●────────┼──────────►  [ 10 | 20 | 30 | 40 | 50 | ... ]
└───────────────┘
   reference（固定 4 或 8 bytes）
```

`ArrayList` 满了要变大时：Java 在 heap **另外开一块更大的 array**，把东西复制过去，然后让 stack 上的 reference **改指向新的 array**。stack 上的 reference 大小不变，所以不会破坏其他变量。

---

## 4. 三种 Allocation

### 4.1 Static allocation（Slide 17–20）

- 在 **compile 时** 就决定地址和大小；**整个程序期间一直存在**
- **程序开始（`main` 之前）就分配好并初始化**
- 会用到 static allocation 的：
  - **全局变量**
  - 明确声明 `static` 的 **local 变量**
- Static local 变量 **不会** 每次调用 function 时重新初始化

```java
static int count = 0;      // 整个程序都在，只初始化一次
```

优点：简单。缺点：**永远占着 memory**（就算后来没用到了），也不能重用。

### 4.2 Stack allocation（Slide 9, 21–24）

- 用于 **non-static 的 local 变量** 和 **pass by value 的参数**
- **大小** 在 compile time 已知，但 **地址** 要看 method 什么时候被调用，所以在 runtime 才分配
- **每次 call method → stack 上多一个 block（叫 frame）**；method 结束 → 这个 frame **被移除**
- **LIFO**：最后 call 的 method 最先结束

**为什么要 stack？**（Slide 21）：Method A call method B 时，A 的状态要先"存起来"，B 结束后才能回到 A 继续。Stack 刚好满足这个需求。

**Trace：`main` → `foo` → `bar`**

```
main 调用 foo，foo 调用 bar：

   │ bar 的 frame  │ ← top（最新）
   │ foo 的 frame  │
   │ main 的 frame │
   └───────────────┘

bar 结束 → bar 的 frame 被移除
foo 结束 → foo 的 frame 被移除
```

优点：**分配 / 释放很快**（只是移动 stack pointer）、自动管理。
限制：Stack **有大小限制**。**无限 recursion** 会把 stack 塞满 → `StackOverflowError`。

### 4.3 Dynamic (Heap) allocation（Slide 26–33）

- 在 **runtime** 才分配（Java 用 `new`，C 用 `malloc`）
- **不依赖 method 的 call / return**，method 结束了，heap 里的东西 **仍然可以存在**
- 大小、地址、内容都可以在 runtime 变化 → 出问题时 **比较难 debug**（Slide 28）
- 比 stack 慢一点，也复杂一点（要管理哪些空间是空的）

**什么时候放 heap？**（Slide 31）：**数据需要比 method 活得更久** 的时候，或者 **大小在 runtime 才知道** 的时候。

**Java Heap 的 Garbage Collection（Slide 30–33）：**

- Heap 满了 → **Garbage collector（GC）** 出动，把 **没人再用的 object** 删掉，腾出空间
- Heap 分成两个区：**Young space（nursery）** 放新 object；**Old space** 放活得久的
- 大部分 object 很快就没用了（短命）→ 只清 young space，比较快

**Explicit vs Implicit allocator（Slide 29）：**

| | Explicit | Implicit |
|---|---|---|
| 谁 free？ | **程序员自己** free | 系统自动（garbage collection） |
| 例子 | C：`malloc / free`；C++：`new / delete` | **Java**、ML、Lisp |

---

## 5. Java 里每个变量到底放哪？（把整章串起来）

```java
public class Demo {
    static int count = 0;                    // ① Static 区

    public static void main(String[] args) {
        int x = 10;                          // ② Stack（primitive，值直接放 stack）
        Student s = new Student("Ali");      // ③ s 是 reference → Stack
                                             //    Student object → Heap
        int[] arr = new int[3];              // ④ arr 是 reference → Stack
                                             //    array 本身 → Heap
        foo(x);
    }

    static void foo(int n) {                 // ⑤ 调用 foo → stack 新增一个 frame（放 n、y）
        int y = n * 2;
    }                                        //    foo 结束 → frame 被移除，n、y 消失
}
```

图：

```
  Static 区          Stack（main 的 frame）             Heap
┌───────────┐       ┌───────────────────┐      ┌──────────────────────┐
│ count = 0 │       │ x   = 10          │      │  Student object      │
└───────────┘       │ s   = ●───────────┼────► │  (name = "Ali")      │
                    │ arr = ●───────────┼──┐   ├──────────────────────┤
                    └───────────────────┘  └─►  │  int[3] = [0, 0, 0]  │
                                                └──────────────────────┘
```

**一句话记法：**
- **Primitive local 变量** → Stack
- **Object / array** → **Heap**；指向它的 **reference 变量** → Stack
- **`static` 变量** → Static 区

> 当 `main` 结束，stack 上的 `s`、`arr` 消失 → heap 里的 Student 和 array 没有人指向它们了 → 变成"垃圾"，之后被 GC 回收。

---

## 6. Slide 27 的例子：三个 program unit A、B、C

**Static allocation**：A、B、C **全部** 一开始就分配好，整个程序期间都占着 memory。

**Dynamic allocation**：只有 **active（正在用）** 的 unit 才有 memory。

| 阶段 | 发生什么 | Static 时 memory 里有 | Dynamic 时 memory 里有 |
|---|---|---|---|
| 1 | 程序开始，只有 A active | A, B, C | **A** |
| 2 | A call B | A, B, C | **A, B** |
| 3 | B return，回到 A | A, B, C | **A** |
| 4 | A call C | A, B, C | **A, C** |

→ Dynamic 更省 memory，而且 B 用完的空间可以给 C 重用（Slide 35 的 "memory reusability"）。

---

## 7. ⚠️ Slide 里容易让人误会的地方

下面这些是 slide 里的说法，和真实的 Java 行为 **不完全一致**。**考试时如果题目直接问 slide 的内容，按 slide 答；但自己要知道真相。**

| Slide | Slide 的说法 | 更准确的理解 |
|---|---|---|
| **24** | Stack 上的 "objects" 只有那个 function 能访问、function 结束就消失 | 在 Java，**stack 上放的是 primitive 和 reference**；object 本身在 **heap**。Object 不会因为 method 结束就立刻消失，只是当没人 reference 它时才会被 GC 回收 |
| **31** | "Java stack 的 memory 在 program **compile** 的时候分配" | Stack frame 是 **method 被调用时（runtime）** 才创建的。只有"每个 frame 要多大"在 compile time 已知（Slide 21 说得对） |
| **34** | Heap："需要自己 free"；"没有 size limit" | 自己 free 是 **C / C++**。**Java 有 GC 自动回收**。另外 heap 也有上限（受 RAM 和 JVM 设定限制），满了会 `OutOfMemoryError` |
| **34** | "Heap 容易 memory leak" | 对。在 Java 里的 leak 是：**object 已经没用，但仍然被某处 reference 着**（例如一个 static list 一直往里加、从不移除），所以 GC 不能回收 |
| **35** | Static allocation "用 stack 实现"；static "less efficient"，dynamic "more efficient" | Static 变量放在 **static 区**，不是 stack。Stack 是另外一种（automatic）分配。所谓 efficient 指的是 **memory 使用**：static 永远占着，dynamic 用完可以重用 |
| **9** | Stack "can pass values to called procedures, but not up to callers" | 因为 method 结束后 frame 就没了，所以 **不能返回指向 local 变量的地址**。要传东西回给 caller 用 `return`，或把 object 放 heap |

---

## 8. Stack vs Heap 总结（改良过的 Slide 34 版本）

| | Stack | Heap |
|---|---|---|
| 存什么 | Local primitive、reference、参数 | Object、array |
| 谁管理 | **自动**（method 进出） | Java：**GC** 自动；C：程序员 |
| 速度 | 快 | 较慢 |
| 大小限制 | 有（较小）→ `StackOverflowError` | 有（较大）→ `OutOfMemoryError` |
| 生命周期 | 只在 method 期间 | 只要还有 reference 指向它 |
| 谁可以访问 | 只有该 method（该 thread 的 frame） | 任何持有 reference 的地方 |
| 常见问题 | 无限 recursion | Memory leak、GC 停顿 |

---

## 9. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Binding | 变量 ↔ 地址 的绑定；binding time = 何时绑 |
| Static allocation | Compile time；程序开始前就分配；一直存在 |
| Stack allocation | Method 被调用时分配一个 frame；结束就移除；LIFO |
| Heap allocation | Runtime、`new`；不依赖 method；由 GC 清理（Java） |
| 为什么变量大小要固定 | 变大会挤走后面的变量，而 code 只记得地址 → 覆盖其他数据 |
| 变大的东西怎么办 | 放 heap，stack 上放固定大小的 reference |
| Explicit vs Implicit | 自己 free vs GC 自动 |
| Young / Old space | 新 object / 活得久的 object |

---

## 10. 练习

### A. MCQ

**A1.** Java 里 `Student s = new Student();` 中，Student object 存在哪里？
a) Stack　b) Heap　c) Static 区　d) Register

**A2.** 哪种 memory 会在 method 结束时 **自动释放** frame？
a) Heap　b) Static　c) Stack　d) Disk

**A3.** Static memory allocation 的 binding 发生在？
a) Runtime　b) Compile time　c) Method 结束时　d) GC 时

**A4.** Java 里由谁回收 heap 中不再使用的 object？
a) 程序员用 `free()`　b) Garbage collector　c) Compiler　d) Stack pointer

**A5.** 无限 recursion 最可能造成什么？
a) OutOfMemoryError　b) StackOverflowError　c) NullPointerException　d) 没事

### B. Short answer

**B1.** 解释 Slide 12–15 的 problem：为什么"大小会变的变量"放在 stack 中间会出问题？

**B2.** 列出 Stack 和 Heap 的 3 个差别。

**B3.** 什么是 explicit 和 implicit memory allocator？各举一个语言例子。

### C. Trace

**C1.** 说出下面每个变量放在哪里：
```java
static int total = 0;
void f() {
    int a = 3;
    String s = new String("hi");
    int[] b = new int[5];
}
```

**C2.** `main` 调用 `fact(3)`，`fact(n)` 在 `n > 1` 时调用 `fact(n-1)`，`fact(1)` 直接 return。stack 最深时有几个 frame？

**C3.** 程序有 unit A、B、C：A 先运行，A call B，B return，A call C。分别在 static 和 dynamic allocation 下，这 4 个阶段 memory 里有哪些 unit？

### D. Thinking

**D1.** 为什么不把所有变量都放在 stack 上就好？

**D2.** Java 有 garbage collector，还会有 memory leak 吗？

---

### 答案

**A1: b**　**A2: c**　**A3: b**　**A4: b**　**A5: b**

**B1.** 如果 B 在 A 和 C 中间变大，后面的 C 会被挤到别的地址；但 compiled code 只记得 C 的旧地址，之后仍然会写旧地址，结果覆盖到 B 的数据。所以变量的大小必须固定、在 compile time 就知道。变大的数据要放 heap，stack 上放一个固定大小的 reference。

**B2.** 任选三个：(1) Stack 自动管理，heap 由 GC（或程序员）管理；(2) Stack 放 local primitive / reference，heap 放 object / array；(3) Stack 很快、较小，heap 较慢、较大；(4) Stack 的东西 method 结束就没了，heap 只要还有 reference 就活着；(5) Stack 溢出 = StackOverflowError，heap 满 = OutOfMemoryError。

**B3.** Explicit：程序员自己分配和释放（C 的 `malloc/free`，C++ 的 `new/delete`）。Implicit：程序员只分配，系统自动回收（Java 的 garbage collection）。

**C1.**
- `total`：**Static 区**
- `a`：**Stack**（f 的 frame）
- `s`：**reference 在 Stack**，`String` object 在 **Heap**
- `b`：**reference 在 Stack**，`int[5]` array 在 **Heap**

**C2.** 最深时：`main`、`fact(3)`、`fact(2)`、`fact(1)` = **4 个 frame**。

**C3.**

| 阶段 | Static | Dynamic |
|---|---|---|
| 1 A active | A, B, C | A |
| 2 A call B | A, B, C | A, B |
| 3 B return | A, B, C | A |
| 4 A call C | A, B, C | A, C |

**D1.** Stack 上的东西 method 一结束就消失，所以不能存"要比 method 活得久"的数据；而且 stack frame 的大小要在 compile time 固定，不能放"runtime 才知道大小 / 会变大"的东西（例如会增长的 list）；stack 也比较小。

**D2.** 会。GC 只回收 **没人 reference** 的 object。如果一个 object 已经没用了，但还被某个地方（例如一个不断增长的 static list）reference 着，GC 就不会回收它，memory 会越用越多，最后 `OutOfMemoryError`。

---

## 11. 和后面章节的连接

- Ch2：Recursion 每 call 一次就多一个 stack frame（fib 的 call tree）
- Ch7：Array 的大小固定（static）；linked list 的 node 用 `new` 在 heap 建立（dynamic）
- Ch7：Stack data structure 和 call stack 是同一个 LIFO 概念
- Ch9：DFS 的 recursion 深度太大也会 StackOverflow
