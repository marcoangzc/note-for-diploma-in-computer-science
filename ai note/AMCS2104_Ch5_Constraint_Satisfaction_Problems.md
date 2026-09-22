# AMCS2104 — Chapter 5: Constraint Satisfaction Problems (5A + 5B + 5C)

> 本章要回答的问题：如果一个 state 不是黑盒子，而是**一组变量**，规则都写成**约束**，我们能不能利用这个结构，**不用搜索就先删掉一大堆不可能的值**？
>
> 📌 考试比重：Oct 2025 Q4a（20 分）与 May 2026 Q4（25 分）都是 **Sudoku + Alldiff + AC-3**。套路完全固定：① formulation（variables / domains / constraints）② 一格一格用 row、column、box 删值。

---

## Scene：填 Sudoku

你在巴士上填 Sudoku。你**不会**从第一格开始"试 1、试 2、试 3……"然后回头（那是 Ch2 的 search）。
你会看某一格："这一行已有 3、5、7，这一列已有 1、9，这个 box 已有 2……只剩 4！"——**直接推出答案**。
你其实是在做 **constraint propagation**。本章把这个直觉变成算法。

---

## Part 1：什么是 CSP

### 1.1 从 atomic 到 factored

| | Search problems（Ch2–4） | CSP（Ch5） |
|---|---|---|
| State | **Atomic**（黑盒子） | **Factored**：一组 variables，每个有值 |
| 解决条件 | goal test 通过 | **每个 variable 都有一个满足所有 constraints 的值** |
| Heuristic | domain-specific（如 straight-line distance、Manhattan distance） | **general-purpose**（MRV、degree、LCV…适用任何 CSP） |

CSP 的优势：找出**违反约束的 variable/value 组合**，就能**一次删掉一大块搜索空间**。

### 1.2 定义：X, D, C

- **X** = {X₁, …, Xₙ}：variables
- **D** = {D₁, …, Dₙ}：每个 variable 一个 domain（允许的值的集合；可以大小不同）
- **C** = {C₁, …, Cₘ}：constraints，规定允许的值的组合

每个 constraint = **⟨scope, rel⟩**：scope = 参与的 variables；rel = 它们可取值的关系。
例：X₁, X₂ ∈ {1, 2, 3}，"X₁ > X₂"：
- **Explicit list（enumeration）**：⟨(X₁, X₂), {(3,1), (3,2), (2,1)}⟩
- **Abstract relation**：⟨(X₁, X₂), X₁ > X₂⟩

### 1.3 Assignment 的种类（May 2026 Q4a，4 + 2 分）

| Type | Definition |
|---|---|
| **Consistent / Legal assignment** | An assignment that **does not violate any constraint**.（课件把两者当同义词） |
| **Complete assignment** | **Every** variable is assigned a value. |
| **Partial assignment** | Only **some** of the variables are assigned. |
| **Partial solution** | A partial assignment that is **consistent**. |
| **Solution** | An assignment that is **both consistent and complete**. |

📝 **(ii) Solution to a CSP**：A solution is a **complete and consistent** assignment — every variable is assigned a value from its domain, and the assignment satisfies all the constraints.

---

## Part 2：例子与 formulation

### 2.1 Map colouring（Australia）

```
        NT ──── Q
       /  \    /  \
     WA ── SA ──── NSW
             \     /
               V

     T  (Tasmania — no neighbours)
```

- X = {WA, NT, Q, NSW, V, SA, T}
- Dᵢ = {red, green, blue}
- C = {SA≠WA, SA≠NT, SA≠Q, SA≠NSW, SA≠V, WA≠NT, NT≠Q, Q≠NSW, NSW≠V}
- SA≠WA 是 ⟨(SA, WA), SA≠WA⟩ 的简写，可枚举为 {(red,green), (red,blue), (green,red), (green,blue), (blue,red), (blue,green)}。
- 一个 solution：{WA=red, NT=green, Q=red, NSW=green, V=red, SA=blue, T=red}。

**Constraint graph**：nodes = variables，edge 连接参与同一个 constraint 的两个 variables（上图）。

**为什么要 formulate 成 CSP？** 容易 formulate；CSP solver 快。例：一选 SA = blue，五个邻居都不能是 blue → 要考虑的组合从 3⁵ = **243** 降到 2⁵ = **32**（减少 **87%**）。一旦 partial assignment 违反约束，就能马上知道是哪些 variables 出问题、放弃这个 partial assignment 的所有延伸。

### 2.2 Job-shop scheduling（汽车组装）

- Variables：每个 task 的**开始时间**：AxleF, AxleB, WheelRF, …, NutsRF, …, CapRF, …, Inspect（15 个）。
- **Precedence constraint**：T₁ 必须在 T₂ 之前、T₁ 需时 d₁ → **T₁ + d₁ ≤ T₂**。例：AxleF + 10 ≤ WheelRF；WheelRF + 1 ≤ NutsRF；NutsRF + 2 ≤ CapRF。
- **Disjunctive constraint**（共用一个工具）：(AxleF + 10 ≤ AxleB) **or** (AxleB + 10 ≤ AxleF)。
- Inspection 最后、需 3 分钟：对每个 X，X + d_X ≤ Inspect。
- 30 分钟内完成 → Dᵢ = {1, 2, …, 27}。

### 2.3 Tutorial 10：用两种方式写 constraint

X₁, X₂, X₃ ∈ {0, 1}（1 = 获奖）：

| 要求 | Abstract relation | Enumeration |
|---|---|---|
| (i) 至少两人获奖 | ⟨(X₁,X₂,X₃), X₁+X₂+X₃ ≥ 2⟩ | {(1,1,0), (1,0,1), (0,1,1), (1,1,1)} |
| (ii) 最多一人获奖 | ⟨(X₁,X₂,X₃), X₁+X₂+X₃ ≤ 1⟩ | {(0,0,0), (1,0,0), (0,1,0), (0,0,1)} |
| (iii) 学生 1 与 3 恰好一人获奖 | ⟨(X₁,X₃), X₁ ≠ X₃⟩ | {(0,1), (1,0)} |
| (iv) 学生 2 与 3 同时获奖或同时不获奖 | ⟨(X₂,X₃), X₂ = X₃⟩ | {(0,0), (1,1)} |
| (v) 不能三人都获奖 | ⟨(X₁,X₂,X₃), X₁+X₂+X₃ ≤ 2⟩ | 除 (1,1,1) 以外的 7 个组合 |
| (vi) 若 2 获奖则 1 必获奖 | ⟨(X₁,X₂), X₂ ≤ X₁⟩ | (X₁,X₂) ∈ {(0,0), (1,0), (1,1)} |

