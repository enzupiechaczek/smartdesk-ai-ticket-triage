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

| Metric                        | Fresh 36-row baseline replay | Fresh 42-row updated replay |
| ----------------------------- | ---------------------------: | --------------------------: |
| Training rows                 |                           36 |                          42 |
| access / billing / technical  |                 12 / 12 / 12 |                12 / 12 / 18 |
| Stratified 20% split accuracy |                  62.5% (5/8) |                 55.6% (5/9) |
| Five-fold CV mean accuracy    |                        63.2% |                       78.3% |
| CV fold standard deviation    |                        19.8% |                       17.8% |
| Separate-set accuracy         |                  4/6 (66.7%) |                 4/6 (66.7%) |
| Separate-set errors           |                            2 |                           2 |

The six-case accuracy stays at 4/6 (66.7%) and both analysed errors remain. The concrete improvement is additional training coverage for technical issues; this experiment does not show improved accuracy on the separate evaluation set. The higher CV mean uses a different training dataset and different folds and must not be presented as a controlled improvement on identical test cases.

## Contributor review of CASE-001 and CASE-005

**Review date:** 2026-10-13 (local date, UTC+07:00)  
**Reviewer:** waitwhat2231; not a member of Group A2 or Group B  
**Evidence reviewed:** the source-pinned case/count captures, the versioned evaluator report, and the proposed category rules. The evaluation CSV is intentionally not included in shared artifacts, so this review does not reproduce or disclose the ticket text.

- **CASE-001:** expected `access`; predicted `billing` at `0.413` in the 36-row replay and `0.396` in the 42-row replay. Recorded label and confidence metadata alone cannot establish or substantiate semantic ambiguity or ticket meaning. The explanation that account/profile-change wording may overlap billing terms remains strictly a hypothesis to be evaluated. Without human routing review of the underlying local ticket text by designated reviewers, operational team ownership cannot be determined. The expected `access` label is retained.
- **CASE-005:** expected `technical`; predicted `access` at `0.465` in the 36-row replay and `0.439` in the 42-row replay. Recorded label and confidence metadata alone cannot establish or substantiate semantic ambiguity or ticket meaning. The explanation that short profile-update wording lacks sufficient context to distinguish an application malfunction from an access request remains strictly a hypothesis to be evaluated. Without human routing review of the underlying local ticket text by designated reviewers, the proper support route cannot be determined. The expected `technical` label is retained.

**Unresolved after this review:** A2 has not confirmed the failure hypotheses; Group B has not confirmed the support-routing impact; no A2/Group B label-boundary agreement has been recorded; and no decision has been made to change either expected label. Recorded metadata alone does not establish semantic ambiguity. A designated A2 member and designated Group B members must review the original local cases and record their actual feedback, date, participants, and any follow-ups. This contributor review does not satisfy those team decisions.

## Team discussion and dependencies

- [ ] Discuss both failure hypotheses together in A2.
- [ ] Ask Group B whether each routing mistake matters to a support agent and record the actual feedback.
- [ ] Agree any label-boundary clarification with the team; do not change expected labels just to raise the score.
- [ ] Record completed A2/Group B discussion outcomes (pending team review).

The obsolete six-line `docs/integration_check.md` addition was backed up outside the repository and removed while honoring its deletion in main from approved/merged PR #46 (`df294c84fed1108c820447f2591e4d9202b442e4`). This PR does not introduce a competing integration report; the expanded report belongs in PR #43 (which is now merged). PR #46's complete historical report is preserved in [a versioned archive](model_evaluation_pr46_baseline.md). Canonical evaluator and 42-row evaluation/failure analysis report ownership belongs to PR #47.

### Cross-PR coordination and ownership agreements

The status and ownership boundaries across related pull requests are recorded below:

