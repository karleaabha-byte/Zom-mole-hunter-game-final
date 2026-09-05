"""
Strategic Adversarial Mole AI for Zom-Mole Hunter.

Zephyr is not trying to sabotage everything.

Zephyr's objective is to:
    1. Avoid becoming too suspicious.
    2. Avoid creating contradictions.
    3. Adapt his interrogation response to the evidence the detective actually found.
    4. Choose truth or lie when that improves his chances of avoiding detection.

The AI uses depth-limited Minimax.

Zephyr = MAX
Detective = MIN
"""

import random
import copy


class MoleAI:

    def __init__(self, seed=None):

        self.rng = random.Random(seed)

        self.sabotage_count = 0
        self.help_count = 0

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
        # VENTILATION EVIDENCE
        # --------------------------------------------------------

        if getattr(
            state,
            "ventilation_override_found",
            False
        ):
            # Physical evidence of the 11:50 PM override makes
            # Zephyr's position more dangerous.
            score -= 18
        else:
            # Missing evidence leaves Zephyr more room to maneuver.
            score += 8

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

        Minimax operates on hypothetical states and must never
        modify the real game.
        """

        try:

            return copy.deepcopy(
                game_state
            )

        except Exception:

            return None

    # ============================================================
    # ROOM MINIMAX
    # ============================================================

    def decide_help_or_sabotage(
        self,
        action_name,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        """
        Choose whether Zephyr should HELP or SABOTAGE.

        This is the main adversarial decision.

        Zephyr = MAX
        Detective = MIN
        """

        # --------------------------------------------------------
        # No game state
        # --------------------------------------------------------

        if game_state is None:

            # Fall back to strategic suspicion-based behaviour.

            current_suspicion = (
                suspicion
                if suspicion is not None
                else 10
            )

            if current_suspicion >= 70:

                decision = "help"

            elif current_suspicion <= 30:

                decision = "sabotage"

            else:

                decision = (
                    "sabotage"
                    if self.rng.random() < 0.5
                    else "help"
                )

            self._record_decision(
                decision,
                action_name
            )

            return decision

        # --------------------------------------------------------
        # Minimax
        # --------------------------------------------------------

        sabotage_state = self._copy_state(
            game_state
        )

        help_state = self._copy_state(
            game_state
        )

        sabotage_score = self._simulate_room_action(
            sabotage_state,
            "sabotage"
        )

        help_score = self._simulate_room_action(
            help_state,
            "help"
        )

        # --------------------------------------------------------
        # Detective response
        # --------------------------------------------------------

        sabotage_score = self._detective_response(
            sabotage_state,
            sabotage_score
        )

        help_score = self._detective_response(
            help_state,
            help_score
        )

        # --------------------------------------------------------
        # MAX: Zephyr chooses higher score
        # --------------------------------------------------------

        if sabotage_score > help_score:

            decision = "sabotage"

        elif help_score > sabotage_score:

            decision = "help"

        else:

            # Tie breaker:
            # at low suspicion Zephyr is more willing to risk
            # sabotage.
            current_suspicion = getattr(
                game_state,
                "suspicion",
                10
            )

            if current_suspicion < 40:

                decision = "sabotage"

            else:

                decision = "help"

        self._record_decision(
            decision,
            action_name
        )

        return decision

    # ============================================================
    # ROOM SIMULATION
    # ============================================================

    def _simulate_room_action(
        self,
        state,
        action
    ):

        if state is None:
            return -9999

        try:

            if action == "sabotage":

                state.suspicion += 8

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                state.room_decisions[
                    "Storage"
                ] = "riddle_sabotage"

                # Sabotage makes the clue less useful,
                # which is good for Zephyr.
                score = self._evaluate_state(
                    state
                )

                score += 18

                # But tampering itself creates risk.
                score -= 12

                return score

            else:

                state.suspicion -= 3

                state.suspicion = max(
                    0,
                    min(
                        100,
                        state.suspicion
                    )
                )

                state.room_decisions[
                    "Storage"
                ] = "help"

                score = self._evaluate_state(
                    state
                )

                # Helping gives the detective useful information.
                score -= 12

                # But Zephyr's cover improves.
                score += 10

                return score

        except Exception:

            return self._evaluate_state(
                state
            )

    # ============================================================
    # DETECTIVE RESPONSE
    # ============================================================

    def _detective_response(
        self,
        state,
        current_score
    ):

        """
        Detective is MIN.

        The detective prefers outcomes that make Zephyr's
        position worse.

        We model two broad responses:

            1. investigate further
            2. increase suspicion / scrutinize the clue

        """

        if state is None:

            return current_score

        try:

            investigate_score = (
                current_score - 5
            )

            scrutinize_score = (
                current_score - 10
            )

            # MIN chooses the lower value.
            return min(
                investigate_score,
                scrutinize_score
            )

        except Exception:

            return current_score

    # ============================================================
    # STORAGE
    # ============================================================

    def decide_room_action(
        self,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        return self.decide_help_or_sabotage(
            "room investigation",
            suspicion,
            actions_remaining,
            game_state
        )

    # ============================================================
    # RIDDLE COMPATIBILITY
    # ============================================================

    def decide_riddle_sabotage(
        self,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        decision = self.decide_help_or_sabotage(
            "Storage riddle",
            suspicion,
            actions_remaining,
            game_state
        )

        return decision == "sabotage"

    # ============================================================
    # CAFETERIA
    # ============================================================

    def decide_cafeteria_action(
        self,
        suspicion=None,
        actions_remaining=None,
        game_state=None
    ):

        return self.decide_help_or_sabotage(
            "Cafeteria clue",
            suspicion,
            actions_remaining,
            game_state
        )

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
        Decide whether Zephyr should activate the Wordle lock.

        This is an actual adversarial decision.

        Option A:
            Activate Wordle
            + delays interrogation
            - raises suspicion
            - looks like tampering

        Option B:
            Do not activate
            + Zephyr appears cooperative
            - detective gets interrogation access
        """

        # --------------------------------------------------------
        # No game state
        # --------------------------------------------------------

        if game_state is None:

            current_suspicion = (
                suspicion
                if suspicion is not None
                else 10
            )

            # Low suspicion:
            # worth taking the risk.
            if current_suspicion < 45:

                activate = True

            else:

                activate = False

            if activate:

                self.security_sabotage_count += 1

                self.decisions_log.append(
                    "Zephyr chose to "
                    "ACTIVATE THE SECURITY LOCK."
                )

            else:

                self.security_skip_count += 1

                self.decisions_log.append(
                    "Zephyr chose to "
                    "ALLOW INTERROGATION."
                )

            return activate

        # --------------------------------------------------------
        # Simulate both choices
        # --------------------------------------------------------

        sabotage_state = self._copy_state(
            game_state
        )

        help_state = self._copy_state(
            game_state
        )

        sabotage_score = (
            self._simulate_security_action(
                sabotage_state,
                True
            )
        )

        help_score = (
            self._simulate_security_action(
                help_state,
                False
            )
        )

        # --------------------------------------------------------
        # Detective MIN response
        # --------------------------------------------------------

        sabotage_score = (
            self._security_detective_response(
                sabotage_state,
                sabotage_score
            )
        )

        help_score = (
            self._security_detective_response(
                help_state,
                help_score
            )
        )

        # --------------------------------------------------------
        # Zephyr MAX
        # --------------------------------------------------------

        if sabotage_score > help_score:

            activate = True

        elif help_score > sabotage_score:

            activate = False

        else:

            # Tie breaker based on suspicion.
            current_suspicion = getattr(
                game_state,
                "suspicion",
                10
            )

            activate = (
                current_suspicion < 50
            )

        # --------------------------------------------------------
        # Record decision
        # --------------------------------------------------------

        if activate:

            self.security_sabotage_count += 1

            self.decisions_log.append(
                "Zephyr chose to "
                "ACTIVATE THE SECURITY LOCK."
            )

        else:

            self.security_skip_count += 1

            self.decisions_log.append(
                "Zephyr chose to "
                "ALLOW INTERROGATION."
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
        # Detective MIN
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
        # MAX
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

                # But suspicion is dangerous.
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
    # LOGGING
    # ============================================================

    def _record_decision(
        self,
        decision,
        action_name
    ):

        if decision == "sabotage":

            self.sabotage_count += 1

        else:

            self.help_count += 1

        self.decisions_log.append(
            f"Zephyr chose to "
            f"{decision.upper()} during "
            f"{action_name}."
        )

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

            "sabotage_count":
                self.sabotage_count,

            "help_count":
                self.help_count,

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

