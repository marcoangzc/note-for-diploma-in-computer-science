# AMCS2034 — Chapter 6: Sets

> Slide 的问题：HashSet 只讲了 "capacity 16、load factor 0.75"，**没解释为什么、也没讲 collision**；
> Union / Intersection / Difference 的 demo 输出会让人以为 code 有 bug；TreeSet 的 `lower / floor / higher / ceiling` 没说清楚差别。
> 这份 note 把这些全部补上。

---

## 0. 这章一句话总览

**Set = 不允许重复的 collection。** Java 有三种 Set：

| | HashSet | LinkedHashSet | TreeSet |
|---|---|---|---|
| 顺序 | **没有**特定顺序 | **插入顺序**（先加先出现） | **排序**（sorted） |
| 速度（额外补充） | 最快，平均 O(1) | 比 HashSet 稍慢，平均 O(1) | O(log n) |
| 什么时候用 | 只要"不重复 + 快" | 不重复 + 想保留放进去的顺序 | 不重复 + 要一直保持排序 |
| 底层（额外补充） | Hash table | Hash table + linked list | Tree（平衡树） |

Slide 33 的建议：**不需要排序就用 HashSet**，因为 insert / remove 比较快。

---

## 1. Set 是什么？（Slide 3–6）

- Set 是 abstract data type（ADT），存 **不重复** 的值，**没有特定顺序**
- 最常用来 **测试一个东西在不在集合里**（`contains`）
- 可以做集合运算：**Union、Intersection、Difference**
- `Set` interface extends `Collection`，**没有新增 method**，只是保证没有重复（Slide 6）

### 常用 methods

| Method | 做什么 |
|---|---|
| `add(e)` | 加入。已存在就不加（返回 false） |
| `remove(e)` | 删除 |
| `contains(e)` | 在不在？ |
| `size()` / `isEmpty()` | 大小 / 是否空 |
| `addAll(c)` | **Union**：把 c 里的都加进来 |
| `retainAll(c)` | **Intersection**：只保留 c 里也有的 |
| `removeAll(c)` | **Difference**：删掉 c 里有的 |

---

## 2. HashSet — 它是怎么运作的？

### 2.1 类比：储物柜

想象一排 **16 个储物柜**（bucket），编号 0–15。你要放东西 x：

1. 算出 x 的 **hash code**（一个整数，"x 的号码"）
2. 用 `hashCode % 16`（简化说法）决定放哪个柜子
3. 要查 x 在不在？**直接算号码，走去那个柜子看**，不用一个一个柜子翻 → 所以很快，平均 **O(1)**

这就是为什么 HashSet 的 `contains` 很快，但也是为什么它 **没有顺序**：位置由 hash 决定，不由放进去的顺序决定。

### 2.2 `add(x)` 的步骤

```
1. 算 x.hashCode()            → 决定去哪个 bucket
2. 去那个 bucket 看
3. 里面有没有 element 跟 x equals？
      有 → 已经存在，不加
      没有 → 加进去
```

所以 HashSet 判断"重复"用 **hashCode + equals** 两个东西。

### 2.3 hashCode（Slide 10–11）

规则：

1. **两个 object equals → hashCode 一定相同**
2. 两个 object 不 equals → hashCode **可以相同**（这叫 collision，见 2.5），但要尽量避免太多

Java 内置类别的 hashCode：

| 类别 | hashCode |
|---|---|
| `Integer` | 它自己的值 |
| `Character` | 它的 Unicode 值 |
| `String` | s₀·31^(n−1) + s₁·31^(n−2) + … + sₙ₋₁ |

（Slide 11 的 String 公式在 PDF 里显示得很乱，中间的 "+ c +" 其实就是 "+ … +"。）

**算一个 String 的 hashCode：`"ab"`**

n = 2，'a' = 97，'b' = 98：

```
hashCode = 97 × 31¹ + 98 × 31⁰ = 3007 + 98 = 3105
```

