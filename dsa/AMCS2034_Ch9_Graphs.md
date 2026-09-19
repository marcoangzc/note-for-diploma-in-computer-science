# AMCS2034 — Chapter 9: Graphs

> 这章 slide 的问题：术语很多但 **没有例子**（degree、cycle、bipartite…）；邻接表 / 邻接矩阵只贴 code 没解释怎么读；
> DFS 和 BFS 只有图和文字，没有一步步 trace 和对比。**另外 DFS 和 BFS 两页 slide 用的其实是两个不同的图**（下面会指出）。
> 这份 note 用一个小 graph 把所有术语、表示法、DFS / BFS 串起来。

---

## 0. 这章一句话总览

> **Graph = 一堆点（vertex）+ 连接它们的线（edge）。用来表示"东西之间的关系"。**
> 学三件事：**① 术语 ② 怎么存进 program（matrix / list）③ 怎么走遍它（DFS / BFS）**

---

## 1. 为什么要 Graph？（Slide 6–10）

- **Königsberg 七桥问题**（Euler，1736）：城市被河分成 4 块陆地，有 7 座桥。能不能 **每座桥走一次刚好一次、并回到起点**？
  Euler 把 **陆地 = 点（vertex）、桥 = 线（edge）**，证明不可能。这是 graph theory 的开始。
  （额外：能走的条件是 **每个点的 degree 都是偶数**。Königsberg 的 4 个点 degree 是 3, 3, 3, 5，全是奇数 → 不可能。）
- 用途：网络（电脑 / 通讯）、地图（最短路径）、社交关系、任务排程（哪个先做）、家族树、AI 找路径…

**Graph 定义：G = (V, E)**，V = 点的集合，E = 边的集合。

例（Slide 12）：V = {Seattle, San Francisco, …}，E = {{Seattle, San Francisco}, {Seattle, Chicago}, …}

---

## 2. 术语：用一个小 graph 全部讲清楚

**我们的例子 graph（等同 BFS slide 的图）：** 5 个点 0–4，7 条 edge

```
            0
         /  |  \
        1---2---3
         \     /
            4

Edges: 0-1, 0-2, 0-3, 1-2, 2-3, 1-4, 3-4
```

### 2.1 Edge 的种类

| 术语 | 意思 | 例子 |
|---|---|---|
| **Undirected edge** | 无方向，(u, v) 和 (v, u) 一样 | 铁路、高速公路 |
| **Directed edge** | 有方向，(u, v) 是 **有序** 的：u = origin，v = destination | 单行道、航班 |
| Undirected graph | 全部 edge 都无方向 | |
| **Directed graph (digraph)** | 全部 edge 都有方向 | |
| **Self loop** | edge 连到自己 | 0—0 |
| **Parallel edges** | 两条 edge 连同一对点 | 两个城市间两条路 |
| **Weighted graph** | edge 有数值（距离 / 成本） | 城市间的距离 |

### 2.2 点和 edge 的关系

| 术语 | 意思 | 我们的例子 |
|---|---|---|
| **Adjacent** | 两个点之间有 edge | 0 和 1 adjacent；1 和 3 **不** adjacent |
| **Incident** | edge 连着某个点 | edge (0,1) incident on 0 和 1 |
| **Degree** | 一个点连着几条 edge | deg(0)=3, deg(1)=3, deg(2)=3, deg(3)=3, deg(4)=2 |

**小规律（额外）**：所有点的 degree 加起来 = **2 × edge 数**（每条 edge 有两个端点）。
例：3+3+3+3+2 = 14 = 2 × 7 ✅

### 2.3 Path 和 Cycle

| 术语 | 意思 | 例子 |
|---|---|---|
| **Path** | 一串 **相邻** 的点 | 0 → 1 → 4 |
| **Simple path** | 点 **不重复** 的 path | 0 → 1 → 4 ✅；0 → 1 → 2 → 0 → 3 ❌（0 重复了） |
| **Cycle** | 第一个点 = 最后一个点的 path | 0 → 1 → 2 → 0 |
| **Simple cycle** | 除了首尾，其他点 / edge 不重复 | 0 → 1 → 2 → 0 ✅ |

### 2.4 Connected

| 术语 | 意思 |
|---|---|
| **Connected（两点）** | 两个点之间有 path |
| **Connected graph** | **任何两个点** 之间都有 path |
| **Connected component** | 一个不 connected 的 graph 里，各个 "连在一起的一块" |

