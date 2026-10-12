# Data Quality Report

## Overlap check: training data vs held-out set

- Date run: 2026-10-11
- Tested commit: 82018f1a6c7d870bda4a0b7010ede80ed47ba72d
- Command: `python tests/leakage_test.py`, run from the project root
- Script: tests/leakage_test.py
- Training file: ai/data/tickets.csv, 36 unique rows
- Held-out file: tests/held_out_tickets.csv, 6 unique rows. It is not stored in this repository.

### Result of this run

```
Training rows (unique): 36
Held-out rows (unique): 6
Overlap count: 0
```

Exit status: 0, which is the no-overlap case. The script exits 2 when the local
held-out file is missing and 1 when an overlap is found. The missing-file path was
confirmed separately: it printed the copy-the-file message and exited 2.

The script reports counts only. It no longer prints the matching ticket text, so
no held-out content reaches the console or this report.

### Hash evidence

```
certutil -hashfile tests\held_out_tickets.csv SHA256
SHA256 hash of tests\held_out_tickets.csv:
e78d1de5547acf325ee6793deff99ca074dea8bf1b0fed22ebe40453bc6a1000
CertUtil: -hashfile command completed successfully.
```

That hash is of the local file only. The ticket contents are not reproduced here.

## What this check does and does not cover

It compares normalised exact text. Each ticket_text is lower-cased and runs of
whitespace are collapsed, then the two sets are compared for identical strings.

It does not detect a reworded or paraphrased copy of a training ticket. It does
not compare labels or category fields. It does not verify a per-category count.
Only the exact-match result above is evidenced.

## Limits

- Only exact matches are found. A reworded copy of a training ticket would not be detected.
- The 36 and 6 are counts of unique normalised strings, not row totals of the raw files.
- The hash above is the version with clean labels. An earlier version with label spacing
  problems exists in this branch history under hash c4438e85add65bc9d4b051469085f9d681a23ea438c1afa1cce7d113261c5195.
- Run the check again if either file changes.

## Exposure

These six tickets were committed on 2026-10-07 in 953d5e8 and remain reachable from
origin/b-username123212312-day1-testplan, origin/b-username123212312-day2-api-tests,
origin/b-username123212312-day2-leakage and origin/b-username123212312-day3-priority.
origin/main is clean.

Because they are already published, this set is no longer blind and cannot be made blind
again. Deleting git history does not undo publication, so it should not be treated as a way
to restore it. The tickets are synthetic, so no customer data is involved.

This set stays useful as a separate overlap-check set, which is what the result above uses
it for. A genuinely blind evaluation needs a fresh set that has never been committed.
Deciding what to do about the published branches is Enzu's call; no history rewrite is
required for the check in this report to be valid.