### 2.4 自己写的 class 要 override `equals` 和 `hashCode`

**如果只写 `equals` 不写 `hashCode`**，HashSet 会以为它们不同（因为 hashCode 不一样，去了不同 bucket，根本没机会比较 equals）：

```java
class Student {
    String id;
    Student(String id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Student)) return false;
        return id.equals(((Student) o).id);
    }

    @Override
    public int hashCode() {          // ← 一定要和 equals 一起写
        return id.hashCode();
    }
}
```

我跑过：只有 `equals` → 加两个 `new Student("A1")` 的 set 大小是 **2**（重复了）；补上 `hashCode` → **1** ✅

**口诀：equals 和 hashCode 是一对，一起写。**

### 2.5 Capacity、Load factor 和 Collision（Slide 8–9 的补充）

**Capacity** = bucket 总数（默认 **16**）。
**Load factor** = 允许装到多满才扩容（默认 **0.75**）。

**Collision**：两个不同的 element 算出 **同一个 bucket**。例如 capacity = 16，Integer 的 hashCode 是自己的值：

```
5  % 16 = 5
21 % 16 = 5      ← 和 5 同一个 bucket = collision
37 % 16 = 5
```

Java 用 **chaining**（同一个 bucket 挂一条 linked list）处理：

```
bucket:   element chain:
  0
  1
  2       [2]
  3
  4
  5       [5] → [21] → [37]     ← collision，接成 linked list
  6
  ...
 10       [10]
```

我用 Java 跑 `new HashSet<>(List.of(5, 21, 37, 2, 10))` 印出来是 `[2, 5, 21, 37, 10]`：2 在 bucket 2，5/21/37 在 bucket 5 排在一起，10 在 bucket 10——和上图一样 ✅

**为什么要 load factor？** Element 越多，collision 越多，同一个 bucket 的 chain 越长，`contains` 就要沿着 chain 一个个比，从 O(1) 慢慢变 O(n)。

所以规则是：**size > capacity × load factor 就 double capacity**（Slide 9）

```
capacity = 16, load factor = 0.75  →  16 × 0.75 = 12
size 到 12 之后再多加 → capacity 变 32
```

扩容后所有 element 会 **rehash**（用新 capacity 重新算位置），因为 `hashCode % capacity` 的 capacity 变了。

**Trade-off（Slide 9）：**

| Load factor | Space | Search time |
|---|---|---|
| 高（例如 0.9） | 省 space | 变慢（collision 多） |
| 低（例如 0.5） | 浪费 space | 变快 |
| **0.75（默认）** | — | 好的平衡 |

如果你 **知道大概会存多少个**，可以在 constructor 指定 initial capacity，避免一路扩容（Slide 8）。

### 2.6 Slide 12 的 demo

```java
Set<String> set = new HashSet<>();
set.add("London"); set.add("Paris"); set.add("New York");
set.add("San Francisco"); set.add("Beijing");
set.add("New York");            // 重复，不会加
```

- "New York" 加了两次，只存一次（Set 不允许重复）
- 印出来的顺序 **不是** 你 add 的顺序

> ⚠️ 顺序完全看 hash，所以 **不同 Java 版本可能印出不同顺序**。我在 Java 21 跑出来是 `[San Francisco, Beijing, New York, London, Paris]`，和 slide 的不一样，这是 **正常** 的。**永远不要依赖 HashSet 的顺序。**

---

## 3. Union / Intersection / Difference（Slide 13–18）

### 3.1 Slide 的 demo 为什么会印出 `[]`？（很多人卡在这里）

关键：`addAll`、`removeAll`、`retainAll` **都会直接修改 set1**。Slide 是 **连续** 对同一个 set1 做三个操作，所以后面的操作看到的 set1 已经被改过了。

初始状态：

