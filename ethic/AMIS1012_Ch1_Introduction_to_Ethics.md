# AMIS1012 — Chapter 1: Introduction to Ethics

> The slides list many definitions but rarely say *why* they matter or show how to apply them. This note adds worked examples (an ethical decision trace, a private-vs-confidential sorting exercise), explains the two figures the text extraction misses (piracy map, ethics/morals/law Venn diagram) and flags the few places where the slides are loose. Items marked **[extra]** are not from the slides.

---

## 0. One-sentence overview

Ethics is the shared set of standards a society or profession uses to decide what behaviour is acceptable; this chapter shows how to make ethical decisions, why IT raises special ethical issues, what is expected of IT professionals, and how codes and certifications support ethical practice.

| Topic | Slides |
|---|---|
| Definition of ethics; virtues and vices | 3–6 |
| Ethical decision making (5-step process) | 7–9 |
| Morals vs ethics vs laws | 10–12 |
| Why ethics matters in IT (scenarios of public concern) | 13–19 |
| Ethics for IT professionals (qualities, codes, 7 trends) | 20–29 |
| Common ethical issues for IT users | 30–34 |
| Certifications | 35–40 |

---

## 1. What is ethics? (slides 3–6)

**Plain-language version.** Ethics answers "how should we behave when others are affected?" It is *shared* — a society, an institution or a profession agrees on the standard — which is why the slides define it as "a set of values that define what is and is not acceptable behaviour in a certain society".

- **Computer ethics** = the same idea applied to computers: guidelines for the morally acceptable use of computers.
- Some standards are almost universal (lying and stealing are wrong); others differ between cultures.
- **Virtue** = a habit that pushes you to do right (fairness, honesty). **Vice** = a habit that pushes you to do wrong (envy, rage). The slide says "sin" in one bullet and "vices" in the next; treat them as the same idea for exam purposes (a vice is the habit; "sin" is the religious word).
- Ethics is a **subset of philosophy** about the rightness/wrongness of acts and the goodness/badness of intentions.

### The piracy map on slide 4 (figure the text misses)

Slide 4 is a Revenera map titled *Top 20 Software License Misuse and Piracy Hotspots* (data as of November 2023). Ranking, top to bottom: China, Russia, United States, India, Brazil, Vietnam, Ukraine, Iran, Italy, Taiwan, France, Turkey, Germany, Mexico, Indonesia, Korea, Hong Kong, Australia, United Kingdom, Peru. Malaysia is not on it.

⚠️ **Common confusion.** Slide 3 says piracy is considered ethical in some countries but not others. The map shows that misuse is a problem in rich countries too (US, Germany, UK, Australia). Attitudes and enforcement differ; that does not make unlicensed copying "ethical" everywhere.

---

## 2. Ethical decision making (slides 7–9)

Slide 7's flowchart has a feedback loop the slide text does not mention: if the outcome is not a success, you go **back to the problem statement**.

```
Develop Problem Statement
        |
Identify Alternatives   <-- involve stakeholders
        |
Evaluate & Choose Alternative   <-- efficacy, risk, cost, implementation time
        |
Implement Decision   <-- timely, reliable, effective
        |
Evaluate Results   <-- did it work? effects on company and stakeholders?
        |
   SUCCESS? --Yes--> OK
        |
       No
        +-------------> back to Develop Problem Statement
```

Note: the slide 8 table says "Identity Alternatives" — that is a typo for **Identify**.

### Worked example (trace)

*Scenario:* Mei Ling, a junior admin, finds that a designer has installed a cracked copy of an expensive graphics program.

| Step | What Mei Ling does |
|---|---|
| Problem statement | "Unlicensed software is installed on a company PC; this exposes the company to legal and security risk." (short and specific) |
| Identify alternatives | (a) Ignore it. (b) Confront the designer privately. (c) Report to the IT manager. (d) Ask the manager to buy a licence. Ask the manager and designer for other ideas. |
| Evaluate & choose | Compare on efficacy, risk, cost, time: (a) leaves the risk; (b) may work but no record; (c) is effective but may cause conflict; (d) fixes the cause but costs money. Choose (c) then (d). |
| Implement | Report in writing to the IT manager this week; propose a licence purchase. |
| Evaluate results | Check next month: cracked copy removed? licence bought? Any retaliation? If not resolved, return to step 1 with a new problem statement ("management ignored the report"). |