### 2.4 Tutorial 10：4-Queens 当 CSP

- X = {Q₁, Q₂, Q₃, Q₄}，Qᵢ = 第 i 列 queen 所在的行
- Dᵢ = {1, 2, 3, 4}
- C：对每对 i < j：**Qᵢ ≠ Qⱼ**（不同行）且 **|Qᵢ − Qⱼ| ≠ j − i**（不在同一对角线）

---

## Part 3：Constraint 的种类

**Domains**：discrete finite（map colouring、scheduling、8-queens）；discrete infinite（整数、字串 → 要用 abstract constraint language，不能枚举）；continuous（精确时间的实验排程）。

| Constraint | 描述 | 例 |
|---|---|---|
| **Unary** | 限制**单一** variable | ⟨(SA), SA ≠ green⟩ |
| **Binary** | 关联**两个** variables；可画成 constraint graph | SA ≠ NSW |
| **Ternary / higher-order** | 三个或以上 | Between(X,Y,Z)：X<Y<Z 或 X>Y>Z |
| **Global** | **任意数量**的 variables（不一定是全部） | **Alldiff**：所有参与的 variables 值都不同 |

- **Binary CSP**：只有 unary 和 binary constraints。
- **Binarization**：任何有限 domain 的 constraint 都可以（加 auxiliary variables）转成 binary constraints；做法 **dual graph transformation**：原本每个 constraint 变成一个新 variable；共享 variables 的每对 constraints 之间加一个 binary constraint。
  例：C₁ = X+Y=Z，C₂ = X+1=Y，domain {1..5}：新 variable C₁ 的 domain = 满足 X+Y=Z 的所有 (x,y,z)；C₂ 的 domain = 满足 X+1=Y 的 (x,y)；关系 R = {((1,2,3),(1,2)), ((2,3,5),(2,3))}（X、Y 要一致）。
- **Alldiff 仍然比一堆 binary constraints 好**：写起来更容易、不易出错；可以设计专门的 inference 算法。
- **Absolute constraint**：违反就不是 solution。**Preference constraint**：违反仍是 solution，但不是 optimal。
  例：没有教授能同时教两门课（absolute）；R 教授偏好早上（preference）。→ R 早上 8 点教两门课：**不是 solution**；R 10am、N 2pm：**optimal**；R、N 都 8am：**sub-optimal**。
- 把 preference 写成 cost（R 下午 2 分、早上 1 分）→ **Constraint Optimization Problem (COP)**，用 optimization search 解。

---

## Part 4：Constraint Propagation —— 先推理，再搜索

非 CSP 的搜索只能做一件事（生成 successors）。CSP 可以：① **search**（选一个 variable 赋值）；② **inference / constraint propagation**：用约束**减少某 variable 的合法值**，这又会减少另一个 variable 的合法值……
可以当 **pre-processing**（在搜索前做，有时直接解完，不用搜索），也可以**和搜索交替进行**。

核心概念：**local consistency**。

### 4.1 Node consistency

一个 variable 的 domain 里所有值都满足它的 **unary constraints** → node-consistent。
例：SA 讨厌 green → D_SA = {red, blue}。之后 unary constraints 就可以删掉。

### 4.2 Arc consistency

> Xᵢ is **arc-consistent with respect to Xⱼ** if for **every** value in Dᵢ there is **some** value in Dⱼ (the **support**) that satisfies the binary constraint on the arc (Xᵢ, Xⱼ).

例：X, Y ∈ {0..10}，Y = X²：
- 让 X 对 Y arc-consistent：X 的值必须有 Y 支持 → **D_X = {0, 1, 2, 3}**（4² = 16 > 10）。
- 让 Y 对 X arc-consistent：**D_Y = {0, 1, 4, 9}**。

### 4.3 AC-3 algorithm

课件 pseudocode（5B p5，AIMA Figure 5.3）：

```
function AC-3(csp) returns false if an inconsistency is found and true otherwise
    queue ← a queue of arcs, initially all the arcs in csp
    while queue is not empty do
        (Xi, Xj) ← POP(queue)
        if REVISE(csp, Xi, Xj) then
            if size of Di = 0 then return false
            for each Xk in Xi.NEIGHBORS − {Xj} do
                add (Xk, Xi) to queue
    return true

function REVISE(csp, Xi, Xj) returns true iff we revise the domain of Xi
    revised ← false
    for each x in Di do
        if no value y in Dj allows (x, y) to satisfy the constraint between Xi and Xj then
            delete x from Di
            revised ← true
    return revised
```
- **REVISE** 只改 **Xi**（arc 左边那个）：Xi 的某个值 x 若在 Xj 里**找不到任何支持 y** → 删掉 x。
- 名字 "AC-3"：发明者 Mackworth（1977）论文中的**第 3 个版本**。
- 做完 AC-3：要么**每个 arc 都 arc-consistent**，要么**某 variable 的 domain 变空**（CSP 无解）。

- Dᵢ **没变** → 看下一个 arc。
- Dᵢ **变小** → 把所有 (Xₖ, Xᵢ) 加回 queue（Xᵢ 的改变可能让邻居也能再删）。
- Dᵢ **变空** → 整个 CSP 无解，**立刻返回 failure**。
- 结束时：新 CSP 与原 CSP **有相同的 solutions**，但 domains 更小 → 搜索更快。
- **Complexity：O(cd³)**（c 个 arcs，domain 大小 d：每个 arc 最多被加入 d 次，检查一次 O(d²)）。

**课件模拟（Y = X²）**：
```
Start : X {0..10}, Y {0..10}, queue {(X,Y), (Y,X)}
Step 1: pop (X,Y) → X {0,1,2,3}            X changed → add (Y,X) (already in queue)
Step 2: pop (Y,X) → Y {0,1,4,9}            Y changed → add (X,Y)
Step 3: pop (X,Y) → X unchanged            queue empty → done
Result: X {0,1,2,3}, Y {0,1,4,9}
```

