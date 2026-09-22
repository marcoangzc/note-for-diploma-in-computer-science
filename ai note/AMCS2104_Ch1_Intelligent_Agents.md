# AMCS2104 — Chapter 1: Introduction to AI & Intelligent Agents (1A + 1B + 1C)

> 本章要回答的问题：一台机器要做到什么，才算"有智能"？如果我们要亲手造一个智能系统，第一步该描述什么？
>
> 📌 考试比重：3 份 past year 每份都有一大题（约 14–25 分）。**全部都是"背 + 解释"题**，是最容易拿满分的一章。

---

## Scene：TAR UMT 的 SmartCar

你和组员被分配做 final year project：一辆自动驾驶车，叫 **SmartCar**。
第一次开会，大家就吵起来了：

- 阿明说："要让乘客**分不出**是人在开还是机器在开，那才叫智能。"
- 小慧说："不对，要让它像人一样**思考**，脑袋里的推理过程要跟人一样。"
- 阿杰说："人会犯错啊。应该让它按**逻辑**推理，永远推出正确结论。"
- 你说："我不管它怎么想，我只要它每一次都**做出最好的动作**，安全、快速到达目的地。"

四个人其实代表了 AI 历史上的四种路线。本章就是从这场争论开始的。

---

## Part 1：四种 AI 路线 —— "智能"到底指什么？

### 1.1 两个维度，切出四格

几乎所有 AI 的定义都可以沿着两个维度来分：

1. **Human performance vs. Rationality**：以"像人"为标准，还是以"理性、做对的事"为标准？
2. **Thought processes (thinking) vs. Behaviour (acting)**：看它**怎么想**，还是看它**怎么做**？

```
                   Human performance          Rationality
                 ┌───────────────────────┬───────────────────────┐
 Thought         │  Thinking Humanly     │  Thinking Rationally  │
 processes       │  (Cognitive Modelling)│  ("Laws of Thought")  │
                 ├───────────────────────┼───────────────────────┤
 Behaviour       │  Acting Humanly       │  Acting Rationally    │
                 │  (Turing Test)        │  (Rational Agent)     │
                 └───────────────────────┴───────────────────────┘
```

回到会议：阿明 = Acting Humanly，小慧 = Thinking Humanly，阿杰 = Thinking Rationally，你 = Acting Rationally。

### 1.2 Acting Humanly —— The Turing Test Approach

阿明的想法有一个著名的测试：**Turing Test**。

- 由 **Alan Turing 在 1950 年**提出，另一个名字叫 **the imitation game**（Oct 2025 考过 1 分："another name for the Turing Test"）。
- 目的：测试电脑能否表现出**与人类相当的智能行为**。
- 三方：**a computer, a human respondent, a human interrogator**。
- 双方**没有直接物理接触**；interrogator 只提出 **written questions**。
- 如果 interrogator 看完书面回答后，**分辨不出**是人还是电脑写的 → 电脑通过。

但只打字就够了吗？一个只会聊天、却看不见也动不了的系统，算完整的智能吗？
所以 **Stevan Harnad 在 1991 年**提出了 **Total Turing Test**，多加了两个要求：

- **Perceptual ability**（感知能力，例如通过视频信号看东西）
- **Object manipulation ability**（操作物体、移动的能力）

要通过 Total Turing Test，电脑至少需要 **6 种能力**（Oct 2025 考 12 分！要写"能力名 + 用途"）：

| # | Capability | 用途（要写出来） |
|---|---|---|
| 1 | **Natural language processing** | to communicate successfully in a human language |
| 2 | **Knowledge representation** | to store what it knows or hears |
| 3 | **Automated reasoning** | to use the stored information to answer questions and draw new conclusions |
| 4 | **Machine learning** | to adapt to new circumstances, detect patterns and handle uncertainties |
| 5 | **Computer vision** | to perceive objects / derive information from its percepts |
| 6 | **Robotics** | to manipulate objects and move about |

记忆口诀：**"说、记、想、学、看、动"**。前 4 个 = 普通 Turing Test 就需要；后 2 个（vision + robotics）= Total Turing Test 额外加的。

### 1.3 Thinking Humanly —— The Cognitive Modelling Approach

小慧要机器"像人一样想"。问题来了：**我们必须先知道人是怎么想的。** 有 3 种方法：

1. **Introspection** —— 捕捉自己脑中闪过的想法（自我反省）。
2. **Psychological experiments** —— 观察一个人在行动中的表现。
3. **Brain imaging** —— 观察大脑运作（如 fMRI）。

相关领域：**Cognitive science**，是跨学科领域，把 AI 的计算模型和心理学的实验技术结合起来，建立关于人类心智的**精确、可测试**的理论。

### 1.4 Thinking Rationally —— The "Laws of Thought" Approach

阿杰要"正确的思考"。**Laws of thought** = 支配所有人思考与讨论的规则，是理性讨论的基础，试图把 "right thinking"（无可反驳的推理过程）规范化，由此催生了 **logic** 这个领域。

例子：**Syllogism**（三段论）——两个 premise + 一个 conclusion 的 deductive reasoning：

```
Premise:    Sam is Michelle's parent.
Premise:    Sam is a woman.
Conclusion: Therefore, Sam is Michelle's mother.   ← inference（推论）
```

⚠️ **Challenge**（tutorial 考过）：现实世界的知识往往是 informal、uncertain 的，很难用严格的逻辑符号表达；而且"原则上能解"和"实际上能解"差很远（计算量太大）。

### 1.5 Acting Rationally —— The Rational Agent Approach

