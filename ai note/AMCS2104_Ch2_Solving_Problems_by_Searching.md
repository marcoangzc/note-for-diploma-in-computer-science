# AMCS2104 — Chapter 2: Solving Problems by Searching (2A + 2B + 2C)

> 本章要回答的问题：一个 goal-based agent 知道自己要去哪里，但**该走哪条路**？在不知道路的情况下，怎样有系统地"试"出一条路，而且最好是最便宜的那条？
>
> 📌 考试比重：3 份 past year 都有画 **search tree** 的大题（Oct Q3、Jan Q4 各 25 分；May Q2d 11 分）。**BFS / DFS / A\* 的画树 + formulation 6 elements** 是必拿分的计算题。

---

## Scene：TAR UMT 校园巴士

TAR UMT 交通组要做一个 AI 巴士系统：从 **Station A** 开到 **Station J**。地图如下（这是 tutorial 3/5/6 用的地图，本章从头到尾用它）：

```
             A ─────────3──────────── F
            /                        / \
           6                        2   7
          /                        /     \
         B ──2── D                G       H
          \     /|                 \     /
           1   1 |                  3   3
            \ /  1                   \ /
             C   |                    I
              \  |                  /   \
               5 |                 5     1
                \|                /       \
                 E ──────────────┘         J
                  \                       /
                   └──────────5──────────┘

Edges (undirected, cost):
A–B 6   A–F 3   B–C 1   B–D 2   C–D 1   C–E 5   D–E 1
E–I 5   E–J 5   F–G 2   F–H 7   G–I 3   H–I 3   I–J 1

Heuristic h(n) (red numbers, estimated distance to J):
A 10 | B 8 | C 5 | D 7 | E 3 | F 6 | G 5 | H 3 | I 1 | J 0
```

司机问："哪条路最短？" 你盯着地图，脑中已经在"试"：A→F→G→I→J？A→B→C→E→J？
本章就是把这个"试"变成**算法**。

---

## Part 1：先把问题"说清楚" —— Problem Formulation

### 1.1 Problem-solving agent

- 是一种 **goal-based agent**，要找出一个**动作序列**来达成目标。
- 环境状态用 **atomic representation**（每个城市就是一个不可分割的 state）。
- 本章假设环境：**episodic, single agent, fully observable, deterministic, static, discrete, known** → 所以解答是一个**固定的动作序列**（开车时不用边走边想）。

### 1.2 Problem-solving 的 4 个 phases（tutorial 考）

1. **Goal formulation** —— 决定目标（例：去 Bucharest / 去 Station J）。目标可以**限制**要考虑的目标与动作。
2. **Problem formulation** —— 建立相关世界的**抽象模型**：要考虑哪些 states 与 actions。
3. **Search** —— 在模型里**模拟**动作序列，直到找到到达目标的序列（**solution**）或确认无解。
4. **Execution** —— 按顺序一个一个执行 solution 里的动作。

⚠️ Tutorial 学生答案把第 3 步写成 "Solution Formulation"——**错**，应为 **Search (Solution Searching)**。

### 1.3 一个 problem 的 6 个 components（Oct 2025 & Jan 2026 各考 6 分，必背）

