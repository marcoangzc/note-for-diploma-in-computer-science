# AMCS2104 — Chapter 1 (1A + 1B + 1C): AI 简介、Intelligent Agents、Designing Agents

> Slide 的问题：大量 "Question: ..." 没有答案（PEAS 的 Vacuum Cleaner 是空的、Rationality Example #2–#5 没答案、"哪种环境更难" 没答案）；agent 架构图只放图不解释。这份笔记把这些答案补上，并把 vacuum world 的分数**实际跑代码算过**。
> 术语保持英文；slide 编号写成 1A-9 表示 Chapter 1A 第 9 页。

---

## 0. 一句话总览

AI 研究的是 **rational agent**：一个通过 sensors 感知环境、用 actuators 行动、并且**在已知信息下最大化期望表现**的东西。本章分三步：1A 说明为什么选 rational agent 这条路；1B 定义 agent 和 rationality；1C 教你怎么描述任务（PEAS + 7 个环境维度）以及 agent 程序有哪几种。

| 部分 | 内容 |
|---|---|
| 1A | AI 的 4 种定义方式；Turing Test；Cognitive Modelling；Laws of Thought；Rational Agent |
| 1B | agent / percept / agent function；performance measure；rationality；omniscience；information gathering、learning、autonomy |
| 1C | PEAS；环境 7 个维度；Table-driven、Simple reflex、Model-based、Goal-based、Utility-based、Learning agents；atomic / factored / structured representation |

---

## 1. (1A) 什么是 AI？四种方法

### 1.1 两个维度 → 四格

|  | Human performance（像人） | Rationality（做对的事） |
|---|---|---|
| **Thought / reasoning**（想） | Thinking Humanly（Cognitive Modelling） | Thinking Rationally（Laws of Thought） |
| **Behavior**（做） | Acting Humanly（Turing Test） | **Acting Rationally（Rational Agent）← 本课采用** |

slide 4 的八个学者定义，只要看它们落在哪一格就行：Haugeland / Bellman → Thinking Humanly；Charniak / Winston → Thinking Rationally；Kurzweil / Rich & Knight → Acting Humanly；Poole / Nilsson → Acting Rationally。

### 1.2 Acting Humanly：Turing Test

- Turing（1950）的 imitation game：一个 interrogator 用**文字**向两个看不见的对象（一个人、一台电脑）提问，如果问完分不出哪个是电脑，电脑就通过。刻意避免物理接触，是为了只测"行为"，不测外貌。
- **Total Turing Test**（Harnad 1991）多加两项：perception（看到东西）和 object manipulation（动手）。
- 通过 Total Turing Test 需要 6 种能力，记忆口诀"语、存、推、学、看、动"：

| 能力 | 英文 | 做什么 |
|---|---|---|
| 语 | Natural language processing | 用人类语言沟通 |
| 存 | Knowledge representation | 存下知道 / 听到的 |
| 推 | Automated reasoning | 推理、得出新结论 |
| 学 | Machine learning | 适应新情况、处理不确定 |
| 看 | Computer vision | 从感知得到信息 |
| 动 | Robotics | 操作物体、移动 |

⚠️ **常见混淆**：Turing Test 只看**行为像不像人**，不管内部怎么想 —— 所以它属于 Acting Humanly，而不是 Thinking Humanly。

### 1.3 Thinking Humanly：Cognitive Modelling

想让电脑"像人一样想"，先要知道人怎么想。三条路：**introspection**（观察自己的想法）、**psychological experiments**（观察人的行为）、**brain imaging**（观察大脑）。**Cognitive science** = AI 的计算模型 + 心理学的实验方法，用来建立可检验的人脑理论。

### 1.4 Thinking Rationally：Laws of Thought

用 **logic** 把"正确的推理"形式化。slide 17 的例子：

```
Sam 是 Michelle 的 parent   [premise]
Sam 是 woman                [premise]
∴ Sam 是 Michelle 的 mother [conclusion]
```

**inference** = 从已知（或假设为真）的 premises 推出结论。（补充，非 slide 内容：最经典的三段论是 "所有人都会死；Socrates 是人；所以 Socrates 会死"。）

### 1.5 Acting Rationally：为什么本课选它（slide 19–20）

**agent** = 会行动的东西；**rational agent** = 行动的目标是得到最好结果，有不确定时得到**最好的期望结果**。

