"""
Strategic Adversarial Mole AI for Zom-Mole Hunter.

Zephyr is a utility-based agent.

Zephyr's objective is to:
    1. Make the detective's investigation harder.
    2. Avoid becoming too suspicious.
    3. Avoid creating contradictions.
    4. Delay access to useful evidence when it is worth the risk.

For truth/lie decisions, Zephyr simulates both actions,
evaluates the resulting game states, estimates the detective's
response, and chooses the action with the higher utility.

The Storage evidence is randomized elsewhere in the game.
The AI does NOT control that 50/50 event.

Zephyr = utility-maximizing agent
Detective = fixed adversarial-response estimate
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
            - less useful evidence
            - fewer contradictions
            - security locked
            - investigation delayed
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

        storage_found = getattr(
            state,
            "storage_evidence_found",
            False
        )

        cafe_found = getattr(
            state,
            "cafeteria_evidence_found",
            False
        )

        if storage_found:
            # Direct physical evidence is dangerous.
            score -= 35
        else:
            # Keeping Storage evidence hidden is valuable.
            score += 20

        if cafe_found:
            # Cafeteria evidence is weaker than Storage evidence.
            score -= 5

        # --------------------------------------------------------
        # COMBINED EVIDENCE
        # --------------------------------------------------------

        if storage_found and cafe_found:

            # Together, these clues give the detective a much
            # stronger basis for connecting Zephyr to the case.
            score -= 30

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

        if getattr(
            state,
            "pin_cracked",
            False
        ):

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
        Create a hypothetical copy of the game state.

        The real game state is never modified during simulation.
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
        Determine whether the hidden secondary security lock
        should activate.

        IMPORTANT:
        The Storage clue itself is randomized elsewhere.

        The lock activates only when:
            Storage FOUND + Cafeteria FOUND

        Therefore this method does not randomize the Storage clue.
        """

        if game_state is None:
            return False

        storage_found = bool(
            getattr(
                game_state,
                "storage_evidence_found",
                False
            )
        )

        cafe_found = bool(
            getattr(
                game_state,
                "cafeteria_evidence_found",
                False
            )
        )

        activate = (
            storage_found
            and cafe_found
        )

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

                # Activate security lock.
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

                # Obvious tampering is risky.
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

                # Avoiding tampering improves cover.
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

                # Detective can attempt Wordle.

                solve = current_score - 12

                wait = current_score - 3

                # Detective chooses the response that is
                # worse for Zephyr.
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
        Decide whether Zephyr should tell the truth or lie.

        Zephyr simulates BOTH possible actions.

        Truth:
            + decreases suspicion
            + preserves credibility
            - gives the detective useful information

        Lie:
            + conceals information
            + can protect Zephyr when evidence is strong
            - increases suspicion
            - may create contradictions

        The final decision is made by comparing utility.
        """

        # --------------------------------------------------------
        # FALLBACK WHEN NO GAME STATE IS AVAILABLE
        # --------------------------------------------------------

        if game_state is None:

            current_suspicion = (
                suspicion
                if suspicion is not None
                else 10
            )

            if current_suspicion >= 65:

                # At extremely high suspicion, lying can be
                # dangerous without enough state information.
                tell_truth = True

            elif current_suspicion <= 30:

                # At low suspicion, lying is relatively safe.
                tell_truth = False

            else:

                # No evidence state is available, so use a
                # controlled 50/50 fallback.
                tell_truth = (
                    self.rng.random() < 0.5
                )

            self._record_truth(
                tell_truth
            )

            return tell_truth

        # --------------------------------------------------------
        # COPY REAL STATE
        # --------------------------------------------------------

        lie_state = self._copy_state(
            game_state
        )

        truth_state = self._copy_state(
            game_state
        )

        # --------------------------------------------------------
        # SIMULATE LIE
        # --------------------------------------------------------

        lie_score = self._simulate_truth_action(
            lie_state,
            False
        )

        # --------------------------------------------------------
        # SIMULATE TRUTH
        # --------------------------------------------------------

        truth_score = self._simulate_truth_action(
            truth_state,
            True
        )

        # --------------------------------------------------------
        # DETECTIVE RESPONSE
        # --------------------------------------------------------

        lie_score = self._interrogation_response(
            lie_state,
            lie_score
        )

        truth_score = self._interrogation_response(
            truth_state,
            truth_score
        )

        # --------------------------------------------------------
        # CHOOSE HIGHER UTILITY
        # --------------------------------------------------------

        if lie_score > truth_score:

            tell_truth = False

        elif truth_score > lie_score:

            tell_truth = True

        else:

            # Only use suspicion as a tie-breaker.
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
    # TRUTH / LIE SIMULATION
    # ============================================================

    def _simulate_truth_action(
        self,
        state,
        truth
    ):

        if state is None:
            return -9999

        try:

            storage_found = getattr(
                state,
                "storage_evidence_found",
                False
            )

            cafe_found = getattr(
                state,
                "cafeteria_evidence_found",
                False
            )

            # ====================================================
            # TRUTH
            # ====================================================

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

                # Truth gives useful information.
                score -= 10

                if storage_found:

                    # A truthful answer gives the detective
                    # a clean comparison against the physical clue.
                    score -= 15

                else:

                    # Without Storage evidence, truth is
                    # comparatively less dangerous.
                    score -= 5

                # Credibility benefit.
                score += 8

                # ------------------------------------------------
                # COMBINED EVIDENCE
                # ------------------------------------------------

                if storage_found and cafe_found:

                    # Once BOTH clues are available, being truthful
                    # makes the detective's case easier.
                    score -= 30

                return score

            # ====================================================
            # LIE
            # ====================================================

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

                if storage_found:

                    # Storage evidence allows the detective
                    # to challenge the lie.
                    score -= 15

                else:

                    # Without Storage evidence, the lie is
                    # harder to disprove.
                    score += 8

                # Suspicion is dangerous.
                score -= 18

                # Potential contradiction.
                score -= 8

                # ------------------------------------------------
                # STRATEGIC VALUE OF LYING
                # ------------------------------------------------

                if storage_found and cafe_found:

                    # BOTH clues are now available.
                    #
                    # At this point Zephyr has strong reason to
                    # conceal information rather than voluntarily
                    # strengthen the detective's case.
                    #
                    # This is a utility bonus, NOT a hard-coded
                    # "always lie" rule.
                    score += 45

                elif storage_found:

                    # With only Storage evidence, lying has
                    # some strategic value but is riskier.
                    score += 10

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

            # Detective compares the answer against
            # existing evidence.

            evidence_check = (
                current_score - 12
            )

            suspicion_check = (
                current_score - 8
            )

            # Detective chooses the response that
            # hurts Zephyr more.
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
