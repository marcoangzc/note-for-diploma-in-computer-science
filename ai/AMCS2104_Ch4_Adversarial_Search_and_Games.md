# AMCS2104 — Chapter 4 (4A + 4B): Adversarial Search and Games

> Slide 的问题：minimax 和 alpha-beta 的例子全是图，没有把每个节点的 α、β 写出来；有几处明显的错误 / 前后矛盾（alpha-beta "减少一半" vs 4B 的 O(b^{m/2})、α > β vs 伪代码的 ≥、初始 α β 的描述、一个 B/C 打字错误）。这份笔记补上逐步 trace，所有例子都用代码重新算过（包括 slide 4B 让你自己做的 "右到左顺序" 那一题）。

---

## 0. 一句话总览

在**对手会反击**的环境里（两个 agent 目标冲突），用 **minimax** 假设对手也走最优，在**game tree** 上算出每个状态的价值；**alpha-beta pruning** 剪掉不可能影响决定的分支（结果和 minimax 完全一样，但快很多）；真实游戏树太深，所以要**在中途截断**并用 **evaluation function** 估计。

| 部分 | 内容 |
|---|---|
| 4A | 游戏的形式化；game tree；minimax；multiplayer；alpha-beta |
| 4B | move ordering；transposition table；Type A / B；heuristic evaluation；cutoff、quiescence、horizon effect；forward pruning；search vs lookup |

---

## 1. (4A) 游戏作为 search 问题

**Adversarial search / games**：竞争环境里 agents 的目标冲突。AI 里最常研究的是：**turn-taking、two-player、perfect information（= fully observable）、deterministic、zero-sum**（对一方好的就是对另一方同等程度的坏）。例：Chess、Go、Tic-Tac-Toe。

术语：**move** = action；**position** = state；两个玩家叫 **MAX**（先走）和 **MIN**。

### 1.1 一个游戏的形式化（6 个要素）

| 要素 | 意思 | Tic-tac-toe |
|---|---|---|
| S₀ | 初始状态 | 空的 3×3 |
| ACTIONS(s) | s 里的合法着法 | 在空格放 X（MAX）或 O（MIN） |
| RESULT(s,a) | 着法的结果 | 该格被占 |
| TO-MOVE(s) | 轮到谁 | MAX 先，之后轮流 |
| IS-TERMINAL(s) | 游戏结束了吗 | 三连或棋盘满 |
| UTILITY(s,p) | 终局时玩家 p 的收益 | +1（MAX 赢）、0（和）、−1（MAX 输） |

（chess 的 utility：赢 1、输 0、和 ½。）

### 1.2 Game tree

**Game tree** 是叠在 state space 上的 search tree，表示双方轮流走后所有可能的状态。**Complete game tree** 从初始位置一直到所有 terminal states；terminal node = leaf。

**Ply** = 一个玩家的一步。slide 18 的 "two-ply game tree" = MAX 走一步 + MIN 走一步。

**Tic-tac-toe 的数字（代码枚举）**：完整游戏树有 **255,168** 个终局（terminal nodes，即所有可能的完整棋局），比 slide 的上界 9! = 362,880 小；不同的棋盘状态只有 **5,478** 个；**minimax 值 = 0**（双方都走最优就是和局）。

### 1.3 为什么叫 MAX 和 MIN

叶子上的数字是从 **MAX 的角度**看的 utility：高 = 对 MAX 好、对 MIN 差；低 = 对 MAX 差、对 MIN 好。所以 **MAX 想最大化，MIN 想最小化**。

### 1.4 Conditional plan

MAX 的策略不能是一串固定动作，而必须是 **conditional plan**：对 MIN 的**每一种可能回应**都有对应的反应。输赢二元结果可以用 AND-OR search；有多种分数的用 minimax。

---

## 2. Minimax

### 2.1 定义

$$\text{MINIMAX}(s)=\begin{cases}\text{UTILITY}(s,\text{MAX}) & \text{terminal}\\ \max_{a}\ \text{MINIMAX}(\text{RESULT}(s,a)) & \text{TO-MOVE}(s)=\text{MAX}\\ \min_{a}\ \text{MINIMAX}(\text{RESULT}(s,a)) & \text{TO-MOVE}(s)=\text{MIN}\end{cases}$$

