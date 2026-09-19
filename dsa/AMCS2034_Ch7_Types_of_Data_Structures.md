# AMCS2034 — Chapter 7: Types of Data Structures

> 这章内容最多（84 张 slide），而且很多是 "只有图没有解释"（cache locality、queue 的 array 实现、tree traversal、stock span…）。
> 这份 note 按 **4 个大块** 整理，每块补上 slide 没解释的地方，并且有 trace 例子。

---

## 0. 地图：这章有两种分类方式

| 分类角度 | 类别 | 例子 |
|---|---|---|
| **Memory 怎么用** | Static / Dynamic | Array / Linked list |
| **数据怎么排** | Linear / Non-linear | Array, Linked list, Stack, Queue / Tree, Graph |

（同一个 data structure 会同时属于两种分类。例如 array 是 static，也是 linear。）

---

## 1. Static vs Dynamic Data Structure

### 1.1 定义

| | Static | Dynamic |
|---|---|---|
| Size | **固定**，要事先知道最大大小 | 可以 **增加 / 缩小** |
| 例子 | Array | Linked list |
| 重点 | 偏向 **performance** | 偏向 **efficient memory 使用** |

**类比**：
- Static = 订一张 **固定 10 人座的桌子**，来 3 个人也占一张桌子；来 11 个就坐不下。
- Dynamic = **可以随时加椅子 / 减椅子** 的桌子，来几个人就摆几张椅子。

### 1.2 Overflow / Underflow（Slide 7, 11）

| 名词 | 意思 |
|---|---|
| Overflow | 装不下了还要加（满了还 add） |
| Underflow | 已经空了还要拿（空了还 remove） |

Slide 27 的表格说：static "不会有 overflow / underflow 问题"，dynamic "会有"。这句话 **容易误导**。比较准确的意思是：
- Static：memory 大小固定，**不用** 自己去管理"还有多少 memory 可用"，程序比较好写。（但你要往满的 array 再加东西，当然还是不行。）
- Dynamic：memory 是运行时向系统要的，程序要自己记录 size 和 data 的位置，比较麻烦。

### 1.3 Array vs Linked List（Slide 12–22）

**Array**：连续（contiguous）的一排格子，用 index 访问。

```
index:   0     1     2     3     4
       ┌─────┬─────┬─────┬─────┬─────┐
       │ 1000│ 1010│ 1050│ 2000│ 2040│      ← 一整块连在一起的 memory
       └─────┴─────┴─────┴─────┴─────┘
```

**Linked list**：一个个 node，每个 node 存 data + 指向下一个 node 的 reference。

```
head
  │
  ▼
┌──────┬───┐    ┌──────┬───┐    ┌──────┬───┐
│ 1000 │ ●─┼──► │ 1010 │ ●─┼──► │ 1050 │null│
└──────┴───┘    └──────┴───┘    └──────┴───┘
   node             node             node        ← 可以散落在 memory 各处
```

### 1.4 对比表（加上 Big-O，帮你看清楚）

| 操作 / 特性 | Array | Linked list |
|---|---|---|
| 用 index 拿第 k 个 | **O(1)**（直接算地址） | **O(n)**（要从 head 一个个走过去） |
| 在 **已知位置** 插入 / 删除 | O(n)（要 **shift** 后面的） | **O(1)**（改几个 reference） |
| 在中间插入 / 删除（**要先找位置**） | O(n) | O(n)（找位置 O(n) + 改 reference O(1)） |
| 搜索 | O(n)（排好序的可以 binary search O(log n)） | O(n)（**不能** binary search） |
| Size | 固定 | 动态 |
| Memory 排列 | 连续 | 分散 |
| 额外 memory | 没有（但预留的空格可能浪费） | 每个 node 多一个 pointer（overhead） |
| Cache 表现 | **好** | 差 |

### ⚠️ Slide 里 3 个需要小心的说法

**① "Linked list 的 insertion / deletion 很快"（Slide 15）**
只有在 **你已经拿到那个位置的 reference** 时才是 O(1)。如果要 "在第 k 个位置插入"，你得先从 head 走过去 → O(n)。所以完整的说法是：**改 reference 很快，但找位置很慢**。

