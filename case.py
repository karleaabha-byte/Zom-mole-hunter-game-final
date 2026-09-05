

# ============================================================
# CASE BASICS
# ============================================================

CHARACTERS = [
    "Raven",
    "Zephyr",
    "Luca",
    "Marinette",
    "Adrien"
]

MOLE = "Zephyr"

ROOMS = [
    "Laboratory",
    "Storage",
    "Cafeteria"
]

LAB_NUMBER = 4
STORAGE_ANSWER = "BREEZE"
STORAGE_NUMBER = len(STORAGE_ANSWER)

CORRECT_PIN = f"{LAB_NUMBER}{STORAGE_NUMBER}19"


# ============================================================
# CASE INTRO
# ============================================================

CASE_INTRO = """
## THE NIGHT SHIFT INCIDENT

**12:18 AM.**

The research facility should have been asleep.

Instead, the emergency lights are flashing, a laboratory alarm is
screaming through the corridors, and six experimental filter
cartridges have disappeared from Storage.

A centrifuge stopped unexpectedly.

A vial was found broken.

And three minutes of corridor camera footage are missing.

Five employees were still inside the facility.

Someone is lying.

Your job is to find out **whose lie matters.**
"""


# ============================================================
# BACKGROUND
# ============================================================

BACKGROUND = {

    "THE CASE": {
        "entries": [
            (
                "12:10 AM",
                "The emergency alarm sounded after the Laboratory "
                "centrifuge stopped unexpectedly."
            ),
            (
                "12:14 AM",
                "Six filter cartridges were found missing from Storage."
            ),
            (
                "12:18 AM",
                "Three minutes of corridor camera footage were missing."
            )
        ]
    },

    "THE TIMELINE": {
        "entries": [
            (
                "11:49 PM",
                "Corridor cameras went offline."
            ),
            (
                "11:50 PM",
                "The Storage ventilation system was overridden."
            ),
            (
                "11:50 PM",
                "The cafeteria vending machine began an unscheduled restock."
            ),
            (
                "11:52 PM",
                "The Laboratory centrifuge was manually interrupted."
            )
        ]
    },

    "THE PEOPLE": {
        "entries": [
            (
                "RAVEN",
                "Head Chemist — responsible for the Laboratory."
            ),
            (
                "ZEPHYR",
                "Supply Coordinator — responsible for Storage and supplies."
            ),
            (
                "LUCA",
                "Security Officer — responsible for cameras and patrols."
            ),
            (
                "MARINETTE",
                "Medic — responsible for the Medical Bay."
            ),
            (
                "ADRIEN",
                "Engineer — responsible for facility power systems."
            )
        ]
    },

    "ONE IMPORTANT DETAIL": {
        "entries": [
            (
                "VENT",
                "The Storage ventilation override can only be used "
                "by Supply or Maintenance."
            ),
            (
                "MAINTENANCE",
                "The Maintenance Chief was off-site that night."
            )
        ]
    }
}


# ============================================================
# SUSPECT PROFILES
# ============================================================

PROFILES = {

    "Raven": {
        "role": "Head Chemist",
        "location": "Laboratory",
        "description": (
            "Brilliant, impatient and visibly annoyed that anyone "
            "would question her work."
        ),
        "personality": "Defensive but confident."
    },

    "Zephyr": {
        "role": "Supply Coordinator",
        "location": "Storage",
        "description": (
            "Quiet, organized and almost painfully calm. "
            "He knows where everything in the facility is kept."
        ),
        "personality": "Helpful, controlled and evasive."
    },

    "Luca": {
        "role": "Security Officer",
        "location": "Corridor Patrol",
        "description": (
            "Takes security seriously, but is clearly embarrassed "
            "that the camera outage happened on his watch."
        ),
        "personality": "Professional and guarded."
    },

    "Marinette": {
        "role": "Medic",
        "location": "Medical Bay",
        "description": (
            "Friendly and observant. She notices more than "
            "she initially admits."
        ),
        "personality": "Kind but cautious."
    },

    "Adrien": {
        "role": "Engineer",
        "location": "Generator Room",
        "description": (
            "Usually relaxed, but was dealing with a brief "
            "power fluctuation that night."
        ),
        "personality": "Casual and slightly nervous."
    }
}


# ============================================================
# ONE QUESTION
# ============================================================

QUESTION_BANK = {
    "alibi": "Where were you at 11:50 PM?"
}


# ============================================================
# INTERROGATION ANSWERS
# ============================================================

