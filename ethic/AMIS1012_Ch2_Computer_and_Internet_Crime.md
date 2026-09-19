# AMIS1012 — Chapter 2: Computer and Internet Crime

> The slides define each attack in one or two lines and rely on diagrams the text extraction misses. This note adds a comparison table for malware, step-by-step traces for the four active attacks, the phishing-kit life cycle, and flags where slides 14, 25 and 34 are confusing. Items marked **[extra]** are not from the slides and were not checked against a source unless stated.

---

## 0. One-sentence overview

Cybercrime is unlawful activity using computers or the Internet as a weapon, a target, or both; this chapter classifies security attacks (passive vs active), the main malware types, spam and phishing, and the kinds of people who commit computer crime.

| Topic | Slides |
|---|---|
| Introduction to cybercrime | 4–6 |
| Why users' expectations and complexity create vulnerability | 7–11 |
| Reliance on commercial software (exploits, patches) | 12 |
| Passive attacks | 13–17 |
| Active attacks (masquerade, replay, message alteration, DoS) | 18–21 |
| Malware: virus, worm, Trojan, botnet, DDoS, rootkit | 22–31 |
| Spam | 32–35 |
| Phishing and phishing-kit life cycle | 36–39 |
| Hackers and crackers; malicious insider; cybercriminals | 40–45 |

---

## 1. Introduction to cybercrime (slides 4–6)

**Cybercrime** = illegal activity carried out over the Internet, using a device as a weapon, a goal (target), or both. It splits into crimes causing **malicious harm** (on purpose) and **accidental harm**.

Examples on the slides: illegal entry/intrusion and computer abuse; data theft; cyber bullying; distributing worms or viruses; hacking to get financial or personal details; **unintentional damage**.

⚠️ **Unintentional damage** — the slide's example: a dissatisfied employee writes a "harmless" virus. It does no immediate theft, but it still costs money in wasted work hours and repair effort. Lesson: *harmless* code is still harm.

---

## 2. Computer user expectations and why vulnerabilities rise (slides 7–11)

Slides 7–11 explain why computer-related incidents keep increasing:

1. **More data captured, in finer detail.** Content/document management systems record every "touch" (create, show, copy, modify) — the *audit trail metadata* can become very large. Good for accountability, but also a big pile of data to protect.
2. **Help-desk pressure.** Users want problems fixed fast, so help desks may skip checking identity or permissions.
3. **Credential sharing.** Users lend logins to colleagues who lost theirs, giving unauthorised people access.
4. **Complexity.** Hundreds of millions of lines of code connect computers, networks, operating systems, web pages, switches, routers and gateways. Each new connected device adds an **entry point** for attackers.
5. **Speed of change.** It is hard to keep evaluating new threats and put controls in place.

**Slide 12 — reliance on commercial software.** An **exploit** is an attack that takes advantage of a flaw (usually poor design or implementation). When a flaw is found, engineers release a **patch** ("fix"). If you do not install it, you are exposed.
**[extra]** A *zero-day* flaw is one attackers exploit before a patch exists.

---

## 3. Security attacks: passive vs active (slides 13–21)

| | Passive attack | Active attack |
|---|---|---|
| Goal | Learn or use information without changing anything | Change data, create fake data, or disrupt service |
| Effect on system | None visible | Alters data or disrupts activity |
| Detection | Very hard (nothing changes) | Easier to detect |
| Focus of defence | **Prevention** (avoid it happening) | Detection and recovery as well |
| Examples | Eavesdropping, traffic monitoring | Masquerade, replay, message alteration, denial of service |

⚠️ **Slide 14 error:** it says a passive attack is "a successful attack tries to change the system's resources or disrupt its activity". That sentence describes an **active** attack. Passive = observe only.

The diagrams use three characters: **Bob** (sender), **Alice** (receiver), **Darth** (attacker).

### Passive attacks

**Eavesdropping.** Darth secretly listens to a call, email or file transfer not meant for him.

