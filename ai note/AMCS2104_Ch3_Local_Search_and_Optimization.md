# AMCS2104 — Chapter 3: Local Search and Optimization Problems

> 本章要回答的问题：如果我们**根本不在乎路径**，只在乎**最后的状态有多好**（一张不冲突的课表、一个没有 queen 互相攻击的棋盘），还需要像 Chapter 2 那样记住整棵 search tree 吗？
>
> 📌 考试比重：**全科最重的一章**。3 份 past year 合计约 97 / 300 分：state-space landscape **三次都要画**（7–8 分）；hill climbing 优缺点与"卡住的原因"三次都考；Evolutionary Algorithm 考了两次（其中一次 25 分整题）。

---

## Scene：排课表的噩梦

学院要排下学期的课表：几十个科目、十几位讲师、二十间教室。
- 同一位讲师不能同时教两堂课；
- 教室容量要够；
- 学生不想早上 8 点连上四堂……

你发现：**你根本不关心"是怎样一步一步排出这张课表的"**，你只要**最后那张表**尽量好。
Chapter 2 的 BFS / A\* 却要把每一条路径都记在 frontier 里——课表的可能组合是天文数字，内存直接爆掉。

我们需要一种新想法：**先随便排一张，然后不断小改，让它越来越好**。这就是 local search。

---

## Part 1：Optimization problem 与 Local search

### 1.1 Classical search 的问题

- **Classical search**（Ch2）：**系统地**探索 search space，记住 expanded / unexpanded nodes；solution = **固定的动作序列**。
- 问题：很多问题里**到达 goal 的路径根本不重要**。

### 1.2 Optimization problem

> **An optimization problem is the problem of finding the best solution from all feasible solutions.**
> 算法会根据 **objective function**，把 candidate solutions（所有可能的解）缩小到 feasible solutions 的一个子集。

**例子（May 2026 Q1a，写两个就有 2 分）**：
- **8-queens problem**（摆 8 个 queen，互不攻击）
- **Traveling-salesman problem (TSP)**（走遍所有城市、回到起点，总距离最短）
- **University course scheduling problem**
- **Cutting stock problem**（切原料，浪费最少）
- 其他：交通灯时间优化、VLSI layout、job-shop scheduling

### 1.3 Local search 的做法

从一个 start state 出发，**只移动到 neighbouring states**：
- 决策**只根据当前 state 的邻居**的信息；
- **不保留**走过的路径或 reached states；
- 搜索**不是 systematic** 的。

**Strengths**：① **memory 非常少**（通常只存当前 state）；② 常常能在**巨大甚至无限**的 state space 里找到合理的 solution。

📝 **Model answer：Local vs Classical search（May 2026 Q1b，4 分，写 2 点）**

> 1. **Memory / what is stored** – Classical search algorithms explore the search space systematically and keep the paths, the frontier and the reached states in memory; local search algorithms keep only the current state (or a few states) and do not retain paths, so memory use is very low (often constant).
> 2. **Solution** – Classical search returns a path, i.e. a fixed sequence of actions from the initial state to the goal; in local search the path is irrelevant and the solution is the goal/final state itself (e.g. a valid 8-queens board).
> 3. (extra) **Systematic vs not** – classical search is systematic and can be complete/optimal; local search is not systematic, moves only to neighbours based on an objective function, and can find reasonable solutions in very large or infinite (continuous) state spaces, but is usually incomplete.

---

## Part 2：State-space landscape —— 把问题想成一片山地

把所有 states 排在横轴上，每个 state 的**高度（elevation）**由 **objective function** 的值决定——就得到一片"地形"。

- 若 elevation = **objective function** → 目标是找 **global maximum**，过程叫 **hill climbing**。
- 若 elevation = **heuristic cost function** → 目标是找 **global minimum**，叫 **gradient descent**。

### 2.1 五个元素（May 2026 Q1d(i)，5 分）

| Element | Definition（考试写这句） |
|---|---|
| **Current state** | The state that the search/agent is currently in (its present position on the landscape). |
| **Global maximum** | The best possible state, with the highest objective-function value in the whole landscape (the optimal solution). |
| **Local maximum** | A state (peak) that is better than all its neighbouring states, but lower than the global maximum. |
| **Flat local maximum** | A flat area (plateau) at the top of a hill: all neighbouring states have the same value and there is no uphill exit. |
| **Shoulder** | A plateau (flat area) whose edge stretches upwards, so further uphill progress is possible after crossing it. |

### 2.2 画图：Objective function 版（Oct 2025 Q2b 7 分 · Jan 2026 Q3b(iii) 7 分 · May 2026 Q1d(ii) 8 分）

下图照**课件 Ch3 p9 的原图排列**（从左到右：shoulder → global maximum → current state 在往 local maximum 的斜坡上 → local maximum → "flat" local maximum）。课件的 current state 画了一个**往上的小箭头**，表示 hill climbing 会从这里往上爬——爬到的是 local maximum，**不是** global maximum。考试照这个排列画最安全。

```
 Objective function
 (elevation)
   ^
   |                   global maximum
   |
   |                 /\
   |                /  \              local maximum
   |               /    \                          "flat" local maximum
   |              /      \          /\      ______
   |             /        \        /  \    /      \
   |            /          \      /    \  /        \
   |shoulder   /            \    /      \/          \
   |      ____/              \  /* <- current state  \
   |     /                    \/                      \
   |    /                                              \
   |   /
   |  /
   | /
   |
   +--------------------------------------------------------------> State space
```