### 4.4 Arc consistency 的限制 → Path consistency

Arc consistency 有时：找到 solution（每个 domain 剩 1）；有时发现无解（某 domain 变 0）；但**有时推不出足够的信息**。
例：WA、SA、NT 两两相邻，只有 {red, blue} 两色 → 每个 arc 都是 consistent（任何颜色对方都有另一色支持），但**显然无解**。

**Path consistency**（更强）：用**三个 variables** 推出隐含的约束。
{Xᵢ, Xⱼ} 对 Xₘ 是 path-consistent：对 {Xᵢ=a, Xⱼ=b} 的每个 consistent assignment，Xₘ 都有一个值同时满足 {Xᵢ, Xₘ} 与 {Xₘ, Xⱼ} 的约束。
例：{WA, SA} 的 consistent assignments：{WA=R, SA=B}、{WA=B, SA=R} → 两种情况 NT 都没有颜色 → 两个都删 → **无解**。

### 4.5 Global constraint 的 inference

**Alldiff 的不一致检测**：m 个 variables、总共只有 n 个不同的可能值，若 **m > n** → 不可能满足。
算法：删掉 singleton domain 的 variable，并把它的值从其他 variables 的 domain 中删除；重复；若出现空 domain 或 variables 比剩下的值多 → inconsistency。
例：{WA=red, NSW=red} 之后，SA、NT、Q 的 domain 都剩 {green, blue} → 3 个 variables、2 个颜色 → Alldiff 违反。

**Resource (Atmost) constraint**：Atmost(10, T₁, T₂, T₃, T₄)（四个 task 总人数 ≤ 10）。
- 若 domains 是 {3, 4, 5, 6}：最小和 = 3 × 4 = 12 > 10 → 不可能满足。
- 若 domains 是 {2, 3, 4, 5, 6}：其他三个最少共 6 → 每个最多 4 → **删掉 5 和 6**。

**Bounds propagation**：大整数 domain 用上下界表示。例：F1 容量 165、F2 容量 385，D₁ = [0, 165]、D₂ = [0, 385]，F1 + F2 = 420 → F1 ≥ 420 − 385 = 35、F2 ≥ 420 − 165 = 255 → **D₁ = [35, 165]，D₂ = [255, 385]**。

---

## Part 5：Sudoku —— 考试的主角

### 5.1 Formulation（9×9）

- **Variables**：81 个，以行字母 + 列数字命名：A1 … A9（第一行）… I1 … I9（最后一行）。
- **Domains**：空格 {1, …, 9}；已填的格子 = 只含那个值的 singleton domain。
- **Constraints**：**27 个 Alldiff**：9 rows + 9 columns + 9 boxes（3×3）。
  Alldiff(A1, A2, …, A9) · Alldiff(A1, B1, …, I1) · Alldiff(A1, A2, A3, B1, B2, B3, C1, C2, C3) · …
- 行、列、box 都叫 **unit**。
- Alldiff 展开成 binary constraints（例 A1 ≠ A2）后，就能直接用 **AC-3**。

### 5.2 AC-3 答题模板（每一格这样写）

> **Variable X** — initial domain {1..n}.
> - Row constraint (Alldiff of row …): remove {…} → {…}
> - Column constraint (Alldiff of column …): remove {…} → {…}
> - Box constraint (Alldiff of box …): remove {…} → {…}
> - (If needed) After Y has been fixed to v, the arc (X, Y) removes v → {…}
> - Therefore X = v.

### 5.3 Tutorial 11（课件同一题）：9×9 的 I4、A4、E4

```
    1 2 3 4 5 6 7 8 9
A   . . 3 . 2 . 6 . .
B   9 . . 3 . 5 . . 1
C   . . 1 8 . 6 4 . .
D   . . 8 1 . 2 9 . .
E   7 . . . . . . . 8
F   . . 6 7 . 8 2 . .
G   . . 2 6 . 9 5 . .
H   8 . . 2 . 3 . . 9
I   . . 5 . 1 . 3 . .
```
- **I4**：column 4 has {3, 8, 1, 7, 6, 2} → {4, 5, 9}; row I has {5, 1, 3} → {4, 9}; box (G–I, 4–6) has {6, 9, 2, 3, 1} → remove 9 → **I4 = 4**.
- **A4**：column 4 → {4, 5, 9}; row A has {3, 2, 6} → no change; box (A–C, 4–6) has {2, 3, 5, 8, 6} → {4, 9}; column 4 now also contains I4 = 4 → **A4 = 9**.
- **E4**：column 4 → {4, 5, 9}; minus I4 = 4 and A4 = 9 → {5}; row E {7, 8} and box (D–F, 4–6) {1, 2, 7, 8} agree → **E4 = 5**.

（顺序很重要：A4 要用到 I4，E4 要用到 I4 和 A4 → 这就是 **propagation**。）

**课件自己的例子（5B p28–29，同一个 puzzle，column 6）**——考试可能直接拿这三格来问：
- **E6**：box (D–F, 4–6) 有 {1, 2, 7, 8} → 删掉后 D_E6 = {3, 4, 5, 6, 9}；column 6 有 {2, 3, 5, 6, 8, 9} → 删掉 → **E6 = 4**。
- **I6**：column 6（现在包括 E6 = 4）有 {2, 3, 4, 5, 6, 8, 9} → 删掉；box (G–I, 4–6) 有 {1, 2, 3, 6, 9} → 删掉 → **I6 = 7**。
- **A6**：column 6 现在已有 **8 个已知值** {2, 3, 4, 5, 6, 7, 8, 9}（含刚推出的 E6、I6）→ 只剩 **A6 = 1**。

课件 p24：(a) 是题目，(b) 是完整解：

```
    1 2 3 4 5 6 7 8 9
A   4 8 3 9 2 1 6 5 7
B   9 6 7 3 4 5 8 2 1
C   2 5 1 8 7 6 4 9 3
D   5 4 8 1 3 2 9 7 6
E   7 2 9 5 6 4 1 3 8
F   1 3 6 7 9 8 2 4 5
G   3 7 2 6 8 9 5 1 4
H   8 1 4 2 5 3 7 6 9
I   6 9 5 4 1 7 3 8 2
```
（对照：I4 = 4、A4 = 9、E4 = 5、E6 = 4、I6 = 7、A6 = 1 ✓）

