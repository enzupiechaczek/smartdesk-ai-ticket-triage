# Model contract

predict_category(text) Contract
Purpose

predict_category(text) classifies plain ticket text into one of three categories and returns a confidence score.

Function Signature
predict_category(text)

Input
      
text: A plain-text support ticket.

The input should be a string containing the ticket's text.

Output

Returns a dictionary with exactly these fields:

{
    "category": "access",
    "confidence": 0.95
}


category: One of:

access — account login, password, authentication, verification, or account recovery issues.

billing — payments, invoices, charges, subscriptions, receipts, or billing issues.

technical — software errors, application behavior, performance, uploads, downloads, or other technical issues.

confidence: A numeric value from 0 to 1, inclusive, representing confidence in the predicted category.

Requirements

The function must accept plain ticket text without requiring additional metadata.

The returned category must be exactly one of access, billing, or technical.

The returned confidence must be between 0 and 1, inclusive.

Higher confidence indicates greater certainty in the classification.



Rules
- It works fully offline.
- It never calls Azure, OpenAI, or any paid service.
- It never requires an API key.
