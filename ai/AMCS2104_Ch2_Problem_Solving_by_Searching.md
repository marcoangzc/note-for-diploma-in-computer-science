# AMCS2104 — Chapter 2 (2A + 2B + 2C): Solving Problems by Searching

> Slide 的问题：算法伪代码和搜索树例子几乎都是图，没有逐步解释；复杂度只给结论；有几处明确的错误（bidirectional 的 space 被写成 "linear"、IDS "find the diameter"、O(n log n) 被叫 logarithmic）。这份笔记把每个例子的 trace 补出来，所有数字都用代码在 Romania 地图上重新算过。
> ⚠️ 你的 slide 里 2B 后半标题是 "Chapter 3B: Uninformed Search"，2C 后半是 "Chapter 3E: Informed Search"，这是从原课件（课本 Ch3）拆出来的编号，内容属于本章。

---

## 0. 一句话总览

把问题变成**在状态空间里找一条从 initial state 到 goal state 的路径**，然后用不同策略决定**下一个展开哪个节点**：不用任何额外信息（uninformed：BFS、UCS、DFS、DLS、IDS、Bidirectional），或者用 heuristic 估计距离（informed：Greedy、A*）。

| 部分 | 内容 |
|---|---|
| 2A | Problem-solving agent；problem formulation 6 要素；abstraction；standardized problems；search tree、frontier、reached；redundant / loopy paths |
| 2B | 4 个评价标准；b、d、m；Big-O；BFS、UCS、DFS |
| 2C | Backtracking、Depth-limited、Iterative deepening、Bidirectional；Best-first、Greedy、A*、admissible、consistent |

---

## 1. (2A) Problem-solving agent

**Problem-solving agent** = 一种 goal-based agent，找一串 action 达成 goal；环境状态用 **atomic representation**（每个状态是不可分的整体）。

**4 个阶段**：Goal formulation → Problem formulation → Solution searching → Solution execution。

- **Goal formulation**：先决定要达成什么（例："从 Arad 开车到 Bucharest"）。goal 限制了要考虑的目标和动作。
- **Problem formulation**：决定要考虑哪些 states 和 actions。
- **Search**：agent 在**自己的模型里模拟**动作序列，直到找到到达 goal 的序列（solution），或发现无解。
- **Execute**：一个一个执行 solution 里的动作。

slide 10–11 的两个场景：① agent 不熟悉 Romania 地图 → 不知道哪个动作导致哪个状态，无从选择；② agent 有地图 → 可以在脑中"假想一趟旅程"。**slide 假设环境是** episodic、single agent、fully observable、deterministic、static、discrete、known（Ch1C 的 7 个维度），所以 solution 是一个**固定的动作序列**（不用边走边看，"闭着眼睛执行"都行）。

---

## 2. Problem formulation：6 个要素

| 要素 | 意思 | Romania 例子 |
|---|---|---|
| States | 所有可能的状态（state space） | 20 个城市 |
| Initial state | 起点 | Arad |
| Goal state | 目标 | Bucharest |
| Actions | `ACTIONS(s)`：s 里能做的动作 | ACTIONS(Arad) = {ToSibiu, ToTimisoara, ToZerind} |
| Transition model | `RESULT(s,a)`：动作的结果 | RESULT(Arad, ToZerind) = Zerind |
| Cost function | `ACTION-COST(s,a,s')` | 路程（英里）或时间 |

- **Path** = 动作序列；**solution** = 从 initial state 到 goal state 的 path；**optimal solution** = 所有 solution 里 path cost 最低的。
- 假设 action costs 是**可加**的：path cost = 各步 cost 之和。
- **State space graph**：顶点 = states，边 = actions。（slide 17 说 "directed edges"；Romania 的路是双向的，所以每条路 = 两条方向相反的边。）

我数了地图（slide 8）：**20 个城市、23 条路**。

### Abstraction

现实世界的路线包含天气、路况、听什么音乐……**abstraction = 去掉细节**。"State = 在哪个城市"、"action = 开到相邻城市"都是抽象。

- **Valid**：任何抽象层的 solution 都可以展开成更详细世界里的 solution。
- **Useful**：执行抽象 solution 的每一步比原问题容易。
- 好的 abstraction：**尽量删细节，同时保持 valid 而且抽象动作容易执行**。

---

## 3. Standardized problems（slide 23–35）

Standardized problem 用来展示 / 测试算法、描述简洁精确、可当 benchmark；real-world problem 的定义则因人而异（例：Waze 的导航、VLSI layout、TSP、robot navigation、automatic assembly sequencing）。

