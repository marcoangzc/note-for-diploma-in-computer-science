# AMCS2034 — Chapter 2: Algorithms

> 这章的 5 个 topic 其实是 5 件不相关的事：**Iterators、Design Patterns、String Operations、Dynamic Programming、Pattern Matching (regex)**。
> 每个 topic 分开学就不会乱。Slide 最大的问题：Iterator 代码被截断、Fibonacci 代码有 bug、DP 没讲"为什么快"。这份 note 全部补上。

---

## 0. 五个 topic 地图

| Topic | 一句话 |
|---|---|
| Iterators | 一个统一的方法，走过（traverse）任何 collection，不用知道里面怎么存 |
| Design Patterns | 前人整理好的"常见问题 + 标准解法"，Iterator 是其中一个 |
| String Operations | Java 的 String 是 **immutable**，操作它的规则 |
| Dynamic Programming | 把做过的结果 **记下来**，不重复计算 |
| Pattern Matching | 用 regular expression 在文字里找 / 验证 pattern |

---

## 1. Collections（Slide 4–8）

**Collection = 一个装很多 object 的容器（container）。**

Java Collections Framework 有两大类：

| 类别 | 存什么 | 例子 |
|---|---|---|
| **Collection** | 一堆 elements | List, Set, Stack, Queue, PriorityQueue |
| **Map** | key / value 配对 | HashMap, TreeMap |

| Collection 类型 | 特点 |
|---|---|
| Set | **不重复** |
| List | **有顺序**（可以重复） |
| Stack | LIFO（后进先出） |
| Queue | FIFO（先进先出） |
| PriorityQueue | 按 **priority** 出来 |

Slide 说 "To define a data structure is essentially to define a class"：意思是 data structure 在 Java 里就是一个 class，data fields 存数据，methods 负责 search / insert / delete。

---

## 2. Iterators

### 2.1 为什么需要 Iterator？

**类比**：电视遥控器。你只需要按 "下一个频道"，不需要知道频道是存在 array 还是 linked list。

Iterator 的意义：**走过 collection 里所有 element，但不暴露它是怎么存的**（Slide 9）。所以 array、linked list、set 都可以用 **同一套** 方法走。

### 2.2 三个 methods（Slide 11）

| Method | 做什么 |
|---|---|
| `hasNext()` | 还有下一个 element 吗？（true / false） |
| `next()` | 拿下一个 element，并往前移 |
| `remove()` | 删掉 **刚刚 next() 拿到的** 那个 element |

### 2.3 关系图

```
Iterable  ──(定义)──►  iterator()  ──(返回)──►  Iterator
   ▲                                              (hasNext / next / remove)
Collection (extends Iterable)
   ▲
List, Set, Queue ...
```

所以 **每个 Collection 都是 Iterable**，都能拿到 Iterator。

### 2.4 Java 内置 Iterator 用法（含 slide 没有的 remove 例子）

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4));
Iterator<Integer> it = list.iterator();
while (it.hasNext()) {
    int x = it.next();
    if (x % 2 == 0) it.remove();   // 删掉偶数
}
System.out.println(list);          // [1, 3]
```

> `for (int x : list)`（for-each）**背后就是 Iterator**。所以在 for-each 里面用 `list.remove(...)` 会出错（`ConcurrentModificationException`），要删就用 `it.remove()`。（这个是额外知识，但实际写 code 很常遇到。）

### 2.5 Iterator Pattern：Slide 22–26 的完整代码

Slide 的代码被截断了（`NameIterator` 只写了一半），完整版本如下（我已经跑过，输出和 slide 一样）：

```java
// Iterator.java
public interface Iterator {
    public boolean hasNext();
    public Object next();
}

// Container.java
public interface Container {
    public Iterator getIterator();
}

// NameRepository.java
public class NameRepository implements Container {
    public String names[] = {"Robert", "John", "Julie", "Lora"};

    @Override
    public Iterator getIterator() {
        return new NameIterator();
    }

    private class NameIterator implements Iterator {
        int index;                         // 从 0 开始

        @Override
        public boolean hasNext() {
            return index < names.length;   // 还没走完？
        }

