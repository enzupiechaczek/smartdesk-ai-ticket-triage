# SmartDesk Live Demo: Group A1 (3 minutes)

SmartDesk, built by the EARTech Information Technology interns.

| Time        | Moment                                           | Speaker          |
| ----------- | ------------------------------------------------ | ---------------- |
| 0:00 – 0:25 | 1. Start the server                              | Hassan Ali       |
| 0:25 – 0:40 | 2. Open the page                                 | Hassan Ali       |
| 0:40 – 1:05 | 3. Submit the urgent ticket                      | Majd             |
| 1:05 – 1:25 | 4. Submit the normal ticket                      | Majd             |
| 1:25 – 1:55 | 5. Explain category, confidence and priority     | Mohammad Ghassan |
| 1:55 – 2:15 | 6. Show urgent first                             | Mohammad Ghassan |
| 2:15 – 2:35 | 7. Stop and restart the server                   | Mahmoud          |
| 2:35 – 3:00 | 8. Refresh and show the same ticket IDs and data | Mahmoud          |

## Before the demo

- Clone the latest `main` and complete README step 2 (Linux/macOS) or step 3 (Windows PowerShell) once, so `.venv` exists and packages are installed.
- Use a disposable demo checkout and a synthetic-only database. If an empty dashboard is needed, stop the server and back up any database you need before removing the disposable demo database (`backend/smartdesk.db`; the server creates an empty one on start). Never clear the database between the before and after restart checks in moments 7 and 8.
- Open `test_tickets.json` so the subjects and descriptions can be copied.
- Keep one terminal at the repository root and one browser window ready.

## Test data

The payloads in [test_tickets.json](../test_tickets.json) contain only `subject` and `description`, so each one can be pasted into the form or posted to `POST /api/tickets` as it is.

The table below lists the **expected** labels separately from the **observed** results. Expected labels come from the priority rule in [priority.md](priority.md) and from the meaning of each ticket. Observed results are what the app returned in the automated technical verification recorded below, not in a speaker rehearsal. Confidence can change whenever the model is retrained on different data, so read the real values from the cards during the demo.

| #   | Subject                   | Expected category | Expected priority | Observed in automated verification (category / confidence / priority) |
| --- | ------------------------- | ----------------- | ----------------- | --------------------------------------------------------------------- |
| 1   | Cannot access account     | access            | urgent            | access / 74% / urgent                                                 |
| 2   | Cannot sign in to portal  | access            | normal            | access / 87% / normal                                                 |
| 3   | Charged twice this month  | billing           | normal            | billing / 88% / normal                                                |
| 4   | Error when saving changes | technical         | normal            | technical / 87% / normal                                              |

The demo uses ticket 1 (urgent) and ticket 2 (normal). Tickets 3 and 4 are spares.

---

## 1. Start the server (0:00 – 0:25): Hassan Ali

From the repository root, run the command for the demo machine (README steps 2 and 3).

Linux / macOS (Bash):

```bash
./start.sh
```

Windows (PowerShell):

```powershell
. .\.venv\Scripts\Activate.ps1
python ai/train.py
python backend/app.py
```

**Says:** "Hi, we are Group A1. SmartDesk is a small help desk that sorts incoming support tickets for you. One command starts it: it installs what it needs, trains the classification model and starts the server. When you see _Running on http://127.0.0.1:5000_, it is ready."

## 2. Open the page (0:25 – 0:40): Hassan Ali

Open **http://127.0.0.1:5000** in the browser.

**Says:** "Flask serves the page and the API from the same address. At the top is the form a customer fills in, and below it is the dashboard a support agent works from."

## 3. Submit the urgent ticket (0:40 – 1:05): Majd

Submit ticket 1:

- Subject: `Cannot access account`
- Description: `I cannot access my account today`

The form sends this request body to `POST /api/tickets`:

```json
{
  "subject": "Cannot access account",
  "description": "I cannot access my account today"
}
```

**Says:** "First, a customer who is locked out. I enter the subject and the description and press _Submit Ticket_. The page confirms it was saved, shows the category and priority, and the ticket appears on the dashboard straight away."

## 4. Submit the normal ticket (1:05 – 1:25): Majd

Submit ticket 2:

- Subject: `Cannot sign in to portal`
- Description: `I cannot sign in to the portal, even though my password appears to be correct.`

```json
{
  "subject": "Cannot sign in to portal",
  "description": "I cannot sign in to the portal, even though my password appears to be correct."
}
```

**Says:** "Now a second ticket. It is also a sign-in problem. The priority rule returns normal because no configured urgent phrase matched. A rule result does not independently establish actual severity. We submit it _after_ the urgent one on purpose, so it is the newest ticket."

## 5. Explain category, confidence and priority (1:25 – 1:55): Mohammad Ghassan

Point at the two cards.

