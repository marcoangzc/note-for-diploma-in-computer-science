# AMCS2104 — Chapter 3: Local Search and Optimization Problems

> Slide 的问题：算法只给伪代码图；8-queens 的数字（h = 17、12、1）没有说明怎么算出来；Simulated Annealing 的公式符号会让人困惑（VALUE 在这里是 cost）；有几处说法过头（SA "completeness"、random-restart 那句话不清楚）。这份笔记把 8-queens 的 h 值、hill climbing 的成功率、GA 的整个例子都用代码重新算过。

---

## 0. 一句话总览

前一章的 search 需要**记住路径**、系统地探索；本章的问题**只关心最终状态好不好**（路径无所谓），所以只保存**一个（或几个）当前状态**，不断看邻居、往更好的方向走 —— 内存极少，但可能卡住。

| 主题 | 一句话 |
|---|---|
| Optimization problem | 在所有可行解里找**最优**（由 objective function 打分） |
| State-space landscape | 把每个状态画成"高度"（= objective 或 cost） |
| Hill climbing | 只走向最好的邻居；快但会卡在 local maximum、ridge、plateau |
| 变体 | stochastic、first-choice、random-restart、允许 sideways move |
| Simulated annealing | 随机选邻居；变差的移动以**随温度下降而变小的概率**被接受 |
| Local beam search | 同时保留 k 个状态，每轮从**所有**后继里挑最好的 k 个 |
| Evolutionary / genetic algorithms | 用 selection、crossover、mutation 演化一个 population |

---

## 1. Classical search vs. Optimization / Local search

| | Classical search（Ch2） | Local search |
|---|---|---|
| 问题 | 从 initial 到 goal 的**路径** | **找到好的状态本身**（例：8-queens 的最终摆法） |
| 是否保留路径 / reached | 是 | **否** |
| 是否系统 | 系统地探索 | **不系统** |
| 内存 | 指数 / 大 | 极少（常数） |

**Optimization problem** = 从所有 feasible solutions 里找最好的，用 **objective function** 打分。**Candidate solutions** = 可能的解集合。例子（slide 5–6）：8-queens、Traveling salesman、Course scheduling、Cutting stock。

优点：内存少；在**很大甚至无限**的状态空间里常常也能找到还不错的解。

---

## 2. State-space landscape

把每个状态想象成地面上的一个点，**elevation** = 该状态的 objective（或 cost）值。

```
objective
   ▲            global maximum
   │              ▲
   │      shoulder│   local maximum      "flat" local maximum
   │      ____    │        ▲                  ______
   │     /    \   │       / \      ____      /      \
   │    /      \  │      /   \    /    \____/        \
   │___/        \_│_____/     \__/                    \____
   └──────────────────────────────────────────────────────► state space
```

| 术语 | 意思 |
|---|---|
| Current state | agent 现在的位置 |
| Global maximum | objective 最高的状态（最好） |
| Local maximum | 比所有邻居都高，但不是最高 |
| Flat local maximum | 邻居**全部**一样高（一片平地，没有上坡出口） |
| Shoulder | 平台，但边缘**向上延伸**（走出去还能继续爬） |
| Ridge（slide 24） | 一串 local maxima，**每个 local maximum 出发的动作都向下**，贪心很难沿着山脊走 |

| elevation 代表 | 目标 | 方法名（slide 11） |
|---|---|---|
| Objective function | 找 global **maximum** | hill climbing |
| Heuristic cost function | 找 global **minimum** | slide 称为 "gradient descent" |

⚠️ 严格说 gradient descent 是**连续、可微**函数上的方法；这里的离散状态空间上"往更低 cost 走"其实就是 hill climbing 的反方向。考试按 slide 用词就好。

---

## 3. Hill climbing（steepest-ascent）

```
HILL-CLIMBING(problem):
    current ← problem.INITIAL
    loop:
        neighbor ← 值最高的 successor
        if VALUE(neighbor) ≤ VALUE(current): return current    # 到达 peak
        current ← neighbor
```

- 只保留**一个** current state；每步移到**最好的邻居**；没有更好的邻居就停；**不会往前看超过直接邻居**。
- 别名 **greedy local search**：优点是快、内存 / 计算都少、常常能很快改善一个差的状态。