        @Override
        public Object next() {
            if (this.hasNext()) {
                return names[index++];     // 先返回，再 index+1
            }
            return null;
        }
    }
}

// IteratorPatternDemo.java
public class IteratorPatternDemo {
    public static void main(String[] args) {
        NameRepository namesRepository = new NameRepository();
        for (Iterator iter = namesRepository.getIterator(); iter.hasNext();) {
            String name = (String) iter.next();
            System.out.println("Name : " + name);
        }
    }
}
```

输出：
```
Name : Robert
Name : John
Name : Julie
Name : Lora
```

**四个角色，谁做什么：**

| 角色 | 做什么 |
|---|---|
| `Iterator` (interface) | 规定 `hasNext()` / `next()` |
| `Container` (interface) | 规定 `getIterator()`，能返回 iterator |
| `NameRepository` | 真正存数据（array），实现 Container |
| `NameIterator`（inner class） | 知道 **怎么走** NameRepository（用 index） |

**重点**：`main` 只跟 `Iterator` 说话，完全不知道里面是 array。如果以后 `names` 改成 linked list，只需要改 `NameIterator`，`main` **不用改**。这就是 pattern 的价值。

> ⚠️ 小陷阱：这里的 `Iterator` 是 slide 自己定义的 interface，不是 `java.util.Iterator`。如果同一个文件 `import java.util.*;` 会撞名。

---

## 3. Design Patterns（Slide 12–21）

**Design pattern = 前人试错很多年，整理出来的"常见问题的标准解法"。**

### 3.1 Gang of Four (GoF)

1994 年四位作者写了《Design Patterns》这本书，所以叫 GoF。他们的两个原则：

| 原则 | 白话 |
|---|---|
| **Program to an interface, not an implementation** | 写 code 时依赖 interface（例如 `List`），不要绑死某个具体 class（例如 `ArrayList`）。要换的时候很容易 |
| **Favor composition over inheritance** | 想扩充功能，优先"把 object 组合起来用"，而不是一直 `extends` |

### 3.2 Design pattern 有什么用（Slide 15–16）

1. **共同语言**：说 "我们用 Singleton" 大家立刻知道是"整个程序只有一个 object"。
2. **Best practice**：新手直接学前人的经验。

### 3.3 三大类（Slide 17–18）

| 类别 | 关心什么 | 例子（额外补充） |
|---|---|---|
| **Creational** | 怎么 **创建** object（隐藏 `new` 的细节） | Singleton, Factory |
| **Structural** | class / object 怎么 **组合** | Adapter, Decorator |
| **Behavioral** | object 之间怎么 **沟通** | **Iterator**, Observer |

**Iterator pattern 属于 Behavioral。**（考试常问。）

---

## 4. String Operations（Slide 27–35）

### 4.1 String 是 object，而且 immutable（Slide 29–30）

**Immutable = 创建了就不能改。** 每次你以为"改了 String"，其实是 **造了一个新 String**。

```java
String s = "Hello";
s.concat(" World");          // 造了新 String，但没人接住它
System.out.println(s);       // Hello   ← 原本的没变！

s = s.concat(" World");      // 用 s 接住新的
System.out.println(s);       // Hello World
```

记住：`concat` **返回** 新 String，一定要把它 assign 回去。

### 4.2 为什么大量修改要用 StringBuilder / StringBuffer？

```java
String result = "";
for (int i = 0; i < 10000; i++) {
    result += i;              // 每次都造新 String，很慢、很浪费 memory
}
```

改用 `StringBuilder`（可以直接改自己，不用每次造新的）：

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10000; i++) sb.append(i);
String result = sb.toString();
```

（`StringBuffer` 和 `StringBuilder` 功能一样，但 `StringBuffer` thread-safe，比较慢。）

### 4.3 其他 slide 内容

| 操作 | 说明 |
|---|---|
| `s.length()` | 返回字符数（accessor method：只读信息，不改 object） |
| `s1.concat(s2)` 或 `s1 + s2` | 接起来，返回新 String |
| `System.out.printf(...)` | 格式化后 **印出来** |
| `String.format(...)` | 格式化后 **返回 String**（可以存起来重复用） |

