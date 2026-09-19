# AMIS1012 — Chapter 3: Organisation Privacy (Part I)

> This chapter is mostly a list of laws, and the slides give each law one line. This note explains what each law is *for*, pulls the actual content out of the figure slides (CFAA's seven offences, the SCA sections, GLBA's six duties), organises everything into comparison tables, and flags facts that are out of date. **Status checks** below were verified against news and law-firm sources in September 2026; items marked **[extra]** are not from the slides.

---

## 0. One-sentence overview

Cyber security protects the confidentiality, integrity and functioning of information systems, and countries back it with laws; this chapter surveys those laws in the US, Europe, UK, China, India and Malaysia.

| Topic | Slides |
|---|---|
| Parts of an information system (recap) | 2–4 |
| Cyber security and its 7 subdomains | 7–9 |
| Purpose of cyber security laws | 10 |
| US laws: CFAA, SCA, ECPA, HIPAA, CCPA, GLBA | 11–19 |
| EU, UK, China, India | 20–22 |
| Malaysian cyber laws and NACSA | 23–25 |

---

## 1. Recap: parts of an information system (slides 2–4)

Six parts: **people** (end users), **procedures** (rules for using software, hardware, data), **software** (step-by-step instructions that turn data into information), **hardware** (equipment that processes data), **data** (raw facts) and the **Internet** (connects computers to share information).

Worked distinction — **data vs information** (payroll example from the slide): hours worked = 40 and pay rate = RM15 are *data*; software multiplies them; RM600 weekly pay is *information*.

---

## 2. Introduction to cyber security (slides 7–9)

**Cyber security** = methods, techniques and processes used to secure the **confidentiality, integrity and functioning** of information systems, networks and data against cyber attacks or unauthorised access.

### The seven subdomains

| Subdomain | What it covers | Everyday example |
|---|---|---|
| Application security | Protected application architecture, secure code, strong input validation | Rejecting unexpected characters typed into a login form |
| Data protection and identity management | Who may access systems; data integrity at rest and in transit | Staff logins with role-based access |
| Network security | Hardware and software defences against unwanted access, delays, misuse | Firewalls |
| Mobile security | Protecting data on phones, tablets, laptops from unauthorised entry, theft, ransomware | Remote wipe of a lost phone |
| Cloud security | Secure cloud architectures and software (AWS, Google, Azure) | Encrypting storage buckets |
| Disaster recovery and business continuity (DR&BC) | Procedures, reporting, warnings so services keep running or resume after a crisis | Backup site |
| Security awareness and training | Formal instruction on best practice, processes, regulations, reporting malicious activity | Phishing awareness course |

Memory aid: **A-D-N-M-C-D-S**.

---

## 3. Why have cyber security laws? (slide 10)

Laws and legal frameworks by governments/organisations safeguard digital information, systems and networks. Five purposes: protect sensitive data; prevent cybercrime; data privacy; national security; consumer trust.

---

## 4. Global laws

### 4.1 United States (slides 11–19)

The US has many separate laws by topic or industry rather than one general law.

