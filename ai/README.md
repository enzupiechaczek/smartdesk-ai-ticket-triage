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