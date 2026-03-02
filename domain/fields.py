"""
Defines the ordered list of fields for a DailyEntry.

Stored separately to avoid circular imports and to centralise field
management, supporting the open/closed principle — adding a field here
propagates automatically.

If a new multiline field is added, it will need to also be added to
the list of multiline fields in screen.py for correct display in the GUI.
"""

FIELDS = [
    "date",
    "work_contribution",
    "learning",
    "win",
    "challenge",
    "next_steps"
]