**Says:** "Each card shows three results. The **category** comes from a machine-learning model trained on synthetic tickets, and here it is _access_. The **confidence**, the percentage next to it, is how sure the model is. If it drops below 50%, the card is flagged _Low confidence_ so an agent checks it. The **priority** does not come from the model. It is a business rule: phrases like _cannot access_, _outage_ or _data loss_ make a ticket urgent. The first ticket says _cannot access_, so it is urgent. For the second ticket, the priority rule returns normal because no configured urgent phrase matched. A rule result does not independently establish actual severity."

Read out the real percentages on the cards. Do not quote numbers from this script.

## 6. Show urgent first (1:55 – 2:15): Mohammad Ghassan

**Says:** "Look at the order. The normal ticket is the newest, but the urgent ticket is still at the top, with a red border. The dashboard sorts urgent tickets first, then newest first within each priority. That way an agent always sees the most important ticket first."

## 7. Stop and restart the server (2:15 – 2:35): Mahmoud

In the server terminal, press `Ctrl+C`, then start the server again.

Linux / macOS:

```bash
./start.sh
```

Windows (PowerShell, with `.venv` still active):

```powershell
python backend/app.py
```

**Says:** "Now I stop the server completely, as if the machine had restarted, and start it again."

## 8. Refresh and show the same ticket IDs and data (2:35 – 3:00): Mahmoud

Refresh **http://127.0.0.1:5000**, then open **http://127.0.0.1:5000/api/tickets** in a new tab. The cards do not show IDs, but the API does.

**Says:** "After the restart, both tickets are still there, with the same subjects, categories and priorities. The API shows they also keep the same IDs. Tickets are saved in a SQLite database, not in memory, so nothing is lost when the server stops. That's the A1 part. Next, the AI team explains how the model was trained, and then QA shows how we tested it."

---

## Automated technical verification

These are automated technical checks run by Claude Code (an AI assistant). **The speakers did not take part and nothing was spoken.** They are not a rehearsal and do not measure presentation time. Tickets were sent as the same JSON `POST /api/tickets` request the form makes, not typed into the form. Headless Chrome loaded the page to check what the cards showed. That checks the card fields, not the spoken explanation in moment 5.

### Run 1: 2026-10-12, 17:33 – 17:34 (local time, time zone not recorded)

| Field                      | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Run for                    | Mohammad Ghassan                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Tested code                | Fresh clone of `main` at `0706db3`, fast-forwarded to `A1-merge-branch` at `0cc6af7`, plus uncommitted changes to `backend/app.py` (model path) and this script. The patch was not saved, so its exact content is not recorded. Commit `0c4d631` committed an `app.py` model-path change at 17:45; whether it is identical to the tested patch was not recorded. At `0cc6af7`, `app.py` also stopped at startup when the model was missing; that check has since been removed (see Run 2). |
| Machine                    | Windows 11, Git Bash, Python 3.12 (exact versions not recorded)                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Model trained              | Yes. `start.sh` ran `python ai/train.py` ("Accuracy: 0.625", "Saved model.joblib").                                                                                                                                                                                                                                                                                                                                                                                                        |
| Technical checks exercised | Server start and restart with `start.sh`, `/api/health`, page load, two `POST /api/tickets` requests, card fields and order in headless Chrome, `/api/tickets` before and after the restart. See the table below.                                                                                                                                                                                                                                                                          |
| Machine execution time     | 1:07 from the first `start.sh` to the last check, including 53 s for the first `start.sh` run (venv creation, package install and training). This is machine time, not presentation duration.                                                                                                                                                                                                                                                                                              |
| Persistence                | IDs 1 and 2, with the same subjects, categories, confidences, priorities and timestamps, before and after a full stop and restart.                                                                                                                                                                                                                                                                                                                                                         |

| Check                  | Result                                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1. Start the server    | One `bash ./start.sh` on a fresh clone (no `.venv`, no model). `/api/health` returned 200 `ok` after 53 s.      |
| 2. Open the page       | HTTP 200. Form shown, dashboard showed "No tickets yet."                                                        |
| 3. Submit urgent       | 201, id 1: access, 74%, urgent                                                                                  |
| 4. Submit normal       | 201, id 2: access, 87%, normal                                                                                  |
| 5. Card fields         | Each card showed the category, confidence % and priority, matching the API response. No explanation was spoken. |
| 6. Urgent first        | The page showed id 1 (urgent, red border) above id 2 (normal), although id 2 is newer.                          |
| 7. Stop and restart    | The server stopped completely (health stopped answering), then `./start.sh` brought it back in 8 s.             |
| 8. Refresh and compare | `/api/tickets` returned identical data for ids 1 and 2. The page showed the same two cards in the same order.   |

### Run 2: 2026-10-12, 18:14 – 18:16 (+03:00), final code