**② "Array 的 memory 在 compile time 分配"（Slide 16）**
在 C 里差不多是对的，但 **Java 的 `new int[n]` 是在 runtime 才分配的**（在 heap，见 Ch8）。真正的重点是：**array 一旦建立，大小就固定了**。

**③ "Array 的 memory utilization 不好、linked list 比较好"（Slide 17）**
要看角度：array 可能 **预留太多没用到的格子**（浪费），但每个 element **没有额外 pointer**；linked list 用多少 node 就是多少，但 **每个 node 都多一个 pointer**。所以没有绝对谁好，要看情况（又是 space/time tradeoff）。

### 1.5 为什么 array 插入很贵？（Slide 18–20）

Array `id[] = [1000, 1010, 1050, 2000, 2040]`，要在 sorted 的位置插入 **1005**：

```
之前:   [1000, 1010, 1050, 2000, 2040, _ ]
                 ↑ 1005 应该放这里
步骤:   把 2040, 2000, 1050, 1010 全部往右移一格（从后面开始移！）
之后:   [1000, 1005, 1010, 1050, 2000, 2040]
```

Element 越多，要移的越多 → **O(n)**。
删除 1010 也一样：后面的都要往左移补上洞 → O(n)。

### 1.6 Cache Locality（Slide 22–26）——slide 只有图，这里解释

**先懂两件事：**
- CPU 读 RAM 很 **慢**，所以 CPU 有一个小而快的 **cache**。
- 每次从 RAM 读一个地址，CPU 会顺便把 **附近的一大块** 一起搬进 cache（因为程序常常接着读附近的东西）。

**类比**：你去图书馆拿一本书，管理员顺便把 **同一个书架上相邻的 10 本** 一起帮你搬到桌上。

**Array（连续）**：读 `data[0]` 时，`data[1]、data[2]…` 通常 **已经一起被搬进 cache** → 后面的读取很快。

**Linked list（分散）**：node 可能散落在 memory 各处。读了第 1 个 node，附近搬进来的大概 **没有下一个 node** → 读 `next` 又要回 RAM（**cache miss**），慢很多。

```
Array:        [■][■][■][■][■][■]     ← 一次搬一整块，后面全部命中
Linked list:  [■]      [■]   [■]         [■]   ← 每一个 node 都可能 cache miss
```

所以即使两者 Big-O 都是 O(n) 的遍历，**array 实际上通常更快**。

---

## 2. Linked List 的实作（Slide 28–46）

### 2.1 Object reference = 指向 object 的"地址"

```java
class Node {
    int info;
    Node next;     // ← 一个 Node 里面有一个指向"同类型 Node"的 reference
}
```

### 2.2 为什么要 intermediate node？（Slide 31）

Data（例如 Student）**不应该知道自己在 list 里**。所以不让 `Student` 自己存 `next`，而是另外做一个 **Node**：

```
Node = [ 指向 Student object 的 reference | 指向下一个 Node 的 reference ]
```

这样同一个 Student 可以放进不同的 list，而 Student class 不用改。

### 2.3 Slide 33–40 Magazine 例子在做什么？

- `Magazine`：一本杂志（存 title）
- `MagazineList`：linked list，里面有 **private inner class `MagazineNode`**
- `MagazineRack`：main，`add` 5 本杂志然后印出来

**`add(Magazine mag)` 怎么运作：**

```java
MagazineNode node = new MagazineNode(mag);
if (list == null)              // list 是空的
    list = node;               // 新 node 就是第一个
else {
    current = list;
    while (current.next != null)   // 走到最后一个 node
        current = current.next;
    current.next = node;           // 接在最后面
}
```

⚠️ 每次 `add` 都要 **从头走到最后** → **O(n)**。如果 list 有 `rear`（尾巴）的 reference（Slide 46 的 header node），`add` 就可以变成 **O(1)**。

### 2.4 Insert / Delete node（Slide 41–44）

**在 `current` 后面插入 `newNode`（Slide 42–43 的答案）：**

