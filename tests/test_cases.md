# SmartDesk Test Cases

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TC-ValidAccess-001 | `{"subject":"Unable to access my account","description":"I cannot log into my account"}` | 1. Open the page.<br>2. Type the subject and description.<br>3. Click Submit Ticket.<br>4. Read the response. | `201 -> {"id","same subject","same description","category (access, billing or technical)","confidence between 0 and 1","priority","created_at"}` | `201 -> {"id": 27, "subject": "Unable to access my account", "description": "I cannot log into my account", "category": "technical", "confidence": 0.5, "priority": "normal", "created_at": "2026-10-08T15:48:59.417316+00:00"}` | Pass | ![Screenshot](evidences/TC-ValidAccess-001.png) |
| TC-ValidBilling-002 | `{"subject":"Billing inquiry regarding invoice #12345","description":"I would like to request an itemized breakdown for my latest invoice."}` | 1. Open the page.<br>2. Type the subject and description.<br>3. Click Submit Ticket.<br>4. Read the response. | `201 -> {"id","same subject","same description","category (access, billing or technical)","confidence between 0 and 1","priority","created_at"}` | `201 -> {"id": 28, "subject": "Billing inquiry regarding invoice #12345", "description": "I would like to request an itemized breakdown for my latest invoice.", "category": "technical", "confidence": 0.5, "priority": "normal", "created_at": "2026-10-08T15:49:35.313693+00:00"}` | Pass | ![Screenshot](evidences/TC-ValidBilling-002.png) |
| TC-ValidTechnical-003 | `{"subject":"PDF upload failed","description":"The app freezes when I upload a PDF"}` | 1. Open the page.<br>2. Type the subject and description.<br>3. Click Submit Ticket.<br>4. Read the response. | `201 -> {"id","same subject","same description","technical","confidence","priority","created_at"}` | `201 -> {"id": 29, "subject": "PDF upload failed", "description": "The app freezes when I upload a PDF", "category": "technical", "confidence": 0.5, "priority": "normal", "created_at": "2026-10-08T15:50:43.445570+00:00"}` | Pass | ![Screenshot](evidences/TC-ValidTechnical-003.png) |
| TC-BlankSubject-004 | `{"subject":"","description":"Need help with my account settings"}` | 1. Send POST {{base_url}}/api/tickets with header Content-Type: application/json.<br>2. In Body choose raw, then JSON.<br>3. Send the request shown in the Input column.<br>4. Read the HTTP status and the response body.<br>The request is sent through the API rather than the browser form.| `400 -> {"error":"Subject is required (max 100 characters)"}` | `400 -> {"error": "Subject is required (max 100 characters)"}` | Pass | ![Screenshot](evidences/TC-BlankSubject-004.png) |
| TC-BlankDescription-005 | `{"subject":"Need help with my account settings","description":""}` | 1. Send POST {{base_url}}/api/tickets with header Content-Type: application/json.<br>2. In Body choose raw, then JSON.<br>3. Send the request shown in the Input column.<br>4. Read the HTTP status and the response body.<br>The request is sent through the API rather than the browser form.| `400 -> {"error":"Description is required (max 500 characters)"}` | `400 -> {"error": "Description is required (max 500 characters)"}` | Pass | ![Screenshot](evidences/TC-BlankDescription-005.png) |
| TC-101CharacterSubject-006 | `subject is 101 x characters, description is "I need help logging in"` | 1. Send POST {{base_url}}/api/tickets with header Content-Type: application/json.<br>2. In Body choose raw, then JSON.<br>3. Send the request shown in the Input column.<br>4. Read the HTTP status and the response body.<br>The request is sent through the API rather than the browser form.<br>The body is generated rather than typed, because 101 characters of one letter is awkward to count by hand:<br>`python -c "print('x' * 101)"`<br>Then build the JSON with a real encoder so the result is valid JSON:<br>`python -c "import json; print(json.dumps({'subject': 'x' * 101, 'description': 'I need help logging in'}))"`<br>Paste that single line into Body, raw, JSON.| `400 -> {"error":"Subject is required (max 100 characters)"}` | `400 -> {"error": "Subject is required (max 100 characters)"}` | Pass | ![Screenshot](evidences/TC-101CharacterSubject-006.png) |
| TC-501CharacterDescription-007 | `subject "Technical support request", description is 501 y characters` | 1. Send POST {{base_url}}/api/tickets with header Content-Type: application/json.<br>2. In Body choose raw, then JSON.<br>3. Send the request shown in the Input column.<br>4. Read the HTTP status and the response body.<br>The request is sent through the API rather than the browser form.<br>The body is generated rather than typed, because 501 characters of one letter is awkward to count by hand:<br>`python -c "print('y' * 501)"`<br>Then build the JSON with a real encoder so the result is valid JSON:<br>`python -c "import json; print(json.dumps({'subject': 'Technical support request', 'description': 'y' * 501}))"`<br>Paste that single line into Body, raw, JSON.| `400 -> {"error":"Description is required (max 500 characters)"}` | `400 -> {"error": "Description is required (max 500 characters)"}` | Pass | ![Screenshot](evidences/TC-501CharacterDescription-007.png) |
| TC-DuplicateTicket-008 | `{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}` | 1. Send POST {{base_url}}/api/tickets with the input above.<br>2. Note the first status and id.<br>3. Send the identical request again and note the second status and id.<br>4. Send GET /api/tickets and read back both ids.<br>5. Confirm the subject and description are identical in both stored tickets. | `201 for both submissions, and the second ticket has a different id` | `Fresh rerun on 2026-10-10 at commit 757cda8: both submissions returned 201, ids 13 then 14, with identical subject and description. The linked dashboard image is from an earlier rerun in the same session and shows two cards; it does not show ids and does not evidence the statuses. The request and response file is what evidences this run.` | Pass | ![Rerun dashboard](evidences/TC-DuplicateTicket-008.png) [Request and response evidence](evidences/TC-DuplicateTicket-008-evidence.md) ![Earlier incomplete evidence](evidences/TC-DuplicateTicket-008-historical-partial.png) |
| TC-HTMLLikeText-009 | `{"subject":"<b>Login Problem</b>","description":"I cannot login to my account. <b>Please help.</b>"}` | Storage, via the API: 1. Send POST {{base_url}}/api/tickets with the input above.<br>2. Read how the tags come back in the JSON response.<br> Rendering, in the browser: 3. Open the page, submit the same text, then reload with F5.<br>4. Observe whether the card shows bold text or the literal tags.<br> The API result and the browser observation are recorded separately. | `201 -> {"id","subject stored unchanged","description stored unchanged","category","confidence","priority","created_at"}` | `Storage -> 201 -> {"id": 31, "subject": "<b>Login Problem</b>", "description": "I cannot login to my account. <b>Please help.</b>", "category": "technical", "confidence": 0.5, "priority": "normal", "created_at": "2026-10-08T16:02:08.094161+00:00"}. The JSON response returns the tags literally. Rendering, observed separately in Chrome on 2026-10-10 after a reload: the card showed the literal text <b>Login Problem</b> and <b>Please help.</b> rather than bold text, and the page HTML contained &lt;b&gt; instead of a b element. That is the whole of the observation for this case: it says nothing about script or image handling, which the Task 2934 rows below cover with their own evidence.` | Pass | ![Storage evidence](evidences/TC-HTMLLikeText-009.png) ![Rendering evidence](evidences/TC-HTMLLikeText-009-rendering.png) |
| TC-AmbiguousTicket-010 | `{"subject":"Help needed","description":"i need help"}` | 1. Open the page.<br>2. Type the subject and description.<br>3. Click Submit Ticket.<br>4. Read the response. | `201 -> {"id","same subject","same description","one valid category (access, billing or technical)","confidence between 0 and 1","priority","created_at"}` | `201 -> {"id": 32, "subject": "Help needed", "description": "i need help", "category": "technical", "confidence": 0.5, "priority": "normal", "created_at": "2026-10-08T16:02:33.623465+00:00"}` | Pass | ![Screenshot](evidences/TC-AmbiguousTicket-010.png) |
| TC-MalformedJson-011 | `{"subject":"Help needed","description":}` | 1. Send POST {{base_url}}/api/tickets with header Content-Type: application/json.<br>2. In Body choose raw, then JSON.<br>3. Paste {"subject":"Help needed","description":} exactly, with no value after the last colon.<br>4. Send and read the status and body. | `400 -> {"error":"Request body must be a JSON object"}` | `400 -> {"error": "Request body must be a JSON object"}` | Pass | ![Screenshot](evidences/TC-MalformedJson-011.png) |