### 3.1 8-Queens 的 formulation（slide 15–20）

- **Complete-state formulation**：8 个 queen 都在盘上，**每列一个**。状态用 8 个数字表示，第 i 位 = 第 i 列 queen 所在的**行**（例：`17468253`）。
- **Successors** = 把某一列的 queen 移到同一列的**另一格**：8 列 × 7 个位置 = **56**（代码验证）。
- **h = 互相攻击的 queen 对数**（直接或间接，同行 / 同对角线；同列不会因为每列一个）。**global minimum = 0**，只在解那里出现。

我用代码核对了 slide 里所有的 h 值：

| 状态 | h | 说明 |
|---|---|---|
| slide 16 的图（每列的行：6 4 2 8 5 7 1 3） | **0** | 这是一个解 |
| slide 19 左（每列的行：5 6 7 4 5 6 7 6） | **17** | 与 slide 20 的图是同一个状态 |
| slide 19 右（每列的行：1 6 7 8 7 6 7 6） | **16** | ⚠️ 我从图上读出 queen 位置后计算，没有 slide 的标准答案 |
| slide 18 的 local minimum（每列的行：8 3 7 4 2 5 1 6） | **1** | 它的 56 个 successors 的 h **全部 ≥ 2**（最小是 2）→ 真的是 local minimum |

**h = 17 的那一页（slide 20）**：56 个 successors 里最小的 h = **12**，共有 **8 个并列**最小的（我数过：slide 图里标出的 12 有 8 个）。slide 问"选哪个？"—— steepest-ascent 的做法是**在并列的里面随机挑一个**。

### 3.2 Hill climbing 的表现（slide 26–27）

我自己写了 hill climbing 各跑 3000 次随机初始状态（tie 随机选）：

| | 成功率 | 成功的平均步数 | 卡住的平均步数 |
|---|---|---|---|
| 基本版（我的模拟） | 14.6% | 4.1 | 3.1 |
| Slide 26 | 14% | 4 | 3 |
| 允许最多 100 次连续 sideways（我的模拟） | 94.4% | 19.0 | 62.7 |
| Slide 27 | 94% | 21 | 64 |

（和 slide 差一点是正常的：随机性 + 我的 tie-breaking / 计步方式和课本可能不同。）

**结论**：状态空间有 8⁸ ≈ 1,700 万个状态，hill climbing 平均只用 3–4 步就能到一个 peak —— 很快，但 **86% 的时候停在 local minimum**。

### 3.3 Hill climbing 会卡在哪里

| 情况 | 原因 |
|---|---|
| **Local maxima** | 比邻居高、但不是最高；到了就无路可走 |
| **Ridges** | 一串 local maxima，贪心步进很难沿脊线走 |
| **Plateaus** | 平地：flat local maximum 无出口；shoulder 有出口，但可能在上面乱走 |

### 3.4 变体

| 变体 | 做法 | 补充 |
|---|---|---|
| **Sideways move** | 平地时也允许走同值的邻居，希望它其实是 shoulder | 必须**限制次数**（例：100 次），否则在 flat local maximum 上无限循环；把成功率从 14% 提到 94% |
| **Stochastic hill climbing** | 在**所有 uphill 移动**里随机选一个（可按坡度加权） | |
| **First-choice hill climbing** | 随机生成邻居，选**第一个比现在好的** | successors 很多时（例：几千个）特别有用 |
| **Random-restart hill climbing** | 从随机初始状态重复 hill climbing，直到找到 goal | 如果单次成功概率是 p，**期望重启次数 = 1/p** |

**Random-restart 的数字（代码算出）**：
- 基本版 p ≈ 0.14：期望重启 ≈ 7.1 次；期望步数 ≈ (1−p)/p × 3 + 4 ≈ **22**。
- 允许 sideways，p ≈ 0.94：期望重启 ≈ 1.06 次；期望步数 ≈ (1−p)/p × 64 + 21 ≈ **25**。（即使每次更"耐心"，总步数也差不多，但**成功率**高得多。）

slide 28 的 "backtracking"（保留有希望的已访问状态、走到坏状态就退回去）不在标准的 hill climbing 里，当作补充知识。