你（选的路线）："做出最好的动作"。
**Agent** 就是会行动的东西（拉丁文 *agere* = to do）。**Rational agent** 会采取行动来达到 **best outcome**；在有不确定性的时候，达到 **best expected outcome**。

**为什么本课程采用 Rational Agent approach？**（tutorial 常问）

- **比 Thinking Rationally 更广**：正确的逻辑推理只是达到理性的**其中一种**方法。有时候没有"可证明正确"的事可做，但还是得行动；有些 reflex action（例如手碰到火马上缩回）不需要推理，却更成功。
- **比 Acting/Thinking Humanly 更可行**：人类行为和思维很难用数学建模；而 rationality 的标准是**通用的、可以用数学清楚定义的**，所以是可达成的。

📝 **Model answer（4 approaches，Oct 2025 & Jan 2026 各 8 分）**

> 1. **Acting Humanly (Turing Test approach)** – the AI system is developed to *act like a human*, so that its behaviour cannot be distinguished from a human's. It is tested by the Turing Test: if a human interrogator cannot tell whether written responses come from a computer or a person, the computer passes. Example: a chatbot / voice assistant such as Siri.
> 2. **Thinking Humanly (Cognitive Modelling approach)** – the AI system is developed to *think like a human*. We must first understand how humans think, through introspection, psychological experiments and brain imaging, and then build computer models of the human mind (cognitive science). Example: an intelligent tutoring system that models a student's thinking.
> 3. **Thinking Rationally ("Laws of Thought" approach)** – the AI system is developed to *think logically*, following laws of thought / formal logic (e.g. syllogisms) so that correct conclusions are always drawn from true premises. Example: a rule-based tax calculation / expert system.
> 4. **Acting Rationally (Rational Agent approach)** – the AI system is developed to *act rationally*: it is an agent that selects the action expected to achieve the best outcome (or best expected outcome under uncertainty) according to a performance measure. Example: a robot vacuum that chooses the most efficient cleaning path.

---

## Part 2：Agent —— 把"做对的事"变成可以设计的东西

选了 rational agent 路线，下一个问题是：**agent 到底由什么组成？**

### 2.1 Definition

> **An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators.**
> （Jan 2026 考 2 分："Define agent in terms of AI"——就写这句。）

```
              percepts
   ┌────────┐ ◀──────── Sensors ◀──┐
   │ Agent  │                      │  Environment
   │   ?    │ ────────▶ Actuators ─┘
   └────────┘   actions
```

| Agent | Sensors | Actuators |
|---|---|---|
| Human | eyes, ears, other organs | hands, legs, vocal tract |
| Robot | cameras, infrared range finders | motors |
| Software | keyboard, mouse, touchscreen, microphone (file contents, network packets) | display screen, speaker (writing files, sending packets) |
| SmartCar | camera, LiDAR, GPS, speedometer | steering, accelerator, brake, horn |

### 2.2 Agent 与环境的 2 种互动（May 2026 Q2b，2+2 分）

| | **Perception** | **Action** |
|---|---|---|
| 性质 | **passive** interaction | **active** interaction |
| 对环境的影响 | 获取环境信息，**不改变**环境 | 执行后**环境被改变** |
| 用什么 | sensors | actuators |
| SmartCar 例子 | 摄像头看到前方红灯 | 踩刹车让车停下 |

### 2.3 Percept、Percept sequence、Agent function、Agent program

- **Percept**：agent 在某一瞬间的感知输入。
- **Percept sequence**：agent 至今感知到的**完整历史**。
- Agent 的选择可以取决于 built-in knowledge + 整个 percept sequence，但**不能取决于它没感知到的东西**。
- **Agent function**：把任意 percept sequence **映射到** action 的**抽象数学描述**（可以想象成一张无限长的表）。
- **Agent program**：agent function 的**具体实现**，在某个物理系统上运行。

例：Vacuum world（两格 A、B；能感知在哪一格、有没有脏；动作 Left / Right / Suck）

```
Percept sequence                      Action
[A, Clean]                            Right
[A, Dirty]                            Suck
[B, Clean]                            Left
[B, Dirty]                            Suck
[A, Clean], [A, Clean]                Right
[A, Clean], [A, Dirty]                Suck
...                                   ...
```

📝 **Agent function vs agent program**：agent function is an *abstract mathematical description* that maps any percept sequence to an action; agent program is the *concrete implementation* of that function running on the agent's physical architecture.

---

## Part 3：Rationality —— 什么叫"做对的事"？

### 3.1 Consequentialism 与 Performance measure

AI 用 **consequentialism** 判断对错：**只看结果**。行动带来想要的结果 → 就是对的。
但机器没有自己的"想要"。所以我们设计 **performance measure**：**评估环境状态序列（sequence of environment states）是否令人满意**的标准。

Vacuum world 三种 performance measure：

| Example | Performance measure | 会发生什么 |
|---|---|---|
| #1 | 8 小时内吸走的灰尘**量** | agent 可以作弊：吸起来→倒回去→再吸，分数无限高 |
| #2 | 每个时间步，每一格干净得 1 分 | agent 会让地板保持干净 |
| #3 | 同 #2，但耗电与噪音要扣分 | agent 会在干净时停下不动 |

**Rule of thumb**：Design performance measures according to **what one actually wants to be achieved in the environment**, not according to how one thinks the agent should behave. ("What you ask for is what you get.")

### 3.2 Rationality 的 4 个依据（Oct 2025 & Jan 2026 各 4 分，必背）

