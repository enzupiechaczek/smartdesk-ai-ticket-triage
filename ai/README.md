# AI folder

## Ticket categories
- billing: charges, invoices, payments, subscriptions, receipts and refunds.
- technical: software errors, freezes, slow pages, uploads, exports and saving problems.
- access: signing in, passwords, verification codes, account recovery and permissions.

Placeholder. Group A2 explains the categories in task A2-1.1.
There are 37 ticket description in ticket.csv file.
## Training dataset

`data/tickets.csv` contains 24 independently written synthetic support tickets: eight `access`, eight `billing`, and eight `technical`. The two columns are `ticket_text,category`; labels are lowercase, text containing commas is enclosed in double quotes, and embedded double quotes are doubled.

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

## Peer review

Reviewers should check label consistency, distinct wording and tone, CSV quoting, duplicate text, and the absence of real data. Teammate peer review and agreement on the edge-case rules are pending; automated validation does not complete that requirement.


