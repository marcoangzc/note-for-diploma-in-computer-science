# AMIS1012 — Chapter 6: Risk Assessment and Trustworthy Computing

> Much of this chapter lives in images (the 8-step risk process, the trustworthy computing pillars, NIST's functions and tiers), so the plain text of the slides is nearly empty in places. This note reads the figures for you, adds a worked risk example with numbers that were actually computed, and corrects the slides' mistakes on **availability**, **"risk tolerance"**, **NIST tiers** and the **age of the ISO 27001 list**. Items marked **[extra]** are not from the slides; **[verified]** means checked against a source in September 2026.

---

## 0. One-sentence overview

Organisations identify and rank security risks, build trust into their systems around four pillars, protect information using the CIA triad, write security policies, and align with standards such as ISO 27001 and the NIST Cybersecurity Framework.

| Topic | Slides |
|---|---|
| 1. General security risk assessment | 4–11 |
| 2. Trustworthy computing | 12–14 |
| 3. CIA triad | 15–17 |
| 4. IT security policy | 18–21 |
| 5. ISO and ISO 27001 | 22–24 |
| 6. NIST and the Cybersecurity Framework | 25–30 |

---

## 1. General security risk assessment (slides 4–11)

**Risk assessment** = a method of finding the security risks an organisation's systems and networks face from internal and external threats. **Aim:** decide which time and money spending will best defend against the most probable and most significant threats.

Terms (slide 5):
- **Asset** = any hardware, software, computer system, network or database the enterprise uses to reach its business goals.
- **Failure case** (the slide's term) = any event that harms an asset, e.g. a virus infection or a DDoS attack. **[extra]** Most textbooks call this a *threat event* or *loss event*.

### The 8-step process (slides 6–10; the figure is a cascade with a feedback loop)

```
1 Identify Assets
2   Specify Loss Events
3     Frequency of Events
4       Impact of Events
5         Options to Mitigate
6           Feasibility of Options
7             Cost/Benefit Analysis
8               Decision  ----> Reassessment (loop back when anticipated or actual change occurs)
```

| Step | What you do | Slide detail |
|---|---|---|
| 1 | **Identify assets** | The IT assets you most worry about; prioritise those supporting business goals |
| 2 | **Specify loss events** | Potential loss cases, risks and threats (DDoS, insider theft) |
| 3 | **Estimate frequency** | Number of incidents or probability of each threat; some (insider theft) are more likely than others |
| 4 | **Determine impact (severity)** | Small effect, or stops the business for a long time? |
| 5 | **Options to mitigate** | Make the event less likely or less harmful (e.g. antivirus on all machines); focus on high-frequency and high-impact risks first |
| 6 | **Feasibility** | Can the mitigation actually be put into action? |
| 7 | **Cost/benefit analysis** | Compare the cost of controls with the loss avoided; no amount of money guarantees perfect compliance, so administrators must use judgment |
| 8 | **Decision** | Decide whether to implement a countermeasure; if not, consider whether the threat is serious and choose a cheaper option |
| Loop | **Reassessment** | Repeat when the environment changes |

### The formula (slide 7)

> Risk level = Probability × Impact

⚠️ **Slide 7 labels it "Risk Tolerance Level".** That label is wrong. Probability × impact gives the **size of a risk** (risk level or exposure). **Risk tolerance** is *how much risk the organisation is willing to accept* — you compare the risk level *against* the tolerance to decide what to do. Say "risk level" in your own words; if a question quotes the slide, quote it.

### Worked example (all numbers computed)

Scale (own, **[extra]**): probability 1–5 and impact 1–5, so risk = P × I (maximum 25).

| Risk | P | I | Score | Rank |
|---|---|---|---|---|
| Phishing leading to stolen credentials | 5 | 4 | **20** | 1 |
| DDoS on the public website | 4 | 4 | **16** | 2 |
| Insider theft of laptops | 3 | 3 | **9** | 3 |
| Public catalogue database, weak controls | 5 | 1 | **5** | tie |
| Customer personal-data database, strong controls | 1 | 5 | **5** | tie |
| Meteor hits data centre | 1 | 5 | **5** | tie |

**Slide 11's two scenarios** are the last two lines with real reasons:

| | Probability | Impact | Decision on the slide |
|---|---|---|---|
| Scenario 1: database of publicly available information, few controls | High | Non-critical (already public) | **Accept the risk** with current controls |
| Scenario 2: customer sensitive database, very high controls | Low (tight security) | Critical (reputation, lawsuits, huge loss) | **Prioritise**: take all necessary actions to avoid the risk |

**Why this matters (the "why" the slide skips):** both score **5** in the table above, yet the slide treats them very differently. A raw multiplication hides the fact that a *critical* impact (legal and reputational ruin) is not acceptable at any probability, while a frequent but trivial event can simply be tolerated. That judgment is what "risk tolerance" means. **[extra]** Common responses to a risk are accept, avoid, mitigate or transfer (e.g. insure).

### Cost/benefit worked example (step 7)

Suppose a fraud loss costs RM50,000 each time and happens twice a year: expected annual loss = 2 × 50,000 = **RM100,000**. A control cuts occurrence to 0.5 per year: new expected loss = 0.5 × 50,000 = **RM25,000**. Saving = **RM75,000 a year**.

| Control's annual cost | Saving RM75,000 | Decision |
|---|---|---|
| RM60,000 | 75,000 > 60,000 | Worth buying |
| RM90,000 | 75,000 < 90,000 | Not worth buying (consider a cheaper option — step 8) |
| RM100,000 | 75,000 < 100,000 | Not worth buying |

(Illustrative figures of my own; the slides give no numbers.)

---

## 2. Trustworthy computing (slides 12–14)

**Trustworthy computing** = a computing approach providing stable, confidential and consistent computing interactions based on sound market practices; it is a top priority for clients of the computer industry. **Microsoft** is the slide's example of a company running a trustworthy-computing campaign.

### The four pillars (slide 13's temple figure; definitions on slide 14)

| Pillar | Meaning |
|---|---|
| **Reliability** | The system is dependable, available when needed, and performs as expected at appropriate levels |
| **Security** | The system is resilient to attack, and the confidentiality, integrity and availability of the system and its data are protected |
| **Privacy** | People can control their personal information, and organisations that use it protect it faithfully |
| **Business integrity** | Companies are responsible to customers, help find suitable solutions, address problems with products and services, and are open in dealing with customers |

Memory aid: **S-P-R-B** ("Safe, Private, Reliable, Business-honest").

---

## 3. The CIA triad (slides 15–17)

| Principle | Correct meaning | Slide example |
|---|---|---|
| **Confidentiality** | Only authorised people can view the information | Credit card number is encrypted on the server; server room has door locks |
| **Integrity** | Information is correct and has not been altered by unauthorised people or malware | Attacker changes a purchase from $10,000.00 to $1.00 |
| **Availability** | Authorised users can get to the information and systems **when they need them** | Warehouse employee must be able to see the ordered quantity to ship the right items |

⚠️ **Slide 17 error.** It says availability "ensures that data is accessible to only authorized users and not to unapproved individuals". That is the definition of **confidentiality**. Availability means *authorised users can reach it when needed* — the opposite failure is downtime (a DoS attack). Also, "constant" access is an over-statement: the aim is timely and reliable access.

Mapping to Chapter 2 attacks **[extra]**: eavesdropping → breaks confidentiality; message alteration → breaks integrity; DoS/DDoS → breaks availability.

---

## 4. IT security policy (slides 18–21)

An **IT security policy** is a written document stating how an organisation plans to protect its IT assets.

| Policy | Purpose |
|---|---|
| **Acceptable Use Policy (AUP)** | Clear direction to network and system users on permitted use of information resources |
| **Information Security Policy** | High-level authority and guidance for the security programme |
| **Incident Response Policy** | How the organisation responds to security incidents |
| **Business Continuity and Disaster Recovery Policy** | Procedures and strategies so essential functions continue during and after a disaster, and data and assets are recovered and protected |
| **Software Development Life Cycle (SDLC) Policy** | Processes and standards ensuring security is built in at every stage of development (the slide says "maintaining software") |
| **Change Management and Change Control Policy** | How proposed changes to information systems are reviewed, approved and implemented, managing both cyber-security and operational risk |

The list is "non-exhaustive".

---

## 5. ISO and ISO 27001 (slides 22–24)

**ISO** = International Organization for Standardization. **ISO 27001** provides requirements for an **information security management system (ISMS)**: a systematic approach to managing sensitive assets (people, processes and IT systems) so they stay secure.

### The 14 control categories on slides 23–24

1. Information security policies
2. Organization of information security
3. Human resource security
4. Asset management
5. Access control
6. Cryptography
7. Physical and environmental security
8. Operations security
9. Communications security
10. System acquisition, development and maintenance
11. Supplier relationships
12. Information security incident management
13. Information security aspects of business continuity management
14. Compliance (with internal policies and external laws)

Memory aid for the first nine (Policies, Organization, HR, Asset, Access, Cryptography, Physical, Operations, Communications): **P-O-H-A-A-C-P-O-C** — "Please Only Hire Any Approved Crypto-Protected Operators Carefully".

⚠️ **Status check [verified].** This 14-category list is the **2013** edition (114 controls). The current edition, **ISO/IEC 27001:2022**, reorganised Annex A into **93 controls in four themes** (organisational 37, people 8, physical 14, technological 34), and organisations certified to the 2013 edition had to move to 2022 by **31 October 2025**. Learn the slide's list for the exam, but state that the standard has since been updated.

---

## 6. NIST and the Cybersecurity Framework (slides 25–30)

**NIST** = National Institute of Standards and Technology, under the US Department of Commerce; its mission is to advance measurement science, standards and technology to improve economic security and quality of life. It created the **NIST Cybersecurity Framework (CSF)** — guidelines to help organisations manage cyber risk, including prevention, detection, response and recovery. The slide says the latest version is **CSF 2.0**.

### Three parts (slides 26–30)

| Part | What it is |
|---|---|
| **1. CSF Core** | The activities/outcomes needed for cyber security, organised as **Functions → Categories → Subcategories** |
| **2. Organizational Profiles** | Describe the organisation's **Current Profile** (what it achieves now) and **Target Profile** (what it wants). The gap between them becomes the roadmap |
| **3. Tiers** | Four tiers describing the rigour of cyber-risk governance and management |

**The six Functions (slide 26 figure):** **Govern**, **Identify**, **Protect**, **Detect**, **Respond**, **Recover**. Slide 25's text names only identify, detect and respond, but the figure shows all six; *Govern* is the newest function in version 2.0.

**Five steps to create and use a Profile (slide 29 figure):**

| Step | Action |
|---|---|
| 1 | Scope the Organizational Profile |
| 2 | Gather needed information |
| 3 | Create the Organizational Profile |
| 4 | Analyse gaps and create an action plan |
| 5 | Implement the action plan and update the Profile (then repeat) |

**Four Tiers (slide 30 figure):** Tier 1 **Partial** → Tier 2 **Risk-Informed** → Tier 3 **Repeatable** → Tier 4 **Adaptive**.

⚠️ **Slide 30 error.** It says the tiers show "their level of compliance: the higher the tier, the more compliant". The CSF is **voluntary** — there is nothing to be "compliant" with. NIST describes Tiers as characterising the *rigour of an organisation's cyber-risk governance and management practices* and they are applied to Profiles. **[verified]** Also, higher is not automatically better; the right tier depends on the organisation's risk and resources. **[extra]** Slide 27 also mixes Profiles and Tiers by saying that after mitigating vulnerabilities an organisation "can move up to higher implementation tiers"; keep the two ideas separate.

---

## ⚠️ Where the slides mislead

| Slide | Says | Better understanding |
|---|---|---|
| 5 | "Failure case" | Usually called threat/loss event |
| 7 | Probability × Impact = "Risk tolerance level" | It is the risk level; tolerance is the acceptable amount |
| 11 | Scenarios decided by probability and impact | Raw multiplication would score both the same (5); judgment about critical impact drives the decision |
| 17 | Availability = access only for authorised users | That is confidentiality; availability = authorised users can access when needed |
| 20 | SDLC policy "for maintaining software" | Covers building security into development |
| 23–24 | 14 ISO 27001 categories | 2013 edition; now 93 controls in 4 themes (2022) |
| 25 | Framework helps identify, detect, respond | Six functions including Govern, Protect, Recover |
| 27, 30 | Tiers = compliance level; move up by fixing vulnerabilities | Voluntary framework; tiers describe rigour of risk management, not compliance |

**Exam strategy:** quote the slide formula, then add "this is the risk level".

---

## Cheat sheet

| Item | Remember |
|---|---|
| Risk assessment steps | Assets → loss events → frequency → impact → mitigation options → feasibility → cost/benefit → decision → reassess |
| Risk level | Probability × impact |
| Pillars | Security, privacy, reliability, business integrity |
| CIA | Confidentiality (only authorised view), integrity (accurate, unaltered), availability (accessible when needed) |
| Policies | AUP, information security, incident response, BC&DR, SDLC, change management |
| ISO 27001 | Requirements for an ISMS |
| CSF parts | Core, Profiles (current/target), Tiers |
| CSF functions | Govern, Identify, Protect, Detect, Respond, Recover |
| Tiers | Partial, Risk-Informed, Repeatable, Adaptive |

---

## Practice

### A. Multiple choice

**A1.** Which best defines *availability*?
(a) Only authorised people can view data (b) Data is accurate and unaltered (c) Authorised users can access data when they need it (d) Data is encrypted

**A2.** An attacker changes a purchase from $10,000.00 to $1.00. Which CIA property is violated?
(a) Confidentiality (b) Integrity (c) Availability (d) None

**A3.** In the risk process, which step comes immediately after "Impact of events"?
(a) Cost/benefit analysis (b) Decision (c) Options to mitigate (d) Identify assets

**A4.** Which is *not* one of the four trustworthy computing pillars?
(a) Reliability (b) Privacy (c) Business integrity (d) Scalability

**A5.** The current Profile compared with the Target Profile in the NIST CSF gives you:
(a) A tier (b) A gap and roadmap (c) A certificate (d) An ISO score

### B. Short answer

**B1.** State the four trustworthy computing pillars.
**B2.** Explain why slide 7's label "risk tolerance level" is misleading.
**B3.** List the six CSF 2.0 functions.

### C. Calculation / trace

**C1.** Risk A: probability 4, impact 3. Risk B: probability 2, impact 5. Risk C: probability 5, impact 2. Compute each score and rank them.
**C2.** A control costs RM40,000 a year. Without it, a breach happens 1.5 times a year costing RM60,000 each time; with it, 0.5 times a year. Compute the expected annual loss before and after, the saving, and decide.
**C3.** Classify the CIA property affected: (i) A DDoS makes the online shop unreachable; (ii) A stranger reads stored customer emails; (iii) A worker edits payroll figures without permission.

### D. Thinking

**D1.** Slide 11's Scenario 1 accepts the risk of a public database with weak controls. Give one reason this could still be wrong (hint: integrity).
**D2.** Why might a small firm choose Tier 2 rather than Tier 4?

---

## Answers

**A1.** (c). (a) is confidentiality; (b) integrity.
**A2.** (b) Integrity.
**A3.** (c) Options to mitigate (step 5).
**A4.** (d). Scalability is a software quality attribute (Chapter 7), not a pillar.
**A5.** (b). The gap drives the action plan.

**B1.** Security, privacy, reliability, business integrity.
**B2.** Probability × impact measures the size of a risk. Risk tolerance is the amount of risk the organisation is willing to accept; you compare the risk level to the tolerance to decide whether to accept, reduce or avoid.
**B3.** Govern, Identify, Protect, Detect, Respond, Recover.

**C1.** A = 4 × 3 = 12; B = 2 × 5 = 10; C = 5 × 2 = 10. Rank: A first; B and C tie at 10. (Judgment: B has critical impact, so many organisations would treat B with more attention despite the tie.)
**C2.** Before: 1.5 × 60,000 = RM90,000. After: 0.5 × 60,000 = RM30,000. Saving = RM60,000 a year. Cost RM40,000 < RM60,000, so the control is worth buying (net benefit RM20,000).
**C3.** (i) Availability; (ii) Confidentiality; (iii) Integrity.

**D1.** Although the data is public, someone could **alter** it (for example replace prices or contact details). Integrity and availability still matter even when confidentiality does not.
**D2.** Tiers describe the rigour of risk management, not compliance. Tier 4 needs more resources; a small firm with low risk may choose a lower tier that matches its risk appetite, and higher tiers are not automatically better.

---

## Links to other chapters

- Ch2: attacks that break each CIA property.
- Ch3: laws vs standards; NACSA and the Cyber Security Act require NCII entities to do risk assessments.
- Ch4: codes of conduct supporting security policies.
- Ch7: SDLC policy links to software quality and testing.
