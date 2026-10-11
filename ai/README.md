# AI Folder

## Dataset Breakdown

The training dataset `ai/data/tickets.csv` contains 36 synthetic support ticket examples, balanced across three categories with 12 examples per category.

- **access:** 12 rows
- **billing:** 12 rows
- **technical:** 12 rows
- **Total:** 36 rows

### Hard Cases Included

- **Multi-topic tickets:** Labeled according to the root or primary issue. For example, tickets mentioning checkout interface bugs and unauthorized card charges are classified according to the main problem requiring resolution.
- **Short queries:** Examples include `"cant log in, fix pls"`, `"Refund pls"`, and `"App crash"`.
- **Typo-heavy text:** Examples include `"accout is loocked"`, `"invoyce"`, and `"downlaod botton throwss"`.

## Ticket Categories

- **access:** Sign-in problems, passwords, verification codes, account recovery, and permissions.
- **billing:** Charges, invoices, payments, subscriptions, receipts, and refunds.
- **technical:** Software errors, freezes, slow pages, uploads, exports, and saving problems.

## Training Dataset

`ai/data/tickets.csv` contains 36 synthetic support tickets, with twelve examples for each category.

The CSV has two columns: `ticket_text` and `category`. Category labels are lowercase. Text containing commas is enclosed in double quotes, and embedded double quotes are escaped by doubling them.

All examples are fictional and contain no real names, email addresses, IDs, or incidents. Group B's held-out examples must remain separate from the training dataset and must not be added to it.

## Category Definitions

- **access:** Problems or requests involving authentication, account recovery, workspace invitations, or permissions. This includes locked accounts, multi-factor authentication recovery, and changes to who may view or edit resources.
- **billing:** Questions or problems involving subscription charges, invoices, receipts, taxes, refunds, or payment methods. This includes incorrect seat charges, duplicate payments, and charges after cancellation.
- **technical:** Failures in application behavior or output, including errors, freezes, broken layouts, exports, search, or saved changes. These tickets concern a malfunction rather than an authentication, authorization, or payment request.

## Proposed Edge-Case Rules for A2 Review

These rules guide the current draft and still require agreement during teammate peer review.

- Classify by the main problem or requested resolution, not by tone or words such as `"urgent"`.
- Failed authentication, expired recovery links, missing permissions, and workspace membership changes are `access`. A general page crash or broken interface after successful sign-in is `technical`.
- A declined subscription payment or access blocked specifically by an unpaid subscription is `billing`. Access denied because of a role or workspace permission is `access`.
- Missing password recovery or invitation messages are `access`. Duplicate routine ticket notifications are `technical`.
- A request to correct an invoice amount is `billing`. A malfunction when downloading an otherwise correct invoice is `technical`.
- If a ticket contains unrelated problems with no clear primary request, split it into separate examples or hold it for team review instead of guessing a label.
- If a ticket mixes two problems, label the main problem the user wants solved. For example, a ticket involving a payment issue and an unauthorized role error is classified as `access` when the permission issue is the primary concern.
- A sign-in or lockout caused by a server error, such as a 502 response, is `technical` because the fix concerns the server rather than the account.

## Peer Review

Reviewers should check label consistency, distinct wording and tone, CSV quoting, duplicate text, and the absence of real data.

Teammate peer review and agreement on the edge-case rules are still pending. Automated validation does not replace this review.

## Setup and Running the Model

Run the training script before starting the server or using the predictor.

```powershell
python ai/train.py
```

The trained model artifact, `ai/model.joblib`, is ignored by version control and must be generated locally before running the server or predictor.

## Reproduce the Model

This section explains how to regenerate the model and reproduce the training and evaluation results.

### Prerequisites

Python and the required packages must be installed.

- `joblib`
- `scikit-learn`

Run the commands from the repository root. The inspected training script does not make network requests or require an API key.

### Training Procedure

Run the following command from the repository root:

```powershell
python ai/train.py
```

The script performs these steps:

1. Loads the synthetic ticket dataset from `ai/data/tickets.csv`.
2. Splits the dataset into training and test sets using an 80/20 split, stratified by category, with `random_state=42`.
3. Builds a text-classification pipeline using TF-IDF with unigrams and bigrams, followed by Logistic Regression with `C=10` and `max_iter=1000`.
4. Trains the model on the training split and evaluates it on the test split.
5. Prints test accuracy, the classification report, and incorrect test predictions.
6. Performs five-fold stratified cross-validation using `random_state=42`.
7. Retrains the pipeline using all 36 available examples.
8. Saves the resulting model to `ai/model.joblib`.

The dataset and model paths are constructed relative to the training script's directory. The inspected script contains no network calls and does not reference files outside the repository.

### Verified Reproducibility Results

The existing `ai/model.joblib` file was deleted before the first training run. The command `python ai/train.py` completed successfully and recreated the file. The same command was then run a second time.

Both runs produced matching results.

| Metric | First run | Second run |
|---|---:|---:|
| Test-split accuracy | 0.625 (62.5%) | 0.625 (62.5%) |
| Cross-validation mean accuracy | 0.632 (63.2%) | 0.632 (63.2%) |
| Cross-validation standard deviation | 0.198 | 0.198 |
| Cross-validation fold 1 | 0.875 | 0.875 |
| Cross-validation fold 2 | 0.429 | 0.429 |
| Cross-validation fold 3 | 0.429 | 0.429 |
| Cross-validation fold 4 | 0.857 | 0.857 |
| Cross-validation fold 5 | 0.571 | 0.571 |
| Incorrect test-split predictions | 3 | 3 |
| Model artifact recreated | Yes | Yes |

The classification report and the three incorrect test-split predictions also matched across both runs.

These results confirm repeatability in the tested environment. They do not establish that the model is highly accurate or that the same results have been verified across different software environments.

### Reproducibility Limitations

The dataset contains only 36 synthetic tickets, and the test split contains eight tickets. Each test example therefore has a substantial effect on the reported accuracy. The results should be interpreted cautiously.

The verification was performed using Python 3.14.4, joblib 1.6.0, and scikit-learn 1.9.1. Identical results across other operating systems, Python versions, or library versions have not been established.