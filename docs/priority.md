# Ticket Priority Rules

The model predicts a ticket's **category**. **Priority** is a business rule
owned by the app (`backend/priority.py`), not by the model.

## Rule

A ticket is **urgent** if its subject or description contains any of these
whole words or phrases, in any capitalisation:

- cannot access
- locked out
- outage
- down
- all users
- everyone
- production
- data loss

Otherwise the ticket is **normal**.

## Matching details

- Subject and description are joined and lowercased before matching.
- Matching is on **whole words/phrases** (regex word boundaries).
  - "download" does NOT match "down".
  - "The server is down" DOES match "down".
- Multi-word phrases must appear with a single space, e.g. "cannot access".
  "can not access" and "can't access" do NOT match.
- One match is enough. Matching more than one phrase is still just "urgent".

## Examples for Group B

| Subject        | Description                        | Expected                               |
| -------------- | ---------------------------------- | -------------------------------------- |
| Login broken   | I cannot access my account         | urgent                                 |
| Server DOWN    | Site unreachable                   | urgent                                 |
| Slow report    | Everyone in finance sees delays    | urgent                                 |
| Download fails | The download button gives an error | normal                                 |
| Printer issue  | Paper jam on floor 2               | normal                                 |
| Reproduction   | Seen in Production last night      | urgent                                 |
| Typo           | Can't access the page              | normal (apostrophe form is not listed) |
| Shutdown       | Please schedule a shutdown         | normal ("down" is inside a word)       |

## Known edge cases (for discussion with Group B)

- "down" is broad: "Please scroll down" or "down arrow key" will be urgent.
- "everyone" can be casual: "Thanks everyone" will be urgent.
- "can't access" / "cant access" are not covered unless we add them.
- Hyphenated words such as "break-down": the hyphen counts as a word
  boundary, so "down" matches.

Changes to this list must be agreed with Group B so their tests stay accurate.
