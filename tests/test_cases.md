# SmartDesk test cases

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |
| TC-ValidAccess-001 |---|---|---|---|---|---|
| TC-ValidBilling-002 |---|---|---|---|---|---|
| TC-ValidTechnical-003 |---|---|---|---|---|---|
| TC-BlankSubject-004 |---|---|---|---|---|---|
| TC-BlankDescription-005 |---|---|---|---|---|---|
| TC-101CharacterSubject-006 |---|---|---|---|---|---|
| TC-501CharacterDescription-007 |---|---|---|---|---|---|
| TC-CharacterDescription-008 |---|---|---|---|---|---|
| TC-DuplicateTicket-009 |---|---|---|---|---|---|
| TC-HTMLLikeText-010 |---|---|---|---|---|---|
| TC-AmbiguousTicket-011 |---|---|---|---|---|---|

## Task 2934 - Unsafe and unusual input

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |
|---|---|---|---|---|---|---|
| TC-HTMLBold-001 | `{"subject":"HTML bold test","description":"<b>bold</b>"}` | 1. Enter HTML bold test as Subject.<br>2. Enter `<b>bold</b>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard. | Status Code: 201 — The exact text `<b>bold</b>` is displayed as plain text. It is not rendered as bold HTML. | Status Code: 201 Created. The ticket was successfully created. The dashboard displayed the exact text `<b>bold</b>` as plain text and did not render it as bold HTML. | PASS | ![HTML bold screenshot](evidences/Task-2934_ScreenShots/html%20bold.png) |
| TC-Script-002 | `{"subject":"Script test","description":"<script>alert(1)</script>"}` | 1. Enter Script test as Subject.<br>2. Enter `<script>alert(1)</script>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard. | Status Code: 201 — The exact script text is displayed as plain text. No JavaScript executes and no alert popup appears. | Status Code: 201 Created. The ticket was successfully created. The response stored the exact text <script>alert(1)</script>. The script was displayed as text and no JavaScript alert was observed. | PASS | ![Script screenshot](evidences/Task-2934_ScreenShots/script.png) |
| TC-Image-003 | `{"subject":"Image test","description":"<img src=x>"}` | 1. Enter Image test as Subject.<br>2. Enter `<img src=x>` as Description.<br>3. Click Submit Ticket.<br>4. Check the Ticket Dashboard. | Status Code: 201 — The exact text `<img src=x>` is displayed as plain text. No image is rendered. | Status Code: 201 Created. The ticket was successfully created. The response stored the exact text <img src=x>, and no image was rendered on the dashboard. | PASS | ![Image screenshot](evidences/Task-2934_ScreenShots/img.png) |
| TC-Spaces-004 | `{"subject":"Spaces test","description":" "}` | 1. Enter Spaces test as Subject.<br>2. Enter only spaces in Description.<br>3. Click Submit Ticket.<br>4. Verify the validation message. | The spaces-only input is rejected. If browser validation prevents submission, no POST request is sent. The same JSON sent through the API should return an appropriate 400 response. | Status Code: 400. The spaces-only description was rejected with the response: "Description is required (max 500 characters)". | PASS | ![Spaces screenshot](evidences/Task-2934_ScreenShots/space.png) |