### 3.1 Vacuum world

- State = agent 位置 × 每格有没有 dirt。2 格：2 × 2² = **8** 个 states；n 格：n × 2ⁿ。
- Goal：每格都干净。Actions：Left、Right、Suck；每个 action cost 1。
- Transition：Suck 清除当前格灰尘（本来就干净就没变化）；Left / Right 撞墙就留在原地。

### 3.2 8-Puzzle

- State = 8 块 tile + 空格的位置；action = **移动空格**（Left / Right / Up / Down），cost 1。
- 可达状态数 = 9!/2 = **181,440**（代码算出）；n 块 tile 的版本是 (n+1)!/2 。例：15-puzzle ≈ 1.05 × 10¹³。
- **为什么除以 2**（补充，非 slide 内容）：一半的排列因奇偶性无法从另一半到达。

### 3.3 8-Queens

关键是**同一个问题有不同的 formulation，状态数差别巨大**：

| Formulation | 状态 | 数量（代码验证） |
|---|---|---|
| **Incremental**（从空盘开始，每步放一个 queen） | 任意放置 | 64×63×…×57 ≈ **1.8 × 10¹⁴** |
| **Complete-state**（8 个 queen 都在盘上，每列一个） | 每列选一个行 | 8⁸ = 16,777,216 ≈ **1.7 × 10⁷** |
| （补充，非 slide）Incremental 改进：只放不互相攻击的 queen，左到右每列一个 | | 只有 **2,057** 个状态 |

slide 34 的 action "把任何一个 queen 垂直移动到任何空格" 是 **complete-state formulation**。Goal = 8 个 queen 互不攻击（有 **92** 个解，代码验证）。

### 3.4 Airline travel（slide 37–38）

State = (机场, 时间)；action = 搭当前地点当前时间之后的某个航班；transition = 新地点 + 新时间；cost = 金钱 + 飞行时间 + 等待时间 + 海关 + 座位质量……

---

## 4. Search tree、frontier、reached

**Search algorithm**：输入 search problem，输出 solution 或 failure。

- **Search tree**：node = 一个 state，edge = 一个 action，root = initial state。
- **Frontier**（open list）= 已经生成、但**还没展开**的节点集合。
- **Expansion**：对节点应用所有可用 actions；**generation**：产生子节点（child / successor）并放进 frontier。
- **Reached**：任何"曾经生成过节点"的 state（不管有没有展开）。
- **Explored set**（closed list）= 已展开的节点。

⚠️ **常见混淆 Search tree vs State space**（slide 47–49）：state space 里每个 state **只出现一次**；search tree 里同一个 state 可以出现在**很多个节点**（Arad → Sibiu → Arad 又是 Arad）。**Search algorithm 是在 state-space graph 上"叠"出一棵 search tree**。

### Node 的数据结构

`n.STATE`（对应哪个 state）、`n.PARENT`（谁生成了我）、`n.ACTION`（对 parent 做了什么动作）、`n.PATH-COST`（从 root 到我的总 cost）。沿着 PARENT 指针回到 root 就能还原整条路径。

### Frontier 用哪种队列

| 队列 | 弹出 | 用在 |
|---|---|---|
| FIFO queue | 最早放入的 | BFS |
| LIFO queue（stack） | 最晚放入的 | DFS |
| Priority queue | f 值最小的 | Best-first（UCS、Greedy、A*） |

操作：`IS-EMPTY`、`POP`、`ADD`。

### Loopy paths 与 redundant paths

- **Loopy path（cycle）**：路径里有重复的 state，可以让搜索无限循环。
- **Redundant path**：到同一个 state 有更差的路径（Arad–Zerind–Oradea–Sibiu 比 Arad–Sibiu 差）。**loopy path 是 redundant path 的特例。**
- 处理方法：
  - **Graph search**：用 `reached` 记住去过哪里，去过就不再加入 frontier（可能改用更便宜的路径替换）。
  - **Tree-like search**：**不**记 reached，不查 redundant path，简单但可能重复很多。
  - **只查 cycle**：沿着 parent 一路查到 root，看有没有重复（省内存，DFS 常用）。

（补充，非 slide 内容：AIMA 把这些算法统一成 `BEST-FIRST-SEARCH(problem, f)`，只是 f 不同：BFS 用深度、UCS 用 g、Greedy 用 h、A* 用 g+h。slide 29 / 35 说 "Greedy 实现和 UCS 相同，只是排序 g→h；A* 只是排序 g+h" 就是这个意思。）

---

## 5. (2B) 怎么评价一个搜索算法

