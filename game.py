"""
Game state and rules engine for Zom-Mole Hunter
"""

import case
import random

from ai_agent import MoleAI
from evidence import EvidenceBoard


# ============================================================
# GAME CONSTANTS
# ============================================================

ROOMS = [
    "Laboratory",
    "Storage",
    "Cafeteria"
]


WORDLE_ANSWER = "VENTS"
WORDLE_MAX_ATTEMPTS = 6


# ============================================================
# GAME STATE
# ============================================================

class GameState:

    def __init__(self, seed=None):

        self.rng = random.Random(seed)

        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        self.mole_ai = MoleAI(seed)

        # ----------------------------------------------------
        # EVIDENCE
        # ----------------------------------------------------

        self.evidence = EvidenceBoard()

        # ----------------------------------------------------
        # ACTION / GAME STATE
        # ----------------------------------------------------

        # Actions are unlimited.
        # We keep track of how many the player has used
        # for the final case report/statistics.

        self.actions_used = 0

        self.suspicion = 10

        self.visited_rooms = {}

        self.room_decisions = {}

        self.asked = {}

        self.log = []

        self.game_over = False

        self.result = None

        self.accused = None

        # ----------------------------------------------------
        # CONTRADICTIONS
        # ----------------------------------------------------

        self.contradiction_flagged = False

        self.last_contradiction = None

        # ----------------------------------------------------
        # CAFETERIA PIN
        # ----------------------------------------------------

        self.pin_cracked = False

        self.pin_attempts = 0

        # ----------------------------------------------------
        # SECURITY CHALLENGE
        # ----------------------------------------------------

        self.security_challenge_active = False

        self.security_challenge_complete = False

        self.wordle_answer = WORDLE_ANSWER

        self.wordle_attempts = []

        self.wordle_max_attempts = WORDLE_MAX_ATTEMPTS

        self.wordle_failed = False

        self.storage_riddle_solved = False
        self.storage_evidence_found = False
        self.storage_roll = None
        self.cafeteria_evidence_found = False


    # ========================================================
    # ACTIONS
    # ========================================================

    def can_act(self):

        return not self.game_over


    def _log(self, text):

        self.log.append(text)


    def _clamp_suspicion(self):

        self.suspicion = max(
            0,
            min(
                100,
                self.suspicion
            )
        )


    # ========================================================
    # ROOM INVESTIGATION
    # ========================================================

    def visit_room(self, room):

        if not self.can_act():

            return (
                False,
                "The case is already closed."
            )

        if room in self.visited_rooms:

            return (
                False,
                f"You've already investigated the {room}."
            )

        if room not in ROOMS:

            return (
                False,
                "Unknown room."
            )


        # ====================================================
        # LABORATORY
        # ====================================================

        if room == "Laboratory":

            clue = case.get_lab_clue()

            self.evidence.add_clue(
                "lab_acrostic"
            )

            self.room_decisions[room] = "neutral"


        # ====================================================
        # STORAGE
        # ====================================================

        elif room == "Storage":

            clue = case.get_storage_clue()
            self.room_decisions[room] = "awaiting_riddle"
            self._log(
                "📦 Storage riddle discovered. Solve BREEZE "
                "to determine whether the evidence can be recovered."
            )


        # ====================================================
        # CAFETERIA
        # ====================================================

        else:

            clue = case.get_cafeteria_clue()

            self.cafeteria_evidence_found = True

            self.evidence.add_clue(
                "cafeteria_pin"
            )

            self.room_decisions[room] = "neutral"


        # ----------------------------------------------------
        # CLAMP SUSPICION
        # ----------------------------------------------------

        self._clamp_suspicion()


        # ----------------------------------------------------
        # SAVE INVESTIGATION
        # ----------------------------------------------------

        self.visited_rooms[room] = clue

        self.actions_used += 1

        self._log(
            f"🔎 Investigated the {room}."
        )

        return (
            True,
            clue
        )


    # ========================================================
    # STORAGE RIDDLE
    # ========================================================

    def solve_storage_riddle(self, answer):

        if "Storage" not in self.visited_rooms:
            return False, "Investigate Storage first."

        if self.storage_riddle_solved:
            return True, "FOUND" if self.storage_evidence_found else "NOT_FOUND"

        if str(answer).strip().upper() != "BREEZE":
            self.actions_used += 1
            self.suspicion += 2
            self._clamp_suspicion()
            self._log("❌ Incorrect Storage riddle answer.")
            return False, "Incorrect answer. Try again."

        self.storage_riddle_solved = True
        self.actions_used += 1
        self.storage_roll = self.rng.random() < 0.5
        self.storage_evidence_found = self.storage_roll

        if self.storage_evidence_found:
            self.evidence.add_clue("storage_riddle")
            self.room_decisions["Storage"] = "evidence_found"
            self._log("🔎 Storage evidence FOUND (50/50 result).")
            return True, "FOUND"

        self.room_decisions["Storage"] = "evidence_not_found"
        self._log("❌ Storage evidence NOT FOUND (50/50 result).")
        return True, "NOT_FOUND"


    # ========================================================
    # PIN
    # ========================================================

    def attempt_pin(self, guess):

        if self.pin_cracked:

            return True

        if not self.can_act():

            return False


        # ----------------------------------------------------
        # EVERY ATTEMPT IS TRACKED
        # ----------------------------------------------------

        self.actions_used += 1

        self.pin_attempts += 1

        digits = "".join(
            character
            for character in str(guess)
            if character.isdigit()
        )

        correct = (
            digits == case.CORRECT_PIN
        )


        # ====================================================
        # CORRECT PIN
        # ====================================================

        if correct:

            self.pin_cracked = True

            self.evidence.set_pin_cracked()

            self._log(
                "🔓 PIN CRACKED. "
                "Restricted employee access unlocked."
            )


            # Wordle is controlled by the hidden evidence state.
            # Cafeteria evidence is always present, so Wordle activates
            # exactly when BOTH Storage and Cafeteria evidence exist.
            activate_challenge = (
                self.storage_evidence_found
                and self.cafeteria_evidence_found
            )

            if activate_challenge:

                self.security_challenge_active = True

                self.security_challenge_complete = False

                self._log(
                    "🚨 SECONDARY SECURITY LOCK ACTIVATED."
                )

            else:

                self.security_challenge_active = False

                self.security_challenge_complete = True

                self._log(
                    "🔓 INTERROGATION SYSTEM UNLOCKED."
                )

            return True


        # ====================================================
        # INCORRECT PIN
        # ====================================================

        self._log(
            f"🔐 Incorrect PIN attempt "
            f"#{self.pin_attempts}."
        )

        return False


    # ========================================================
    # WORDLE / SECURITY CHALLENGE
    # ========================================================

    def submit_wordle(self, guess):

        # ----------------------------------------------------
        # CHALLENGE ACTIVE?
        # ----------------------------------------------------

        if not self.security_challenge_active:

            if self.security_challenge_complete:

                return (
                    True,
                    "ALREADY_COMPLETE"
                )

            return (
                False,
                "No security challenge is active."
            )


        # ----------------------------------------------------
        # NORMALIZE GUESS
        # ----------------------------------------------------

        guess = str(guess).strip().upper()


        # ----------------------------------------------------
        # LENGTH CHECK
        # ----------------------------------------------------

        if len(guess) != 5:

            return (
                False,
                "Enter a 5-letter word."
            )


        # ----------------------------------------------------
        # LETTER CHECK
        # ----------------------------------------------------

        if not guess.isalpha():

            return (
                False,
                "Letters only."
            )


        # ----------------------------------------------------
        # ATTEMPT LIMIT
        # ----------------------------------------------------

        if (
            len(self.wordle_attempts)
            >= self.wordle_max_attempts
        ):

            self.security_challenge_active = False

            self.wordle_failed = True

            self._log(
                "🔐 SECURITY CHALLENGE FAILED: "
                "Maximum attempts reached."
            )

            return (
                False,
                "ATTEMPTS_EXHAUSTED"
            )


        # ----------------------------------------------------
        # SAVE ATTEMPT
        # ----------------------------------------------------

        self.wordle_attempts.append(
            guess
        )

        answer = self.wordle_answer

        result = []


        # ----------------------------------------------------
        # WORDLE RESULT
        # ----------------------------------------------------

        for index, letter in enumerate(guess):

            if letter == answer[index]:

                result.append("🟩")

            elif letter in answer:

                result.append("🟨")

            else:

                result.append("⬛")


        # ====================================================
        # CORRECT
        # ====================================================

        if guess == answer:

            self.security_challenge_complete = True

            self.security_challenge_active = False

            self._log(
                "🔓 SECONDARY SECURITY LOCK DEFEATED."
            )

            return (
                True,
                {
                    "status": "CORRECT",
                    "result": result,
                    "attempts_remaining": (
                        self.wordle_max_attempts
                        - len(self.wordle_attempts)
                    )
                }
            )


        # ====================================================
        # OUT OF ATTEMPTS
        # ====================================================

        if (
            len(self.wordle_attempts)
            >= self.wordle_max_attempts
        ):

            self.security_challenge_active = False

            self.wordle_failed = True

            self._log(
                "🔐 SECURITY CHALLENGE FAILED."
            )

            return (
                False,
                {
                    "status": "FAILED",
                    "result": result,
                    "attempts_remaining": 0
                }
            )


        # ====================================================
        # INCORRECT BUT CONTINUE
        # ====================================================

        return (
            True,
            {
                "status": "CONTINUE",
                "result": result,
                "attempts_remaining": (
                    self.wordle_max_attempts
                    - len(self.wordle_attempts)
                )
            }
        )


    # ========================================================
    # INTERROGATION
    # ========================================================

    def ask_question(
        self,
        character,
        question_key
    ):

        # ----------------------------------------------------
        # PIN LOCK
        # ----------------------------------------------------

        if not self.pin_cracked:

            return (
                False,
                "🔒 The interrogation system is locked. "
                "Crack the Cafeteria PIN first."
            )


        # ----------------------------------------------------
        # SECURITY CHALLENGE LOCK
        # ----------------------------------------------------

        if self.security_challenge_active:

            return (
                False,
                "🔐 Interrogation is locked. "
                "Complete the secondary security challenge."
            )


        # ----------------------------------------------------
        # FAILED SECURITY CHALLENGE
        # ----------------------------------------------------

        if self.wordle_failed:

            return (
                False,
                "🔐 Interrogation access was blocked "
                "by the security system."
            )


        # ----------------------------------------------------
        # ACTION CHECK
        # ----------------------------------------------------

        if not self.can_act():

            return (
                False,
                "The case is already closed."
            )


        # ----------------------------------------------------
        # ONE QUESTION PER SUSPECT
        # ----------------------------------------------------

        if character in self.asked:

            return (
                False,
                f"You've already questioned {character}."
            )


        # ----------------------------------------------------
        # VALID CHARACTER
        # ----------------------------------------------------

        if character not in case.CHARACTERS:

            return (
                False,
                "Unknown character."
            )


        # ----------------------------------------------------
        # VALID QUESTION
        # ----------------------------------------------------

        if question_key not in case.QUESTION_BANK:

            return (
                False,
                "Unknown question."
            )


        # ====================================================
        # MOLE AI DECIDES TRUTH / LIE
        # ====================================================

        if character == case.MOLE:

            tell_truth = (
                self.mole_ai.decide_truth_or_lie(
                    self.suspicion,
                    game_state=self
                )
            )

            answer = case.get_answer(
                character,
                question_key,
                tell_truth=tell_truth
            )

            lied = not tell_truth

        else:

            answer_data = case.get_question(
                character,
                question_key
            )

            answer = answer_data["answer"]

            lied = False


        # ----------------------------------------------------
        # SAVE STATEMENT
        # ----------------------------------------------------

        self.asked[character] = {

            "question": question_key,

            "answer": answer,

            "lied": lied
        }


        # ----------------------------------------------------
        # SAVE TO EVIDENCE BOARD
        # ----------------------------------------------------

        self.evidence.log_answer(
            character,
            question_key,
            answer,

            # EvidenceBoard stores whether statement
            # is true.
            not lied
        )


        # ====================================================
        # SUSPICION
        # ====================================================

        if character == case.MOLE:

            if lied:

                self.suspicion += 8

                self._log(
                    "⚠️ Zephyr's answer feels rehearsed."
                )

            else:

                self.suspicion -= 2

                self._log(
                    "🔎 Zephyr gave a surprisingly "
                    "straightforward answer."
                )

        else:

            self.suspicion -= 1


        self._clamp_suspicion()


        # ----------------------------------------------------
        # TRACK ACTION
        # ----------------------------------------------------

        self.actions_used += 1


        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        self._log(
            f"💬 Questioned {character}."
        )


        # ====================================================
        # CONTRADICTION DETECTION
        # ====================================================

        try:

            new_contradictions = (
                self.evidence.detect_contradictions()
            )

        except AttributeError:

            new_contradictions = []


        for contradiction in new_contradictions:

            self.contradiction_flagged = True

            self.last_contradiction = (
                contradiction["detail"]
            )

            self._log(
                f"🚨 {contradiction['detail']}"
            )


        return (
            True,
            answer
        )


    # ========================================================
    # FINAL ACCUSATION
    # ========================================================

    def make_accusation(
        self,
        character
    ):

        if self.game_over:

            return (
                False,
                "The case is already closed."
            )


        if character not in case.CHARACTERS:

            return (
                False,
                "Unknown character."
            )


        self.accused = character

        self.game_over = True


        if character == case.MOLE:

            self.result = "win"

        else:

            self.result = "lose"


        self._log(
            f"⚖️ Final accusation: "
            f"{character}."
        )


        return (
            True,
            self.result
        )


    # ========================================================
    # STATS
    # ========================================================

    def get_stats(self):

        return {

            "actions_used":
                self.actions_used,

            "suspicion":
                self.suspicion,

            "result":
                self.result,

            "accused":
                self.accused,

            "contradiction_flagged":
                self.contradiction_flagged,

            "guilt_scores":
                getattr(
                    self.evidence,
                    "guilt_scores",
                    {}
                ),

            "last_contradiction":
                self.last_contradiction,

            "pin_cracked":
                self.pin_cracked,

            "pin_attempts":
                self.pin_attempts,

            "security_challenge_active":
                self.security_challenge_active,

            "security_challenge_complete":
                self.security_challenge_complete,

            "wordle_attempts":
                self.wordle_attempts,

            "wordle_failed":
                self.wordle_failed,

            "mole_ai":
                self.mole_ai.stats()
        }