```
Graph 有 2 个 connected component：

   0 ── 1        3 ── 4
   │             │
   2             5
```

### 2.5 特殊的 graph

| 术语 | 意思 |
|---|---|
| **Tree** | **没有 cycle 的 connected graph**（acyclic connected）。n 个点的 tree 一定有 n − 1 条 edge |
| **Forest** | 好几棵 tree（互相不连） |
| **Subgraph** | graph 的一部分（一些点和 edge） |
| **Spanning tree** | connected graph 的一个 subgraph：**包含全部的点**，而且是一棵 tree（无 cycle） |
| **DAG** | Directed Acyclic Graph：有方向、无 cycle（例如 "课程先修关系"） |
| **Bipartite graph** | 点可以分成 **两组**，所有 edge 都是 **跨组** 的（组内没有 edge） |
| **Complete graph** | 所有可能的 edge 都有 |
| **Sparse / Dense** | edge 很少 / edge 很多（接近 complete） |

**Bipartite 例子**：学生 ↔ 课程（学生只连课程，学生和学生之间没有 edge）。
我们的例子 graph **不是** bipartite：0-1-2 是个 **三角形**（奇数长度的 cycle），没办法分两组。

**Edge 数量（Slide 31）**：
- Undirected：最多 **|V|(|V|−1)/2**（每对点一条）。例：5 个点 → 最多 10 条；我们的例子有 7 条，算比较 dense
- Directed：最多 **|V|(|V|−1)**
- Slide 说 edge < |V| log |V| 算 **sparse**（很少 edge）

---

## 3. Graph 怎么存进 program？（Slide 32–57）

以下都用上面的例子 graph（或 Slide 的 city graph）。

### 3.1 先存 vertices

用 array 存名字，然后 **用 index 当 vertex 的编号**（Slide 33–34）：

```java
String[] vertices = {"Seattle", "San Francisco", "Los Angeles", ...};
// vertices[0] = "Seattle", vertices[1] = "San Francisco", ...
```

### 3.2 存 edges 的方法一：Edge array（Slide 35–37）

```java
int[][] edges = {{0,1}, {0,2}, {0,3}, {1,2}, {1,4}, {2,3}, {3,4}};
```

每一行 `{u, v}` = 一条 edge。

**⚠️ Slide 36 的 city graph 为什么有 46 行？** 因为它是 **undirected**，每条 edge 被存了 **两次**（`{0,1}` 和 `{1,0}`），所以 46 行 = **23 条真正的 edge**。

Slide 37 的 directed 例子：
```java
String[] names = {"Peter", "Jane", "Mark", "Cindy", "Wendy"};
int[][] edges = {{0,2}, {1,2}, {2,4}, {3,4}};
// Peter→Mark, Jane→Mark, Mark→Wendy, Cindy→Wendy
```

### 3.3 方法二：Edge objects（Slide 38–41）

```java
public class Edge {
    int u; int v;                 // 从 u 到 v
    public Edge(int u, int v) { this.u = u; this.v = v; }
    public boolean equals(Object o) { return u == ((Edge) o).u && v == ((Edge) o).v; }
}
ArrayList<Edge> list = new ArrayList<>();
list.add(new Edge(0, 1));
```

好处：**不知道会有几条 edge 时**（ArrayList 会自己变大）；还可以给 Edge 加 `weight` 等属性。

> Slide 41：这两种方法 **输入时直觉**，但 **处理时不够有效率**（要找 "某个点的邻居" 得扫全部 edge）。所以有下面两种。

### 3.4 方法三：Adjacency Matrix（邻接矩阵）

**n × n 的 2D array**。`m[i][j] = 1` 表示 **有一条从 i 到 j 的 edge**，否则 0。

我们的例子（undirected）：

```
        0  1  2  3  4
   0  [ 0, 1, 1, 1, 0 ]
   1  [ 1, 0, 1, 0, 1 ]
   2  [ 1, 1, 0, 1, 0 ]
   3  [ 1, 0, 1, 0, 1 ]
   4  [ 0, 1, 0, 1, 0 ]
```

**怎么读：**
- **行（row）= from，列（column）= to**
- **Undirected → matrix 对称**（`m[i][j] == m[j][i]`），因为 edge 没方向
- 一行的和 = 那个点的 **degree**（第 0 行：0+1+1+1+0 = 3 ✅）

Slide 47 的 **directed** 例子：Peter→Mark, Jane→Mark, Mark→Wendy, Cindy→Wendy