| Component | 定义 | 校园巴士例子 |
|---|---|---|
| **States (state space)** | 环境可能处于的所有 states 的集合 | {A, B, C, …, J}（10 个站） |
| **Initial state** | agent 开始的 state | A |
| **Goal state** | 满足目标的 state | J |
| **Actions** | 在 state s 可执行的动作集合 `ACTIONS(s)` | `ACTIONS(A) = {ToB, ToF}` |
| **Transition model** | 描述每个动作做了什么 `RESULT(s, a)` | `RESULT(A, ToF) = F` |
| **Cost function** | 在 s 执行 a 到达 s' 的代价 `ACTION-COST(s, a, s')` | `ACTION-COST(A, ToF, F) = 3` |

- **Path** = 动作序列；**solution** = 从 initial state 到 goal state 的 path；**optimal solution** = 所有 solution 中 **path cost 最低**的。
- 假设 action cost 是 **additive**：path cost = 各 action cost 之和。
- **State space graph**：vertices = states，directed edges = actions。

📝 **Model answer（Jan 2026 Q4a：Wi-Fi access points A→I）**
> - **State space**: the set of nine access points {A, B, C, D, E, F, G, H, I}; each state = the access point the data packet is currently at.
> - **Initial state**: Access Point A.
> - **Goal state**: Access Point I.
> - **Actions**: transmit to a directly connected next access point, e.g. ACTIONS(A) = {ToB, ToC, ToD}, ACTIONS(F) = {ToE, ToG}.
> - **Transition model**: RESULT(s, a) returns the access point reached, e.g. RESULT(A, ToB) = B, RESULT(G, ToI) = I.
> - **Cost function**: ACTION-COST(s, a, s') = the signal transmission cost on the edge, e.g. ACTION-COST(A, ToB, B) = 4; the path cost is the sum of the edge costs along the path.

（Oct 2025 Q3a 一样写法：9 个 bus stops，initial = A，goal = I，cost = 距离 km。）

### 1.4 Abstraction

Formulated problem 是真实世界的**简化**。去掉细节的过程 = **abstraction**。
- **State abstraction**：人在 Arad（天气、车况都忽略）→ state "Arad"。
- **Action abstraction**：开车去 Sibiu（转弯、换档全忽略）→ action "ToSibiu"。
- Abstraction 的两个性质：**Valid**（任何 abstract solution 都能展开成详细世界里的 solution）；**Useful**（执行 solution 里的每个 abstract action 比原问题容易）。
- 好的 abstraction：**尽量去掉细节、同时保持 valid、而且 abstract actions 容易执行**。

### 1.5 Standardized vs Real-world problems

| | Standardized | Real-world |
|---|---|---|
| 目的 | 展示/练习问题求解方法、给研究者当 benchmark | 人们真正会用到 solution 的问题 |
| 描述 | 简洁、精确 | idiosyncratic（各有各的形式） |
| 例子 | vacuum world、8-puzzle、8-queens、grid world | GPS 导航(Waze)、airline travel、TSP、VLSI layout、robot navigation、automatic assembly sequencing |

**要背的数字**：
- Vacuum world 2 格：2 × 2² = **8 states**；n 格：**n · 2ⁿ**。
- 8-puzzle：9!/2 = **181,440** reachable states；n 格：(n+1)!/2。动作 = **blank** 的 Left/Right/Up/Down，每步 cost 1。
- 8-queens：随便放 64×63×…×57 ≈ **1.8 × 10¹⁴**；每列一个 8⁸ ≈ **1.7 × 10⁷**。**Incremental formulation**（从空棋盘，每步加一个 queen）vs **complete-state formulation**（8 个 queen 都在棋盘上，每次移动一个）。
- Airline：state = 地点 + 时间；cost = 票价 + 飞行时间 + 等候、海关、座位质量……

**课件图：Vacuum world 的 state space（2A p26）**：8 个 states，每个 state 画成两格（agent 在哪一格 + 每格有没有灰尘）。连线是动作：**L** = Left、**R** = Right、**S** = Suck。
- 在最左格做 L、在最右格做 R、在干净的格做 S → 画成**指回自己的圈（self-loop）**，因为 state 不变。
- 从"两格都脏"开始：S 让所在格变干净 → R/L 移到另一格 → S → 到达两格都干净的 **goal states**（agent 在 A 或在 B，共 2 个）。

**课件图：8-puzzle 的 transition model（2A p29–31）**

```
Start state      Goal state (课件)       RESULT(current, Left)
7 2 4            _ 1 2                   7 2 4        7 2 4
5 _ 6            3 4 5                   5 _ 6  -->   _ 5 6     (blank 往左，tile 5 往右)
8 3 1            6 7 8                   8 3 1        8 3 1
```

**课件图：8-queens transition（2A p35）**：action "Up" 作用在第 4 列的 queen 上 → 那个 queen 在**同一列**往上移到空格，其他 queen 不动。

### 1.6 课件的主角：Romania 地图（2A p8，Ch2 所有 Romania 例子都用它）

```
Edges (undirected, km):
Arad–Zerind 75        Arad–Sibiu 140        Arad–Timisoara 118
Zerind–Oradea 71      Oradea–Sibiu 151      Timisoara–Lugoj 111
Lugoj–Mehadia 70      Mehadia–Drobeta 75    Drobeta–Craiova 120
Sibiu–Fagaras 99      Sibiu–Rimnicu Vilcea 80
Rimnicu Vilcea–Pitesti 97                   Rimnicu Vilcea–Craiova 146
Craiova–Pitesti 138   Fagaras–Bucharest 211 Pitesti–Bucharest 101
Bucharest–Giurgiu 90  Bucharest–Urziceni 85 Urziceni–Hirsova 98
Hirsova–Eforie 86     Urziceni–Vaslui 142   Vaslui–Iasi 92    Iasi–Neamt 87
```

**Straight-line distance to Bucharest, h_SLD（2C p28，Figure 3.16）**

| City | h | City | h | City | h |
|---|---|---|---|---|---|
| Arad | 366 | Hirsova | 151 | Pitesti | 100 |
| Bucharest | 0 | Iasi | 226 | Rimnicu Vilcea | 193 |
| Craiova | 160 | Lugoj | 244 | Sibiu | 253 |
| Drobeta | 242 | Mehadia | 241 | Timisoara | 329 |
| Eforie | 161 | Neamt | 234 | Urziceni | 80 |
| Fagaras | 176 | Oradea | 380 | Vaslui | 199 |
| Giurgiu | 77 | | | Zerind | 374 |

**课件的 search tree 图（2A p40–46）**：root = Arad → expand 得到 Sibiu、Timisoara、Zerind → 选 Sibiu expand 得到 Arad、Fagaras、Oradea、Rimnicu Vilcea。图中用虚线把 nodes 分成三区：**expanded nodes**（Arad、Sibiu）、**frontier**（Arad、Fagaras、Oradea、Rimnicu Vilcea、Timisoara、Zerind）、**unexplored nodes**（还没生成的，例如 Timisoara 下面的 Arad、Lugoj）。注意 Sibiu 底下又出现 **Arad** → 这就是 **loopy path**（Arad→Sibiu→Arad，2A p56）。

---

## Part 2：Search Tree —— "试路"的记录本

### 2.1 基本名词（tutorial 必考定义）

- **Search tree**：node = state，edge = action，**root = initial state**。
- **Frontier (open list)**：已生成但**还没 expand** 的 nodes。
- **Node expansion**：对一个 node 应用所有可行 actions，看会到哪些 states。
- **Node generation**：把新产生的 child nodes（successors）**加入 frontier**。
- **Reached**：任何**已经生成过 node** 的 state（不管有没有 expand）。
- **Explored set (closed list)**：已经 expand 过的 nodes。

📝 **Expansion vs Generation**：expansion applies all available actions to the *current* node to find its successor states; generation creates the child nodes for those successor states and *adds them to the frontier* so they can be explored later.

### 2.2 Search tree vs State space

| State space | Search tree |
|---|---|
| 世界所有 states 与 actions（通常是 graph） | 从 initial state 出发、走向 goal 的**路径** |
| 每个 state **只出现一次** | **同一个 state 可以出现多次**（不同路径到达） |

### 2.3 Node 的数据结构（4 components）

`n.STATE`（对应的 state）· `n.PARENT`（生成它的 node）· `n.ACTION`（从 parent 到这里的 action）· `n.PATH-COST`（从 root 到这里的总 cost，记作 g(n)）。
沿着 PARENT 指针往回走就能还原整条路径。

课件图（2A p51）：一个 node 指向它的 **STATE**（一个 8-puzzle 盘面），有一个 **PARENT** 指针往上指，并记着 **ACTION = Right**、**PATH-COST = 6**（从 root 走了 6 步）；它自己的 children 各有指针指回它。

### 2.4 Frontier 用什么 queue？（tutorial 题）

| Queue | 先 pop 谁 | 用于 |
|---|---|---|
| **FIFO** | 最早加入的 | **BFS** |
| **LIFO (stack)** | 最新加入的 | **DFS** |
| **Priority queue** | evaluation function f 最小的 | **UCS (f=g)、Greedy (f=h)、A\* (f=g+h)** |

操作：`IS-EMPTY(frontier)`, `POP(frontier)`, `ADD(node, frontier)`。

**Tutorial 4 例：FIFO vs LIFO 的 frontier 变化**（树：8 → {3, 10}；3 → {1, 6}；6 → {4, 7}；10 → {14}；14 → {13}；左到右）

```
FIFO (BFS)            LIFO (DFS)
[8]                   [8]
[3, 10]               [3, 10]
[10, 1, 6]            [1, 6, 10]
[1, 6, 14]            [6, 10]
[6, 14]               [4, 7, 10]
[14, 4, 7]            [7, 10]
[4, 7, 13]            [10]
[7, 13]               [14]
[13]                  [13]
[]                    []
```

### 2.5 Loopy path & Redundant path

- **Loopy path (cycle)**：路径中**重复出现同一个 state**（Arad→Sibiu→Arad）。可能让搜索陷入无限循环。
- **Redundant path**：用更差的路到达**已经可以用更好方法到达**的 state（Arad→Zerind→Oradea→Sibiu 比 Arad→Sibiu 差）。**Loopy path 是 redundant path 的特例**。
- 解决：
  - **Graph search**：用 **reached** 记住去过哪里，重复的就不再加。
  - **Tree-like search**：**不**检查 reached（省内存）；但可以沿 parent 往上检查，**检测 loopy path**。

---

## Part 3：怎么比较算法？ —— COST

| Criterion | 问题 |
|---|---|
| **C**ompleteness | 有 solution 时保证找到？无 solution 时正确报告 failure？ |
| **O**ptimality (cost-optimal) | 找到的是 path cost 最低的吗？ |
| **S**pace complexity | 需要多少内存？ |
| **T**ime complexity | 要多久？（秒，或考虑的 states/actions 数） |

复杂度用三个量表达（state space 隐式表示时）：
- **b** = branching factor（任何 node 的最大 successor 数）
- **d** = **最浅 goal node** 的深度
- **m** = state space 中任何 path 的**最大深度**

**Big-O**：衡量算法**随输入增长**的速度，描述 **worst case**，不是实际快慢。
O(1) constant < O(log n) logarithmic < O(n) linear < O(n log n) linearithmic < O(n²) quadratic < O(2ⁿ) exponential < O(n!) factorial。
（⚠️ 课件把 O(n log n) 写成 "logarithmic"，是错的，见文末。）

**指数有多可怕**（2B p12：BFS 的时间与内存，b = 10、每秒 1 百万 nodes、每 node 1000 bytes）：

| Depth | Nodes | Time | Memory |
|---|---|---|---|
| 2 | 110 | 0.11 ms | 107 KB |
| 4 | 11,110 | 11 ms | 10.6 MB |
| 6 | 10⁶ | 1.1 s | 1 GB |
| 8 | 10⁸ | 2 min | 103 GB |
| 10 | 10¹⁰ | 3 hours | 10 TB |
| 12 | 10¹² | 13 days | 1 PB |
| 14 | 10¹⁴ | 3.5 years | 99 PB |
| 16 | 10¹⁶ | 350 years | 10 EB |

→ **内存比时间更早成为问题**（d = 12 时 13 天还能等，但 1 PB 内存不可能）；指数复杂度的问题只能靠 uninformed search 解最小的例子。

---

## Part 4：Uninformed (blind) Search —— 只知道"是不是 goal"

**Uninformed search**：除了 problem definition 之外没有任何信息；只能分辨 goal / non-goal，**无法判断哪个 non-goal state 更有希望**。

### 4.1 Breadth-First Search (BFS)

**一层一层**：先 expand root，再 expand root 的所有 successors，再下一层……
- Frontier = **FIFO queue**。
- 使用 **early goal test**：node 一**生成**就检查是不是 goal。（**Late goal test** = pop 出来要 expand 时才检查。）
- Complete（b 有限）；**只有当所有 action cost 相同时才 cost-optimal**；Time = Space = **O(bᵈ)**（生成 1 + b + b² + … + bᵈ 个 nodes）。

课件图（2B p17）：binary tree A → {B, C}，B → {D, E}，C → {F, G}。展开顺序 **A → B → C → D → E → F → G**（同一层全部 expand 完才到下一层；▶ 表示下一个要 expand 的 node）。

课件 pseudocode（2B p18）——注意 goal test 写在**生成 child 时**（early goal test），并用 `reached` 做 graph search：

```
function BREADTH-FIRST-SEARCH(problem) returns a solution node or failure
    node ← NODE(problem.INITIAL)
    if problem.IS-GOAL(node.STATE) then return node
    frontier ← a FIFO queue, with node as an element
    reached ← {problem.INITIAL}
    while not IS-EMPTY(frontier) do
        node ← POP(frontier)
        for each child in EXPAND(problem, node) do
            s ← child.STATE
            if problem.IS-GOAL(s) then return child        ← early goal test
            if s is not in reached then
                add s to reached
                add child to frontier
    return failure