---

## Part 6：Backtracking Search —— 推不完就搜

### 6.1 为什么不直接用 DFS / DLS？

State = partial assignment，action = 多赋值一个 variable。n 个 variables、domain 大小 d：第一层 branching = nd，第二层 (n−1)d…→ 共 **n! · dⁿ** 个 leaves，但真正的 assignments 只有 dⁿ 个！
关键：**CSP 是 commutative**（交换律）——赋值顺序不影响结果（{WA=R, NT=G} 与 {NT=G, WA=R} 一样）→ 每个 node **只考虑一个 variable** → leaves 降到 **dⁿ**。

### 6.2 Backtracking search

DFS 的变体：**一次为一个 variable 选值**，当某 variable **没有合法值**时就 backtrack。
- 重复选一个未赋值的 variable → 依次试它 domain 中的值，递归延伸 → 成功就返回；失败就恢复原状、试下一个值 → 都不行返回 failure。
- 只保留**一份** state 并修改它；不依赖 domain-specific heuristic。
- 实作上 = **DFS + pruning**。

**Backtracking vs local search（tutorial 12）**：backtracking works on **partial assignments** (extends one variable at a time, systematic); local search works on **complete assignments** (changes the value of one variable at a time to reduce conflicts).

**Backtracking vs DFS**：backtracking generates one value/successor at a time, keeps a single state that is modified and restored (less memory), checks constraints as soon as a variable is assigned and prunes inconsistent partial assignments immediately, and exploits commutativity (one variable per level).

**Domain-specific vs domain-independent heuristic**：domain-specific heuristics use knowledge of a particular problem (straight-line distance for route finding); domain-independent heuristics (MRV, degree, LCV) use only the structure of the CSP and work for any CSP.

课件 pseudocode（5B p39 / p46，AIMA Figure 5.5）——红框标出 4 个可以改进的地方：

```
function BACKTRACKING-SEARCH(csp) returns a solution or failure
    return BACKTRACK(csp, { })

function BACKTRACK(csp, assignment) returns a solution or failure
    if assignment is complete then return assignment
    var ← SELECT-UNASSIGNED-VARIABLE(csp, assignment)                 ← ① variable ordering (MRV, degree)
    for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do    ← ② value ordering (LCV)
        if value is consistent with assignment then
            add {var = value} to assignment
            inferences ← INFERENCE(csp, var, assignment)             ← ③ inference (forward checking, MAC)
            if inferences ≠ failure then
                add inferences to csp
                result ← BACKTRACK(csp, assignment)
                if result ≠ failure then return result
                remove inferences from csp
            remove {var = value} from assignment                      ← ④ 失败就撤销、试下一个值
    return failure
```

**课件图（5B p36，Figure 5.6）：map-colouring 的 search tree**。root = 空地图 → 第一层只对 **WA** 选 red / green / blue（3 个分支，**每层只一个 variable**，因为 commutative）→ WA=red 下面第二层只对 **NT** 选 green / blue（red 不 consistent）→ 第三层只对 **Q** 选……

**课件图（5B p40）：Backtracking = DFS + pruning**。一棵树上 DFS 一路往下；遇到违反约束的 node 就标 "**Pruned**"（它的整棵 subtree 不再生成），然后沿红色虚线 "**backtrack**" 回到上一层试下一个值，直到走到 "**Complete**" 的 leaf（= solution）。

**课件例 #1**：X = Y − 1，Y = Z，Dᵢ = {1, 2, 3}
```
X=1 → Y=1 ✗ (1 ≠ 0) → Y=2 ✓ → Z=1 ✗, Z=2 ✓   → solution {X=1, Y=2, Z=2}
```

**影响 backtracking 效率的 4 件事**：
1. **Which variable next?** → SELECT-UNASSIGNED-VARIABLE（variable ordering）
2. **What order to try values?** → ORDER-DOMAIN-VALUES（value ordering）
3. **What inference at each step?** → INFERENCE（forward checking、MAC）
4. **Can we backtrack more than one step?** → BACKTRACK（backjumping）＋ 如何避免重复同一个冲突（constraint learning）

### 6.3 Variable ordering

- Static / random ordering：不 optimal。课件图（5B p49）：{WA=Red, NT=Green} 之后，
  - 若下一个选 **Q**：Q 可以是 Red 或 Blue——选 Blue 会让 SA 没颜色，但 static ordering 不会察觉；
  - 若下一个选 **SA**：SA 只剩 **Blue** 一个选择，马上就能确定 → 这正是 MRV 会选的 variable。
- **MRV (minimum-remaining-values)**：选**合法值最少**的 variable。也叫 **"most constrained variable"** 或 **"fail-first"**：最容易失败的先处理，失败能**马上被发现**。常比 random/static 好 **1000 倍以上**。
  - 第一步没用：一开始所有 variables 合法值一样多。
- **Degree heuristic**：选**与最多未赋值 variables 有约束**的 variable → 降低未来的 branching factor。
  - Australia：**SA degree 5**（最高）；其他 2 或 3；**T = 0**。
- **MRV = 主要指引；Degree = tie-breaker**（例如第一步）。

### 6.4 Value ordering：LCV

**Least-constraining-value**：优先选**让邻居剩下最多选择**的值。
例：{WA=R, NT=G}，给 Q 选值：
- Q = Blue → SA = {}（SA 没有值了！）、NSW = {R, G} → 坏选择
- Q = Red → SA = {Blue}、NSW = {G, B}… 仍有选择 → **选 Red**

📝 **为什么 variable 要 fail-first、value 要 fail-last？**
> Every variable must be assigned eventually, so choosing the variable most likely to fail first detects dead ends early and means fewer successful assignments to backtrack over. For values we only need ONE solution, so we try the value most likely to succeed first (least constraining) — starting with a failing value would defeat the purpose.

### 6.5 Tutorial 10/12：排课 CSP（完整）