**slide 31 的总结**：hill climbing **永远不做下坡** → 一定 incomplete；purely random walk 是 complete 但极慢。所以后面的算法（stochastic、first-choice、random-restart，然后是 SA）都是在"往上走"和"随机探索"之间找平衡。

---

## 4. Simulated Annealing（SA）

**灵感**：退火 —— 金属加热到高温、再**缓慢**冷却，分子排列更好。

**弹珠比喻（slide 34）**：把一个乒乓球放到凹凸不平的表面上，找最深的凹槽。让它自己滚，会停在**local minimum**；摇晃这个表面可以把它震出来，但摇太用力又会把它从**global minimum** 震出去。所以：**先大力摇（高温 T），然后逐渐减小力度（降低 T）**。

### 4.1 算法（slide 35）

```
SIMULATED-ANNEALING(problem, schedule):
    current ← problem.INITIAL
    for t = 1 to ∞:
        T ← schedule(t)
        if T = 0: return current
        next ← 随机选一个 successor
        ΔE ← VALUE(current) − VALUE(next)
        if ΔE > 0: current ← next                       # 变好：一定接受
        else:      current ← next  只以概率 e^(ΔE / T)   # 变差：以一定概率接受
```

⚠️ **符号陷阱**：这里 **VALUE 是 cost（越小越好）**。所以 ΔE > 0 表示"next 的 cost 比 current 低 = 更好"；ΔE ≤ 0 表示更差，ΔE 是**负数**，e^{ΔE/T} < 1。（如果你把 VALUE 想成 objective（越大越好），符号就反了 —— 这是本页最容易搞混的地方。）

### 4.2 接受概率随温度变化（代码算出）

变差程度 ΔE = −2（cost 增加 2）时：

| 温度 T | 接受概率 e^{−2/T} | 直观意思 |
|---|---|---|
| 100 | 0.980 | 几乎什么都接受 → 接近 random walk |
| 10 | 0.819 | 大多数变差的也接受 |
| 1 | 0.135 | 偶尔接受 |
| 0.1 | ≈ 2 × 10⁻⁹ | 几乎不接受 → 接近 hill climbing |

变差得**越多**，被接受的概率也**越小**（ΔE 越负，e^{ΔE/T} 越小）。

### 4.3 与其他算法的关系

- **Stochastic hill climbing**：只在变好时才移动。
- **Simulated annealing** = stochastic hill climbing + **有时接受变差的**，才能逃出 local optimum。
- T → ∞ ≈ random walk；T → 0 ≈ hill climbing。

⚠️ slide 32 说 SA "yields both efficiency and completeness"：严格来说，**只有在降温足够慢**时才有"概率趋近 1 找到全局最优"的理论保证，实际应用中做不到，所以不要把它当作真正的 complete 算法。

---

## 5. Local Beam Search

- 保留 **k 个**状态（beam width = k），从 k 个随机状态开始。
- **每一步**：生成**所有 k 个状态的所有后继**，放在一起；如果有 goal 就停；否则选**最好的 k 个**继续。

⚠️ **不等于"并行跑 k 次 hill climbing"**（slide 39）：

| Random-restart hill climbing | Local beam search |
|---|---|
| k 个搜索**独立**进行 | 信息**互相传递**：好状态的后继会"抢走"差状态的名额 |
| 差的搜索也继续到底 | 没有前景的搜索**立刻被放弃**，资源转移到有进展的地方 |

缺点：k 个状态很快**集中**到同一区域，又容易陷入 local maxima / plateau。**Stochastic beam search**：不是取最好的 k 个，而是**按适应度成比例的概率随机选** k 个后继。（k = 1 时，local beam search = hill climbing。）

---

## 6. Evolutionary / Genetic Algorithms

**想法**：像自然选择一样，一群（population）个体不断繁殖，好的更容易留下来；后继不是修改一个状态，而是**组合两个 parent**。EA 可以视为 stochastic beam search 的变体。

### 6.1 五个阶段

