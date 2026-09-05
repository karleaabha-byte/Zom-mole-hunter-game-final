"""
Strategic Adversarial Mole AI for Zom-Mole Hunter.

Zephyr is not trying to sabotage everything.

Zephyr's objective is to:
    1. Make the detective's investigation harder.
    2. Avoid becoming too suspicious.
    3. Avoid creating contradictions.
    4. Delay access to useful evidence when it is worth the risk.

The AI is a utility-based agent: for each decision point it scores a
small set of candidate actions with a hand-tuned utility function
(_evaluate_state), applies a one-step penalty representing the
detective's likely counter-response, and picks the candidate with
the highest resulting utility.

Zephyr = utility-maximizing agent
Detective = fixed adversarial-response estimate (not a searched agent)
"""

import random
import copy


class MoleAI:

    def __init__(self, seed=None):

        self.rng = random.Random(seed)

        self.lie_count = 0
        self.truth_count = 0

        self.security_sabotage_count = 0
        self.security_skip_count = 0

        self.decisions_log = []

    # ============================================================
    # GENERAL UTILITY
    # ============================================================

    def _evaluate_state(self, state):

        """
        Evaluate the game from Zephyr's perspective.

        Higher score = better for Zephyr.

        Zephyr wants:
            - lower suspicion
            - less useful evidence for detective
            - fewer contradictions
            - security locked
            - investigation delayed

        Zephyr does NOT simply want maximum sabotage.
        """

        suspicion = getattr(
            state,
            "suspicion",
            10
        )

        score = 0

        # --------------------------------------------------------
        # SUSPICION
        # --------------------------------------------------------

        # Low suspicion is extremely valuable.
        score += (100 - suspicion) * 1.5

        # --------------------------------------------------------
        # CONTRADICTIONS
        # --------------------------------------------------------

        if getattr(
            state,
            "contradiction_flagged",
            False
        ):
            score -= 30

        # --------------------------------------------------------
        # PHYSICAL EVIDENCE
        # --------------------------------------------------------

        storage_found = getattr(state, "storage_evidence_found", False)
        cafe_found = getattr(state, "cafeteria_evidence_found", False)

        if storage_found:
            # Storage evidence is direct physical evidence against Zephyr.
            score -= 35
        else:
            # No Storage evidence means less material for the detective.
            score += 20

        if cafe_found:
            # Cafeteria evidence is always present and therefore must be
            # considered by the interrogation utility evaluation.
            score -= 5

        # --------------------------------------------------------
        # SECURITY
        # --------------------------------------------------------

        if getattr(
            state,
            "security_challenge_active",
            False
        ):
            score += 20

        if getattr(
            state,
            "security_challenge_complete",
            False
        ):
            score -= 10

        if getattr(
            state,
            "wordle_failed",
            False
        ):
            score += 25

        # --------------------------------------------------------
        # INTERROGATION ACCESS
        # --------------------------------------------------------

        if getattr(state, "pin_cracked", False):

            if not getattr(
                state,
                "security_challenge_complete",
                False
            ):

                score += 15

        # --------------------------------------------------------
        # EVIDENCE
        # --------------------------------------------------------

        evidence = getattr(
            state,
            "evidence",
            None
        )

        if evidence is not None:

            guilt_scores = getattr(
                evidence,
                "guilt_scores",
                {}
            )

            if guilt_scores:

                # If Zephyr has accumulated guilt evidence,
                # that is bad for Zephyr.
                try:

                    mole_score = guilt_scores.get(
                        "Zephyr",
                        guilt_scores.get(
                            "zephyr",
                            0
                        )
                    )

                    score -= mole_score * 2

                except Exception:
                    pass

        # --------------------------------------------------------
        # GAME OVER
        # --------------------------------------------------------

        if getattr(
            state,
            "game_over",
            False
        ):

            result = getattr(
                state,
                "result",
                None
            )

            if result == "win":
                score += 1000

            elif result == "lose":
                score -= 1000

        return score

    # ============================================================
    # SAFE STATE COPY
    # ============================================================

    def _copy_state(self, game_state):

        """
        Make a simulation copy.

        The utility evaluation operates on hypothetical states
        and must never modify the real game.
        """

        try:

            return copy.deepcopy(
                game_state
            )

        except Exception:

            return None

    # ============================================================
    # SECURITY / WORDLE
    # ============================================================

    def decide_security_sabotage(
        self,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        """
        Decide whether the hidden secondary security lock activates.

        The player does not know this is a Zephyr decision.  The only
        evidence state that can exist at this point is: 

            Storage FOUND + Cafeteria FOUND
            Storage NOT FOUND + Cafeteria FOUND

        The lock activates only when both physical clues are present.
        Cafeteria evidence is guaranteed; Storage evidence is the only
        randomized clue.
        """

        if game_state is None:
            return False

        storage_found = bool(
            getattr(game_state, "storage_evidence_found", False)
        )
        cafe_found = bool(
            getattr(game_state, "cafeteria_evidence_found", False)
        )

        activate = storage_found and cafe_found

        if activate:
            self.security_sabotage_count += 1
            self.decisions_log.append(
                "Zephyr activated the hidden secondary security lock."
            )
        else:
            self.security_skip_count += 1
            self.decisions_log.append(
                "Zephyr did not activate the hidden secondary security lock."
            )

        return activate

    # ============================================================
    # SECURITY SIMULATION
    # ============================================================

    def _simulate_security_action(
        self,
        state,
        sabotage
    ):

        if state is None:
            return -9999

        try:

            if sabotage:

                # Security lock activates.
                state.security_challenge_active = True

                state.security_challenge_complete = False

                state.suspicion += 7

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                score = self._evaluate_state(
                    state
                )

                # Delaying interrogation is valuable.
                score += 25

                # But obvious tampering is risky.
                score -= 12

                return score

            else:

                # Detective gets immediate interrogation.
                state.security_challenge_active = False

                state.security_challenge_complete = True

                state.suspicion -= 2

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                score = self._evaluate_state(
                    state
                )

                # Losing control of interrogation hurts Zephyr.
                score -= 20

                # But avoiding tampering improves cover.
                score += 12

                return score

        except Exception:

            return self._evaluate_state(
                state
            )

    # ============================================================
    # SECURITY DETECTIVE RESPONSE
    # ============================================================

    def _security_detective_response(
        self,
        state,
        current_score
    ):

        if state is None:

            return current_score

        try:

            if getattr(
                state,
                "security_challenge_active",
                False
            ):

                # Detective can attempt the Wordle.

                solve = current_score - 12

                wait = current_score - 3

                # Detective chooses whichever hurts Zephyr more.
                return min(
                    solve,
                    wait
                )

            else:

                # Detective gets interrogation.

                interrogation = (
                    current_score - 20
                )

                return interrogation

        except Exception:

            return current_score

    # ============================================================
    # EXTRA CHALLENGE COMPATIBILITY
    # ============================================================

    def decide_extra_challenge(
        self,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        return self.decide_security_sabotage(
            suspicion,
            actions_remaining,
            game_state
        )

    # ============================================================
    # TRUTH / LIE
    # ============================================================

    def decide_truth_or_lie(
        self,
        suspicion=None,
        game_state=None
    ):

        """
        Decide whether Zephyr should lie.

        Lying:
            + conceals information
            - increases suspicion
            - can create contradictions

        Truth:
            + reduces suspicion
            - gives detective information
        """

        if game_state is None:

            current_suspicion = (
                suspicion
                if suspicion is not None
                else 10
            )

            if current_suspicion >= 65:

                tell_truth = True

            elif current_suspicion <= 30:

                tell_truth = False

            else:

                tell_truth = (
                    self.rng.random() < 0.5
                )

            self._record_truth(
                tell_truth
            )

            return tell_truth

        # --------------------------------------------------------
        # Simulate LIE
        # --------------------------------------------------------

        lie_state = self._copy_state(
            game_state
        )

        truth_state = self._copy_state(
            game_state
        )

        lie_score = (
            self._simulate_truth_action(
                lie_state,
                False
            )
        )

        truth_score = (
            self._simulate_truth_action(
                truth_state,
                True
            )
        )

        # --------------------------------------------------------
        # Detective response (utility penalty)
        # --------------------------------------------------------

        lie_score = (
            self._interrogation_response(
                lie_state,
                lie_score
            )
        )

        truth_score = (
            self._interrogation_response(
                truth_state,
                truth_score
            )
        )

        # --------------------------------------------------------
        # Zephyr picks the higher-utility action
        # --------------------------------------------------------

        if lie_score > truth_score:

            tell_truth = False

        elif truth_score > lie_score:

            tell_truth = True

        else:

            current_suspicion = getattr(
                game_state,
                "suspicion",
                10
            )

            tell_truth = (
                current_suspicion >= 55
            )

        self._record_truth(
            tell_truth
        )

        return tell_truth

    # ============================================================
    # TRUTH SIMULATION
    # ============================================================

    def _simulate_truth_action(
        self,
        state,
        truth
    ):

        if state is None:
            return -9999

        try:

            if truth:

                state.suspicion -= 2

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                score = self._evaluate_state(
                    state
                )

                # Truth gives detective useful information.
                score -= 10

                if getattr(state, "storage_evidence_found", False):
                    # With Storage evidence present, a truthful alibi gives
                    # the detective a clean comparison point.
                    score -= 15
                else:
                    # Without Storage evidence, truth is less damaging.
                    score -= 5

                # But credibility improves.
                score += 8

                return score

            else:

                state.suspicion += 8

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                score = self._evaluate_state(
                    state
                )

                # A lie conceals useful information.
                score += 15

                if getattr(state, "storage_evidence_found", False):
                    # Storage evidence gives the detective more opportunity
                    # to challenge a lie.
                    score -= 15
                else:
                    # When Storage evidence is absent, a lie is harder to
                    # disprove from physical evidence.
                    score += 8

                # Suspicion is dangerous.
                score -= 18

                # Potential contradiction.
                score -= 8

                return score

        except Exception:

            return self._evaluate_state(
                state
            )

    # ============================================================
    # DETECTIVE RESPONSE TO INTERROGATION
    # ============================================================

    def _interrogation_response(
        self,
        state,
        current_score
    ):

        if state is None:

            return current_score

        try:

            # Detective can compare the answer against
            # existing evidence.

            evidence_check = (
                current_score - 12
            )

            suspicion_check = (
                current_score - 8
            )

            return min(
                evidence_check,
                suspicion_check
            )

        except Exception:

            return current_score

    # ============================================================
    # TRUTH LOGGING
    # ============================================================

    def _record_truth(
        self,
        tell_truth
    ):

        if tell_truth:

            self.truth_count += 1

        else:

            self.lie_count += 1

        self.decisions_log.append(
            "Zephyr chose to "
            f"{'TELL THE TRUTH' if tell_truth else 'LIE'}."
        )

    # ============================================================
    # STATS
    # ============================================================

    def stats(self):

        return {

            "lie_count":
                self.lie_count,

            "truth_count":
                self.truth_count,

            "security_sabotage_count":
                self.security_sabotage_count,

            "security_skip_count":
                self.security_skip_count,

            "decisions_log":
                list(self.decisions_log)
        }