Courses：1（8–10am）、2（9–11am）、3（10:30–12:30）、4（11am–1pm）、5（11am–1pm）。
Lecturers（Table 2）：Alex {1,3,4}、Billy {2,3,4,5}、Carolyn {1,2,4}。

**Formulation**
- Variables：C1, C2, C3, C4, C5（每门课由谁教）
- Domains（已做 unary constraint）：C1 {A, C} · C2 {B, C} · C3 {A, B} · C4 {A, B, C} · C5 {B}
- Constraints（时间重叠的课不能同一位讲师）：**C1≠C2, C2≠C3, C3≠C4, C3≠C5, C4≠C5**（2 与 4 在 11am 接触但不重叠）

```
Constraint graph:   C1 ── C2 ── C3 ── C4
                                 \    /
                                  C5
```

**AC-3**：C5 = {B} → (C3, C5) 删 B → C3 = {A} → (C4, C3) 删 A、(C4, C5) 删 B → C4 = {C}；C2 对 C3 = {A}：B、C 都有支持 → 不变；C1 不变。
→ **C1 {A, C}, C2 {B, C}, C3 {A}, C4 {C}, C5 {B}**
**One solution**：C1 = Alex, C2 = Billy, C3 = Alex, C4 = Carolyn, C5 = Billy。

**Plain backtracking**（order C1…C5，values A, B, C）：C1=A → C2=B → C3=A → C4=B → C5: B 与 C4 冲突 ✗ → backtrack C4=C → C5=B ✓（1 次 backtrack）。
**+ MRV**（配合 forward checking 更新合法值）：C5 (1 value) = B → C3 剩 {A} = A → C4 剩 {C} = C → C1、C2 平手（2 个值）→ C1 = A → C2 = B。**0 backtrack**。
**+ Degree**：degrees C3 = 3 最高 → C3 = A 先；之后平手按顺序 C1=A、C2=B、C4=B、C5 ✗ → backtrack C4=C → C5=B（1 次）。Degree 只减少 branching，不保证不 backtrack。
**+ LCV**：为 C4 选值时，C4 = B 会删掉 C5 唯一的值，C4 = C 不删任何值 → 选 **C** → 避免那次 backtrack。

**Table 3 版本**（Alex {3,5}、Billy {2,3,4,5}、Carolyn {1,2,4}）：C1 {C}、C2 {B,C}、C3 {A,B}、C4 {B,C}、C5 {A,B}。
AC-3：C1 = C → C2 = {B} → C3 = {A} → C5 = {B} → C4 = {C} → 唯一解 **C1=C, C2=B, C3=A, C4=C, C5=B**（AC-3 直接解完，不用搜索）。

### 6.6 Tutorial 11：arc-consistent 但无解

3 门课时间两两重叠（8–10、9–11、9:30–11:30），只有 Alex、Billy 两位（都能教全部）。
- Variables C1, C2, C3；domains {A, B}；constraints C1≠C2, C1≠C3, C2≠C3。
- AC-3 之后：**domains 不变**——每个值在对方都有支持（A 有 B，B 有 A）→ graph **是 arc-consistent**。
- 但 3 个 variables 只有 2 个值 → **无解**。
- 结论：**arc consistency 不保证有解**；它推不出这种情况。
- 用 **Alldiff(C1, C2, C3)**：m = 3 > n = 2 → **立刻检测出 inconsistency**。

---

## Part 7：Interleaving search and inference（5C）

### 7.1 Forward checking

每当 variable X 被赋值：对每个与 X 有约束的**未赋值** variable Y，把 Y 的 domain 中与 X 不一致的值删掉（= 只让 X 的邻居对 X arc-consistent）。

```
                 WA   NT   Q    NSW  V    SA   T
Initial          RGB  RGB  RGB  RGB  RGB  RGB  RGB
WA = R           R    GB   RGB  RGB  RGB  GB   RGB
Q  = G           R    B    G    RB   RGB  B    RGB
V  = B           R    B    G    R    B    {}   RGB   ← SA 空了 → 立刻 backtrack
```

- **Backtracking vs forward checking**：plain backtracking 只检查**已赋值**的 variables 之间有无冲突；forward checking 还**往前**删掉**未赋值邻居**的值，能更早发现死路。
- **FC + MRV**：WA=R 之后 NT、SA 的 domain 缩得最多 → 下一步先处理它们。
- ❌ **Limitation**：只让**当前 variable 的邻居** arc-consistent，**不再往外传**。例：WA=R、Q=G 后 NT、SA 都被迫 = {B}，但 NT 与 SA 相邻不能同色——forward checking **没发现**。

### 7.2 MAC（Maintaining Arc Consistency）

Xᵢ 被赋值后，用 AC-3，但 queue 一开始只放 **(Xⱼ, Xᵢ)**（Xⱼ = Xᵢ 的未赋值邻居），之后**递归传播**（有 domain 改变就继续把相关 arcs 加回去）。→ 能发现 forward checking 漏掉的 NT = SA = {B} 冲突。

**课件图（5C p6 / p8 / p11）**：constraint graph 中间一条虚线标 "Current variable"（黑点 = 刚赋值的 variable；灰点 = 已赋值；白点 = 未赋值）。图上用椭圆圈出三种检查范围：

```
   已赋值 (grey)        │ current (black)        未赋值 (white)
                        │
   ●───●                │                 ○───○
    \   \  backtracking │  forward        │     \
     ●───●═════════════ ◉ ═══checking═══ ○ ─── ○ ─── ○
          (检查左边的边) │  (只检查 current   │  look ahead (MAC:
                        │   与白点的边)      │   白点之间的边也检查)
```

**Scope 比较（tutorial 12 图）**：
- **Backtracking**：只检查当前 variable 与**已赋值** variables 之间的约束。
- **Forward checking**：+ 当前 variable 与它**直接相连的未赋值邻居**。
- **FC + MAC**：+ 从那些邻居**一直往外传播**到整个未赋值部分的 graph。

### 7.3 Chronological backtracking vs Backjumping

**Chronological backtracking**：失败就回到**最近的**决定点。
例：顺序 {Q, NSW, V, T, SA, WA, NT}，partial assignment {Q=R, NSW=G, V=B, T=R}；SA 没有合法值 → 回到 T、换颜色——**没用！** T 跟 SA 根本不相邻。