> At any given time, what is rational depends on:
> 1. **The performance measure** that defines the criterion of success.
> 2. **The agent's prior knowledge** of the environment.
> 3. **The actions** that the agent can perform.
> 4. **The agent's percept sequence** to date.

口诀：**P-K-A-P**（Performance, Knowledge, Actions, Percepts）。

**Definition of a rational agent**：For each possible percept sequence, a rational agent should select an action that is **expected to maximize its performance measure**, given the evidence provided by the percept sequence and whatever built-in knowledge the agent has.

### 3.3 用 4 个依据判断"是不是 rational"（tutorial 题型）

基准情境（Example #1）：两格世界，1000 个时间步，每格干净每步 +1 分；地理已知，灰尘分布与初始位置未知；动作 Left/Right/Suck；感知位置和灰尘都准确。agent 的规则："脏就吸，否则移到另一格"。
→ **Rational**：在这些条件下，没有其他 agent 的 expected performance 比它高。

之后每个 example 只改**一个**依据，你要指出**是哪一个依据变了**、会有什么后果：

| Example | 改变的依据 | 答案思路 |
|---|---|---|
| #2 每次移动扣 1 分 | Performance measure | **不再 rational**：两格都干净后它还在来回走，一直扣分；更好的 agent 会在确定都干净后停下（NoOp）。 |
| #3 实际 4 格，它以为只有 2 格 | Prior knowledge | 它永远不会去 C、D，那两格一直脏 → performance 很低；需要 **information gathering / learning / exploration** 才能补救。考试写：**not rational (poor expected performance) because its prior knowledge is incorrect**，并提出补救。 |
| #4 只能 Suck，不能移动 | Actions | 只能清理自己所在的那格。 |
| #5 传感器坏了，percept 不是最新的 | Percept sequence | 它不知道哪里脏 / 自己在哪 → 行动基于错误的 evidence。 |

⚠️ **#4、#5 的微妙之处**：严格按定义，rationality 是**相对于它拥有的**动作与感知来判断的——一个只能 Suck 的 agent，如果每次脏就吸，它已经"尽了自己能力的最好"，按课本定义仍可算 rational（只是 performance 低）。课件只提出问题没给答案，tutorial 的学生答案则写 "No"。**考试策略**：先点名是哪一个 criterion 改变了，再说明对 expected performance 的影响，最后给结论。理由写得清楚，两种结论都能拿分。

### 3.4 Rationality ≠ Omniscience

| | Rational agent | Omniscient agent（全知） |
|---|---|---|
| 知不知道行动的实际结果 | 不知道 | 知道 |
| 行动环境 | 大部分时间在 uncertainty 下 | 永远在 certainty 下 |
| 目标 | 最大化 **expected** outcome | 最大化 **actual** outcome |

例子：你过马路前看了两边，没车才走，结果天上掉下一块门板砸中你——你**仍然是 rational** 的，因为你不可能预知。Rationality 只依据**至今为止的 percept sequence**。

### 3.5 Rational agent 应具备的 3 种能力

1. **Information gathering**：行动前先感知环境；做一些动作去**改变未来的 percepts**（例如过马路前先看两边）。
2. **Learning**：设计者不是全知的，环境通常不是事先完全已知的；学习可以**弥补不完整或错误的 prior knowledge**，表现更好、适应更多环境。
3. **Autonomy**：如果只依赖设计者的 prior knowledge 而不是自己的 percepts 与学习，就**缺乏 autonomy**，很脆弱。Rational agent 应能根据自己的经验行动。实务上：先给一些初始知识 + 学习能力，经验足够后，行为可以**独立于 prior knowledge**。

---

## Part 4：Task Environment —— 设计 agent 的第一步

要设计 SmartCar，**第一步永远是把 task environment 描述清楚**。工具：**PEAS**。

### 4.1 PEAS

- **P**erformance measure
- **E**nvironment
- **A**ctuators
- **S**ensors

📝 **Model answer：SmartCar / automated taxi PEAS（May 2026 Q2c，2+4 分）**

> - **Performance measure**: safe (no accidents), fast / shortest travel time to the correct destination, legal (obeys traffic laws), comfortable trip, minimum fuel/energy consumption.
> - **Environment**: roads, other vehicles, pedestrians, traffic lights and signs, road works, weather, passengers.
> - **Actuators**: steering, accelerator, brake, gear, signal lights, horn, display/speaker to talk to passengers.
> - **Sensors**: cameras, LiDAR, radar, ultrasonic sensors, GPS, speedometer, odometer, accelerometer, engine/fuel sensors.

**课件（1C p4–p7）的 PEAS 例子表**——考试题目常常换成这些 agent，要能照格式写：

| Agent type | Performance measure | Environment | Actuators | Sensors |
|---|---|---|---|---|
| **Taxi driver** | safe, fast, legal, comfortable trip, maximize profits, minimize impact on other road users | roads, other traffic, police, pedestrians, customers, weather | steering, accelerator, brake, signal, horn, display, speech | cameras, radar, speedometer, GPS, engine sensors, accelerometer, microphones, touchscreen |
| **Medical diagnosis system** | healthy patient, reduced costs | patient, hospital, staff | display of questions, tests, diagnoses, treatments | touchscreen/voice entry of symptoms and findings |
| **Satellite image analysis system** | correct categorization of objects, terrain | orbiting satellite, downlink, weather | display of scene categorization | high-resolution digital camera |
| **Part-picking robot** | percentage of parts in correct bins | conveyor belt with parts; bins | jointed arm and hand | camera, tactile and joint angle sensors |
| **Refinery controller** | purity, yield, safety | refinery, raw materials, operators | valves, pumps, heaters, stirrers, displays | temperature, pressure, flow, chemical sensors |
| **Interactive English tutor** | student's score on test | set of students, testing agency | display of exercises, feedback, speech | keyboard entry, voice |
| **Vacuum cleaner**（课件留作练习 "?"） | cleanliness (clean squares per time step), energy used, noise, time | squares/rooms, dirt, furniture/walls | wheels (Left/Right), suction (Suck) | location sensor, dirt sensor |

