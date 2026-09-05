# 🧟 Zom-Mole Hunter

A Python and Streamlit-based detective game where the player investigates a laboratory sabotage, solves puzzles, collects evidence, and interrogates suspects to identify the hidden mole.

The player knows that a mole exists, but does not know how, when, or where the sabotage is happening. The mole uses a **utility-based adversarial agent** to decide whether to tell the truth or lie during interrogation, adapting to the evidence state and player suspicion level.

---

## 📁 Project Structure

```
Zom-Mole-Hunter/
├── app.py
├── game.py
├── case.py
├── evidence.py
├── ai_agent.py
└── README.md
```

### Files

**`app.py`**
Streamlit user interface layer. Displays game progression, room investigations, evidence discovery, PIN puzzles, Wordle challenges, and interrogation system.

**`game.py`**
Main game state and gameplay logic. Tracks room visits, puzzle solving, evidence discovery, PIN validation, Wordle mechanics, and interrogation flow.

**`case.py`**
Case data: suspects, roles, locations, clues, riddles, PIN construction, interrogation answers, and helper functions.

**`evidence.py`**
Evidence board tracker. Manages discovered clues, suspect statements, player notes, and contradiction detection.

**`ai_agent.py`**
Utility-based AI for the mole (Zephyr). Scores candidate truth/lie decisions based on current game state (suspicion, evidence presence, security locks). Includes state simulation and detective-response modeling.

---

## 🎮 Game Flow

### Investigation Phase

1. **LABORATORY**
   - Clue contains an acrostic
   - First four letters spell out: **F-O-U-R** → PIN digit **4**

2. **STORAGE**
   - Solve the riddle: **BREEZE** (6 letters)
   - Unlock Cafeteria clue
   - 50/50 roll determines if ventilation override evidence is found
   - **If FOUND:** Ventilation note appears in Storage
   - **If NOT_FOUND:** No note, mystery preserved

3. **CAFETERIA**
   - PIN clue shows: **??19**
   - Laboratory digit (4) + Storage letters length (6) + Cafeteria fragment (19) = **4619**

### Puzzle Solving

**PIN Construction:**
```
LAB_NUMBER (4) + STORAGE_ANSWER length (6) + "19" = 4619
```

**Wordle Activation:**
- Triggered only when **both** physical evidence pieces are present
- If ventilation found AND cafeteria found → Wordle activates
- If ventilation not found → Wordle silently skipped
- Player is not told why Wordle does or doesn't appear

### Interrogation Phase

**One question per suspect:**
- "Where were you at 11:50 PM?"

**Zephyr (the mole) makes truth/lie decision using utility-based reasoning:**
- Evaluates current suspicion level
- Considers whether evidence has been found
- Scores truth option vs. lie option
- Applies fixed penalty for "detective's anticipated response"
- Picks the higher-utility choice

**Other suspects always tell the truth.**

### Accusation

Player selects the guilty party based on evidence and statements. Must provide reasoning.

---

## 🤖 Adversarial AI — Utility-Based Agent

**Zephyr** is controlled by a utility-based agent, not true adversarial search:

- **Percepts:** suspicion level, evidence state, security lock status
- **Actions:** tell truth or lie during interrogation
- **Utility Function:** weighted sum of factors:
  - Low suspicion is valuable (+150 × (100 - suspicion))
  - Physical evidence against Zephyr is bad (-35 if storage found)
  - Contradictions are penalized (-30)
  - Security locks delay interrogation (+20 if active)
  - Game outcome weighted heavily (±1000 if win/loss)

- **Decision Process:**
  1. Simulate both candidate actions (truth vs. lie) on state copies
  2. Score each with `_evaluate_state()`
  3. Apply fixed penalty modeling "detective's likely response"
  4. Pick action with higher utility
  5. Tiebreaker: if tied, current suspicion threshold determines choice

**The detective is NOT an implemented agent** — only modeled as a fixed penalty constant. Zephyr reasons about the detective's response without the detective actually searching a game tree.

---

## 🧩 Core Mechanics

### Laboratory Clue

Four lines form an acrostic. First letters spell **FOUR**.

```
Filter pressure was stable before midnight.
One centrifuge cycle was interrupted manually.
Up and active Raven's workstation.
Recorded interruption at 11:52 PM.
```

Answer: **4**

### Storage Riddle

```
I cannot be seen, but I shake every leaf.
I fill the sails of ships, yet I weigh nothing at all.
I can carry a whisper farther than the person who spoke it.
Sailors welcome me when I am gentle, but fear what I become when I grow wild.
What am I?
```

Answer: **BREEZE**

Solving correctly unlocks the Cafeteria PIN clue and triggers a 50/50 roll for ventilation evidence. The ventilation override note only displays **if evidence is found**.