| PR / task | Owner | Action & Agreed Handling | Status |
| --- | --- | --- | --- |
| [#43](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/43) / 2929 | AakashAaku | Authoritative for the expanded integration report (`docs/integration_check.md`). | Merged into `main` (`c8e7e34`) |
| [#44](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/44) | A1 team | Backend startup, API endpoints, and test infrastructure. | Merged into `main` (`0d877ba`) |
| [#46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46) / 2930 | WhitneyKataka | Historical baseline 36-row report and artifact-provenance limitations preserved intact in `docs/model_evaluation_pr46_baseline.md`. | Merged into `main` (`df294c8`) |
| [#49](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/49) / 2939 | WhitneyKataka | Baseline model card for the 36-row baseline preserved in `docs/model_card.md`. Any 42-row model card material will be added as a separately identified version upon transition. | Merged into `main` (`73853f2`) |
| #47 / 2931 | WhitneyKataka and A2 | Owns the canonical evaluator implementation (`ai/evaluate_heldout.py`, `tests/test_evaluate_heldout.py`) including text-safe CLI failure handling, and the versioned 42-row evaluation report and failure analysis (`docs/model_evaluation.md`, `docs/failure_analysis.md`). | Open (pending recheck & discussion) |
| [#48](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/48) / 2938 | WhitneyKataka / Blaqcodex | Responsible owner of `ai/README.md` reproduction section (`## Reproduce the Model`). Agreement confirmed on 2026-10-13 between Blaqcodex and PR #47: historical reproduction uses the recorded baseline source commits (`6be765d` / `0c65c2f`) and checkout bytes (`525ac01b...`), not assuming current CSV is 36 rows; reconciles current dataset counts and instructions against whichever PR lands first; 42-row results identified separately. Distinct from pending A2/Group B discussions and pending PR #50 presentation handoff. | Agreement recorded (2026-10-13); open |
| [#50](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/50) / 2940 | WhitneyKataka / justacoder120 | Preserves historical 36-row demo observations tied to the baseline model. Agrees explicit model-version boundary: historical demo captures (IDs 11/12 and 13/14) remain tied to the 36-row baseline; any live demo of the current 42-row model requires separate focused verification without overwriting historical captures. Presentation handoff remains pending. | Open (handoff pending) |

### Participant boundary

The current contributor is not a member of Group A2 or Group B and cannot claim or complete those teams' discussion decisions. A designated A2 member must review the two failure hypotheses, and designated Group B members must provide the routing-impact feedback and agree any label boundaries. The actual date, participants, feedback, and unresolved follow-ups must be recorded after those discussions occur.

### Ownership boundaries and merge-order agreement

- **`ai/README.md` Owner and Merge-Order Handling:** Confirmed on **2026-10-13** between contributor Blaqcodex (PR #48) and PR #47 contributors. PR #48 owns the reproduction section. Historical reproduction must be executed at the recorded baseline source commits (`6be765d` / `0c65c2f`) with the baseline 36-row dataset checkout bytes (`525ac01b...`), not assuming the current CSV still contains 36 rows once PR #47 merges. Whichever PR lands first:
  - If PR #48 merges first: PR #47 will preserve PR #48's 36-row reproduction section intact, update current dataset counts to 42 rows, and link to the 42-row evaluation.
  - If PR #47 merges first: PR #48 will reconcile its reproduction instructions by targeting the historical 36-row baseline source commits and checkout bytes rather than assuming current `main` contains 36 rows.
  In both merge orders, original 36-row captures, hashes, metrics, and tested source commits remain preserved, and 42-row results are identified separately. This agreement is distinct from the still-pending A2/Group B discussions and the pending PR #50 presentation handoff.
- **Evaluator & Report Ownership:** PR #47 owns the updated text-safe evaluator (`ai/evaluate_heldout.py`, `tests/test_evaluate_heldout.py`) and the 42-row evaluation/failure reports (`docs/model_evaluation.md`, `docs/failure_analysis.md`).
- **PR #46** remains the preserved historical 36-row report archive (`docs/model_evaluation_pr46_baseline.md`).
- **PR #43** remains authoritative for the expanded integration report (`docs/integration_check.md`).
- **PR #49** remains authoritative for the baseline model card (`docs/model_card.md`).
- **PR #50** preserves historical 36-row demo observations; any 42-row demo verification must be recorded separately.

The 36-row metrics, demo captures, session/file/model hashes, and archived provenance limits remain historical evidence. The 42-row metrics and any current-model demo evidence retain their own dataset, source, session, file, and model identifiers. No old result may be relabelled as a 42-row or current-model result.

Until actual A2/Group B discussions are conducted and recorded, these items remain pending follow-ups and the explicit **Do not merge yet** hold remains in force. Expected evaluation labels must remain unchanged merely to raise the score.

## Evidence

- [Baseline training output](evidence/pr47/baseline-train.txt).
- [Baseline count-only separate-set evaluation](evidence/pr47/baseline-evaluation.txt).
- [Updated training output](evidence/pr47/updated-train.txt).
- [Updated count-only separate-set evaluation](evidence/pr47/updated-evaluation.txt).
- [Actual run dates, tested commits, dataset/model hashes and exact commands](evidence/pr47/manifest.json).
- [Original executed-source hashes and LF/CRLF content comparison](evidence/pr47/source-comparison.json).
- [CLI follow-up source version, eight passing tests and unchanged evaluation](evidence/pr47/cli-followup.json).

The technical fixes and captured evidence are prepared for PR #47. Team discussion, dependency agreement, Enzu recheck/approval, and merge remain pending. Add the merged PR link to the task only after the actual merge.
