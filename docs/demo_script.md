# SmartDesk Live Demo: Group A1 (3 minutes)

SmartDesk, built by the EARTech Information Technology interns.

| Time        | Moment                                              | Speaker          |
| ----------- | --------------------------------------------------- | ---------------- |
| 0:00 – 0:25 | 1. Start the server                                 | Hassan Ali       |
| 0:25 – 0:40 | 2. Open the page                                    | Hassan Ali       |
| 0:40 – 1:05 | 3. Submit the urgent ticket                         | Majd             |
| 1:05 – 1:25 | 4. Submit the normal ticket                         | Majd             |
| 1:25 – 1:55 | 5. Explain category, confidence and priority        | Mohammad Ghassan |
| 1:55 – 2:15 | 6. Show urgent first                                | Mohammad Ghassan |
| 2:15 – 2:35 | 7. Stop and restart the server                      | Mahmood          |
| 2:35 – 3:00 | 8. Refresh and show the same ticket IDs and data    | Mahmood          |

## Before the demo

- Clone the latest `main` and complete README step 2 (Linux/macOS) or step 3 (Windows PowerShell) once, so `.venv` exists and packages are installed.
- For a clean dashboard, stop the server and delete `backend/smartdesk.db`. The server creates an empty one on start. The file is not tracked by Git.
- Open `test_tickets.json` so the subjects and descriptions can be copied.
- Keep one terminal at the repository root and one browser window ready.

## Test data

The payloads in [test_tickets.json](../test_tickets.json) contain only `subject` and `description`, so each one can be pasted into the form or posted to `POST /api/tickets` as it is.

The table below lists the **expected** labels separately from the **observed** results. Expected labels come from the priority rule in [priority.md](priority.md) and from the meaning of each ticket. Observed results are what the app returned in the rehearsal recorded below. Confidence can change whenever the model is retrained on different data, so read the real values from the cards during the demo.

| # | Subject                   | Expected category | Expected priority | Observed in rehearsal (category / confidence / priority) |
| - | ------------------------- | ----------------- | ----------------- | -------------------------------------------------------- |
| 1 | Cannot access account     | access            | urgent            | access / 74% / urgent                                    |
| 2 | Cannot sign in to portal  | access            | normal            | access / 87% / normal                                    |
| 3 | Charged twice this month  | billing           | normal            | billing / 88% / normal                                   |
| 4 | Error when saving changes | technical         | normal            | technical / 87% / normal                                 |

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

**Says:** "Hi, we are Group A1. SmartDesk is a small help desk that sorts incoming support tickets for you. One command starts it: it installs what it needs, trains the classification model and starts the server. When you see *Running on http://127.0.0.1:5000*, it is ready."

## 2. Open the page (0:25 – 0:40): Hassan Ali

Open **http://127.0.0.1:5000** in the browser.

**Says:** "Flask serves the page and the API from the same address. At the top is the form a customer fills in, and below it is the dashboard a support agent works from."

## 3. Submit the urgent ticket (0:40 – 1:05): Majd

Submit ticket 1:

- Subject: `Cannot access account`
- Description: `I cannot access my account today`

**Says:** "First, a customer who is locked out. I enter the subject and the description and press *Submit Ticket*. The page confirms it was saved, shows the category and priority, and the ticket appears on the dashboard straight away."

## 4. Submit the normal ticket (1:05 – 1:25): Majd

Submit ticket 2:

- Subject: `Cannot sign in to portal`
- Description: `I cannot sign in to the portal, even though my password appears to be correct.`

**Says:** "Now a second ticket. It is also a sign-in problem, but it is less severe. We submit it *after* the urgent one on purpose, so it is the newest ticket."

## 5. Explain category, confidence and priority (1:25 – 1:55): Mohammad Ghassan

Point at the two cards.

**Says:** "Each card shows three results. The **category** comes from a machine-learning model trained on synthetic tickets, and here it is *access*. The **confidence**, the percentage next to it, is how sure the model is. If it drops below 50%, the card is flagged *Low confidence* so an agent checks it. The **priority** does not come from the model. It is a business rule: phrases like *cannot access*, *outage* or *data loss* make a ticket urgent. The first ticket says *cannot access*, so it is urgent. The second does not match any phrase, so it is normal."