ANSWERS = {

    "Raven": {
        "alibi": {
            "answer": (
                "In the Laboratory. I was working with the "
                "centrifuge. It stopped a couple of minutes later."
            ),
            "truth": True
        }
    },

    "Zephyr": {
        "alibi": {
            "answer": (
                "In Storage. I was checking the filter inventory. "
                "I didn't think anything was wrong."
            ),
            "truth_answer": (
                "In Storage. I was checking the filter inventory. "
                "I didn't think anything was wrong."
            ),
            "lie_answer": (
                "I was in the Cafeteria during the restocking cycle. "
                "I never went near Storage."
            ),
            "truth": True
        }
    },

    "Luca": {
        "alibi": {
            "answer": (
                "Near the west corridor. The cameras had just "
                "gone down, so I was checking the security panel."
            ),
            "truth": True
        }
    },

    "Marinette": {
        "alibi": {
            "answer": (
                "In the Medical Bay, preparing the emergency kit. "
                "I heard the alarm a little later."
            ),
            "truth": True
        }
    },

    "Adrien": {
        "alibi": {
            "answer": (
                "In the Generator Room. There was a brief power "
                "fluctuation, so I stayed there to check the system."
            ),
            "truth": True
        }
    }
}


# ============================================================
# LABORATORY CLUE
# ============================================================

LAB_CLUE = {
    "title": "THE LABORATORY NOTE",

    "lines": [
        "Filter pressure was stable before midnight.",
        "One centrifuge cycle was interrupted manually.",
        "Up and active Raven's workstation.",
        "Recorded interruption at 11:52 PM."
    ]
}


# ============================================================
# STORAGE CLUE
# ============================================================

STORAGE_CLUE = {
    "title": "THE STORAGE RIDDLE",

    "riddle": [
        "I cannot be seen, but I shake every leaf.",
        "I fill the sails of ships, yet I weigh nothing at all.",
        "I can carry a whisper farther than the person who spoke it.",
        "Sailors welcome me when I am gentle, but fear what I become when I grow wild.",
        "What am I?"
    ],

    "note": (
        "A ventilation override was recorded at 11:50 PM."
    )
}


# ============================================================
# SABOTAGED STORAGE CLUE
# ============================================================

STORAGE_SABOTAGED_RIDDLE = {
    "title": "THE STORAGE RIDDLE — CORRUPTED",

    "riddle": [
        "I move without feet and speak without a voice.",
        "I can be felt but never held.",
        "I shake every leaf and can fill a ship's sails.",
        "I may pass through a room without opening its door.",
        "I can be gentle enough to cool you,",
        "or violent enough to tear through a forest.",
        "What am I?"
    ],

    "note": (
        "Some of the original storage terminal data "
        "appears to have been corrupted."
    )
}

# ============================================================
# CAFETERIA CLUE
# ============================================================

CAFETERIA_CLUE = {
    "title": "RESTOCKING LOG — MACHINE #3",

    "job": "SUPPLY COORDINATOR",

    "pin_digits": [
        "?",
        "?",
        "1",
        "9"
    ],

    "redacted": [
        True,
        True,
        False,
        False
    ],

    "note": (
        "Restocking began at 11:50 PM — during the camera blackout."
    )
}


# ============================================================
# SABOTAGED CAFETERIA CLUE
# ============================================================

CAFETERIA_SABOTAGED_CLUE = {
    "title": "RESTOCKING LOG — MACHINE #3 — TAMPERED",

    # Keep the visible ??19 fragment so the case remains solvable.
    "job": "SUPPLY COORDINATOR",

    "pin_digits": [
        "?",
        "?",
        "1",
        "9"
    ],

    "redacted": [
        True,
        True,
        False,
        False
    ],

    "note": (
        "The receipt has been tampered with, but the final two PIN "
        "digits remain visible: 19."
    ),

    "description": (
        "Someone tried to damage the employee record. The useful "
        "PIN fragment survived the sabotage."
    )
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_lab_clue():
    return LAB_CLUE


def get_storage_clue(decision=None):
    if decision == "sabotage":
        return STORAGE_SABOTAGED_RIDDLE

    return STORAGE_CLUE


def get_cafeteria_clue(decision=None):
    if decision == "sabotage":
        return CAFETERIA_SABOTAGED_CLUE

    return CAFETERIA_CLUE


def get_question(character, question_key):
    return ANSWERS[character][question_key]


def get_answer(character, question_key, tell_truth=True):
    data = ANSWERS[character][question_key]

    if tell_truth and "truth_answer" in data:
        return data["truth_answer"]

    if not tell_truth and "lie_answer" in data:
        return data["lie_answer"]

    return data["answer"]


def get_profile(character):
    return PROFILES[character]
