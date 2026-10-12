# Model evaluation: versioned baseline and updated results

## Fresh verification

Both models were trained and evaluated locally on **2026-10-12 (UTC+03:00, Asia/Damascus)**. Exact start/end timestamps, commands, working directories, package versions, dataset hashes, model hashes, and output hashes are recorded in [the manifest](evidence/pr47/manifest.json).

- Reviewed PR #47 head: `3698de47425d1a0dcd60fec5c3c8f654f7517c82`.
- Historical baseline source for the fresh replay: `4267ae5495b83b28b2f079803726cfa345a29429` (36-row training data, training script, and predictor).
- Tested local code commit: `213281c9cc717f1677451cb31db8c47b50d81173`. It merges current main `0706db3add33fab7f5007049d30be6ef25a81115` and uses the original six additional technical examples.
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

## Task ownership and next steps

The evaluator/report were inherited from task 2930, [PR #46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46). The historical integration report belongs to task 2929, [PR #43](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/43); its expanded integration changes are not supplied by this PR. Enzu and the task owners still need to agree how these dependencies will be reviewed/merged. Neither dependency is treated as approved by this report.

Discuss the ambiguous failure categories with A2 and ask Group B about support-routing impact. Record the discussion after it happens. Generate `ai/model.joblib` locally; keep it and the local evaluation CSV out of Git. Enzu approval and merge remain pending.
