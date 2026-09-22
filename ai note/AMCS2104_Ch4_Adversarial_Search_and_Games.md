# AMCS2104 — Chapter 4: Adversarial Search and Games (4A + 4B)

> 本章要回答的问题：Chapter 2–3 里环境只有我们自己。如果对面有一个**专门跟你作对**的对手，你每走一步他都会挑对你最不利的回应——该怎么"搜索"？
>
> 📌 考试比重：May 2026 Q3 整题 25 分（minimax + alpha-beta **左到右 & 右到左**）；Jan 2026 Q3a 8 分（minimax values + best move + multiagent 类型）。**计算题，照步骤做一定满分。**

---

## Scene：跟室友下棋

你和室友下 tic-tac-toe（或象棋）。你想："我走这里，他会怎么回？他回了之后，我再怎么走？……"
你假设他**每次都会选对你最坏的那一步**——因为他真的想赢。
这种"我想最大化、他想最小化"的推理，就是 **minimax**。

---

## Part 1：Games 是一种搜索问题

### 1.1 Adversarial search

- 在 **competitive environment** 里，agents 的目标互相冲突（我赢 = 你输）→ 产生 **adversarial search problems**，也就是 **games**。
- 名词：**move = action**，**position = state**。

### 1.2 AI 常研究的 games 的 5 个特征（May 2026 Q3a，5 分）

| Characteristic | 说明 |
|---|---|
| **Turn-taking** | 玩家轮流走（MAX 先，再 MIN，重复直到结束） |
| **Two-player** | 两个玩家 |
| **Perfect information** | = **fully observable**，双方都看得到全部状态 |
| **Deterministic** | 没有随机成分（没有骰子） |
| **Zero-sum** | 对一方好 = 对另一方同样坏，双方 utility 总和固定 |

例：chess、Go、tic-tac-toe。

### 1.3 Game 的 6 个 elements（tutorial 8 考）

| Element | 意思 | Tic-tac-toe |
|---|---|---|
| **S₀** | initial state，游戏开局设定 | 9 格全空 |
| **ACTIONS(s)** | 在 s 的合法走法 | MAX 在空格放 X；MIN 在空格放 O |
| **RESULT(s, a)** | transition model | 放入符号后那格被占 |
| **TO-MOVE(s)** | 轮到谁 | MAX、MIN 轮流，MAX 先 |
| **IS-TERMINAL(s)** | terminal test，游戏结束为 true | 有人连成三个，或 9 格填满 |
| **UTILITY(s, p)** | utility / objective / **payoff function**：终局对玩家 p 的数值 | +1 MAX 赢、0 平手、−1 MAX 输（chess：1、0、½） |

📝 **Tic-tac-toe 的环境属性**：fully observable, multiagent (competitive), deterministic, sequential, static, discrete, known.

**为什么叫 MAX 和 MIN？** Leaf 上的数字是**从 MAX 的角度**看的 utility：MAX 想要**最大化**这个值；MIN（对手）想要**最小化**这个值（数值越低对 MIN 越好）。

### 1.4 Game tree

- **Game tree**：一种 search tree，表示双方轮流走所产生的所有 game states。
- **Complete game tree**：从初始局面一路展开所有走法直到 terminal states。
- Terminal states 的 nodes = **leaf / terminal nodes**。
- Tic-tac-toe 的完整 game tree 少于 **9! = 362,880** 个 terminal nodes。
- **Ply**：**一个玩家**走一步 = 1 ply。"Two-ply game" = MAX 走一次 + MIN 走一次。
- MAX 的 strategy 是一个 **conditional plan**（对 MIN 每种可能回应都有对策）。输赢只有两种结果 → 用 **AND-OR search**；有多种分数 → 用 **minimax**。

---

## Part 2：Minimax —— 假设对手永远走最好的一步

### 2.1 Minimax value

> The **minimax value** of a state is the utility (for MAX) of being in that state, **assuming both players play optimally** from there to the end of the game. For a terminal state, its minimax value is its utility.

```
MINIMAX(s) = UTILITY(s, MAX)                        if IS-TERMINAL(s)
           = max over a of MINIMAX(RESULT(s, a))    if TO-MOVE(s) = MAX
           = min over a of MINIMAX(RESULT(s, a))    if TO-MOVE(s) = MIN
```

**做法**：从 leaves 往上算——**MAX 层取最大、MIN 层取最小**（"backed up"）。
**Minimax decision**：MAX 在 root 选**通往最高 minimax value** 的那一步。

课件的 two-ply 例子：

