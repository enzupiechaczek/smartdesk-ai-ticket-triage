# Task 2931: Failure Analysis and Training Data Improvement

Historical author-reported results from the original PR #47; original run timestamps, tested revisions, and captured outputs were not supplied. These values are not a fresh verification of the updated 42-row model. The six evaluation cases were previously exposed in Git history, so this is a separate evaluation set rather than a blind benchmark. Versioned fresh-run evidence is being prepared locally.

## 1. Objective

The objective was to analyse incorrect separate-set predictions, add six synthetic training examples for the technical category, retrain the model, and compare performance before and after the change.

## 2. Baseline

Before adding the six training examples:

* Training dataset: 36 tickets
* Technical examples: 12
* Separate-set evaluation dataset: 6 tickets
* Separate-set accuracy: 4/6 (66.7%)

## 3. Failure Analysis

### Failure 1: Registered email address update

* **Ticket:** CASE-001
* **True category:** access
* **Predicted category before improvement:** billing
* **Confidence before improvement:** 0.413
* **Predicted category after improvement:** billing
* **Confidence after improvement:** 0.396
* **Outcome:** Incorrect before and after retraining.

**Possible explanation:** This ticket describes an account-related change, but it does not explicitly mention a sign-in problem. The model may not have enough context to distinguish an account-access request from other account-related requests. This is a hypothesis, not a confirmed explanation of the model's internal decision.

**Potential impact:** The request could be routed to the wrong support team, delaying assistance.

### Failure 2: Unable to update email

* **Ticket:** CASE-005
* **True category:** technical
* **Predicted category before improvement:** access
* **Confidence before improvement:** 0.465
* **Predicted category after improvement:** access
* **Confidence after improvement:** 0.439
* **Outcome:** Incorrect before and after retraining.

**Possible explanation:** The ticket is brief and does not explain what happens when the user tries to update the email address. The model may associate email-related wording with account access because the ticket does not clearly describe an application error or failed operation.

**Potential impact:** The ticket could be routed to access support instead of the team responsible for investigating a failed application function.

## 4. Training Data Improvement

Added six synthetic examples labelled `technical` to `ai/data/tickets.csv`. They cover:

1. A report page returning an internal server error.
2. An application crash during document upload.
3. Search results stopping after a filter change.
4. A timeout while retrieving records.
5. An export failure before a download is generated.
6. Notification preferences not being saved.

The training dataset now contains 42 tickets, including 18 technical examples. The separate-set dataset remains unchanged at six tickets. No separate-set examples were added to the training data.

## 5. Before-and-After Results

| Metric                              |                Before |       After |
| ----------------------------------- | --------------------: | ----------: |
| Training dataset size               |                    36 |          42 |
| Technical training examples         |                    12 |          18 |
| Training script test-split accuracy | Baseline not recorded |       55.6% |
| Five-fold cross-validation mean     |                 63.2% |       78.3% |
| Separate-set accuracy                   |           4/6 (66.7%) | 4/6 (66.7%) |
| Incorrect separate-set predictions      |                     2 |           2 |

The separate-set accuracy remained at 66.7% after retraining. Both email-related errors remained unchanged. The cross-validation mean increased from 63.2% to 78.3%, but the small dataset and variation between folds mean that this result should be interpreted cautiously. The training script's test-split accuracy and separate-set accuracy come from different evaluation sets and should not be treated as directly comparable.

## 6. Conclusion and Next Steps

Adding six technical examples increased the representation of technical tickets in the training data, but did not resolve the two observed separate-set classification errors.

Possible next steps include adding carefully labelled examples that distinguish account-access requests from account-profile changes and technical failures. The team should review the categories and consider whether these routing outcomes would affect real support agents.

Group discussion and supervisor review should be documented once completed.

## 7. Evidence

* Training output after adding the six examples.
* Separate-set evaluation output after retraining.
* Commit and pull request link to be added after submission.
