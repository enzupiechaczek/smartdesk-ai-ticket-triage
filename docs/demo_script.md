## Demo For SmartDesk built by EARTech Information Technology interns

<!--
todo : three-minute script with timed sections
named speakers and what each says
-->
## Test data : "test_tickets.json"
for SmartDesk ticket triage POST inputs and expected classifications.subject / description demonstrate payload; expected_priority / expected_category are synthetic labels for test validation, not observed model predictions.

----
named speakers: 
#### speaker: *** Hassan Ali ***
* Hassan Ali
* Majd
* Mohammad Ghassan
* Mahmood

## start the server

speaker: Hassan Ali

follow the step in [README](../README.md) to launch the server , step 2 for Linux/MacOS and step 3 for Windows 

## open the page

speaker: Hassan Ali

open **http://127.0.0.1:5000**

## submit an urgent ticket
speaker: Majd

```json
{
    "subject": "Cannot access account",
    "description": "I cannot access my account today",
    "expected_priority": "urgent",
    "expected_category": "access"
},
```

## submit a normal ticket
speaker: Majd

```json
{
    "subject": "Cannot sign in to portal",
    "description": "I cannot sign in to the portal, even though my password appears to be correct.",
    "expected_priority": "normal",
    "expected_category": "access"
},
```

## point out category, confidence and priority
speaker: Mohammad Ghassan

## show urgent first
speaker: Mohammad Ghassan

> Note: Tickets are sorted primarily by urgency (urgent first), followed by creation date (newest first)

## stop and restart the server
speaker: Mahmood

## refresh and show the data is still there.
speaker: Mahmood

## coordination with Group A2 , B
<!-- End with relative links AI demo and QA demo. -->
[ai demo](./demo_ai.md) , [qa demo](./demo_qa.md)
> the linked scripts are pending until those PRs merge