| 标准 | 问什么 |
|---|---|
| **Completeness** | 有解时保证找到；无解时能正确报告失败？ |
| **Optimality** | 找到的是 cost 最低的解吗？ |
| **Time complexity** | 花多久（或考虑了多少 states / actions） |
| **Space complexity** | 用多少内存 |

图可以完整显式表示时，复杂度用顶点数和边数；只能隐式表示（initial state + actions + transition）时，用：

- **b**：branching factor（一个节点最多有几个 successors）
- **d**：最浅 goal 的深度（depth of the shallowest goal）
- **m**：状态空间里任何路径的最大长度

**Big-O**：描述代价随输入 size 增长的**速度**（不是"多快"），常用来说最坏情况。O(1) 常数、O(n) 线性、O(log n) 对数、O(n log n) 线性对数、O(n²) 平方、O(2ⁿ) 指数、O(n!) 阶乘。

### 指数复杂度有多可怕

b = 10、每秒 100 万节点、每节点 1000 bytes 的 BFS（我用代码按 slide 的假设重算，跟 slide 表吻合）：

| Depth | Nodes | Time | Memory |
|---|---|---|---|
| 2 | 110 | 0.11 ms | 107 KB |
| 4 | 11,110 | 11 ms | 10.6 MB |
| 6 | ~10⁶ | 1.1 s | 1 GB |
| 8 | ~10⁸ | ~2 min | 103 GB |
| 10 | ~10¹⁰ | ~3 hours | 10 TB |
| 12 | ~10¹² | ~13 days | ~1 PB |
| 14 | ~10¹⁴ | ~3.5 years | 99 PB |
| 16 | ~10¹⁶ | 350 years | 10 EB |

**内存比时间更早成为瓶颈**（1 秒能生成的节点，内存要存下来）。**结论**：指数复杂度的问题，uninformed search 只能解最小的实例。

---

## 6. Uninformed（blind）search

只知道问题定义，**只能区分 goal 和 non-goal**，无法判断哪个 non-goal 更接近 goal。

### 6.1 Breadth-First Search（BFS）

**策略**：先展开 root，再展开它所有 successors，再展开它们的 successors……**同一深度全部展开完才进入下一层**。用 **FIFO queue**。

```
BFS(problem):
    node ← root; if goal(node) return node          # early goal test
    frontier ← FIFO{node};  reached ← {initial}
    while frontier not empty:
        node ← POP(frontier)
        for child in EXPAND(node):
            if goal(child.state) return child        # 生成时就测
            if child.state not in reached: add to reached and frontier
    return failure
```

- **Early goal test**：节点**生成**时就测；**Late goal test**：节点**被弹出**时才测。BFS 用 early（省一层），UCS 必须 late（原因见下）。
- Complete（b 有限）；cost-optimal **仅当所有 action cost 相同**；Time = O(b^d)（1 + b + … + b^d）；Space = O(b^d)。（用 late goal test 会变成 O(b^{d+1})。）

⚠️ **BFS 找的是"步数最少"的路，不是 cost 最低的路**。Romania 例子（代码算出）：Arad → Bucharest，BFS 找到 Arad–Sibiu–Fagaras–Bucharest（3 步，cost **450**）；而 cost 最低的是 Arad–Sibiu–Rimnicu Vilcea–Pitesti–Bucharest（4 步，cost **418**）。

### 6.2 Uniform-Cost Search（UCS）

**策略**：总是展开 **path cost g(n) 最小**的节点。frontier 是 **priority queue（按 g 排序）**。AI 界叫 UCS，理论 CS 界叫 **Dijkstra's algorithm**。

**为什么必须 late goal test**：BFS 里第一次生成 goal 就是最优（因为 cost 相同）；UCS 里**第一次生成的 goal 不一定是最便宜的**。slide 23–24 的例子（从 Sibiu 到 Bucharest，我用代码验证）：

| 步骤 | 弹出（最小 g） | 做了什么 |
|---|---|---|
| 1 | Sibiu (0) | 生成 Rimnicu Vilcea (80)、Fagaras (99)（还有 Arad 140、Oradea 151） |
| 2 | Rimnicu Vilcea (80) | 生成 Pitesti = 80+97 = **177**（Craiova 226） |
| 3 | Fagaras (99) | 生成 **Bucharest = 99+211 = 310** ← goal 已经生成，但**不停** |
| 4 | Pitesti (177) | 生成 Bucharest = 177+101 = **278**，比 310 便宜 → **替换 reached 里的旧路径** |
| 5 | …（其他节点） | … |
| 6 | Bucharest (278) | 现在**弹出**它并 goal test → 返回 solution，cost **278** |