选它而不是 Thinking Rationally 的理由：
1. 有时**没有任何可证明正确的做法，但你还是得做点什么**（例如要不要过马路）。
2. 很多**反射动作**（手碰到烫的东西缩回来）成功率高，但根本没有推理。
3. 所以 "正确推理" 只是达到 rationality 的**其中一种**方式。

选它而不是 Human 那两格的理由：人的想法和行为很难用数学描述，目标可能无法实现；而 rationality 有**清楚的数学定义**，可以证明能不能达到。

---

## 2. (1B) Agent 与 Rationality

### 2.1 基本词汇

| 词 | 意思 | 例子（vacuum） |
|---|---|---|
| **agent** | 通过 sensors 感知环境、通过 actuators 作用于环境的任何东西 | 扫地机 |
| **percept** | 某一时刻的感知输入 | [A, Dirty] |
| **percept sequence** | 到目前为止**所有**感知的完整历史 | [A,Dirty],[A,Clean],[B,Dirty] |
| **agent function** | 把 percept sequence 映射成 action 的**抽象数学函数** | 那张（无穷长的）表 |
| **agent program** | agent function 的**具体实现**，跑在实体系统上 | REFLEX-VACUUM-AGENT 代码 |

slide 4–5 的 "Environment: ?" 的答案：Human → 物理世界（周围的一切）；Robotic agent → 它所在的物理空间（如工厂 / 房间）；Software agent → 屏幕上的软件 / 数字世界（文件、网络、用户界面）。

⚠️ **常见混淆 agent function vs agent program**：function 是"说明书 / 输入输出对照表"（可以是无限的），program 是"实际写出来的代码"。同一个 function 可以有很多种 program 实现。

### 2.2 Vacuum World（slide 10–13）

两个格子 A、B；agent 感知（所在位置，是否有 dirt）；actions：Left、Right、Suck。agent function 的一部分：

| Percept sequence | Action |
|---|---|
| [A, Clean] | Right |
| [A, Dirty] | Suck |
| [B, Clean] | Left |
| [B, Dirty] | Suck |
| [A,Clean],[A,Clean] | Right |
| [A,Clean],[A,Dirty] | Suck |
| … | … |

它可以用一个很小的程序实现（slide 13 / 36）：

```python
def reflex_vacuum_agent(location, status):
    if status == "Dirty": return "Suck"
    return "Right" if location == "A" else "Left"
```

### 2.3 Performance Measure（衡量的是 environment states，不是 agent 的"感觉"）

**consequentialism**：只看结果。因为机器没有自己的欲望，所以要用 **performance measure** 把"什么状态是好的"写下来 —— 它评价的是 **environment states 的序列**。

Vacuum 的三个例子（slide 17–19）—— 这里我真的跑了 10 个时间步（起点 A，A、B 都脏，每步结束后每个干净格子 +1 分）：

| t | 动作 | 位置 | 干净格数 | 累计分（无罚分） | 累计分（每次移动 −1） |
|---|---|---|---|---|---|
| 1 | Suck | A | 1 | 1 | 1 |
| 2 | Right | B | 1 | 2 | 1 |
| 3 | Suck | B | 2 | 4 | 3 |
| 4 | Left | A | 2 | 6 | 4 |
| 5 | Right | B | 2 | 8 | 5 |
| 6 | Left | A | 2 | 10 | 6 |
| 7 | Right | B | 2 | 12 | 7 |
| 8 | Left | A | 2 | 14 | 8 |
| 9 | Right | B | 2 | 16 | 9 |
| 10 | Left | A | 2 | 18 | 10 |

（这个表由代码算出。）

**Example #1（"一个 8 小时班次清掉的灰尘量"）的陷阱**：agent 可以把灰尘倒出去再吸一次来"刷分"。slide 20 的 **rule of thumb**：performance measure 要按"你**真正想要环境变成什么样**"来设计，而不是按"你觉得 agent 应该怎么做"来设计。**你要什么就得到什么**（对 rational agent 来说是这样）。

### 2.4 Rationality 依赖 4 件事（slide 21）

1. performance measure（成功的标准）
2. agent 对环境的 **prior knowledge**
3. agent **能做的 actions**
4. 到目前为止的 **percept sequence**

**定义**：对每个可能的 percept sequence，rational agent 应该选择**期望能最大化 performance measure** 的 action，依据是 percept sequence 提供的证据加上它内置的知识。