```
                         A (MAX) = 3
          ┌──────────────┼──────────────┐
      B (MIN)=3      C (MIN)=2      D (MIN)=2
      /  |  \         /  |  \        /  |  \
     3  12   8       2   4   6     14   5   2
```
Best move = a1（往 B），value 3。

**如果 MIN 不走最优？**（tutorial）MAX 的结果**至少一样好，甚至更好**——minimax value 是 MAX 能保证的**下限**。但 minimax 策略不会刻意"利用"一个弱对手的错误。

### 2.2 Minimax algorithm 分析

- 递归计算，一路到 leaves，再随 recursion 回收时把值往上传 → 本质是 **complete depth-first exploration**。
- Complete（有限树）；对 optimal 对手是 optimal。
- **Time O(bᵐ)**；**Space O(bm)**（一次生成所有 actions）或 **O(m)**（一次生成一个）。
- 国际象棋：b ≈ 35、m ≈ 80 → 35⁸⁰ ≈ **10¹²³** states → 不实际。

### 2.3 多人游戏（Multiplayer）

- 每个 node 的值变成一个 **vector**，例如三人 <v_A, v_B, v_C>。
- Terminal：vector = 每个玩家各自的 utility。
- Non-terminal：backed-up value = 轮到走的那个玩家**对他自己分数最高**的 successor 的 vector。
- 例：轮到 C，选项 <1, 2, **6**> 和 <4, 2, **3**> → C 选 **<1, 2, 6>**（v_C = 6 较大）。

课件的完整三人 game tree（4A p27–31），层次 A → B → C → D(leaves)，每层由那个玩家选**对自己最高的分量**：

```
A (A 选 vA 最大)                          (1,2,6)
                          ┌──────────────────┴──────────────────┐
B (B 选 vB 最大)        (1,2,6)                               (0,5,2)
                   ┌───────┴───────┐                     ┌───────┴───────┐
C (C 选 vC 最大)  X (1,2,6)      (6,1,2)               (0,5,2)        (5,4,5)
                 /      \        /     \              /     \        /     \
D (leaves)   (1,2,6) (4,2,3) (6,1,2) (7,4,1)      (5,1,1) (0,5,2) (7,7,1) (5,4,5)
```
- C 层：X 选 (1,2,6)（6 > 3）；(6,1,2) vs (7,4,1) 选 vC=2；(5,1,1) vs (0,5,2) 选 vC=2；(7,7,1) vs (5,4,5) 选 vC=5。
- B 层：左边 (1,2,6) vs (6,1,2) → vB 2 > 1 → (1,2,6)；右边 (0,5,2) vs (5,4,5) → vB 5 > 4 → (0,5,2)。
- A 层：vA 1 > 0 → **(1,2,6)**，A 走左边。

---

## Part 3：Alpha-Beta Pruning —— 不用看完所有 leaves

### 3.1 概念

Minimax 要看的 states 数量随深度**指数**增长。**Alpha-beta pruning**：
- 返回**和 minimax 一样的 move / value**；
- 但**剪掉不可能影响最终决定的分支**；可以剪掉整棵 subtree，不只是 leaves。

**General principle**：如果玩家在某处（同一层的 m，或更上层的 m'）已经有**更好的选择**，他就**永远不会走到 n**，所以 n 可以被剪掉。

**两个参数**：
- **α** = 到目前为止，沿路径上 **MAX** 找到的**最好（最高）**值 → MAX 的**下限**。初始 −∞。
- **β** = 到目前为止，沿路径上 **MIN** 找到的**最好（最低）**值 → MIN 的**上限**。初始 +∞。
- 当某 node 出现 **α ≥ β** → 它剩下的 successors **被剪掉**。

**实用规则（做题用这个）**：
- 在 **MIN node**：得到一个 child 值 v，若 **v ≤ α**（上面的 MAX 已有更好的）→ 剪掉剩下的 children。否则 β = min(β, v)。
- 在 **MAX node**：得到 v，若 **v ≥ β**（上面的 MIN 已有更好的）→ 剪掉剩下的 children。否则 α = max(α, v)。
- α、β **由上往下传**；值由下往上回传。

### 3.2 讲师的标注法：每个 node 旁边写 [α, β]（⚠️ 考试照这个写）

课件（4A p35–45）在**每个 node 旁边写 [α, β]**，并且每走一步就更新。一开始 root = [−∞, +∞]，**往下传给 child**；child 算出值后，**MAX node 更新 α、MIN node 更新 β**；某 node 出现 **α > β**（lecturer 写 >，pseudocode 用 ≥）→ 剪掉剩下的 children。

课件 walkthrough（上面那棵树，左到右）：