**Minimax value** = 从这个状态开始、**双方都走最优**时，MAX 能得到的 utility。

### 2.2 slide 的 two-ply 例子（slide 19、24–25）

叶子（从左到右）：`3 12 8 | 2 4 6 | 14 5 2`，B、C、D 是 MIN 节点，A 是 MAX 根。

| 节点 | 类型 | 子节点值 | 值 |
|---|---|---|---|
| B | MIN | 3, 12, 8 | **3** |
| C | MIN | 2, 4, 6 | **2** |
| D | MIN | 14, 5, 2 | **2** |
| A | MAX | 3, 2, 2 | **3** → 选 a₁（走到 B） |

（**Minimax decision**：MAX 的最佳着法是 a₁，因为它通向 minimax 值最高的状态。）

**slide 21 的问题：如果 MIN 不走最优会怎样？** 那 MAX 的结果**不会比 minimax 值更差**（只会更好或一样）：minimax 值是 MAX 面对**最坏对手**时的保底。

### 2.3 算法

```
MINIMAX-SEARCH(state): value, move ← MAX-VALUE(state); return move

MAX-VALUE(state):
    if terminal: return UTILITY, null
    v ← −∞
    for a in ACTIONS: v2 ← MIN-VALUE(RESULT(state,a)); if v2 > v: v, move ← v2, a
    return v, move

MIN-VALUE(state):   # 对称：v ← +∞，取更小
```

一个**递归的 DFS**：一直往下到叶子，再随着递归返回把值**backed up** 回来。

### 2.4 复杂度

- Complete（有限树）；**Time O(b^m)**；**Space** O(bm)（一次生成所有 actions）或 **O(m)**（一次生成一个 action）。
- 指数时间 → 复杂游戏不实用。例：平均一盘 chess，b ≈ 35、m ≈ 80 → 35⁸⁰ ≈ **10^123.5**（代码算出，slide 写 ≈ 10¹²³）。

### 2.5 Multiplayer games（slide 27–31）

单个值换成**向量** ⟨v_A, v_B, v_C⟩；每个节点的值 = **轮到走的那个人**在其后继里选**自己那一项最大**的向量。

slide 的树（三个玩家 A、B、C；最后一行的 "D" 只是 terminal 层的标签，不是第四个玩家）。我逐层算：

| 层 | 谁选 | 选择规则 | 结果 |
|---|---|---|---|
| C 层，4 个节点 | C（看 v_C） | (1,2,6)vs(4,2,3)→v_C 6 > 3；(6,1,2)vs(7,4,1)→2 > 1；(5,1,1)vs(0,5,2)→2 > 1；(7,7,1)vs(5,4,5)→5 > 1 | (1,2,6)、(6,1,2)、(0,5,2)、(5,4,5) |
| B 层，2 个节点 | B（看 v_B） | (1,2,6)vs(6,1,2)→2 > 1；(0,5,2)vs(5,4,5)→5 > 4 | (1,2,6)、(0,5,2) |
| A 根 | A（看 v_A） | (1,2,6)vs(0,5,2)→1 > 0 | **(1,2,6)** |

**slide 31 的问题**：在节点 X，C 在 ⟨1,2,6⟩ 和 ⟨4,2,3⟩ 之间选择 → C 只看**自己的** v_C：6 > 3，选 **⟨1,2,6⟩**。（补充，非 slide 内容：三人游戏里玩家可能形成**联盟**。）

---

## 3. Alpha-Beta Pruning

**目标**：返回**和 minimax 完全相同的着法**，但剪掉不可能影响决定的分支。可以剪整个子树，不只是叶子。

**General principle**：如果 Player 在**同一层**（m）或**更高层的某处**（m'）已经有更好的选择，那么 Player 永远不会走到 n → n 可以被剪。

### 3.1 α 和 β 的意思

