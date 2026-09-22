# AMCS2104 Fundamentals of AI — 考前一天攻略（Chapter 1–5）

> 先读这一页，再按顺序读 Ch1 → Ch5。每章结构都一样：**故事讲解 → Exam radar（past year 完整答案）→ Cheat sheet → Practice**。
> 讲解用中文；**📝 Model answer 用英文**，可以直接照写进考卷。

---

## 1. 考卷长什么样

- **2 小时，4 题，全部要答，每题 25 分**。
- 三份 past year（Oct 2025、Jan 2026、May 2026）题型非常固定：一半是**背+解释**，一半是**画树/算题**。

## 2. Past year 出题地图

| 主题 | Oct 2025 | Jan 2026 | May 2026 | 哪里有答案 |
|---|---|---|---|---|
| 4 AI approaches | Q1a (8) | Q1a (8) | Q2a (4) | Ch1 Part 1 |
| Turing / Total Turing Test | Q1b–c (13) | Q1b (11) | — | Ch1 Part 1 + Exam radar |
| Define agent / perception vs action | — | Q1c (2) | Q2b (4) | Ch1 Part 2 |
| Rationality 4 criteria | Q1d (4) | Q1d (4) | — | Ch1 Part 3 |
| PEAS | — | — | Q2c (6) | Ch1 Part 4 |
| Problem formulation (6 components) | Q3a (6) | Q4a (6) | — | Ch2 Part 1 |
| BFS / DFS / A\* search tree | Q3b–c (19) | Q4b–c (19) | Q2d (11, A\* only) | Ch2 Exam radar |
| Hill climbing: greedy / pros / cons / stuck causes | Q2a,d (11) | Q3b (10) | Q1b–c (10) | Ch3 Part 3 |
| **State-space landscape 画图** | Q2b–c (14) | Q3b(iii) (7) | Q1d (13) | Ch3 Part 2 |
| Evolutionary algorithm | Q4b (5) | Q2 (25) | — | Ch3 Part 6 |
| Minimax / game properties | — | Q3a (8) | Q3a–b(ii) (11) | Ch4 |
| Alpha-beta L→R & R→L | — | — | Q3b(iii–iv) (14) | Ch4 Exam radar |
| CSP Sudoku + Alldiff + AC-3 | Q4a (20) | — | Q4 (25) | Ch5 Exam radar |

**按章节粗算（三份合计 300 分）**：Ch3 ≈ 97 · Ch1 ≈ 64 · Ch2 ≈ 61 · Ch5 ≈ 45 · Ch4 ≈ 33。

**规律**：
1. **Ch1 的背诵题三次都出**（4 approaches 必出）→ 最容易拿的分。
2. **Landscape 图三次都画** → 一定要能在 3 分钟内画出（objective 版和 cost 版都要会）。
3. **Search tree 三次都有**（BFS/DFS/A\* 或只有 A\*）。
4. **Ch4 与 Ch5 轮流出现**：Oct 有 CSP 没 games；Jan 有 games（少量）没 CSP；May 两个都有。**两个都要准备**。

## 3. 一天读书计划（约 9–10 小时）

| 时段 | 内容 | 目标 |
|---|---|---|
| 1:00 h | **Ch1** 全读 + 默写：4 approaches、6 capabilities、4 criteria、PEAS、7 env dimensions | 背诵题零失分 |
| 2:00 h | **Ch2** 读 Part 1–5；然后**不看答案**自己做 Oct 2025 Q3 和 Jan 2026 Q4 的三棵树，再对答案 | 画树熟练 |
| 2:00 h | **Ch3** 全读；**亲手画 2 次** objective 和 cost landscape；背 3 causes；读 EA 交通灯答案 | 最重的一章 |
| 1:30 h | **Ch4** 读 Part 1–3；自己做 May 2026 Q3 的 alpha-beta 两个方向，再对表格 | 会写 step-by-step |
| 1:30 h | **Ch5** 读 Part 1–7；自己做 May 2026 Q4b 与 Oct 2025 Q4a | AC-3 模板熟练 |
| 1:00 h | 睡前：只看 5 章的 **Cheat sheet** + 做每章 MCQ | 巩固 |

⏱️ 时间不够时的优先顺序：**Ch3 landscape + causes → Ch1 背诵 → Ch2 A\* → Ch5 Sudoku AC-3 → Ch4 alpha-beta → EA**。

## 4. 考场答题技巧

