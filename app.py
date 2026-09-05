import html
import streamlit as st
import case

from game import GameState, ROOMS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Zom-Mole Hunter",
    page_icon="🧟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# NOIR AESTHETIC
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #1a0f2e 0%,
                #2d1b4e 50%,
                #1f1135 100%
            );
        color: #e0d5d5;
    }

    body {
        font-family: Georgia, serif;
    }

    h1 {
        color: #d4af37;
        font-family: monospace;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        letter-spacing: 3px;
    }

    h2,
    h3 {
        color: #f39c12;
        font-family: monospace;
        text-shadow: 0 0 8px rgba(243, 156, 18, 0.4);
    }

    /* ========================================================
       TABS
       ======================================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #3d2860;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        color: #c9a961;
        font-family: monospace;
        border: 1px solid #5a3d8a;
    }

    .stTabs [aria-selected="true"] {
        background-color: #5a3d8a !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37;
    }

    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid #5a3d8a;
        border-radius: 10px;
        background-color: #2d1f42;
    }

    /* ========================================================
       METRICS
       ======================================================== */

    div[data-testid="stMetricValue"] {
        color: #f39c12;
        font-size: 1.8rem;
        font-family: monospace;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #5a3d8a;
        color: #d4af37;
        border-radius: 8px;
        border: 1.5px solid #d4af37;
        font-family: monospace;
        font-weight: bold;
        box-shadow: 0 0 8px rgba(212, 175, 55, 0.3);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #d4af37;
        color: #1a0f2e;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }

    /* ========================================================
       CASE FILE
       ======================================================== */

    .case-file {
        background: rgba(45, 31, 66, 0.85);
        border: 1px solid #5a3d8a;
        border-left: 4px solid #d4af37;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.35);
    }

    /* ========================================================
       BACKGROUND
       ======================================================== */

    .background-section {
        background: #2d1f42;
        border: 1px solid #5a3d8a;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        font-family: monospace;
    }

    .background-title {
        color: #d4af37;
        font-weight: bold;
        margin-bottom: 12px;
        font-size: 1rem;
        letter-spacing: 1px;
    }

    .background-entry {
        color: #c9a961;
        padding: 8px 0;
        border-bottom: 1px dotted #5a3d8a;
        line-height: 1.5;
    }

    /* ========================================================
       START SCREEN
       ======================================================== */

    .game-title-main {
        color: #d4af37;
        font-family: monospace;
        font-size: 3.2rem;
        font-weight: bold;
        letter-spacing: 6px;
        text-align: center;
        text-shadow:
            0 0 10px rgba(212, 175, 55, 0.5),
            0 0 25px rgba(212, 175, 55, 0.2);
        padding-top: 35px;
    }

    .game-title-sub {
        color: #c9a961;
        font-family: monospace;
        font-size: 1rem;
        letter-spacing: 3px;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 25px;
    }

    .opening-story {
        background: rgba(26, 16, 36, 0.92);
        border: 1px solid #5a3d8a;
        border-left: 4px solid #d4af37;
        border-radius: 8px;
        padding: 30px;
        margin: 20px 0;
        line-height: 1.8;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }

    .opening-label {
        color: #d4af37;
        font-family: monospace;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }

    .opening-warning {
        color: #f39c12;
        font-family: monospace;
        font-weight: bold;
        border-top: 1px solid #5a3d8a;
        border-bottom: 1px solid #5a3d8a;
        padding: 15px 0;
        margin: 18px 0;
        text-align: center;
        letter-spacing: 1px;
    }

    /* ========================================================
       UNLOCKED ACCESS
       ======================================================== */

    .unlock-box {
        background: #21152d;
        border: 2px solid #d4af37;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);
    }

    .unlock-title {
        color: #d4af37;
        font-family: monospace;
        font-weight: bold;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }

    /* ========================================================
       LOCKED INTERROGATION
       ======================================================== */

    .locked-box {
        background: #21152d;
        border: 1px solid #705d7d;
        border-left: 4px solid #725b7b;
        border-radius: 8px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
    }

    .locked-title {
        color: #c9a961;
        font-family: monospace;
        font-weight: bold;
        font-size: 1.2rem;
        letter-spacing: 1px;
    }

    /* ========================================================
       SECURITY CHALLENGE
       ======================================================== */

    .security-box {
        background: #21152d;
        border: 2px solid #d4af37;
        border-left: 5px solid #f39c12;
        border-radius: 8px;
        padding: 28px;
        margin: 20px 0;
        text-align: center;
        box-shadow:
            0 0 20px rgba(212, 175, 55, 0.12),
            0 5px 25px rgba(0, 0, 0, 0.35);
    }

    .security-title {
        color: #d4af37;
        font-family: monospace;
        font-size: 1.35rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .security-warning {
        color: #f39c12;
        font-family: monospace;
        font-weight: bold;
        letter-spacing: 1px;
        margin: 12px 0;
    }

    .security-word {
        color: #d4af37;
        font-family: monospace;
        font-size: 1.8rem;
        font-weight: bold;
        letter-spacing: 7px;
        margin: 20px 0;
    }

    .security-attempt {
        color: #c9a961;
        font-family: monospace;
        font-size: 0.9rem;
        margin-top: 10px;
    }

    /* ========================================================
       LAB NOTE
       ======================================================== */

    .note-card {
        background: #f4ecd8;
        color: #3a3226;
        font-family: Georgia, serif;
        padding: 25px;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
        transform: rotate(-1deg);
        margin: 14px 4px;
        line-height: 1.9;
        font-size: 1.05rem;
    }

    .note-line {
        margin: 7px 0;
    }

    /* ========================================================
       STORAGE RIDDLE
       ======================================================== */

    .riddle-board {
        background-color: #10151f;
        background-image:
            linear-gradient(
                #1c2434 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                #1c2434 1px,
                transparent 1px
            );
        background-size: 22px 22px;
        color: #e5e7eb;
        font-family: Georgia, serif;
        font-size: 1.1rem;
        padding: 24px;
        border-radius: 8px;
        border: 2px solid #334155;
        line-height: 1.8;
        margin: 14px 4px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }

    .riddle-line {
        margin: 5px 0;
    }

    .riddle-question {
        color: #f1f5f9;
        font-style: italic;
        margin-top: 14px;
    }

    /* ========================================================
       RECEIPT
       ======================================================== */

    .receipt {
        background: #fdfdfd;
        color: #111;
        font-family: "Courier New", monospace;
        padding: 20px;
        border: 1px dashed #777;
        max-width: 340px;
        margin: 14px auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
    }

    .receipt-title {
        text-align: center;
        font-weight: bold;
        margin-bottom: 12px;
        border-bottom: 1px dashed #777;
        padding-bottom: 8px;
    }

    .pin-display {
        margin-top: 12px;
        font-size: 1.2rem;
        font-weight: bold;
    }

    .pin-digit {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 34px;
        margin: 0 3px;
        border-bottom: 2px solid #333;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .pin-redacted {
        color: #999;
    }

    /* ========================================================
       STATEMENTS
       ======================================================== */

    .statement-card {
        background: #241936;
        border-left: 4px solid #d4af37;
        border-radius: 6px;
        padding: 16px;
        margin: 12px 0;
    }

    .statement-character {
        color: #d4af37;
        font-family: monospace;
        font-weight: bold;
        font-size: 1rem;
    }

    .statement-question {
        color: #9d8ca8;
        font-size: 0.85rem;
        margin-top: 8px;
    }

    .statement-answer {
        color: #f0e7d8;
        font-family: Georgia, serif;
        font-size: 1.15rem;
        line-height: 1.5;
        margin-top: 8px;
    }

    /* ========================================================
       SUSPECT
       ======================================================== */

    .suspect-card {
        background: #3d2860;
        border-left: 4px solid #f39c12;
        padding: 15px;
        margin: 8px 0;
        border-radius: 4px;
    }

    /* ========================================================
       QUOTE
       ======================================================== */

    .quote-box {
        background: #1a1024;
        border-left: 3px solid #d4af37;
        padding: 18px;
        margin: 12px 0;
        font-family: Georgia, serif;
        font-size: 1.2rem;
        line-height: 1.5;
        color: #f0e7d8;
    }

    /* ========================================================
       LOG
       ======================================================== */

    .case-log-scroll {
        height: 280px;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 10px 12px;
        background: #21152d;
        border: 1px solid #5a3d8a;
        border-radius: 7px;
        scrollbar-width: thin;
    }

    .log-entry {
        font-family: monospace;
        font-size: 0.85rem;
        color: #c9a961;
        padding: 7px 0;
        border-bottom: 1px dotted #5a3d8a;
        line-height: 1.4;
    }

    /* ========================================================
       CLUE CHIP
       ======================================================== */

    .clue-chip {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border: 1px solid #725b7b;
        color: #d8c9dc;
        background: #201825;
        font-size: 0.75rem;
        border-radius: 4px;
    }

    /* ========================================================
       FINAL REPORT
       ======================================================== */

    .verdict-box {
        background: #21152d;
        border: 2px solid #d4af37;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
    }

    .result-open {
        background: #21152d;
        border: 1px solid #5a3d8a;
        border-left: 4px solid #c9a961;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = GameState()

if "detective_name" not in st.session_state:
    st.session_state.detective_name = ""

if "case_started" not in st.session_state:
    st.session_state.case_started = False

if "final_evidence_saved" not in st.session_state:
    st.session_state.final_evidence_saved = []

if "final_reasoning_saved" not in st.session_state:
    st.session_state.final_reasoning_saved = ""

if "pin_result" not in st.session_state:
    st.session_state.pin_result = None

if "storage_code_result" not in st.session_state:
    st.session_state.storage_code_result = None


game = st.session_state.game


# ============================================================
# ROOM DESCRIPTIONS
# IMPORTANT: DEFINE THIS BEFORE IT IS USED ANYWHERE.
# ============================================================

room_descriptions = {
    "Laboratory":
        "The centrifuge room where the incident began.",

    "Storage":
        "Shelves, the ventilation system and a strange riddle.",

    "Cafeteria":
        "A vending machine, a restocking cart and one suspicious receipt.",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_html(value):
    return html.escape(str(value))


def get_profile(character):

    profiles = getattr(case, "PROFILES", {})

    if isinstance(profiles, dict):
        return profiles.get(character, {})

    return {}


def get_question_text(question_key):

    questions = getattr(case, "QUESTION_BANK", {})

    if isinstance(questions, dict):
        return questions.get(
            question_key,
            question_key
        )

    return str(question_key)


def get_statement_data(character):

    statements = getattr(
        game.evidence,
        "suspect_statements",
        {}
    )

    if not isinstance(statements, dict):
        return {}

    value = statements.get(
        character,
        {}
    )

    if isinstance(value, dict):
        return value

    return {}


def statement_count():

    total = 0

    statements = getattr(
        game.evidence,
        "suspect_statements",
        {}
    )

    if not isinstance(statements, dict):
        return 0

    for value in statements.values():

        if isinstance(value, dict):
            total += len(value)

        elif value:
            total += 1

    return total


# ============================================================
# CASE LOG FILTER
# ============================================================

def clean_case_log():

    """
    Removes player-facing references to internal mechanics.

    The player should NEVER see:
    - 50/50 mechanics
    - random/chance mechanics
    - probability/roll information
    - the BREEZE answer
    - messages saying BREEZE unlocks another clue
    - storage-answer mechanics
    - internal storage discovery messages
    """

    hidden_terms = (
        "50/50",
        "50-50",
        "50–50",
        "random",
        "chance",
        "probability",
        "roll",
        "solve breeze",
        "breeze",
        "storage riddle discovered",
        "storage answer",
        "riddle answer",
        "correct code",
        "code correct",
        "pin correct",
        "pin cracked",
        "security word",
        "wordle",
    )

    cleaned = []

    for entry in getattr(game, "log", []):

        text = str(entry)
        lower_text = text.lower()

        if any(
            term in lower_text
            for term in hidden_terms
        ):
            continue

        cleaned.append(text)

    return cleaned


# ============================================================
# LAB RENDERER
# ============================================================

def render_lab_note(lines):

    html_output = '<div class="note-card">'

    for item in lines:

        if isinstance(item, str):

            text = item

        elif (
            isinstance(item, (list, tuple))
            and len(item) >= 2
        ):

            text = f"{item[0]}{item[1]}"

        elif isinstance(item, dict):

            text = item.get(
                "text",
                item.get("content", "")
            )

            if item.get("letter"):

                text = (
                    f'{item["letter"]}'
                    f'{text}'
                )

        else:

            text = str(item)

        html_output += (
            '<div class="note-line">'
            f'{safe_html(text)}'
            '</div>'
        )

    html_output += "</div>"

    st.html(html_output)


# ============================================================
# STORAGE RIDDLE
# ============================================================

def render_storage_riddle(riddle):

    html_output = '<div class="riddle-board">'

    for index, line in enumerate(riddle):

        if index == len(riddle) - 1:

            html_output += (
                '<div class="riddle-question">'
                f'{safe_html(line)}'
                '</div>'
            )

        else:

            html_output += (
                '<div class="riddle-line">'
                f'{safe_html(line)}'
                '</div>'
            )

    html_output += "</div>"

    st.html(html_output)


# ============================================================
# CAFETERIA RECEIPT
# ============================================================

def render_receipt(
    job,
    pin_digits,
    redacted
):

    if isinstance(
        pin_digits,
        (list, tuple)
    ):

        digits = list(pin_digits)

    else:

        digits = list(
            str(pin_digits)
        )

    if isinstance(
        redacted,
        str
    ):

        redacted_values = [
            char in ("?", "x", "X", "*")
            for char in redacted
        ]

    elif isinstance(
        redacted,
        (list, tuple)
    ):

        redacted_values = list(
            redacted
        )

    else:

        redacted_values = []

    html_output = (
        '<div class="receipt">'
    )

    html_output += (
        '<div class="receipt-title">'
        'RESTOCKING LOG — MACHINE #3'
        '</div>'
    )

    html_output += (
        '<div>'
        'Restocked by: '
        f'<b>{safe_html(job)}</b>'
        '</div>'
    )

    html_output += (
        '<div class="pin-display">'
        'Employee PIN: '
    )

    for index, digit in enumerate(
        digits
    ):

        is_redacted = (
            index < len(redacted_values)
            and bool(
                redacted_values[index]
            )
        )

        if is_redacted:

            html_output += (
                '<span class="pin-digit '
                'pin-redacted">'
                '?'
                '</span>'
            )

        else:

            html_output += (
                '<span class="pin-digit">'
                f'{safe_html(digit)}'
                '</span>'
            )

    html_output += "</div>"
    html_output += "</div>"

    st.html(html_output)


# ============================================================
# GENERIC CLUE RENDERER
# ============================================================

def render_clue(
    room,
    clue
):

    if not isinstance(clue, dict):

        st.write(clue)

        return

    # ========================================================
    # LABORATORY
    # ========================================================

    if room == "Laboratory":

        if clue.get("title"):

            st.markdown(
                f"### "
                f"{safe_html(clue['title'])}"
            )

        if clue.get("lines"):

            render_lab_note(
                clue["lines"]
            )

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )

    # ========================================================
    # STORAGE
    # ========================================================

    elif room == "Storage":

        if clue.get("title"):

            st.markdown(
                f"### "
                f"{safe_html(clue['title'])}"
            )

        if "CORRUPTED" in str(
            clue.get("title", "")
        ).upper():

            st.warning(
                "⚠️ The Storage terminal has been "
                "tampered with. The original riddle "
                "appears to have been replaced."
            )

        if clue.get("riddle"):

            render_storage_riddle(
                clue["riddle"]
            )

        # IMPORTANT:
        # Do NOT reveal what solving the riddle
        # discovers. The player must infer its
        # significance from the evidence.

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )

    # ========================================================
    # CAFETERIA
    # ========================================================

    elif room == "Cafeteria":

        if clue.get("title"):

            st.markdown(
                f"### "
                f"{safe_html(clue['title'])}"
            )

        if all(
            key in clue
            for key in (
                "job",
                "pin_digits",
                "redacted"
            )
        ):

            render_receipt(
                clue["job"],
                clue["pin_digits"],
                clue["redacted"]
            )

        if clue.get("note"):

            st.info(
                clue["note"]
            )

        if clue.get("description"):

            st.write(
                clue["description"]
            )


# ============================================================
# INTERNAL LOG CLEANUP
# ============================================================

def clean_internal_log():

    if not hasattr(game, "log"):
        return

    hidden_terms = (
        "50/50",
        "50-50",
        "50–50",
        "random",
        "chance",
        "probability",
        "roll",
        "solve breeze",
        "breeze",
        "storage riddle discovered",
        "storage answer",
        "riddle answer",
        "correct code",
        "code correct",
        "pin correct",
        "pin cracked",
        "security word",
        "wordle",
    )

    game.log = [
        entry
        for entry in game.log
        if not any(
            term in str(entry).lower()
            for term in hidden_terms
        )
    ]


# ============================================================
# RESET CASE
# ============================================================

def reset_case():

    st.session_state.game = GameState()

    st.session_state.detective_name = ""

    st.session_state.case_started = False

    st.session_state.final_evidence_saved = []

    st.session_state.final_reasoning_saved = ""

    st.session_state.pin_result = None

    st.session_state.storage_code_result = None

    keys_to_remove = [
        "final_reasoning",
        "final_suspect",
        "final_evidence",
        "pin_guess",
        "start_detective_name",
        "wordle_guess",
        "storage_riddle_answer",
    ]

    for key in keys_to_remove:

        if key in st.session_state:

            del st.session_state[key]


# ============================================================
# OPENING SCREEN
# ============================================================

if not st.session_state.case_started:

    st.html(
        """
        <div class="game-title-main">
            🧟 ZOM-MOLE HUNTER
        </div>

        <div class="game-title-sub">
            A NOIR DETECTIVE INVESTIGATION
        </div>
        """
    )

    st.html(
        """
        <div class="opening-story">

            <div class="opening-label">
                📁 CASE FILE
            </div>

            <div class="opening-label">
                CLASSIFIED — NIGHT SHIFT INVESTIGATION
            </div>

            <h2>
                THE NIGHT SHIFT INCIDENT
            </h2>

            <p>
                <b>12:18 AM.</b>
            </p>

            <p>
                The research facility should have been asleep.
            </p>

            <p>
                Instead, emergency lights are flashing,
                a laboratory alarm is screaming through the
                corridors, and six experimental filter
                cartridges have disappeared from Storage.
            </p>

            <p>
                At first, security believed it was an
                equipment failure.
            </p>

            <p>
                Then they found the broken vial.
            </p>

            <p>
                Then the ventilation panel.
            </p>

            <p>
                Then someone noticed that three minutes of
                corridor camera footage had vanished.
            </p>

            <div class="opening-warning">
                FIVE PEOPLE WERE STILL INSIDE THE FACILITY.
            </div>

            <p>
                One of them is lying.
            </p>

            <p>
                Possibly more than one.
            </p>

            <p>
                But finding a liar is not enough.
                You need to determine which lie actually
                connects to the missing materials.
            </p>

            <p>
                Search the rooms. Examine the evidence.
                Crack the restricted access PIN.
                Interrogate the employees.
                Then decide who is the Mole.
            </p>

        </div>
        """
    )

    st.write("")

    st.html(
        """
        <div
            style="
                color:#d4af37;
                font-family:monospace;
                font-weight:bold;
                font-size:1.15rem;
                letter-spacing:2px;
                margin-top:25px;
                margin-bottom:12px;
            "
        >
            🕵️ IDENTIFY YOURSELF
        </div>
        """
    )

    detective_name = st.text_input(
        "Enter your detective name",
        placeholder="e.g. Detective Morgan",
        key="start_detective_name",
    )

    st.write("")

    if st.button(
        "🔎 ENTER THE CASE",
        use_container_width=True,
    ):

        if not detective_name.strip():

            st.warning(
                "Enter your detective name before beginning."
            )

        else:

            st.session_state.detective_name = (
                detective_name.strip()
            )

            st.session_state.case_started = True

            st.rerun()

    st.stop()


# ============================================================
# GAME TITLE
# ============================================================

st.title(
    "🧟 ZOM-MOLE HUNTER"
)

st.markdown(
    f"""
    <div style="
        height: 48px;
        color: rgba(255,255,255,0.65);
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 8px;
    ">
        {safe_html(
            room_descriptions.get(
                getattr(game, "current_room", ""),
                "A location inside the facility."
            )
        )}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "CASE DOSSIER"
    )

    st.write(
        f"**Detective:** "
        f"{st.session_state.detective_name}"
    )

    st.divider()

    st.subheader(
        "Investigation"
    )

    st.write(
        f"🏚️ Scenes searched: "
        f"**{len(game.visited_rooms)}/{len(ROOMS)}**"
    )

    st.write(
        f"🗣️ Statements collected: "
        f"**{statement_count()}**"
    )

    st.write(
        f"🔎 Physical clues: "
        f"**{len(game.evidence.clues_found)}**"
    )

    # ========================================================
    # SECURITY STATUS
    # ========================================================

    if not game.pin_cracked:

        st.warning(
            "🔒 Interrogations locked"
        )

    elif game.security_challenge_active:

        st.error(
            "🔐 Security challenge active"
        )

    elif game.wordle_failed:

        st.error(
            "🔐 Interrogation access blocked"
        )

    else:

        st.success(
            "🔓 Interrogations unlocked"
        )

    st.divider()

    # ========================================================
    # CASE LOG
    # ========================================================

    with st.expander(
        "📋 CASE LOG"
    ):

        visible_log = clean_case_log()

        if visible_log:

            st.html(
                '<div class="case-log-scroll">'
                +
                "".join(
                    '<div class="log-entry">'
                    f'• {safe_html(entry)}'
                    '</div>'
                    for entry in reversed(
                        visible_log
                    )
                )
                +
                '</div>'
            )

        else:

            st.write(
                "*No entries yet.*"
            )

    st.divider()

    if st.button(
        "🔄 START NEW CASE",
        use_container_width=True
    ):

        reset_case()

        st.rerun()


# ============================================================
# CASE INTRO
# ============================================================

st.markdown(
    '<div class="case-file">',
    unsafe_allow_html=True
)

case_intro = getattr(
    case,
    "CASE_INTRO",
    "A mysterious incident has occurred."
)

st.markdown(
    case_intro
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# MAIN GAME TABS
# ============================================================

(
    tab_background,
    tab_rooms,
    tab_people,
    tab_accuse,
    tab_result,
) = st.tabs(
    [
        "📋 BACKGROUND",
        "🏚️ CRIME SCENES",
        "🗣️ INTERROGATIONS",
        "⚖️ ACCUSATION",
        "📁 RESULT",
    ]
)


# ============================================================
# BACKGROUND TAB
# ============================================================

with tab_background:

    st.subheader(
        "THE NIGHT SHIFT INCIDENT"
    )

    st.write(
        "These are the established facts of the case. "
        "Pay attention to times, locations and who had "
        "access to what."
    )

    background = getattr(
        case,
        "BACKGROUND",
        {}
    )

    if isinstance(
        background,
        dict
    ):

        for section, section_data in background.items():

            html_output = (
                '<div class="background-section">'
                '<div class="background-title">'
                f'{safe_html(section)}'
                '</div>'
            )

            if isinstance(
                section_data,
                dict
            ):

                if "entries" in section_data:

                    for entry in section_data["entries"]:

                        if (
                            isinstance(
                                entry,
                                (list, tuple)
                            )
                            and len(entry) >= 2
                        ):

                            label = entry[0]
                            text = entry[1]

                            html_output += (
                                '<div class="background-entry">'
                                f'<strong>{safe_html(label)}</strong>'
                                '&nbsp; '
                                f'{safe_html(text)}'
                                '</div>'
                            )

                        else:

                            html_output += (
                                '<div class="background-entry">'
                                f'{safe_html(entry)}'
                                '</div>'
                            )

                if "notes" in section_data:

                    for note_text in section_data["notes"]:

                        html_output += (
                            '<div class="background-entry">'
                            f'• {safe_html(note_text)}'
                            '</div>'
                        )

            else:

                html_output += (
                    '<div class="background-entry">'
                    f'{safe_html(section_data)}'
                    '</div>'
                )

            html_output += "</div>"

            st.html(
                html_output
            )

    else:

        st.write(
            background
        )


# ============================================================
# CRIME SCENES
# ============================================================

with tab_rooms:

    st.subheader(
        "🏚️ Crime Scenes"
    )

    st.write(
        "Investigate the facility rooms and examine "
        "whatever evidence you can find."
    )

    cols = st.columns(
        len(ROOMS)
    )

    for col, room in zip(
        cols,
        ROOMS
    ):

        with col:

            st.markdown(
                f"### {safe_html(room)}"
            )

            st.caption(
                room_descriptions.get(
                    room,
                    "A location inside the facility."
                )
            )

            # =================================================
            # INVESTIGATED
            # =================================================

            if room in game.visited_rooms:

                st.success(
                    "✓ Location investigated"
                )

                clue = game.visited_rooms[room]

                render_clue(
                    room,
                    clue
                )

                # =================================================
                # STORAGE RIDDLE
                # =================================================

                if (
                    room == "Storage"
                    and not game.storage_riddle_solved
                ):

                    st.divider()

                    st.markdown(
                        "**🧩 Solve the Storage Riddle**"
                    )

                    storage_answer = st.text_input(
                        "What is the answer?",
                        key="storage_riddle_answer"
                    )

                    if st.button(
                        "🔎 SUBMIT RIDDLE ANSWER",
                        key="submit_storage_riddle",
                        use_container_width=True,
                    ):

                        success, result = (
                            game.solve_storage_riddle(
                                storage_answer
                            )
                        )

                        # -----------------------------------------
                        # CORRECT
                        # -----------------------------------------

                        if success:

                            game.storage_riddle_solved = True

                            st.session_state.storage_code_result = (
                                "correct"
                            )

                            clean_internal_log()

                            st.rerun()

                        # -----------------------------------------
                        # INCORRECT
                        # -----------------------------------------

                        else:

                            st.session_state.storage_code_result = (
                                "incorrect"
                            )

                            st.rerun()

                # =================================================
                # STORAGE RESULT
                #
                # Do NOT reveal the actual evidence here.
                # The solved riddle should simply become another
                # piece of evidence for the detective to interpret.
                # =================================================

                if (
                    room == "Storage"
                    and st.session_state.storage_code_result
                    == "correct"
                ):

                    st.success(
                        "✓ RIDDLE SOLVED"
                    )

                    st.info(
                        "The terminal accepts the entry. "
                        "Whatever was hidden behind the corrupted "
                        "record is now part of the case file."
                    )

                elif (
                    room == "Storage"
                    and st.session_state.storage_code_result
                    == "incorrect"
                ):

                    st.error(
                        "✗ INCORRECT ENTRY"
                    )

                # =================================================
                # CAFETERIA PIN
                # =================================================

                if room == "Cafeteria":

                    st.divider()

                    st.markdown(
                        "**🔐 Crack the Employee PIN**"
                    )

                    # ------------------------------------------------
                    # PIN RESULT
                    # ------------------------------------------------

                    if (
                        st.session_state.pin_result
                        == "incorrect"
                    ):

                        st.error(
                            "✗ PIN INCORRECT"
                        )

                    # ------------------------------------------------
                    # PIN CRACKED
                    # ------------------------------------------------

                    if game.pin_cracked:

                        # --------------------------------------------
                        # SECURITY CHALLENGE ACTIVE
                        # --------------------------------------------

                        if game.security_challenge_active:

                            st.html(
                                """
                                <div class="security-box">

                                    <div class="security-title">
                                        🔐 SECONDARY SECURITY LOCK
                                    </div>

                                    <div class="security-warning">
                                        ADDITIONAL VERIFICATION REQUIRED
                                    </div>

                                    <p>
                                        The restricted system is requesting
                                        an additional verification step.
                                    </p>

                                    <p>
                                        <b>
                                            Further access is currently locked.
                                        </b>
                                    </p>

                                </div>
                                """
                            )

                        # --------------------------------------------
                        # FULL ACCESS
                        # --------------------------------------------

                        else:

                            st.html(
                                """
                                <div class="unlock-box">

                                    <div class="unlock-title">
                                        🔓 RESTRICTED ACCESS GRANTED
                                    </div>

                                    <p>
                                        The restricted employee records
                                        are now accessible.
                                    </p>

                                    <p>
                                        The recovered record can be
                                        compared against the physical
                                        evidence and witness statements.
                                    </p>

                                    <p>
                                        <b>
                                            INTERROGATION SYSTEM: ONLINE
                                        </b>
                                    </p>

                                </div>
                                """
                            )

                    # ------------------------------------------------
                    # PIN NOT CRACKED
                    # ------------------------------------------------

                    else:

                        pin_guess = st.text_input(
                            "Enter four digits",
                            max_chars=4,
                            key="pin_guess",
                            disabled=not game.can_act(),
                        )

                        if st.button(
                            "🔓 VERIFY PIN",
                            key="verify_pin",
                            use_container_width=True,
                            disabled=not game.can_act(),
                        ):

                            pin_correct = game.attempt_pin(
                                pin_guess
                            )

                            if pin_correct:

                                st.session_state.pin_result = (
                                    "correct"
                                )

                            else:

                                st.session_state.pin_result = (
                                    "incorrect"
                                )

                            clean_internal_log()

                            st.rerun()

                        st.caption(
                            "PIN attempts are unlimited. "
                            "Use the evidence to determine the correct code."
                        )

            # =================================================
            # NOT INVESTIGATED
            # =================================================

            else:

                if st.button(
                    f"🔎 Investigate {room}",
                    key=f"visit_{room}",
                    disabled=not game.can_act(),
                    use_container_width=True,
                ):

                    success, payload = (
                        game.visit_room(room)
                    )

                    if success:

                        clean_internal_log()

                        st.rerun()

                    else:

                        st.warning(
                            str(payload)
                        )


# ============================================================
# INTERROGATIONS
# ============================================================

with tab_people:

    st.subheader(
        "🗣️ Interrogation Room"
    )

    # ========================================================
    # PIN NOT CRACKED
    # ========================================================

    if not game.pin_cracked:

        st.html(
            """
            <div class="locked-box">

                <div class="locked-title">
                    🔒 INTERROGATION SYSTEM LOCKED
                </div>

                <p>
                    Employee interrogation records are protected
                    behind restricted access.
                </p>

                <p>
                    You must crack the Cafeteria employee PIN
                    before you can question anyone.
                </p>

                <p>
                    <b>
                        Locate the Cafeteria and recover the
                        missing digits.
                    </b>
                </p>

            </div>
            """
        )

    # ========================================================
    # SECURITY CHALLENGE
    # ========================================================

    elif game.security_challenge_active:

        attempts_used = len(
            game.wordle_attempts
        )

        attempts_remaining = (
            game.wordle_max_attempts
            - attempts_used
        )

        st.html(
            f"""
            <div class="security-box">

                <div class="security-title">
                    🔐 SECONDARY SECURITY LOCK
                </div>

                <div class="security-warning">
                    INTERROGATION ACCESS DENIED
                </div>

                <p>
                    The restricted employee system has detected
                    an additional authentication requirement.
                </p>

                <p>
                    Someone has modified the security protocol.
                </p>

                <p>
                    Complete the emergency verification challenge
                    to continue.
                </p>

                <div class="security-word">
                    _ _ _ _ _
                </div>

                <p>
                    <b>
                        FIVE-LETTER SECURITY WORD
                    </b>
                </p>

            </div>
            """
        )

        st.metric(
            "ATTEMPTS REMAINING",
            attempts_remaining
        )

        # ====================================================
        # PREVIOUS ATTEMPTS
        # ====================================================

        if game.wordle_attempts:

            st.markdown(
                "### Previous Attempts"
            )

            for attempt in game.wordle_attempts:

                result = ["⬛"] * 5
                remaining = list(game.wordle_answer)

                # Green first
                for index, letter in enumerate(attempt):

                    if (
                        index < len(game.wordle_answer)
                        and letter == game.wordle_answer[index]
                    ):

                        result[index] = "🟩"
                        remaining[index] = None

                # Yellow second
                for index, letter in enumerate(attempt):

                    if result[index] == "🟩":
                        continue

                    if letter in remaining:

                        result[index] = "🟨"

                        remaining[
                            remaining.index(letter)
                        ] = None

                display = "".join(result)

                st.write(
                    f"`{attempt}`  {display}"
                )

        # ====================================================
        # WORDLE INPUT
        # ====================================================

        guess = st.text_input(
            "Enter a 5-letter word",
            max_chars=5,
            key="wordle_guess",
            placeholder="_____",
        )

        if st.button(
            "🔓 SUBMIT SECURITY WORD",
            key="submit_wordle",
            use_container_width=True,
        ):

            success, result = (
                game.submit_wordle(
                    guess
                )
            )

            # -----------------------------------------------
            # CORRECT
            # -----------------------------------------------

            if (
                isinstance(result, dict)
                and result.get("status")
                == "CORRECT"
            ):

                clean_internal_log()

                st.success(
                    "🔓 SECURITY LOCK DEFEATED."
                )

                st.balloons()

                st.rerun()

            # -----------------------------------------------
            # CONTINUE
            # -----------------------------------------------

            elif (
                isinstance(result, dict)
                and result.get("status")
                == "CONTINUE"
            ):

                clean_internal_log()

                st.rerun()

            # -----------------------------------------------
            # FAILED
            # -----------------------------------------------

            elif (
                isinstance(result, dict)
                and result.get("status")
                == "FAILED"
            ):

                clean_internal_log()

                st.error(
                    "🔐 SECURITY LOCK FAILED. "
                    "Interrogation access has been blocked."
                )

                st.rerun()

            else:

                st.warning(
                    str(result)
                )

        st.caption(
            "A successful solution is required to unlock interrogation."
        )

    # ========================================================
    # FAILED SECURITY CHALLENGE
    # ========================================================

    elif game.wordle_failed:

        st.html(
            """
            <div class="locked-box">

                <div class="locked-title">
                    🔐 INTERROGATION ACCESS BLOCKED
                </div>

                <p>
                    The secondary security protocol could not
                    be defeated.
                </p>

                <p>
                    The employee interrogation system remains
                    inaccessible.
                </p>

                <p>
                    <b>
                        You must rely on the physical evidence,
                        timeline and case records.
                    </b>
                </p>

            </div>
            """
        )

        st.divider()

        st.info(
            "The case is still solvable. "
            "The security sabotage does not remove "
            "any physical evidence."
        )

    # ========================================================
    # FULLY UNLOCKED
    # ========================================================

    else:

        st.write(
            "The interrogation system is online. "
            "Everyone has something to say. "
            "The trick is figuring out whether it matters."
        )

        question_bank = getattr(
            case,
            "QUESTION_BANK",
            {}
        )

        for character in case.CHARACTERS:

            profile = get_profile(
                character
            )

            with st.expander(
                f"🧑 {character} — "
                f"{profile.get('role', 'Unknown role')}"
            ):

                st.html(
                    '<div class="suspect-card">'
                    f'<strong>{safe_html(character)}</strong>'
                    '<br>'
                    '<span style="color:#c9a961;font-size:.8rem;">'
                    f'{safe_html(profile.get("role", "Unknown role"))}'
                    ' • '
                    f'{safe_html(profile.get("location", "Unknown"))}'
                    '</span>'
                    '<br><br>'
                    f'{safe_html(profile.get("description", ""))}'
                    '<br><br>'
                    f'<i>{safe_html(profile.get("personality", ""))}</i>'
                    '</div>'
                )

                asked_data = game.asked.get(
                    character
                )

                # =================================================
                # ALREADY QUESTIONED
                # =================================================

                if asked_data:

                    question_key = asked_data.get(
                        "question"
                    )

                    answer = asked_data.get(
                        "answer",
                        ""
                    )

                    st.markdown(
                        "**Statement collected:**"
                    )

                    st.html(
                        '<div class="statement-card">'
                        '<div class="statement-question">'
                        f'Q: {safe_html(get_question_text(question_key))}'
                        '</div>'
                        '<div class="statement-answer">'
                        f'“{safe_html(answer)}”'
                        '</div>'
                        '</div>'
                    )

                    st.info(
                        "You have already questioned this person. "
                        "Study their statement against the evidence."
                    )

                # =================================================
                # NOT QUESTIONED
                # =================================================

                else:

                    if (
                        isinstance(
                            question_bank,
                            dict
                        )
                        and question_bank
                    ):

                        q_key = "alibi"

                        st.info(
                            "Where were you at 11:50 PM?"
                        )

                        if st.button(
                            f"💬 Ask {character}",
                            key=f"ask_{character}",
                            disabled=not game.can_act(),
                            use_container_width=True,
                        ):

                            success, answer = (
                                game.ask_question(
                                    character,
                                    q_key
                                )
                            )

                            if success:

                                clean_internal_log()

                                st.rerun()

                            else:

                                st.warning(
                                    str(answer)
                                )

                    else:

                        st.warning(
                            "No questions are configured."
                        )


# ============================================================
# ACCUSATION
# ============================================================

with tab_accuse:

    st.subheader(
        "⚖️ Final Accusation"
    )

    # ========================================================
    # CASE ALREADY ENDED
    # ========================================================

    if game.game_over:

        st.html(
            """
            <div class="result-open">

                <h2>
                    CASE CLOSED
                </h2>

                <p>
                    You have already submitted your final accusation.
                </p>

                <p>
                    Open the
                    <b>📁 RESULT</b>
                    tab to view the final outcome.
                </p>

            </div>
            """
        )

    # ========================================================
    # ACCUSATION FORM
    # ========================================================

    else:

        st.warning(
            "Once you submit an accusation, "
            "the investigation ends."
        )

        st.write(
            "Don't accuse someone simply because they lied. "
            "Accuse the person whose statements and actions "
            "connect to the actual incident."
        )

        suspect = st.selectbox(
            "Who is the Mole?",
            case.CHARACTERS,
            key="final_suspect",
        )

        st.divider()

        st.subheader(
            "What convinced you?"
        )

        evidence_options = []

        clue_labels = {

            "lab_acrostic":
                "🧪 Laboratory note",

            "storage_riddle":
                "📦 Storage riddle",

            "cafeteria_pin":
                "🥤 Cafeteria restocking receipt",
        }

        # ========================================================
        # PHYSICAL CLUES
        # ========================================================

        for clue in getattr(
            game.evidence,
            "clues_found",
            []
        ):

            label = clue_labels.get(
                clue,
                str(clue)
            )

            if label not in evidence_options:

                evidence_options.append(
                    label
                )

        # ========================================================
        # STATEMENTS
        # ========================================================

        for character in case.CHARACTERS:

            statements = get_statement_data(
                character
            )

            for question_key in statements:

                label = (
                    f"🗣️ {character}: "
                    f"{get_question_text(question_key)}"
                )

                if label not in evidence_options:

                    evidence_options.append(
                        label
                    )

        if evidence_options:

            selected_evidence = st.multiselect(
                "Select the clues/statements "
                "that support your accusation",
                evidence_options,
                key="final_evidence",
            )

        else:

            selected_evidence = []

            st.info(
                "You haven't collected any evidence yet."
            )

        st.divider()

        st.subheader(
            "Your Reasoning"
        )

        reasoning = st.text_area(
            "Build your case",
            placeholder=(
                "Explain why the evidence points to this person..."
            ),
            height=180,
            key="final_reasoning",
        )

        st.divider()

        if st.button(
            "🔨 SUBMIT FINAL ACCUSATION",
            type="primary",
            use_container_width=True,
            disabled=not game.can_act(),
        ):

            if not selected_evidence:

                st.error(
                    "A detective needs evidence. "
                    "Select at least one piece of evidence."
                )

            elif not reasoning.strip():

                st.error(
                    "Explain your reasoning before "
                    "closing the case."
                )

            else:

                st.session_state.final_evidence_saved = (
                    selected_evidence.copy()
                )

                st.session_state.final_reasoning_saved = (
                    reasoning.strip()
                )

                success, result = (
                    game.make_accusation(
                        suspect
                    )
                )

                if success:

                    clean_internal_log()

                    st.rerun()

                else:

                    st.error(
                        str(result)
                    )


# ============================================================
# FINAL RESULT TAB
# ============================================================

with tab_result:

    # ========================================================
    # CASE STILL OPEN
    # ========================================================

    if not game.game_over:

        st.html(
            """
            <div class="result-open">

                <h1>CASE STILL OPEN</h1>

                <h2>
                    THE MOLE HAS NOT BEEN IDENTIFIED
                </h2>

                <p>
                    Complete your investigation and submit
                    your final accusation.
                </p>

            </div>
            """
        )

        st.info(
            "Return to the ⚖️ ACCUSATION tab when you are ready."
        )

    # ========================================================
    # CASE FINISHED
    # ========================================================

    else:

        # ====================================================
        # CASE SOLVED
        # ====================================================

        if game.result == "win":

            st.html(
                """
                <div class="verdict-box">

                    <h1>CASE SOLVED</h1>

                    <h2>
                        THE MOLE HAS BEEN IDENTIFIED
                    </h2>

                    <p>
                        Your accusation was correct.
                        The evidence led you to the right suspect.
                    </p>

                </div>
                """
            )

            st.success(
                "✓ Your accusation was correct."
            )

        # ====================================================
        # CASE NOT SOLVED
        # ====================================================

        else:

            st.html(
                """
                <div class="verdict-box">

                    <h1>CASE NOT SOLVED</h1>

                    <h2>
                        THE MOLE GOT AWAY
                    </h2>

                    <p>
                        Your accusation did not identify the Mole.
                    </p>

                </div>
                """
            )

            st.error(
                "✗ Your accusation was incorrect."
            )

            st.warning(
                f"The real Mole was **{case.MOLE}**."
            )

        # ====================================================
        # INVESTIGATION REPORT
        # ====================================================

        st.divider()

        st.subheader(
            "📋 INVESTIGATION REPORT"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Actions Used",
                game.actions_used
            )

        with col2:

            st.metric(
                "Scenes Searched",
                len(game.visited_rooms)
            )

        with col3:

            st.metric(
                "Statements",
                statement_count()
            )

        # ====================================================
        # ACCUSATION
        # ====================================================

        st.divider()

        st.subheader(
            "⚖️ YOUR ACCUSATION"
        )

        st.write(
            f"**Suspect:** {game.accused}"
        )

        if game.result == "win":

            st.success(
                "✓ Correct accusation."
            )

        else:

            st.error(
                "✗ Incorrect accusation."
            )

        # ====================================================
        # SELECTED EVIDENCE
        # ====================================================

        if st.session_state.final_evidence_saved:

            st.divider()

            st.subheader(
                "🔎 EVIDENCE YOU SELECTED"
            )

            for evidence in (
                st.session_state.final_evidence_saved
            ):

                st.html(
                    '<span class="clue-chip">'
                    f'✓ {safe_html(evidence)}'
                    '</span>'
                )

        # ====================================================
        # REASONING
        # ====================================================

        if st.session_state.final_reasoning_saved:

            st.divider()

            st.subheader(
                "🧠 YOUR REASONING"
            )

            st.html(
                '<div class="quote-box">'
                f'{safe_html(st.session_state.final_reasoning_saved)}'
                '</div>'
            )

        # ====================================================
        # NEW CASE
        # ====================================================

        st.divider()

        if st.button(
            "🔄 START A NEW CASE",
            use_container_width=True
        ):

            reset_case()

            st.rerun()
