# Model evaluation: versioned baseline and updated results

## Fresh verification

Both models were trained and evaluated locally on **2026-10-12 (UTC+03:00, Asia/Damascus)**. Exact start/end timestamps, commands, working directories, package versions, dataset hashes, model hashes, and output hashes are recorded in [the manifest](evidence/pr47/manifest.json).

- Reviewed PR #47 head: `3698de47425d1a0dcd60fec5c3c8f654f7517c82`.
- Historical baseline source for the fresh replay: `4267ae5495b83b28b2f079803726cfa345a29429` (36-row training data, training script, and predictor).
- Tested local code commit: `213281c9cc717f1677451cb31db8c47b50d81173`. It includes main at `0706db3add33fab7f5007049d30be6ef25a81115` and uses the original six additional technical examples.
- Both replays use the evaluator content from the tested local code commit. The executed snapshots have different LF/CRLF line endings; training, predictor and evaluator contents are identical after CRLF-to-LF normalization only. Original byte hashes are preserved rather than relabelled. The training dataset grows from 36 to 42 rows.
- Evaluation-file SHA-256: `043a43417794e25e405d418248110d5cf7b1b2957706da782887927bfdc571c1`. Case IDs identify rows in this unchanged file and are not ticket text.

The six evaluation cases were previously exposed in Git history. These scores are for a **separate evaluation set, not a genuinely blind benchmark**. Removing tracking does not undo that exposure.

## Executed-source comparison

[The source comparison](evidence/pr47/source-comparison.json) records an actual comparison of the executed baseline snapshot and the executed updated files before the CLI follow-up edits. The updated files' original hashes were checked against the manifest; copies of both source snapshots were retained outside the repository. Each normalized source was also checked against its recorded Git source commit.

| Source | Baseline CRLF sequences | Updated CRLF sequences | Equal after CRLF-to-LF only |
| --- | ---: | ---: | --- |
| `ai/train.py` | 0 | 51 | Yes |
| `ai/evaluate_heldout.py` | 0 | 81 | Yes |
| `ai/predictor.py` | 0 | 17 | Yes |

Both original-byte hashes and normalized-content hashes are in that artifact. No trimming, BOM removal or other source rewriting was used in this comparison. The replay sources differ only in line endings; no training, prediction or evaluation logic difference was found between those two executed versions.

The later CLI error-handling change is a follow-up evaluator version. It must not be attributed to the already captured baseline/updated runs. Their original evaluator hashes, model hashes, dates, metrics and output captures remain unchanged; no new training run was needed to explain the verified formatting differences.

## CLI follow-up verification

The CLI follow-up was tested on 2026-10-12 at source commit `57a4de72e286d6bf07b2e6ea221ea83869b7a4e9`, which includes main `02a9d941ffe8691aec4a75473984e638790ef1b5`. Exact timestamps, executed source-byte hashes, committed-source hashes and captured output hashes are in [cli-followup.json](evidence/pr47/cli-followup.json).

```text
python -m unittest discover -s tests -p "test_evaluate_heldout.py" -v
```

The actual result was **8 tests passed**. Coverage includes missing CSV, malformed CSV, invalid labels/encoding, nonzero process exit, and text-safe stderr without private ticket text, raw paths or tracebacks. Internal validation remains independently testable. [The actual test output](evidence/pr47/cli-tests-stderr.txt) is on stderr, as emitted by unittest; stdout was empty.

A focused `python ai/evaluate_heldout.py` execution also succeeded: its [case/count output](evidence/pr47/cli-evaluation-stdout.txt) is identical to the original updated replay capture and still reports 4/6. The saved model SHA-256 was checked before and after and is unchanged. No training run was performed for this CLI/documentation follow-up, and the historical training/evaluator hashes and baseline/updated metrics in this report remain attached to their original executed versions.

## Actual fresh results

| Metric | Fresh 36-row baseline replay | Fresh 42-row updated replay |
| --- | ---: | ---: |
| Training rows | 36 | 42 |
| access / billing / technical | 12 / 12 / 12 | 12 / 12 / 18 |
| Stratified 20% split accuracy | 62.5% (5/8) | 55.6% (5/9) |
| Five-fold CV mean accuracy | 63.2% | 78.3% |
| CV fold standard deviation | 19.8% | 17.8% |
| Separate-set accuracy | 4/6 (66.7%) | 4/6 (66.7%) |
| Separate-set errors | 2 | 2 |

The split scores evaluate models trained on the corresponding training subset. Each cross-validation fold trains its own pipeline on its training fold. The saved baseline/updated models are then fitted on all 36/42 training rows, respectively; their separate-set scores are measured after that final fit.

The two split scores use different validation cases and sample sizes. The CV means also use different datasets and folds, so they are not a controlled comparison on identical evaluation cases. The separate-set comparison uses the same six cases, but prior exposure and its small size limit what it can establish.

## Case-level results without ticket text

| Case ID | Expected | Baseline prediction | Baseline confidence | Updated prediction | Updated confidence |
| --- | --- | --- | ---: | --- | ---: |
| CASE-001 | access | billing | 0.413 | billing | 0.396 |
| CASE-002 | access | access | 0.814 | access | 0.792 |
| CASE-003 | billing | billing | 0.682 | billing | 0.671 |
| CASE-004 | billing | billing | 0.690 | billing | 0.673 |
| CASE-005 | technical | access | 0.465 | access | 0.439 |
| CASE-006 | technical | technical | 0.763 | technical | 0.845 |

