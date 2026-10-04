# SmartDesk

A local AI-powered support-ticket triage application, built by the EARTech Information Technology interns.

A user submits a support ticket (subject and description). A Python Flask server checks it, a locally trained machine learning model predicts the category (access, billing or technical) with a confidence score, a documented rule sets the priority (urgent or normal), and the ticket is saved in SQLite. The web page shows tickets as cards with urgent tickets first.

## Tech stack

Python 3.11 or newer, Flask, SQLite, scikit-learn (TF-IDF and Logistic Regression), HTML, CSS, JavaScript, Git and GitHub.

## Project structure

```
frontend/   Web page (HTML, CSS, JavaScript)          Group A1
backend/    Flask server, database, priority rule     Group A1
ai/         Dataset, training, predictor              Group A2
tests/      Test plan, held-out data, bug template    Group B
docs/       Architecture, model card, reports         All groups
```

## How to run SmartDesk

Group A1 completes this section on Day 4 (task A1-4.2). Until then, follow your task in Azure Boards.

## How we work

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you push anything. The short version:

1. Never push to `main`.
2. Work on your task branch.
3. Sync with `main` before you push.
4. Open a pull request. Enzu reviews and merges.

## Rules

- Synthetic data only. No real names, emails or customer data.
- No keys, tokens or passwords in code, screenshots or chat.
- The model works offline and never calls a paid or cloud AI service.
