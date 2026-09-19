# AMIS1012 — Chapter 7: Software Development

> This is the shortest chapter, but it has the densest cluster of definition errors: "scalable" is defined as portability, black-box testing says "any" where it should say "all", and QA is blurred with QC and testing. This note explains the ideas, runs a small testing demo (real output pasted below) that shows why "100% statement coverage" is not enough, and lists what the slides get wrong. Items marked **[extra]** are not from the slides and were not source-checked; the code output was actually run.

---

## 0. One-sentence overview

Good software comes from a disciplined development method, systematic testing and a quality assurance process, and the ethical reason is that defective software harms users and exposes the developer to liability.

| Topic | Slides |
|---|---|
| 1. Software development methodology (Agile, Waterfall, cost of defects, liability) | 3–9 |
| 2. Software testing (manual, automation, dynamic, black-box, white-box) | 10–15 |
| 3. Quality assurance and standards (PDCA) | 16–20 |
| 4. Software quality and assurance techniques | 21–25 |

---

## 1. Software development methodology (slides 3–9)

A **methodology** is a tried-and-true work procedure that helps analysts, designers and project managers produce high-quality software in an orderly way. It describes the tasks in each phase and who is responsible. A **technique** is a specific way to carry out one task, e.g. recording program logic in a **flowchart**.

### Agile vs Waterfall (slides 4–6; diagram on slide 4)

| | Agile | Waterfall |
|---|---|---|
| Approach | Flexible, iterative | Traditional, linear |
| Structure | Small portions delivered repeatedly (plan → design → develop → test → deploy → review, as a loop) | Strict sequence of phases, each finished before the next |
| Change | Welcomes change; adjusts to client feedback | Little room to revisit earlier phases |
| Delivery | Working increments delivered rapidly and continuously | Product delivered at the end |
| Best when | Requirements are uncertain or evolving | Requirements are well defined and change is unlikely or costly |

⚠️ **Phases differ between the text and the figure.** Slide 6's text lists six waterfall phases (requirements, design, implementation, testing, deployment, maintenance); slide 4's diagram shows five (analysis, design, implementation, testing, maintenance). In the exam list the slide 6 version; mention that different books merge or rename phases.

### Cost of finding defects late (slides 7–9)

Slide 7: finding and fixing a defect at the **requirements** stage costs **up to 100 times less** than fixing it after the software has shipped. Why (slide 8): a flaw found later means **rework** of everything built on it, plus higher costs of **communicating** and **correcting** the mistake. Hence engineers try to find mistakes early, both to save money and to raise quality.

Illustration (my own numbers, **[extra]**): if a requirements error costs RM100 to fix on paper, it may cost RM1,000 when coded, RM2,000 in testing and RM10,000 after shipping (100×).

⚠️ "Up to 100 times" is a widely quoted rule of thumb, not an exact law; the ratio varies by project and by method (Agile tries to lower late-change costs). Say "can be much higher".

**Ethics link (slide 9):** flawed products that harm consumers can lead to **warranty lawsuits**; failing to design applications carefully and reliably creates significant **liability exposure**.

---

## 2. Software testing (slides 10–15)

**Software testing** = evaluating a program's functionality to see whether it meets the required specifications and to find bugs, so a better product is delivered.

### Types on the slides

| Type | Meaning |
|---|---|
| **Manual testing** | People test the software: check functions listed in the specification and try it from the end customer's point of view |
| **Automation testing** | Tools run test scripts and produce results automatically |
| **Dynamic testing** | Testing by **running** the code with test data and comparing actual with expected results; has two kinds: black-box and white-box |

### Black-box testing (slide 14)

The tester treats the unit as a box with known **inputs and expected outputs** but unknown inner workings. The tester needs no knowledge of the code, so it is often done by someone other than the author (giving an independent view).

⚠️ **Slide 14 error.** "The unit passes the test if it exhibits the predicted behaviours with **any** of the input data". A unit passes only if it behaves correctly for **all** the test data. One failing case is enough to fail.

### White-box testing (slide 15)

The tester knows the code's logic and designs test data to exercise it. The slide says the tester tests "all feasible logic pathways" and "each program statement must be executed at least once".

⚠️ **Simplification.** Executing every statement (**statement coverage**) is only a *minimum*. Testing every possible path is usually impossible, because the number of paths grows very fast. Better coverage goals: **branch coverage** (every decision taken both ways). **[extra]** Other terms not on the slides: *static testing* (reviewing code without running it), and testing levels (unit, integration, system, acceptance).

### Worked demo: why statement coverage is not enough (real output)

Requirement: base shipping fee RM5; express adds RM10; weight over 20 kg adds RM8 **whether or not** express is chosen.