**Traffic monitoring (slide 17 diagram).** Darth does not read or change the message. He observes *patterns*: who transmits, where, how often, how long. Bob's message still reaches Alice unchanged, so neither knows.

⚠️ Slide 16 says cryptography can stop these attempts. **[extra]** Encryption hides the *content*, but traffic patterns (who, when, how much) can still show through, so it protects content better than it protects patterns.

### Active attacks

**Masquerade (slide 19).** Darth sends Alice a message that *appears* to come from Bob, or an entity with few permissions pretends to be one with more.

**Replay (slide 20).** Darth *passively records* a legitimate message from Bob to Alice and *later retransmits* it to get an unauthorised result (e.g. re-sending a "transfer RM100" instruction). The diagram's label "Inter Reply Message to Alice" is a typo for "later replay".

**Message alteration.** Part of a genuine message is changed, or messages are delayed or reordered.

**Denial of service (DoS).** Flood a system with fake requests or data so the service, site or server becomes unavailable.

### Trace: each attack on a bank-transfer message

| Step | Eavesdropping | Traffic monitoring | Masquerade | Replay | Alteration |
|---|---|---|---|---|---|
| Bob sends "Pay Alice RM100" | Darth reads it | Darth notes size, time, parties | — | Darth copies it | Darth intercepts it |
| What Darth does next | Nothing | Nothing | Sends "Pay Darth RM100" claiming to be Bob | Re-sends the copy tomorrow | Changes to "Pay Alice RM1000" |
| Class | Passive | Passive | Active | Active | Active |

---

## 4. Malware (slides 22–31)

**Malware** = malicious software. Slide 22 puts these under "active attacks". Payload = the malicious action a piece of malware carries out.

### Comparison table

| Type | Needs a host file/program? | Self-replicates? | Needs a person's action? | Key idea |
|---|---|---|---|---|
| **Virus** | Yes (attached to a file, disc, document) | Yes, when the infected file is passed on | **Yes** — spreads when the infected file is opened or shared | Code that makes a system behave unexpectedly; carries a payload |
| **Macro virus** (a kind of virus) | Yes (documents) | Yes, inserts itself in later documents | Yes | Written in an application's macro language (Visual Basic, VBScript) |
| **Worm** | No — standalone | Yes | Slide says **no** (but see below) | Duplicates itself; spreads by network, often emailing copies |
| **Trojan horse** | No | **No** | Yes — the user installs it | Disguised as a genuine file or application |
| **Botnet** | — | — | — | Group of infected computers ("bots"/"zombies") controlled by an attacker |
| **Rootkit** | — | — | — | Toolkit giving remote access and control (run programs, read logs, monitor users, change settings) |

⚠️ **Slide 25 contradiction.** It says worms need no human help, yet also that worms "use social engineering to persuade users to run them". Both cannot be fully true. Safe way to answer: *worms can spread by themselves by exploiting a flaw; some also rely on tricking users.* The core difference from a virus is that a worm does not need a host program.

### DDoS (slides 28–30)

A **Distributed Denial of Service** attack uses many compromised machines at once.
1. Attacker infects many devices (including IoT devices) with malware → they become **bots** (zombies).
2. The set of bots is a **botnet**; the attacker sends remote commands.
3. Every bot sends requests to the target's IP address.
4. The server or network is overloaded (DoS).