### 2.5 Rationality Example #1–#5（slide 23–28）—— slide 没有答案，下面是按 4 个条件的分析

> ⚠️ 这五题 slide 没给答案，下面是**我的分析**，考试答题时请写清楚"根据哪个条件"。

| # | 改动 | 结论 | 理由 |
|---|---|---|---|
| 1 | 每个干净格每步 +1，共 1000 步；知道地图、看得到位置和灰尘 | **Rational** | 4 个条件都满足；slide 24 也这样说。（我跑过：起点 A、两格都脏，共 1998 分，是这个环境能拿的最高分） |
| 2 | 每次左右移动 −1 分 | **原来的 reflex agent 不再 rational** | 两格都干净后它仍然来回走，每步净赚 +1，1000 步只有 **1000 分**；一个"确认两格都干净后就停"的 agent 有 **1997 分**（两个数字都是代码跑出来的）。注意：这需要 agent **记得** 另一格已经干净 → simple reflex agent 做不到，需要 model-based（有内部状态） |
| 3 | agent 以为是 2 格世界，实际是 2×2 | **不是 rational 的**（我的判断） | prior knowledge 是错的，而且没有 learning，它永远不会去清 C、D。如果它有 learning 能力就能补救（slide 33） |
| 4 | 不能移动，只能 Suck | 在它**能做的 actions** 内，脏就 Suck 是 rational 的 | rationality 是相对于"能做的 actions"来评价的；只是它的最终表现有上限 |
| 5 | 两个传感器坏了 | 没有可靠 percept，agent 无法做出有依据的选择 | rationality 依赖 percept sequence；percept 失效，就没有"依据证据"可言 |

### 2.6 Rational ≠ Omniscient（slide 29–30）

| | Rational agent | Omniscient agent |
|---|---|---|
| 是否知道行动的**实际结果** | 不知道 | 知道 |
| 决策环境 | 多数时候在不确定下 | 完全确定 |
| 优化目标 | **期望**表现 | **实际**表现 |

类比：看天气预报（70% 下雨）带伞，结果没下雨 —— 你的决定仍然 rational（依据当时的证据最大化期望）；"事后诸葛"才是 omniscient。**类比的局限**：真实中你的"预报"也可能是错的，rationality 只保证"给定你的信息下最优"。

### 2.7 一个 rational agent 应该具备的三种能力（slide 31–36）

- **Information gathering**：先感知、也可以**做动作来改变以后的 percepts**（例如过马路先看左右）。
- **Learning**：因为设计者不是 omniscient，环境大多**不是完全已知**；learning 弥补错误 / 不完整的 prior knowledge。
- **Autonomy**：如果只靠设计者给的 prior knowledge 而不靠自己的 percept 和学习，就**缺少 autonomy**，会很脆弱。

slide 36 的问题（prior knowledge 和 experience 哪个重要）：都要。**一开始给一些 prior knowledge + 学习能力；经验足够多以后，agent 的行为可以基本独立于 prior knowledge。**

---

## 3. (1C) 设计 Intelligent Agents

### 3.1 Task environment 与 PEAS

设计 agent 的**第一步**永远是尽量完整地写出 task environment，用 **PEAS**：**P**erformance measure、**E**nvironment、**A**ctuators、**S**ensors。

slide 4–6 的例子：

| Agent | P | E | A | S |
|---|---|---|---|---|
| Taxi driver | 安全、快、合法、舒适、利润高、少影响其他道路使用者 | 道路、其他车辆、警察、行人、乘客、天气 | 方向盘、油门、刹车、信号灯、喇叭、显示、语音 | 摄像头、雷达、速度表、GPS、引擎传感器、加速度计、麦克风、触屏 |
| Medical diagnosis | 病人健康、成本低 | 病人、医院、员工 | 显示问题 / 检验 / 诊断 / 治疗 | 触屏或语音输入症状 |
| Satellite image analysis | 物体、地形分类正确 | 卫星、下行链路、天气 | 显示场景分类 | 高分辨率数码相机 |
| Part-picking robot | 放入正确箱子的零件百分比 | 传送带、箱子 | 机械臂和手 | 摄像头、触觉、关节角度传感器 |

**slide 7 空白的 Vacuum Cleaner（我的答案）**：