**画图的得分点（每项约 1 分）**：
1. **Y-axis** 标 "Objective function"（elevation）；**X-axis** 标 "State space"。
2. **Current state** —— 在某个斜坡上画一个点。
3. **Shoulder** —— 平台，**右边继续往上升**。
4. **Local maximum** —— 一个尖峰，比两边高，但**比 global maximum 低**。
5. **Flat local maximum** —— 平顶，**两边都往下**。
6. **Global maximum** —— **整张图最高**的那个峰。

### 2.3 画图：Cost function 版（Oct 2025 Q2c，7 分）

把上图**上下颠倒**：目标变成最低点。五个元素变成 current state、**global minimum**、**local minimum**、**flat local minimum**、**shoulder**（平台，边缘继续往下）。
下图照**课件 Ch3 p12 的原图排列**（左边高处 → shoulder → 最深的 global minimum → 高峰 → current state 往下滑 → local minimum → 小峰 → "flat" local minimum）。课件 p17、p18 还把这张图接到 8-queens：**global minimum = h = 0 的解**；**local minimum = h = 1 但所有邻居都更差的盘面**。

```
 Cost function
 (elevation)
   ^
   |
   |
   | \
   |  \
   |   \
   |    \                                             /
   |     \                      /\                   /
   |      \____                /  \*<- current state/
   |shoulder   \              /    \               /
   |            \            /      \    /\       /
   |             \          /        \  /  \_____/
   |              \        /          \/     "flat" local minimum
   |               \      /              <- local minimum
   |                \    /
   |                 \  /
   |                  \/
   |                     <- global minimum
   |
   +--------------------------------------------------------------> State space
```

检查：global minimum 必须是**整张图最低**；flat local minimum 是**平底、两边都升高**；shoulder 是平台、**边缘继续往下**。

---

## Part 3：Hill Climbing —— 只往上走

### 3.1 做法（steepest-ascent version）

- 只记录**一个 current state**（node = state + value）。
- 每一轮：看所有邻居，**移到值最高的那个邻居**。
- 当没有邻居比自己高（到达"峰顶"）时**停止**。
- **不会往前看**，只看直接邻居。

课件 pseudocode（Ch3 p14，AIMA Figure 4.2）——node 只有两部分：**state** 和 **value**：

```
function HILL-CLIMBING(problem) returns a state that is a local maximum
    current ← problem.INITIAL
    while true do
        neighbor ← a highest-valued successor state of current
        if VALUE(neighbor) ≤ VALUE(current) then return current     ← 没有更高的邻居 = 到"峰顶"
        current ← neighbor
```
注意返回的是 "**a state that is a local maximum**"——课本自己都承认它不保证是 global maximum。

📝 **为什么叫 greedy local search？（Oct 2025 Q2a · Jan 2026 Q3b(i)，2 分）**
> Hill climbing always grabs the best (highest-valued) immediate neighbour at each step, without thinking ahead about where to go next or looking beyond its immediate neighbours. Like a greedy person, it takes the best-looking choice right now, hoping it leads to the best overall solution.

### 3.2 8-queens 例子（课件）

- **Complete-state formulation**：棋盘上已有 8 个 queen，每列一个。
- Successors：把某个 queen 移到**同一列**的另一格 → **8 × 7 = 56** 个 successors。
- **Heuristic cost h = 互相攻击（直接或间接）的 queen 对数**。Global minimum h = 0 = solution。
- 厉害之处：从 h = 17 到 h = 1 **只用了 5 步**（课件 p22）。

**课件 p19 的问题："What are the h values of these two states?"**（我用程序验算过）
把盘面写成"每列 queen 所在的行"（行 1 = 最上面）：

```
State 1 (左图):  c1..c8 = 5 6 7 4 5 6 7 6     → h = 17
State 2 (右图):  c1..c8 = 1 6 7 8 7 6 7 6     → h = 16
```

```
State 1                          State 2
   c1 c2 c3 c4 c5 c6 c7 c8          c1 c2 c3 c4 c5 c6 c7 c8
r1  .  .  .  .  .  .  .  .       r1  Q  .  .  .  .  .  .  .
r2  .  .  .  .  .  .  .  .       r2  .  .  .  .  .  .  .  .
r3  .  .  .  .  .  .  .  .       r3  .  .  .  .  .  .  .  .
r4  .  .  .  Q  .  .  .  .       r4  .  .  .  .  .  .  .  .
r5  Q  .  .  .  Q  .  .  .       r5  .  .  .  .  .  .  .  .
r6  .  Q  .  .  .  Q  .  Q       r6  .  Q  .  .  .  Q  .  Q
r7  .  .  Q  .  .  .  Q  .       r7  .  .  Q  .  Q  .  Q  .
r8  .  .  .  .  .  .  .  .       r8  .  .  .  Q  .  .  .  .
```

算法：逐对检查 28 对 queens，**同一行**（row 相同）或**同一对角线**（|row 差| = |column 差|）就算一对"attacking"，间接攻击（中间隔着别的 queen）也算。