```
Step  事件                                         标注（[α, β]）
(a)   B 的第 1 个 leaf = 3                          B [−∞, 3]      （MIN：β 变 3 = "B 最多 3"）
(b)   B 的第 2 个 leaf = 12，MIN 不会选               B [−∞, 3]
(c)   B 的第 3 个 leaf = 8 → B = 3                   B [−∞, 3] 值 3；root [3, +∞]  （MAX：α 变 3 = "root 至少 3"）
(d1)  进入 C，把 root 的 [3, +∞] 传下去               C [3, +∞]
(d2)  C 的第 1 个 leaf = 2                           C [3, 2]  → α=3 > β=2 → 剪掉 C 的另外 2 个 leaves
(e1)  进入 D                                         D [3, +∞]
(e2)  D 的第 1 个 leaf = 14                          D [3, 14]  （14 > 3，继续）
(f)   D 的第 2 个 leaf = 5                           D [3, 5]
(g)   D 的第 3 个 leaf = 2 → D = 2                   D [3, 2]；root 值 = 3
```

```
                          [3, +∞]  A  = 3
             ┌──────────────────┼──────────────────┐
     [−∞, 3] B = 3        [3, 2] C ≤ 2          [3, 2] D = 2
      /    |    \           /   ✂    ✂           /    |    \
     3    12     8         2   (4)  (6)        14     5     2
```
（✂ = pruned；括号里的 leaf 根本没被看。）

课件的 pseudocode（4A p47，AIMA Figure 5.7）：

```
function ALPHA-BETA-SEARCH(game, state) returns an action
    player ← game.TO-MOVE(state)
    value, move ← MAX-VALUE(game, state, −∞, +∞)
    return move

function MAX-VALUE(game, state, α, β) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← −∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MIN-VALUE(game, game.RESULT(state, a), α, β)
        if v2 > v then
            v, move ← v2, a
            α ← MAX(α, v)
        if v ≥ β then return v, move          ← prune: MIN 上面已有更好的
    return v, move

function MIN-VALUE(game, state, α, β) returns a (utility, move) pair
    if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
    v ← +∞
    for each a in game.ACTIONS(state) do
        v2, a2 ← MAX-VALUE(game, game.RESULT(state, a), α, β)
        if v2 < v then
            v, move ← v2, a
            β ← MIN(β, v)
        if v ≤ α then return v, move          ← prune: MAX 上面已有更好的
    return v, move
```

（没有 alpha-beta 的 MINIMAX-SEARCH（4A p23）完全一样，只是没有 α、β 两个参数，也没有两行 prune。）

**Right-to-left 的课件问题（4B p3–6）**：同一棵树右到左 → 先看 D（2, 5, 14）→ D = 2，root [2, +∞]；C（6, 4, 2）要看到最后一个 leaf 2 才 ≤ α → 没有东西可剪；B（8, 12, 3）→ 3。→ **没有任何 node 被剪**。
课件的解释：左到右在 C 能剪，是因为 **MIN 的最好 successor（2）先被看到**；D 剪不到是因为**最差的 successor（14）先被看到**。p6 把 D 的 leaves 排成 **2, 5, 14** → D 的第一个 leaf 就是 2 → D [3, 2] → 5 和 14 都被剪。

另一种看法：MINIMAX(root) = max(min(3,12,8), min(2,x,y), min(14,5,2)) = max(3, z, 2)（z ≤ 2）= **3** → 与 x、y 无关。

📝 **Affected / not affected（tutorial）**：Alpha-beta pruning **does not affect** the minimax value at the root or the move chosen; it **only affects** the number of nodes examined (search time), and how much is pruned depends on the order in which nodes are examined.

📝 **Advantage / disadvantage**：Advantage – examines far fewer nodes, so it can search roughly twice as deep in the same time, with exactly the same result. Disadvantage – effectiveness depends heavily on move ordering (bad ordering prunes almost nothing) and it still must search down to terminal states, which is impractical for deep games.

### 3.2 Move ordering 的影响（4B）

课件的同一棵树改成**右到左**：先看 D（2, 5, 14 → D = 2），再 C（6, 4, 2 → 最后才看到 2），最后 B → **几乎剪不到**。
在 D 里，如果 MIN 的**最好 successor 先被看到**（2 先出现），后面的就能剪。

| Ordering | Nodes examined |
|---|---|
| 最差（worst-first） | O(bᵐ)（跟 minimax 一样） |
| **Random** | **O(b^(3m/4))** |
| **Best move first（killer move）** | **O(b^(m/2))** → effective branching factor 从 b 变成 **√b**（chess 35 → 约 6）→ 同样时间可以搜**两倍深** |