1. **Initialization**：随机生成 k 个状态（population）。
2. **Fitness function**：给每个状态打分（越高越好），再归一化成被选中的**概率**。
3. **Selection**：按概率**随机**选 parent（有放回，好的可能被选多次）。
4. **Crossover**：两个 parent 在随机点切开互换。
5. **Mutation**：每个位置以**很小的独立概率**随机改变。

### 6.2 完整的 8-Queens 例子（slide 43–54，我用代码逐项验证）

编码：8 位数字，第 i 位 = 第 i 列 queen 所在的行。

**(a) Initial population + (b) fitness**（fitness = **不互相攻击的 pairs 数**，满分 = C(8,2) = **28**）

| 状态 | Fitness | 概率 |
|---|---|---|
| 24748552 | 24 | 24/78 = 30.8% ≈ 31% |
| 32752411 | 23 | 29.5% ≈ 29% |
| 24415124 | 20 | 25.6% ≈ 26% |
| 32543213 | 11 | 14.1% ≈ 14% |
| 合计 | 78 | 100% |

⚠️ 注意与 hill climbing 的差别：**fitness = 28 − h**（h = 攻击对数）。hill climbing 要**最小化 h**（目标 0），这里要**最大化 fitness**（目标 28）—— 方向相反，同一件事。

**(c) Selection**：按概率抽了 2 对：(32752411, 24748552) 和 (32752411, 24415124)（32752411 被选中两次，32543213 一次也没被选）。crossover 点：第一对在第 3 位后，第二对在第 5 位后。

**(d) Crossover**：

| 对 | Parent 1 | Parent 2 | Child 1 | Child 2 |
|---|---|---|---|---|
| 1 | 327 \| 52411 | 247 \| 48552 | 327 + 48552 = **32748552** | 247 + 52411 = **24752411** |
| 2 | 32752 \| 411 | 24415 \| 124 | 32752 + 124 = **32752124** | 24415 + 411 = **24415411** |

**(e) Mutation**：第 1、3、4 个孩子各有 1 位变了：

| 孩子 | 突变后 | 变化 |
|---|---|---|
| 32748552 | 32748**1**52 | 第 6 位 5 → 1 |
| 24752411 | 24752411 | 没变 |
| 32752124 | 32**2**52124 | 第 3 位 7 → 2 |
| 24415411 | 2441541**7** | 第 8 位 1 → 7 |

新一代的 fitness（代码算出）：突变前 23、22、21、20；突变后 24、22、18、22 —— 注意**突变可能让个体变好也可能变差**（第三个从 21 降到 18）。

### 6.3 Crossover 的种类（slide 50–52）

| 种类 | 做法 |
|---|---|
| Single-point | 选一个切点，把切点之后的部分互换 |
| Two-point（N-point 的特例） | 选两个点，中间那段互换 |
| Uniform | 每一位像抛硬币一样从某个 parent 复制 |

- Crossover 早期 population 差别大 → 大步跳跃；后期个体越来越像 → 小步。当所有个体都一样，进化停止 → **convergence**。
- **Schema**：部分位置未指定的子串。例：`247*****` 描述所有前三个 queen 在第 2、4、7 行的状态；`24713578` 是这个 schema 的一个 **instance**。如果这个"前三个 queen"的搭配本身就有用，crossover 可以把它和别的有用块拼在一起 —— 这正是 EA 相对其他方法的主要优势。

### 6.4 不同的设定（slide 55–57）

| 设定 | 内容 |
|---|---|
| Population size | 个体数 |
| 个体表示 | genetic algorithm：有限字母表上的字符串；evolution strategies：一串实数；genetic programming：一段程序 |
| **Mixing number ρ** | 组合成一个后代的 parent 数量；最常见 ρ = 2；**ρ = 1 就是 stochastic beam search** |
| Selection 方式 | 按 fitness 比例选全体；或从随机挑出的 n 个里选 ρ 个最好的 |
| Mutation rate | 每个位置突变的概率 |
| 新一代的构成 | 只有新后代；或再加几个上一代**最好的个体**（这样 fitness 不会下降；补充：这叫 elitism） |

### 6.5 终止条件（slide 59）

population 不再进步；达到预设的**世代数**；fitness 达到预设值。

### 6.6 slide 60 的问题