**课件 p20：h = 17 的 state（就是 State 1）与每个 successor 的 h 值**（格子里的数字 = 把那一列的 queen 移到这格后的 h）：

```
     c1  c2  c3  c4  c5  c6  c7  c8
r1   18  12  14  13  13  12  14  14
r2   14  16  13  15  12  14  12  16
r3   14  12  18  13  15  12  14  14
r4   15  14  14   Q  13  16  13  16
r5    Q  14  17  15   Q  14  16  16
r6   17   Q  16  18  15   Q  15   Q
r7   18  14   Q  15  15  14   Q  16
r8   14  14  13  17  12  14  12  18
```
- 最好的 successors 的 **h = 12**，一共有 **8 个**（c2r1、c6r1、c5r2、c7r2、c2r3、c6r3、c5r8、c7r8）。
- 课件问 "**Which successor to choose?**"：steepest-ascent 在最好的几个之间**随机选一个**（课本做法），因为它们一样好。

**课件 p18：local minimum，h = 1**（c1..c8 = 8 3 7 4 2 5 1 6）——只剩一对 queen 互相攻击，但移动任何一个 queen 都会让 h 变大 → hill climbing 卡住。

### 3.3 Tutorial 7 例：4-Queens（手算 h）

Formulation：每列一个 queen → 状态数 **4⁴ = 256**；每个 state 的 successors **4 × 3 = 12**。
Initial state（queen 所在的行，由左至右各列，1 = 最上面）：**(1, 2, 3, 2)**

```
     c1  c2  c3  c4
r1   Q   .   .   .
r2   .   Q   .   Q
r3   .   .   Q   .
r4   .   .   .   .
```

算 h（逐对检查同行或同对角线，|行差| = |列差|）：
- c1–c2：(1,2) 对角 ✓ · c1–c3：(1,3) 对角 ✓ · c1–c4：(1,2) 列差 3 ✗
- c2–c3：(2,3) 对角 ✓ · c2–c4：同一行 ✓ · c3–c4：(3,2) 对角 ✓
→ **h = 5**

每个空格填"把那一列的 queen 移到这里后的 h"：

```
Step 0  (h = 5)            Step 1  (h = 2)            Step 2  (h = 1)            Step 3  (h = 0)
     c1 c2 c3 c4                c1 c2 c3 c4                c1 c2 c3 c4                c1 c2 c3 c4
r1   Q  3  5  4            r1   Q  1  5  2            r1   Q  Q  4  3            r1   1  Q  3  1
r2   5  Q  4  Q            r2   4  Q  4  Q            r2   3  2  3  Q            r2   3  2  2  Q
r3   5  3  Q  4            r3   2  1  5  2            r3   0  1  3  3            r3   Q  2  2  3
r4   3  4  2* 6            r4   2  2  Q  4            r4   1  2  Q  3            r4   1  3  Q  1
 best: c3 → r4 (h=2)        best: c2 → r1 or r3 (h=1)   best: c1 → r3 (h=0)        goal!
                            (tie → 取第一个 r1)
```

Solution：**(3, 1, 4, 2)**，3 步到达 global minimum。
（Landscape 描述：一路下坡，没有遇到 local minimum 或 plateau；若 Step 1 选到不同的 tie，也可能进入不同的路径。）

### 3.4 Tutorial 7 例：8-puzzle（Manhattan distance）

h = 每个 tile 到 goal 位置的**水平 + 垂直距离**之和。

```
Initial        Goal
 _ 1 3         1 2 3
 4 2 5         4 5 6
 7 8 6         7 8 _
```
h(initial)：tile 1 差 1、tile 2 差 1、tile 5 差 1、tile 6 差 1，其余 0 → **h = 4**；h(goal) = **0**。

Steepest-ascent（这里是 descent：选 h 最小的邻居）：

```
State (blank moves)        successors (h)                     chosen
h=4  _13/425/786           Right(tile1)=3, Down(tile4)=5      Right → h=3
h=3  1_3/425/786           Down(tile2)=2, Left=4, Right(3)=4  Down  → h=2
h=2  123/4_5/786           Right(tile5)=1, Left=3, Down=3, Up=3  Right → h=1
h=1  123/45_/786           Down(tile6)=0, Up=2, Left=2        Down  → h=0 ✓ goal
```
4 步解完，h 严格下降：4 → 3 → 2 → 1 → 0。

**Local beam search**：k = 1 时每步只保留最好的 1 个 → 路径与 hill climbing 相同。k = 2（不走立即的反向动作；同 h 时选 tile 号码小的）：
- 第 1 轮：保留 {Right h3, Down h5}
- 第 2 轮：候选 h2, h4（来自 h3）和 h6, h6（来自 h5）→ 保留 {h2, h4}
- 第 3 轮：候选 h1, h3, h3（来自 h2）和 h5（来自 h4）→ 保留 {h1, h3(tile 4)}
- 第 4 轮：h1 的邻居出现 h0 → goal ✓

### 3.5 Hill climbing 的优点（Jan 2026 Q3b(ii) · May 2026 Q1c(i)，2 分）

> 1. **Low memory consumption** – it only stores the current state (no search tree / frontier).
> 2. **Fast / low computation** – it often makes rapid progress toward a solution and is efficient at improving a bad state (8-queens: from h = 17 to h = 1 in only 5 moves); it can find reasonable solutions in large or infinite state spaces.