- **"Briefly explain / describe"**：名称 + 一句定义 + 一个例子（最好用题目的情境：SmartCar、交通灯、Meta AI）。
- **"Differentiate … in TWO ways"**：用表格或 "Whereas …" 句型，每一点都**两边都写**。
- **"Justify your answer"**：先写结论（Yes/No/哪一个），再写理由；理由要连到题目给的信息。
- **画 search tree**：每个 node 写 g+h=f，用 [1][2]… 标 expansion order；先写一行假设（graph/tree search、early/late goal test、alphabetical order）。
- **Alpha-beta**：用表格写每一步的 (α, β)、得到的值、为什么剪；最后列出被剪的 nodes。
- **AC-3**：每格写"row removes … → column removes … → box removes … → value"，并注明用到之前推出的哪一格。
- **Landscape**：两轴都要标名称，五个元素**都要标**，global 必须是最高（或最低）点。

## 5. 我发现的问题（考试时注意）

| 位置 | 问题 | 处理 |
|---|---|---|
| **Oct 2025 Q4 Sudoku** | Row A 印了两个 2（A3 和 A6），整个 puzzle 按题目**无解**（已用程序验证） | 题目问的 A4、C2、E6 仍可推出唯一值（6、2、1），不受影响。详见 Ch5。 |
| Oct 2025 Q3 heuristic | h(I) = 1（goal 通常为 0） | 不影响 A\* 结果，照表格算。 |
| Jan 2026 Q4 heuristic | h(D)=9、h(H)=9 其实高估（不 admissible） | A\* 仍返回 optimal A-D-H-I = 16。照表格算。 |
| DFS 的 goal test | Jan 2026 没说 early/late | Late：A-B-E-G-H-I = 45；Early：A-B-E-G-I = 31。写明你用哪种。 |
| 课件小错 | O(n log n) 被叫 "logarithmic"、bidirectional space 被叫 "linear"、alpha-beta "reduced by half"、"cannot be expressed with a unary constraint" 等 | 每章末尾 "Where the slides mislead" 有说明。 |
| Tutorial handbook | 那是同学们的答案，有几处不对（如 4 phases 写成 "Solution Formulation"、UCS 的 expansion 数） | 本笔记的答案都用程序或手算重新验证过。 |

## 6. 更新记录（第二版）

第一版只用了课件的**文字**，漏掉了课件里以**图片**形式出现的内容。第二版已逐页检查课件的全部图片页（约 260 页），补上：
- **Ch1**：四种 agent + learning agent 的**方框图**（考试"with the schematic diagram"要画）；TABLE-DRIVEN / REFLEX-VACUUM / SIMPLE-REFLEX / MODEL-BASED 的 **pseudocode**；课件的 **PEAS 例子表**（taxi、medical diagnosis、part-picking robot……）；**task environment 例子表**（crossword、poker、backgammon……）。
- **Ch2**：Romania 地图全部距离 + **h_SLD 表**；**Greedy 与 A\* 的 Romania 每一步**（450 vs 418）；BFS、UCS/BEST-FIRST、IDS/DLS 的 **pseudocode**；DFS 12 步图；BFS 时间/内存表；vacuum、8-puzzle、8-queens 的图。
- **Ch3**：landscape 图改成**照课件原图的排列**；HILL-CLIMBING、SIMULATED-ANNEALING（含 e^(ΔE/T) 计算）、GENETIC-ALGORITHM 的 **pseudocode**；8-queens **h = 17 的 successor 数值表**、p19 两个盘面的 h（17 与 16，已用程序验算）；EA 五阶段完整流程图；crossover 的 bit-string 例子；local beam 图。
- **Ch4**：讲师在每个 node 旁写 **[α, β]** 的标注法（逐步表格）；MINIMAX / ALPHA-BETA **pseudocode**；三人游戏完整的 vector 树；right-to-left 与 move ordering 的图解；May 2026 Q3 用 [α, β] 标注的两棵完整树；transposition、horizon effect、quiescence 的课件例子。
- **Ch5**：AC-3 / REVISE、BACKTRACKING、MIN-CONFLICTS 的 **pseudocode**；课件 Sudoku 的 **E6 / I6 / A6** 推导 + 完整解；search tree 与 backtracking/DFS 图；forward checking/MAC 范围图；min-conflicts 8-queens 两步图。

**不在范围内**：Tutorial 13（propositional logic、truth tables、CNF）属于 Chapter 6，本笔记没有包含。