- Complete：b 有限，且所有 action cost ≥ ε > 0（否则零成本环路会无限循环）。
- Cost-optimal。Time / Space = O(b^{1+⌊C*/ε⌋})（C* = 最优解的 cost）。

我自己的小例子（图：S→A 2，S→B 4，A→C 4，A→G 9，B→C 1，C→G 3；起点 S，goal G）：UCS 依次展开 S(0)、A(2)、B(4)、C(5)、G(8)，解是 S–B–C–G，cost **8**；BFS 找到 S–A–G（2 步），cost 11。

### 6.3 Depth-First Search（DFS）

**策略**：总是展开 frontier 里**最深**的节点，一路向下直到没有 successors，再**回溯**到最近还有未展开 successors 的节点。用 **LIFO queue（stack）**。

slide 28–30 的二叉树（A 是 root；B、C；D、E、F、G；叶子 H…O），goal 是 M。DFS 的展开顺序（代码算出，与 slide 12 步一致）：

```
步骤:  1  2  3  4  5  6  7  8  9  10 11 12
节点:  A  B  D  H  I  E  J  K  C  F  L  M
```

（对比：BFS 要展开 A、B、C、D…L、M 共 13 个节点才弹出 M。）

**Space 小的原因**：slide 30 的图中，一个子树展开完就从内存**删掉**（变淡）。DFS 只需保存**当前路径 + 每层未展开的兄弟**，所以是 O(bm)（线性）。

- 通常用 **tree-like**（不存 reached）。
- Complete：**finite tree-shaped 或 finite acyclic** 状态空间；finite cyclic 空间要**检查环**；**infinite** 状态空间不 complete。（所以 slide 21 的对比表写 "No"，指一般情况。）
- **Not cost-optimal**（找到的是"最左边的 solution"，不一定最浅或最便宜）。
- Time = O(b^m)；Space = O(bm)。

### 6.4 Backtracking search

DFS 的变体：**一次只生成一个 successor**，每个部分展开的节点记住"下一个要生成哪个"。内存从 O(bm) 降到 **O(m)**。

### 6.5 Depth-Limited Search（DLS）

给 DFS 设一个**深度上限 ℓ**，解决无限深度问题。超过 ℓ 的节点当作没有 successors。没找到解就返回 **cutoff**（"因为 limit 没找到"），**不是** failure（"确认没有解"）。

- Incomplete 如果 **ℓ < d**（goal 比上限深）；如果 ℓ > d **不是 cost-optimal**（可能先找到更深的解）。
- Time O(b^ℓ)，Space O(bℓ)。
- slide 6：Romania 有 20 个城市，所以 ℓ = 19 一定够；仔细看地图，**任何两城之间最多 9 步** —— 这个数叫 state-space graph 的 **diameter**，是更好的 ℓ。**我用代码验证：diameter = 9**（最远的一对是 Lugoj 和 Neamt）。

### 6.6 Iterative Deepening Search（IDS）

**策略**：DLS with ℓ = 0, 1, 2, …，直到找到解；若返回的不是 cutoff（是 failure）就停。

slide 9–10 的图（binary tree，goal M 在深度 3）—— 我用代码数了每个 limit 生成的节点：

| Limit | 生成的节点数 | 找到 M？ |
|---|---|---|
| 0 | 1 | ✘ |
| 1 | 3 | ✘ |
| 2 | 7 | ✘ |
| 3 | 13 | ✔ |
| 总计 | 24 | |

IDS 结合了两者的优点：

| 来自 DFS | 来自 BFS |
|---|---|
| Space：有解时 O(bd)；无解（有限空间）时 O(bm) | Cost-optimal（所有 action cost 相同时） |
| Complete：finite acyclic；或 finite cyclic 且检查环 | |

Time：有解 O(b^d)；无解 O(b^m)。

**IDS 浪费吗？**（slide 14–16）重复展开的都是上面的层，而节点数集中在最底层（成指数增长）。b = 10、d = 5：

| | 节点数 | 计算 |
|---|---|---|
| IDS（slide 的算法） | **123,450** | 50 + 400 + 3,000 + 20,000 + 100,000 |
| BFS | **111,111** | 1 + 10 + … + 100,000 |

⚠️ slide 里 IDS 的算式**没算 root**，BFS 的算式**算了 root** —— 不公平。IDS 的 root 在 6 次迭代里各生成一次，一致地算进去 IDS = **123,456**，是 BFS 的 **1.111 倍**（≈ b/(b−1)，代码验证）。所以 IDS 只比 BFS 多约 11%，但内存是 O(bd) 而不是 O(b^d)。**当搜索空间大、solution 深度未知时，IDS 是首选的 uninformed 方法。**