**Why the slides list five characteristics of ethical choices (slide 9):** several options, long-term consequences, unpredictable outcomes, mixed costs/benefits (money, legal, social) and personal impact. This is why ethics is "not black-and-white" and needs a process rather than a gut reaction.

---

## 3. Morals vs ethics vs laws (slides 10–12)

| Term | Slide's definition | Where the rules come from | Enforced by |
|---|---|---|---|
| **Morals** | Personal views of right and wrong, described on the slide as religious views | Individual conscience, religion, upbringing | Your conscience |
| **Ethics** | Rules or codes of conduct a society, institution or profession expects | A group (company, profession, nation) | Peers, employer, professional body |
| **Law** | What we are and are not permitted to do | Government | Courts, police, penalties |

**Slide 12's Venn diagram** shows three overlapping circles: Ethics, Morality, Law. The overlaps are EM (ethics∩morality), EL (ethics∩law), ML (morality∩law) and EML (all three). The point: the three often agree but not always.

Examples of each region (own examples):
- **All three agree:** stealing is personally wrong, professionally unacceptable and illegal.
- **Legal but a person may consider it immoral:** the slide's abortion example — the law permits it, some people's morals reject it. (This is a contested topic; use it only as the slide does, to show the law and personal morals can differ.)
- **Ethics vs personal morals:** the slide's lawyer example. A lawyer's professional ethics require defending a client to the best of their ability even when the lawyer personally finds the crime repugnant.
- **Legal but unethical [extra]:** a company legally sells users' browsing data after hiding consent in a 40-page policy.

⚠️ **Simplification.** "Morals = religious views" is only one source of morals. A non-religious person still has morals. If an exam question quotes the slide, answer as the slide does.

---

## 4. Why ethics matters in IT (slides 13–19)

**Why IT is special:** information systems are tied up with social and political affairs; devices are in every part of work and personal life; the Internet lets organisations collect and keep huge volumes of personal data, so misuse is easier.

**Employee monitoring (slides 15–16)** is the standard dilemma: companies want to protect productivity and catch ethical lapses; employees use work email for personal messages. Difficulty: visiting a website does not tell you *why* the person visited, so monitoring alone cannot prove misuse.

### The six scenarios of public concern (slides 18–19)

| Scenario | What the tension is |
|---|---|
| Tracking employee email and Internet use | Managers want productivity control vs employees' need for self-direction and privacy |
| Downloading free music and movies | Likely copyright breach; costs copyright owners |
| Spamming | Unsolicited bulk email; cheap for the sender, costly for millions of recipients |
| Hackers and identity fraud | Stealing customer records to create identities and charge cards |
| Plagiarism | Copying material from the Internet for term papers |
| Cookies and spyware | Sites log users' online transactions and events on their machines |

---

## 5. Ethics for IT professionals (slides 20–29)

**IT professional** = someone who works in information technology (slide 20). Good-tech-career characteristics (slides 21–22): patience, communicates effectively, adapts quickly, multitasks, problem-solving ability, excited about the job.

**"Professional" in the US Code of Federal Regulations (slides 23–25):** work needing advanced expertise from lengthy specialised study; original and creative work; consistent use of discretion and judgment; mainly intellectual work whose output cannot be standardised to a time frame. Professionals are also expected to keep learning and help others develop.

⚠️ **Note [extra, not checked against the regulation]:** criteria 1 and 2 look like two different definitions merged (advanced knowledge vs artistic creativity). Learn the slide's four criteria as given.

### Professional code of ethics (slides 26–27)

A code has two parts: (1) the organisation's goals, (2) the guidelines and standards members must follow. The slide's four benefits:

| Benefit | Meaning |
|---|---|
| Ethical decision-making | Everyone decides from a shared set of principles |
| High ethical principles and practice | Reminds people of responsibilities they might be tempted to breach under business pressure |
| Public interest and confidence | Public trusts professionals to tell the truth and warn of consequences |
| Self-evaluation benchmark | A yardstick for self-checking and peer praise or criticism |

Key line: *laws should not serve as a comprehensive roadmap to ethical conduct* — obeying the law is the minimum.