```
           Peter Jane Mark Cindy Wendy
  Peter  [   0     0    1    0     0  ]     ← Peter → Mark
  Jane   [   0     0    1    0     0  ]     ← Jane → Mark
  Mark   [   0     0    0    0     1  ]     ← Mark → Wendy
  Cindy  [   0     0    0    0     1  ]     ← Cindy → Wendy
  Wendy  [   0     0    0    0     0  ]     ← Wendy 没有出去的 edge
```
**Directed → 不对称**。

### 3.5 方法四：Adjacency List（邻接表）

**每个点存一个 list，里面是它的邻居。** 我们的例子：

```
0: [1, 2, 3]
1: [0, 2, 4]
2: [0, 1, 3]
3: [0, 2, 4]
4: [1, 3]
```

Java 写法（Slide 49, 57 的简化版，用 `List<List<Integer>>` 比较不容易出错）：

```java
List<List<Integer>> neighbors = new ArrayList<>();
for (int i = 0; i < 5; i++) neighbors.add(new ArrayList<>());

int[][] edges = {{0,1}, {0,2}, {0,3}, {1,2}, {1,4}, {2,3}, {3,4}};
for (int[] e : edges) {
    neighbors.get(e[0]).add(e[1]);     // undirected：两个方向都要加
    neighbors.get(e[1]).add(e[0]);
}
```

**Adjacency vertex list vs Adjacency edge list（Slide 48–55）：**

| | Vertex list | Edge list |
|---|---|---|
| List 里存 | 邻居的 **编号**（`List<Integer>`） | **Edge object**（`List<Edge>`） |
| 适合 | 简单、unweighted graph | 想在 edge 上放额外信息（weight 等）→ **更有弹性** |

Slide 56：list 用 **ArrayList** 还是 **LinkedList**？ArrayList 好在 "找邻居 / 遍历" 快；要频繁增删中间 element 才考虑 LinkedList。

### 3.6 Matrix vs List 怎么选？

| | Adjacency Matrix | Adjacency List |
|---|---|---|
| Space | **O(\|V\|²)** | **O(\|V\| + \|E\|)** |
| 检查 i 和 j 有没有 edge | **O(1)** | O(i 的邻居数) |
| 找 i 的所有邻居 | O(\|V\|)（扫一整行） | **O(deg(i))** |
| 走过全部 edge | O(\|V\|²) | **O(\|V\| + \|E\|)** |
| 适合 | **Dense** graph（edge 很多） | **Sparse** graph（edge 很少） |

**例子**：|V| = 1000，|E| = 2000。
- Matrix：1000 × 1000 = **1,000,000** 格（大部分是 0，浪费）
- List：大约 1000 + 2×2000 = **5,000** 个 entry
→ 这个 sparse graph 用 list 划算很多。（Slide 53）

> **Slide 54 的补充**：它说 "用 adjacency list 印出全部 edge 是 O(n)，n 是 edge 数"，更完整的说法是 **O(|V| + |E|)**（还要走过每个点）。

---

## 4. Graph Traversal（Slide 58–73）

**Traversal = 每个点 **visit 一次**。** 两种方法：**DFS** 和 **BFS**。两种都会得到一棵 **spanning tree**（Slide 60）。

### ⚠️ 先说一个 slide 的问题

**DFS 那几页（Slide 64–65）和 BFS 那页（Slide 70）用的是两个不同的 graph！**

| | DFS slide 的图 | BFS slide 的图 |
|---|---|---|
| Edges | 0-1, 0-2, 0-3, 1-2, 1-4, 2-3 | 0-1, 0-2, 0-3, 1-2, 1-4, 2-3, **3-4** |
| 差别 | **没有** 3-4 | 多了 3-4 |

这就是为什么 DFS slide 说 "3 的邻居都 visit 过了，backtrack"，而 BFS slide 说 "3 有 3 个邻居 0, 2, 4"。别被搞混。下面我两个都 trace。

### 4.1 DFS（Depth-First Search）：一直往深处走，走不下去才退回来

**类比**：走迷宫。每次遇到岔路选一条一直走到底，死路了就 **退回上一个岔路口**，换另一条。

**Algorithm（Slide 63）**

```
dfs(v):
    visit v; mark v as visited
    for each neighbor w of v:
        if w has not been visited:
            set v as parent of w
            dfs(w)
```

Graph 可能有 **cycle**，不记录 visited 会 **无限 recursion**（Slide 62），所以要 `isVisited[]` array。