**Dynamic move ordering**：用之前找到的最好走法（上一步 / 之前的探索）先试。实现：**iterative deepening**——先搜 1 ply 记录最佳路径，再搜深一层并用它来排序。

**Transpositions**：不同的走法顺序到达**同一个局面**（[w1, b1, w2, b2] 和 [w2, b2, w1, b1] 都到 s）。课件 4B p9 的国际象棋例子，三种顺序都到同一个局面：`1. e4 e5 2. Nf3 Nc6`、`1. Nf3 Nc6 2. e4 e5`、`1. e4 Nc6 2. Nf3 e5`。用 **transposition table**（以前见过的局面的 cache）存 backed-up value，下次直接查表 → chess 里可**让搜索深度加倍**。缺点：表本身可能很占内存。

---

## Part 4：搜不完怎么办？ —— Imperfect real-time decisions（4B）

就算有 alpha-beta，chess 还是太深。**Claude Shannon（1950）** 提出两种策略：

| Type A | Type B |
|---|---|
| **Wide but shallow**：考虑到某深度的**所有**走法 | **Deep but narrow**：忽略看起来差的走法 |
| 在那个深度用 **heuristic evaluation function** 估计 utility | 沿有希望的路线**尽量往深**走 |
| 例：cut-off search | 例：forward pruning |

### 4.1 Heuristic alpha-beta（cut-off search）

课件 4B p26–27：只要把 alpha-beta pseudocode 里**两行**提到 IS-TERMINAL 的地方（MAX-VALUE 和 MIN-VALUE 各一行）换掉：

```
if game.IS-TERMINAL(state) then return game.UTILITY(state, player), null
                               ▼
if game.IS-CUTOFF(state, depth) then return game.EVAL(state, player), null
```

把 alpha-beta 改两处：
1. **UTILITY → EVAL(s, p)**：heuristic evaluation function，估计局面的 utility。
2. **IS-TERMINAL → IS-CUTOFF(s, d)**：cutoff test，决定何时停止往下搜。

```
H-MINIMAX(s, d) = EVAL(s, MAX)                                if IS-CUTOFF(s, d)
                = max over a of H-MINIMAX(RESULT(s, a), d+1)  if TO-MOVE(s) = MAX
                = min over a of H-MINIMAX(RESULT(s, a), d+1)  if TO-MOVE(s) = MIN
```

**设定 cutoff 的两种方法（tutorial 9c）**：
- **Fixed depth limit**：depth > d 就 cutoff；d 选得让走法能在时间内完成。缺点：时间难以准确控制。
- **Iterative deepening**：一层一层加深，**时间到就返回最深完成的那次搜索的走法**。✅ **较好**：永远有答案、能充分利用时间，还可以帮 move ordering。

### 4.2 好的 evaluation function

- **Time**：计算不能太久（目的就是搜快一点）。
- **Performance**：对 nonterminal states，要与**真正的获胜机会强烈相关**。
- 通常计算局面的各种 **features**。

**Approach #1：Categories + expected value**。例：two-pawns vs one-pawn endgames，经验上 82% 赢（+1）、2% 输（0）、16% 和（½）：

```
EVAL = 0.82 × 1 + 0.02 × 0 + 0.16 × ½ = 0.82 + 0 + 0.08 = 0.90
```
❌ 不实际：需要太多 categories、太多经验来估计概率。

**Approach #2：Weighted linear function**

```
EVAL(s) = w₁f₁(s) + w₂f₂(s) + … + wₙfₙ(s)
```
fᵢ = feature（例：白方 bishop 数量），wᵢ = 权重。Material values：**pawn 1、knight / bishop 3、rook 5、queen 9**；好的 pawn structure、king safety ≈ ½ pawn。
- ❌ 假设各 feature 的贡献**互相独立**——不对（一对 bishops > 两倍单个 bishop；endgame 时 bishop 更值钱）→ 现代程序也用 **nonlinear** 组合。
- Features 与 weights 来自几百年的人类棋局经验；没有经验的游戏用 **machine learning** 估计（ML 也证实 bishop ≈ 3 pawns）。

### 4.3 Cut-off search 的三个问题（tutorial 9c(ii)）