### 6.7 Bidirectional Search

同时做**从 initial state 向前**和**从 goal 向后**两个搜索，希望在中间相遇（两个 frontier 碰撞）。动机：b^{d/2} + b^{d/2} ≪ b^d。

slide 17 的数字（b = 10, d = 6，代码验证）：

| | 节点数 |
|---|---|
| BFS 总数 | 1,111,111 |
| 上半（深度 0–3） | 1,111 |
| 下半（深度 4–6） | 1,110,000（约上半的 **999 倍**） |
| Bidirectional | 2 × 10³ = **2,000** |

要做**向后搜索**，需要能求"一个 state 的 predecessors"（哪些状态经过一个动作可以到达它）；动作可逆时，predecessors = successors。

- 两个方向都用 BFS 时：complete（b 有限）；cost-optimal（action cost 相同）；Time = **O(b^{d/2})**；Space = **O(b^{d/2})**。

### 6.8 对比表（slide 21）

| Criterion | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| Complete? | Yes¹ | Yes¹˒² | No | No | Yes¹ | Yes¹˒⁴ |
| Optimal cost? | Yes³ | Yes | No | No | Yes³ | Yes³˒⁴ |
| Time | O(b^d) | O(b^{1+⌊C*/ε⌋}) | O(b^m) | O(b^ℓ) | O(b^d) | O(b^{d/2}) |
| Space | O(b^d) | O(b^{1+⌊C*/ε⌋}) | O(bm) | O(bℓ) | O(bd) | O(b^{d/2}) |

¹ b 有限；² action cost ≥ ε > 0；³ action cost 相同；⁴ 两个方向都用 BFS 或 UCS。

---

## 7. (2C) Informed（heuristic）search

有关于 states 的**额外信息**，能估计一个 state 离 goal 多远、区分哪个 non-goal 更"有希望"。

### 7.1 Best-first search 与 heuristic

**Best-first search**：用**evaluation function f(n)** 选节点，f 最小的先展开。不同的 f → 不同的算法。

**Heuristic function h(n)** = 从节点 n 的 state 到 goal 的**最便宜路径的估计成本**。例：**straight-line distance h_SLD**。注意：h_SLD **不能从 ACTIONS / RESULT 算出来**，是额外信息。

Romania 到 Bucharest 的 h_SLD（slide 28，我读图核对）：

| City | h | City | h |
|---|---|---|---|
| Arad | 366 | Mehadia | 241 |
| Bucharest | 0 | Neamt | 234 |
| Craiova | 160 | Oradea | 380 |
| Drobeta | 242 | Pitesti | 100 |
| Eforie | 161 | Rimnicu Vilcea | 193 |
| Fagaras | 176 | Sibiu | 253 |
| Giurgiu | 77 | Timisoara | 329 |
| Hirsova | 151 | Urziceni | 80 |
| Iasi | 226 | Vaslui | 199 |
| Lugoj | 244 | Zerind | 374 |

### 7.2 Greedy best-first search

f(n) = **h(n)**：只看"离 goal 多近"，忽略已走了多远。（实现和 UCS 一样，只是 priority queue 按 h 排序。）

Arad → Bucharest（slide 30–32，代码验证）：

| 步骤 | 展开 | frontier 里最小 h | 说明 |
|---|---|---|---|
| 1 | Arad | Sibiu (253) | Timisoara 329、Zerind 374 |
| 2 | Sibiu | Fagaras (176) | 另外 Rimnicu Vilcea 193、Oradea 380、Arad 366 |
| 3 | Fagaras | Bucharest (0) | Sibiu 253 |
| 4 | Bucharest | — | goal |

路径 Arad–Sibiu–Fagaras–Bucharest，cost = 140 + 99 + 211 = **450**，**不是最优**（最优 418）。

- Complete：tree-like 版本在有限状态空间**不** complete（会在环里打转）；graph search 版本 complete（有限空间）。
- **Not cost-optimal**。Time O(b^m)，好的 heuristic 可以大幅降低。Space：graph 版本 O(b^m)。

### 7.3 A* search

f(n) = **g(n) + h(n)**：**g** = 已走的成本，**h** = 估计剩余成本 → f = "经过 n 的最便宜 solution 的估计总成本"。

**Arad → Bucharest 的 trace**（slide 37–41，我用代码算出展开顺序和 f 值，与图完全一致）：

