# SmartDesk Ticket Dataset

The dataset contains synthetic support tickets classified into three categories.

- **access**: Issues related to signing in, passwords, account access, and authentication.
- **billing**: Issues related to payments, invoices, subscriptions, charges, and refunds.
- **technical**: Issues related to application errors, broken features, crashes, performance, and other technical problems.

All tickets are synthetic and do not contain real user information.

## Edge-case rules

Label the main problem described in the ticket. Do not infer a cause that the ticket does not state.

- Use **access** for rejected credentials, account lockouts, password resets, authentication, and permission denials. A password reset link that does not work is access unless the ticket explicitly describes a software failure such as a page crash.
- Use **billing** for charges, invoices, refunds, subscription payments, renewals, cancellations, and payment-method changes. A failed payment or an inability to update a payment method stays billing when no specific software failure is described.
- Use **technical** for an explicit crash, freeze, blank page, server error, slow performance, or broken application feature. This includes a crash on a login or payment page when the crash is the main reported problem.
- Distinguish permission problems from broken features: being denied permission to download a file is access; a download that fails without an authentication or permission issue is technical. An invoice-copy request is billing.
- For tickets mentioning multiple categories, use the explicit cause when one problem clearly causes the others. For example, an account blocked because of an unpaid subscription is billing. If there are separate problems or no clear primary issue, flag the ticket for team review before adding it to the dataset; do not guess a label or introduce another category.

## Review status

An assistant review checked all 30 tickets against these rules and found no label changes necessary. CSV validation confirmed 10 access, 10 billing, and 10 technical tickets, with no empty fields, invalid labels, or duplicate ticket texts after normalizing case and whitespace. The tickets contain no apparent personal data.

Team peer review and agreement on these edge-case rules are pending. A teammate must review the rows and rules in the pull request; Enzu's review and merge are also required before the task is complete.