Read out the real percentages on the cards. Do not quote numbers from this script.

## 6. Show urgent first (1:55 – 2:15): Mohammad Ghassan

**Says:** "Look at the order. The normal ticket is the newest, but the urgent ticket is still at the top, with a red border. The dashboard sorts urgent tickets first, then newest first within each priority. That way an agent always sees the most important ticket first."

## 7. Stop and restart the server (2:15 – 2:35): Mahmood

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

## 8. Refresh and show the same ticket IDs and data (2:35 – 3:00): Mahmood

Refresh **http://127.0.0.1:5000**, then open **http://127.0.0.1:5000/api/tickets** in a new tab. The cards do not show IDs, but the API does.

**Says:** "After the restart, both tickets are still there, with the same subjects, categories and priorities. The API shows they also keep the same IDs. Tickets are saved in a SQLite database, not in memory, so nothing is lost when the server stops. That's the A1 part. Next, the AI team explains how the model was trained, and then QA shows how we tested it."

---

## Rehearsal record

### Rehearsal 1: automated technical run

| Field                                         | Value |
| --------------------------------------------- | ----- |
| Date                                          | 2026-10-12, 17:33 – 17:34 (local time) |
| Tested commit                                 | Fresh clone of `main` at `0706db3`, fast-forwarded to `A1-merge-branch` at `0cc6af7`, plus the uncommitted A1 changes in this PR (model-path fix in `backend/app.py`, this script) |
| Machine                                       | Windows 11, Git Bash, Python 3.12 |
| Participants                                  | Automated run by Claude Code (AI assistant) for Mohammad Ghassan. The four speakers did not take part, so nothing was spoken. |
| Model trained                                 | Yes. `start.sh` ran `python ai/train.py` ("Accuracy: 0.625", "Saved model.joblib"). |
| All eight moments completed?                  | Yes, see the results below |
| A1 segment duration                           | 1:07 machine time for all eight moments, including 53 s for the first `start.sh` run (venv creation, package install and training on a fresh clone). Speaking time is not included. |
| Persistence: same IDs and data after restart? | Yes. IDs 1 and 2, with the same subjects, categories, confidences, priorities and timestamps, before and after a full stop and restart. |

How it was run: `start.sh` started and restarted the server. Tickets were sent as the same JSON `POST /api/tickets` request the form makes, not typed into the form. Headless Chrome loaded http://127.0.0.1:5000 after moments 2, 6 and 8 to check what the page actually showed.

| Moment                | Result |
| --------------------- | ------ |
| 1. Start the server   | One `bash ./start.sh` on a fresh clone (no `.venv`, no model). `/api/health` returned 200 `ok` after 53 s. |
| 2. Open the page      | HTTP 200. Form shown, dashboard showed "No tickets yet." |
| 3. Submit urgent      | 201, id 1: access, 74%, urgent |
| 4. Submit normal      | 201, id 2: access, 87%, normal |
| 5. Explain the fields | Each card showed the category, confidence % and priority, matching the API response. |
| 6. Urgent first       | The page showed id 1 (urgent, red border) above id 2 (normal), although id 2 is newer. |
| 7. Stop and restart   | The server stopped completely (health stopped answering), then `./start.sh` brought it back in 8 s. |
| 8. Refresh            | `/api/tickets` returned identical data for ids 1 and 2. The page showed the same two cards in the same order. |

> **Still to do: a live team rehearsal.** The four speakers should run the script once in the browser, typing into the form, and time the full three minutes with speaking. Add the result as "Rehearsal 2" below.
>
> Timing note: on a fresh clone the first `start.sh` takes about 50 seconds, which is longer than the 25 seconds planned for moment 1. Do the "Before the demo" setup first. With `.venv` already installed, the restart in moment 7 took only a few seconds.

## Next parts of the demo

These scripts are written by Groups A2 and B in their own pull requests. The links below will not work until those pull requests are merged.

- [AI demo](demo_ai.md)
- [QA demo](demo_qa.md)