## How each result was produced

Three sessions. Nothing was reconstructed from memory and no observed value was
adjusted to make a row pass.

- Main table, API rows other than TC-DuplicateTicket-008: recorded on 2026-10-08 against the
  temporary stub predictor, which returned technical with confidence 0.5 for every ticket. The ids
  27 to 32 are the ones visible in the screenshots linked from those rows, so those rows and their
  evidence match each other. They are the historical record for task 2915 and are not evidence about
  the trained model.
- Main table, TC-DuplicateTicket-008: not historical. It is a fresh rerun on 2026-10-10 at commit
  757cda8 against the trained model, with both 201 statuses and ids 13 then 14. Its request and
  response evidence is a separate file; the dashboard image beside it is from an earlier rerun in the
  same session.
- Current-model API rerun table: a fresh run on 2026-10-11 at commit 04dcb2c, ids 22 to 28, with
  full requests, statuses and responses in its own evidence file.
- An earlier rerun at commit a07ed14 on 2026-10-10 produced real results but was recorded only as
  abbreviated text with no saved request or response evidence, so it could not be verified. Its
  table has been replaced by the 2026-10-11 run above rather than kept, because keeping
  unevidenced numbers next to evidenced ones invites confusion. Nothing in it was reused: the
  2026-10-11 values come from a new run.