**Backjumping**：回到 **conflict set** 中**最近**的那个 variable。
- **Conflict set of X**：之前已赋值、与 X 的某些值冲突的 assignments。
- 上例：SA 的 conflict set = {Q=R, NSW=G, V=B} → **跳过 T，直接改 V**。
- 实作：检查合法值时累积 conflict set；没有合法值就返回 conflict set 中最近的元素 + failure。
- ⚠️ 在 forward-checking 搜索中，**简单 backjumping 是多余的**：forward checking 在 domain 变空时就阻止搜索走到那里了。

**Conflict-directed backjumping**：更深入追查"真正原因"。
例：{WA=R, NSW=R} 已定，接着 T=R，然后 NT、Q、V、SA……无论怎样 SA 都失败。简单 backjumping 跳去 V 也没用——真正原因是 {WA=R, NSW=R}。
做法：跳到 Xⱼ 时，Xⱼ **吸收**失败 variable 的 conflict set：conf(Xⱼ) ← conf(Xⱼ) ∪ conf(Xᵢ) − {Xⱼ}。
课件链：SA 失败，conflict set {WA, NT, Q} → 跳到 Q，Q 自己的 conflict set 是 {NT, NSW}，吸收后 → {WA, NT, NSW} → 仍失败 → 跳到最近的 NT，NT 自己的 {WA} 吸收后 → {WA, NSW} → 跳到 **NSW**，找到真正问题 **NSW = Red**。

### 7.4 Tutorial 12 Q2：Backjumping 完整答案

Fixed order WA, V, NT, Q, NSW, T, SA；partial assignment {WA=R, V=B, NT=B, Q=R, NSW=G, T=R}；颜色试的顺序 R, G, B。

- **(i) Chronological backtracking** 回到 **T**（最近的决定点）。
- **(ii) 同意"不太有效"**：T 与 SA 不相邻，改 T 的颜色对 SA 没有任何帮助，只会白白试完 T 的所有颜色（Green、Blue）后再退回 NSW。
- **(iii) Backjumping** 不回到最近的 variable，而回到 **SA 的 conflict set 中最近的那个 variable**，跳过无关的决定。
- **(iv) Conflict sets**（先赋值、且与该 variable 相邻的 variables）：

| Variable | Neighbours assigned earlier | Conflict set |
|---|---|---|
| WA | — | { } |
| V | (SA, NSW not yet) | { } |
| NT | WA | {WA} |
| Q | NT | {NT} |
| NSW | Q, V | {Q, V} |
| T | — | { } |
| SA | WA, V, NT, Q, NSW | {WA, V, NT, Q, NSW} |

- **(v)** SA：Red 与 WA、Q 冲突，Green 与 NSW 冲突，Blue 与 V、NT 冲突 → 没有值。conflict set 中最近的是 **NSW** → **跳过 T，直接回到 NSW** 换值。
- **(vi)** 比简单 backtracking 有效：省掉试 T 的所有颜色（T 无关）。但若 NSW 也没有别的可行颜色，需要 **conflict-directed backjumping**（NSW 吸收 SA 的 conflict set → {WA, V, NT, Q}）继续往前跳到 Q。

### 7.5 Constraint learning

到达矛盾时，conflict set 的某个子集是罪魁。**Constraint learning**：找出造成问题的**最小** variables 集合 + 它们的值 = **no-good**，并**记录**下来，以后不再重犯。
例：{WA=red, NT=green, Q=blue} 是 no-good（SA 无值）。如果这棵树只是更大搜索树的一部分（例如先赋值 V、T），对 V、T 的每一种组合都会再遇到它 → 值得记录。

---

## Part 8：Local search for CSPs

- Backtracking 用 **partial (incremental) formulation**；local search 用 **complete-state formulation**：每个 state 给**所有** variables 赋值，每次改**一个** variable 的值。
- 初始猜测会违反几个 constraints；目标是消除违反。
- **Min-conflicts heuristic**：为选中的 variable 挑**造成最少冲突**的值。CONFLICTS 函数 = 违反约束的数量。

课件 pseudocode（5C p23，AIMA Figure 5.9）：

```
function MIN-CONFLICTS(csp, max_steps) returns a solution or failure
    inputs: csp, a constraint satisfaction problem
            max_steps, the number of steps allowed before giving up

    current ← an initial complete assignment for csp
    for i = 1 to max_steps do
        if current is a solution for csp then return current
        var ← a randomly chosen conflicted variable from csp.VARIABLES
        value ← the value v for var that minimizes CONFLICTS(csp, var, v, current)
        set var = value in current
    return failure
```

**课件图（5C p24）：8-queens 两步解完**（每一格的数字 = 把该列 queen 移到那里后的冲突数）：
1. 选**第 8 列**（有冲突）的 queen，看它那一列每格的冲突数：2, 2, **1**, 2, 3, **1**, 2, (现在位置) → 有两格是 1，随机选其中一格移过去。
2. 选**第 6 列**的 queen：各格冲突数 3, 3, (现在), 2, 3, 2, 3, **0** → 移到冲突数 **0** 的最底格 → **solution**。

课件图（5C p21）：**incremental formulation** = 从空棋盘开始一个一个放（backtracking 用）；**complete-state formulation** = 8 个 queen 已全部在棋盘上（local search 用）。
- 非常有效：**million-queens problem 平均约 50 步**解完。
- 问题：landscape 常有一连串 **plateaus**（数百万个"只差一个冲突"的 assignments）→ 用 **plateau search（sideways moves）** 或 **simulated annealing** 逃离。

---

## Closing the loop

回到巴士上的 Sudoku：你写下每格可能的数字（**domain**），看行、列、box（**Alldiff constraints**）删值，一格确定后再影响别的格子（**AC-3 propagation**）。遇到推不下去，就挑选择最少的格子（**MRV**）先猜，猜的时候选最不妨碍别人的数字（**LCV**），猜错就回头——而且直接跳回真正出问题的地方（**backjumping**）。

Ch1 定义了 rational agent；Ch2 让它会找路；Ch3 让它会优化；Ch4 让它会对抗；Ch5 让它会利用结构推理。这就是整个考试范围。

---

## ⚠️ Where the slides / papers mislead