EA 结合了三种策略：**uphill tendency**（hill climbing）、**random exploration**（random walk / 突变）、**在并行搜索之间交换信息**（local beam search）。对应到 EA 的阶段：**selection ↔ uphill tendency**；**mutation ↔ random exploration**；**crossover ↔ 信息交换**。

---

## ⚠️ Slide 里有问题或需要小心的地方

| Slide | Slide 写的 | 更准确的理解 |
|---|---|---|
| 3-11 / 3-33 | 最小化 cost 的版本叫 "gradient descent" | gradient descent 严格指连续、可微函数上的方法；离散状态上等同于"hill climbing 反方向"。考试按 slide 用词 |
| 3-30 | random-restart："if there is no local maxima, then it will always get the same best state" | 意思不清。真实要点：单次 hill climbing 成功概率 p → 期望重启 1/p，最终一定会成功（概率 → 1）；如果**没有** local maxima，一次 hill climbing 就够了，根本不需要重启 |
| 3-32 | SA "yields both efficiency and completeness" | 只在降温**足够慢**时才理论上趋近最优，不是一般意义的 complete |
| 3-35 | ΔE = VALUE(current) − VALUE(next)，ΔE>0 就接受 | 这里的 VALUE 是 **cost**；如果 VALUE 是 objective，符号反了（见 4.1） |
| 3-36 | SA "accepts worse states to *learn* answers that are eventually better" | 没有"学习"，是随机探索以逃出 local optimum |
| 3-41 | EA "identify the perfect combination" | EA 给的是好的解，不保证最优 |
| 3-58 | GA 伪代码每次 REPRODUCE 返回**一个** child | 而 slide 43–48 的图里每对 parent 产生**两个** child（图是简化的示例） |
| 3-22 | "Only 5 moves"：h=17 → h=1 | ⚠️ 这条我**没有逐步验证**那条 5 步路径（只验证了两个端点的 h 值） |

---

## Cheat sheet

| 算法 | 关键点 | 会不会卡住 |
|---|---|---|
| Hill climbing | 移到最好的邻居；没更好就停 | 会：local max、ridge、plateau |
| Sideways moves | 平地也走，限制次数 | 大幅减少（14% → 94%） |
| Stochastic / First-choice | 随机选上坡 / 第一个更好的 | 仍会 |
| Random-restart | 重复 + 随机初始 | 期望重启 1/p，最终成功 |
| Simulated annealing | 随机邻居；变差以 e^{ΔE/T}（ΔE<0）接受；T ↓ | 降温慢才能逃出 |
| Local beam (k) | k 个状态，从所有后继挑 k 个最好 | 会集中；stochastic beam 缓解 |
| Genetic / EA | selection、crossover、mutation | 可能 convergence 到同一个 |

8-queens：状态 = 8 位数字；successors = 56；h = 攻击对数（min 0）；fitness = 28 − h（max 28）。

---

## Practice

### A. 选择题（5）

**A1.** 下面哪个**不是** hill climbing 会卡住的情形？
(a) local maximum  (b) ridge  (c) plateau  (d) global maximum

**A2.** Simulated annealing 在**温度很高**时表现得像什么？
(a) hill climbing  (b) random walk  (c) BFS  (d) local beam search

**A3.** Local beam search 与"并行的 k 次 random-restart hill climbing"最大的区别？
(a) 用了更多内存  (b) 各搜索之间共享信息，差的被放弃  (c) 不会陷入 local maxima  (d) 只用一个状态

**A4.** 在 8-queens 的 GA 中，crossover 作用于什么？
(a) 单个状态的一位  (b) 两个 parent 状态  (c) population 的大小  (d) fitness function

**A5.** EA 里哪个阶段对应"random exploration"？
(a) selection  (b) crossover  (c) mutation  (d) initialization

### B. 简答题（3）

**B1.** 为什么 hill climbing 的 sideways move 必须**限制次数**？

**B2.** 比较 stochastic hill climbing、first-choice hill climbing、random-restart hill climbing 的做法。

**B3.** 什么是 schema？为什么它和 crossover 的优势有关？

### C. 计算 / 追踪（3）