**Trace（DFS slide 的图，从 0 开始，邻居按小到大）**

邻居表：0:[1,2,3]，1:[0,2,4]，2:[0,1,3]，3:[0,2]，4:[1]

| 步骤 | 动作 | Visited 顺序 |
|---|---|---|
| 1 | visit 0 | 0 |
| 2 | 0 的邻居 1 未访问 → 走 1 | 0, 1 |
| 3 | 1 的邻居：0 已访问，2 未访问 → 走 2 | 0, 1, 2 |
| 4 | 2 的邻居：0, 1 已访问，3 未访问 → 走 3 | 0, 1, 2, 3 |
| 5 | 3 的邻居：0, 2 都已访问 → **backtrack** 到 2 → 2 也没了 → backtrack 到 1 | |
| 6 | 1 的下一个邻居 4 未访问 → 走 4 | **0, 1, 2, 3, 4** |
| 7 | 4 的邻居 1 已访问 → backtrack … 全部结束 | |

**DFS tree**（parent）：1←0，2←1，3←2，4←1

```
    0
    │
    1
   / \
  2   4
  │
  3
```

**Time complexity**：每个点和每条 edge 各处理一次 → **O(|V| + |E|)**（用 adjacency list）。

### 4.2 BFS（Breadth-First Search）：一层一层往外扩

**类比**：把石头丢进水里，**涟漪一圈一圈扩散**。先访问离起点 1 步的，再 2 步的，再 3 步的…

**Algorithm（Slide 69）—— 用 queue：**

```
bfs(v):
    create an empty queue
    add v into queue; mark v visited
    while queue is not empty:
        u = dequeue
        add u into traversed list
        for each neighbor w of u:
            if w not visited:
                add w into queue
                set u as parent of w
                mark w visited        ← 在"放进 queue 时"就 mark
```

> ⚠️ 重点：**在 add 进 queue 时就 mark visited**（第 13 行），不是等 dequeue 才 mark。否则同一个点可能被 add 进 queue 很多次。

**Trace（BFS slide 的图，从 0 开始）**

邻居表：0:[1,2,3]，1:[0,2,4]，2:[0,1,3]，3:[0,2,4]，4:[1,3]

| dequeue 的 u | 新加入 queue 的邻居 | Queue（front → rear） | Traversed |
|---|---|---|---|
| （开始） | 0 | [0] | |
| 0 | 1, 2, 3 | [1, 2, 3] | 0 |
| 1 | 4（0, 2 已 visited） | [2, 3, 4] | 0, 1 |
| 2 | 无 | [3, 4] | 0, 1, 2 |
| 3 | 无 | [4] | 0, 1, 2, 3 |
| 4 | 无 | [ ] | **0, 1, 2, 3, 4** |

**BFS tree**：1, 2, 3 的 parent 是 0；4 的 parent 是 1

```
      0
    / | \
   1  2  3
   │
   4
```

**Time complexity**：**O(|V| + |E|)**（用 adjacency list）。

### 4.3 同一个 graph，DFS 和 BFS 的 tree 不一样！

用 **BFS slide 的图（7 条 edge）**，两种都从 0 开始，visit 顺序都是 0,1,2,3,4（巧合！），但 **tree 的形状不同**：

```
DFS tree（一条长链）:        BFS tree（很"宽"）:
    0                             0
    │                           / | \
    1                          1  2  3
    │                          │
    2                          4
    │
    3
    │
    4
```

DFS 的路径：0 → 1 → 2 → 3 → 4（4 步）。
BFS 找到 4 的路径：0 → 1 → 4（**只有 2 步**）。

→ **这就是为什么 BFS 能找 shortest path，DFS 不行。**

### 4.4 为什么 BFS 找到的是最短路径？（Slide 71）

BFS **一层一层** 走：先走完离起点 1 步的所有点，才走 2 步的…。所以 **第一次到达某个点的时候，一定是用最少的 edge 数到的**。BFS tree 里从 root 到任何点的 path 就是 shortest path（**unweighted graph**）。

DFS 一条路走到底，先找到的路径可能绕了很大一圈。

### 4.5 Java 实作（我用 Java 跑过，结果和上面的 trace 一样）