| Field                      | Value                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tested code                | Fresh clone of `A1-merge-branch` at `e5d3f96` (which includes `main` at `0706db3`), with one uncommitted change: the startup exit removed from `backend/app.py`. The tested `backend/app.py` is blob `7bdd2a98443f42b02f96c9ffab990c4a082fd9e3`, the same file as in the commit that adds this record (check with `git rev-parse HEAD:backend/app.py`). No other code file differed from `e5d3f96`. |
| Machine                    | Windows 11 Pro 10.0.26300, Git Bash (bash 5.3.15), Python 3.12.7, headless Chrome for the page checks                                                                                                                                                                                                                                                                                               |
| Start state                | No `.venv`, no `ai/model.joblib`, no `backend/smartdesk.db`                                                                                                                                                                                                                                                                                                                                         |
| Model trained              | Yes. `start.sh` ran `python ai/train.py` ("Accuracy: 0.625", "Saved model.joblib").                                                                                                                                                                                                                                                                                                                 |
| Technical checks exercised | The same checks as Run 1, listed below. The restart was started from outside the repository folder.                                                                                                                                                                                                                                                                                                 |
| Machine execution time     | 1:58 from the first `start.sh` to the after-restart comparison, including pauses between steps that were run one at a time. This is machine time, not presentation duration.                                                                                                                                                                                                                        |
| Persistence                | IDs 1 and 2, every field identical in `/api/tickets` before and after the restart. The page showed the same two cards in the same order.                                                                                                                                                                                                                                                            |

| Check                  | Result                                                                                                                                                                                                           |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Start the server    | `./start.sh` from the repository root created `.venv`, installed the requirements, trained and started. `/api/health` returned 200 `{"service": "SmartDesk local API", "status": "ok"}` after 71 s.              |
| 2. Open the page       | `GET /` returned 200 with the ticket form. `/api/tickets` returned `[]`.                                                                                                                                         |
| 3. Submit urgent       | 201, id 1: access, 0.739, urgent                                                                                                                                                                                 |
| 4. Submit normal       | 201, id 2: access, 0.867, normal                                                                                                                                                                                 |
| 5. Card fields         | Chrome showed "Category: access (74%) \| Priority: urgent" and "Category: access (87%) \| Priority: normal". No explanation was spoken.                                                                          |
| 6. Urgent first        | Chrome showed the urgent card (id 1) above the newer normal card (id 2). `/api/tickets` listed id 1 first.                                                                                                       |
| 7. Stop and restart    | The server process was ended and `/api/health` refused connections; `backend/smartdesk.db` was kept. `start.sh`, run from the folder above the repository, brought the server back: `/api/health` 200 after 7 s. |
| 8. Refresh and compare | `/api/tickets` returned the same ids 1 and 2 with identical data. Chrome showed the same two cards in the same order.                                                                                            |

Evidence for these checks is split by session:

- Unit tests run with and without a trained model: [Test evidence](../testevidence.md). The tests import and are discovered without a model; `test_valid_ticket_is_created` needs one.
- Earlier manual startup session at commit [3030606](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/commit/3030606b93ff7fac7cc4b901b53f03a37461d5b4), on Windows 11 and Ubuntu 24.04 (WSL): [Startup evidence](../startupevidence.md). That session predates the removal of the startup exit and does not verify the final health behaviour.

The `/api/health` response on an untrained setup, with the final code, is not recorded in either file yet.

## Speaker rehearsal

**Pending: not yet performed.** Fill in each field only after the four speakers have run the script once from a fresh clone of `main`, in a browser, typing into the form and speaking their lines. Do not record rehearsal results or handoff outcomes before that run is performed.

| Field                                                 | Value     |
| ----------------------------------------------------- | --------- |
| Date, time and time zone                              | [pending] |
| Tested version (`git rev-parse HEAD`, fresh clone)    | [pending] |
| Environment (OS, Python version, startup command)     | [pending] |
| Participants                                          | [pending] |
| Measured spoken duration of the A1 part (target 3:00) | [pending] |
| Urgent ticket: id, category, confidence, priority     | [pending] |
| Normal ticket: id, category, confidence, priority     | [pending] |
| Urgent card above the newer normal card?              | [pending] |
| Same IDs and data after the restart?                  | [pending] |
| Problems seen and changes made                        | [pending] |

## Next parts of the demo

These scripts are written by Groups A2 and B in their own pull requests, so the links below are pending and will not work until those pull requests are merged. On 12 October 2026 the AI demo was in PR #50 (open, not merged) and no QA demo pull request existed yet. The hand-over order (A1 shows the app, A2 explains the model, B explains the testing) and the three-minute limits still have to be agreed with the A2 and B owners.

- [AI demo](demo_ai.md)
- [QA demo](demo_qa.md)

## Health-check evidence

The affected health checks were rerun in a clean disposable checkout without
touching the working checkout's model or database. See the complete record of
the commit, environment, commands, training result, server logs, and actual
`GET /api/health` responses in [health_check_evidence.md](health_check_evidence.md).