**C1.** 一维 landscape（下标 0–9，值为 `[3, 5, 4, 6, 8, 7, 5, 9, 10, 6]`），邻居 = 左右相邻。用 steepest-ascent hill climbing 分别从下标 **0、3、6** 出发，写出路径和最终值。

**C2.** SA 中 cost 增加 1（ΔE = −1）：T = 5 和 T = 0.5 时接受的概率各是多少？

**C3.** 8-queens GA：parent 1 = `13572468`，parent 2 = `86421357`，crossover 点在第 3 位之后。写出两个 child，并算出 parents 和 children 的 fitness（不互相攻击的 pairs 数，满分 28）。

### D. 思考题（2）

**D1.** 8-queens 里，基本 hill climbing 成功率约 14%，允许 sideways 后约 94%。用 random-restart 时，两种版本的期望重启次数各是多少？

**D2.** EA 结合了哪三种搜索策略？它们分别对应 EA 的哪个阶段？

---

### 答案

**A1.** (d)。到达 global maximum 是成功，不是卡住。

**A2.** (b)。高温下几乎接受所有移动，像 random walk；低温才像 hill climbing。

**A3.** (b)。

**A4.** (b)。crossover 把两个 parent 在切点处拼成 child。

**A5.** (c)。

**B1.** 如果是 **flat local maximum**（平地没有出口），sideways move 会无限循环。限制连续 sideways 次数（例：100）可以在"这个平台其实是 shoulder"的希望和"无限循环"的风险之间取平衡。

**B2.**
- **Stochastic**：在所有上坡移动里**随机**挑一个（可按坡度加权）。
- **First-choice**：随机生成邻居，选**第一个**比现在好的（successors 很多时很有用）。
- **Random-restart**：重复从随机初始状态跑 hill climbing，直到成功。

**B3.** Schema = 部分位置未指定的子串（例：`247*****`）。它代表"前三个 queen 在第 2、4、7 行"这样的**有用构件**；crossover 可以把不同 parent 上各自有用的构件组合起来，这是 EA 相对 hill climbing 的主要优势（前提是这些块确实有用）。

**C1.**（代码验证）
- 从 0：0（值 3）→ 1（值 5）；下标 0 值 3、下标 2 值 4，都比 5 低 → **停在下标 1，值 5**（local maximum）。
- 从 3：3（值 6）→ 4（值 8）；邻居 6（下标 3）、7（下标 5）都比 8 低 → **停在下标 4，值 8**（local maximum）。
- 从 6：6（值 5）→ 7（值 9）→ 8（值 10）；邻居 9、6 都低 → **停在下标 8，值 10**（global maximum）。

**C2.** T = 5：e^{−1/5} ≈ **0.819**；T = 0.5：e^{−1/0.5} = e^{−2} ≈ **0.135**。温度越低，越不容易接受变差的移动。

**C3.**（代码验证）
- Child 1 = `135` + `21357` = **13521357**；Child 2 = `864` + `72468` = **86472468**。
- Fitness：parent 1 = 27，parent 2 = 25；child 1 = 23，child 2 = 24。
- 注意：两个 child 的 fitness 都**比 parents 低** —— crossover 不保证变好，这也是为什么需要 selection 反复筛选。

**D1.** 期望重启次数 = 1/p：基本版 p ≈ 0.14 → ≈ **7.1** 次；带 sideways p ≈ 0.94 → ≈ **1.06** 次。

**D2.** ① uphill tendency（hill climbing）↔ selection；② random exploration（random walk）↔ mutation；③ 在并行搜索之间交换信息（local beam search）↔ crossover。

---

## 与其他章节的联系

- Ch2 的 8-queens 有 incremental 和 complete-state 两种 formulation；**本章用 complete-state**（8⁸ ≈ 1.7×10⁷ 个状态）。
- Ch1C 的 model-based / utility-based 思想：SA 的 e^{ΔE/T} 是在"效用差"上做随机决策。
- Ch2 的 A* 用 h 估计剩余成本；本章的 h 是**评价当前状态好坏**（8-queens 的 h = 攻击对数）—— 同样叫 heuristic，用途不同。
- Ch4 的 evaluation function 与本章的 objective / fitness function 同类：都是给状态打分。