| 展开顺序 | 节点 | g | h | f = g + h | 生成的子节点（f） |
|---|---|---|---|---|---|
| 1 | Arad | 0 | 366 | 366 | Sibiu 393、Timisoara 447、Zerind 449 |
| 2 | Sibiu | 140 | 253 | 393 | Arad 646、Fagaras 415、Oradea 671、Rimnicu Vilcea 413 |
| 3 | Rimnicu Vilcea | 220 | 193 | 413 | Craiova 526、Pitesti 417、Sibiu 553 |
| 4 | Fagaras | 239 | 176 | 415 | Sibiu 591、**Bucharest 450 (=450+0)** |
| 5 | Pitesti | 317 | 100 | 417 | **Bucharest 418 (=418+0)**、Craiova 615、Rimnicu Vilcea 607 |
| 6 | Bucharest | 418 | 0 | 418 | goal ← 弹出并测试 → **cost 418** |

**要点**：
- 第 4 步之后 frontier 里有 Bucharest（f = 450，经 Fagaras），但 A* **不**停 —— 因为 Pitesti（f = 417）更小。到第 5 步发现经 Pitesti 的 Bucharest 只有 418。
- **Pruning**：Timisoara（447）和 Zerind（449）的 f 都大于最优 cost 418，所以**永远不会被展开**。pruning 效果好不好取决于 heuristic 的质量。

**我的小例子：Greedy 失败、A* 成功**（图：S→A 1，S→B 4，A→G 12，B→G 5；h：S=5，A=4，B=5，G=0）：
- Greedy：A 的 h=4 < B 的 h=5，选 A → S–A–G，cost **13**。
- A*：f(A) = 1+4 = 5，f(B) = 4+5 = 9。展开 A → G 得 f = 13；再弹出 B（f=9）→ G 得 g = 9，比 13 好，替换；弹出 G(9) → cost **9**（最优）。

### 7.4 A* 什么时候最优？Admissible 与 Consistent

- **Admissible**：h **绝不高估**到 goal 的真实最低成本，即对所有 n：h(n) ≤ h*(n)。h_SLD admissible：直线是两点间最短路径。
- **Consistent（monotonic）**：对每个节点 n 和它的每个 successor n'（经过动作 a）：

$$h(n) \le c(n,a,n') + h(n')$$

  这是 **triangle inequality**。（还要求 h(goal) = 0。）

**关系**：consistent ⟹ admissible（反过来不成立）。

**为什么 admissible 保证最优**（直觉）：A* 弹出 goal 时，frontier 里所有节点的 f ≥ 这个 goal 的 g。因为 h 不高估，f(n) ≤ "经过 n 的真实最优 cost"，所以没有任何路径比它更便宜。

**我用代码对 Romania 的全部 23 条路（两个方向）检查**：h_SLD **没有任何违反 consistency 的边**，并且每个城市 h ≤ 真实最短距离（例：Arad 366 ≤ 418；Sibiu 253 ≤ 278；Fagaras 176 ≤ 211；Pitesti 100 ≤ 101）。

⚠️ **A* 的最优性条件要区分版本**：tree-like search 只需要 admissible；**用 reached 的 graph search 需要 consistent**（slide 43 把两个条件写成并列，没说明这个区别）。

**A* 的性能**：Complete（b 有限，cost > ε）；cost-optimal（heuristic admissible / consistent）；Time 和 Space 一般都是指数，具体取决于 heuristic 质量（slide 写 O(b^d) 是简化）；Space 通常是 A* 的实际瓶颈。

---

## ⚠️ Slide 里有问题或需要小心的地方