| P | E | A | S |
|---|---|---|---|
| 清洁的格子数、省电、低噪音（对应 slide 19 的 example #3） | 房间地板、灰尘、家具、墙壁 | 轮子 / 马达、吸尘器（Suck）、（可选）扬声器 | 脏污传感器、位置传感器（或摄像头）、碰撞传感器 |

### 3.2 环境的 7 个维度

**判断口诀**（每条都问一个问题）：

| 维度 | 问自己 | 前者（易） | 后者（难） |
|---|---|---|---|
| Observability | sensors 给我完整状态吗？ | Fully observable | Partially observable |
| Agents | 有别的东西也在**最大化自己的 performance measure**（且我的行为影响它）吗？ | Single-agent | Multiagent（competitive / cooperative / partially both） |
| Determinism | 下一个状态 100% 由**当前状态 + 我的动作**决定吗？ | Deterministic | Stochastic / non-deterministic |
| Episodic? | 这次决定会影响以后吗？ | Episodic（每集独立） | Sequential |
| Static? | 我思考时环境会变吗？ | Static | Dynamic（Semi-dynamic：环境不变但**分数**随时间变） |
| Discrete? | 状态 / 时间 / percepts / actions 是有限个吗？ | Discrete | Continuous |
| Known? | 我知道"物理规律"（每个动作的结果）吗？ | Known | Unknown |

**slide 29 的表（我逐格读图确认）**：

| Task | Observable | Agents | Deterministic | Episodic | Static | Discrete |
|---|---|---|---|---|---|---|
| Crossword puzzle | Fully | Single | Deterministic | Sequential | Static | Discrete |
| Chess with a clock | Fully | Multi | Deterministic | Sequential | Semi | Discrete |
| Poker | Partially | Multi | Stochastic | Sequential | Static | Discrete |
| Backgammon | Fully | Multi | Stochastic | Sequential | Static | Discrete |
| Taxi driving | Partially | Multi | Stochastic | Sequential | Dynamic | Continuous |
| Medical diagnosis | Partially | Single | Stochastic | Sequential | Dynamic | Continuous |
| Image analysis | Fully | Single | Deterministic | Episodic | Semi | Continuous |
| Part-picking robot | Partially | Single | Stochastic | Episodic | Dynamic | Continuous |
| Refinery controller | Partially | Single | Stochastic | Sequential | Dynamic | Continuous |
| English tutor | Partially | Multi | Stochastic | Sequential | Dynamic | Discrete |

**slide 28 的问题（哪种更难）**：右边那一列（partially observable、multiagent、stochastic、sequential、dynamic、continuous、unknown）。最难的现实例子是 **taxi driving**，它几乎每一项都在"难"的那一边。

⚠️ **常见混淆**
- **Known vs Unknown 不是 observable**。Known 说的是 agent 知不知道规则；Poker 规则完全已知，但牌是看不到的（partially observable，known）；一个刚拿到手的新游戏可能屏幕完全看得到（fully observable）但你不知道规则（unknown）。
- **Static 与 Semi-dynamic**：有钟的 chess，棋盘不会自己变，但你想得越久分数（时间）越少 → semi-dynamic。
- **Deterministic 是"整个系统"的属性**：即使 fully observable，也可能 stochastic（backgammon 掷骰子）。
- **怎么判断 other entity 是不是 agent**（slide 15）：看它的行为能不能被描述为"在最大化一个依赖我的行为的 performance measure"。路边的树 → 不是；另一辆车 → 是。

### 3.3 Agent = Architecture + Program

architecture 把 sensor 数据送给 program、运行 program、把 program 选出的 action 送给 actuators。

### 3.4 Table-Driven Agent 为什么不可行

slide 32 的程序：把 percept 追加到历史，然后**在表里查**。表的 entries 数：

$$\sum_{t=1}^{T} |P|^t$$

vacuum world 里 |P| = 4（2 个位置 × 2 种状态）：

| T | entries |
|---|---|
| 1 | 4 |
| 2 | 20 |
| 3 | 84 |
| 10 | 1,398,100 |
| 100 | ≈ 2.1 × 10^60 |

（代码算出）—— 存不下、造不出、也无法从经验学习。**挑战**：写很小的程序也能产生 rational 行为。

### 3.5 四种基本 agent program

#### (a) Simple reflex agent

只根据**当前 percept**选 action，靠 **condition–action rules**（if–then）。

```
function SIMPLE-REFLEX-AGENT(percept):
    state  ← INTERPRET-INPUT(percept)     # 把 percept 抽象成状态描述
    rule   ← RULE-MATCH(state, rules)     # 找第一条匹配的规则
    return rule.ACTION
```