### Seven trends reshaping professional services (slides 28–29)

| Trend | Meaning in one line |
|---|---|
| Client sophistication | Clients know what they need and negotiate hard |
| Governance | After scandals, stricter rules, e.g. the US Sarbanes-Oxley Act 2002 (corporate governance and financial reporting integrity) |
| Interconnectedness | Instant global communication ties clients and providers |
| Discretion | Clients want to monitor work-in-progress in real time, not just the final product |
| Modularization | Clients split processes into steps and outsource some |
| Globalization | Clients compare providers worldwide, so competition is high |
| Commoditization | Low-end services bought on price; clients want partnerships for high-end services |

Memory aid: **C-G-I-D-M-G-C** ("Clients Govern Interconnected Digital Markets, Globally Commoditised").

---

## 6. Common ethical issues for IT users (slides 30–34)

1. **Software piracy** — in a business it can often be traced to IT staff who encourage or take part; policies should let users report and contest it.
2. **Inappropriate use of computing resources** — personal browsing, chat rooms, games waste resources; offensive jokes or hate email can lead to complaints that the organisation tolerated a racist or sexually harassing environment.
3. **Inappropriate sharing of information.**

### Private vs confidential data (slide 32) — sorting exercise

| Category | Examples from the slide |
|---|---|
| **Private** (about a person) | Employees: wages, attendance, health records, performance reviews. Customers: payment card numbers, phone numbers, home addresses |
| **Confidential** (about the business) | Sales and marketing calendars, manufacturing processes, formulas, tactical and strategic plans, research and development |

Sharing either with an unauthorised party — even by accident — compromises privacy or lets rivals get business information.

**Three things an IT use policy can do (slide 34):** set guidelines for company software; define and limit appropriate use of IT resources (limited personal use allowed, offensive sites and harassing email not); structure information systems so data access is limited to those who need it (e.g. sales managers see sales data, not research and development results). The last is the *need-to-know* principle.

---

## 7. Certifications (slides 35–40)

A **certification** is awarded by a certifying body to show a practitioner has a certain range of skills. Employers differ: some see it as a barometer of skills; some are sceptical because it is no substitute for experience.

| | Vendor certification | Industry association certification |
|---|---|---|
| Who offers | A product vendor | A professional body |
| Purpose | Configure, implement, manage, troubleshoot *that vendor's* products | Broader expertise and outlook |
| Examples (slide) | Cisco, Microsoft, AWS | (ISC)², ISACA |
| Typical requirements | Pass exam(s) | Qualifications and experience, pass exam, follow the body's code of ethics, pay annual fee, earn continuing education credits, sometimes renew |

Trend: certifications are moving from purely technical content to a wider mix of academic, industry and behavioural competencies.

---

## ⚠️ Where the slides mislead

| Slide | What it says | Better understanding |
|---|---|---|
| 3 | Piracy is ethical in some countries | Attitudes and enforcement differ; the slide 4 map shows misuse in rich countries too |
| 5 | "sin" then "vices" | Same idea; "vice" is the habit |
| 8 | "Identity Alternatives" | Typo for Identify Alternatives |
| 10 | Morals = religious views | One source of morals only; simplified |
| 23–24 | Four criteria of a professional | Appears to merge two definitions **[unverified]** |
| 29 | "Discretion" trend | The description is about real-time oversight of work-in-progress |
| 38 | Renewal "monthly or yearly" test | Simplified; renewal rules vary by body |

**Exam strategy:** if a question quotes the slide's wording, answer as the slide does, then add the nuance if space allows.

---

## Cheat sheet

| Concept | Key point |
|---|---|
| Ethics | Shared standards of acceptable behaviour in a group |
| Ethical decision steps | Problem statement → Identify alternatives → Evaluate & choose → Implement → Evaluate results (loop back if not successful) |
| Morals / Ethics / Law | Personal / group expectations / government rules |
| Private vs confidential | About a person vs about the business |
| Code of ethics benefits | Decisions, high principles, public confidence, self-benchmark |
| Vendor vs association cert | Product-specific vs profession-wide, with ethics code and renewal |
| IT policy measures | Software guidelines, resource-use limits, need-to-know access |

---

## Practice

### A. Multiple choice