```python
def buggy_shipping_v2(weight_kg, express):
    fee = 5
    if express:
        fee += 10
        if weight_kg > 20:      # BUG: heavy surcharge only applied inside the express branch
            fee += 8
    return fee
```

**Suite A — one test** `(25 kg, express)` expected 23 → runs **every statement** (100% statement coverage):

```
((25, True), expected 23, got 23, PASS)
```

The bug is missed. **Suite B — four tests** (both outcomes of both decisions, i.e. branch coverage):

```
((25, True),  expected 23, got 23, PASS)
((25, False), expected 13, got 5,  FAIL)   <-- bug found
((10, True),  expected 15, got 15, PASS)
((10, False), expected 5,  got 5,  PASS)
```

The correct version passes all four. **Lesson:** 100% statement coverage can still miss a bug; the failing case was a heavy parcel with no express option.

### Why "test all paths" is unrealistic (computed)

With *n* independent if-statements in a row there are 2ⁿ paths:

| n | Paths |
|---|---|
| 1 | 2 |
| 5 | 32 |
| 10 | 1,024 |
| 20 | 1,048,576 |
| 30 | 1,073,741,824 |

**[extra]** This is why testing can show that bugs exist but cannot prove none remain.

---

## 3. Quality assurance and standards (slides 16–20)

**Quality** is hard to define; the slide summarises it as **"fit for use or purpose"**: meeting customers' needs and desires for functionality, style, efficiency, longevity and price (slide 16 misprints "desires and desires").

**Quality assurance (QA)** = the approaches used *during production* to ensure a product's consistent service; concerned with making the development **process** dependable and competitive while meeting quality standards. **Assurance** = a confident statement that inspires confidence that a product or service can perform well.

⚠️ **QA vs QC vs testing (slides 16–17).** The slides say "software testing QA is defined as a method for assuring quality of software" and also that assurance "ensures that the product will perform flawlessly". Two cautions:

| Term | Focus | Question it answers |
|---|---|---|
| **QA** [extra] | The **process** (prevent defects) | "Are we building it the right way?" |
| **QC / testing** [extra] | The **product** (detect defects) | "Does this product have defects?" |

And QA cannot guarantee "flawless": it reduces defects and risk; it does not eliminate them.

### PDCA / Deming cycle (slide 19 diagram)

A repeated four-stage cycle used to evaluate and improve operations:

| Stage | What happens |
|---|---|
| **Plan** | Set process-related objectives and the processes needed for a high-quality result |
| **Do** | Implement the plan; develop and test processes; make system changes |
| **Check** | Monitor and check whether the procedures meet their objectives |
| **Act** | Take the measures needed to improve processes (the slide says a QA tester may do this) |

Then the cycle starts again with a new Plan. Example (own): Plan: reduce login-page defects by 50% via code reviews. Do: introduce reviews. Check: count defects after a month. Act: keep reviews, add checklists, set a new target.

**Purpose of QA (slide 20):** verify the product is developed and delivered properly, reducing the number of problems and faults in the final product.

⚠️ **Heading vs content.** The section is titled "Quality assurance **and standards**" but the slides name no standards. **[extra, not checked]** Typical examples: ISO 9001 (quality management) and ISO/IEC 25010 (software product quality). Chapter 6 covers ISO 27001 for security.

---

## 4. Software quality and assurance techniques (slides 21–25)

A high-quality product meets customers' expectations, commonly measured against the **Software Requirements Specification (SRS)**. The slides list quality attributes:

| Attribute | Slide's meaning | Correct note |
|---|---|---|
| **Scalable** | "Able to operate on a range of operating systems, on various computers, or with other software devices" | ⚠️ That is **portability** (and compatibility). *Scalability* = ability to handle growing load (more users or data) without breaking |
| **Usability** | All types of consumers can conveniently use the system's features | OK |
| **Reusability** | Components can easily be reused to make new applications | OK |
| **Correctness** | The SRS specifications have been applied properly | OK |
| **Maintainability** | Bugs can be fixed easily, new tasks added, functions changed | OK |

**[extra]** Other common attributes: reliability, efficiency, security, portability.

Slide 22's heading says "techniques" but lists **attributes**. Techniques would be reviews, inspections, testing.

### Quality system (slides 24–25)

- A **quality control scheme** helps produce high-quality goods. The whole organisation is responsible for it; there may be several quality departments; **top management must approve** the scheme (otherwise staff take it negatively).
- Functions of the quality system: **project auditing**; **quality system review**; developing principles, procedures and protocols; producing publications for senior management on how well the quality system works.

---

## ⚠️ Where the slides mislead