- **α** = 到目前为止，**沿着这条路径 MAX 已经找到的最好（最大）选择**（MAX 的保底下界，只增不减）。
- **β** = 到目前为止，**沿着这条路径 MIN 已经找到的最好（最小）选择**（MIN 的上界，只降不升）。
- 一个节点的值 N 只在 **α ≤ N ≤ β** 时才有意义；当窗口关上（**α ≥ β**），剩下的后继就可以剪掉。

伪代码（slide 47）：

```
ALPHA-BETA-SEARCH(state): value, move ← MAX-VALUE(state, −∞, +∞)

MAX-VALUE(state, α, β):
    if terminal: return UTILITY
    v ← −∞
    for a in ACTIONS:
        v2 ← MIN-VALUE(RESULT(state,a), α, β)
        if v2 > v: v ← v2;  α ← max(α, v)
        if v ≥ β: return v          # ← 剪枝：MIN 不会让我到这里
    return v

MIN-VALUE(state, α, β):   # 对称
    v ← +∞
    for a in ACTIONS:
        v2 ← MAX-VALUE(RESULT(state,a), α, β)
        if v2 < v: v ← v2;  β ← min(β, v)
        if v ≤ α: return v          # ← 剪枝：MAX 已有更好的
    return v
```

**根节点开始时 α = −∞，β = +∞**，然后沿路径往下传。

### 3.2 slide 的例子逐步 trace（叶子 `3 12 8 | 2 4 6 | 14 5 2`，左到右）

代码验证：根值 = **3**，只评估了 **7 / 9** 个叶子（顺序 3, 12, 8, 2, 14, 5, 2）。

| 步 | 事件 | 窗口 [α, β] | 结果 |
|---|---|---|---|
| a | B 的第一个叶子 3 | B: [−∞, 3] | B 是 MIN，最多 3 |
| b | 第二个叶子 12 | B: [−∞, 3] | MIN 不会选 12，B 仍 ≤ 3 |
| c | 第三个叶子 8 | B: 值 = **3**；根 α = 3 | 根**至少 3**（MAX 已有一个 3 的选择） |
| d | C 的第一个叶子 2 | C: [3, 2]，α > β | C ≤ 2 < 3，MAX 永远不会选 C → **剪掉 C 的另外两个叶子（4、6）** |
| e | D 的第一个叶子 14 | D: [3, 14] | 14 > 3，不能剪，继续 |
| f | D 的第二个叶子 5 | D: [3, 5] | D 变成最多 5 |
| g | D 的第三个叶子 2 | D 值 = **2** | 根 = max(3, 2, 2) = **3** |

**Slide 46 的另一种看法**：把 C 的两个没评估的叶子记为 x、y：

MINIMAX(root) = max( min(3,12,8), min(2,x,y), min(14,5,2) ) = max(3, z, 2)，其中 z = min(2,x,y) ≤ 2 → **= 3**。所以决定**跟 x、y 无关**。

---

## 4. (4B) 让 alpha-beta 更有效

### 4.1 Move ordering

**剪枝的效果高度依赖检查后继的顺序**。

同一棵树，我用代码测了三种顺序（叶子评估数 / 9）：

| 顺序 | 评估的叶子 | 顺序 |
|---|---|---|
| 左到右（slide 4A） | **7 / 9** | B: 3,12,8；C: 2（剪）；D: 14,5,2 |
| **右到左（slide 4B-3 让你做的）** | **9 / 9（完全没剪）** | D: 2,5,14；C: 6,4,2；B: 8,12,3 |
| 把 D 改成 2, 5, 14（slide 4B-6） | **5 / 9** | B: 3,12,8；C: 2（剪 4、6）；D: 2（剪 5、14） |

**为什么**：从 MIN 的角度**最好的后继要先生成**（D 里的 2 是 MIN 最喜欢的），α ≥ β 才尽早发生。

**右到左这题的答案**：从右开始，D 里 2 是第一个 → D ≤ 2，但根的 α 还是 −∞，没法剪；然后 5、14 也要评估（D=2）；接着 C（6, 4, 2）→ C=2；最后 B（8, 12, 3）→ B=3。**没有任何剪枝**，根 = max(3, 2, 2) = 3。