**A1.** Which item is *confidential* (business) information rather than *private* (personal) information?
(a) Employee wage details (b) Customer phone numbers (c) Manufacturing process formulas (d) Employee health records

**A2.** In the ethical decision-making flowchart, what happens if "Evaluate Results" shows the solution was not a success?
(a) The process ends (b) Return to Develop Problem Statement (c) Skip to Implement Decision (d) Choose the cheapest alternative

**A3.** Which is an *industry association* certification body?
(a) Cisco (b) Microsoft (c) AWS (d) (ISC)²

**A4.** Clients breaking business processes into steps and deciding which to outsource illustrates which trend?
(a) Commoditization (b) Modularization (c) Globalization (d) Governance

**A5.** Which statement best supports the claim "laws are not a full guide to ethical conduct"?
(a) Laws change (b) Something can be legal but still unethical (c) Ethics is enforced by police (d) Morals are always religious

### B. Short answer

**B1.** Distinguish morals, ethics and laws, using the lawyer example from slide 11.
**B2.** List the five steps of ethical decision making and explain why the flowchart loops back.
**B3.** Give three measures an organisation's IT use policy may include.

### C. Application

**C1.** A support technician notices a manager emailing a spreadsheet of staff salaries to a personal Gmail account "to work from home". Apply the five decision steps (one line each).

**C2.** Sort into private or confidential: (i) marketing calendar for next year; (ii) an employee's attendance record; (iii) a customer's home address; (iv) a secret product formula.

**C3.** Match each situation to one of the six scenarios on slides 18–19: (i) Ahmad downloads a pirated film; (ii) A website records every page a visitor opens without asking; (iii) An intruder steals bank customer records and opens credit cards in their names.

### D. Thinking

**D1.** Give one example of behaviour that is legal but unethical, and explain why relying on the law alone is not enough for an IT professional.
**D2.** A hiring manager says, "I prefer candidates with experience over certificates." A student says, "Certificates prove skill." Argue both sides in three sentences and say which the slides support.

---

## Answers

**A1.** (c). Formulas are business information (confidential). The others are personal data (private).
**A2.** (b). The figure loops back to the problem statement, because the problem may have been framed wrongly or changed.
**A3.** (d). Cisco, Microsoft and AWS are vendors.
**A4.** (b). Modularization.
**A5.** (b). Legal ≠ ethical; slide 27 says laws should not serve as a comprehensive roadmap.

**B1.** Morals: personal views of right and wrong (slide: religious views). Ethics: rules a society or profession expects. Law: what we are permitted or not permitted to do. In the lawyer example, the *ethics* of the legal profession require defending a client even if the lawyer's *morals* find the crime terrible; the law itself guarantees the defendant a defence.
**B2.** Problem statement; identify alternatives; evaluate and choose; implement; evaluate results. It loops back because success is checked after acting; if the outcome is not achieved, the problem or options need to be re-examined.
**B3.** Any three of: guidelines for using company software; defining and limiting appropriate use of IT resources; structuring information systems to protect data (need-to-know access).

**C1.** Problem: confidential staff data being sent to a personal account. Alternatives: ignore, speak to manager, report to IT security/HR, ask for a secure remote-access option. Evaluate: ignoring leaves the risk; secure remote access solves the real need. Implement: report or raise it, and propose secure remote access. Evaluate results: confirm the practice stopped and no data leak occurred; if not, restate the problem.
**C2.** (i) confidential; (ii) private; (iii) private; (iv) confidential.
**C3.** (i) Downloading free music and movies; (ii) Cookies and spyware; (iii) Hackers and identity fraud.

**D1.** Example: a company legally collects and sells detailed location data with consent buried in small print. It is lawful but deceives users. Law sets a minimum, changes slowly, and can lag behind technology; professionals also owe honesty and care to the public, as codes of ethics stress.
**D2.** Experience shows the person can do the job under real conditions; a certificate shows they passed a standard test and follow a code of ethics. The slides present both views (35) — certifications are a barometer of skills but "no substitute for experience".

---

## Links to other chapters

- Ch2 gives the technical side of the hacking, spam and identity fraud scenarios listed here.
- Ch3 and Ch5 develop the privacy issues (monitoring, cookies).
- Ch4 develops codes of conduct and whistleblowing.
- Ch8 covers piracy, plagiarism and copyright in depth.
