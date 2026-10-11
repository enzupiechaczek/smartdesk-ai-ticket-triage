# Model Card: SmartDesk AI Ticket Classifier



## Purpose



The SmartDesk AI ticket classifier predicts a support ticket category based on its text. It classifies tickets into three categories: `access`, `billing`, and `technical`.



The model is intended to support ticket triage by helping route incoming support requests. Its predictions are recommendations for assisting human support staff, not final decisions.



## Data



The model was developed using 36 synthetic support ticket examples, with 12 examples per category:



- `access`: Authentication, passwords, account recovery, and permissions.

- `billing`: Payments, invoices, subscriptions, charges, receipts, and refunds.

- `technical`: Application errors, performance problems, uploads, exports, and saving issues.



The dataset is small and synthetic. It does not represent the full variety, wording, or complexity of real support tickets. Results from this dataset should not be assumed to reflect performance on real-world tickets.



## Method



The classifier uses a machine-learning pipeline consisting of:



- \*\*TF-IDF vectorization:\*\* Converts ticket text into numerical features using unigrams and bigrams.

- \*\*Logistic Regression:\*\* Predicts one of the three ticket categories from the text features.



The dataset is split into 80% training data and 20% test data using stratification by category. The split uses `random\_state=42` for repeatability. Five-fold stratified cross-validation is also used to assess performance across multiple splits.



After evaluation, the training script fits the pipeline on all 36 examples and saves the model to `ai/model.joblib`.



## Evaluation



The held-out test set contains eight tickets. The model achieved the following results:



| Metric | Result |

|---|---:|

| Test accuracy | 0.625 (62.5%) |

| Cross-validation mean accuracy | 0.632 (63.2%) |

| Cross-validation standard deviation | 0.198 |

| Access precision | 0.50 |

| Access recall | 1.00 |

| Billing precision | 0.67 |

| Billing recall | 0.67 |

| Technical precision | 1.00 |

| Technical recall | 0.33 |



The test accuracy and cross-validation results indicate that the model can identify some ticket categories, but performance is inconsistent. The cross-validation scores ranged from 0.429 to 0.875, showing variation across the five folds.



One observed failure involved this ticket:



> We updated our billing card details successfully, but the data export script hangs indefinitely at99%



The true category was `technical`, but the model predicted `billing`. The ticket contains billing-related wording alongside a technical problem, and the model appears to have relied on the billing terms instead of identifying the primary issue.



Another technical ticket, â€œSome settings are not being saved after I update them,â€ was incorrectly predicted as `access`. This illustrates the difficulty of classifying short or ambiguous text.



These results describe evaluation on the held-out test split. The saved model is subsequently trained on all 36 examples, so the reported test metrics are not an independent evaluation of that final saved model.



## Limitations



- The dataset contains only 36 synthetic examples and is too small to represent the full range of support tickets.

- The held-out test set contains only eight tickets. Each incorrect prediction changes test accuracy by 12.5 percentage points.

- Technical recall was 0.33 on the test split, meaning the model missed two of the three technical tickets in that evaluation.

- Tickets that contain multiple topics, ambiguous wording, spelling mistakes, or few category-specific terms may be misclassified.

- Cross-validation accuracy varied considerably between folds.

- Performance on real support tickets has not been established.

- The evaluation does not establish that the model is suitable for unattended or high-impact decisions.



Group B review: Please assess whether these limitations are sufficiently clear, identify additional risks, and recommend further evaluation or data improvements.



## Responsible use



Use the classifier as a triage aid, not as a replacement for human judgment.



- Support staff should review predictions, especially when tickets are ambiguous or contain multiple issues.

- Incorrect predictions should be corrected and considered during future dataset improvements.

- Do not rely on this model as the sole basis for decisions affecting account access, payments, refunds, or customer rights.

- Do not treat model confidence as proof that a prediction is correct.

- Use appropriately protected data and follow applicable privacy requirements when working with real support tickets.

- Evaluate the model on a larger, representative dataset before considering broader deployment.



The model should be improved and evaluated further before it is used to automate ticket routing without human oversight.


