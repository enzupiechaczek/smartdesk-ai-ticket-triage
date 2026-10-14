# SmartDesk QA — Two-Minute Demo

A two-minute talk on how SmartDesk was tested and what testing found.

## The numbers

| | Count | What they cover |
|---|---:|---|
| Regression cases | **28** | The full test suite from `tests/test_cases.md` |
| Built-in unit tests | **17** | API validation and priority rules in `backend/` |

The 28 cases split three ways:

| Kind | Count | What they prove |
|---|---:|---|
| API validation | **11** | Valid tickets are stored unchanged; invalid ones get the documented 400 |
| Priority rules | **13** | Urgent phrases are detected, and near-misses like "download" are not |
| Unsafe input | **4** | HTML, scripts, images and spaces are stored as literal text, never executed |

## The bug that surprised me most

**The app said it was healthy while it was broken.**

The README never told you to run `python ai/train.py`. Without a model:

- `GET /api/health` returned `200 {"status":"ok"}`
- Every `POST /api/tickets` returned **500**

So the one check the README asks you to perform — "open `/api/health`, you should see ok" — **passed while the app could not do its only job.**

![Health check reporting ok with no model](before_and_after_evidences/before-health-returns-ok.png)

## How it was fixed

Current `main` returns a real answer:

```
GET /api/health  ->  503
{"status": "error", "message": "Model not trained. Run python ai/train.py"}
```

The README now has the training step, and documents the 503. The ticket endpoint behaves exactly as before — 500 without a model, 201 with one. Only the reporting changed.

![Health check reporting the truth](before_and_after_evidences/after-health-returns-503.png)

## What is still risky

| Issue | Status |
|---|---|
| Built-in test suite fails on a fresh clone | Open — it needs a model it never trains |
| `ResourceWarning: unclosed database` in `backend/test_api.py` | Still present, exit 0 |
| Stale stub note in `README.md` | Still claims a temporary stub exists |

None of these block a user. All three are worth a small follow-up.

## One line

Testing found that **the app's own health check was lying**, and the fix means it now tells you what to run instead of letting you discover a 500 the hard way.
