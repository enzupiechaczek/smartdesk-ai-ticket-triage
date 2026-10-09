# Data Quality Report

## Overlap check: training data vs held-out set

- Date run: 2026-10-08
- Script: tests/leakage_test.py
- Training file: ai/data/tickets.csv (36 unique rows, 12 per category: access, billing, technical)
- Held-out file: tests/held_out_tickets.csv (6 unique rows). SHA-256: e78d1de5547acf325ee6793deff99ca074dea8bf1b0fed22ebe40453bc6a1000
- Method: each ticket_text is lower-cased and extra spaces are removed, then the two sets are compared for exact matches.
- Result: Overlap: set(). There are 0 overlapping rows.

## Limits

- Only exact matches are found. A reworded copy of a training ticket would not be detected.
- The six held-out tickets are recoverable from git history on the published branches, so they cannot be treated as a secret or blind test set. They are still valid for checking overlap with the training data, which is what this check does.
- The hash above is the version with clean labels (access, billing, technical, no stray spaces). An earlier version with the label problems still exists in history under hash c4438e85add65bc9d4b051469085f9d681a23ea438c1afa1cce7d113261c5195.
- Run the check again if either file changes.

## Exposure to fix

The held-out tickets were committed on 2026-10-07 in 953d5e8 and are still reachable from origin/b-username123212312-day1-testplan, origin/b-username123212312-day2-api-tests, origin/b-username123212312-day2-leakage and origin/b-username123212312-day3-priority. origin/main is clean. The tickets are synthetic, so no customer data is affected, but the branches need a history rewrite before this set can be called held-out again.