### 3.6 为什么会卡住？ —— 三个原因（Oct 2025 Q2d 9 分 · Jan 2026 Q3b(iv) 6 分 · May 2026 Q1c(ii)）

> 1. **Local maxima** – a peak that is higher than each of its neighbouring states but lower than the global maximum. When hill climbing reaches it, every neighbour is worse, so the algorithm stops there with nowhere else to go, returning a sub-optimal solution.
> 2. **Ridges** – a sequence of local maxima (a narrow ridge rising diagonally). From each point on the ridge, all available single-step actions point downhill, so a greedy algorithm, which only moves to better neighbours, finds it very difficult to navigate along the ridge towards the top.
> 3. **Plateaus** – a flat area of the landscape where neighbours have the same value. It can be a **flat local maximum** (no uphill exit exists) or a **shoulder** (uphill progress is possible). Because no neighbour is strictly better, the search has no direction and can get lost wandering, or simply stop.

**数据（课件，8-queens，8⁸ ≈ 17 million states）**：
- 普通 steepest-ascent：**86% 卡住**（平均 3 步），**14% 成功**（平均 4 步）。
- 允许最多 **100 次连续 sideways moves**：**94% 成功**（平均 21 步），6% 卡住（平均 64 步）。

**Disadvantages（May 2026 Q1c(ii)，2 分）**：
> 1. It often gets stuck at local maxima, ridges or plateaus and returns a sub-optimal solution; it never makes downhill moves, so it is **incomplete**.
> 2. The result depends heavily on the initial state, and it does not look ahead beyond immediate neighbours.

### 3.7 解决方法与 variants

1. **Sideways moves**：在 plateau 上允许走"一样高"的邻居，希望它其实是 shoulder（要设上限，例如 100 次，避免在 flat local maximum 上无限绕）。
2. **Backtracking**：记住一些有希望的 visited states；走到不好的地方就退回去换一条路。
3. **Variants**：

| Variant | 做法 | 特点 |
|---|---|---|
| **Stochastic hill climbing** | 从所有**上坡**的动作中**随机**选一个；越陡的选中概率可以越高 | 收敛较慢，但有时找到更好的解 |
| **First-choice hill climbing** | 随机生成邻居，**第一个比当前好的就选** | 当 state 有**很多** successors 时很好用（不用全部生成） |
| **Random-restart hill climbing** | 从**随机生成的初始 states** 重复跑 hill climbing，直到找到 goal | 做得够多次，最终会找到 global maximum（complete with probability → 1） |

**Insight**：hill climbing 从不往下走 → efficient 但 **incomplete**；纯 random walk（均匀随机挑邻居）→ **complete 但极度 inefficient**。能不能两者兼得？→ **simulated annealing**。

📝 **Tutorial 7：排课表 (UCSP) 该用 steepest ascent 还是 variant？**
> Use a variant such as **random-restart** (or first-choice) hill climbing. The UCSP landscape has many local maxima and plateaus (many timetables with the same number of clashes), so basic steepest ascent easily gets stuck. Random restarts escape local maxima by starting again elsewhere, and first-choice avoids generating the huge number of neighbours of each timetable.

---

## Part 4：Simulated Annealing —— 偶尔允许往下走

**Annealing（退火）**：把金属加热到高温，分子快速随机重新排列，然后**慢慢冷却**，改善金属的物理性质。

**乒乓球比喻**（cost function，要找最低点）：
- 让球自己滚 → 会停在 **local minimum**。
- **摇晃**表面 → 球可以弹出 local minimum。
- 诀窍：摇得**够用力**以跳出 local minima，但**不能太用力**以免把球从 global minimum 弹出去。
- 做法：一开始**用力摇（高温 T）**，然后**逐渐减弱（降低 T）**。

课件 pseudocode（Ch3 p35，AIMA Figure 4.5）——这里 VALUE 当成 **cost**（越低越好，所以是找 global minimum）：

```
function SIMULATED-ANNEALING(problem, schedule) returns a solution state
    current ← problem.INITIAL
    for t = 1 to ∞ do
        T ← schedule(t)                                   ← 温度随时间下降
        if T = 0 then return current
        next ← a randomly selected successor of current   ← 随机挑，不是挑最好的
        ΔE ← VALUE(current) − VALUE(next)
        if ΔE > 0 then current ← next                     ← 更好（cost 变低）→ 一定接受
        else current ← next only with probability e^(ΔE/T) ← 更差 → 按概率接受
```

算法要点：
- 不是挑最好的邻居，而是**随机挑一个邻居**。
- **ΔE > 0**（next 的 cost 更低，更好）→ 一定接受。
- **ΔE ≤ 0**（更差）→ 以概率 **e^(ΔE/T)** 接受：
  - 变差越多（ΔE 越负）→ 概率越小；
  - 温度 T 越低 → 概率越小。一开始 T 高，常常接受坏的移动（"用力摇"）；T 慢慢降到 0 时就几乎只接受好的移动，行为接近 hill climbing。
- 例：ΔE = −2、T = 10 → e^(−0.2) ≈ **0.82**；同样 ΔE = −2、T = 1 → e^(−2) ≈ **0.14**。
- 与 **stochastic hill climbing** 的差别：后者**只接受改进**；simulated annealing **有时也接受更差的 state**，让算法有机会最终找到更好的答案。→ 同时兼顾 **efficiency 与 completeness**。

