# SmartDesk test cases

Placeholder. Group B writes the test plan in task B-1.1.

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |

| TC-ValidAccess-001 | 
{"subject" : "Unable to access my account","description" : "I cannot log into my account"} 
| 1. Enter the subject.<br>2. Enter the description.<br>3. Submit the ticket. | 201 -> {"id","same subject","same description","access","confidence","priority","created_at"} |--- |--- |--- |

| TC-ValidBilling-002 | {"subject":"Billing inquiry regarding invoice #12345","description":"I would like to request an itemized breakdown for my latest invoice."} | 1. Open billing form -> 2. Enter valid subject -> 3. Enter valid description -> 4. Submit ticket | 201 -> {"id","same subject","same description","billing","confidence","priority","created_at"} |--- |--- |---|

| TC-ValidTechnical-003 |{"subject": "Database connection timeout", "description": "i can't access the database and it says "connection timeout""}|1. Navigate to support portal ->  2. Enter subject and description -> 3. Click Submit|201 -> {"id","same subject","same description","technical","confidence","priority","created_at"}|---|---|---|

| TC-BlankSubject-004 |{"subject": "", "description": "Need help with my account settings"}| 1. Navigate to support portal 2. Leave Subject blank 3. Click Submit  | 422 -> {"error" : "subject cannot be empty"}|---|---|---|

| TC-BlankDesctiption-005 |{"subject": "Need help with my account settings", "description": ""}| 1. Navigate to support portal 2. Leave description blank 3. Click Submit  | 422 -> {"error" : "description cannot be empty"}|---|---|---|

| TC-101CharacterSubject-006 | {"subject":"101-character subject entered by user","description":"i need tech support cuz i can't use this platform easily"} | 1. Open ticket form -> 2. Enter a subject longer than 100 characters -> 3. Enter a valid description -> 4. Submit ticket | 422 -> {"error":"Subject must not exceed 100 characters"} |--- |--- |--- |

| TC-501CharacterDescription-007 | {"subject":"Technical support request","description":"501-character description entered by user"} | 1. Open ticket form -> 2. Enter valid subject -> 3. Enter a description longer than 500 characters -> 4. Submit ticket | 422 -> {"error":"Description must not exceed 500 characters"} |--- |--- |--- |

TC-DuplicateTicket-008 | { "subject": "Unable to access my account", "description": "I cannot log into my account using my correct credentials." } | { "1. Submit the ticket with the specified subject and description.", "2. Submit the same ticket again with the identical subject and description.", "3. Check the response for the second submission." } | 201 -> {"id","same subject","same description","category","confidence","priority","created_at"} |--- |--- |--- |

|TC-HTMLLikeText-009|{"subject": "<b>Login Problem</b>", "description": "I cannot login to my account. <b>Please help.</b>"}|1. Navigate to support portal → 2. Enter HTML-like text in Subject and Description → 3. Click Submit → 4. Check the response/UI| 200 -> {"id","same subject as plain text not html","same description as plain text not html","category","confidence","priority","created_at"}|--- |--- |--- | 

|TC-AmbiguousTicket-010|{"subject": "Contact the company", "description": "i wanna have the phone number of the Company"}|1. Navigate to support portal → 2. Enter some text that couldn't be classified as one of the three categories → 3. Click Submit → 4. Check the response/UI| 201 -> {"id","same subject as plain text not html","same description as plain text not html","access","0.2","priority","created_at"}|--- |--- | --- |