**效果**：

| 顺序 | 要检查的节点数 |
|---|---|
| 最差（无效） | O(b^m)（slide 称 "depth-first move"，就是没有剪枝的意思） |
| **最好（best / killer move 先）** | **O(b^{m/2})** → effective branching factor = √b（chess：35 → 约 6，√35 = 5.9） |
| 随机 | O(b^{3m/4}) |

**动态 move ordering**：用上一步 / 之前探索里找到的好着法优先。做法：**iterative deepening**——先搜 1 ply 记录最佳路径，再搜深一 ply，用记录的路径决定顺序。

### 4.2 Transposition table

**Transposition**：不同的着法顺序到达**同一个局面**。例（chess）：White w₁、Black b₁、White w₂、Black b₂ 与 w₂、b₂、w₁、b₁ 到同一个局面 s。**Transposition table** = 已见过局面的 cache：第二次到达 s 时直接查表，不用再搜。chess 里能让相同时间内的搜索**深度翻倍**。代价：表可能指数大。

---

## 5. Imperfect real-time decisions

### 5.1 Type A vs Type B（Shannon 1950）

| | 做法 |
|---|---|
| **Type A** | **宽而浅**：考虑所有着法到某个深度，用 heuristic evaluation 估计那里的价值 |
| **Type B** | **窄而深**：忽略看起来很差的着法，沿有希望的路线尽量深入 |

### 5.2 Heuristic alpha-beta

把 alpha-beta 里的 **utility 换成 EVAL(s, p)**（估计局面的价值），把 **terminal test 换成 cutoff test**：

$$\text{H-MINIMAX}(s,d)=\begin{cases}\text{EVAL}(s,\text{MAX}) & \text{IS-CUTOFF}(s,d)\\ \max_a \text{H-MINIMAX}(\text{RESULT}(s,a),d+1) & \text{MAX}\\ \min_a \text{H-MINIMAX}(\text{RESULT}(s,a),d+1) & \text{MIN}\end{cases}$$

**好的 evaluation function 的要求**：① **快**（重点就是搜得更快）；② 对**非终局**状态，要和**真实获胜机会强相关**。多数 EVAL 是先算局面的若干 **features**。

### 5.3 设计方法

**方法 1：按类别取期望值。** 一个类别（feature 组合）里的状态，有些赢、有些和、有些输。slide 例（两兵对一兵的残局）：82% 赢（+1）、2% 输（0）、16% 和（½）：

EVAL = 0.82×1 + 0.02×0 + 0.16×½ = **0.90**（代码验证）。

不实用：类别太多、需要太多经验来估计概率。

**方法 2：Weighted linear function。** 每个 feature 单独贡献，再加起来：

$$\text{EVAL}(s)=w_1f_1(s)+w_2f_2(s)+\dots+w_nf_n(s)=\sum_i w_if_i(s)$$

chess 的入门书数值：pawn = 1，knight / bishop = 3，rook = 5，queen = 9；好的 pawn structure / king safety 各 ≈ ½ pawn。

我自己的小算例：White：1 queen、2 rooks、1 bishop、5 pawns → 9 + 2×5 + 3 + 5 = **27**；Black：1 queen、1 rook、1 bishop、1 knight、3 pawns → 9 + 5 + 3 + 3 + 3 = **23**；White 领先 4（约 4 个兵）。

**问题**：weighted linear 假设**每个 feature 的贡献彼此独立**。现实里不是：一对 bishops 可能比单个 bishop 的两倍还值钱；bishop 在残局比开局更有价值（move number 高、剩余棋子少）。所以现在的程序也用**非线性组合**。

**features 和 weights 从哪来**？来自几百年的人类下棋经验；没有这种经验的游戏，用 **machine learning** 估计（结果确认 bishop 大约值 3 个兵）。

### 5.4 Cutting off search

把 alpha-beta 里两处 `IS-TERMINAL → UTILITY` 换成 `IS-CUTOFF(state, depth) → EVAL`。**怎么决定截断点**：