### Cafeteria Evidence

Receipt shows partial PIN: **??19**

Combined with lab digit and storage letter count:
- 4 (Laboratory)
- 6 (length of "BREEZE")
- 19 (visible on receipt)
- **PIN = 4619**

### Ventilation Override Discovery

- **Background briefing:** NOT mentioned (no spoiler)
- **Storage clue:** Only shown if 50/50 roll succeeds
- **Timeline:** Removed from background to preserve mystery
- **Interrogation:** Zephyr's alibi for 11:50 PM connects to this evidence

### Wordle Security Challenge

Activates only when both evidence pieces exist:
- Ventilation override found
- Cafeteria PIN clue found

If ventilation evidence is missing, Wordle is silently skipped — player doesn't know why.

Word: **VENTS**

---

## 👥 Suspects

| Name | Role | Location | Profile |
|------|------|----------|---------|
| **Raven** | Head Chemist | Laboratory | Brilliant, impatient, defensive |
| **Zephyr** | Supply Coordinator | Storage | Quiet, organized, evasive — **THE MOLE** |
| **Luca** | Security Officer | Corridor Patrol | Professional, embarrassed about camera outage |
| **Marinette** | Medic | Medical Bay | Friendly, observant, cautious |
| **Adrien** | Engineer | Generator Room | Casual, slightly nervous |

---

## 🔐 PIN & Security

**Correct PIN:** 4619

**PIN Digits:**
- 1st: 4 (Laboratory acrostic)
- 2nd: 6 (BREEZE length)
- 3rd–4th: 19 (Cafeteria receipt)

**Secondary Security Lock:**
Activates when player cracks PIN AND both evidence pieces are found. Requires solving Wordle (VENTS) before interrogation access.

---

## 🕵️ Player Objective

1. Investigate the Laboratory, Storage, and Cafeteria
2. Solve the Laboratory acrostic → **4**
3. Solve the Storage riddle (BREEZE) → unlock Cafeteria clue
4. Discover whether ventilation evidence exists (50/50 chance)
5. Crack the PIN → **4619**
6. Complete Wordle challenge if activated (VENTS)
7. Interrogate all suspects
8. Analyze evidence and statements
9. Accuse the mole
10. Provide reasoning for the accusation

---

## 🎲 Randomization

**Only the ventilation override evidence is randomized:**
- 50% → Evidence Found
- 50% → Evidence Not Found

Everything else (riddle answers, clue locations, suspect identities) is deterministic.

---

## 🕐 Key Timeline

| Time | Event |
|------|-------|
| 11:49 PM | Corridor cameras went offline |
| 11:50 PM | Cafeteria vending machine began unscheduled restock |
| 11:52 PM | Laboratory centrifuge was manually interrupted |
| 12:10 AM | Emergency alarm sounded |
| 12:14 AM | Six filter cartridges found missing from Storage |
| 12:18 AM | Three minutes of corridor footage missing |

**Ventilation override:** Not listed in background (discoverable only via evidence roll)

---

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- Standard library only (random, copy, html)

```bash
pip install streamlit
```

---

## ▶️ Running the Game

```bash
streamlit run app.py
```

Open the Streamlit application in your browser and begin the investigation.

---

## 🧪 Syntax Testing

```bash
python -m py_compile app.py game.py case.py evidence.py ai_agent.py
```

If no errors appear, all files are syntactically valid.

---

## 📌 Technologies

- **Python**
- **Streamlit** (web UI)
- **Game State Management** (class-based tracking)
- **Utility-Based AI Agent** (heuristic decision-making with state simulation)
- **Puzzle Mechanics** (acrostic, riddle, PIN, Wordle)
- **Evidence-Based Deduction** (player must connect clues to suspects)

---

## 🏁 Core Design Principle

**Uncertainty and Deduction**

The player knows:
- There is a mole
- Five employees were present

The player does NOT automatically know:
- When the mole acted
- How the mole acted
- What evidence is missing
- Whether Zephyr is telling the truth

The game avoids directly exposing the mole's hidden actions. Instead, the player must combine:
- Laboratory information
- BREEZE puzzle solution
- Cafeteria PIN data
- Randomized ventilation evidence
- Wordle results (if triggered)
- Suspect statements
- Zephyr's utility-based interrogation response

to reach the final accusation.

---

## 🧟 The Mole: Zephyr

**Identity:** Supply Coordinator

**Objective:** Avoid detection while Zephyr's utility-based agent reasons about truth vs. lies

**Decision-Making:** Each interrogation, Zephyr evaluates the current game state and chooses the response (truth or lie) that maximizes utility — considering suspicion level, evidence presence, and the detective's likely counter-response.

---

## 📖 License

This is a student project for AI/game design coursework.

---

**Good luck, detective. The mole is waiting.**