Why it is hard to stop: each bot is a genuine Internet device, so attack traffic looks like normal traffic (slide 30's diagram shows attackers and real users both sending traffic to the server).

DoS vs DDoS: one source vs many sources.

---

## 5. Spam (slides 32–35)

**Spam** = unrequested, usually promotional messages sent to huge numbers of people.

| Type (slide) | Where |
|---|---|
| Email spam | Clogs the mailbox |
| Social media spam | Fake profiles on social networking sites |
| Mobile spam | SMS text messages and push alerts |
| Instant-messaging spam ("spam text messages") | WhatsApp, Telegram; like email spam but faster |
| SEO spam / spam indexing | Using search-engine-optimisation tricks to boost a spammer's site in results |

⚠️ Slide 34's titles are confusing: "Spam on mobile phones" is SMS/push alerts; "Spam text messages" is really messaging-app spam. Do not mix them up in the exam.

---

## 6. Phishing (slides 36–39)

**Phishing** is a **social engineering** attack to obtain sensitive information (passwords, card details). **Social engineering** = manipulating a person into acting (creating an account, sending a message, revealing data) by pretending to be trustworthy.

**Phishing by email (slide 37).** Looks like a real business email (same wording, fonts, logos, signatures); creates **urgency**; links look real but usually have a misspelled domain or extra subdomains.

**Spear phishing** (the slide calls it "phishing with a specific purpose"): targets one person or organisation; needs deeper knowledge of the target. (The slide's phrase "power system" is likely meant to read "organisation's structure".)

### Life cycle of a phishing kit (slide 39 diagram)

| Step | What happens |
|---|---|
| 1 | The legitimate website is **cloned** |
| 2 | The login page is changed to send credentials to a **credential-stealing script** |
| 3 | Modified files are bundled into a **zip** file: the *phishing kit* |
| 4 | The kit is **uploaded to a hacked website** and unzipped |
| 5 | **Emails** are sent with links to the spoofed site |

Tell-tale signs you can teach from the slides: urgency, look-alike domain, request for credentials.

---

## 7. People: hackers, crackers, insiders, cybercriminals (slides 40–45)

| Person | Slide description |
|---|---|
| **Ethical hacker** | Explores network limits with permission to test security; often holds a licence such as CEH; works with a company to protect its data |
| **Cracker** (malicious hacker) | Breaks in maliciously; deletes records, denies legitimate users service; profit-driven |
| **Malicious insider** | Current or former employee/contractor/partner who intentionally exceeded or misused authorised access, harming confidentiality, integrity or availability; fraud often needs coordination with a third party |
| **Cybercriminal** | Financial motive; steals then resells card numbers, names, mobile IDs; can pay dishonest insiders for access |
| **Hacktivist** | Uses computer attacks for a political or social goal |
| **Cyber terrorist** | More radical aims: to damage or shut down networks rather than collect information (e.g. dams, air traffic control) |

⚠️ **Time-sensitive claim (slide 45):** "there has yet to be a single case of true cyber terrorism". This is a slide claim that depends on definitions and date; quote it as the slide states it. **[extra]** Hacktivism is described on slide 44 as "use of malware"; in practice it also includes defacing websites and DDoS, but answer with the slide's version.

**[extra]** Many textbooks also use "white hat / black hat / grey hat" for these motives.

---

## ⚠️ Where the slides mislead

| Slide | What it says | Better understanding |
|---|---|---|
| 14 | Passive attack "tries to change the system's resources" | That is an active attack; passive only observes |
| 16 | Cryptography avoids traffic monitoring | Hides content; patterns can still leak **[extra]** |
| 20 | "Inter Reply Message" / "passive recording of a data device" | Typos: later replay; data unit |
| 25 | Worms need no human help but use social engineering | Contradictory; worm = standalone, self-spreading, sometimes helped by tricks |
| 34 | Two spam types with similar names | SMS/push vs messaging-app spam |
| 38 | "power system" | Organisation's structure |
| 44 | Hacktivism = use of malware | Narrow; other techniques are used **[extra]** |
| 45 | No true cyber terrorism yet | Definition- and date-dependent claim |

**Exam strategy:** answer as the slide does, but say "generally" where it is contradictory.

---

## Cheat sheet

| Term | Definition in one line |
|---|---|
| Cybercrime | Illegal activity with a device as weapon, target or both |
| Exploit / patch | Attack on a flaw / fix for the flaw |
| Passive / active | Observe only / change or disrupt |
| Masquerade, replay, alteration, DoS | The four active attacks |
| Virus / worm / Trojan | Needs host and user / standalone and self-spreading / disguised, no self-replication |
| Botnet / DDoS | Controlled infected devices / attack using many of them |
| Rootkit | Tool set for remote access and control |
| Spam types | Email, social media, mobile (SMS/push), IM, SEO |
| Phishing / spear phishing | Mass deception for credentials / targeted deception |
| Phishing kit steps | Clone → alter login → zip → upload to hacked site → send emails |
| Malicious insider | Insider who misuses authorised access |

---

## Practice

### A. Multiple choice

**A1.** An attacker records a valid payment message and re-sends it later. Which attack?
(a) Masquerade (b) Replay (c) Eavesdropping (d) Traffic monitoring

**A2.** Which malware does **not** copy itself?
(a) Worm (b) Virus (c) Trojan horse (d) Macro virus

**A3.** A defender's main goal against passive attacks, per the slides, is:
(a) Detection (b) Prevention (c) Recovery (d) Prosecution

**A4.** A group of infected computers controlled remotely is a:
(a) Rootkit (b) Botnet (c) Spear phish (d) Macro

**A5.** Step 3 of the phishing-kit life cycle is:
(a) Clone the website (b) Send emails (c) Bundle the modified files into a zip (d) Upload to a hacked site

### B. Short answer

**B1.** Explain the difference between a virus and a worm.
**B2.** Why is DDoS traffic hard to filter?
**B3.** Give two reasons why help-desk practices and user habits increase vulnerability (slides 9–11).

### C. Application

**C1.** Classify each as passive or active and name the attack: (i) An attacker notes that Bob sends Alice ten messages every night at 2 a.m., without reading them; (ii) An attacker changes "RM100" to "RM10,000" in a message; (iii) An attacker floods a shop's website so customers cannot buy.
**C2.** An email says "Your bank account will be closed in 24 hours! Log in at bank-secure-login.example-help.com". List three phishing signs.
**C3.** Trace a DDoS in four steps, starting from an attacker infecting IoT devices.

### D. Thinking

**D1.** A dissatisfied employee writes a "harmless" virus that only displays a joke. Is it cybercrime? Use slide 6.
**D2.** Compare a cracker and a malicious insider. What advantage does an insider have?

---

## Answers

**A1.** (b) Replay.
**A2.** (c) Trojan horse; slide 26 says Trojans cannot reproduce themselves.
**A3.** (b) Prevention; slide 14: the focus is avoidance rather than identification, because passive attacks are hard to detect.
**A4.** (b) Botnet.
**A5.** (c). Order: clone, alter login, zip, upload, email.

**B1.** A virus attaches to a host file/program and spreads because a user passes on or opens the infected item. A worm is a standalone program that duplicates itself and spreads over networks (for example by emailing itself) without a host program.
**B2.** Each bot is a real Internet device, so the requests look like ordinary traffic and are hard to tell apart from real users.
**B3.** Any two of: help desks rush and may skip identity/permission checks; users share credentials; growing complexity adds entry points; hard to keep up with new threats.

**C1.** (i) Passive: traffic monitoring; (ii) Active: message alteration; (iii) Active: denial of service.
**C2.** Urgency ("24 hours"); a misspelled/unusual domain with extra subdomains; a request to log in via an email link.
**C3.** (1) Attacker infects many devices; (2) devices become bots forming a botnet; (3) attacker sends commands to all bots; (4) bots flood the target's IP with requests, overloading it.

**D1.** Yes, slide 6 treats it as cybercrime causing unintentional damage: no immediate theft, but real cost in wasted work hours and repair resources.
**D2.** Both may harm confidentiality, integrity or availability. A cracker breaks in from outside; a malicious insider already has authorised access, so it is harder to detect and may be coordinated with an outside party.

---

## Links to other chapters

- Ch1: the hacking, spam and identity-fraud scenarios.
- Ch3: laws against these crimes (CFAA, Computer Crimes Act).
- Ch6: CIA triad — DoS attacks availability, alteration attacks integrity, eavesdropping attacks confidentiality.
- Ch8: cybersquatting overlaps with phishing.