- 固定深度 d（选的 d 要让着法在**规定时间内**选出来）；
- 或 **iterative deepening**：时间用完时，返回**最深的已完成搜索**选出的着法。

### 5.5 Cut-off 的局限

| 问题 | 现象 | 解决 |
|---|---|---|
| **Non-quiescent positions** | 在深度限制处，局面**正处于剧烈变化**（例：slide 29(b)，Black 领先一个 knight 和两个兵，但 White 下一步就吃掉 Black 的 queen，没有补偿）。EVAL 会误判 | **Quiescence search**：EVAL 只用在 quiescent（平静）局面；non-quiescent 的继续搜，直到平静 |
| **Horizon effect** | 面对不可避免的严重损失，程序用**拖延手段**把坏事推到"地平线"之外，看起来暂时避开了 | **Singular extensions**：找到"明显好于其他"的着法后，即使深度用完也允许考虑它 |

### 5.6 Forward pruning（属于 Type B）

直接剪掉**看起来差的着法**，省时间但**有出错风险**。

- **Beam search**（此处指每个 ply 只考虑 evaluation 最好的 n 个着法）：太冒险，没有保证最好的着法不被剪掉。（注意：这里的 "beam search" 与 Ch3 的 local beam search 是相似的思路，但用在游戏树的每一层。）
- **PROBCUT**（probabilistic cut，Buro 1995）：alpha-beta 的 forward-pruning 版本，用**过去经验的统计**降低把最佳着法剪掉的概率。在 Othello 中，赢常规版本 64% 的对局，即使常规版本有**两倍的时间**。也在 Shogi 里有效。

### 5.7 Search vs Lookup

开局和残局的选择少，**查表**（人类专家知识 + 数据库里的胜率统计）比搜索更合理；大约走了 10–15 步、选择多的中局才用搜索。

### 5.8 各改进的效果（slide 39，chess）

| 配置 | 深度 | 水平 |
|---|---|---|
| minimax + 合理的 cutoff + quiescence search | 约 5 ply | 一般水平（会被一般人类棋手 6–8 ply 打败） |
| + alpha-beta + 大 transposition table | 约 14 ply | 专家 |
| + 精调的 evaluation function + 残局数据库 | ≥ 30 ply | 特级大师 |

---

## ⚠️ Slide 里有问题或需要小心的地方

| Slide | Slide 写的 | 更准确的理解 |
|---|---|---|
| 4A-15 | 完整 tic-tac-toe 树 "fewer than 9! = 362,880 terminal nodes" | 没错但是很松的上界；实际是 **255,168**（我枚举过），distinct 棋盘只有 5,478 |
| 4A-32 | alpha-beta 把状态数 "reduced by almost half" | 和 4B-7 矛盾。最好情况是 O(b^m) → **O(b^{m/2})**，是**指数减半**（√），不是数量减半 |
| 4A-34 | "当 α > β 时剪枝" | 伪代码（4A-47）写的是 **v ≥ β**（MAX）和 **v ≤ α**（MIN），即 **α ≥ β 就可以剪**（相等也剪） |
| 4A-36 | "α and β ... is a number greater than negative infinity and less than infinity respectively" | 意思是：初始 **α = −∞、β = +∞**（见伪代码 4A-47 的调用） |
| 4A-41 | "The first leaf below C has the value 2, and hence **B** has a value of at most 2" | 打字错误，应该是 **C** ≤ 2 |
| 4A-28 图 | multiplayer 树最后一行标 "D" | 那是 **terminal 层**，不是第四个玩家（slide 28 文字说的是三人 A、B、C） |
| 4B-7 | "Depth-first move: O(b^m)" | 非标准说法；指的就是**没有获益于排序的最差情况**（等同于不剪枝） |
| 4B-20 | 权重 "normalized" 使总和在 0（输）到 +1（赢）之间 | slide 自己的例子（pawn 1、queen 9）并没有归一化；实际系统会再把这个值**压缩**到有限范围 |

---

## Cheat sheet