- 优点：容易实现，程序很小（slide 37 说"把可能性从 4^T 降到 4"，是在说规则只需要看 4 种当前 percept；严格说表的大小是 Σ4^t）。
- 缺点：**只在 fully observable 时好用**。例子：如果 vacuum agent 没有位置传感器，只有 dirt sensor，那 [Clean] 时应该 Left 还是 Right？无论选哪个都可能永远卡住。slide 40 说 randomized 版本更好 —— 在这个例子里成立（随机选方向最终会走到另一格），但不是一般结论。

#### (b) Model-based reflex agent

为了处理 partial observability，agent 保存一个**内部状态**，记录"现在看不到的那部分世界"。要编码两种知识：

| Model | 内容 | 用途 |
|---|---|---|
| **Transition model** | 世界怎么变化：① 不管我做什么它自己怎么变；② 我的动作会造成什么效果 | 预测"动作后世界变成什么" |
| **Sensor model** | 当前世界状态**如何反映在 percepts 里** | 从 percept 推回世界状态 |

`UPDATE-STATE(state, action, percept, transition_model, sensor_model)` 产出新的 state = "现在世界大概是什么样"。⚠️ 这个 state 只是 **best guess**，所以 partially observable 环境里仍要在不确定下做决定。

例：2.5 里"确认两格都干净后停下"的 agent，就是靠内部状态"记得 B 已经干净"。

#### (c) Goal-based agent

除了 state，还记录 **goals**（哪些情况是想要的），选择**最终能达成 goal 的动作**（需要搜索 / planning）。

| | Goal-based | Reflex |
|---|---|---|
| 决策方式 | 推理（考虑"如果我这样做会怎样"） | 规则匹配（slide 47 写成 "Reflection"，意思是 reflex） |
| 适应性 | 高（改 goal 就行，不用改规则） | 低 |

缺点：goal 只有 **达成 / 没达成** 两种（binary）；到达 goal 的路径有好有坏它分不出来。

#### (d) Utility-based agent

用 **utility function** 给每个世界状态打分（"这状态让我多开心"），选**期望 utility 最大**的动作：