```java
newNode.next = current.next;   // ① 先让新 node 指向后面那个
current.next = newNode;        // ② 再让 current 指向新 node
```

```
之前:  current ──► B ──► C
① :    newNode ──► B         （newNode.next = current.next，也就是 B）
② :    current ──► newNode ──► B ──► C
```

> ⚠️ **顺序不能反！** 如果先做 `current.next = newNode`，你就失去了 B 的 reference，后面整条 list 就丢了。

**删除 `current` 后面的 node：**

```java
current.next = current.next.next;   // 直接跳过它
```

```
之前:  current ──► B ──► C
之后:  current ────────► C          （B 没人指向，之后被 garbage collect）
```

**在最前面插入 / 删除（更新 head）：**

```java
newNode.next = head; head = newNode;   // addFirst
head = head.next;                      // removeFirst
```

我跑过：`10→20→30`，`insertAfter(10, 15)` 得 `10→15→20→30`，再删除 15 后面的 20 得 `10→15→30` ✅

### 2.5 其他形式（Slide 45–46）

| 形式 | 特点 |
|---|---|
| **Doubly linked list** | 每个 node 有 `next` 和 `previous`，可以往前走，删除一个 node 时不需要先找它的前一个 |
| **Header node** | 另外一个 node 存 `count`、`front`、`rear`，加 / 删头尾更快 |

---

## 3. Linear Data Structures

**Linear = element 排成一条线，一个接一个。** 例子：Array, Linked list, Stack, Queue。

### 3.1 Queue（队列）—— FIFO

**类比**：银行排队。**先来的先服务**（First-In, First-Out）。

```
Rear（加入）                                Front（离开）
    ──►  [ E ][ D ][ C ][ B ][ A ]  ──►
enqueue                                    dequeue
```

| Operation | 做什么 |
|---|---|
| `enqueue(x)` | 加到 **rear**（队尾） |
| `dequeue()` | 从 **front**（队头）拿走 |
| `empty()` | 是否空 |

**Linked list 实作**：front 指向第一个 node，rear 指向最后一个。`dequeue` 改 front，`enqueue` 接在 rear 后面，都是 O(1)。（Slide 53：references 从 front 指向 rear 最有效率。）

**Array 实作（Slide 53 的 `%` wrap-around）—— circular queue：**

问题：一直 dequeue 的话，array 前面会空出来，但 rear 已经到最后了。解决：**把 array 首尾接成圈**。

- 存 `front`（队头 index）和 `size`（现在有几个）
- 队尾要放的位置：`(front + size) % capacity`
- `%`（取余数）让 index 到了尾巴以后 **绕回 0**

**Trace（capacity = 5）：**

| 操作 | front | size | array（index 0–4） |
|---|---|---|---|
| 开始 | 0 | 0 | [ _ , _ , _ , _ , _ ] |
| enqueue 10, 20, 30, 40 | 0 | 4 | [10, 20, 30, 40, _ ] |
| dequeue（拿走 10） | 1 | 3 | [10, 20, 30, 40, _ ] |
| dequeue（拿走 20） | 2 | 2 | [10, 20, 30, 40, _ ] |
| enqueue 50 → 位置 (2+2)%5 = **4** | 2 | 3 | [10, 20, 30, 40, **50**] |
| enqueue 60 → 位置 (2+3)%5 = **0**（绕回） | 2 | 4 | [**60**, 20, 30, 40, 50] |

现在 queue 里的内容（从 front 开始读）是 **30, 40, 50, 60**。（index 0 的旧值 10 和 index 1 的 20 已经"被拿走"，只是没有清掉，不算在里面。）

**应用（Slide 54）**：print queue、CPU job scheduling、客服中心排队、BFS（Ch9）。

### 3.2 Stack（栈）—— LIFO

**类比**：一叠盘子。**最后放上去的最先拿**（Last-In, First-Out）。

```
        │  C  │ ← top（最后放进去的，也是最先拿走的）
        │  B  │
        │  A  │
        └─────┘
```

| Operation | 做什么 |
|---|---|
| `push(x)` | 放到 top |
| `pop()` | 拿走 top 并返回 |
| `peek()` (top) | 只看 top，**不拿走** |
| `empty()` | 是否空 |