| 概念 | 要点 |
|---|---|
| 游戏 6 要素 | S₀、ACTIONS、RESULT、TO-MOVE、IS-TERMINAL、UTILITY |
| Ply | 一个玩家的一步 |
| Minimax | MAX 取 max、MIN 取 min；O(b^m) 时间，O(bm) 或 O(m) 空间 |
| Multiplayer | 值是向量，每人选自己那一项最大的 |
| α | MAX 路径上已找到的**最大**下界；β | MIN 路径上已找到的**最小**上界 |
| 剪枝条件 | MAX 节点 v ≥ β；MIN 节点 v ≤ α（即 α ≥ β） |
| Alpha-beta 复杂度 | 最好 O(b^{m/2})；随机 O(b^{3m/4})；最差 O(b^m) |
| Move ordering | 最好的着法先；iterative deepening 提供排序信息 |
| Transposition table | 缓存局面的价值，避免重复搜索 |
| Type A / Type B | 宽浅 + EVAL / 窄深 + 剪掉差着 |
| H-MINIMAX | 用 EVAL 和 IS-CUTOFF 取代 UTILITY 和 IS-TERMINAL |
| Weighted linear EVAL | Σ w_i f_i；假设 features 独立 |
| Quiescence search | 局面平静才用 EVAL |
| Horizon effect | 拖延手段把坏结果推出搜索范围；singular extensions 缓解 |
| PROBCUT | 用统计经验做概率式 forward pruning |

---

## Practice

### A. 选择题（5）

**A1.** 在 two-player zero-sum 游戏里，MIN 节点的值是？
(a) 后继的最大值  (b) 后继的最小值  (c) 后继的平均值  (d) 随机

**A2.** Alpha-beta pruning 与 minimax 相比？
(a) 返回不同的着法  (b) 返回相同的着法但检查更少的节点  (c) 只对深度 2 的树有效  (d) 需要 heuristic

**A3.** 最好的 move ordering 下，alpha-beta 检查的节点数是？
(a) O(b^m)  (b) O(b^{3m/4})  (c) O(b^{m/2})  (d) O(m)

**A4.** Horizon effect 指的是？
(a) 搜索深度太浅时评估不准  (b) 程序用拖延手段把不可避免的损失推到搜索深度之外  (c) transposition table 太大  (d) 对手不走最优

**A5.** 为什么需要 quiescence search？
(a) 为了让搜索更快  (b) 因为 EVAL 在**局势剧烈变化**的局面上不可靠  (c) 为了处理三人游戏  (d) 为了记住已见局面

### B. 简答题（3）

**B1.** 为什么 minimax 算法在 chess 中不实用？给出数字。

**B2.** 解释 α 和 β 的含义，并说明什么时候剪枝。

**B3.** 解释 Type A 和 Type B 策略，并各举一个用到它的技术。

### C. 计算 / 追踪（3）

**C1.** MAX 根、3 个 MIN 子节点，叶子（左到右）：`4 7 9 | 6 5 8 | 3 10 2`。(a) 用 minimax 写出每个 MIN 节点和根的值；(b) 用 alpha-beta（左到右）写出被剪掉的叶子，以及评估了几个叶子。

**C2.** 三层树：MAX 根 → 2 个 MIN → 每个 MIN 有 2 个 MAX 子节点 → 每个 MAX 有 2 个叶子。叶子（左到右）：`3 5 | 6 9 | 1 2 | 0 −1`。用 alpha-beta（左到右）求根值，并写出被剪掉的叶子。

**C3.** Chess evaluation：White 有 1 queen、2 rooks、1 bishop、5 pawns；Black 有 1 queen、1 rook、1 bishop、1 knight、3 pawns。用 pawn = 1、knight / bishop = 3、rook = 5、queen = 9 的 weighted linear function，算出 White 的 EVAL（White 总和 − Black 总和）。

### D. 思考题（2）

**D1.** 如果 MIN 不走最优着法，minimax 选出的着法还有意义吗？minimax 能保证什么？

**D2.** 为什么 weighted linear evaluation function 对"一对 bishops"这种情况处理不好？现代程序怎么补救？

---

