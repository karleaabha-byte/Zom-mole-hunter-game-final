# 🧟 Zom-Mole Hunter

**Zom-Mole Hunter** is a Python-based detective game built with **Streamlit**.
The player investigates a mysterious laboratory, solves clues, collects evidence, unlocks a security challenge, and interrogates suspects to identify the hidden mole.

---

## 🎮 Game Overview

A mole is secretly sabotaging the laboratory.

The player knows that **one of the characters is the mole**, but does not know:

* When the sabotage happens
* How the sabotage happens
* Which evidence may be missing
* Whether a suspect is telling the truth or lying

The goal is to investigate the rooms, solve puzzles, collect evidence, and finally identify the mole.

---

## 🗂️ Project Structure

The project contains five Python files:

```text
Zom-Mole-Hunter/
│
├── app.py
├── game.py
├── case.py
├── evidence.py
├── ai_agent.py
└── README.md
```

### `app.py`

Handles the Streamlit user interface.

It displays:

* Game introduction
* Room navigation
* Clues
* Riddles
* PIN input
* Wordle challenge
* Interrogation
* Final accusation

### `game.py`

Contains the main game logic and manages the current game state.

It controls:

* Room visits
* Puzzle solving
* Evidence collection
* PIN validation
* Wordle activation
* Interrogation
* Suspicion
* Game progression

### `case.py`

Contains the case information and investigation data.

It stores:

* Characters
* Mole identity
* Room information
* Laboratory clue
* Storage riddle
* Cafeteria clue
* PIN
* Interrogation questions and answers

### `evidence.py`

Manages the evidence collected by the player during the investigation.

### `ai_agent.py`

Contains the adversarial AI logic for the mole.

Zephyr uses a **depth-limited Minimax-style decision process** during interrogation to decide whether to tell the truth or lie.

---

# 🧩 Game Flow

The investigation follows this sequence:

```text
LABORATORY
     ↓
Solve Laboratory clue
     ↓
Get PIN digit: 4
     ↓
STORAGE
     ↓
Solve BREEZE riddle
     ↓
        50/50
       /    \
      /      \
 FOUND      NOT FOUND
   |            |
   |         CAFETERIA
   |            |
   |       Evidence found
   |            |
   └──────┬─────┘
          ↓
     Enter PIN 4619
          ↓
  Check Storage + Cafeteria
          ↓
     ┌────┴────┐
     ↓         ↓
   BOTH      NOT BOTH
   FOUND      FOUND
     ↓         ↓
  WORDLE     SKIP WORDLE
     └────┬────┘
          ↓
   INTERROGATION
          ↓
 Ask everyone:
 "Where were you at 11:50 PM?"
          ↓
      ACCUSATION
```

---

# 🔬 Laboratory

The player begins in the Laboratory.

The Laboratory clue contains exactly four lines:

```text
Filter pressure was stable before midnight.
One centrifuge cycle was interrupted manually.
Up and active Raven's workstation.
Recorded interruption at 11:52 PM.
```

Solving the Laboratory investigation gives the first PIN digit:

```text
4
```

---

# 📦 Storage

The player then investigates Storage.

The Storage puzzle is a riddle.

The correct answer is:

```text
BREEZE
```

After correctly solving the riddle, the game performs a genuine **50/50 random check**.

There are two possible outcomes:

### Evidence Found

The Storage evidence is added to the player's evidence.

### Evidence Not Found

The Storage evidence is not added.

The player is **not told that Zephyr caused the missing evidence**.

This is intentional because the player should have to reason about the case rather than being given the mole's actions directly.

Storage is the **only randomized evidence location**.

---

# 🍽️ Cafeteria

The Cafeteria is different from Storage.

The Cafeteria clue is **always found**.

There is no 50/50 random chance for the Cafeteria.

The Cafeteria clue provides the remaining PIN information:

```text
??19
```

Combined with the Laboratory and Storage information, the correct PIN is:

```text
4619
```

---

# 🔐 Security PIN

The player must enter:

```text
4619
```

The PIN is constructed from:

```text
Laboratory = 4
Storage answer length = 6
Cafeteria = 19
```

Therefore:

```text
4 + 6 + 19 = 4619
```

---

# 🟩 Wordle Challenge

The Wordle challenge is activated only when:

```python
storage_evidence_found and cafeteria_evidence_found
```

Both pieces of evidence must exist.

Because the Cafeteria clue is always found, the Storage evidence determines whether the Wordle is reached in a particular playthrough.

However, the game logic explicitly checks **both** evidence states.

If both are found:

```text
Security unlocked
       ↓
     Wordle
       ↓
 Interrogation
```

If both are not found:

```text
Security unlocked
       ↓
 Wordle skipped
       ↓
 Interrogation
```