| Issue | 描述 | 例子 | 解决 |
|---|---|---|---|
| **Approximation errors** | EVAL 只是估计，可能与真实获胜机会不符 | material 领先但王很危险 | 更好的 features / nonlinear / ML 调 weights；搜更深 |
| **Non-quiescent positions** | 局面**即将剧烈变化**，EVAL 值在下一步会大翻转 | Black 领先 knight + 2 pawns，但 White 下一步就能**吃掉 Black 的 queen** | **Quiescence search**：在 non-quiescent 位置**额外搜索**，直到局面平静（quiescent）才用 EVAL |
| **Horizon effect** | 对手有一个**严重且终究无法避免**的威胁，但程序用**拖延战术**把它推到搜索深度（horizon）之外，以为避开了 | 课件 4B p32：己方 **queen 被对方 bishops pin 住** → 程序把 **rook 挡在中间**拖延 → 但 rook 被吃掉后**还是会失去 queen**（白白多损失一个 rook） | **Singular extensions**：某个走法"明显比其他好"时记住它，到深度上限时若它合法就**继续延伸**考虑 |

课件 4B p21–22、p29 的图：(a) 与 (b) 棋盘几乎一样（都是 White to move，Black 多一个 knight 和两个 pawns），但在 (b) 里 **White 下一步可以吃掉 Black 的 queen** → (a) 是 **quiescent**（局面平静，EVAL 可信），(b) 是 **non-quiescent**（马上会大翻转，EVAL "Black 领先" 是错的）。

### 4.4 Forward pruning（Type B）

- 直接**剪掉看起来很差的走法**；省时间，但**冒着出错的风险**。
- **Beam search**：每层只考虑 EVAL 最好的 **n 个**走法 → 太冒险，可能把最好的走法剪掉。
- **PROBCUT**（probabilistic cut，Michael Buro 1995）：forward-pruning 版的 alpha-beta，用**以往经验的统计**降低剪掉最佳走法的概率。在 Othello 中胜过普通版本 **64%**（即使普通版有两倍时间）；在 Othello、Shogi 都有效。

📝 **Alpha-beta vs forward pruning**：Alpha-beta pruning only removes branches that are *provably* irrelevant, so the result is identical to minimax (safe). Forward pruning (Type B) removes moves that merely *appear* poor according to an evaluation, so it saves more time but may prune the best move and give a wrong decision.

### 4.5 Search vs Lookup

开局和残局的选择少，而且有大量书籍与统计 → 用 **table lookup**（人类经验 + 数据库胜率）；中局（约 10–15 步之后）选择多 → 用 **search**。

**Improved minimax 的等级**：
- minimax + cutoff test + quiescence search → 看 **5 ply** → 普通水平（会输给普通人类，他们约 6–8 ply）
- + alpha-beta + 大型 transposition table → **14 ply** → expert
- + 调得很好的 evaluation function + 大型残局数据库 → **30 ply** → grandmaster

### 4.6 Tutorial 9 Q2：六种技术与组合

| Label | Technique | 作用 |
|---|---|---|
| A | Minimax | 假设双方最优，递归算出最佳走法（完整但 O(bᵐ)） |
| B | Alpha-beta pruning | 剪掉不影响决策的分支，结果不变 |
| C | Cut-off search | 在某深度停止，不搜到终局 |
| D | Heuristic (evaluation) function | 在 cutoff 处估计局面的值 |
| E | Transposition table | 缓存已见过的局面，避免重复搜索 |
| F | Lookup table | 开局/残局直接查表 |

- **A + B**：结果与 minimax 相同，但 nodes 更少（最佳排序时 O(b^(m/2))）；仍要搜到终局，对 chess 不实际。
- **A + B + C + D**：可在时间内做决定（real-time）；但决定质量取决于 EVAL，会有 approximation error、non-quiescence、horizon effect。
- **+ E**：避免重复计算 transpositions，同样时间可搜更深（chess 约加倍）；代价是内存。
- **+ F**：开局与残局几乎零搜索时间、下得像专家，把时间留给中局 → 接近 grandmaster 等级的完整系统。

---

## Closing the loop

跟室友下棋：你用 **minimax** 假设他永远走最好的一步；用 **alpha-beta** 避开不必看的分支（先看好的走法，剪得更多）；棋太深就在某层 **cutoff**，用 **evaluation function** 估分，再用 **quiescence search / singular extensions** 修补缺点，开局残局**查表**。

到目前为止，每个 state 都是一个"黑盒子"（atomic）。但像 Sudoku、排课、地图着色这类问题，state 其实是**一组变量**，而且规则都写成**约束**——如果能利用这个结构，就能一次剪掉一大片搜索空间。这就是 Chapter 5：**CSP**。

---

## ⚠️ Where the slides mislead