### 答案

**A1.** (b)。

**A2.** (b)。alpha-beta 保证同样的决定，只是剪掉不影响决定的分支。

**A3.** (c)。O(b^{m/2})，effective branching factor 是 √b。

**A4.** (b)。

**A5.** (b)。在深度限制处，若局面还在剧烈变化（例：即将被吃掉 queen），EVAL 会误判；quiescence search 继续搜到局面平静。

**B1.** 时间 O(b^m)；chess 平均 b ≈ 35、m ≈ 80 → 35⁸⁰ ≈ 10^123.5 个状态，远远超过可计算范围。

**B2.** α = 沿这条路径 MAX 已找到的最好（最大）值（MAX 的保底）；β = 沿这条路径 MIN 已找到的最好（最小）值。当一个节点的窗口关上（**α ≥ β**），即某一方在别处已有更好的选择，不会走进这个节点，剩下的后继可以剪掉。

**B3.**
- Type A：宽而浅——考虑所有着法到某深度，用 EVAL 估计（例：heuristic alpha-beta + cutoff）。
- Type B：窄而深——只沿有希望的路线，忽略差着（例：forward pruning：beam search、PROBCUT）。

**C1.**（代码验证）
- (a) MIN 值：B = 4，C = 5，D = 2；根 = max(4, 5, 2) = **5**（走到 C）。
- (b) alpha-beta（左到右）：评估 B 的 4, 7, 9 → B = 4，根 α = 4；C：6 → 5 → 8 → C = 5，α = 5；D：3 → D ≤ 3 ≤ α = 5 → **剪掉 10 和 2**。评估的叶子顺序 4, 7, 9, 6, 5, 8, 3，共 **7 / 9** 个。

**C2.**（代码验证）
- 第一个 MIN：MAX(3,5) = 5；MAX(6, 9)：读到 6 后 6 ≥ β(=5) → **剪掉 9**；第一个 MIN = min(5, 6+) = 5；根 α = 5。
- 第二个 MIN：MAX(1, 2) = 2 → MIN ≤ 2 ≤ α = 5 → **剪掉 0 和 −1**。
- 根 = **5**。被剪掉的叶子：**9、0、−1**；评估了 **3, 5, 6, 1, 2** 共 5 / 8 个。
- 对照不剪枝的 minimax：第一个 MIN = min(max(3,5), max(6,9)) = min(5, 9) = 5；第二个 MIN = min(max(1,2), max(0,−1)) = min(2, 0) = 0；根 = max(5, 0) = **5**（与 alpha-beta 一致）。注意被剪掉的分支里 9 的真实值不影响结果，第二个 MIN 的真实值是 0，但只要知道它 ≤ 2 < α = 5 就足够了。

**C3.** White = 9 + 2×5 + 3 + 5×1 = **27**；Black = 9 + 5 + 3 + 3 + 3×1 = **23**；EVAL = 27 − 23 = **+4**（White 领先约 4 个兵）。

**D1.** 仍有意义：minimax 给出的是 **MAX 面对最坏对手时的保底**。如果 MIN 走得更差，MAX 的结果只会**更好或一样**，不会更差。（缺点：它不会去"利用"对手的错误。）

**D2.** weighted linear 假设各 feature **独立**，每个 bishop 各贡献 3；但一对 bishops 的组合价值可能高于 2×3。补救：用**非线性组合**的 features；或把 features 和 weights 用 machine learning 估计。

---

## 与其他章节的联系

- Ch2 的 DFS / IDS 直接用在这里：minimax 是 DFS（O(b^m) 时间），iterative deepening 用来做时间控制和 move ordering。
- Ch2 的 A* 用 heuristic h 引导搜索；本章的 EVAL 也是 heuristic，但估计的是**局面的胜率**，不是"距离 goal 多远"。
- Ch3 的 evaluation / fitness function 和这里的 EVAL 同类；forward pruning 里的 beam search 与 local beam search 是同一个思想。
- Ch1C 的 utility：本章的 UTILITY(s,p) 是终局收益；multiplayer 里每个玩家有自己的 utility。
