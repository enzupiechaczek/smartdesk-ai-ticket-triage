import re

URGENT_PHRASES = ["cannot access", "locked out", "outage", "down",
                  "all users", "everyone", "production", "data loss"]

def compute_priority(subject, description):
    text = (subject + " " + description).lower()
    for phrase in URGENT_PHRASES:
        if re.search(r"\b" + re.escape(phrase) + r"\b", text):
            return "urgent"
    return "normal"