格式符：`%d` 整数、`%f` 小数、`%s` 字符串。

### 4.4 额外：`==` 和 `equals` 的区别

```java
String x = new String("hi"), y = "hi", z = "hi";
x == y        // false（不同 object）
y == z        // true （literal 共用同一个）
x.equals(y)   // true （内容相同）
```
**比较 String 内容永远用 `equals`。**

---

## 5. Dynamic Programming (DP)

### 5.1 一句话

> **DP = 把算过的结果记下来，下次直接用，不重算。**
> （Slide 45 的故事：1+1+1+1+1+1+1+1 = 8；再加一个 1 → 9，你不用重新数，因为你记得前面是 8。）

### 5.2 Fibonacci：为什么 pure recursion 很慢？

**注意 slide 的定义**：`Fib(0) = 1, Fib(1) = 1`，所以数列是 **1, 1, 2, 3, 5, 8, 13, 21…**
（一般教科书是 0, 1, 1, 2, …，考试按 slide 的来。）

**Pure recursion（Slide 47）**

```java
int fib(int n) {
    if (n < 2) return 1;
    return fib(n - 1) + fib(n - 2);
}
```

**`fib(5)` 的 call tree** — 看有多少重复：

```
                          fib(5)
                    /               \
               fib(4)                fib(3)
              /      \               /     \
          fib(3)     fib(2)      fib(2)    fib(1)
          /    \      /   \       /   \
      fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
      /   \
  fib(1) fib(0)
```

- `fib(3)` 被算了 **2 次**
- `fib(2)` 被算了 **3 次**
- 这些重复 = 浪费

我跑过 code，naive 版本 call 的次数：

| n | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| calls | 3 | 5 | 9 | 15 | 25 | 41 |

每次 n +1，calls 大约乘 1.6 倍 → 时间大约 **O(2ⁿ)** 的规模（指数爆炸）。

### 5.3 DP 版本：每个值只算一次 → O(n)

**Slide 48 的 code 有两个问题：**
1. 用 `i < n` 的话，只填到 `fibresult[n-1]`，**没有** fib(n)；
2. 它没有写 `fibresult` 的大小。

**修正版（bottom-up，从小填到大）：**

```java
int fib(int n) {
    int[] f = new int[n + 1];
    f[0] = 1;
    f[1] = 1;
    for (int i = 2; i <= n; i++) {     // 注意是 <=
        f[i] = f[i - 1] + f[i - 2];
    }
    return f[n];
}
```

填表：

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| f[i] | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 |

**Top-down 版本（recursion + 记忆 = 真正的 memoization）：**

```java
long[] memo = new long[50];
long fib(int n) {
    if (n < 2) return 1;
    if (memo[n] != 0) return memo[n];     // 算过了 → 直接用
    return memo[n] = fib(n - 1) + fib(n - 2);
}
```
`fib(40)` 用 naive 要 3 亿多次 call，memo 版几十次就好。

| | 方向 | 怎么做 |
|---|---|---|
| **Top-down (memoization)** | 从大问题开始 | recursion + 用 array 记住结果 |
| **Bottom-up (tabulation)** | 从小问题开始 | 用 loop 从小填到大 |

Slide 把两种都叫 "memoization"，其实严格来说 bottom-up 叫 tabulation。考试写 memoization 就好，理解这个差别就更稳。

### 5.4 什么问题适合 DP？（Slide 39, 51–52）

需要 **两个条件**：

1. **Overlapping subproblems**：同一个小问题会被重复遇到（例如 fib(2) 出现很多次）
2. **Optimal substructure**：大问题的最优解，可以由小问题的最优解组成

**DP vs Divide & Conquer vs Greedy**

| | 小问题独立吗？ | 特点 |
|---|---|---|
| Divide & Conquer | **独立**（不重复） | 分开解，再合并（例如 merge sort） |
| **Dynamic Programming** | **重叠**（会重复） | 记住小问题结果，追求 **整体最优** |
| Greedy | — | 每一步只选 **眼前最好**（local optimum），不一定整体最优 |