```
set1 = { San Francisco, New York, Paris, Beijing }      （London 已被 remove）
set2 = { London, Shanghai, Paris }
```

| 步骤 | 操作 | 做了什么 | set1 变成 |
|---|---|---|---|
| ① | `set1.addAll(set2)` **Union** | 把 set2 全加进来 | {SF, NY, Paris, Beijing, **London, Shanghai**} |
| ② | `set1.removeAll(set2)` **Difference** | 删掉 set2 里有的（Paris, London, Shanghai） | {SF, NY, Beijing} |
| ③ | `set1.retainAll(set2)` **Intersection** | 只保留 set2 里也有的 | **{ }**（空！） |

第 ③ 步 set1 是 {SF, NY, Beijing}，**这三个没有一个在 set2 里** → 什么都不留 → `[]`。这不是 bug，是因为 set1 在第 ② 步已经被改了。

### 3.2 三个运算的意思（用 Venn 想）

```
      set1            set2
   ┌────────┐      ┌────────┐
   │  只在  │ ┌──┐ │  只在  │
   │  set1  │ │共│ │  set2  │
   │        │ │同│ │        │
   └────────┘ └──┘ └────────┘

Union        (addAll)    = 全部三块
Intersection (retainAll) = 只有"共同"那块
Difference   (removeAll) = set1 减去"共同" = 只在 set1
```

### 3.3 安全的写法：先 copy 再操作

```java
Set<String> union = new HashSet<>(set1);   // 复制一份
union.addAll(set2);                        // set1 保持不变

Set<String> inter = new HashSet<>(set1);
inter.retainAll(set2);

Set<String> diff = new HashSet<>(set1);
diff.removeAll(set2);
```

---

## 4. LinkedHashSet（Slide 19–22）

- `LinkedHashSet extends HashSet`，加上 **linked list** 来记住 **插入顺序**
- 不重复（因为它还是 Set）
- 用途：**要去重，但又要保留顺序**

```java
Set<String> s = new LinkedHashSet<>();
s.add("b"); s.add("a"); s.add("b"); s.add("c");
System.out.println(s);      // [b, a, c]   顺序 = 第一次出现的顺序，重复的 b 没有影响
```

### ⚠️ Slide 21 的 code 有小错误

```java
for (Object element : set)
    System.out.print(element.toLowerCase() + " ");   // ❌ Object 没有 toLowerCase()
```

`set` 是 `Set<String>`，所以要写 **`for (String element : set)`** 才能编译。

---

## 5. TreeSet（Slide 23–34）

### 5.1 概念

- `TreeSet` 实现 `SortedSet`（更准确是 `NavigableSet`），element **一直保持排好序**
- 放进去的 element 必须 **可以互相比较**

### 5.2 怎么比较？两种方式（Slide 26, 34）

| 方式 | 怎么用 |
|---|---|
| **Comparable**（自然顺序） | element 的 class 自己实现 `compareTo`。`new TreeSet<>()` 就用它 |
| **Comparator**（自订顺序） | 另外写一个 comparator，`new TreeSet<>(comparator)` |

```java
TreeSet<String> asc  = new TreeSet<>(List.of("b", "c", "a"));   // [a, b, c]
TreeSet<String> desc = new TreeSet<>(Comparator.reverseOrder());
desc.addAll(asc);                                                // [c, b, a]
```

（Slide 32：所有 concrete class 至少有两个 constructor：no-arg，和"用另一个 collection 建立"。`new TreeSet<>(set)` 就是后者，把 HashSet 变成排序的 TreeSet。）

### 5.3 Slide 27–31：SortedSet 和 NavigableSet 的 methods

例子里排好序的 tree set：

```
[ Beijing,  London,  New York,  Paris,  San Francisco ]
```

**SortedSet：**