---

## Part 5：Local Beam Search —— 同时派 k 个登山者

- 同时记录 **k 个 states**（beam width），一开始随机生成 k 个。
- 每一步：生成**所有 k 个 states 的所有 successors**；如果有 goal 就停；否则从整张列表里选**最好的 k 个**，重复。

课件图（Ch3 p38，k = 3）：从一个起点生成 3 个 successors（红色 = 被选中的 k 个）→ 下一步把这 3 个的**所有** successors（共 9 个）放在一起比，只留最好的 3 个（红色）→ 再下一步同样。被选中的 3 个**可能都来自同一个 parent**，这就是它"把资源移到进展最多的地方"，也是它**缺乏 diversity** 的原因。

**与 random-restart hill climbing 的差别（tutorial 考）**：

| Random-restart hill climbing | Local beam search |
|---|---|
| 每次搜索**各自独立**进行 | **有用的信息在 k 条搜索之间共享** |
| 没有希望的搜索也会跑完 | 没成果的搜索**立刻被放弃**，资源移到进展最多的地方 |

- ❌ 缺点：k 个 states 很快**挤到同一个区域**（缺乏 diversity）→ 仍会卡在 local maxima / plateau。
- 解决：**Stochastic beam search** —— 按"值越高、概率越高"**随机**选 k 个 successors。

---

## Part 6：Evolutionary Algorithms (EA) —— 让解答"生小孩"

**EA = stochastic beam search 的变体**：successors 不是修改单一 state 产生，而是**把两个 parent states 组合**起来产生。模仿**自然选择**：族群适应环境、更容易生存。

### 6.1 五个 phases（Oct 2025 Q4b 5 分 · Jan 2026 Q2b 15 分）

用课件的 8-queens 例子（每个 state = 8 位数字串，第 i 位 = 第 i 列 queen 所在的行，例如 `24748552`）：

**① Initialization** —— 随机生成 **k 个 states** 组成 **population**。
```
24748552   32752411   24415124   32543213
```

**② Fitness function** —— 用 objective / fitness function 给每个 state 打分。8-queens 用**不互相攻击的 queen 对数**（solution = 28）。
```
24748552 → 24   32752411 → 23   24415124 → 20   32543213 → 11
```
把分数**正规化成概率**：总和 78 → 24/78 = **31%**，23/78 = **29%**，20/78 = **26%**，11/78 = **14%**。越好的 state 越容易被选中。

**③ Selection** —— 按概率**随机选出 pairs** 来繁殖。（例：选出 (32752411, 24748552) 和 (32752411, 24415124)；最差的 32543213 这次没被选中。）每对随机选一个 **crossover point**（第一对在第 3 位之后，第二对在第 5 位之后）。

**④ Crossover** —— 在 crossover point 交换 parent strings：
```
327|52411  +  247|48552   →   327 48552   and   247 52411
32752|411  +  24415|124   →   32752 124   and   24415 411
```

**⑤ Mutation** —— 每一位以一个**小的独立概率**随机改变（8-queens：随机选一个 queen 移到它那一列的随机格子）。课件例子中，第 1、3、4 个 offspring 各有一位被 mutate：
```
32748552 → 32748152   (第 6 位 5 → 1)
24752411 → 24752411   (没有 mutation)
32752124 → 32252124   (第 3 位 7 → 2)
24415411 → 24415417   (第 8 位 1 → 7)
```

**完整流程图（课件 p43，AIMA Figure 4.6）**：

```
(a) Initial      (b) Fitness      (c) Selection    (d) Crossover    (e) Mutation
    Population       Function
24748552          24   31%        327|52411        32748552         32748152
32752411          23   29%        247|48552        24752411         24752411
24415124          20   26%        32752|411        32752124         32252124
32543213          11   14%        24415|124        24415411         24415417
```
（注意 32752411 被选了**两次**，而最差的 32543213 **一次都没被选中**——fitness 越高越容易被选。）

**表示方式（课件 p44）**：8-queens state 写成 8 位数字，例 **17468253**：第 i 位 = 第 i 列（a–h），数字 = 该列 queen 所在的**行号**（这里行 1 在**最下面**，跟棋盘记法一样）。

课件 pseudocode（Ch3 p58，AIMA Figure 4.8）：

```
function GENETIC-ALGORITHM(population, fitness) returns an individual
    repeat
        weights ← WEIGHTED-BY(population, fitness)            ← fitness 越高，权重越大
        population2 ← empty list
        for i = 1 to SIZE(population) do
            parent1, parent2 ← WEIGHTED-RANDOM-CHOICES(population, weights, 2)   ← selection
            child ← REPRODUCE(parent1, parent2)                                  ← crossover
            if (small random probability) then child ← MUTATE(child)            ← mutation
            add child to population2
        population ← population2
    until some individual is fit enough, or enough time has elapsed             ← termination
    return the best individual in population, according to fitness

function REPRODUCE(parent1, parent2) returns an individual
    n ← LENGTH(parent1)
    c ← random number from 1 to n                                                ← crossover point
    return APPEND(SUBSTRING(parent1, 1, c), SUBSTRING(parent2, c + 1, n))
```