```java
// DFS (recursion)
void dfs(int v, List<List<Integer>> g, boolean[] visited, List<Integer> order) {
    visited[v] = true;
    order.add(v);
    for (int w : g.get(v))
        if (!visited[w]) dfs(w, g, visited, order);
}

// BFS (queue)
List<Integer> bfs(int start, List<List<Integer>> g) {
    boolean[] visited = new boolean[g.size()];
    Queue<Integer> q = new LinkedList<>();
    List<Integer> order = new ArrayList<>();
    q.add(start);
    visited[start] = true;
    while (!q.isEmpty()) {
        int u = q.poll();
        order.add(u);
        for (int w : g.get(u))
            if (!visited[w]) { visited[w] = true; q.add(w); }
    }
    return order;
}
```

**DFS 用的是 stack，BFS 用的是 queue**：DFS 的 recursion 背后就是 call stack（Ch8），也可以自己用 `Stack` 写。

---

## 5. DFS vs BFS 对比（Slide 73）

| | DFS | BFS |
|---|---|---|
| 顺序 | 一条路走到底，再 backtrack | 一层一层 |
| 用什么 | **Stack**（recursion） | **Queue** |
| 找 shortest path？ | ❌ 不保证 | ✅（unweighted） |
| Time | O(\|V\|+\|E\|) | O(\|V\|+\|E\|) |
| 类比 | 走迷宫 | 涟漪扩散 |

**应用（Slide 66–67, 71–72）：**

| 应用 | DFS | BFS |
|---|---|---|
| 检查 graph 是不是 connected（visit 到的点数 = 总点数？） | ✅ | ✅ |
| 两点之间有没有 path / 找 path | ✅ | ✅ |
| 找所有 connected components | ✅ | ✅ |
| 检测 / 找 cycle | ✅ | ✅ |
| **Shortest path（unweighted）** | ❌ | ✅ |
| **Test bipartite** | — | ✅ |
| Hamiltonian path / cycle（每个点走一次） | ✅（配合 backtracking） | — |

**BFS 测 bipartite 的想法**：一层一层给点涂颜色（红、蓝、红、蓝…），如果发现某条 edge 两端是 **同一种颜色** → 不是 bipartite。

---

## 6. Cheat sheet

| 概念 | 一句话 |
|---|---|
| G = (V, E) | 点的集合 + 边的集合 |
| Degree | 点连着几条 edge |
| Path / Cycle | 一串相邻的点 / 首尾相同的 path |
| Connected | 任何两点之间都有 path |
| Tree | 无 cycle 的 connected graph（n 点 n−1 边） |
| DAG | 有方向、无 cycle |
| Bipartite | 点分两组，edge 只能跨组 |
| Max edges | undirected \|V\|(\|V\|−1)/2；directed \|V\|(\|V\|−1) |
| Matrix | Space O(\|V\|²)，查 edge O(1)，适合 dense；undirected 时对称 |
| List | Space O(\|V\|+\|E\|)，适合 sparse |
| DFS | Stack / recursion，一路走到底，O(\|V\|+\|E\|) |
| BFS | Queue，一层一层，找 shortest path，O(\|V\|+\|E\|) |
| 必须记 visited | 因为 graph 可能有 cycle |

---

## 7. 练习

### A. MCQ

**A1.** 一个有 6 个点的 undirected graph（没有 self loop / parallel edge），最多有几条 edge？
a) 6　b) 12　c) 15　d) 30

**A2.** BFS 用什么 data structure？
a) Stack　b) Queue　c) Tree　d) Hash table

**A3.** 要在 unweighted graph 找两点之间的 shortest path，用？
a) DFS　b) BFS　c) 都可以保证　d) 都不行

**A4.** Undirected graph 有 7 条 edge，所有点的 degree 加起来是？
a) 7　b) 14　c) 21　d) 不确定

**A5.** 对于 **很 sparse** 的大 graph，哪种表示法比较省 space？
a) Adjacency matrix　b) Adjacency list　c) 一样　d) 都不行

### B. Short answer

**B1.** Tree 和 graph 有什么差别？

**B2.** DFS 为什么需要 `isVisited` array？

**B3.** 解释 adjacency matrix 和 adjacency list 各自适合什么情况。

### C. Trace / Calculation

**C1.** Undirected graph，5 个点 0–4，edges：(0,1), (0,2), (1,3), (2,3), (3,4)。写出：(a) 每个点的 degree；(b) adjacency matrix；(c) adjacency list；(d) 从 0 开始 BFS 的顺序；(e) 从 0 开始 DFS 的顺序（邻居按小到大）。

**C2.** Directed graph，4 个点，edges：0→1, 0→2, 1→3, 2→3。写出 adjacency matrix，0 的 out-degree 和 3 的 in-degree。这个 graph 是 DAG 吗？