其他 tutorial 考过的 PEAS（写法一样，**每项写 3–5 个具体东西**）：

| Agent | P | E | A | S |
|---|---|---|---|---|
| Vacuum cleaner | cleanliness, energy used, time taken | rooms/squares, dirt, furniture | wheels (Left/Right), suction | location sensor, dirt sensor |
| Facial recognition (Meta) | accuracy of identification, speed, few false matches | uploaded photos/videos, users' faces | tag suggestion / notification display | the uploaded images (pixels) |
| Hearts card game | minimise penalty points, win the game | 52-card deck, 3 opponents, rules | play a card, pass cards | own hand, cards played, scores |
| Chinese chess program | win, enjoyable difficulty | board, pieces, opponent | move a piece | board state / opponent's moves |

### 4.2 环境的 7 个维度

| 维度 | 定义（考试写这句） | 例子 |
|---|---|---|
| **Fully vs Partially observable** | Fully: sensors give access to the **complete state** of the environment at each point in time; otherwise partially (noisy sensors / missing parts). No sensors → **unobservable**. | Fully: chess, image recognition · Partially: card game, taxi driving |
| **Single-agent vs Multiagent** | only one agent vs more than one agent interacting | Single: crossword, Spider solitaire · Multi: chess, taxi |
| **Deterministic vs Non-deterministic (stochastic)** | next state is **completely determined by current state + action** | Det: chess, tic-tac-toe · Non-det: soccer, taxi |
| **Episodic vs Sequential** | episodic: experience divided into **atomic episodes**, each = one percept + one action, next episode **does not depend** on previous actions; sequential: **current decision affects all future decisions** | Episodic: mail sorting, defect detection · Sequential: chess, taxi |
| **Static vs Dynamic** | static: environment **does not change while the agent is deliberating**; dynamic: changes; **semi-dynamic**: environment unchanged but **performance score changes with time** | Static: crossword, chess without clock · Dynamic: taxi, soccer · Semi: chess **with a clock** |
| **Discrete vs Continuous** | finite number of distinct states, percepts, actions (and time points) | Discrete: chess, tic-tac-toe · Continuous: basketball, taxi |
| **Known vs Unknown** | about the agent's knowledge of the "**laws of physics**" of the environment (outcomes of actions are given or not) — not the environment itself | Known: chess rules · Unknown: a new video game without instructions |

**课件（1C p29）的 Task environment 例子表**（背熟，考试直接问 "identify the properties"）：

| Task environment | Observable | Agents | Deterministic | Episodic | Static | Discrete |
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

容易错的：**Backgammon** fully observable 但 **stochastic**（掷骰子）；**Image analysis** 是 **semi**-dynamic；**Part-picking robot** 是 **episodic**（每个零件独立判断）；**English tutor** 是 **multi**agent（学生也是 agent）。

**Multiagent 再细分**（Jan 2026 Q3a(i) 考 2 分：chess game tree 属于哪种 multiagent）：

- **Competitive**：一方得益 = 另一方损失。例：**chess**（→ 答案：competitive multiagent environment）。
- **Cooperative / collaborative**：一起合作产生想要的结果，大家都得到奖励。例：多机器人救援。
- **Partially both**：同时竞争又合作（多个 performance measure）。例：taxi driving（避免相撞 = 合作；抢车位 = 竞争）、soccer（同队合作、对队竞争）。

**判断"某实体是不是 agent"**：看 B 的行为是不是**在最大化一个受 A 行为影响的 performance measure**。

**最难的环境**：partially observable, multiagent, non-deterministic, sequential, dynamic, continuous, unknown（例：taxi driving 几乎全中）。