```

**Worked example（Tutorial 3，graph search、early goal test、字母顺序）**：

```
Expanded   Frontier (after expansion)      Reached (new)
—          [A]                              A
A          [B, F]                           B, F
B          [F, C, D]                        C, D
F          [C, D, G, H]   ← max size 4      G, H
C          [D, G, H, E]                     E
D          [G, H, E]                        (B, C, E already reached)
G          [H, E, I]                        I
H          [E, I]                           (F, I reached)
E          J generated → goal! (early goal test) stop
```

```
                A
          ┌─────┴─────┐
          B           F
       ┌──┴──┐     ┌──┴──┐
       C     D     G     H
       │           │
       E           I
       │
       J ✓
```

Solution：**A → B → C → E → J**，cost = 6 + 1 + 5 + 5 = **17**。
- Expanded 8 nodes（A, B, F, C, D, G, H, E）；max frontier = 4。
- 注意：BFS 找到的是**步数最少**的路（4 步），**不是最便宜**的（最便宜是 9）。因为 cost 不相同 → **BFS not cost-optimal here**。

### 4.2 Uniform-Cost Search (UCS) = Dijkstra's algorithm

BFS 只数"步数"，不看"距离"。修正：**每次 expand path cost g(n) 最小的 node**。
- Frontier = **priority queue ordered by g(n)**。
- 使用 **late goal test**（pop 出来时才检查）——因为先生成的 goal 可能不是最便宜的。

课件例（Sibiu → Bucharest）：Sibiu 的 successors：Rimnicu Vilcea 80、Fagaras 99 → expand RV，加入 Pitesti 177 → expand Fagaras，加入 Bucharest 310（**已生成 goal，但继续**）→ expand Pitesti，找到 Bucharest 278 < 310，**替换** → pop Bucharest 278 → 返回。

- Complete（b 有限且每个 action cost ≥ ε > 0）；**cost-optimal**；Time = Space = **O(b^(1+⌊C\*/ε⌋))**，C\* = optimal cost。

课件 pseudocode（2B p25–26）——UCS 就是 **BEST-FIRST-SEARCH 用 f = PATH-COST (g)**。同一个 BEST-FIRST-SEARCH 换 f 就变成 Greedy（f = h）或 A\*（f = g + h）：

```
function EXPAND(problem, node) yields nodes
    s ← node.STATE
    for each action in problem.ACTIONS(s) do
        s' ← problem.RESULT(s, action)
        cost ← node.PATH-COST + problem.ACTION-COST(s, action, s')
        yield NODE(STATE=s', PARENT=node, ACTION=action, PATH-COST=cost)

function UNIFORM-COST-SEARCH(problem) returns a solution node, or failure
    return BEST-FIRST-SEARCH(problem, PATH-COST)

function BEST-FIRST-SEARCH(problem, f) returns a solution node or failure
    node ← NODE(STATE=problem.INITIAL)
    frontier ← a priority queue ordered by f, with node as an element
    reached ← a lookup table, with one entry with key problem.INITIAL and value node
    while not IS-EMPTY(frontier) do
        node ← POP(frontier)
        if problem.IS-GOAL(node.STATE) then return node          ← late goal test
        for each child in EXPAND(problem, node) do
            s ← child.STATE
            if s is not in reached or child.PATH-COST < reached[s].PATH-COST then
                reached[s] ← child                                ← 找到更便宜的路就替换
                add child to frontier
    return failure
```

对照课件 Sibiu→Bucharest 例子（2B p22）：`child.PATH-COST < reached[s].PATH-COST` 这一行就是 "Bucharest 278 < 310，替换" 那一步。

**Worked example（Tutorial 5，graph search、late goal test、同 cost 按字母）**：

```
Pop (g)    Frontier after (g)                         备注
A 0        F3, B6
F 3        G5, B6, H10
G 5        B6, I8, H10
B 6        C7, D8, I8, H10
C 7        D8, I8, H10, E12                          D via C = 8, 不比 8 好 → 不更新
D 8        I8, E9, H10                               E: 8+1=9 < 12 → 更新 (D, I 同 8 → 字母 D 先)
I 8        E9, J9, H10                               H via I = 11 > 10 不更新
E 9        J9, H10                                   E, J 同 9 → 字母 E 先
J 9        → goal popped ✓
```

Solution：**A → F → G → I → J**，cost = 3 + 2 + 3 + 1 = **9**（optimal）。Expanded 8 nodes，max frontier 4。

### 4.3 Depth-First Search (DFS)

**永远 expand frontier 中最深的 node**，一路走到底，没路了再退回（back up）到下一个还有未 expand successor 的最深 node。
- Frontier = **LIFO queue (stack)**。
- 通常实现成 **tree-like search**（不存 reached）。
- **Complete**：finite tree-shaped / finite acyclic state space；finite cyclic 且**检查 cycle** 时。**Incomplete**：infinite state space。
- **Not cost-optimal**；Time **O(bᵐ)**；Space **O(bm)**（**linear**——这是它最大的优点）。

课件的 12 步图（2B p28–30），binary tree A → B, C；B → D, E；C → F, G；D → H, I；E → J, K；F → L, M；G → N, O；**goal = M**：

```
Step  expand   frontier (stack, top on the left)      说明
1     A        B C
2     B        D E C
3     D        H I E C
4     H        I E C                                  H 没有 successors (leaf)
5     I        E C                                    H 已从记忆中删除（DFS 不存 reached）
6     E        J K C                                  back up 到下一个最深、还有未 expand successor 的 node
7     J        K C
8     K        C                                      B 的整棵 subtree 探索完，从记忆中删除
9     C        F G
10    F        L M G
11    L        M G
12    M        → goal ✓
```
重点：已探索完的 subtree **会被丢掉**（图中变淡），所以 DFS 只需记住一条路径 + 路上各 node 未 expand 的兄弟 → O(bm)。

课件对比图（2B p31）：同一棵树 0 → {1, 2}，1 → {3, 4}，2 → {5, 6}：**BFS 顺序 0, 1, 2, 3, 4, 5, 6**（一层一层）；**DFS 顺序 0, 1, 3, 4, 2, 5, 6**（一路到底再回头）。

**Worked example（Tutorial 5，tree-like、late goal test、检测 loopy path、字母顺序）**：

```
A
├── B
│   ├── C
│   │   ├── D
│   │   │   └── E
│   │   │       ├── I
│   │   │       │   ├── G ─ F ─ H   (dead end: all neighbours on path)
│   │   │       │   ├── H ─ F ─ G   (dead end)
│   │   │       │   └── J ✓
│   │   │       └── J   (never popped)
│   │   └── E  (never popped)
│   └── D  (never popped)
└── F  (never popped)
```

Solution：**A → B → C → D → E → I → J**，cost = 6 + 1 + 1 + 1 + 5 + 1 = **15**（不是 optimal）。
Expanded：A, B, C, D, E, I, G, F, H, H, F, G = 12 nodes。

### 4.4 Backtracking, Depth-Limited, Iterative Deepening, Bidirectional

**Backtracking search**（DFS 的变体）：一次只生成**一个** successor，每个 node 记住下一个要生成哪个 → 内存从 O(bm) 降到 **O(m)**。

**Depth-Limited Search (DLS)**：DFS 在无限深的树里会一直往下走。修正：设定深度上限 **l**。
- 找不到时返回 **cutoff**（不是 failure）。
- Incomplete if **l < d**；not cost-optimal（例如 l > d 时）；Time O(bˡ)，Space O(bl)。
- 选 l：Romania 有 20 城 → l = 19 有效；更好的是 **diameter**（任两城最多 9 步可达）→ l = 9。但大多数问题事前不知道好的 l。

课件 DLS 图（2C p4）：l = 1 时，从 A 往下到 B（深度 1）就不能再往下，D、E 不会被生成 → 返回 cutoff。

课件 pseudocode（2C p8）：

```
function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution node or failure
    for depth = 0 to ∞ do
        result ← DEPTH-LIMITED-SEARCH(problem, depth)
        if result ≠ cutoff then return result

function DEPTH-LIMITED-SEARCH(problem, ℓ) returns a node or failure or cutoff
    frontier ← a LIFO queue (stack) with NODE(problem.INITIAL) as an element
    result ← failure
    while not IS-EMPTY(frontier) do
        node ← POP(frontier)
        if problem.IS-GOAL(node.STATE) then return node
        if DEPTH(node) > ℓ then
            result ← cutoff                         ← 太深，不 expand，记下"被截断过"
        else if not IS-CYCLE(node) do               ← 沿 parent 检查 loopy path
            for each child in EXPAND(problem, node) do
                add child to frontier
    return result
```
- 只要有 node 被截断过就返回 **cutoff**（"加深也许找得到"）；整棵树都搜完仍没有 → **failure**（"真的无解"）。IDS 只在 result ≠ cutoff 时停。

课件 IDS 图（2C p9–10，binary tree，goal = M）：
- **Limit 0**：只看 A。
- **Limit 1**：A → B → C。
- **Limit 2**：A → B → D → E → C → F → G。
- **Limit 3**：A → B → D → H → I → E → J → K → C → F → L → **M ✓**（找到 goal）。
每一轮都**从 root 重新开始**，上层 nodes 被重复生成。

**Iterative Deepening Search (IDS)**：不知道 l？**l = 0, 1, 2, … 逐步加大**，直到找到最浅的 goal（深度 d）。找不到返回 **failure**。
- 结合 DFS 与 BFS 的优点：**Space O(bd)**（像 DFS，linear）；**complete**（finite acyclic）、**cost-optimal if all action costs equal**（像 BFS）；Time **O(bᵈ)**。
- 会浪费吗？上层 nodes 被重复生成，但**大部分 nodes 在最底层**，所以浪费很少：

```
N(IDS) = (d)b + (d−1)b² + … + (1)bᵈ
b = 10, d = 5:
N(IDS) = 50 + 400 + 3,000 + 20,000 + 100,000 = 123,450
N(BFS) = 1 + 10 + 100 + 1,000 + 10,000 + 100,000 = 111,111
```
→ **当 search space 大、solution 深度未知时，IDS 是首选的 uninformed search**。

**Tutorial 5 map 上的 IDS（tree-like、late goal test）**：l = 0, 1, 2, 3 都找不到；**l = 4** 时先走 A→B→C→D→E（E 在深度 4，不是 goal，cutoff），退回 C 再走 C→E→J（J 在深度 4）找到 **A → B → C → E → J**，cost **17**（和 BFS 一样：最浅，但不最便宜）。

**Bidirectional search**：同时跑两个搜索——从 initial state **往前**，从 goal **往后**，希望在中间相遇（两个 frontier 碰撞）。动机：**b^(d/2) + b^(d/2) ≪ bᵈ**（b = 10、d = 6 时 BFS 要 1,111,111 nodes，下半部分比上半部分多约 1000 倍）。需要能"往回推"（predecessor）。两边都用 BFS 时：complete（b 有限）、cost-optimal（cost 相同）、Time & Space **O(b^(d/2))**。

### 4.5 Uninformed search 总表（背这张）

| Criterion | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| Complete? | Yes¹ | Yes¹,² | No | No | Yes¹ | Yes¹,⁴ |
| Cost-optimal? | Yes³ | Yes | No | No | Yes³ | Yes³,⁴ |
| Time | O(bᵈ) | O(b^(1+⌊C\*/ε⌋)) | O(bᵐ) | O(bˡ) | O(bᵈ) | O(b^(d/2)) |
| Space | O(bᵈ) | O(b^(1+⌊C\*/ε⌋)) | **O(bm)** | O(bl) | **O(bd)** | O(b^(d/2)) |

¹ b finite（且 state space finite 或有 solution）· ² all action costs ≥ ε > 0 · ³ all action costs identical · ⁴ both directions use BFS or UCS

---

## Part 5：Informed (heuristic) Search —— 给 agent 一个"方向感"

UCS 找到了最便宜的路，但它**往四面八方同样努力地找**（它连 B、C、D、E 都 expand 了，其实那边离 J 很远）。
如果 agent 能**估计**每个城市离 J 有多远，就可以优先往"看起来近"的方向走。

### 5.1 Heuristic function

**h(n) = estimated cost of the cheapest path from the state at node n to a goal state.**
例：**straight-line distance h_SLD**。注意 h 的值**不能从 problem description（ACTIONS、RESULT）算出来**——是额外的知识。

**Informed vs Uninformed（tutorial 考 3 differences）**：

| | Uninformed (blind) | Informed (heuristic) |
|---|---|---|
| 信息 | 只有 problem definition | 额外的 heuristic h(n) |
| 能否比较 non-goal states | 不能 | 能判断哪个 "more promising" |
| 效率 | 较低，探索很多无关路径，耗时耗内存 | 通常更快、搜索空间更小 |
| 例子 | BFS, UCS, DFS, DLS, IDS, bidirectional | Greedy best-first, A\* |

**Best-first search**：用 evaluation function **f(n)** 选 node，**f 最小的先 expand**。不同 informed search 只差在 f 的选法。

### 5.2 Greedy Best-First Search：f(n) = h(n)

只看"离 goal 看起来多近"→ 贪心。
- Priority queue ordered by **h**（UCS 是 g）。
- Tree-like 版本在 finite space 也 **incomplete**（会绕圈）；graph 版本在 finite space **complete**。**Not cost-optimal**。
- Time O(bᵐ)（好的 heuristic 可降到 O(bm)）；Space O(bm) tree-like / O(bᵐ) graph。

**课件例子：Romania, Arad → Bucharest（2C p30–32）**，每个 node 下面是 h_SLD：

```
(a) Arad 366
(b) expand Arad    → Sibiu 253 ▶, Timisoara 329, Zerind 374
(c) expand Sibiu   → Arad 366, Fagaras 176 ▶, Oradea 380, Rimnicu Vilcea 193
(d) expand Fagaras → Sibiu 253, Bucharest 0 ▶  → goal

                     Arad
          ┌───────────┼────────────┐
       Sibiu 253   Timisoara 329  Zerind 374
   ┌──────┼──────┬────────┐
 Arad   Fagaras  Oradea  Rimnicu Vilcea
 366     176     380      193
       ┌──┴───┐
    Sibiu   Bucharest 0 ✓
     253
```

Solution：Arad → Sibiu → Fagaras → Bucharest，cost = 140 + 99 + 211 = **450**。
非常快（只 expand 3 个 nodes），但**不是 optimal**：经过 Rimnicu Vilcea、Pitesti 的路只要 **418**（便宜 32 km）。这就是 greedy 的问题——只看"离 goal 多近"，不管"已经走了多远"。

**Worked example（Tutorial 6，tree-like、late goal test、检测 loopy path）**：

```
Pop (h)   Frontier after (h)
A 10      F6, B8
F 6       H3, G5, B8
H 3       I1, G5, B8
I 1       J0, E3, G5, G5, B8
J 0       → goal ✓
```

```
             A(10)
          ┌────┴────┐
        B(8)       F(6)
                 ┌──┴──┐
               G(5)   H(3)
                        │
                      I(1)
                   ┌───┼───┐
                 E(3) G(5) J(0) ✓
```

Solution：**A → F → H → I → J**，cost = 3 + 7 + 3 + 1 = **14** ✗（贪心走了 F→H 那条 7 的长边）。Expanded 4 nodes（A, F, H, I）；max frontier 5。

### 5.3 A\* Search：f(n) = g(n) + h(n)

把 UCS 的"已经走了多远 g"和 Greedy 的"估计还剩多远 h"加起来：
**f(n) = g(n) + h(n) = 经过 n 的最便宜 solution 的估计 cost**。
- Priority queue ordered by **g + h**。
- Complete（b 有限、每个 cost ≥ ε > 0）；**cost-optimal if h is admissible（tree search）/ consistent（graph search）**；Time & Space 仍是指数。
- **Pruning**：A\* 不会 expand f > C\* 的 nodes（例：Timisoara f = 447、Zerind f = 449 从来没被 expand）。Heuristic 越好，prune 越多。

**课件例子：Romania, Arad → Bucharest（2C p37–41）**，每个 node 写成 **f = g + h**：

```
Step  expand            new nodes (f = g + h)                                     frontier 最小
(a)   —                 Arad 366 = 0 + 366
(b)   Arad              Sibiu 393 = 140+253, Timisoara 447 = 118+329,             Sibiu 393
                        Zerind 449 = 75+374
(c)   Sibiu             Arad 646 = 280+366, Fagaras 415 = 239+176,                RV 413
                        Oradea 671 = 291+380, Rimnicu Vilcea 413 = 220+193
(d)   Rimnicu Vilcea    Craiova 526 = 366+160, Pitesti 417 = 317+100,             Fagaras 415
                        Sibiu 553 = 300+253
(e)   Fagaras           Sibiu 591 = 338+253, Bucharest 450 = 450+0                Pitesti 417
(f)   Pitesti           Bucharest 418 = 418+0, Craiova 615 = 455+160,             Bucharest 418
                        Rimnicu Vilcea 607 = 414+193
(g)   Bucharest 418 popped → goal ✓
```

```
                                   Arad
            ┌───────────────────────┼─────────────────────┐
        Sibiu 393              Timisoara 447           Zerind 449
   ┌─────────┼───────────┬──────────────────┐
 Arad 646  Fagaras 415  Oradea 671   Rimnicu Vilcea 413
          ┌────┴─────┐          ┌────────────┼────────────┐
      Sibiu 591  Bucharest 450  Craiova 526  Pitesti 417  Sibiu 553
                                        ┌────────┼──────────┐
                                  Bucharest 418  Craiova 615  RV 607
```

重点：
- 在 (e) **Bucharest 450 已经被生成**，但 A\* 用 late goal test，不马上返回；因为 Pitesti 417 < 450，先 expand Pitesti，找到 **Bucharest 418**。
- Solution：**Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest = 140 + 80 + 97 + 101 = 418**（optimal；Greedy 给的是 450）。

**Worked example（Tutorial 6，graph search、late goal test）**：

```
Pop (f=g+h)     Frontier after
A (0+10=10)     F(3+6=9), B(6+8=14)
F (3+6=9)       G(5+5=10), H(10+3=13), B14
G (5+5=10)      I(8+1=9), H13, B14
I (8+1=9)       J(9+0=9), H13, B14, E(13+3=16)     H via I = 11+3=14 → worse, ignored
J (9+0=9)       → goal ✓
```

```
                 A 0+10=10
            ┌──────┴──────┐
       B 6+8=14        F 3+6=9
                     ┌────┴────┐
                G 5+5=10    H 10+3=13
                     │
                I 8+1=9
                 ┌───┴───┐
            E 13+3=16  J 9+0=9 ✓
```

Solution：**A → F → G → I → J**，cost **9**（optimal，和 UCS 一样），但只 expand 了 4 个 nodes（UCS 要 8 个）→ **这就是 heuristic 的价值**。

**六种算法在同一张地图上的比较**（time = expanded nodes，space = max frontier）：

| Algorithm | Solution | Cost | Optimal? | Expanded |
|---|---|---|---|---|
| BFS (graph, early) | A-B-C-E-J | 17 | ✗ | 8 |
| DFS (tree, late) | A-B-C-D-E-I-J | 15 | ✗ | 12 |
| IDS (tree, late) | A-B-C-E-J | 17 | ✗ | 16（l=1:1, l=2:3, l=3:7, l=4:5，上层重复 expand） |
| UCS (graph, late) | A-F-G-I-J | 9 | ✓ | 8 |
| Greedy (tree, late) | A-F-H-I-J | 14 | ✗ | 4 |
| **A\*** (graph, late) | A-F-G-I-J | 9 | ✓ | **4** |

→ 结论（tutorial "select ONE strategy"）：**A\***，因为和 UCS 一样 complete + cost-optimal，但 expand 的 nodes 少得多（更快）。

### 5.4 Admissibility 与 Consistency

**Admissible**：**never overestimates** the cost to reach the goal：h(n) ≤ h\*(n)（h\* = 真实最便宜 cost）。
例：h_SLD 是 admissible，因为两点之间直线最短，不可能高估。
→ A\*（tree search）用 admissible h 一定 cost-optimal。

**证明思路（tutorial）**：设 optimal cost 为 C\*。若 A\* 返回一个 cost C > C\* 的 goal，则 optimal path 上必有某个未 expand 的 node n，f(n) = g(n) + h(n) ≤ g(n) + h\*(n) = C\* < C。A\* 总是先 pop f 最小的，所以会先 expand n 而不是那个较贵的 goal → 矛盾。

**Consistent (monotonic)**：对每个 node n 和它经 action a 到达的 successor n'：

```
h(n) ≤ c(n, a, n') + h(n')        ← 三角不等式 (triangle inequality)
```

例：n = Arad、n' = Sibiu：h(Arad) = 366 ≤ c = 140 + h(Sibiu) = 253 → 393 ✓。
- Consistency 比 admissibility **稍强**：consistent ⇒ admissible（反之不一定）。
- 意义：f 沿着任何路径**不会减少**，所以 A\* graph search 第一次 pop 某个 state 时就已经是最便宜的路径，不需要重新打开。

⚠️ **小提醒**：tutorial 地图的 h 其实**不 admissible**（h(A)=10 > 真实 9；h(D)=7 > 6；h(G)=5 > 4），但这张图上 A\* 还是找到了 optimal。考试时**照题目给的 h 计算就好**，除非题目问你判断 admissible。

---

## Closing the loop

回到巴士：司机要"最短的路"。
- 只数站数的 **BFS** 给了 17 km 的路；**DFS** 一路钻到底给了 15 km；**Greedy** 太贪心给了 14 km。
- **UCS** 和 **A\*** 都给了真正最短的 **A→F→G→I→J = 9 km**，但 A\* 只看了一半的站。

可是这些方法都要**记住整条路**（frontier 很大）。如果我们根本**不关心路径**、只关心**最终状态**呢？例如排课表、摆 8 个 queen——只要最后那张表/棋盘是好的就行。那就需要完全不同的搜索方式：**local search**（Chapter 3）。

---

## ⚠️ Where the slides mislead

| Slide | 课件写法 | 更准确的理解 |
|---|---|---|
| 2B Big-O | "Logarithmic time: O(n log n)" | Logarithmic = **O(log n)**；O(n log n) 叫 **linearithmic**。 |
| 2C Bidirectional | "Space complexity: **Linear** complexity O(b^(d/2))" | O(b^(d/2)) 仍是 **exponential**，只是比 O(bᵈ) 小很多。 |
| 2C IDS | "a general strategy, used to find the diameter" | IDS 是用来**找出最适合的 depth limit**（逐步加深直到 d），不是专门求 diameter。 |
| 2A Search Tree | "Suppose Sibiu is chonse... run a goal test on Sibiu" | 那是 late goal test 的做法；BFS 用 early goal test。考试注意题目给的 goal test 类型。 |
| Tutorial 3 答案 | 4 phases 写 "Solution Formulation" | 应为 **Search**。 |

---

## Exam radar

| Paper | 题目 | 分数 |
|---|---|---|
| Oct 2025 Q3 | formulation 6 components (6) · BFS/DFS/A\* search trees (4+4+8) · 三个 solution (3) | **25** |
| Jan 2026 Q4 | formulation (6) · BFS/DFS/A\* trees (16) · solutions (3) | **25** |
| May 2026 Q2d | A\* search tree (8) · search path vs solution path (2) · total cost (1) | **11** |

**考试画树的规矩（这门课的惯例）**：
1. 每个 node 标 **g + h = f**（A\*）；用 [1], [2]… 标 **expansion order**。
2. 按题目说的 **alphabetical order** 生成 children。
3. 没说 tree / graph 时，写一句你的假设（例："graph search, late goal test for A\*, early goal test for BFS"）。
4. **"Search path explored"** = 节点被 expand 的顺序；**"solution path"** = 从 root 到 goal 的那一条。

### 📝 Oct 2025 Q3（Station A → I）

图（directed）：A→B 9, A→C 14, B→E 17, B→F 17, C→D 6, D→H 3, E→G 12, F→I 2, G→H 6, H→I 2。
h：A9 B8 C10 D8 E7 F4 G2 H4 I1。

**BFS**（graph search, early goal test, alphabetical）

```
                A [1]
          ┌─────┴─────┐
        B [2]        C [3]
      ┌──┴──┐          │
    E [4]  F [5]      D
     │      │
     G      I ✓  (goal detected when generated)
```
Expansion order：A, B, C, E, F。Solution **A → B → F → I**，cost 9 + 17 + 2 = **28**。
（用 late goal test 也得到同一个 solution，只是多 expand D、G。）

**DFS**（tree-like, alphabetical）

```
A [1]
├── B [2]
│   ├── E [3]
│   │   └── G [4]
│   │       └── H [5]
│   │           └── I ✓
│   └── F
└── C
```
Solution **A → B → E → G → H → I**，cost 9 + 17 + 12 + 6 + 2 = **46**。

**A\***（graph search, late goal test）

```
Pop (f)          Frontier after
A 0+9=9          B 9+8=17, C 14+10=24
B 9+8=17         C24, F 26+4=30, E 26+7=33
C 14+10=24       D 20+8=28, F30, E33
D 20+8=28        H 23+4=27, F30, E33
H 23+4=27        I 25+1=26, F30, E33
I 25+1=26        → goal ✓
```

```
                          A 0+9=9 [1]
               ┌─────────────┴─────────────┐
          B 9+8=17 [2]               C 14+10=24 [3]
          ┌────┴─────┐                     │
    E 26+7=33   F 26+4=30            D 20+8=28 [4]
                                           │
                                     H 23+4=27 [5]
                                           │
                                     I 25+1=26 [6] ✓
```
Solution **A → C → D → H → I**，cost 14 + 6 + 3 + 2 = **25**（optimal；BFS 28、DFS 46）。

⚠️ 题目的 h(I) = 1（goal 的 heuristic 通常应为 0），严格来说这个 h 在 I 上 overestimate（真实 cost 0）。不影响计算，照表格算即可。

### 📝 Jan 2026 Q4（Access Point A → I）

图（directed）：A→B 4, A→C 5, A→D 8, B→E 6, C→F 7, F→E 7, F→G 3, E→G 13, D→H 2, G→H 16, G→I 8, H→I 6。
h：A13 B17 C6 D9 E19 F7 G6 H9 I0。

**BFS**（graph, early goal test）

```
                  A [1]
       ┌──────────┼──────────┐
     B [2]      C [3]      D [4]
       │          │          │
     E [5]      F [6]      H [7]
       │     (E, G already        │
       G      reached → skip)     I ✓
```
Expansion order：A, B, C, D, E, F, H。Solution **A → D → H → I**，cost 8 + 2 + 6 = **16**。

**DFS**（tree-like, late goal test, alphabetical）

```
A [1]
├── B [2]
│   └── E [3]
│       └── G [4]
│           ├── H [5]
│           │   └── I ✓
│           └── I
├── C
└── D
```
Solution **A → B → E → G → H → I**，cost 4 + 6 + 13 + 16 + 6 = **45**。
（若用 early goal test：expand G 时就生成 I → **A → B → E → G → I**，cost 31。考试写明你用哪一种。）

**A\***（graph, late goal test；f 相同按字母）

```
Pop (f)          Frontier after
A 0+13=13        C 5+6=11, D 8+9=17, B 4+17=21
C 5+6=11         D17, F 12+7=19, B21
D 8+9=17         F19, H 10+9=19, B21          (F, H 同 19 → 字母 F 先)
F 12+7=19        H19, B21, G 15+6=21, E 19+19=38
H 10+9=19        I 16+0=16, B21, G21, E38
I 16+0=16        → goal ✓
```

```
                              A 0+13=13 [1]
          ┌───────────────────────┼────────────────────────┐
     B 4+17=21               C 5+6=11 [2]             D 8+9=17 [3]
                                  │                         │
                           F 12+7=19 [4]              H 10+9=19 [5]
                            ┌─────┴─────┐                   │
                     E 19+19=38     G 15+6=21         I 16+0=16 [6] ✓
```
Solution **A → D → H → I**，cost **16**（optimal）。

📝 **Q4c solutions**：BFS → A-D-H-I (16)；DFS → A-B-E-G-H-I (45)；A\* → A-D-H-I (16)。

### 📝 May 2026 Q2d（TAR-GPS, Station A → H）

图（directed）：A→B 9, A→D 16, A→E 13, B→C 13, C→D 11, D→F 15, E→G 7, F→H 17, G→H 18。
h：A8 B11 C9 D6 E4 F2 G3 H0。

```
Pop (f)          Frontier after
A 0+8=8          E 13+4=17, B 9+11=20, D 16+6=22
E 13+4=17        B20, D22, G 20+3=23
B 9+11=20        D22, G23, C 22+9=31
D 16+6=22        G23, C31, F 31+2=33
G 20+3=23        C31, F33, H 38+0=38
C 22+9=31        F33, H38              (C→D: g=33 > 16 已 reached → discard)
F 31+2=33        H38                   (F→H: g=48 > 38 → discard)
H 38+0=38        → goal ✓
```

```
                                A 0+8=8 [1]
            ┌────────────────────┼──────────────────────┐
     B 9+11=20 [3]         D 16+6=22 [4]          E 13+4=17 [2]
            │                    │                      │
     C 22+9=31 [6]         F 31+2=33 [7]          G 20+3=23 [5]
            │                    │                      │
     D 33+6=39 ✗           H 48+0=48 ✗            H 38+0=38 [8] ✓
```
（✗ = graph search 丢弃；若当 tree search 画，这两个会留在 frontier 但永远不会在 H(38) 之前被 pop，答案一样。）

- **(ii) Search path explored**：A → E → B → D → G → C → F → H。
- **Solution path returned**：**A → E → G → H**。
- **(iii) Total cost** = 13 + 7 + 18 = **38 km**。

---

## Cheat sheet

| 项目 | 要点 |
|---|---|
| 4 phases | goal formulation → problem formulation → search → execution |
| 6 components | states, initial state, goal state, actions ACTIONS(s), transition model RESULT(s,a), cost ACTION-COST(s,a,s') |
| Abstraction | valid + useful |
| Frontier / reached / explored | unexpanded / any generated state / expanded |
| Node fields | STATE, PARENT, ACTION, PATH-COST |
| Queues | FIFO → BFS · LIFO → DFS · priority → UCS/Greedy/A\* |
| Loopy ⊂ redundant | graph search (reached) fixes both |
| COST | Completeness, Optimality, Space, Time |
| b, d, m | branching factor, depth of shallowest goal, max depth |
| BFS | FIFO, early goal test, O(bᵈ), optimal only if equal costs |
| UCS | priority by g, late goal test, optimal |
| DFS | LIFO, O(bm) space, not optimal, incomplete in infinite spaces |
| DLS / IDS | limit l, cutoff / increase l gradually, O(bd) space |
| Bidirectional | two searches meet in middle, O(b^(d/2)) |
| Greedy | f = h, not optimal |
| A\* | f = g + h, optimal if admissible / consistent |
| Admissible | h(n) ≤ true cost (never overestimates) |
| Consistent | h(n) ≤ c(n,a,n') + h(n') |

---

## Practice (answers included)

### A. MCQ

1. Which search uses a LIFO queue? (a) BFS (b) UCS (c) DFS (d) A\*
2. BFS is cost-optimal when: (a) always (b) h is admissible (c) all action costs are equal (d) the tree is finite
3. Space complexity of IDS: (a) O(bᵈ) (b) O(bd) (c) O(b^(d/2)) (d) O(bᵐ)
4. Greedy best-first search orders its priority queue by: (a) g (b) h (c) g + h (d) depth
5. A heuristic that never overestimates the true cost is: (a) consistent (b) admissible (c) monotonic (d) optimal

**Answers**：1 (c) · 2 (c) · 3 (b) · 4 (b) · 5 (b)

### B. Short answer

**B1.** Differentiate BFS and UCS in two ways.
> (1) BFS expands the shallowest node (level by level, by number of steps); UCS expands the node with the lowest path cost g(n). (2) BFS uses a FIFO queue with an early goal test and is optimal only when all action costs are equal; UCS uses a priority queue ordered by g(n) with a late goal test and is always cost-optimal (costs ≥ ε > 0).

**B2.** Why does UCS use a late goal test instead of an early one?
> A goal node generated early may not be on the cheapest path (e.g. Bucharest first generated with cost 310, later found with 278). Testing only when the node is popped guarantees it has the lowest g among all frontier nodes, so the returned solution is optimal.

**B3.** Explain why IDS does not waste much time even though it regenerates nodes.
> Most nodes are at the bottom level. Nodes at depth d are generated once, depth d−1 twice, …, the root d times. With b = 10, d = 5: IDS generates 123,450 nodes vs BFS 111,111 — only about 11% more — while using only O(bd) memory.

### C. Calculation

**C1.** A small graph: S→A 1, S→B 4, A→B 2, A→G 12, B→G 5. h: S 7, A 6, B 4, G 0. Run A\* (graph search).

> ```
> Pop S 0+7=7   → A 1+6=7, B 4+4=8
> Pop A 1+6=7   → B via A: g=3 < 4 → update B 3+4=7; G 13+0=13
> Pop B 3+4=7   → G via B: g=8 < 13 → update G 8+0=8
> Pop G 8       → goal
> ```
> Solution S → A → B → G, cost 1 + 2 + 5 = **8**.
> Check: h admissible? true costs: S 8, A 7, B 5 → 7 ≤ 8, 6 ≤ 7, 4 ≤ 5 ✓.

**C2.** For the same graph, run greedy best-first search (graph search).
> Pop S (h7) → A6, B4; pop B (h4) → G0; pop G → goal. Solution S → B → G, cost 4 + 5 = **9** (not optimal; A\* found 8).

### D. Thinking

**D1.** Is h(n) = 0 for all n admissible? What does A\* become?
> Yes – 0 never overestimates. f = g + 0 = g, so A\* becomes **uniform-cost search**: still optimal, but loses the efficiency of a good heuristic.

**D2.** Why is DFS preferred over BFS for memory, but not for optimality?
> DFS only stores a single path plus unexpanded siblings, O(bm) (linear), while BFS stores whole levels, O(bᵈ). However, DFS returns the first goal found along a deep branch, which may be far from the cheapest, and can get lost in infinite branches.