| Slide | 课件写法 | 更准确的理解 |
|---|---|---|
| 4A Alpha-beta | "the gigantic number can be reduced by almost half" | 课本意思是把**指数**减半：O(bᵐ) → O(b^(m/2))（最佳排序），不是 nodes 数量减半。实际节省远多于一半。 |
| 4A Alpha-beta | "when α > β … pruned" | 标准做法是 **α ≥ β** 就剪（相等也剪）。本课 past year 的题目里没有遇到相等的情况，结果一样；遇到相等时写 ≥ 并说明。 |
| 4B Limitation | 右到左的例子只给出树，没有写出答案 | 右到左时该树**没有任何 node 被剪**（D=2、C 要看到最后一个 leaf 2 才 ≤ α=2，已无剩下 children）。 |

---

## Exam radar

| Paper | 题目 | 分数 |
|---|---|---|
| Jan 2026 Q3a | multiagent 类型 (2) · minimax values A,B,C,D,H,I,J,K (4) · best move (2) | 8 |
| May 2026 Q3 | 5 characteristics (5) · minimax values (4) · best move (1+1) · alpha-beta L→R & R→L (12) · conclusion (2) | **25** |

### 📝 May 2026 Q3（完整答案）

```
                                   A (MAX)
             ┌──────────────────────┼──────────────────────┐
           B (MIN)                C (MIN)                D (MIN)
        ┌────┴─────┐           ┌────┼────┐            ┌────┴─────┐
      E (MAX)    F (MAX)      G    H    I           J (MAX)    K (MAX)
      /   \      /  |  \      9    8   11          /  |  \      /   \
    L=20 M=12  N=27 O=11 P=13                    Q=9 R=2 S=7  T=14 U=8
```

**(i) Minimax values**
```
E = max(20, 12)       = 20
F = max(27, 11, 13)   = 27
B = min(20, 27)       = 20
C = min(9, 8, 11)     = 8
J = max(9, 2, 7)      = 9
K = max(14, 8)        = 14
D = min(9, 14)        = 9
A = max(20, 8, 9)     = 20
```

**(ii) Best move**：**A → B**。Justification: B has the highest minimax value (20) among A's successors (B = 20, C = 8, D = 9); assuming MIN plays optimally, moving to B guarantees MAX a utility of at least 20.

**(iii) Alpha-beta, left-to-right**

| Step | Node | α, β passed in | What happens |
|---|---|---|---|
| 1 | A → B → E | (−∞, +∞) | E is MAX: L = 20 → α_E = 20; M = 12 → no change. **E = 20** |
| 2 | B | (−∞, +∞) | B is MIN: v = 20 → β_B = 20 |
| 3 | F | (−∞, 20) | F is MAX: N = 27 → v = 27 ≥ β = 20 → **prune O, P**. (MIN at B already has 20, so it will never let MAX reach F.) F ≥ 27 |
| 4 | B → A | | B = min(20, ≥27) = **20**. At A: **α = 20** |
| 5 | C | (20, +∞) | C is MIN: G = 9 → v = 9 ≤ α = 20 → **prune H, I**. C ≤ 9 |
| 6 | D → J | (20, +∞) | J is MAX: Q = 9, R = 2, S = 7 → **J = 9** (never ≥ β = +∞) |
| 7 | D | (20, +∞) | D is MIN: v = 9 ≤ α = 20 → **prune K (with T, U)**. D ≤ 9 |
| 8 | A | | A = max(20, ≤9, ≤9) = **20**, best move B |

**Pruned (L→R)：O, P, H, I, K（含 T, U）** —— 共 7 个 nodes（6 个 leaves + K）。

**Alpha-beta, right-to-left**

| Step | Node | α, β passed in | What happens |
|---|---|---|---|
| 1 | A → D → K | (−∞, +∞) | K is MAX: U = 8, T = 14 → **K = 14** |
| 2 | D | | D is MIN: β_D = 14 |
| 3 | J | (−∞, 14) | J is MAX: S = 7, R = 2, Q = 9 → **J = 9** (none ≥ 14) |
| 4 | D → A | | D = min(14, 9) = **9**. At A: **α = 9** |
| 5 | C | (9, +∞) | C is MIN: I = 11 → β = 11; H = 8 → 8 ≤ α = 9 → **prune G**. C ≤ 8 |
| 6 | B → F | (9, +∞) | F is MAX: P = 13, O = 11, N = 27 → **F = 27** |
| 7 | B | | β_B = 27 |
| 8 | E | (9, 27) | E is MAX: M = 12, L = 20 → **E = 20** (20 < 27, no prune) |
| 9 | B → A | | B = min(27, 20) = **20**; A = max(9, ≤8, 20) = **20**, best move B |

**Pruned (R→L)：G only** —— 1 个 node。

**用讲师的 [α, β] 标注法画出最后的树**（考卷上画这两棵，每个 node 旁写最终的 [α, β]；✂ = pruned）：