$$EU(a) = \sum_{s'} P(s' \mid a)\, U(s')$$

例（我自己的数字）：去机场，路线 A：80% 概率 30 分钟、20% 概率 60 分钟；路线 B：一定 40 分钟。用 utility = −时间：EU(A) = −(0.8×30 + 0.2×60) = **−36**，EU(B) = **−40** → 选 A。goal-based agent 只知道"到了没"，无法做这种比较。

| 情况 | Utility-based | Goal-based |
|---|---|---|
| 有多个 goal | ✔ | ✘ |
| goal 互相冲突（快 vs 安全） | ✔ | ✘ |
| 环境不确定（partially observable） | ✔ | ✘ |

**utility function ≠ performance measure**：utility function 是 agent **内部**的评分，performance measure 是**外部**的评分。两者一致时，rational agent 选择最大化 utility 就等于最大化 performance。

难点（slide 53）：要建模复杂环境、要做感知 / 表示 / 推理 / 学习的研究，utility 计算复杂度高就不实用。

#### (e) Learning agent（任何一种 agent 都可以做成 learning agent）

```
            performance standard
                    │
                    ▼
   Sensors ───► [ Critic ]
       │            │ feedback
       │            ▼
       │      [ Learning element ] ──learning goals──► [ Problem generator ]
       │            │ changes  ▲ knowledge                    │
       ▼            ▼          │                             │
     [ Performance element ] ◄─────────────────────────────┘
                    │
                    ▼
                Actuators
```

| 组件 | 职责 | 自动驾驶 taxi 例子 |
|---|---|---|
| Performance element | 选**外部动作**（就是前面说的整个 agent） | 现有的驾驶知识和程序 |
| Critic | 依据**固定的 performance standard** 评价行为 | 发现"刚才急转弯，乘客被吓到" |
| Learning element | 改进 performance element | 修改转弯规则 |
| Problem generator | 提议**新的探索性动作**以获得新经验 | 试试不同刹车距离 |

⚠️ **常见混淆**：critic 用的是**固定**标准（外部的），所以不是 agent 自己可以偷偷改的 —— 否则它会把标准改到容易达成为止。

### 3.6 环境状态的三种表示（slide 58–62）

| 表示 | 特点 | 例子（路线规划） |
|---|---|---|
| **Atomic** | 状态是不可分的"黑盒" | 城市 B、城市 C 各是一个符号 |
| **Factored** | 状态 = 一组固定的变量，每个有值 | GPS 位置、过路费等属性 |
| **Structured** | 状态里有**对象**，对象有属性，还有对象之间的**关系** | "卡车倒车进农场车道，被一头牛挡住" |

复杂度和表达力依次增加。slide 62 的要点：factored 表示不会预先有一个变量叫 `TruckAheadBackingIntoDairyFarmDrivewayBlockedByLooseCow`，structured 表示可以直接描述"卡车"、"牛"以及它们的关系。（补充，非 slide 内容：Chapter 2 的 search 用 atomic 表示。）

---

## ⚠️ Slide 里有问题或需要小心的地方

| Slide | Slide 写的 | 更准确的理解 |
|---|---|---|
| 1A-18 | agent 来自拉丁文 "agree" | 应该是 **agere**（to do），"agree" 是打字错误 |
| 1A-17 | 用 Sam / Michelle 例子说明 syllogism | 推理本身有效，但它不是经典三段论形式（All A are B…）；考试按 slide 答即可 |
| 1B-25 / 26 / 27 / 28 | 提问但没有答案 | 见 2.5 节（我的分析，不是 slide 官方答案） |
| 1C-3 | "task environment represents the problems to which a rational agent is going to solve" | 意思是 task environments 是问题，rational agents 是**解答** |
| 1C-17 | 表头写 "Deterministic / Stochastic"，标题却是 "Non-Deterministic" | 严格说 stochastic（有概率）和 nondeterministic（只列出可能结果）不同；本课把它们当成同一类"不是 deterministic" |
| 1C-37 | reflex agent 把可能性从 4^T 降到 4 | 简化说法；表的实际大小是 Σ4^t |
| 1C-40 | randomized reflex agent outperforms simple reflex | 只在"没有位置传感器"这类例子里成立，不是一般规律 |
| 1C-47 | reflex 的 decision making 写成 "Reflection" | 应该理解为 reflex（规则触发），不是 reflection |

**考试策略**：如果题目引用 slide 的说法，按 slide 答；但你要知道上面这些真实情况。

---

## Cheat sheet

| 概念 | 一句话 |
|---|---|
| Rational agent | 对每个 percept sequence，选**期望**最大化 performance measure 的 action |
| Rationality 的 4 因素 | performance measure、prior knowledge、可用 actions、percept sequence |
| Rational vs omniscient | 前者最大化**期望**，后者知道**实际结果** |
| Agent function / program | 抽象映射 / 具体实现 |
| PEAS | Performance, Environment, Actuators, Sensors |
| 7 维度 | observable、agents、deterministic、episodic、static、discrete、known |
| Table-driven 表大小 | Σ_{t=1..T} \|P\|^t |
| Simple reflex | 只看当前 percept；需要 fully observable |
| Model-based | + 内部状态（transition model + sensor model） |
| Goal-based | + goals（binary） |
| Utility-based | + utility function，最大化**期望 utility** |
| Learning agent 4 部分 | performance element、critic、learning element、problem generator |
| 3 种表示 | atomic → factored → structured |

---

## Practice

### A. 选择题（5）

**A1.** Total Turing Test 比 Turing Test 多要求哪两种能力？
(a) NLP 和 reasoning  (b) perception 和 object manipulation  (c) learning 和 knowledge representation  (d) logic 和 psychology

**A2.** Rationality 依赖以下哪一项**不**在 slide 的 4 个条件里？
(a) performance measure  (b) prior knowledge  (c) 可执行的 actions  (d) 动作的**实际**结果

**A3.** 下面哪个是 episodic 环境？
(a) Chess  (b) Taxi driving  (c) 装配线上的缺陷检测  (d) Poker

**A4.** Simple reflex agent 只有在什么情况下才表现良好？
(a) 环境是 stochastic  (b) 环境 fully observable  (c) 环境是 continuous  (d) 环境是 multiagent

**A5.** Learning agent 里哪个组件负责建议"新的探索性动作"？
(a) critic  (b) learning element  (c) performance element  (d) problem generator

### B. 简答题（3）

**B1.** 为一个"自动垃圾邮件过滤器"写出 PEAS。

**B2.** 判断 Poker 和 Backgammon 各自在 7 个维度中的 observable / deterministic / static 三项，并说明它们唯一的关键差异是什么。

**B3.** 解释 utility function 和 performance measure 的区别。

### C. 计算 / 追踪（3）

**C1.** vacuum world 里 |P| = 3，agent 生命周期 T = 5，table-driven agent 的 lookup table 有多少 entries？

**C2.** 用 REFLEX-VACUUM-AGENT，起点 A，A 和 B 都脏，performance measure = 每个时间步结束后每个干净格子 +1 分。跑 10 步，总分是多少？如果每次左右移动再 −1，总分是多少？

**C3.** 路线 X：60% 概率 20 分钟、40% 概率 50 分钟；路线 Y：一定 35 分钟。utility = −时间，agent 选哪条？

### D. 思考题（2）

**D1.** 如果 vacuum 的 performance measure 是"每吸走一份灰尘 +1 分"，rational agent 会怎么做？这说明了什么设计原则？

**D2.** slide 12 问："Turing Test 今天还 relevant 吗？"请给出两个支持和两个反对的理由。

---

### 答案

**A1.** (b)。Total Turing Test 加了 perceptual ability 和 object manipulation（对应 computer vision 和 robotics）。

**A2.** (d)。Rational 不需要 omniscience，它只依赖 percept sequence 到目前为止的信息。

**A3.** (c)。每件产品独立检测，这次判断不影响下一次。

**A4.** (b)。Simple reflex 只看当前 percept，如果看不到完整状态（partially observable），就会做出没有依据的选择。

**A5.** (d)。Critic 评价、learning element 改进、performance element 行动、problem generator 提出新实验。

**B1.**
- P：把垃圾邮件正确分到垃圾箱、把正常邮件留在收件箱（少误杀）、处理速度
- E：邮箱服务器、收到的邮件流、用户
- A：把邮件移到垃圾箱 / 收件箱、打标签、（可选）向用户显示提示
- S：邮件内容（文字、发件人、链接）、用户的"这不是垃圾"反馈

**B2.**
| | Observable | Deterministic | Static |
|---|---|---|---|
| Poker | **Partially**（看不到对手的牌） | Stochastic（发牌） | Static |
| Backgammon | **Fully**（棋盘全部可见） | Stochastic（掷骰子） | Static |

关键差异是 **observability**：两者都有随机性，但 backgammon 的棋盘完全可见，poker 有隐藏信息。

**B3.** utility function 是 agent **内部**的评分，把每个世界状态映射成数字；performance measure 是**外部**（设计者定义）的评分。两者一致时，rational agent 最大化 utility 就同时最大化 performance。

**C1.** 3 + 9 + 27 + 81 + 243 = **363**。

**C2.** 跟 2.3 节的表一致：无罚分 **18** 分；每次移动 −1 时 **10** 分（代码验证）。第 3 步之后两格都干净，agent 还在来回走：无罚分时每步 +2，有罚分时每步净 +1。

**C3.** EU(X) = −(0.6×20 + 0.4×50) = −(12 + 20) = **−32**；EU(Y) = **−35**。选 **X**。

**D1.** 它会把灰尘倒出去再吸一次来刷分（甚至专门制造灰尘）。这就是 slide 20 的原则：performance measure 要按"你真正希望环境变成什么样"设计（比如"干净的格子数"），而不是按"你觉得 agent 应该怎么做"设计。

**D2.**（参考）支持：它仍是评价"看起来像不像人"的直觉基准（例如聊天机器人评测）；6 项能力仍是 AI 的核心组成。反对：现代 AI 的目标是做**有用 / rational** 的系统，而不是骗人；通过测试可以靠"会骗人"而不是"真的智能"；Rational agent 观点（本课采用）把目标定义得更清楚、可数学分析。

---

## 与其他章节的联系

- Ch1C 的 **goal-based agent** = Ch2 的 **problem-solving agent**（用 search 找 action 序列）。
- Ch2 的假设"environment 是 episodic、single agent、fully observable、deterministic、static、discrete、known"正是用 Ch1C 的 7 个维度列出来的。
- Ch4 的 games 是 **multiagent + competitive** 环境；Ch4 的 utility（终局收益）就是 Ch1C 的 utility 概念。
- Ch3 的 local search 适用于"路径不重要，只要最终状态"的问题。
