# Task 2931: Failure analysis and one honest data improvement

## Scope and versioned evidence

PR #47 adds six synthetic technical training examples to a 36-row baseline. The updated dataset has 42 rows: 12 access, 12 billing, and 18 technical. All original training rows and the six added rows were preserved. Fresh baseline and updated models were trained/evaluated on 2026-10-12; [the evaluation report](model_evaluation.md) and [manifest](evidence/pr47/manifest.json) identify the exact sources, environment and captured outputs.

The local six-case evaluation file is unchanged, identified by SHA-256 `043a43417794e25e405d418248110d5cf7b1b2957706da782887927bfdc571c1`. It was previously exposed in Git history and must be described as a separate evaluation set, not a blind benchmark. Shared documentation uses case IDs and metrics; detailed ticket text stays local.

## Failure 1: CASE-001

- Expected label: `access`.
- Baseline prediction: `billing`, confidence `0.413`.
- Updated prediction: `billing`, confidence `0.396`.
- Outcome: still incorrect after retraining.
- Hypothesis: account/profile-change language can overlap category boundaries when a request does not make an authentication or permission problem explicit. This is an explanation to discuss, not a confirmed account of the model's internal decision.
- Potential support impact: routing to billing could delay handling by the team responsible for the account request. Group B has not yet confirmed that impact.

## Failure 2: CASE-005

- Expected label: `technical`.
- Baseline prediction: `access`, confidence `0.465`.
- Updated prediction: `access`, confidence `0.439`.
- Outcome: still incorrect after retraining.
- Hypothesis: a short profile-update request may lack enough failure context for a bag-of-words classifier to distinguish an application malfunction from an access request. This remains a hypothesis.
- Potential support impact: routing to access support may postpone investigation of a malfunction. Group B has not yet confirmed that impact.

## The six new synthetic examples

The weakest baseline split category was technical (recall 0.33 in the historical/fresh baseline report). Six technical examples were added covering an internal server error on a report page, document-upload crash, filtered-search failure, record-fetch timeout, failed export, and unsaved notification preferences.

The additions are synthetic examples, not copies of evaluation rows. Both training versions have zero whitespace-normalized exact overlap with the evaluation set. The expected evaluation labels and CSV hash were preserved. Exact non-overlap is narrower than semantic independence; prior benchmark exposure remains a limitation.

## Honest before-and-after scores

| Metric | Fresh 36-row baseline replay | Fresh 42-row updated replay |
| --- | ---: | ---: |
| Training rows | 36 | 42 |
| access / billing / technical | 12 / 12 / 12 | 12 / 12 / 18 |
| Stratified 20% split accuracy | 62.5% (5/8) | 55.6% (5/9) |
| Five-fold CV mean accuracy | 63.2% | 78.3% |
| CV fold standard deviation | 19.8% | 17.8% |
| Separate-set accuracy | 4/6 (66.7%) | 4/6 (66.7%) |
| Separate-set errors | 2 | 2 |

The six-case accuracy stays at 4/6 (66.7%) and both analysed errors remain. The concrete improvement is additional training coverage for technical issues; this experiment does not show improved accuracy on the separate evaluation set. The higher CV mean uses a different training dataset and different folds and must not be presented as a controlled improvement on identical test cases.

## Team discussion and dependencies

- [ ] Discuss both failure hypotheses together in A2.
- [ ] Ask Group B whether each routing mistake matters to a support agent and record the actual feedback.
- [ ] Agree any label-boundary clarification with the team; do not change expected labels just to raise the score.
- [ ] Agree ownership/dependency handling with Enzu for task 2930 / PR #46 and task 2929 / PR #43.
- [ ] Agree the 42-row README/evaluation/model-card/demo transition with the owners of PR #48, #49 and #50.

The obsolete six-line `docs/integration_check.md` addition was backed up outside the repository and removed while honoring its deletion in main from approved/merged PR #46 (`df294c84fed1108c820447f2591e4d9202b442e4`). This PR does not introduce a competing integration report; the expanded report belongs in PR #43. PR #46's complete historical report is preserved in [a versioned archive](model_evaluation_pr46_baseline.md). Final shared evaluator/report ownership for #47 remains pending.

### Proposed coordination plan — not yet agreed

No completed team discussion or dependency agreement has been reported. The following proposals need confirmation from Enzu and the task owners; they are not completed work or permission to merge.

| PR / task | Owner | Proposed action | Status |
| --- | --- | --- | --- |
| [#43](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/43) / 2929 | AakashAaku | Keep the expanded integration report authoritative. The obsolete addition is removed in line with merged main; agree the remaining integration dependency plan without replacing #43's expanded report. | Pending agreement |
| [#46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46) / 2930 | WhitneyKataka | The approved report is now archived intact after #46 merged. Agree remaining shared evaluator/report ownership for #47. | #46 merged; #47 agreement pending |
| #47 / 2931 | WhitneyKataka and A2 | Keep the source-pinned 42-row failure analysis/results; agree the canonical evaluator including CLI failure handling and tests. | Pending agreement |
| [#48](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/48) / 2938 | WhitneyKataka | Preserve the reproducibility captures for the 36-row baseline. Agree the shared README's current dataset/version wording and separate 42-row evidence links. | Pending agreement |
| [#49](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/49) / 2939 | WhitneyKataka | Keep baseline model-card metrics versioned; agree a separate 42-row dataset/metric/limitation section after transition. | Pending agreement |
| [#50](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/50) / 2940 | WhitneyKataka | Keep existing demo observations attached to their tested baseline. Agree whether the demo stays historical or needs focused verification with the 42-row model. | Pending agreement |

After the discussions actually happen, record the date, participants, A2 feedback for CASE-001/CASE-005, Group B's routing-impact feedback, agreed label boundaries, and the owner/merge order of each shared update. Expected evaluation labels must remain unchanged merely to raise the score.

## Evidence

- [Baseline training output](evidence/pr47/baseline-train.txt).
- [Baseline count-only separate-set evaluation](evidence/pr47/baseline-evaluation.txt).
- [Updated training output](evidence/pr47/updated-train.txt).
- [Updated count-only separate-set evaluation](evidence/pr47/updated-evaluation.txt).
- [Actual run dates, tested commits, dataset/model hashes and exact commands](evidence/pr47/manifest.json).
- [Original executed-source hashes and LF/CRLF content comparison](evidence/pr47/source-comparison.json).
- [CLI follow-up source version, eight passing tests and unchanged evaluation](evidence/pr47/cli-followup.json).

The technical fixes and captured evidence are prepared for PR #47. Team discussion, dependency agreement, Enzu recheck/approval, and merge remain pending. Add the merged PR link to the task only after the actual merge.