| Method | 结果 | 说明 |
|---|---|---|
| `first()` | Beijing | 最小的 |
| `last()` | San Francisco | 最大的 |
| `headSet("New York")` | [Beijing, London] | 比 New York **小**的（**不含** New York） |
| `tailSet("New York")` | [New York, Paris, San Francisco] | **大于或等于** New York（**含** New York） |

> **记法**：head 不含（exclusive），tail 含（inclusive）。

**NavigableSet：`lower / floor / higher / ceiling`**

这四个是最容易混的。先看差别：

| Method | 找什么 |
|---|---|
| `lower(e)` | **严格小于** e 的最大的那个 |
| `floor(e)` | **小于或等于** e 的最大的那个 |
| `higher(e)` | **严格大于** e 的最小的那个 |
| `ceiling(e)` | **大于或等于** e 的最小的那个 |

（都找不到就返回 `null`）

**Slide 用的是 `"P"`（不在 set 里）：**

```
Beijing   London   New York   [P]   Paris   San Francisco
                       ▲        ↑      ▲
                    lower/floor  |   higher/ceiling
```

"P" 排在 "New York" 和 "Paris" 之间（"P" 是 "Paris" 的开头，较短的比较小）。因为 "P" 不在 set 里，所以：

| | 结果 |
|---|---|
| `lower("P")` | New York |
| `floor("P")` | New York（和 lower 一样） |
| `higher("P")` | Paris |
| `ceiling("P")` | Paris（和 higher 一样） |

**如果 e 本来就在 set 里，差别才出现。** 我用 `"Paris"` 跑过：

| | 结果 |
|---|---|
| `lower("Paris")` | New York（**不含** Paris 自己） |
| `floor("Paris")` | **Paris**（含自己） |
| `higher("Paris")` | San Francisco（**不含** Paris 自己） |
| `ceiling("Paris")` | **Paris**（含自己） |

**记法**：`lower`/`higher` 是"严格"，`floor`/`ceiling` 是"可以等于"。floor = 往下找，ceiling = 往上找。

**`pollFirst()` / `pollLast()`**：**移除** 并返回最小 / 最大的（`first()` / `last()` 只是看，不移除）。

Slide 28 的输出最后一行 `[London, New York, Paris]` 就是 Beijing 和 San Francisco 被 poll 掉之后。

### 5.4 String 怎么比大小？

按字符的 Unicode 一个个比：

- 大写字母 < 小写字母（`"P" < "a"`）
- 前面都一样时，**较短的比较小**（`"P" < "Paris"`）

---

## 6. 三个 Set 怎么选？

| 需求 | 用 |
|---|---|
| 只要不重复、要快 | **HashSet** |
| 不重复，并且保留 **放进去的顺序** | **LinkedHashSet** |
| 不重复，并且要 **排序**（或者要 first / last / floor / ceiling） | **TreeSet** |

额外补充：`HashSet` 可以放一个 `null`；`TreeSet`（自然顺序）放 `null` 会抛 `NullPointerException`。

---

## 7. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Set | 不重复的 collection |
| HashSet | 无序、最快；用 hashCode + equals |
| LinkedHashSet | 保留插入顺序 |
| TreeSet | 排序；Comparable 或 Comparator |
| Capacity / Load factor | bucket 数 / 装到多满就扩容（默认 16 / 0.75） |
| 扩容规则 | size > capacity × load factor → capacity × 2，然后 rehash |
| Collision | 不同 element 落到同一个 bucket；用 chaining |
| equals / hashCode | 一起 override |
| Union / Intersection / Difference | addAll / retainAll / removeAll（**会修改原本的 set**） |
| head / tail | 不含 / 含 |
| lower/higher vs floor/ceiling | 严格 vs 可等于 |

---

## 8. 练习

### A. MCQ

**A1.** 哪种 Set 保留 **插入顺序**？
a) HashSet　b) TreeSet　c) LinkedHashSet　d) 都保留

**A2.** HashSet 默认 initial capacity 和 load factor 是？
a) 10, 0.5　b) 16, 0.75　c) 16, 1.0　d) 32, 0.75

