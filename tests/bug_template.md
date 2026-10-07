# Bug template

| Title | Steps to reproduce | Expected | Actual | Severity (high, medium, low) |  Evidence |  Owner
| exceed subject character limit | 1. Open ticket form -> 2. Enter a subject longer than 100 characters -> 3. Enter a valid description -> 4. Submit ticket | 422 -> {"error":"Subject must not exceed 500 characters"} | --- |  medium |  --- |  Yousef Razzouk | 