# SmartDesk AI Ticket Classifier — Demo Script



## Objective



Demonstrate how the SmartDesk AI ticket classifier predicts support ticket categories and explain its current limitations.



**Duration:** Under 2 minutes



## Demo walkthrough



### 1. Introduction (15 seconds)



"SmartDesk AI is a ticket classification project designed to assist support teams with routing incoming tickets. The model predicts one of three categories: access, billing, or technical. Its purpose is to support human decision-making, not replace it."



### 2. Explain the model (20 seconds)



"The classifier uses TF-IDF to convert ticket text into numerical features. A Logistic Regression model uses these features to predict the most likely category. The prediction also includes a confidence score to help users interpret the result."



### 3. Demonstrate a prediction (25 seconds)



"I will test a ticket about a user who cannot log in after resetting a password. This is an access-related issue. In a previous test, the model predicted `access` with a confidence score of 0.844. This demonstrates an example where the predicted category matches the nature of the ticket."



### 4. Show a limitation (25 seconds)



"The model does not classify every ticket correctly. During evaluation, a ticket reporting that a data export script hangs was incorrectly classified as `billing`, even though its expected category was `technical`. This illustrates why predictions need to be reviewed by a human support agent."



### 5. Conclusion (15 seconds)



"The model is a useful starting point for automated ticket triage, but the dataset contains only 36 synthetic examples. More representative data and further evaluation are needed before relying on it in a real support environment."



## Key points to demonstrate



\- The three supported categories: `access`, `billing`, and `technical`.

\- How the model returns a predicted category and confidence score.

\- One example of a correct prediction and one documented misclassification.

\- Why human review and further evaluation remain important.



## Demo outcome



The demonstration explains the model's workflow, illustrates its predictions, and communicates its current limitations and responsible-use requirements.