**Trace：**

| 操作 | Stack（左边是 bottom，右边是 top） | 返回 |
|---|---|---|
| push 1 | [1] | |
| push 2 | [1, 2] | |
| push 3 | [1, 2, 3] | |
| pop | [1, 2] | 3 |
| peek | [1, 2] | 2 |
| pop | [1] | 2 |

**实作**：Linked list（第一个 node 当 top）或 array（bottom 在 index 0，用一个 `top` 记录位置）。

**应用（Slide 59）**：symbol balancing、infix → postfix、function call（recursion）、browser 的 Back 按钮、text editor 的 Undo、HTML tag 匹配。

**例子：Balancing of symbols（括号配对）**

规则：遇到 `(` `[` `{` → push；遇到 `)` `]` `}` → pop 一个，要 **配对** 才对。最后 stack 要是空的。

`{[()]}`：

| 读到 | 动作 | Stack |
|---|---|---|
| `{` | push | { |
| `[` | push | { [ |
| `(` | push | { [ ( |
| `)` | pop `(` ✅ 配对 | { [ |
| `]` | pop `[` ✅ | { |
| `}` | pop `{` ✅ | 空 → **balanced** |

`{[(])}`：读到 `]` 时 pop 出来的是 `(`，配不上 `]` → **not balanced** ❌。
`((` → 结束时 stack 还剩东西 → ❌；`())` → 读到第二个 `)` 时 stack 已经空 → ❌。（我用 Java 跑过这 4 个，结果一致。）

### 3.3 Stock Span Problem（Slide 60）

**定义**：第 i 天的 span = **包括今天在内**，往前连续多少天的价格 **≤ 今天的价格**。

价格 `{100, 80, 60, 70, 60, 75, 85}`，span = `{1, 1, 1, 2, 1, 4, 6}`。

**为什么？**
- 第 4 天（70）：往前看，60 ≤ 70 ✓，80 > 70 ✗ → 今天 + 前一天 = 2
- 第 6 天（75）：往前 60 ✓、70 ✓、60 ✓（第 5、4、3 天），80 > 75 ✗ → 今天 + 3 = 4
- 第 7 天（85）：往前一直到 100 才停 → 今天 + 前 5 天 = 6

**用 stack 的做法（存 index，price 由大到小）：**

```
for 每一天 i:
    while stack 不空 且 price[stack顶] ≤ price[i]:  pop
    span[i] = stack 空 ? i+1 : i − stack顶
    push i
```

Trace：

| Day i | price | pop 掉的 | stack 顶（pop 后） | span | Stack（存 index） |
|---|---|---|---|---|---|
| 0 | 100 | — | 空 | 0+1 = 1 | [0] |
| 1 | 80 | — | 0 | 1−0 = 1 | [0,1] |
| 2 | 60 | — | 1 | 2−1 = 1 | [0,1,2] |
| 3 | 70 | 2 | 1 | 3−1 = 2 | [0,1,3] |
| 4 | 60 | — | 3 | 4−3 = 1 | [0,1,3,4] |
| 5 | 75 | 4, 3 | 1 | 5−1 = 4 | [0,1,5] |
| 6 | 85 | 5, 1 | 0 | 6−0 = 6 | [0,6] |

结果 `{1, 1, 1, 2, 1, 4, 6}` ✅（和 slide 一样，我用 Java 验证过）。

---

## 4. Non-linear Data Structures

**Non-linear = 一个 element 可以连到 **很多个** 其他 element**，形状是层级或网络。不能一次走完就"一条线"。

### 4.1 Tree

| 术语 | 意思 |
|---|---|
| **Root** | 最上面的 node（没有 parent） |
| **Parent / Child** | 上一层 / 下一层直接相连的 |
| **Leaf** | 没有 child 的 node |
| **Internal node** | 不是 root、也不是 leaf 的 node（Slide 66） |
| **Binary tree** | 每个 node **最多 2 个** child（left、right） |

```
            1            ← root
          /   \
         2     3         ← internal nodes
        / \   / \
       4   5 6   7       ← leaves
```

**Binary tree 的应用（Slide 69）**：expression tree（compiler）、Huffman coding（压缩）、**Binary Search Tree**（平均 O(log n) 的 search / insert / delete）、**Priority Queue**。

### 4.2 Binary Tree Traversal（Slide 70–76）

**Traversal = 把 tree 里每个 node 都访问一遍**（和 search 的差别：traversal 要处理 **全部**，search 找到就停，Slide 71）。

三个动作：**D**（visit 这个 node）、**L**（走 left subtree）、**R**（走 right subtree）。差别只是 **D 放在哪里**：

| Traversal | 顺序 | D 的位置 | 上图结果 |
|---|---|---|---|
| **Preorder** | D L R | **前** | 1 2 4 5 3 6 7 |
| **Inorder** | L D R | **中** | 4 2 5 1 6 3 7 |
| **Postorder** | L R D | **后** | 4 5 2 6 7 3 1 |

（记法：Pre = 先 visit root；In = root 在中间；Post = root 最后。）

**怎么一步步 trace Inorder（对每个 subtree 都用同一个规则）：**

```
inorder(1):
   inorder(2):                    ← 先走 1 的 left
       inorder(4): 没有 child → visit 4
       visit 2
       inorder(5): visit 5
   visit 1                        ← left 全走完，才 visit 1
   inorder(3):
       inorder(6): visit 6
       visit 3
       inorder(7): visit 7
结果: 4 2 5 1 6 3 7
```

**Slide 70："每个 node 只 process 一次，但可能被 visit 多次"**：意思是 recursion 从 child 回到 parent 时，会 **路过** parent 好几次（下去一次、从 left 回来一次、从 right 回来一次），但真正"做 D 动作"只做一次。

**额外**：Binary Search Tree 做 **inorder** traversal，会得到 **从小到大** 排好的结果。

### 4.3 Graph（Slide 77–81，Ch9 详细讲）

- Graph = **vertices（点）+ edges（线）**
- 和 tree 不同：**没有 root**，任何点都可以连到任何点，可以有 **cycle（环）**
- **Directed graph（digraph）**：edge 有方向（类比：航班，A→B 不代表 B→A）
- Undirected：edge 没有方向（类比：高速公路）

---

## 5. Linear vs Non-linear（Slide 82）

| | Linear | Non-linear |
|---|---|---|
| 排列 | 一条线 | 层级 / 网络 |
| 一次走完？ | 可以，一个 loop | 不行，要用 recursion / stack / queue |
| 实作 | 比较简单 | 比较难 |
| 例子 | Array, Linked list, Stack, Queue | Tree, Graph |

---

## 6. Cheat sheet

| 概念 | 一句话 |
|---|---|
| Static / Dynamic | 固定 size / 可变 size |
| Array | O(1) 访问，O(n) 插入 / 删除；cache 好 |
| Linked list | O(n) 访问，改 reference O(1)（但要先找到位置）；每 node 有 pointer overhead |
| 插入 node | `new.next = cur.next; cur.next = new`（顺序不能反） |
| Queue | FIFO；enqueue rear / dequeue front；array 用 `%` 绕圈 |
| Stack | LIFO；push / pop / peek |
| Tree traversal | Pre = D L R；In = L D R；Post = L R D |
| Tree vs Graph | Tree 有 root、无 cycle；Graph 没 root、可以有 cycle |

---

## 7. 练习

### A. MCQ

**A1.** 下面哪个是 static data structure？
a) Linked list　b) Array　c) Tree　d) Graph

**A2.** 在 array 中间插入一个 element，最主要的成本是？
a) 建新 node　b) 把后面的 element 往后 shift　c) 排序　d) 没有成本

**A3.** Stack 的原则是？
a) FIFO　b) LIFO　c) 随机　d) 按大小

