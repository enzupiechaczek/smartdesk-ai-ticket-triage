# Model Card: SmartDesk AI Ticket Classifier

## 1. Purpose

The SmartDesk AI ticket classifier predicts a support ticket category from its text. It classifies tickets into `access`, `billing`, and `technical`.

The model is intended to assist support staff with initial ticket triage. Its predictions are recommendations, not final decisions.

## 2. Intended Use

The classifier may be used as a starting point for routing support tickets, provided a human reviews the prediction and corrects it when necessary.

It should not be used as the sole basis for decisions affecting account access, payments, refunds, or other consequential support outcomes. Uncertain, ambiguous, or incorrectly classified tickets must be reviewed by a person.

## 3. Data

The documented baseline uses 36 synthetic support-ticket examples from [`ai/data/tickets.csv`](../ai/data/tickets.csv), with 12 examples per category:

- `access`: authentication, passwords, account recovery, and permissions.
- `billing`: payments, invoices, subscriptions, charges, receipts, and refunds.
- `technical`: application errors, performance problems, uploads, exports, and saving issues.

The dataset is small and synthetic. It does not represent the full variety, wording, or complexity of real support tickets. Its results should not be assumed to represent real-world performance.

This report describes the 36-row baseline. Pull request [#47](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/47) proposes a 42-row dataset. If that proposal merges, the dataset version, evaluation figures, and related documentation must be checked and updated together. The figures below must not be presented as results for a 42-row dataset unless that version has been evaluated.

**Baseline provenance:** These metrics apply to the 36-row dataset with SHA-256 `525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1`. The evaluation procedure and reported results are documented in [the evaluation report](model_evaluation.md) and use the training script at [`ai/train.py`](../ai/train.py). This hash identifies the dataset version; it is not a claim that the documentation commit itself was the tested model version.

Group B's separate six-ticket evaluation is documented in [pull request #46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46). Those tickets and results are separate from the eight-record test split reported here. The Group B evaluation has already been exposed and is not a blind benchmark.

## 4. Method

The classifier is a scikit-learn pipeline containing:

- **TF-IDF vectorization:** Converts ticket text into numerical features using unigrams and bigrams.
- **Logistic Regression:** Predicts one of the three ticket categories from the text features.

The training script uses an 80% training split and a 20% test split, stratified by category, with `random_state=42`. It also performs five-fold stratified cross-validation on all 36 dataset rows.

After these evaluation steps, the script fits the pipeline on all 36 examples and saves it as `ai/model.joblib`.

The split-test metrics describe the model fitted on the 80% training portion. Cross-validation reports performance across five separate folds. Neither set of metrics is an independent evaluation of the final saved model trained on all 36 rows.

## 5. Evaluation

Source: [`model_evaluation.md`](model_evaluation.md), which reports the 36-row baseline using the training and evaluation procedure in [`ai/train.py`](../ai/train.py).

### 20% test split

The eight-record test split produced by `test_size=0.2` achieved an accuracy of 0.625 (62.5%).

| Metric | Result |
|---|---:|
| Test-split accuracy | 0.625 (62.5%) |
| Cross-validation mean accuracy | 0.632 (63.2%) |
| Cross-validation standard deviation | 0.198 |
| Access precision | 0.50 |
| Access recall | 1.00 |
| Billing precision | 0.67 |
| Billing recall | 0.67 |
| Technical precision | 1.00 |
| Technical recall | 0.33 |

The five cross-validation fold accuracies were 0.875, 0.429, 0.429, 0.857, and 0.571. These are a separate estimate from the eight-record test-split results; the two must not be conflated.

### Observed misclassifications

One test-split ticket was:

> We updated our billing card details successfully, but the data export script hangs indefinitely at 99%

Its true category was `technical`, while the model predicted `billing`. The ticket combines billing-related wording with an export failure. Billing terms may have influenced the prediction, but the model's internal reasoning has not been independently verified.

Another misclassified technical ticket was:

> Some settings are not being saved after I update them.

The model predicted `access` instead of `technical`. The short wording may make the underlying application malfunction difficult to distinguish from an account or permissions issue; this is a possible explanation, not a verified account of the model's internal reasoning.

A billing ticket, "Please send me a receipt for my most recent payment.", was predicted as `access`. This is another observed error on the same eight-record test split.

These examples illustrate observed prediction errors. They do not establish how the model will perform on other datasets or real support traffic.

## 6. Limitations

- **Small dataset:** The baseline contains only 36 synthetic examples. A single incorrect prediction changes eight-record test accuracy by 12.5 percentage points.
- **Low technical recall:** Technical recall was 0.33 on the test split. Two of the three technical tickets in that split were misclassified.
- **Limited representativeness:** Synthetic examples may not reflect the vocabulary, ambiguity, spelling, and variety of real support requests.
- **Potential category overlap:** Tickets mentioning multiple issues may contain words associated with a category other than the primary problem.
- **No guarantee of generalization:** Test-split and cross-validation scores do not establish performance on production traffic or independently establish the final model's performance.
- **Independent evaluation limitations:** Group B's six-ticket evaluation in PR #46 is separate and already exposed; it must not be described as a blind benchmark.

## 7. Responsible use

- **Human review required:** A person should check predictions, especially for technical issues, ambiguous tickets, and decisions with meaningful consequences.
- **Decision support only:** Do not use the classifier as the sole basis for decisions affecting account access, payments, refunds, or other consequential support outcomes.
- **Correction and escalation:** Support staff should correct incorrect predictions and review uncertain or misclassified tickets rather than relying on the model without oversight.

### Verification and review checklist

- [ ] Preview the complete Markdown document and confirm that the evaluation table renders correctly.
- [ ] Verify that the evaluation report and related pull-request links work.
- [ ] Verify UTF-8 encoding, absence of a leading BOM, inline code formatting, and the absence of unintended escaped formatting markers.
- [ ] Run the whitespace check and record its actual result.
- [ ] Confirm that all metric descriptions refer to the correct dataset and evaluation procedure.
- [ ] Complete and document Group B review only after actual feedback and its outcome are available.
- [ ] Recheck the documentation if PR #47 merges and the proposed 42-row dataset becomes the applicable baseline.