Skipping the Wordle does **not** automatically make Zephyr suspicious.

The player is not told that Zephyr intentionally skipped or sabotaged the challenge.

---

# 🤖 Adversarial AI

The mole is:

```text
Zephyr
```

The AI is designed around adversarial decision-making.

The basic model is:

```text
Zephyr = MAX player
Detective = MIN player
```

Zephyr attempts to maximize his chances of avoiding detection.

The detective attempts to minimize Zephyr's advantage.

The AI evaluates factors such as:

* Suspicion
* Contradictions
* Physical evidence
* Storage evidence state
* Cafeteria evidence
* Security state
* Wordle outcome

---

# 🕵️ Interrogation

During interrogation, every character is asked the same question:

> Where were you at 11:50 PM?

The important point is that **Zephyr does not always tell the truth**.

The AI evaluates two possible actions:

```text
TELL TRUTH
     vs
LIE
```

The Minimax-style search evaluates the possible consequences of both choices.

The option that gives Zephyr the better adversarial outcome is selected.

The player only sees Zephyr's resulting statement.

The internal AI decision is hidden.

---

# 🧠 Hidden Evidence State

The AI receives the actual evidence state of the game.

There are two important states:

### State 1 — Storage Found

```text
Storage evidence = FOUND
Cafeteria evidence = FOUND
```

This gives the detective more physical evidence.

### State 2 — Storage Not Found

```text
Storage evidence = NOT FOUND
Cafeteria evidence = FOUND
```

This gives the detective less physical evidence.

The AI considers the actual state when deciding how Zephyr responds during interrogation.

The player does not receive the internal AI reasoning.

---

# 👥 Characters

The suspects are:

```text
Raven
Zephyr
Luca
Marinette
Adrien
```

The actual mole is:

```text
Zephyr
```

The player must determine this through investigation rather than being directly told by the game.

---

# 🎯 Objective

The player's objective is to:

1. Investigate the Laboratory.
2. Solve the Laboratory clue.
3. Obtain the first PIN digit.
4. Investigate Storage.
5. Solve the `BREEZE` riddle.
6. Discover whether Storage evidence is available.
7. Investigate the Cafeteria.
8. Obtain the Cafeteria evidence.
9. Enter PIN `4619`.
10. Complete the Wordle challenge if both required evidence pieces exist.
11. Interrogate every suspect.
12. Compare their statements with the evidence.
13. Accuse the correct mole.

The correct mole is:

```text
ZEphyr
```

or, with normal capitalization:

```text
Zephyr
```

---

# 🛠️ Requirements

You need Python installed on your computer.

Install the required dependency:

```bash
pip install streamlit
```

If the project contains additional dependencies, install them according to your environment.

---

# ▶️ Running the Game

Open a terminal in the project directory.

Run:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL.

Open that URL in your browser to play the game.

---

# 🎲 Randomness

Storage uses a real 50/50 random event.

The game uses Python's random number generator:

```python
random.Random(seed)
```

If a seed is supplied, the result can be reproduced for testing.

If no seed is supplied, the game produces a normal random outcome.

---

# 🔎 Important Design Rules

The game intentionally follows these rules:

### 1. Storage is the only randomized evidence

```text
Storage → 50/50
Cafeteria → Always found
```

### 2. The player does not see sabotage decisions

The game does not tell the player:

```text
"Zephyr sabotaged Storage."
```

or:

```text
"Zephyr skipped the Wordle."
```

### 3. Missing evidence does not directly identify Zephyr

A missing clue is part of the uncertainty of the investigation.

### 4. Wordle depends on evidence

Wordle requires:

```text
Storage evidence = FOUND
AND
Cafeteria evidence = FOUND
```

### 5. Zephyr's interrogation response is AI-controlled

The AI chooses between:

```text
Truth
Lie
```

based on the current game/evidence state.

### 6. The player always asks the same interrogation question

```text
Where were you at 11:50 PM?
```

---

# 🧪 Testing

The Python files can be syntax-checked using:

```bash
python -m py_compile app.py game.py case.py evidence.py ai_agent.py
```

If no output is produced, the files passed the Python syntax check.

---

# 📌 Technologies Used

* **Python**
* **Streamlit**
* **Randomized game mechanics**
* **Adversarial search**
* **Minimax-style AI**
* **Puzzle/riddle mechanics**
* **Evidence-based deduction**

---

# 🏁 Final Goal

The game is designed as an adversarial detective experience.

The player investigates incomplete evidence while the hidden mole attempts to survive interrogation.

The key challenge is not simply solving puzzles — it is determining **which evidence can be trusted, what information is missing, and whether a suspect's statement is truthful**.

The final objective is to identify:

```text
🕵️ THE MOLE: ZEPHYR
```