**A4.** Binary tree 的 Inorder traversal 顺序是？
a) D L R　b) L R D　c) L D R　d) R D L

**A5.** Array 通常比 linked list 更有 cache locality，因为？
a) Array 比较小　b) Array 的 element 在 memory 里连续　c) Array 有 pointer　d) Array 是 dynamic

### B. Short answer

**B1.** 列出 linked list 相比 array 的 2 个优点和 2 个缺点。

**B2.** 为什么在 linked list 插入 node 时要先做 `newNode.next = current.next`，再做 `current.next = newNode`？

**B3.** 解释 Queue 的 array 实作里 `%` 的作用。

### C. Trace / Calculation

**C1.** Stack 开始是空的，依序：`push 5, push 8, pop, push 2, peek, pop, pop`。写出每个操作的返回值和 stack 变化。

**C2.** 用 circular queue（capacity = 4），依序 `enqueue A, B, C`，`dequeue`，`enqueue D, E`。写出最后 front、size、array 内容，以及 queue 内容（从 front 开始）。

**C3.** Binary tree：A 是 root，A 的 left child 是 B，right child 是 C；B 的 children 是 D（left）、E（right）；C 只有 right child F。写出 Preorder、Inorder、Postorder。

### D. Thinking

**D1.** 如果你的程序 **很常在 list 中间插入 / 删除**，但 **很少按 index 读取**，array 和 linked list 你选哪个？如果反过来呢？

