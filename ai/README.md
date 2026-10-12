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

This section documents the 36-row dataset baseline, the training procedure, the historical two-run comparison, and a separately captured fresh verification.

### Baseline and environment

The baseline is tied to the versioned dataset `ai/data/tickets.csv`, containing 36 synthetic tickets.

- **Baseline dataset SHA-256:** `525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1`
- **Commit tested during fresh verification:** `6be765d874141750d1b4cac81bb1d410aa51edda`
- **Operating system:** Microsoft Windows 11 Pro, version 10.0.22000, build 22000
- **Python:** 3.14.4
- **pip:** 26.0.1
- **AI dependencies:** `joblib` 1.6.0 and `scikit-learn` 1.9.1

The complete installed package versions are recorded in [`docs/evidence/requirements-ai-baseline-2026-10-11.txt`](../docs/evidence/requirements-ai-baseline-2026-10-11.txt). The fresh verification output, timestamp, commit, dataset hash, operating system, and package details are recorded in [`docs/evidence/training-baseline-2026-10-11.txt`](../docs/evidence/training-baseline-2026-10-11.txt).

### Fresh-environment setup

The commands below are for Windows PowerShell. Install Python 3.14.4 first and run the commands from the repository root.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip==26.0.1
python -m pip install -r docs\evidence\requirements-ai-baseline-2026-10-11.txt
python -m pip show joblib scikit-learn
```

Confirm that `python --version` reports Python 3.14.4 before proceeding. The requirements snapshot pins the packages observed in the verification environment; it does not install Python itself or guarantee identical behavior on other operating systems.

### Clean-environment verification — 2026-10-12 (Git Bash)

A separate clean-environment verification was completed on Microsoft Windows (build 10.0.26300.9550) using Python 3.14.8 and pip 26.0.1.

The verification used commit `0c65c2fb6f7afccec91c980d69476a6b2a24ce80` and the existing 36-row dataset in `ai/data/tickets.csv`.

Dataset SHA-256:

`525ac01b9a55b86bb69d77b17128d5529535d1844f9018cf8dce1db4c2f896a1`

The following commands were used from the repository root in Git Bash:

```bash
py -3.14 -m venv .venv-repro-check
source .venv-repro-check/Scripts/activate
python --version
python -m pip install --upgrade pip==26.0.1
python -m pip install -r docs/evidence/requirements-ai-baseline-2026-10-11.txt
python -m pip check
python -m pip show scikit-learn numpy scipy joblib
python ai/train.py
```

All seven pinned dependencies installed successfully in the separate virtual environment. `pip check` reported no broken requirements.

The requirements snapshot initially contained a UTF-8 BOM, which was removed without changing the pinned dependency versions. The corrected file was subsequently accepted by pip with all requirements already satisfied. This subsequent check was not a second clean installation.

Training completed with exit status `0` and reproduced the previously documented printed results:

- Test accuracy: **0.625 (62.5%)**
- Cross-validation mean accuracy: **0.632**
- Cross-validation standard deviation: **0.198**
- Incorrect test predictions: **3**

The classification report, cross-validation fold scores and incorrect predictions matched the previously documented baseline.

The captured verification is available in [`docs/evidence/training-clean-setup-2026-10-12.txt`](../docs/evidence/training-clean-setup-2026-10-12.txt).

**Limitations:** This verification used Python 3.14.8 rather than the previously recorded Python 3.14.4. Matching printed results do not establish byte-identical model artifacts or reproducibility across different environments. The original historical two-run logs remain unavailable. These results apply only to the existing 36-row dataset baseline; PR #47 proposes a different dataset version.

### Training procedure

Run the following command from the repository root:

```powershell
python ai/train.py
```

The script:

1. Loads `ai/data/tickets.csv`.
2. Splits the data into training and test sets using an 80/20 split, stratified by category, with `random_state=42`.
3. Builds a text-classification pipeline using TF-IDF unigrams and bigrams, followed by Logistic Regression with `C=10` and `max_iter=1000`.
4. Trains and evaluates the model on the training and test split.
5. Prints test accuracy, the classification report, and incorrect test predictions.
6. Performs five-fold stratified cross-validation using `random_state=42`.
7. Retrains the pipeline using all 36 examples.
8. Saves the generated model as `ai/model.joblib`.

The inspected training script contains no network requests or API-key requirements. The generated model is an output artifact and should not be committed.

### Historical two-run baseline

The previously recorded comparison reported matching metrics, classification reports, and incorrect test predictions across two training runs. The original raw logs and run-specific environment metadata were not retained, so the historical runs cannot now be independently verified from those original outputs.

| Metric | Previously recorded run 1 | Previously recorded run 2 |
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

These values describe the previously recorded 36-row baseline, not a guarantee about future dataset versions.

### Fresh verification - 11 October 2026

A fresh training run was captured on commit `6be765d874141750d1b4cac81bb1d410aa51edda` using the environment and dataset identified above. The command `python ai/train.py` completed successfully and recreated the model artifact.

The fresh run produced:

- Test-split accuracy: `0.625`
- Cross-validation fold accuracies: `[0.875, 0.429, 0.429, 0.857, 0.571]`
- Cross-validation mean accuracy: `0.632`
- Cross-validation standard deviation: `0.198`
- Incorrect test-split predictions: 3

The fresh classification report and the three incorrect predictions are preserved in the training evidence file. These observations match the previously recorded baseline results. This fresh run is separate evidence; it does not replace the missing original logs for the historical two-run comparison.

The reported repeatability concerns printed evaluation results. No comparison of model-artifact hashes was performed, so byte-for-byte identity of generated model files has not been established.

### Limitations and dataset updates

The dataset contains only 36 synthetic tickets, and the test split contains eight tickets. Each test example therefore has a substantial effect on the reported accuracy. These results should not be interpreted as proof of production readiness or generalization to real-world support tickets.

These metrics are the baseline for this specific dataset version. PR #47 proposes a 42-row dataset. If that change is merged, coordinate the update with the dataset owner and rerun training before publishing new results. Record the new dataset hash and verification evidence, and clearly distinguish the new results from this 36-row baseline.