Two different things should not be confused. Every API row satisfied its API contract in every
session: valid rows returned 201 with the subject and description echoed back unchanged, and invalid
rows returned 400 with the documented message. Separately, the category expectation on
TC-ValidAccess-001 and TC-ValidBilling-002 did not match what the stub returned, because the stub
returned technical for everything. With the trained model those two rows return access and billing, so
the category expectation was correct all along and the stub was the cause of the earlier failures.

## Current-model API rerun

Run at commit 04dcb2ce188cce5fc027d871ac86de1b231208f1 on 2026-10-11, after
`python ai/train.py` and `python backend/app.py`. The full requests, HTTP statuses
and full responses are in [API current-model evidence](evidences/API-current-model-evidence.md).
The rows below are a summary of that file, not excerpts of it.

| Test ID | Expected | Result | Evidence |
| --- | --- | --- | --- |
| TC-ValidAccess-001 | 201, subject and description unchanged, category one of the three, confidence 0 to 1, priority and created_at present | 201, id 22, subject and description unchanged, category access, confidence 0.768, priority normal, created_at 2026-10-10T21:02:39.140407+00:00 | [API evidence](evidences/API-current-model-evidence.md) |
| TC-ValidBilling-002 | 201, unchanged, valid category, confidence 0 to 1, priority and created_at present | 201, id 23, unchanged, category billing, confidence 0.642, priority normal, created_at 2026-10-10T21:02:39.156060+00:00 | [API evidence](evidences/API-current-model-evidence.md) |
| TC-ValidTechnical-003 | 201, unchanged, technical, priority and created_at present | 201, id 24, unchanged, category technical, confidence 0.661, priority normal, created_at 2026-10-10T21:02:39.169160+00:00 | [API evidence](evidences/API-current-model-evidence.md) |
| TC-BlankSubject-004 | 400 Subject is required | 400, Subject is required (max 100 characters) | [API evidence](evidences/API-current-model-evidence.md) |
| TC-BlankDescription-005 | 400 Description is required | 400, Description is required (max 500 characters) | [API evidence](evidences/API-current-model-evidence.md) |
| TC-101CharacterSubject-006 | 400 Subject is required | 400, Subject is required (max 100 characters) | [API evidence](evidences/API-current-model-evidence.md) |
| TC-501CharacterDescription-007 | 400 Description is required | 400, Description is required (max 500 characters) | [API evidence](evidences/API-current-model-evidence.md) |
| TC-DuplicateTicket-008 | 201 for both, different ids | 201 then 201, id 25 then 26, identical subject and description | [API evidence](evidences/API-current-model-evidence.md) |
| TC-HTMLLikeText-009 | 201, subject and description stored unchanged | 201, id 27, both stored with the tags literal, category access, confidence 0.69 | [API evidence](evidences/API-current-model-evidence.md) |
| TC-AmbiguousTicket-010 | 201, unchanged, one valid category, confidence 0 to 1 | 201, id 28, unchanged, category access, confidence 0.51, priority normal | [API evidence](evidences/API-current-model-evidence.md) |
| TC-MalformedJson-011 | 400 Request body must be a JSON object | 400, Request body must be a JSON object | [API evidence](evidences/API-current-model-evidence.md) |

