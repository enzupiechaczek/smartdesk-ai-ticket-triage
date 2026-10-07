# AI folder

## Dataset Breakdown

The training dataset `ai/data/tickets.csv` contains 36 synthetic support ticket examples balanced across three categories (12 per class):

- **access**: 12 rows
- **billing**: 12 rows
- **technical**: 12 rows
- **Total**: 36 rows

### Hard Cases Included

- **Multi-topic tickets**: Labeled strictly by the root/primary issue (e.g., tickets mentioning checkout UI bugs vs. unauthorized card charges are routed to `billing` if the underlying request is financial reversal).
- **Short queries**: e.g., `"cant log in, fix pls"`, `"Refund pls"`, `"App crash"`.
- **Typo-heavy text**: Real-world phonetics and misspellings (e.g., `"accout is loocked"`, `"invoyce"`, `"downlaod botton throwss"`).

## Ticket categories
- billing: charges, invoices, payments, subscriptions, receipts and refunds.
- technical: software errors, freezes, slow pages, uploads, exports and saving problems.
- access: signing in, passwords, verification codes, account recovery and permissions.


## Training dataset

`data/tickets.csv` contains 36 independently written synthetic support tickets: twelve  `access`, twelve `billing`, and twelve `technical`. The two columns are `ticket_text,category`; labels are lowercase, text containing commas is enclosed in double quotes, and embedded double quotes are doubled.

All examples are fictional and contain no real names, emails, IDs, or incidents. Group B's held-out examples were not consulted and must remain separate from the training data.

## Categories

- **access:** Problems or requests involving authentication, account recovery, workspace invitations, or permissions. This includes locked accounts, multi-factor authentication recovery, and changes to who may view or edit resources.
- **billing:** Questions or problems involving subscription charges, invoices, receipts, taxes, refunds, or payment methods. This includes incorrect seat charges, duplicate payments, and charges after cancellation.
- **technical:** Failures in application behavior or output, including errors, freezes, broken layouts, exports, search, or saved changes. These tickets concern a malfunction rather than an authentication, authorization, or payment request.

## Proposed edge-case rules for A2 review

These rules guide this draft and still need agreement during teammate peer review.

- Classify by the main problem or requested resolution, not by tone or words such as "urgent".
- Failed authentication, expired recovery links, missing permissions, and workspace membership changes are `access`. A general page crash or broken interface after successful sign-in is `technical`.
- A declined subscription payment or access blocked specifically by an unpaid subscription is `billing`. Access denied because of a role or workspace permission is `access`.
- Missing password recovery or invitation messages are `access`; duplicate routine ticket notifications are `technical`.
- A request to correct an invoice amount is `billing`; a malfunction when downloading an otherwise correct invoice is `technical`.
- If a ticket contains unrelated problems with no clear primary request, split it into separate examples or hold it for team review instead of guessing a label.
- If a ticket mixes two problems, label the main problem the user wants solved. Example: a paid-fine card plus an unauthorized role error is `access`.
- A sign-in or lockout caused by a server error (for example a 502) is `technical`, because the fix is on the server, not the account.

## Peer review

Reviewers should check label consistency, distinct wording and tone, CSV quoting, duplicate text, and the absence of real data. Teammate peer review and agreement on the edge-case rules are pending; automated validation does not complete that requirement.