| Slide | Slide 写的 | 更准确的理解 |
|---|---|---|
| 2A-17 | "directed edges" | 地图是双向路，每条路 = 两条有向边 |
| 2B-9 | Big-O "analyzing the worst case" | Big-O 是**增长速度的上界**，"最坏情况"是另一回事（常一起用） |
| 2B-10 | "Logarithmic time: O(n log n)" | **错**。logarithmic 是 O(log n)；O(n log n) 是 linearithmic |
| 2B-20 | BFS Time = 1 + b + … + b^d = O(b^d) | 这是 early goal test；late goal test 是 O(b^{d+1}) |
| 2C-7 | IDS "used to find the diameter" | **错**。IDS 找的是**最浅 goal 的深度 d**（最合适的 ℓ），不是 graph diameter（diameter 是 2C-6 里 DLS 的另一种选 ℓ 方法） |
| 2C-16 | IDS 123,450 vs BFS 111,111 | IDS 没算 root、BFS 算了。一致计数是 123,456 vs 111,111（比值 ≈ 1.11） |
| 2C-20 | Bidirectional："Space: **Linear** complexity O(b^{d/2})" | **错**。O(b^{d/2}) 是指数级；slide 21 的表是对的 |
| 2C-34 | Greedy tree-like 版本 "Space: Linear O(bm)" | 我的判断是**应为 O(b^m)**（frontier 是 priority queue，装着所有已生成节点）。⚠️ 这条是我凭 AIMA 的印象，**没有对照原书核实** |
| 2C-36 | 地图标 "Step cost, g(n)" | 地图上的数字是**单步 cost c(n,a,n')**；g(n) 是**累计** path cost |
| 2C-43 | A* optimal "if admissible; if consistent" | 见 7.4：tree-like 只要 admissible；graph search（有 reached）需要 consistent。Time O(b^d) 是简化 |
| 2C-47 | 只算 Arad→Sibiu 一条边就写 "∴ h_SLD is consistent" | 一条边不能证明；要**所有**边都满足。（我全部检查过，确实成立） |

**考试策略**：题目引用 slide 的公式就按 slide；但要知道 DFS 的 "Complete" 是有条件的、UCS / A* 的 goal test 是 late、consistency 要对所有边成立。

---

## Cheat sheet

| 概念 | 公式 / 规则 |
|---|---|
| Problem 6 要素 | States、Initial、Goal、Actions、Transition model、Cost |
| Frontier vs reached | 未展开 / 已生成过的 states |
| Queue 类型 | FIFO=BFS，LIFO=DFS，Priority=UCS/Greedy/A* |
| BFS | early goal test；O(b^d) time & space；cost 相同才 optimal |
| UCS | f = g；late goal test；O(b^{1+⌊C*/ε⌋}) |
| DFS | O(b^m) time，O(bm) space；tree-like；不 optimal |
| DLS | ℓ 太小不 complete；返回 cutoff |
| IDS | O(b^d) time，O(bd) space；多花 ≈ b/(b−1) |
| Bidirectional | O(b^{d/2}) time **和** space |
| Greedy | f = h；不 optimal |
| A* | f = g + h；admissible / consistent 时 optimal |
| Admissible | h(n) ≤ h*(n) |
| Consistent | h(n) ≤ c(n,a,n') + h(n')，h(goal)=0 |

---

## Practice

### A. 选择题（5）

**A1.** UCS 的 goal test 应该在什么时候做？
(a) 节点生成时  (b) 节点被弹出 frontier 时  (c) 节点入 reached 时  (d) 不需要 goal test

**A2.** DFS 的 space complexity 是？
(a) O(b^m)  (b) O(b^d)  (c) O(bm)  (d) O(b^{d/2})

**A3.** 用带 reached 的 graph search 版 A*，为了保证 cost-optimal，heuristic 应该是？
(a) 只要 admissible  (b) consistent  (c) 任意  (d) 恒等于 g

**A4.** 什么情况下 IDS 是首选？
(a) 空间小、解很浅  (b) 空间很大且 solution 深度未知  (c) 所有 action cost 不同  (d) 有很好的 heuristic

**A5.** Bidirectional search（两边都 BFS）的 time complexity？
(a) O(b^d)  (b) O(b^{d/2})  (c) O(bd)  (d) O(2b)

### B. 简答题（3）

**B1.** 解释 frontier、reached、explored set 的区别，以及为什么 graph search 需要 reached。

**B2.** 为什么 IDS 重复展开上层节点并不浪费？

**B3.** admissible 和 consistent 的区别是什么？h(n) = 0（对所有 n）是 admissible 吗？这时 A* 变成什么？

### C. 计算 / 追踪（3）

**C1.** 图：S→A 2，S→B 4，A→C 4，A→G 9，B→C 1，C→G 3。写出 UCS 的展开顺序（含 g 值）、最优路径与 cost；再写出 BFS 找到的路径及其 cost。

**C2.** 图：S→A 1，S→B 4，A→G 12，B→G 5；h(S)=5，h(A)=4，h(B)=5，h(G)=0。先检查这个 h 是不是 consistent，再分别写出 Greedy 和 A* 的结果与 A* 的 f 表。

**C3.** b = 3、d = 3，(a) BFS 生成多少节点？(b) IDS 生成多少节点（一致地把 root 算进去，最坏情况）？

### D. 思考题（2）

**D1.** 8-Queens 的 incremental 和 complete-state 两种 formulation 各有什么状态数？这说明 formulation 的选择对搜索有什么影响？

**D2.** 如果图里有 **cost 为 0 的环**，UCS 会怎样？如果有 **negative cost**，UCS / A* 的最优性还成立吗？

---

### 答案

**A1.** (b)。UCS 第一次生成 goal 时不一定是最便宜的（例：Sibiu→Bucharest 先得到 310，后来发现 278）。

**A2.** (c)。只存当前路径和每层的兄弟。

**A3.** (b)。tree-like 只要 admissible；graph search 需要 consistent（否则可能先用了较贵的路径到达某个 state 并把它标成 reached）。

**A4.** (b)。

**A5.** (b)。两个方向各搜 d/2 层。

**B1.**
- **Frontier**：已生成、还没展开的节点（等待展开）。
- **Reached**：所有曾经生成过节点的 **states**（不管展开了没有）。
- **Explored set（closed list）**：已经展开的节点。
- graph search 用 reached 来识别 redundant / loopy paths：state 已经在 reached 里就不再加入 frontier（除非新路径更便宜）→ 避免无限循环和指数重复。

**B2.** 节点数随深度成指数增长，最底层占绝大部分。上层每层被重复生成，但总量小：b = 10、d = 5 时 IDS 123,456 vs BFS 111,111，只多约 11%（≈ b/(b−1)）。换来的是 BFS 的完整性 / 最优性和 DFS 的 O(bd) 内存。

**B3.**
- Admissible：对每个 n，h(n) ≤ 真实最低成本 h*(n)；consistent：对每条边 h(n) ≤ c(n,a,n') + h(n')（triangle inequality）。Consistent ⟹ admissible，反之不一定。
- h ≡ 0 是 admissible（不高估）也是 consistent（0 ≤ c + 0）。此时 f = g，A* 就变成 **UCS**。

**C1.**（代码验证）
- UCS 展开顺序：S(0) → A(2) → B(4) → C(5) → G(8)。最优路径 S–B–C–G，cost **8**。
  - 过程：展开 S → A(2)、B(4)；展开 A → C(6)、G(11)；展开 B → C 的更便宜路径 5（4+1）替换 6；展开 C(5) → G = 8 替换 11；弹出 G(8)。
- BFS：S–A–G（2 步），cost **11**（步数少但 cost 高）。

**C2.**
- Consistency 检查：S→A：5 ≤ 1+4 = 5 ✔；S→B：5 ≤ 4+5 ✔；A→G：4 ≤ 12+0 ✔；B→G：5 ≤ 5+0 ✔ → **consistent**（且 admissible：h(A)=4 ≤ 12，h(B)=5 ≤ 5，h(S)=5 ≤ 9）。
- Greedy：选 A（h=4 < 5）→ G：S–A–G，cost **13**。
- A*（代码验证）：

| 展开 | g | f |
|---|---|---|
| S | 0 | 5 |
| A | 1 | 5 |
| B | 4 | 9 |
| G | 9 | 9 |

  展开 A 后 G 的 f = 13；展开 B 后 G 的 g = 9 < 13，替换；弹出 G(9)。结果 S–B–G，cost **9**（最优）。

**C3.**（代码验证）
- (a) BFS：1 + 3 + 9 + 27 = **40**。
- (b) IDS：limit 0..3 分别生成 1、4、13、40，合计 **58**（即 4×1 + 3×3 + 2×9 + 1×27 = 58）。

**D1.** Incremental（任意放）：64×63×…×57 ≈ 1.8×10¹⁴；complete-state（每列一个）：8⁸ ≈ 1.7×10⁷；改进的 incremental（不互相攻击）只有 2,057 个状态。**同一个问题，formulation 好坏能让状态空间小几个数量级**，直接决定能不能搜得动。

**D2.** cost 为 0 的环：g 永远不增加，UCS 可能在环里无限循环（所以要求 cost ≥ ε > 0）。negative cost：UCS（Dijkstra）的"先弹出的就是最便宜"的前提被破坏，最优性不再保证；A* 的 admissible / consistent 论证同样依赖非负 cost。

---

## 与其他章节的联系

- Ch1C 的 **goal-based agent** 就是本章的 problem-solving agent；7 个环境维度决定了本章的"闭眼执行"假设是否成立。
- Ch3 的 local search 放弃了"记住路径"，只在乎**最终状态**（例：8-queens 的 complete-state formulation）。
- Ch4 的 minimax 是 DFS 的一个版本（同样 O(b^m) 时间、O(bm) 空间）；alpha-beta 的 move ordering 类似"先探索最有希望的"，iterative deepening 也用在 game search 里。
