# Data Quality Report

## Overlap check: training data vs held-out set

- Date run: 2026-10-08
- Script: tests/leakage_test.py
- Training file: ai/data/tickets.csv (36 unique rows, 12 per category: access, billing, technical)
- Held-out file: tests/held_out_tickets.csv (6 unique rows). SHA-256: c4438e85add65bc9d4b051469085f9d681a23ea438c1afa1cce7d113261c5195
- Method: each ticket_text is lower-cased and extra spaces are removed, then the two sets are compared for exact matches.
- Result: Overlap: set(). There are 0 overlapping rows.

## Limits

- Only exact matches are found. A reworded copy of a training ticket would not be detected.
- The real held-out file is not in the repository, so reviewers rely on the hash above. Run the check again if either file changes.
- tests/held_out_tickets.csv is still tracked by git, so adding it to .gitignore does not protect it on its own; it also needs `git rm --cached`. The copy that is committed in the repository is placeholder data, not this held-out set.