### 6.2 Crossover 的三种方式

| Type | 做法 | 例（P1 = 11111111，P2 = 00000000） |
|---|---|---|
| **Single-point** | 选一个点，之后的部分对调 | 1111\|0000 , 0000\|1111 |
| **Two-point**（N-point 的特例） | 选两个点，中间那段对调 | 11\|0000\|11 , 00\|1111\|00 |
| **Uniform** | 每一位**随机**（像掷硬币）决定来自哪个 parent | 10110010 , 01001101 |

课件用的 bit-string 例子（Ch3 p50–52）：

```
Single-point:  Chromosome1  11011|00100110110      Offspring1  11011|11000011110
               Chromosome2  11011|11000011110      Offspring2  11011|00100110110

Two-point:     Chromosome1  11011|00100|110110     Offspring1  11011|11000|110110
               Chromosome2  10101|11000|011110     Offspring2  10101|00100|011110

Uniform:       Parent 1  0000000000…              Child 1   1000110101…
               Parent 2  1111111111…              Child 2   0111001010…
               （每一位掷硬币决定来自哪个 parent；两个孩子在每一位上互补）
```

课件 p48 还把 crossover 画成棋盘：**32752411** 的前 3 列 + **24748552** 的后 5 列 = **32748552**——左半边的 queen 来自 parent 1，右半边来自 parent 2。

**为什么 crossover 有用？** 如果**区块 (blocks)** 本身有用（例：前三个 queen 在 2、4、7 行不互相攻击），crossover 可以把好的区块组合起来。区块用 **schema** 表示：`247*****`（\* = 未指定），符合的字串（如 `24713578`）叫该 schema 的 **instances**。
- 早期 population 很多样 → crossover 步子**大**；后期个体很相似 → 步子**小**。
- **Convergence**：所有个体几乎一样 → 演化停止。

### 6.3 不同的 setup

- **Population size**；**representation**：genetic algorithm = 有限字母的字串；evolution strategies = 实数序列；genetic programming = 计算机程序。
- **Mixing number ρ**：几个 parents 组成一个 offspring。**ρ = 1 → stochastic beam search**；最常见 **ρ = 2**。
- **Selection**：按 fitness 比例随机选（roulette）；或从随机抽出的 n 个里选最 fit 的（tournament）。
- **Mutation rate**：每一位被翻转的概率。
- **New population**：offspring，可再加入几个**最高分的 parents**（**elitism**）→ 保证整体 fitness 不会随时间下降。

### 6.4 Termination / stopping criteria（Jan 2026 Q2c，8 分）

1. **No improvement**：population 的 best/average fitness 连续若干代没有改善（已 converge）。
2. **Fixed number of generations**：达到预先设定的繁殖次数（或时间预算）。
3. **Fitness threshold**：fitness 达到预设的目标值（例：8-queens 达到 28）。

### 6.5 EA 结合了哪些策略的优点？（课件 insight 题）

| EA 的优点 | 来自哪种策略 | 对应哪个 phase |
|---|---|---|
| **Uphill tendency**（往更好的方向） | hill climbing | **Selection**（fitness 高的更常被选） |
| **Random exploration** | stochastic search / random walk / simulated annealing | **Mutation**（和随机 initialization） |
| **Exchange of information among parallel search threads** | local beam search | **Crossover**（组合两个 parent 的区块） |

### 6.6 Tutorial 7 Q3：EA 完整计算

Fitness：**f(X) = (A + B) − (C + D) + (E + F) − (G + H)**，每位 0–9。

**(i) Fitness**
```
X1 = 74235341: (7+4) − (2+3) + (5+3) − (4+1) = 11 − 5 + 8 − 5 =  9
X2 = 32567741: (3+2) − (5+6) + (7+7) − (4+1) =  5 − 11 + 14 − 5 =  3
X3 = 85390164: (8+5) − (3+9) + (0+1) − (6+4) = 13 − 12 + 1 − 10 = −8
X4 = 26730459: (2+6) − (7+3) + (0+4) − (5+9) =  8 − 10 + 4 − 14 = −12
Descending: X1 (9) > X2 (3) > X3 (−8) > X4 (−12)      Parent average = −8/4 = −2
```

**(ii) Crossover**
```
1. Single-point (middle), X1 × X2:
   7423|5341 , 3256|7741  →  74237741 (f = 15) , 32565341 (f = −3)
2. Two-point (after B and after F), X2 × X3:
   32|5677|41 , 85|3901|64 →  32390141 (f = −11) , 85567764 (f = 6)
3. Uniform, X1 × X3, coin pattern X1,X3,X1,X3,X1,X3,X1,X3 (one possible outcome):
   → 75295144 (f = −1) , 84330361 (f = 2)
```

**(iii) 比较**：offspring 平均 = (15 − 3 − 11 + 6 − 1 + 2) / 6 = 8/6 ≈ **1.33** > parents 平均 **−2**，而且最好的个体从 9 进步到 15 → **overall fitness improved**，因为 crossover 把 X1 的高分区块（74 前段）和 X2 的高分区块（77 的 E、F 位置）组合在一起了。

**(v) Optimal solution**：让加号的位最大、减号的位最小 → **99009900**，max fitness = (9+9) − 0 + (9+9) − 0 = **36**。