| Law | What it protects / regulates | Key content |
|---|---|---|
| **CFAA** — Computer Fraud and Abuse Act | Federal computers, bank computers and computers connected to the Internet from hacking and online fraud | Slide 11's figure lists seven offences under 18 U.S.C. §1030(a): (1) accessing a computer to commit espionage; (2) trespass resulting in exposure of government, credit or financial information; (3) trespass in a government computer; (4) fraud involving unauthorised access; (5) damaging a computer (worm, virus, Trojan, time bomb, DoS); (6) trafficking in passwords; (7) threatening to damage a computer |
| **SCA** — Stored Communications Act | **Data at rest** (stored emails, texts, instant messages, cloud storage, hard drive) | Slide 13's figure: §2701 bans unauthorised access to stored communications; §2702 bars providers (email, cell, social media, cloud) from knowingly disclosing stored communications; §2703 explains how government can compel disclosure by warrant, court order or subpoena; §2705 lets government get a non-disclosure order |
| **ECPA** — Electronic Communications Privacy Act | **Data in transit** (emails, texts, calls, uploads) — bans intentional interception, mainly wiretaps | Three titles: **I** wiretaps (and illegally obtained communications can't be used as evidence); **II** = the SCA; **III** government needs authorisation for pen registers and trap-and-trace devices |
| **HIPAA** 1996 | Individually identifiable health information | **Privacy Rule** protects Protected Health Information (PHI) in any form (electronic, written, oral). **Security Rule** requires confidentiality, integrity and security of **electronic** PHI (ePHI). Covered entities: healthcare providers, health insurers, clearinghouses and their **business associates** |
| **CCPA** — California Consumer Privacy Act | State law: consumers' control over personal information businesses collect | Four rights: know, delete (with exceptions), opt out of sale/sharing, non-discrimination for using these rights |
| **GLBA** — Gramm-Leach-Bliley Act | Financial institutions (loans, investment advice, insurance) | Slide 19's figure gives six duties: give an **annual notice** of information-sharing practices; **secure** customer data; **dispose** of it properly; limit **access** to staff who need it; **train** employees; **manage** third-party risks |

**Trick to remember SCA vs ECPA:** *S*tored → *S*CA (at rest); *E*lectronic *C*ommunications in motion → ECPA Title I (in transit). SCA is also ECPA Title II, so the two overlap.

Worked example — where does the law bite?

| Situation | Data state | Main law |
|---|---|---|
| Someone intercepts your email as it is sent | In transit | ECPA Title I |
| Someone hacks the mail server to read your saved emails | At rest | SCA §2701 (and possibly CFAA) |
| An email provider hands your stored emails to a stranger | At rest | SCA §2702 |
| A hospital clerk emails a patient's record to the wrong person | PHI | HIPAA Privacy Rule |

⚠️ **HIPAA "subset" (slide 16).** The slide says the Security Rule is a subset of the Privacy Rule. The two are **separate rules**; the Security Rule covers only electronic PHI (ePHI), which is a subset of *the data* the Privacy Rule covers. Safe wording: "The Privacy Rule covers all PHI; the Security Rule applies to electronic PHI." Source: legal explainers of HIPAA rules.

### 4.2 Europe, UK, China, India (slides 20–22)

| Law | Key points |
|---|---|
| **GDPR** (EU) — in effect **25 May 2018** | Applies to any organisation that targets or collects data on people in the EU, wherever it is; organisations must be able to prove compliance; heavy fines |
| **Personal data (GDPR definition)** | Any information relating to a person who can be identified directly or indirectly: names, email addresses, location, race/ethnicity, gender, biometric data, religious beliefs, web cookies, IP address, health and genetic data, political opinions |
| **UK Data Protection Act 2018** | UK's implementation of GDPR |
| **China PIPL** | Protects personal information of Chinese citizens, regulates cross-border data transfer |
| **India** | Slide says "Digital Personal Data Protection **Bill**, 2023" applying to digital personal data in India and to processing outside India for offering goods or services in India |

**Status check (India):** It is now an **Act**. India's Parliament enacted the Digital Personal Data Protection Act on 11 August 2023, and the implementing Rules were notified in November 2025. Learn the slide's name for the exam but know it became law.

⚠️ Slide 20 calls GDPR "the toughest privacy and security law in the world" — that is an opinion, not a definition. **[extra, not source-checked]** GDPR's top fine tier is up to €20 million or 4% of worldwide annual turnover, whichever is higher.

---

## 5. Malaysian laws (slides 23–25)

**NACSA** — National Cyber Security Agency, established **February 2017** as the national lead agency for cyber security; its aim is to coordinate the nation's experts and resources to build resilience against cyber attacks.

### The 11 laws on the NACSA list (slides 24–25)

| # | Act | Note |
|---|---|---|
| 1 | Copyright (Amendment) Act 1997 | Copyright in software/works |
| 2 | Computer Crimes Act 1997 | Offences such as unauthorised access |
| 3 | Digital Signature Act 1997 | Legal recognition of digital signatures |
| 4 | Telemedicine Act 1997 | Remote medical practice |
| 5 | Communications and Multimedia Act **1998** | Slide 24 prints "1988", a typo **[extra]** |
| 6 | Electronic Commerce Act 2006 | Online transactions |
| 7 | Electronic Government Activities Act 2007 | Government services electronically |
| 8 | Personal Data Protection Act (PDPA) 2010 | Personal data in commercial transactions |
| 9 | Penal Code | General criminal law |
| 10 | Anti-Fake News (Repeal) Act 2020 | Its effect is to repeal the Anti-Fake News Act 2018 **[extra]** |
| 11 | Cyber Security Act 2024 | See below |

(One-line purposes are for orientation; the slides ask you to read NACSA's website for descriptions.)

### Status checks (slides are out of date on two of these)

1. **Cyber Security Act 2024 (Act 854).** Slide 25 says it "has not yet been enforced". It **came into force on 26 August 2024**, with regulations on risk assessment and audit, incident notification, service-provider licensing and compounding of offences. For entities operating national critical information infrastructure (NCII), a cyber security risk assessment is required at least once a year and an audit every two years, and incidents must be reported (initial details within six hours, more within 14 days).
2. **PDPA 2010 amended.** The Personal Data Protection (Amendment) Act 2024 was brought into force in three phases (January, April and June 2025). Key changes: data processors directly bound by the security principle; "sensitive personal data" widened (biometric data included); higher penalties; mandatory data breach notification and data protection officer appointment; data portability rights. The slides do not mention these.

---

## ⚠️ Where the slides mislead

| Slide | What it says | Better understanding |
|---|---|---|
| 16 | Security Rule is a subset of the Privacy Rule | Separate rules; Security Rule covers ePHI only |
| 20 | GDPR "toughest law in the world" | Opinion; describe its reach and fines instead |
| 22 | India's DPDP **Bill** 2023 | Now an Act (2023), Rules 2025 |
| 24 | Communications and Multimedia Act 1988 | Enacted 1998 **[extra]** |
| 25 | Cyber Security Act 2024 not yet enforced | In force since 26 Aug 2024 |
| 25 | PDPA 2010 listed alone | Amended 2024, in force in phases 2025 |

**Exam strategy:** if the question is on the Malaysian list, give the slide's list; add the updates as extra marks.

---

## Cheat sheet

| Item | Remember |
|---|---|
| Cyber security | Confidentiality, integrity, functioning of systems/data |
| 7 subdomains | Application; data protection & identity; network; mobile; cloud; DR&BC; awareness & training |
| CFAA | Hacking/fraud on federal, bank and Internet-connected computers |
| SCA | Data at rest |
| ECPA | Data in transit; 3 titles (wiretap, SCA, pen register/trap and trace) |
| HIPAA | Health data; Privacy Rule (all PHI) vs Security Rule (ePHI) |
| CCPA | California; know, delete, opt out, non-discrimination |
| GLBA | Financial institutions; notice, secure, dispose, access, train, third parties |
| GDPR | EU; effective 25 May 2018; extraterritorial |
| NACSA | Est. Feb 2017; Malaysia's lead cyber agency |
| Cyber Security Act 2024 | Act 854; in force 26 Aug 2024 |

---

## Practice

### A. Multiple choice

**A1.** Emails stored on a mail server are protected mainly by which US law?
(a) ECPA Title I (b) SCA (c) GLBA (d) CCPA

**A2.** Which is *not* one of the seven cyber security subdomains on slides 8–9?
(a) Network security (b) Cloud security (c) Application security (d) Physical building design

**A3.** GLBA applies chiefly to:
(a) Hospitals (b) Financial institutions (c) Schools (d) Retail shops

**A4.** GDPR applies to an organisation in Malaysia when it:
(a) Has a Malaysian server (b) Targets or collects data of people in the EU (c) Has an EU citizen employee only (d) Sells in the US

**A5.** Which body is Malaysia's national lead agency for cyber security?
(a) MCMC (b) NACSA (c) MyIPO (d) SC

### B. Short answer

**B1.** Distinguish the SCA from the ECPA Title I using "data at rest" and "data in transit".
**B2.** List the four CCPA consumer rights.
**B3.** Explain the difference between the HIPAA Privacy Rule and Security Rule.

### C. Application

**C1.** Classify the data state and pick the US law: (i) A hacker taps a Wi-Fi link and reads texts as they are sent; (ii) An employee of a cloud provider gives your stored photos to a journalist; (iii) A bank leaves customer files in an unlocked skip when it closes a branch.
**C2.** Slide 3's example: 35 hours × RM12 an hour. Which is data and which is information? Compute the information.
**C3.** A Malaysian online shop with EU customers asks whether GDPR and PDPA apply. Give one sentence for each.

### D. Thinking

**D1.** Why might many different laws (CFAA, SCA, ECPA, HIPAA, GLBA…) be a challenge for a company compared with one general privacy law?
**D2.** Slide 25 said the Cyber Security Act 2024 was "not yet enforced". What does this teach you about using lecture slides as legal sources?

---

## Answers

**A1.** (b) SCA (data at rest).
**A2.** (d). The subdomains are application, data protection and identity, network, mobile, cloud, DR&BC, awareness and training.
**A3.** (b).
**A4.** (b). Location of the server or company does not matter; targeting or collecting EU people's data does.
**A5.** (b) NACSA (established Feb 2017).

**B1.** SCA protects stored communications (emails in a database, cloud data): data at rest. ECPA Title I bans intentional interception of communications while they are travelling: data in transit. The SCA is also Title II of the ECPA.
**B2.** Right to know what is collected and how it is used/shared; right to delete (with exceptions); right to opt out of sale or sharing; right to non-discrimination for exercising these rights.
**B3.** Privacy Rule: protects PHI in any form (electronic, written, oral). Security Rule: requires safeguards for the confidentiality, integrity and security of electronic PHI only.

**C1.** (i) In transit → ECPA Title I. (ii) At rest → SCA §2702 (provider disclosure). (iii) Financial institution failing to safeguard/dispose customer data → GLBA.
**C2.** Data: 35 hours and RM12/hour. Information: 35 × 12 = RM420 weekly pay.
**C3.** GDPR applies if the shop targets or collects data on people in the EU, regardless of where it is based. The PDPA (Malaysia) applies to personal data in commercial transactions in Malaysia (as amended in 2024, with breach notification and DPO rules).

**D1.** A company must identify which laws apply to each type of data and sector, follow different definitions and rules, and may face overlapping duties; a single law would be simpler but the US takes a sector-by-sector approach.
**D2.** Laws change; slides are snapshots. Always check the current status (gazette, official portal) before relying on a slide for legal status.

---

## Links to other chapters

- Ch2: the crimes these laws address.
- Ch4: US laws (HIPAA, GLBA, FISMA…) reappear; Malaysia's Whistleblower Protection Act.
- Ch5: privacy in digital technology and major privacy laws.
- Ch6: ISO 27001 and NIST provide standards rather than laws.