| Slide | Says | Better understanding |
|---|---|---|
| 4 vs 6 | Waterfall has 5 phases (figure) vs 6 (text) | Lists vary; know slide 6 |
| 7 | Up to 100× cheaper to fix early | Rule of thumb, not exact |
| 14 | Passes "with any of the input data" | Must pass **all** test cases |
| 15 | Test all logic paths / each statement once | Statement coverage is a minimum; all-paths is impractical |
| 16 | "desires and desires" | Needs and desires |
| 17 | QA "ensures … flawlessly"; "software testing QA" | QA reduces defects; testing is part of QC |
| 22 | "Scalable" = works on different systems | That is portability |
| 22 | Heading "techniques" | Lists attributes |

**Exam strategy:** if asked to define *scalable*, give the slide's meaning if the question quotes it, but write "(usually called portability; scalability is handling growth)".

---

## Cheat sheet

| Item | Remember |
|---|---|
| Methodology vs technique | Whole procedure vs a specific way to do a task |
| Agile / Waterfall | Iterative, flexible / linear, phase-by-phase |
| Early defects | Cheaper to fix; up to ~100× in the slide |
| Manual / automation / dynamic | People run tests / tools run scripts / run code with data |
| Black-box / white-box | Inputs and outputs only / code logic known |
| Statement vs branch coverage | Each line run / each decision both ways |
| QA | Process-focused; PDCA |
| PDCA | Plan, Do, Check, Act |
| Attributes | Scalable*, usability, reusability, correctness, maintainability (*slide's meaning is portability) |
| SRS | Software Requirements Specification |

---

## Practice

### A. Multiple choice

**A1.** Which method suits a project with clearly defined, stable requirements?
(a) Agile (b) Waterfall (c) Neither (d) Both equally

**A2.** In black-box testing the tester:
(a) Reads the code (b) Knows inputs and expected outputs but not the internals (c) Tests only after shipping (d) Tests statement coverage

**A3.** Which stage of PDCA compares results with objectives?
(a) Plan (b) Do (c) Check (d) Act

**A4.** Which describes *maintainability*?
(a) Works on many operating systems (b) Bugs are easy to fix and features easy to change (c) Handles many more users (d) Meets the SRS

**A5.** A test suite that executes every statement at least once achieves:
(a) Branch coverage (b) Path coverage (c) Statement coverage (d) Proof of no bugs

### B. Short answer

**B1.** Give two reasons finding defects early is cheaper (slide 8).
**B2.** Explain the difference between black-box and white-box testing.
**B3.** State what the four PDCA stages do.

### C. Calculation / trace

**C1.** Using the demo function `buggy_shipping_v2`, trace `(weight = 30, express = False)`: start fee = 5; is `express` true? ... What does it return, and what should the specification give?
**C2.** A program has 12 independent if-statements in sequence. How many paths are there? How many tests are needed for branch coverage at the very least (each decision both ways)?
**C3.** A requirements defect costs RM200 to fix during requirements. Using the slide's "up to 100 times", what is the maximum cost after shipping?

### D. Thinking

**D1.** Slide 17 says QA "ensures the product will perform flawlessly". Why is that too strong?
**D2.** Explain why a developer can face legal liability for poor design (slide 9) and link it to ethics.

---

## Answers

**A1.** (b) Waterfall.
**A2.** (b).
**A3.** (c) Check.
**A4.** (b). (a) is portability; (c) scalability; (d) correctness.
**A5.** (c).

**B1.** Later discovery needs rework of earlier deliverables, and costs of communicating and correcting the mistake are higher.
**B2.** Black-box: tests inputs against expected outputs without knowing the code, often by someone other than the author. White-box: tester knows the internal logic and designs test data to exercise it.
**B3.** Plan: set objectives and processes. Do: implement and test. Check: monitor against objectives. Act: improve the process.

**C1.** fee = 5; express is False so the `if express` block (including the weight check) is skipped; returns **5**. The specification says the heavy surcharge applies regardless: 5 + 8 = **13**. This is the bug the demo found.
**C2.** 2¹² = **4,096** paths. Branch coverage needs each decision to be true at least once and false at least once; at minimum **2** tests can achieve this for a chain of independent ifs (one test taking all-true, one taking all-false) — although real suites use more to cover combinations. (Note: fewer tests than paths, which is why branch coverage is practical.)
**C3.** 200 × 100 = **RM20,000**.

**D1.** Testing and QA can only reduce and detect defects; they cannot prove absence of bugs (the number of possible paths and inputs is enormous), so "flawlessly" overpromises.
**D2.** If a design flaw causes damage, the developer can face warranty lawsuits and liability. Ethically, professionals owe users reliable products; cutting corners on design or testing to save cost or time puts users at risk.

---

## Links to other chapters

- Ch1: professional responsibility and codes.
- Ch4: Whistleblowing on safety defects; ICT code of conduct.
- Ch6: SDLC policy; risk assessment for software risks; the pillar "reliability".
- Ch8: licensing and open source used in software development.