CASE-001 and CASE-005 remain incorrect after adding the six technical examples. Expected labels were not changed to improve the score. One error changes the six-case accuracy by approximately 16.7 percentage points.

## Captured evidence and reproduction

- [Baseline training output](evidence/pr47/baseline-train.txt) and [baseline separate-set output](evidence/pr47/baseline-evaluation.txt).
- [Updated training output](evidence/pr47/updated-train.txt) and [updated separate-set output](evidence/pr47/updated-evaluation.txt).
- [Versions, file hashes, timestamps and exact executed commands](evidence/pr47/manifest.json).
- [Replay method and command notes](evidence/pr47/README.md).

The training file hashes are `f3eea6dcfca3bd7786a04874ca00f7041ab169ba752653e9e703e071e29a4b71` (baseline bytes used) and `4490b651424ba6633d534633e1ace4765e527493a6b4c91d52379acecc983209` (updated bytes used). Both have zero whitespace-normalized exact text overlap with the evaluation set. This check does not establish semantic independence or restore blindness.

## Historical baseline evidence

The original PR report described a 36-row model with split accuracy 62.5%, CV mean 63.2%, and separate-set score 4/6. Those values and its baseline confidences are historical author-reported evidence; the original run dates, environment and captured outputs were not supplied. The fresh baseline replay above reproduces those values in the recorded environment. Its captured outputs are new evidence from 2026-10-12, not reconstructed original logs.

The original updated-model report described a 42-row model with split accuracy 55.6%, CV mean 78.3%, and separate-set score 4/6. The fresh updated run also reproduces these values. Refer to its own captured outputs and model hash, rather than attributing historical baseline evidence to the updated saved model.

## Preserved PR #46 report after synchronization

PR #46 was approved and merged into main at `df294c84fed1108c820447f2591e4d9202b442e4` during this follow-up. Its complete report is preserved in [the historical PR #46 archive](model_evaluation_pr46_baseline.md), including its recorded artifact-provenance limitations and original case/count output. Its distinct CSV/model hashes remain separate from this PR's replay metadata.

The merged PR #46 evaluator's clear missing-file failure, label normalization, case/count output and prediction call are retained by this PR's tested implementation. The latter additionally validates malformed/invalidly encoded CSV and emits path-safe errors with exit status 1. The evaluator source remains byte-identical to the CLI source tested at `57a4de72e286d6bf07b2e6ea221ea83869b7a4e9`; source hashes and eight-test outputs are retained in the follow-up evidence. Final shared evaluator/report ownership for #47 still needs agreement.

## Task ownership and next steps

Task 2930, [PR #46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46), owned by WhitneyKataka, is approved and merged into `main` (`df294c8`); its report is preserved in the historical archive (`model_evaluation_pr46_baseline.md`). Task 2929, [PR #43](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/43), owned by AakashAaku, is approved and merged into `main` (`c8e7e34`), providing the authoritative expanded integration report (`docs/integration_check.md`). Task 2939, [PR #49](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/49), is merged into `main` (`73853f2`), providing the baseline model card (`docs/model_card.md`). PR #47 owns the canonical evaluator implementation (`ai/evaluate_heldout.py`, `tests/test_evaluate_heldout.py`) and the versioned 42-row failure analysis and evaluation report.

Discuss the ambiguous failure categories with A2 and ask Group B about support-routing impact. Record the discussion after it happens. Generate `ai/model.joblib` locally; keep it and the local evaluation CSV out of Git. Enzu approval and merge remain pending.

The current contributor is not a member of Group A2 or Group B. A designated member from A2 must conduct or confirm the failure discussion, and designated Group B members must provide or confirm the routing-impact feedback and label-boundary decisions. No discussion outcome is claimed here until those participants and the actual date are recorded.

## Versioned handoff for related PRs

This report is the versioned #47 evaluation record. Its updated evaluator, 42-row results, CLI follow-up, and associated source/file/model hashes belong to #47. The following related evidence remains separate:

- [PR #46's historical report](model_evaluation_pr46_baseline.md) remains an unchanged archive of the historical 36-row evidence and its artifact-provenance limitations (merged into `main`).
- [PR #43](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/43) is merged and authoritative for the expanded integration report; this report does not replace it.
- [PR #48](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/48) (WhitneyKataka / Blaqcodex) owns the `ai/README.md` reproduction section for the historical 36-row baseline. Merge-order handling is agreed: historical reproduction must use the recorded baseline source/data (`525ac01b...`), not assume the current CSV still contains 36 rows; instructions reconcile against whichever PR lands first; and 42-row results are identified separately.
- [PR #49](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/49) is merged; its baseline model card in `docs/model_card.md` is preserved, and any 42-row additions will be versioned separately upon transition.
- [PR #50](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/50) preserves historical 36-row demo observations. If a live demo of the current 42-row model is required, focused verification of that model must be recorded separately rather than overwriting historical captures.

The ownership and transition agreements above reflect coordination with task owners. They do not mark pending A2/Group B discussions complete, change expected labels, or authorize merge. The explicit **Do not merge yet** hold remains in place.