| 来源 | 写法 | 更准确的理解 |
|---|---|---|
| 5A Unary constraint | "South Australians won't tolerate green, and hence that **cannot** be expressed with a unary constraint: ⟨(SA), SA≠green⟩" | 应为 "**can** be expressed"——后面那个就是 unary constraint。 |
| 5B Backtracking Example #2 | 第一张写 constraints "X>Y, Y≠Z, **Z>X**"，下一张写 "**Z<X**" | 两张不一致。若 Z>X：唯一解 {X=2, Y=1, Z=3}。若 Z<X：第一个找到的解是 {X=3, Y=1, Z=2}（{X=3, Y=2, Z=1} 也是解）。考试照题目给的约束做。 |
| 5C Conflict-directed backjumping | "Q absorbs the conflict set from SA, which is {NT, NSW}" | {NT, NSW} 是 **Q 自己的** conflict set；Q 吸收 SA 的 {WA, NT, Q} 之后变成 {WA, NT, NSW}。 |
| **Oct 2025 Q4 Sudoku（试卷本身）** | Row A 印了 **3 1 2 _ _ 2**——同一行出现两个 2 | 这是试卷的 typo：按印出来的题目，整个 puzzle **无解**（我用程序检查过两种 box 形状都无解；AC-3 会让 B6 的 domain 变空）。但题目问的 A4、C2、E6 三格，**不论 box 是 2×3 还是 3×2，推出来都一样**（A4=6、C2=2、E6=1），见下方答案。 |

---

## Exam radar

| Paper | 题目 | 分数 |
|---|---|---|
| Oct 2025 Q4a | 6×6 Sudoku formulation with Alldiff (11) · AC-3 for A4, C2, E6 (9) | **20** |
| May 2026 Q4 | 4 assignment types (4) · define solution (2) · 4×4 Sudoku formulation (9) · AC-3 for A1, B2, B3, C3, D4 (10) | **25** |
| Tutorial | constraint enumeration · course scheduling · arc-consistent-but-no-solution · backtracking + MRV/degree/LCV · backjumping conflict sets | — |

### 📝 May 2026 Q4b（4×4 Sudoku）

```
    1 2 3 4
A   . 2 3 4
B   3 . . 2
C   2 . . 3
D   . . 2 .
```

**(i) Formulation（9 分）**
> - **Variables**: 16 variables, one per cell: A1, A2, A3, A4, B1, …, D4.
> - **Domains**: each empty cell has domain {1, 2, 3, 4}; each pre-filled cell has a singleton domain, e.g. D_A2 = {2}, D_A3 = {3}, D_A4 = {4}, D_B1 = {3}, D_B4 = {2}, D_C1 = {2}, D_C4 = {3}, D_D3 = {2}.
> - **Constraints**: 12 Alldiff constraints —
>   4 rows: Alldiff(A1, A2, A3, A4), Alldiff(B1, B2, B3, B4), Alldiff(C1, C2, C3, C4), Alldiff(D1, D2, D3, D4);
>   4 columns: Alldiff(A1, B1, C1, D1), Alldiff(A2, B2, C2, D2), Alldiff(A3, B3, C3, D3), Alldiff(A4, B4, C4, D4);
>   4 boxes (2×2): Alldiff(A1, A2, B1, B2), Alldiff(A3, A4, B3, B4), Alldiff(C1, C2, D1, D2), Alldiff(C3, C4, D3, D4).

**(ii) AC-3 step by step（10 分）**
> 1. **A1** — domain {1,2,3,4}. Row A constraint (A1≠A2, A1≠A3, A1≠A4) removes 2, 3, 4 → **A1 = 1**.
> 2. **B2** — row B (B2≠B1, B2≠B4) removes 3, 2 → {1, 4}; column 2 (B2≠A2) removes 2 → {1, 4}; box (A1, A2, B1, B2): now A1 = 1, so B2≠A1 removes 1 → **B2 = 4**.
> 3. **B3** — box (A3, A4, B3, B4) removes 3, 4, 2 → **B3 = 1**. (Check: row B now has 3, 4, 2 → also gives 1.)
> 4. **C3** — column 3 (C3≠A3, C3≠B3, C3≠D3) removes 3, 1, 2 → **C3 = 4**.
> 5. **D4** — column 4 (D4≠A4, D4≠B4, D4≠C4) removes 4, 2, 3 → **D4 = 1**.

（完整解：A 1 2 3 4 / B 3 4 1 2 / C 2 1 4 3 / D 4 3 2 1。）

### 📝 Oct 2025 Q4a（6×6 Sudoku）

```
    1 2 3 4 5 6
A   3 1 2 . . 2     ← 试卷印刷：同一行两个 2（typo）
B   4 6 3 1 . .
C   . . . 5 . 6
D   6 . . . 2 3
E   . . 5 . . .
F   2 . . . 6 4
```

**(i) Formulation（11 分）**
> - **Variables**: 36 variables, one per square, named by row letter and column number: A1, …, A6, B1, …, F6.
> - **Domains**: each empty square has domain {1, 2, 3, 4, 5, 6}; each pre-filled square has a singleton domain containing its given digit (e.g. D_A1 = {3}, D_B4 = {1}).
> - **Constraints**: 18 Alldiff constraints:
>   6 rows: Alldiff(A1, A2, A3, A4, A5, A6), …, Alldiff(F1, …, F6);
>   6 columns: Alldiff(A1, B1, C1, D1, E1, F1), …, Alldiff(A6, …, F6);
>   6 sub-grids (2 rows × 3 columns): Alldiff(A1, A2, A3, B1, B2, B3), Alldiff(A4, A5, A6, B4, B5, B6), Alldiff(C1, C2, C3, D1, D2, D3), Alldiff(C4, C5, C6, D4, D5, D6), Alldiff(E1, E2, E3, F1, F2, F3), Alldiff(E4, E5, E6, F4, F5, F6).

**(ii) AC-3（9 分）**