**(vii) 没有 mutation 能找到 optimal 吗？** **不能。** Crossover 只会**重组**已有的数字，不会在某一位产生新的数字。例如第 A 位在初始 population 里只有 {7, 3, 8, 2}，永远不会出现 9；第 C 位只有 {2, 5, 3, 7}，永远不会出现 0。所以需要 **mutation** 带来新的基因（diversity）。

---

## Closing the loop

回到排课表：我们不再记路径，而是
1. 随便排一张课表（**current state**），
2. 用 **hill climbing** 不断小改——很快变好，却常常卡在 **local maxima / plateau**；
3. 用 **random restart、sideways move、simulated annealing** 逃离；
4. 或者直接用 **EA**：一整群课表互相"交配"（crossover）、偶尔突变（mutation），一代比一代好，直到没有进步或达到代数上限。

但到目前为止，环境里**只有我们自己**。如果对面有一个**专门跟你作对**的对手——下棋的时候——该怎么搜索？这就是 Chapter 4。

---

## ⚠️ Where the slides mislead

| Slide | 课件写法 | 更准确的理解 |
|---|---|---|
| Random-restart | "Unfortunately, if there is no local maxima, then it will always get the same best state." | 如果**没有** local maxima，普通 hill climbing 本来就会直达 global maximum，每次重启得到同一个最佳 state **并不是坏事**。课本原意是：local maxima 越少，random restart 越快找到好解。 |
| Flat local maximum | "All neighboring states of the current state have the same value." | 还要加上：**这个平台没有往上的出口**（边缘都往下）——这是它与 shoulder 的分别。 |
| Simulated annealing (p35) | pseudocode 的 VALUE 当 cost 用（ΔE = VALUE(current) − VALUE(next) > 0 才算改进），但前面 hill climbing 的 VALUE 是越高越好 | 两段 pseudocode 的 VALUE 方向相反：hill climbing 找最大，simulated annealing 这里找最小（配合 p33 的 "gradient descent / global minimum"）。考试解释时写清楚你的 VALUE 是 cost 还是 objective。 |

---

## Exam radar

| Paper | 题目 | 分数 |
|---|---|---|
| Oct 2025 Q2 | greedy? (2) · landscape objective (7) · landscape **cost** (7) · **3 causes** (9) | **25** |
| Oct 2025 Q4b | EA 5 key concepts | 5 |
| Jan 2026 Q2 | EA 交通灯：分析 (2) · 5 phases (5+10) · 2 stopping criteria (8) | **25** |
| Jan 2026 Q3b | greedy? (2) · 2 strengths (2) · landscape objective (7) · 2 causes (2+4) | 17 |
| May 2026 Q1 | 2 optimisation examples (2) · local vs classical (4) · 2 adv (2) · 2 disadv (2) · 2 other local search (2) · 5 elements (5) · sketch landscape (8) | **25** |

### 📝 Jan 2026 Q2：用 EA 优化交通灯（完整答案）

**(a) How can an EA help?（2 分）**
> Traffic patterns are dynamic and unpredictable, and the number of possible timing combinations for many intersections is huge, so traditional algorithms cannot search them efficiently. An EA keeps a population of candidate timing plans and evolves them over generations — keeping plans that give lower waiting time, higher flow rate and better fuel efficiency and combining/mutating them — so it can find near-optimal signal timings without exhaustively searching every combination, and can adapt as traffic changes.

**(b) Five phases（名称 5 分 + 解释 10 分）**
> 1. **Initialization** – Randomly generate a population of k candidate timing plans. Each individual is encoded as a string, e.g. the green-light durations (in seconds) of each phase at each junction: `[30, 45, 20, 60, …]`.
> 2. **Fitness function** – Evaluate each timing plan (e.g. in a traffic simulation) with a fitness function combining the three objectives, e.g. fitness = w₁·(traffic flow rate) + w₂·(fuel efficiency) − w₃·(average waiting time). Higher fitness = better plan; scores are normalised into selection probabilities.
> 3. **Selection** – Choose parent plans for reproduction with probability proportional to their fitness (or by tournament), so plans with shorter waiting times are more likely to pass on their timings.
> 4. **Crossover** – Combine two parent plans at a randomly chosen crossover point (single-point, two-point or uniform), e.g. take the timings of junctions 1–3 from parent 1 and junctions 4–6 from parent 2, producing offspring that mix good timing blocks.
> 5. **Mutation** – With a small probability, randomly change a gene, e.g. increase or decrease one green duration by a few seconds. This keeps diversity and lets the EA explore timings not present in the initial population, avoiding premature convergence.

**(c) Two stopping criteria + recommendation（8 分）**
> 1. **Maximum number of generations / time limit** – stop after a predefined number of reproduction cycles (e.g. 200 generations). This guarantees the computation time is bounded, which matters because new timings must be produced before peak hours.
> 2. **No improvement (convergence)** – stop when the best fitness has not improved for a set number of consecutive generations (e.g. 20), meaning the population has converged and further generations waste computation.
> (3. Fitness threshold – stop once a plan reaches a target, e.g. average waiting time below 30 s.)
>
> **Recommendation**: use a **combination** — stop when there is no improvement for N generations **or** when the maximum number of generations is reached, whichever comes first. The no-improvement rule avoids wasting time after convergence (efficiency), while the generation cap guarantees termination within the available time even if the fitness keeps changing slightly, so optimal performance is balanced against computation time.