### 5.5 一个 Greedy 失败、DP 成功的例子（帮你理解 Slide 40）

硬币 `{1, 3, 4}`，凑 **6** 块，最少要几个硬币？

- **Greedy**（每次拿最大的）：4 + 1 + 1 = **3 个**
- **DP**：3 + 3 = **2 个** ✅

DP 表（`dp[x]` = 凑 x 最少几个硬币）：

| x | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| dp[x] | 0 | 1 | 2 | 1 | 1 | 2 | **2** |

`dp[6] = min(dp[5]+1, dp[3]+1, dp[2]+1) = min(3, 2, 3) = 2`

### 5.6 两类 DP 问题（Slide 51）

- **Optimization**：求最大 / 最小（例如最少硬币、最短路径）
- **Combinatorial**：求"有几种方法"（例如爬楼梯有几种走法）

### 5.7 DP 的 4 步 schema（Slide 52）

1. 证明问题可以拆成 **最优的小问题**
2. 用小问题的解，**递归地定义** 大问题的值（写出公式，例如 `f[i] = f[i-1] + f[i-2]`）
3. **Bottom-up** 把值算出来（填表）
4. 用算好的资料 **重建** 最优解

---

## 6. Pattern Matching（regex）

**Regular expression (regex)** = 一种特殊写法的字符串，用来描述"要找的文字长什么样"。

### 6.1 三个 class（Slide 55–57）

| Class | 角色 | 怎么拿到 |
|---|---|---|
| `Pattern` | 编译好的 regex | `Pattern.compile("...")`（没有 public constructor，不能 `new`） |
| `Matcher` | 拿 pattern 去对 input string 的"引擎" | `pattern.matcher("input")` |
| `PatternSyntaxException` | regex 写错时抛出的 error | — |

**流程：**  `compile` → `matcher` → `matches()` / `find()`

### 6.2 Slide 58 的 code 为什么是这个结果？

```java
Pattern pat = Pattern.compile("JavaFX");
Matcher mat = pat.matcher("JavaFX");
mat.matches();        // true  → "1 : Matches"

mat = pat.matcher("JavaSwing");
mat.matches();        // false → "2 : No Match"
```

### 6.3 `matches()` vs `find()`（非常常考）

| Method | 意思 |
|---|---|
| `matches()` | **整个 string** 要完全符合 pattern |
| `find()` | 只要 string **里面某一段** 符合就行 |

```java
Pattern p = Pattern.compile("JavaFX");
p.matcher("JavaFX").matches();          // true
p.matcher("I love JavaFX").matches();   // false （整句不等于 JavaFX）
p.matcher("I love JavaFX").find();      // true  （里面有 JavaFX）
```

### 6.4 Regex 小抄（额外，Slide 没有）