```
LEFT-TO-RIGHT                                     [20, +∞] A = 20
                    ┌──────────────────────────────────┼──────────────────────────────┐
             [−∞, 20] B = 20                   [20, 9] C ≤ 9 ✂               [20, 9] D ≤ 9 ✂
            ┌──────┴───────┐                  /    ✂     ✂                ┌──────┴──────┐
   [20, +∞] E = 20   [27, 20] F ≥ 27 ✂       G=9  (H)   (I)      [20, +∞] J = 9      (K) ✂
     /      \          /    ✂     ✂                                 /   |   \          /  \
   L=20    M=12      N=27  (O)   (P)                              Q=9  R=2  S=7     (T)  (U)
```
- F：α = 27 > β = 20 → 剪 O、P。C：β = 9 < α = 20 → 剪 H、I。D：J 回传 9 → β = 9 < α = 20 → 剪 K（连同 T、U）。

```
RIGHT-TO-LEFT                                     [20, +∞] A = 20
                    ┌──────────────────────────────────┼──────────────────────────────┐
             [9, 20] B = 20                    [9, 8] C ≤ 8 ✂                [−∞, 9] D = 9
            ┌──────┴───────┐                  ✂     /     \                ┌──────┴──────┐
   [20, 27] E = 20   [27, +∞] F = 27        (G)   H=8   I=11      [9, 14] J = 9     [14, +∞] K = 14
     /      \          /    |    \                                   /   |   \          /  \
   L=20    M=12      N=27  O=11  P=13                              Q=9  R=2  S=7     T=14  U=8
```
- 顺序：K（U=8, T=14 → 14）→ D [−∞, 14] → J [−∞, 14] 看 S, R, Q → 9 → D = 9 → A [9, +∞] → C：I=11 → [9, 11]；H=8 → [9, 8]，α > β → 剪 G → B：F（P, O, N → 27）→ B [9, 27] → E [9, 27]：M=12, L=20 → 20 → B = 20 → A [20, +∞] = 20。

**(iv) Conclusion（2 分）**
> Both orders return the same minimax value (20) at the root and the same best move (B), so alpha-beta pruning does not change the result of minimax. However, the number of pruned nodes differs greatly: 7 nodes (O, P, H, I, K, T, U) left-to-right versus only 1 node (G) right-to-left. In left-to-right order MAX's best move (B = 20) is examined first, which sets a high α early and allows more cut-offs. Hence the effectiveness of alpha-beta pruning depends heavily on move ordering — examining the best successors first maximises pruning.

**(a) Five characteristics（5 分）**：turn-taking, two-player, perfect information (fully observable), deterministic, zero-sum —— 每个加一句解释（见 Part 1.2）。

### 📝 Jan 2026 Q3a

```
                                  A (MAX)
          ┌────────────────────────┼────────────────────────┐
        B (MIN)                  C (MIN)                  D (MIN)
       /   |   \              ┌────┴────┐              ┌────┴────┐
     E=8  F=7  G=10         H (MAX)   I (MAX)        J (MAX)   K (MAX)
                            /   \     /  |  \        /  |  \    /   \
                          L=19 M=11 N=8 O=10 P=12  Q=18 R=21 S=26 T=13 U=7
```

**(i)** **Competitive multiagent environment** – two players compete against each other in chess; the gain of one player (a win) is the loss of the other (zero-sum).

**(ii)**
```
B = min(8, 7, 10)    = 7
H = max(19, 11)      = 19
I = max(8, 10, 12)   = 12
C = min(19, 12)      = 12
J = max(18, 21, 26)  = 26
K = max(13, 7)       = 13
D = min(26, 13)      = 13
A = max(7, 12, 13)   = 13
```
**(iii)** Best move **A → D**：D has the highest minimax value (13) versus B (7) and C (12); assuming MIN plays optimally, D guarantees MAX at least 13.

---

## Cheat sheet

| 项目 | 要点 |
|---|---|
| Game characteristics | turn-taking, two-player, perfect information, deterministic, zero-sum |
| 6 elements | S₀, ACTIONS, RESULT, TO-MOVE, IS-TERMINAL, UTILITY |
| Ply | one move by one player |
| Minimax value | utility for MAX assuming both play optimally; MAX takes max, MIN takes min |
| Minimax complexity | time O(bᵐ), space O(bm) / O(m); chess 35⁸⁰ ≈ 10¹²³ |
| Multiplayer | vector of utilities; each player maximizes own component |
| α / β | best for MAX so far (lower bound) / best for MIN so far (upper bound) |
| Prune | MIN node: v ≤ α · MAX node: v ≥ β · (α ≥ β) |
| Alpha-beta | same result, fewer nodes; depends on ordering |
| Ordering | best-first O(b^(m/2)), random O(b^(3m/4)), worst O(bᵐ) |
| Transposition table | cache of seen positions |
| Type A vs B | wide-shallow + EVAL vs deep-narrow (forward pruning) |
| EVAL | fast + correlated with winning; weighted linear Σwᵢfᵢ |
| Cutoff | fixed depth or iterative deepening |
| Problems | approximation error, non-quiescence (→ quiescence search), horizon effect (→ singular extensions) |
| PROBCUT | Buro 1995, probabilistic forward pruning |
| Lookup | opening & endgame tables |