**A4**
> - Row A: remove {3, 1, 2} → {4, 5, 6}. Column 4: remove {1, 5} (B4, C4) → {4, 6}. Box (A4–A6, B4–B6): {1, 2} already removed → {4, 6}.
> - Propagate through neighbours: **B5** – row B removes {4, 6, 3, 1} → {2, 5}; column 5 removes {2, 6} → **B5 = 5**.
> - **A5** – row A → {4, 5, 6}; column 5 removes {2, 6} and now B5 = 5 → **A5 = 4**.
> - Back to A4: A4 ≠ A5 = 4 removes 4 → **A4 = 6**.

**C2**
> - Row C: remove {5, 6} → {1, 2, 3, 4}. Column 2: remove {1, 6} → {2, 3, 4}. Box (C1–C3, D1–D3): remove {6} → {2, 3, 4}.
> - **C1** – row C → {1, 2, 3, 4}; column 1 removes {3, 4, 6, 2} → **C1 = 1**.
> - **C3** – row C → {1, 2, 3, 4}; column 3 removes {2, 3, 5} → {1, 4}; C3 ≠ C1 = 1 → **C3 = 4**.
> - **C5** – row C → {1, 2, 3, 4}; column 5 removes {2, 6} → {1, 3, 4}; minus C1 = 1, C3 = 4 → **C5 = 3**.
> - Back to C2: row C now holds 1, 4, 5, 3, 6 → **C2 = 2**.

**E6**
> - Row E: remove {5} → {1, 2, 3, 4, 6}. Column 6: remove {2, 6, 3, 4} → {1}. Box (E4–E6, F4–F6): {6, 4} consistent → **E6 = 1**.

（若把 sub-grid 理解成 3 行 × 2 列：C2 可直接由 box (A1, A2, B1, B2, C1, C2) = {3, 1, 4, 6} 得到 {2}；A4、E6 结果不变。）

---

## Cheat sheet

| 项目 | 要点 |
|---|---|
| CSP = ⟨X, D, C⟩ | variables, domains, constraints ⟨scope, rel⟩ |
| Assignments | consistent/legal (no violation) · complete (all) · partial (some) · partial solution · **solution = consistent + complete** |
| Constraint types | unary, binary, ternary/higher-order, global (Alldiff) · absolute vs preference · COP |
| Binarization | dual graph transformation |
| Node consistency | satisfy unary constraints |
| Arc consistency | every value of Xᵢ has a support in Xⱼ |
| AC-3 | queue of arcs (both directions); revise; re-add (Xₖ, Xᵢ) when Dᵢ shrinks; empty → failure; O(cd³) |
| Path consistency | triples; catches WA–SA–NT with 2 colours |
| Alldiff check | m variables > n values → inconsistent |
| Atmost / bounds | sum of minimums; F1+F2 = 420 → [35,165], [255,385] |
| Sudoku | 81 vars, 27 Alldiff (9×9); 36 vars, 18 Alldiff (6×6); 16 vars, 12 Alldiff (4×4) |
| Commutativity | one variable per level → dⁿ leaves (not n!·dⁿ) |
| Backtracking | DFS + one variable at a time + backtrack when no legal value |
| MRV | fewest legal values, fail-first |
| Degree | most constraints on unassigned vars; tie-breaker; SA = 5 |
| LCV | value ruling out fewest neighbour choices, fail-last |
| Forward checking | after assigning X, prune unassigned neighbours; one step only |
| MAC | AC-3 from (Xⱼ, Xᵢ) arcs, propagate recursively |
| Backjumping | jump to most recent variable in conflict set |
| Conflict-directed | absorb conflict sets; find real culprit |
| Constraint learning | record no-goods |
| Min-conflicts | local search, complete assignment; million-queens ~50 steps |

---

## Practice (answers included)

### A. MCQ

1. A CSP solution must be: (a) partial and consistent (b) complete and consistent (c) complete only (d) legal only
2. Which heuristic is called "fail-first"? (a) LCV (b) degree (c) MRV (d) min-conflicts
3. AC-3 returns failure when: (a) queue is empty (b) a domain becomes empty (c) a domain becomes singleton (d) all arcs are revised
4. In the Australia map, the variable with the highest degree is: (a) WA (b) NT (c) SA (d) T
5. Forward checking fails to detect NT = SA = {Blue} because it: (a) uses LCV (b) only checks neighbours of the current variable (c) uses MRV (d) is a local search

**Answers**：1 (b) · 2 (c) · 3 (b) · 4 (c) · 5 (b)

### B. Short answer

**B1.** "The constraint graph is arc-consistent, therefore the CSP has a solution." Do you agree? (4 marks)
> No. Arc consistency only ensures every value has a support along each single arc. E.g. three mutually overlapping courses with two lecturers {A, B}: every arc is consistent (A is supported by B and vice versa), yet three variables cannot all take different values from two — no solution. Stronger checks (path consistency, or the Alldiff rule m > n) are needed.

**B2.** Differentiate forward checking and MAC. (4 marks)
> Forward checking, after assigning X, only removes inconsistent values from the domains of X's unassigned neighbours (one step). MAC runs AC-3 starting from the arcs (Xⱼ, X) and keeps propagating whenever a domain shrinks, so it makes all the remaining unassigned variables arc-consistent and detects failures (e.g. NT and SA both forced to Blue) that forward checking misses.

### C. Calculation

**C1.** X, Y ∈ {1, 2, 3, 4, 5}, constraint X + Y = 6 and Y > 3. Apply node then arc consistency.
> Node consistency (unary Y > 3): D_Y = {4, 5}. Arc (X, Y): X = 6 − Y ∈ {2, 1} → D_X = {1, 2}. Arc (Y, X): 4 supported by 2, 5 supported by 1 → unchanged. Result D_X = {1, 2}, D_Y = {4, 5}.

**C2.** Atmost(8, T1, T2, T3) with each domain {1, 2, 3, 4, 5, 6}. Which values can be deleted?
> The other two variables need at least 1 + 1 = 2, so each variable can be at most 8 − 2 = 6 → nothing deleted. If domains were {2, …, 6}: others need ≥ 4 → max 4 → delete 5 and 6.

### D. Thinking

**D1.** Why is Alldiff preferred over the equivalent set of binary ≠ constraints even though AC-3 needs binary constraints?
> It is easier and less error-prone to write (one Alldiff instead of C(9,2) = 36 binary constraints per unit), and special-purpose inference (e.g. m > n detection) can find inconsistencies that pairwise arc consistency cannot.