**C3.** 一个 graph 有 |V| = 1000，|E| = 2000（undirected）。Adjacency matrix 要多少格？Adjacency list 大约要多少个 entry？按 slide 的定义（edge < |V| log |V|）它是 sparse 吗？

### D. Thinking

**D1.** 为什么 BFS 找到的路径是最短的，DFS 找到的不一定？

**D2.** 下面的关系用 directed 还是 undirected graph 比较合适？(a) Facebook 好友　(b) Instagram follow　(c) 课程先修关系

---

### 答案

**A1: c**（6×5/2 = 15）　**A2: b**　**A3: b**　**A4: b**（2 × 7）　**A5: b**

**B1.** Tree 是 **没有 cycle 的 connected graph**，有 root（有层级 parent-child 关系），n 个点有 n−1 条 edge。Graph 没有 root，任何点可以连到任何点，可以有 cycle，也可以不 connected。Tree 是 graph 的一种特殊情况。

**B2.** 因为 graph 可能有 cycle。如果不记录哪些点已经 visit 过，DFS 会沿着 cycle 一直绕，造成无限 recursion。`isVisited[v] = true` 保证每个点只处理一次。

**B3.** Adjacency matrix：edge 很多（dense）、或者常常需要检查 "两点有没有 edge"（O(1)）时适合，但 space 是 O(|V|²)。Adjacency list：edge 很少（sparse）时适合，space 是 O(|V|+|E|)，找某个点的邻居很快。

**C1.**

(a) Degree：0→2, 1→2, 2→2, 3→3, 4→1（加起来 10 = 2×5 ✅）

(b) Adjacency matrix：
```
        0  1  2  3  4
   0  [ 0, 1, 1, 0, 0 ]
   1  [ 1, 0, 0, 1, 0 ]
   2  [ 1, 0, 0, 1, 0 ]
   3  [ 0, 1, 1, 0, 1 ]
   4  [ 0, 0, 0, 1, 0 ]
```

(c) Adjacency list：`0:[1,2]`，`1:[0,3]`，`2:[0,3]`，`3:[1,2,4]`，`4:[3]`

(d) **BFS**：queue [0] → 0 出，加 1, 2 → 1 出，加 3 → 2 出（3 已 visited）→ 3 出，加 4 → 4 出。顺序 **0, 1, 2, 3, 4**

(e) **DFS**：0 → 1 → 3（1 的邻居 0 已访问，3 未访问）→ 3 的邻居 1 已访问，2 未访问 → 2（2 的邻居 0, 3 都已访问，backtrack 回 3）→ 3 的下一个邻居 4 → 4。顺序 **0, 1, 3, 2, 4**

**C2.**
```
        0  1  2  3
   0  [ 0, 1, 1, 0 ]
   1  [ 0, 0, 0, 1 ]
   2  [ 0, 0, 0, 1 ]
   3  [ 0, 0, 0, 0 ]
```
0 的 out-degree = **2**（出去到 1、2）；3 的 in-degree = **2**（从 1、2 进来）。**是 DAG**（有方向、没有 cycle）。

**C3.** Matrix：1000 × 1000 = **1,000,000** 格。List：约 1000 + 2×2000 = **5,000** 个 entry。|V| log₂|V| ≈ 1000 × 10 = 10,000，2000 < 10,000 → 按 slide 的定义是 **sparse**。

**D1.** BFS 一层一层走，先访问离起点 1 步的所有点，再 2 步的…，所以第一次到达某点时用的 edge 数一定最少。DFS 一条路走到底，先到达某点的路径可能绕了很远，不保证最短。

**D2.** (a) **Undirected**（A 是 B 的朋友 ⇔ B 是 A 的朋友）；(b) **Directed**（我 follow 你，不代表你 follow 我）；(c) **Directed**（A 是 B 的先修课，有方向；而且不应该有 cycle，所以是 DAG）。

---

## 8. 和前面章节的连接

- Ch7：Graph 是 non-linear data structure；BFS 用 **queue**，DFS 用 **stack**
- Ch8：DFS 的 recursion 用 call stack，太深会 StackOverflow
- Ch5：DFS / BFS 都是 O(|V| + |E|)；matrix 遍历全部 edge 是 O(|V|²)
- Ch7：Tree 是特殊的 graph（connected + acyclic）；tree traversal 的 level-order 其实就是 BFS