| 符号 | 意思 | 例子 |
|---|---|---|
| `.` | 任何一个字符 | `a.c` 匹配 abc, a1c |
| `*` | 前一个出现 **0 次或以上** | `ab*` 匹配 a, ab, abbb |
| `+` | **1 次或以上** | `ab+` 匹配 ab, abbb |
| `?` | 0 或 1 次 | `colou?r` |
| `[a-z]` | 任一小写字母 | |
| `\\d` | 一个数字（Java 里 `\` 要写两个） | `\\d{4}` 4 个数字 |
| `^` / `$` | 开头 / 结尾 | |

```java
Pattern.matches("\\d{4}-\\d{2}", "2026-09");                  // true
Pattern.matches("[a-z]+@[a-z]+\\.com", "zichen@tar.com");    // true
```

---

## 7. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Iterator | 不暴露内部结构地走过 collection；`hasNext` / `next` / `remove` |
| Iterator pattern | Behavioral pattern |
| GoF 两原则 | Program to interface；composition over inheritance |
| String | immutable；改 = 造新的；比较内容用 `equals` |
| StringBuilder | 大量修改时用 |
| `printf` vs `String.format` | 印出来 vs 返回 String |
| DP 条件 | overlapping subproblems + optimal substructure |
| Naive fib | ≈ O(2ⁿ) |
| DP fib | O(n) |
| `matches()` vs `find()` | 整个 string vs 里面某一段 |

---

## 8. 练习

### A. MCQ

**A1.** Iterator 的哪个 method 删除"上一次 `next()` 返回的 element"？
a) `delete()`　b) `remove()`　c) `pop()`　d) `clear()`

**A2.** 下面会印什么？
```java
String s = "Hi";
s.concat("!");
System.out.println(s);
```
a) `Hi!`　b) `Hi`　c) error　d) `null`

**A3.** 下面哪个是 DP 适用的必要条件？
a) 数据必须已排序　b) Overlapping subproblems　c) 必须用 recursion　d) 必须用 array

**A4.** `Pattern.compile("JavaFX").matcher("I love JavaFX").matches()` 返回？
a) true　b) false　c) 抛 exception　d) 编译错误

**A5.** Iterator pattern 属于哪一类 design pattern？
a) Creational　b) Structural　c) Behavioral　d) Functional

### B. Short answer

**B1.** 为什么要用 Iterator，而不是直接用 index 走 collection？

**B2.** DP 和 Divide & Conquer 有什么不同？

**B3.** 为什么 naive recursive Fibonacci 慢？DP 怎么解决？

### C. Trace / Calculation

**C1.** 用 slide 的定义（Fib(0)=Fib(1)=1），用 bottom-up 算 `Fib(8)`，写出填表。

**C2.** naive recursion 的 `fib(5)` 里，`fib(2)` 被 call 了几次？总 call 数是多少？

**C3.** 硬币 `{1, 5, 6}`，凑 **10** 块，用 greedy 得几个？DP 最少几个？

### D. Thinking

**D1.** 为什么 Java 的 String 要设计成 immutable？（提示：想想多个变量指向同一个 String 的情况）

**D2.** Merge sort 是 D&C，可以用 DP 优化吗？为什么？

---

### 答案

**A1: b**　**A2: b**（`concat` 返回新 String，没有 assign 回 `s`）　**A3: b**　**A4: b**（`matches()` 要整句符合）　**A5: c**

**B1.** 因为 Iterator 提供 **统一** 的走法（`hasNext` / `next`），不需要知道 collection 内部是 array、linked list 还是 set；以后换内部结构，使用的 code 不用改。

**B2.** D&C 的小问题 **互相独立**，分别解完再合并；DP 的小问题 **重叠**，所以把结果记下来重复利用，并追求整体最优。

**B3.** Naive recursion 会重复计算同样的子问题（例如 fib(2) 在 fib(5) 里算 3 次），所以 call 次数指数增长（≈ O(2ⁿ)）。DP 每个子问题只算一次并存起来，所以变成 O(n)。

**C1.**

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| f[i] | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 | **34** |

**C2.** `fib(2)` 被 call **3 次**；`fib(5)` 总共 **15** 次 call。

**C3.** Greedy：6 + 1 + 1 + 1 + 1 = **5 个**。DP：5 + 5 = **2 个**。

（DP 表 `dp[0..10]`：0,1,2,3,4,1,1,2,3,4,2；`dp[10] = min(dp[9]+1, dp[5]+1, dp[4]+1) = min(5, 2, 5) = 2`）

**D1.** 因为 String 会被很多变量共用（例如 literal pool）。如果可以改，一个变量改了，其他指向同一个 String 的变量也会被改到，造成 bug。Immutable 让 String 安全、可以共用，也可以当 HashMap 的 key（hash 不会变）。

**D2.** 不适合。Merge sort 拆出来的小问题（左半、右半）**不重叠**，没有重复计算，所以 DP 的"记住结果"帮不上忙。DP 要有 overlapping subproblems 才有用。

---

## 9. 和后面章节的连接

- Ch3/4：naive fib ≈ O(2ⁿ) vs DP O(n)，就是 Big-O 差距的实例
- Ch6：`Set` 也是 Collection，也用 Iterator（for-each）
- Ch8：recursion 的 call stack（fib 的每次 call 会占 stack）
- Ch9：DFS 是 recursion，BFS 用 queue