**A3.** `set1.retainAll(set2)` 做的是？
a) Union　b) Intersection　c) Difference　d) Complement

**A4.** TreeSet `[1, 3, 5, 7]`，`ceiling(4)` 返回？
a) 3　b) 4　c) 5　d) null

**A5.** 自己写 class 放进 HashSet 时，为什么要 override `hashCode`？
a) 为了排序　b) 让相同内容的 object 会被判为重复　c) 让 toString 好看　d) 不需要

### B. Short answer

**B1.** HashSet 的 load factor 是什么？为什么是 0.75？

**B2.** 什么是 collision？Java 怎么处理？

**B3.** 什么时候用 LinkedHashSet 而不是 HashSet 或 TreeSet？

### C. Calculation / Trace

**C1.** capacity = 16，load factor = 0.75。加到第几个 element 之后会扩容？扩容到多少？

**C2.** capacity = 8，Integer 的 hashCode 是自己的值。`10, 18, 3, 26` 各落在哪个 bucket（用 `value % 8`）？哪些发生 collision？

**C3.** TreeSet `[2, 4, 6, 8]`，写出：`lower(6)`, `floor(6)`, `higher(6)`, `ceiling(5)`, `headSet(6)`, `tailSet(6)`。

### D. Thinking

**D1.** 如果 hashCode 永远返回同一个数字（例如 `return 1;`），HashSet 会变成什么样？还正确吗？

**D2.** 你要保存"已经访问过的网址"，并且想每次快速检查一个网址有没有访问过。用哪种 Set？为什么？

---

### 答案

**A1: c**　**A2: b**　**A3: b**　**A4: c**（大于或等于 4 的最小值是 5）　**A5: b**

**B1.** Load factor 是"允许装到多满才扩容"的比例。当 size 超过 capacity × load factor，capacity 会 double。0.75 是 time 和 space 的折中：太高省空间但 collision 多、search 变慢；太低搜索快但浪费 space。

**B2.** Collision = 两个不同的 element 算出同一个 bucket。Java 用 chaining：同一个 bucket 挂一条 linked list 存放。

**B3.** 需要 **去重复，同时保留 element 加进去的顺序** 的时候（例如去掉重复的网址但保持第一次出现的顺序）。不需要顺序就用更快的 HashSet；需要排序就用 TreeSet。

**C1.** 16 × 0.75 = 12。size 到 **12** 之后再加（超过 12）就扩容，变成 **32**。

**C2.**

| value | value % 8 |
|---|---|
| 10 | 2 |
| 18 | 2 |
| 3 | 3 |
| 26 | 2 |

**10、18、26 全部落在 bucket 2 → collision**；3 在 bucket 3 没有 collision。

**C3.**
- `lower(6)` = **4**
- `floor(6)` = **6**
- `higher(6)` = **8**
- `ceiling(5)` = **6**（5 不在 set 里，找 ≥ 5 的最小）
- `headSet(6)` = **[2, 4]**（不含 6）
- `tailSet(6)` = **[6, 8]**（含 6）

**D1.** 所有 element 都落到同一个 bucket，变成一条很长的 linked list，`add` / `contains` 从 O(1) 退化成 **O(n)**。结果仍然 **正确**（因为还是会用 equals 判断重复），只是 **很慢**。这就是为什么 hashCode 要"分散得好"（Slide 10）。

**D2.** 用 **HashSet**。只需要"有没有访问过"，不在乎顺序，HashSet 的 `contains` 平均 O(1)，最快。

---

## 9. 和后面章节的连接

- Ch2：Set 也是 Collection → 也能用 Iterator（for-each）
- Ch4：Load factor 是 space/time tradeoff 的例子
- Ch5：HashSet 平均 O(1)，TreeSet O(log n)（tree 的高度）
- Ch7：TreeSet 底层是 tree（non-linear data structure）
