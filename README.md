# 🧟 Zom-Mole Hunter

**Zom-Mole Hunter** is a Python and Streamlit-based detective game where the player investigates a laboratory, solves puzzles, collects evidence, and interrogates suspects to identify the hidden mole.

The player knows that a mole exists, but does **not** know how, when, or where the sabotage is happening. Missing evidence is intentionally ambiguous, and the mole uses adversarial decision-making during interrogation.

---

## 📁 Project Structure

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

Handles the Streamlit user interface and displays the game progression.

### `game.py`

Contains the main game state and gameplay logic, including rooms, puzzles, evidence, PIN validation, Wordle, and interrogation.

### `case.py`

Stores the case information, clues, suspects, PIN information, and interrogation answers.

### `evidence.py`

Manages evidence collected during the investigation.

### `ai_agent.py`

Contains the adversarial AI logic used by the mole, Zephyr. The AI uses Minimax-style reasoning to decide whether Zephyr should tell the truth or lie during interrogation.

---

# 🎮 Game Flow

The investigation follows this sequence:

```text
LABORATORY
      ↓
Solve Laboratory clue
      ↓
PIN digit = 4
      ↓
STORAGE
      ↓
Solve BREEZE riddle
      ↓
BREEZE solved
      ↓
CAFETERIA PIN CLUE UNLOCKED
      ↓
CAFETERIA
      ↓
PIN clue = ??19
      ↓
PIN = 4619
      ↓
VENTILATION OVERRIDE CLUE
50/50 RANDOMIZED
      ↓
 ┌───────────────────┐
 │                   │
FOUND             NOT FOUND
 │                   │
 ↓                   ↓
Cafe found        Cafe found
 │                   │
 ↓                   ↓
WORDLE             SKIP WORDLE
 │                   │
 └─────────┬─────────┘
           ↓
     INTERROGATION
           ↓
Ask everyone:
"Where were you at 11:50 PM?"
           ↓
Zephyr uses Minimax
to choose truth or lie
           ↓
      ACCUSATION
```

---

# 🔬 Laboratory

The player begins in the Laboratory.

The Laboratory clue contains exactly these four lines:

```text
Filter pressure was stable before midnight.
One centrifuge cycle was interrupted manually.
Up and active Raven's workstation.
Recorded interruption at 11:52 PM.
```

Solving the Laboratory investigation provides the first PIN digit:

```text
4
```

---

# 📦 Storage

The player then investigates Storage.

Storage contains the **BREEZE riddle**.

The correct answer is:

```text
BREEZE
```

The BREEZE riddle is **not randomized**.

The player must correctly solve BREEZE in order to progress to the Cafeteria PIN clue.

```text
Storage
   ↓
Solve BREEZE
   ↓
Cafeteria PIN clue becomes available
```

---

# 🍽️ Cafeteria

After solving the BREEZE riddle, the player can access the Cafeteria PIN clue.

The Cafeteria clue provides:

```text
??19
```

Together with the Laboratory digit and Storage information, the player determines the correct PIN:

```text
4619
```

The Cafeteria clue is **always found**.

There is no 50/50 randomization for the Cafeteria clue.

---

# 🌬️ Ventilation Override Evidence

The important randomized clue is:

```text
A ventilation override was recorded at 11:50 PM.
```

This clue has a genuine **50/50 chance of being found**.

The BREEZE riddle does **not** determine whether the ventilation clue is found.

Instead:

```text
BREEZE
  ↓
Unlock Cafeteria PIN clue
  ↓
Ventilation Override
  ↓
50/50 FOUND / NOT FOUND
```

There are therefore two possible evidence states.

### Evidence Found

```text
Ventilation override = FOUND
Cafeteria evidence = FOUND
```

The player has both pieces of evidence required to activate the Wordle challenge.

### Evidence Not Found

```text
Ventilation override = NOT FOUND
Cafeteria evidence = FOUND
```

The player continues the investigation, but the Wordle challenge is skipped.

The player is **not told that Zephyr caused the missing evidence**.

The absence of the clue is deliberately left ambiguous.

---

# 🟩 Wordle Challenge

Wordle is activated only when **both** required evidence conditions are satisfied:

```python
ventilation_override_found and cafeteria_evidence_found
```

### If both are found:

```text
Ventilation evidence → FOUND
Cafeteria evidence → FOUND
                ↓
              WORDLE
```

### If ventilation evidence is missing:

```text
Ventilation evidence → NOT FOUND
Cafeteria evidence → FOUND
                ↓
          WORDLE SKIPPED
```

Skipping Wordle does **not** directly make Zephyr suspicious.

The player should not receive a message saying that Zephyr deliberately skipped or sabotaged the challenge.

---

# 🤖 Adversarial AI