---

## Practice (answers included)

### A. MCQ

1. Alpha-beta pruning changes: (a) the root value (b) the best move (c) the number of nodes examined (d) the utility function
2. With perfect move ordering, alpha-beta examines about: (a) O(bᵐ) (b) O(b^(3m/4)) (c) O(b^(m/2)) (d) O(bm)
3. A position about to undergo a big material swing is: (a) quiescent (b) non-quiescent (c) terminal (d) transposed
4. Forward pruning is a Type ___ strategy: (a) A (b) B
5. In chess, a knight is worth about: (a) 1 (b) 3 (c) 5 (d) 9

**Answers**：1 (c) · 2 (c) · 3 (b) · 4 (b) · 5 (b)

### B. Calculation 1 — Tutorial 8/9 tree

```
                               A (MAX)
                 ┌───────────────┴───────────────┐
              B (MIN)                          C (MIN)
          ┌─────┴──────┐                  ┌─────┴──────┐
        D (MAX)      E (MAX)            F (MAX)      G (MAX)
       /    \       /   |   \          /    \       /    \
    H(MIN) I(MIN) J(MIN) K(MIN) L(MIN) M(MIN) N(MIN) O(MIN) P(MIN)
    6  8  3 11 9  17 16  7  3   9  4   5  3   2  4  10  1   8 11
    Q  R  S  T  U  V  W   X  Y   Z AA  AB AC  AD AE AF AG  AH AI
```
Find all minimax values, the best move, and nodes pruned left-to-right and right-to-left.

> **Minimax**：H 6, I 3, D 6; J 16, K 3, L 4, E 16; B 6; M 3, N 2, F 3; O 1, P 8, G 8; C 3; **A 6** → best move **B**.
>
> **L→R pruned**：T, U（I: S = 3 ≤ α = 6）· K, L 和它们的 leaves X, Y, Z, AA（E: J = 16 ≥ β = 6）· AC（M: AB = 5 ≤ α = 6）· AE（N: AD = 2 ≤ 6）· G 和它下面的全部 O, P, AF, AG, AH, AI（C: F returns 5 ≤ α = 6）。
>
> **R→L pruned**：只有 **AF**（O: AG = 1 ≤ α = 8）和 **X**（K: Y = 3 ≤ α = 4）。
>
> 结论同 May 2026：root value 相同（6），但左到右剪得多很多。

### C. Calculation 2 — alpha-beta on the Jan 2026 tree (extra practice)

> **L→R**：B = 7 (α = 7) → C: H = 19, I = 12 → C = 12 (α = 12) → D: J = 26, K = 13 → D = 13. **No pruning at all** (every MIN value found is above the current α).
> **R→L**：D first: K = 13 (U = 7, T = 13), J: S = 26 ≥ β = 13 → **prune R, Q** → D = 13, α = 13. C: I: P = 12, O = 10, N = 8 → I = 12 ≤ α = 13 → **prune H (L, M)**. B: G = 10 ≤ 13 → **prune F, E**. A = 13.
> 这次反过来：右到左剪得多，因为最佳走法 D 在最右边。

### D. Short answer

**D1.** Explain the horizon effect with an example and a solution. (4 marks)
> The horizon effect occurs when the program faces a serious, unavoidable loss but uses delaying moves to push the loss beyond its search depth (horizon), so it wrongly believes it has avoided it. E.g. a program sacrifices pawns to keep checking the opponent, delaying the capture of its trapped bishop past the depth limit — losing the pawns and still losing the bishop. Solution: **singular extensions** — a move that is clearly better than all others is remembered and allowed to be searched beyond the normal depth limit.

**D2.** Evaluate this position with material values: White has Q, 2R, B, 5 pawns; Black has Q, R, 2N, 6 pawns.
> White = 9 + 10 + 3 + 5 = 27; Black = 9 + 5 + 6 + 6 = 26 → EVAL = **+1** for White (slight advantage), assuming features are independent.
