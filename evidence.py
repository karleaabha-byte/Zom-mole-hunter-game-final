


class EvidenceBoard:

    def __init__(self):

        # Physical clues discovered
        self.clues_found = set()

        # Statements collected
        self.suspect_statements = {}

        # Optional detective notes
        self.notes = []

        # PIN progress
        self.pin_cracked = False

        # Kept for compatibility with the existing app/game
        self.guilt_scores = {}

    # ========================================================
    # CLUES
    # ========================================================

    def add_clue(self, clue_name):

        if clue_name in self.clues_found:
            return False

        self.clues_found.add(clue_name)

        return True

    def has_clue(self, clue_name):

        return clue_name in self.clues_found

    # ========================================================
    # STATEMENTS
    # ========================================================

    def log_answer(
        self,
        character,
        question_key,
        answer,
        truth
    ):

        if character not in self.suspect_statements:
            self.suspect_statements[character] = {}

        self.suspect_statements[character][question_key] = {
            "answer": answer,
            "truth": truth
        }

    def get_statement(
        self,
        character,
        question_key
    ):

        return (
            self.suspect_statements
            .get(character, {})
            .get(question_key)
        )

    # ========================================================
    # CONTRADICTIONS
    # ========================================================

    def detect_contradictions(self):
        """
        The new game uses a simple deduction system.

        We intentionally do not automatically tell the player
        who is lying. The player should compare statements with
        the physical evidence themselves.
        """

        return []

    # ========================================================
    # NOTES
    # ========================================================

    def add_note(self, note):

        note = note.strip()

        if not note:
            return False

        self.notes.append(note)

        return True

    # ========================================================
    # PIN
    # ========================================================

    def set_pin_cracked(self):

        self.pin_cracked = True

    # ========================================================
    # SUMMARY
    # ========================================================

    def get_summary(self):

        return {
            "clues_found": list(self.clues_found),
            "suspect_statements": self.suspect_statements,
            "notes": self.notes,
            "pin_cracked": self.pin_cracked,
            "contradictions": []
        }