The hidden mole is:

```text
Zephyr
```

Zephyr is controlled by an adversarial AI.

The AI models the interaction as:

```text
Zephyr = MAX
Detective = MIN
```

Zephyr attempts to maximize his chances of avoiding detection.

The detective attempts to minimize Zephyr's advantage.

The AI considers the current game state, including the available evidence.

---

# 🧠 Evidence-Aware Interrogation

After the investigation, the player interrogates all suspects.

Everyone is asked:

```text
Where were you at 11:50 PM?
```

Zephyr's response is different from the other suspects.

The AI chooses between:

```text
TELL THE TRUTH
        vs
       LIE
```

using Minimax-style adversarial reasoning.

The decision is based on the actual evidence state.

For example:

### State A — Ventilation Evidence Found

```text
Ventilation override = FOUND
Cafeteria evidence = FOUND
```

Zephyr must account for the fact that the player has the ventilation evidence.

### State B — Ventilation Evidence Not Found

```text
Ventilation override = NOT FOUND
Cafeteria evidence = FOUND
```

Zephyr has less physical evidence to worry about and may therefore choose a different response.

The player does **not** see the internal AI calculation.

They only see Zephyr's final answer.

---

# 🌬️ Connection Between Evidence and Zephyr

The ventilation override clue is important because it is connected to the interrogation.

The player may discover:

```text
A ventilation override was recorded at 11:50 PM.
```

and then compare that information with Zephyr's answer to:

```text
Where were you at 11:50 PM?
```

This creates the deduction mechanic.

The player must determine whether Zephyr's statement is consistent with the available evidence.

The game does **not** simply announce:

```text
Zephyr sabotaged the ventilation system.
```

or:

```text
Zephyr hid the clue.
```

Instead, the player has to infer what happened from the evidence and interrogation.

---

# 👥 Suspects

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

The player must identify Zephyr through deduction.

---

# 🔐 PIN

The correct security PIN is:

```text
4619
```

The PIN is constructed from the investigation:

```text
Laboratory → 4
Storage/BREEZE → 6
Cafeteria → 19
```

Therefore:

```text
4619
```

---

# 🎯 Player Objective

The player must:

1. Investigate the Laboratory.
2. Solve the Laboratory clue.
3. Obtain the PIN digit `4`.
4. Investigate Storage.
5. Solve the `BREEZE` riddle.
6. Unlock the Cafeteria PIN clue.
7. Investigate the Cafeteria.
8. Obtain the `??19` PIN information.
9. Enter PIN `4619`.
10. Determine whether the ventilation override clue is found.
11. Play Wordle only if the required evidence is present.
12. Interrogate every suspect.
13. Ask everyone where they were at 11:50 PM.
14. Analyze Zephyr's AI-generated truth/lie response.
15. Accuse the mole.

---

# 🎲 Randomization

Only the **ventilation override evidence** is randomized.

The probability is:

```text
50% → Evidence Found
50% → Evidence Not Found
```

The BREEZE riddle is always solvable with:

```text
BREEZE
```

The Cafeteria clue is always available after BREEZE is solved.

---

# 🕵️ Core Design Principle

The game is designed around **uncertainty and deduction**.

The player knows:

```text
There is a mole.
```

But the player does not automatically know:

```text
When the mole acted
How the mole acted
What evidence is missing
Whether Zephyr is telling the truth
```

The game therefore avoids directly exposing the mole's hidden actions.

Instead, the player must combine:

* Laboratory information
* The BREEZE puzzle
* Cafeteria PIN information
* The randomized ventilation evidence
* Wordle results
* Suspect statements
* Zephyr's Minimax-controlled interrogation response

to reach the final accusation.

---

# 🛠️ Requirements

Install Python and Streamlit.

```bash
pip install streamlit
```

---

# ▶️ Running the Game

From the project directory, run:

```bash
streamlit run app.py
```

Then open the Streamlit application in your browser.

---

# 🧪 Syntax Testing

The Python files can be checked with:

```bash
python -m py_compile app.py game.py case.py evidence.py ai_agent.py
```

If the command produces no errors, the Python files passed the syntax check.

---

# 📌 Technologies

* Python
* Streamlit
* Randomized evidence mechanics
* Puzzle/riddle mechanics
* Evidence-based deduction
* Adversarial search
* Minimax-style AI
* Interactive interrogation

---

# 🏁 Final Mystery

The central mystery is not simply:

> "Who is the mole?"

The real challenge is determining **what happened at 11:50 PM**, whether the available evidence supports the suspects' stories, and whether Zephyr's interrogation response is truthful.

The player must use the evidence rather than being explicitly told what Zephyr did.

```text
🧟 THE MOLE: ZEPHYR
```