Browser rendering is not covered by that file. The rendering observation for
TC-HTMLLikeText-009 has its own screenshot.

## Model quality, reported separately

Model accuracy is not a pass or fail condition for any row here.

docs/model_evaluation.md reports two numbers and they are not interchangeable. 0.625 is the accuracy on
the 20% test split, which contains only 8 tickets, so a single wrong prediction moves it by 12.5 points.
0.632 (+/- 0.198) is the 5-fold cross-validation mean, and that report names it the more reliable figure.
Neither is a pass or fail condition for these rows.

The model also mislabels some tickets. TC-Priority-015 was classified billing for a printer problem.
That is a quality observation for the model owners, not an API bug.

## Known gaps

- The current-model API rerun is evidenced as requests, statuses and full responses in
  tests/evidences/API-current-model-evidence.md, but there is no Postman screenshot for each of those
  eleven cases. The main table rows still point at the 2026-10-08 stub screenshots, which match their
  own Actual values but are not evidence about the trained model.
- TC-DuplicateTicket-008 has a dashboard image from an earlier rerun in the same session. The ids and
  statuses come from its request and response file, not from that image.

## Task 2934 - Unsafe and unusual input

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |
|---|---|---|---|---|---|---|
| TC-HTMLBold-001 | `{"subject":"HTML bold test","description":"<b>bold</b>"}` | 1. Enter HTML bold test as Subject.<br>2. Enter `<b>bold</b>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard.<br>5. Reload the dashboard and check the ticket again. | Status Code: 201 — The exact text `<b>bold</b>` is displayed as plain text. It is not rendered as bold HTML. | Status Code: 201 Created. The ticket was successfully created. The dashboard displayed the exact text `<b>bold</b>` as plain text and did not render it as bold HTML. After reloading the dashboard, the exact text remained literal. | PASS | ![HTML bold screenshot](evidences/Task-2934_ScreenShots/html%20bold.png) |
| TC-Script-002 | `{"subject":"Script test","description":"<script>alert(1)</script>"}` | 1. Enter Script test as Subject.<br>2. Enter `<script>alert(1)</script>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard.<br>5. Reload the dashboard and check the ticket again. | Status Code: 201 — The exact script text is displayed as plain text. No JavaScript executes and no alert popup appears. | Status Code: 201 Created. The ticket was successfully created. The response stored the exact text `<script>alert(1)</script>`. The script was displayed as text and no JavaScript alert was observed. After reloading the dashboard, the exact text remained literal and no alert appeared. | PASS | ![Script screenshot](evidences/Task-2934_ScreenShots/script.png) |
| TC-Image-003 | `{"subject":"Image test","description":"<img src=x>"}` | 1. Enter Image test as Subject.<br>2. Enter `<img src=x>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard.<br>5. Reload the dashboard and check the ticket again. | Status Code: 201 — The exact text `<img src=x>` is displayed as plain text. No image is rendered. | Status Code: 201 Created. The ticket was successfully created. The response stored the exact text `<img src=x>`, and no image was rendered on the dashboard. After reloading the dashboard, the exact text remained literal and no image was rendered. | PASS | ![Image screenshot](evidences/Task-2934_ScreenShots/img.png) |
| TC-Spaces-004 | `{"subject":"Spaces test","description":" "}` | 1. Enter Spaces test as Subject.<br>2. Enter only spaces in Description.<br>3. Click Submit Ticket.<br>4. Verify the browser validation behavior in DevTools Network.<br>5. Send the same JSON through Postman to the API. | The spaces-only input is rejected. If browser validation prevents submission, no POST request is sent. The same JSON sent through the API should return an appropriate 400 response. | Browser validation blocked submission; no POST sent. Separately, the same JSON sent through Postman returned Status Code: 400 Bad Request with the response: `"Description is required (max 500 characters)"`. | PASS | ![Spaces screenshot](evidences/Task-2934_ScreenShots/space.png) |