📝 **例：Chess（with a clock）环境属性**：fully observable (sees whole board), multiagent – competitive (two players), deterministic (no chance), sequential (every move affects future), semi-dynamic (board doesn't change while thinking, but clock reduces score/time), discrete (finite positions and moves), known (rules known).

---

## Part 5：Agent Program —— 如何写出"小而聪明"的程序

**Agent = Architecture + Program**。Architecture（硬件）把 sensor 的 percepts 交给 program、执行 program、把 action 送到 actuators。

### 5.1 最笨的方法：Table-driven agent

课件 1C p32 的 pseudocode（**persistent** = 在多次调用之间保留的变量）：

```
function TABLE-DRIVEN-AGENT(percept) returns an action
    persistent: percepts, a sequence, initially empty
                table, a table of actions, indexed by percept sequences, initially fully specified

    append percept to the end of percepts
    action ← LOOKUP(percepts, table)
    return action
```

它**每次把新的 percept 接到整段历史后面，再用整段历史去查表**（表就是 1B 的 vacuum agent function 表：[A, Clean] → Right、[A, Dirty] → Suck …）。
它确实做到了我们要的事——**但它是好的程序吗？** 不是。设 P = 可能的 percept 集合，T = agent 寿命，表的项数：

```
 T
 Σ  |P|^t        （t = 1 到 T 的总和，天文数字）
t=1
```

问题：① 这么大的表**存不下**；② **建表要花太多时间**；③ agent **无法从经验中学习**（表是设计者事先写死的）。
挑战：**写出小程序，也能产生理性行为**。于是有了 4 种基本 agent program（+ learning）。

### 5.2 四种 agent（一个比一个聪明，每一个都解决前一个的缺点）

> 📌 考试常要 "with the use of the schematic diagram, explain how the agent makes decisions"。下面每种 agent 都给出**课件的方框图**（照着画）+ **pseudocode** + 一段英文决策流程。方框图里：**长方形 = agent 当下推出的信息/决策**；**圆括号（课件是椭圆）= agent 拥有的背景知识**。

---

**① Simple reflex agent**

- 只看**当前 percept**，**忽略其余 percept history**；用 **condition–action rules**（又叫 situation–action rules / if-then rules）。

课件的 vacuum 版本（1B p13 / 1C p36）：

```
function REFLEX-VACUUM-AGENT([location, status]) returns an action
    if status = Dirty then return Suck
    else if location = A then return Right
    else if location = B then return Left
```

为什么小？它不看历史 → 要考虑的可能性从 **4^T 降到 4**（location 2 种 × status 2 种）。

课件的通用版本（1C p38）：

```
function SIMPLE-REFLEX-AGENT(percept) returns an action
    persistent: rules, a set of condition–action rules

    state  ← INTERPRET-INPUT(percept)
    rule   ← RULE-MATCH(state, rules)
    action ← rule.ACTION
    return action
```
- **INTERPRET-INPUT**：从 percept 产生对**当前 state 的抽象描述**。
- **RULE-MATCH**：返回规则集中**第一条**与该 state 描述相符的规则。

方框图（1C p39）：

```
 +---------------------- Agent ----------------------+     +-------------+
 |                               Sensors <-----------+-----|             |
 |                                  |                |     |             |
 |                                  v                |     |             |
 |                     [ What the world is like now ]|     |             |
 |                                  |                |     | Environment |
 |                                  v                |     |             |
 |  (Condition-action rules) --> [ What action I     |     |             |
 |                                 should do now ]   |     |             |
 |                                  |                |     |             |
 |                                  v                |     |             |
 |                              Actuators -----------+---->|             |
 +---------------------------------------------------+     +-------------+
```

📝 **How it decides**：The sensors give the current percept → the agent interprets it into "what the world is like now" → it matches this description against its **condition–action rules** → the first matching rule gives "what action I should do now" → the actuators perform it. No memory of past percepts is used.

- ✅ **Pros**：easy to implement（简单、程序小）。
- ❌ **Cons**：only works well if the environment is **fully observable**；例：没有 location sensor、只有 dirt sensor 的 vacuum agent 表现很差；容易陷入 **infinite loop**（在 A 格一直 "Left" 撞墙）。**Randomized** simple reflex agent（随机选 Left/Right）会比它好。

→ **但是**：环境只能部分观察时怎么办？（课件 p41 的图：前车挡住了后面那辆车——你看不见它，但知道它还在。）

---

**② Model-based reflex agent**

- 解决方法：**记住现在看不到的那部分世界**。维持一个 **internal state**（取决于 percept history），反映当前 state 中未被观察到的部分，并**不时更新**。
- 程序里要编入两种知识：
  - **Sensor model**：世界的状态如何反映在 agent 的 percepts 上。
  - **Transition model**：世界如何随时间改变——(a) **How the world evolves**（不受 agent 影响的变化）；(b) **What my actions do**（agent 动作造成的变化）。

```
function MODEL-BASED-REFLEX-AGENT(percept) returns an action
    persistent: state, the agent's current conception of the world state
                transition_model, how the next state depends on the current state and action
                sensor_model, how the current world state is reflected in the agent's percepts
                rules, a set of condition–action rules
                action, the most recent action, initially none

    state  ← UPDATE-STATE(state, action, percept, transition_model, sensor_model)
    rule   ← RULE-MATCH(state, rules)
    action ← rule.ACTION
    return action
```
- **UPDATE-STATE**：产生新的 internal state 描述，告诉 agent **"What the world is like now"**。

方框图（1C p45）：

```
 +------------------------- Agent --------------------------+     +-------------+
 |   (State) <- - - - - - - - - - - - - - +                 |     |             |
 |      |                                 :    Sensors <----+-----|             |
 |      +---------------------------+     :       |         |     |             |
 |  (How the world evolves) --------+--> [ What the world   |     |             |
 |  (What my actions do) -----------+      is like now ]    |     | Environment |
 |                                             |            |     |             |
 |                                             v            |     |             |
 |  (Condition-action rules) ----------> [ What action I    |     |             |
 |                                         should do now ]  |     |             |
 |                                             |            |     |             |
 |                                             v            |     |             |
 |                                         Actuators -------+---->|             |
 +----------------------------------------------------------+     +-------------+
   (虚线：新推出的 "what the world is like now" 回存为下一轮的 State)
```

📝 **How it decides**：The agent combines the new percept with its **internal state** (memory of the past), using its model of **how the world evolves** and **what its actions do**, to update its description of "what the world is like now" — including parts it cannot currently see. It then applies **condition–action rules** to that updated state to choose the action.

- ❌ **Limitation**：internal state 只能代表 agent 的 **best guess**——在 partially observable 环境里仍无法**确切**知道当前 state，还是要在不确定下做决定；而且**没有 goal** 描述什么情况是想要的，当某个 state 下有**多个动作可做**时，agent 不知道该选哪个。

→ **但是**：它不知道自己"要去哪里"。

---

**③ Goal-based agent**

- 除了追踪 world state，还记录一组 **goals**（描述**想要的情况**），选择**（最终）能达成目标**的动作。多了一个问题："**What it will be like if I do action A?**"（预测未来）→ 需要 **search / planning**（Ch2）。

方框图（1C p48）：

```
 +------------------------- Agent --------------------------+     +-------------+
 |   (State) <- - - - - - - - - - - - - - +                 |     |             |
 |                                        :    Sensors <----+-----|             |
 |  (How the world evolves) -----> [ What the world is      |     |             |
 |  (What my actions do) ---+        like now ]             |     |             |
 |                          |              |                |     |             |
 |                          +-----> [ What it will be like  |     | Environment |
 |                                    if I do action A ]    |     |             |
 |                                         |                |     |             |
 |  (Goals) ----------------------> [ What action I         |     |             |
 |                                    should do now ]       |     |             |
 |                                         |                |     |             |
 |                                         v                |     |             |
 |                                     Actuators -----------+---->|             |
 +----------------------------------------------------------+     +-------------+
```

📝 **How it decides**：Like the model-based agent, it keeps track of the world state. It then **predicts the result of each possible action** ("what it will be like if I do action A") using its model, compares these predicted states with its **goals**, and chooses an action (or a sequence of actions found by search/planning) that will eventually achieve a goal.

| | Goal-based agents | Reflex agents |
|---|---|---|
| Decision making | **Reasoning**（预测未来、规划） | **Reflection**（条件反射） |
| Adaptability | **Higher**（换目标即可，不用重写规则） | Lower |

- ❌ **Limitation**：goal 只能给 **binary** 区分（达成 / 未达成）；当不确定**哪一串 world states 更令人满意**时，agent 仍然要做决定，但 goal 无法比较"多好"。

→ **但是**：去同一个目的地，有快有慢、有安全有危险，goal 分不出来。

---

**④ Utility-based agent**

- **Utility function**：按"**how happy they would make the agent**"给不同 world states 打分。
  - Utility function = **internal** performance measure；performance measure = **external**。
  - 两者**一致**时，选择最大化 utility 的动作的 agent 就是 rational。
- 选择带来 **best expected utility** 的动作：对所有可能结果状态，按**结果的概率加权平均**。

方框图（1C p51）——和 goal-based 一样，但把 "Goals" 换成 "Utility"，并多一格 "How happy I will be in such a state"：

```
 +------------------------- Agent --------------------------+     +-------------+
 |   (State) <- - - - - - - - - - - - - - +                 |     |             |
 |                                        :    Sensors <----+-----|             |
 |  (How the world evolves) -----> [ What the world is      |     |             |
 |  (What my actions do) ---+        like now ]             |     |             |
 |                          |              |                |     |             |
 |                          +-----> [ What it will be like  |     |             |
 |                                    if I do action A ]    |     | Environment |
 |                                         |                |     |             |
 |  (Utility) --------------------> [ How happy I will be   |     |             |
 |                                    in such a state ]     |     |             |
 |                                         |                |     |             |
 |                                  [ What action I         |     |             |
 |                                    should do now ]       |     |             |
 |                                         |                |     |             |
 |                                         v                |     |             |
 |                                     Actuators -----------+---->|             |
 +----------------------------------------------------------+     +-------------+
```

📝 **How it decides**：It tracks the world state and predicts the outcome of each action, then uses its **utility function** to score "how happy I will be in such a state". Because outcomes are uncertain, it chooses the action with the **highest expected utility** — the average utility of all possible outcome states, weighted by their probabilities.

**Utility-based vs goal-based（课件 1C 表）**：Can a rational decision be made when…

| Situation | Utility-based | Goal-based |
|---|---|---|
| There is **more than one goal** to be achieved | Yes | No |
| There are **conflicting goals**（例：速度 vs 安全） | Yes | No |
| The environment is **uncertain** (partially observable) | Yes | No |

- ❌ **Challenges**：agent 要为复杂环境建模并追踪它（需要 perception、representation、reasoning、learning 的大量研究）；utility function 需要**有效率的算法**，计算复杂度太高就不实际。

---

**⑤ Learning agent**（任何一种 agent 都可以做成 learning agent；Turing 1950 就提出"造会学习的机器，再教它"）

能学习是竞争优势：可以在**一开始未知的环境**里运作，并变得比它的初始知识**更有能力**。

方框图（1C p56）：

```
                 Performance standard
                         |
 +-----------------------|------ Agent ----------------------+     +-------------+
 |                       v                                   |     |             |
 |                  [ Critic ] <------------- Sensors <------+-----|             |
 |                       |                       |           |     |             |
 |                       | feedback              v           |     |             |
 |                       v        changes                    |     | Environment |
 |               [ Learning   ] -----------> [ Performance ] |     |             |
 |               [ element    ] <----------- [ element     ] |     |             |
 |                       |       knowledge        ^    |     |     |             |
 |                       | learning goals         |    v     |     |             |
 |                       v                        | Actuators+---->|             |
 |               [ Problem    ] ------------------+          |     |             |
 |               [ generator  ]                              |     |             |
 +-----------------------------------------------------------+     +-------------+
```

箭头要记：**Performance standard → Critic**；**Sensors → Critic** 和 **→ Performance element**；**Critic →(feedback)→ Learning element**；**Learning element →(changes)→ Performance element**，**Performance element →(knowledge)→ Learning element**；**Learning element →(learning goals)→ Problem generator**；**Problem generator → Performance element**（建议探索性的动作）；**Performance element → Actuators**。

| Component | 职责 | Automated taxi 例子（课件） |
|---|---|---|
| **Performance element** (the agent) | Responsible for **selecting external actions** | 出租车用来选择驾驶动作的知识与程序 |
| **Critic** | **Evaluates** the agent's behaviour with respect to a **fixed performance standard**, gives feedback | 观察世界的变化（例：急转弯后别的司机猛按喇叭），按固定标准把 feedback 给 learning element |
| **Learning element** | Responsible for **making improvements** | 根据 feedback **修改** performance element（"下次不要那样急转弯"） |
| **Problem generator** | **Suggests actions that lead to new experiences** | 建议在某些行为上做"实验"（例：在不同路面试刹车）以进一步改进 |

📝 **Learning vs non-learning agent（3 differences）**：(1) learns from past experience vs only follows fixed predefined rules; (2) adapts when the environment changes vs cannot adapt; (3) performance improves over time vs performance stays the same (and can work in initially unknown environments).

**比较题（tutorial Q2b）一句话答案：**

| Pair | 较适合 | 理由 |
|---|---|---|
| Table-driven vs Simple reflex | Simple reflex | 不必存巨大的表，只用少量 if-then 规则 |
| Simple reflex vs Model-based | Model-based | 有 internal state，可处理 partially observable 环境 |
| Model-based vs Goal-based | Goal-based | 有目标，可规划、可在多个可行动作中选择，更灵活 |
| Goal-based vs Utility-based | Utility-based | 能比较"多好"，处理多目标、冲突目标与不确定性 |

---

## Part 6：环境状态的表示（Representation）

Agent 内部的模型可以用三种方式表示（表达力递增）：

| | 描述 | 例子（开车从 B 城到 C 城） |
|---|---|---|
| **Atomic** | 每个 state 是**不可分割的黑盒子**，没有内部结构 | 状态就是 "B"、"C" —— 用于 search（Ch2–4） |
| **Factored** | 每个 state 拆成**固定的一组 variables/attributes**，各有值 | 位置 GPS、油量、过路费……—— 用于 CSP（Ch5） |
| **Structured** | state 包含 **objects**、它们的属性以及**彼此的关系** | "前面一辆卡车正倒车进入奶牛场，但一头走失的牛挡住了它" |

---

## Closing the loop

回到 SmartCar 的会议：四个人代表四种 AI 路线，而课程选择的是你那一条——**acting rationally**。
要造一个 rational 的 SmartCar，我们要：用 **PEAS** 描述它的任务环境 → 判断环境属性（partially observable、multiagent、stochastic、sequential、dynamic、continuous，最难的那种）→ 选择合适的 agent program（至少要 model-based，最好 utility-based + learning）。

但 SmartCar 最基本的一件事——"从 A 站开到 H 站该走哪条路"——还没解决。这就是一个 **goal-based agent** 要做的 **search**，也就是 Chapter 2。

---

## ⚠️ Where the slides mislead

| Slide | 课件写法 | 更准确的理解 |
|---|---|---|
| 1A Rational Agent | "agent" originates from Latin "agree" | 是 **agere**（to do）。拼写错误。 |
| 1C Deterministic 表格 | "Any action has a single guaranteed effect: No / Yes" 与 "Need to deal with uncertainty" 两行错位 | Deterministic：每个动作只有一个确定结果（Yes），不需处理不确定性（No）；Stochastic 相反。 |
| 1B Example #2–#5 | 只提问、不给答案 | 见 Part 3.3：先指出是哪一个 criterion 改变，再推论。 |

---

## Exam radar

| Paper | 题目 | 分数 |
|---|---|---|
| Oct 2025 Q1 | 4 approaches (8) · Turing Test 另一个名字 (1) · Total Turing Test 6 capabilities + purpose (12) · rationality 4 criteria (4) | **25** |
| Jan 2026 Q1 | 4 approaches (8) · Total vs Turing (2) · Meta AI 能否通过 Turing / Total Turing (3+3) · 哪个更 relevant (3) · define agent (2) · 4 criteria (4) | **25** |
| Jan 2026 Q3a(i) | chess game tree 是哪种 multiagent environment | 2 |
| May 2026 Q2a–c | 4 approaches 名称 (4) · perception vs action (4) · PEAS 全名 + SmartCar PEAS (6) | **14** |

👉 结论：**4 approaches 三次都考；4 criteria 考两次；Turing / Total Turing 考两次；PEAS 考一次**。这些必须能默写。

### 📝 Jan 2026 Q1b：Meta AI（完整答案）

**(i) Total Turing Test vs Turing Test（2 分）**
> The Turing Test only checks whether a computer can hold a written (text) conversation that is indistinguishable from a human's, with no physical interaction. The Total Turing Test (Harnad, 1991) adds two requirements: **perceptual ability** (e.g. computer vision through a video signal) and **object manipulation ability** (robotics), so the machine must also see and physically act like a human.

**(ii) Can Meta AI pass the Turing Test?（1+2 分）**
> **Yes (likely).** Meta AI has natural language processing (it chats with users in human language), knowledge representation (it stores and answers questions), automated reasoning (it gives suggestions and draws conclusions) and machine learning (it adapts to users' requests). Through text chat, an interrogator could find it difficult to distinguish its responses from a human's.

**(iii) Can Meta AI pass the Total Turing Test?（1+2 分）**
> **No.** Although it can create and analyse images, it has no robotic body, so it lacks the **robotics** capability to manipulate objects and move about, and it cannot perceive the physical world through its own senses in real time. The Total Turing Test requires both perception and object manipulation.

**(iv) Which is more relevant to the definition of AI?（1+2 分）** —— 选一个、理由写好就有分：
> **The Turing Test.** The question defines AI as simulating human intelligence – to *think, learn and make decisions*. These are cognitive abilities that the Turing Test measures through conversation (NLP, knowledge representation, reasoning, learning); a physical body (robotics) is not required for intelligence itself.
>
> （另一种写法：选 Total Turing Test，因为它测试完整的人类能力——感知 + 行动 + 思考，是更强的 benchmark。）

---

## Cheat sheet

| 主题 | 要点 |
|---|---|
| 2 dimensions | Human vs Rational × Thinking vs Acting |
| 4 approaches | Acting Humanly = Turing Test · Thinking Humanly = Cognitive Modelling · Thinking Rationally = Laws of Thought · Acting Rationally = Rational Agent |
| Turing Test | Turing 1950, **imitation game**, computer + human respondent + interrogator, written questions, no physical contact |
| Total Turing Test | Harnad 1991, + perception + object manipulation |
| 6 capabilities | NLP, knowledge representation, automated reasoning, machine learning, computer vision, robotics |
| Cognitive modelling 3 ways | introspection, psychological experiments, brain imaging |
| Laws of thought | logic, syllogism (2 premises + conclusion) |
| Agent | perceives via sensors, acts via actuators |
| Interaction | perception (passive, no change) vs action (active, changes env) |
| Agent function vs program | abstract mapping vs concrete implementation |
| Rationality 4 criteria | performance measure, prior knowledge, actions, percept sequence |
| Rational agent | maximizes **expected** performance given percepts + built-in knowledge |
| Rational vs omniscient | expected outcome vs actual outcome |
| 3 capabilities | information gathering, learning, autonomy |
| PEAS | Performance, Environment, Actuators, Sensors |
| 7 env dimensions | observable, agents, deterministic, episodic, static, discrete, known |
| Agent types | simple reflex → model-based → goal-based → utility-based (+ learning) |
| Learning components | performance element, critic, learning element, problem generator |
| Representation | atomic → factored → structured |

---

## Practice (answers included)

### A. MCQ

1. Which approach is known as the "Laws of Thought" approach?
   (a) Acting Humanly (b) Thinking Humanly (c) Thinking Rationally (d) Acting Rationally
2. Which two capabilities are needed for the Total Turing Test but not the Turing Test?
   (a) NLP & reasoning (b) Computer vision & robotics (c) Learning & knowledge representation (d) Reasoning & robotics
3. Chess played **with a clock** is:
   (a) static (b) dynamic (c) semi-dynamic (d) continuous
4. Which agent can handle conflicting goals such as speed vs safety?
   (a) Simple reflex (b) Model-based reflex (c) Goal-based (d) Utility-based
5. The component of a learning agent that suggests exploratory actions is the:
   (a) critic (b) learning element (c) problem generator (d) performance element

**Answers**：1 (c) · 2 (b) · 3 (c) 棋盘不动但时间在扣分 · 4 (d) · 5 (c)

### B. Short answer

**B1.** Differentiate a rational agent from an omniscient agent. (4 marks)
> A rational agent does not know the actual outcome of its actions, acts under uncertainty most of the time, and maximizes its **expected** performance based on its percept sequence to date. An omniscient agent knows the actual outcome of its actions, acts under certainty, and achieves the best **actual** outcome. Omniscience is impossible in reality, so rationality does not require it.

**B2.** Explain why a performance measure should be designed according to what one wants in the environment, not how the agent should behave. (3 marks)
> Because a rational agent will do exactly what maximizes the measure. E.g. if a vacuum agent is rewarded for the *amount of dirt sucked up*, it could dump dirt and suck it up again repeatedly. Rewarding *clean squares per time step* describes the desired environment state instead.

**B3.** A simple reflex vacuum agent loses its location sensor. What problem occurs and how can it be solved? (4 marks)
> It only perceives [Dirty]/[Clean]. With the rule "if clean then move Left", when it is already in the leftmost square it moves Left forever → **infinite loop**; the environment is now partially observable. Solutions: **randomize** the action (e.g. flip a coin to go Left/Right), or use a **model-based reflex agent** that keeps an internal state of where it has been.

### C. Scenario (environment properties)

**C1.** An online poker bot. Identify the properties of its environment and justify.
> - **Partially observable** – it cannot see the opponents' cards.
> - **Multiagent (competitive)** – other players try to win its money.
> - **Stochastic** – the cards dealt are random.
> - **Sequential** – betting now affects later rounds.
> - **Static** (turn-based; nothing changes while it thinks) — semi-dynamic if there is a timer.
> - **Discrete** – finite cards and betting actions.
> - **Known** – the rules of poker are known.

**C2.** An X-ray image defect classifier on an assembly line.
> Fully observable (whole image available), single-agent, deterministic, **episodic** (each item is judged independently), static, continuous (pixel intensities) — tutorial 也接受 discrete if the image is treated as a finite pixel grid; justify either way. Known.

### D. Thinking

**D1.** Is it possible for a simple reflex agent to be perfectly rational? Explain.
> Yes, **if the environment is fully observable** and the correct action depends only on the current percept (e.g. the two-square vacuum world with location and dirt sensors). In partially observable environments it usually cannot be rational, because the right action depends on things it cannot currently see.

**D2.** Why is the Rational Agent approach "more practical" than Acting Humanly?
> Human behaviour is hard to model mathematically, so "act like a human" is a vague, possibly unachievable target. Rationality has a clear mathematical definition (maximize expected performance measure), so it can be designed, tested and proven. It is also more general than thinking rationally, because correct inference is only one way to act rationally.