**D2.** 用 stack 检查括号：`"(a + b) * [c - d"` 是否 balanced？

---

### 答案

**A1: b**　**A2: b**　**A3: b**　**A4: c**　**A5: b**

**B1.**
- 优点：(1) size 动态，不用事先知道；(2) 在已知位置插入 / 删除只要改 reference，不用 shift。
- 缺点：(1) 不能 random access（要从头走，O(n)）；(2) 每个 node 多一个 pointer 的 memory；（另外：cache 表现比 array 差，也不能 binary search。）

**B2.** 因为 `current.next` 原本指向后面那串 node。如果先做 `current.next = newNode`，就会失去 "后面那个 node" 的 reference，后面整条 list 就断了、找不回来。所以要先让 newNode 记住后面的，再让 current 指向 newNode。

**B3.** `%`（取余数）让 index 走到 array 尾巴之后 **绕回 0**，把 array 当成一个圈，这样前面被 dequeue 空出来的位置可以重复使用。队尾位置 = `(front + size) % capacity`。

**C1.**

| 操作 | 返回 | Stack（bottom → top） |
|---|---|---|
| push 5 | | [5] |
| push 8 | | [5, 8] |
| pop | 8 | [5] |
| push 2 | | [5, 2] |
| peek | 2 | [5, 2] |
| pop | 2 | [5] |
| pop | 5 | [ ] |

**C2.** capacity = 4：

| 操作 | front | size | array |
|---|---|---|---|
| enqueue A, B, C | 0 | 3 | [A, B, C, _] |
| dequeue（拿走 A） | 1 | 2 | [A, B, C, _] |
| enqueue D → 位置 (1+2)%4 = 3 | 1 | 3 | [A, B, C, D] |
| enqueue E → 位置 (1+3)%4 = 0（绕回） | 1 | 4 | [E, B, C, D] |

最后：**front = 1，size = 4**，array = **[E, B, C, D]**；queue 内容（从 front 读起）= **B, C, D, E**。

**C3.**
- Preorder（D L R）：**A B D E C F**
- Inorder（L D R）：**D B E A C F**
- Postorder（L R D）：**D E B F C A**

（用 Java 跑过对应的数字版本，结果一致。）

**D1.** 很常在中间插入 / 删除、很少按 index 读 → **linked list**（改 reference 快；前提是你已经在那个位置附近，例如用 iterator 走到该处）。反过来，常常按 index 读、很少插入 → **array**（O(1) 访问、cache 好）。

**D2.** 逐字读：`(` push；`)` pop 配对 ✅；`[` push；到结束时 stack 里还剩 `[` → **不 balanced**（少了 `]`）。

---

## 8. 和后面章节的连接

- Ch8：Stack 就是 method call 用的 memory（call stack）；linked list 的 node 放在 heap
- Ch9：DFS 用 stack / recursion，BFS 用 queue；Graph 的详细表示法
- Ch6：TreeSet 底层是 tree；HashSet 的 chaining 用 linked list