### 📝 Oct 2025 Q4b：EA 的 5 key concepts（5 分）

> 1. **Initialization (population)** – start with k randomly generated individuals (candidate solutions encoded as strings).
> 2. **Fitness function** – rates how good each individual is; converted into selection probabilities.
> 3. **Selection** – fitter individuals are more likely to be chosen as parents.
> 4. **Crossover** – two parents exchange parts of their strings at crossover point(s) to form offspring.
> 5. **Mutation** – each gene may be randomly changed with a small probability to maintain diversity.

### 📝 May 2026 Q1c(iii)：Two other local search algorithms（2 分）
> **Simulated annealing** and **local beam search** (also acceptable: evolutionary / genetic algorithms, stochastic hill climbing, random-restart hill climbing).

---

## Cheat sheet

| 项目 | 要点 |
|---|---|
| Optimization problem | find best solution among all feasible solutions, using an objective function |
| Examples | 8-queens, TSP, course scheduling, cutting stock |
| Local search | neighbours only, no paths kept, not systematic; low memory; large/infinite spaces |
| Landscape | objective → global maximum (hill climbing); cost → global minimum (gradient descent) |
| 5 elements | current state, global max, local max, flat local max, shoulder |
| Hill climbing | move to best neighbour; stop at peak; greedy; incomplete |
| Stuck causes | local maxima, ridges, plateaus (flat local max / shoulder) |
| 8-queens stats | 56 successors; 86% stuck / 14% success; sideways ≤100 → 94% success |
| Variants | stochastic (random uphill), first-choice (first better random neighbour), random-restart |
| Simulated annealing | random move; accept worse with probability decreasing with T; high T → low T |
| Local beam | k states, keep k best successors; shares info; stochastic beam for diversity |
| EA phases | initialization, fitness, selection, crossover, mutation |
| Crossover types | single-point, two-point, uniform |
| Schema | 247***** ; instances match it |
| ρ | mixing number; ρ = 1 → stochastic beam search |
| Termination | no improvement / fixed generations / fitness threshold |
| EA strengths | uphill (selection), random exploration (mutation), info exchange (crossover) |

---

## Practice (answers included)

### A. MCQ

1. Which variant picks the **first** randomly generated neighbour that is better than the current state? (a) stochastic (b) first-choice (c) random-restart (d) steepest-ascent
2. In an EA, with mixing number ρ = 1, the algorithm becomes: (a) hill climbing (b) random walk (c) stochastic beam search (d) simulated annealing
3. A plateau whose edge leads further uphill is a: (a) ridge (b) local maximum (c) shoulder (d) flat local maximum
4. Simulated annealing differs from stochastic hill climbing because it: (a) keeps k states (b) sometimes accepts worse moves (c) uses crossover (d) always picks the best move
5. Number of successors of an 8-queens state (one queen per column): (a) 8 (b) 28 (c) 56 (d) 64

**Answers**：1 (b) · 2 (c) · 3 (c) · 4 (b) · 5 (c)

### B. Short answer

**B1.** Differentiate local beam search from random-restart hill climbing. (4 marks)
> In random-restart hill climbing, each search runs independently of the others. In local beam search, the k searches share information: all successors of all k states are pooled and only the best k are kept, so unfruitful searches are abandoned immediately and resources move to where most progress is being made. (But local beam search may lose diversity and crowd into one region.)

**B2.** Explain how simulated annealing avoids getting stuck at a local maximum. (4 marks)
> It picks a random neighbour. Better moves are always accepted; worse moves are accepted with a probability that decreases as the move gets worse and as the "temperature" T is lowered. At the start T is high, so the search often moves downhill and can escape local maxima; as T slowly decreases, it behaves more like hill climbing and settles at a (hopefully global) maximum.

### C. Calculation

**C1.** 4-queens state (2, 4, 1, 3) (row of queen in columns 1–4). Compute h.
> Pairs: c1–c2 (2,4) diff 2, col diff 1 ✗ · c1–c3 (2,1) diff 1, col diff 2 ✗ · c1–c4 (2,3) diff 1, col diff 3 ✗ · c2–c3 (4,1) diff 3, col diff 1 ✗ · c2–c4 (4,3) diff 1, col diff 2 ✗ · c3–c4 (1,3) diff 2, col diff 1 ✗ → **h = 0** (this is a solution).

**C2.** Two parents 12345678 and 87654321, two-point crossover after the 2nd and 6th digits. Give the offspring.
> 12|3456|78 and 87|6543|21 → **12654378** and **87345621**.

### D. Thinking

**D1.** Why is the population's diversity important in an EA, and which phase maintains it?
> If all individuals become identical (convergence), crossover produces nothing new and evolution stops, possibly at a sub-optimal solution. **Mutation** (and a random initial population) introduces new genes and keeps diversity, so the EA can still explore.

**D2.** Would you use A\* or hill climbing for the 1,000,000-queens problem? Why?
> Hill climbing (or min-conflicts local search). The path does not matter, only the final board, and the state space is astronomically large; A\* would need to store an exponential frontier, whereas local search uses almost no memory and can reach a solution in a few dozen steps (min-conflicts solves the million-queens problem in ~50 steps on average).
