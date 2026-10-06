# Functional Specification Document
## Complaint Triage Assistant for Retail Banking

**Author:** Samiha Tasnim Diba
**Version:** 0.1 (draft)
**Date:** October 2026
**Based on:** BRD version 0.1

---

## 1. Purpose

This document explains how the Complaint Triage Assistant will work, screen by screen and step by step. It turns each business requirement (BR) in the BRD into functional requirements (FR) that a developer can build and a tester can check.

## 2. System Overview

| Part | What it does | Tool |
|------|--------------|------|
| Web screen | Where staff paste complaints and review results | HTML and JavaScript |
| Backend | Runs the steps and connects every part | Python, FastAPI |
| Rule layer | Masks numbers and forces High urgency for fraud words | Python |
| AI model | Sorts complaints and drafts replies | LLM API |
| Policy store | Holds the bank policy files and finds the right ones | Vector store (RAG) |
| Log | Saves every suggestion and every staff decision | SQLite |

## 3. Users

| User | What they can do |
|------|------------------|
| Complaint Officer | Submit complaints, review results, approve, edit or reject |
| Team Lead | Everything above, plus view the full log and summary numbers |

## 4. Functional Requirements

### FR1. Submit a complaint (BR1)
* The officer pastes the complaint text into a text box and clicks **Triage**.
* Text must be between 20 and 2,000 characters.
* If the box is empty or too short, show: "Please enter the full complaint."

### FR2. Protect personal data (BR8)
* Before anything is sent to the AI model, any run of 8 or more digits (card or account numbers) is replaced with `****`.
* Phone numbers and email addresses are also replaced with `[phone]` and `[email]`.

### FR3. Sort the complaint (BR1, BR2)
* The AI model gets the complaint and returns only this JSON:

```json
{
  "category": "Cards",
  "urgency": "High",
  "reason": "Customer says the card was used for a payment they did not make"
}
```

* Category must be one of: Cards, Accounts, Loans, Digital Banking, Fraud, Other.
* Urgency must be one of: High, Medium, Low.
* If the answer is not valid JSON or uses a value outside these lists, the system asks once more. If it fails again, the complaint is marked **Needs manual review**.

### FR4. Fraud safety rule (BR3)
* The system checks the complaint for fraud words: fraud, stolen, lost card, hacked, unauthorized, did not make this payment, money taken.
* If any are found, urgency is set to **High** no matter what the AI model said.
* The screen shows "Urgency raised by fraud rule" so staff know why.

### FR5. Suggest the team (BR4)
* The team comes from a fixed table, not from the AI model. This keeps routing predictable.

| Category | Team |
|----------|------|
| Cards | Card Services |
| Accounts | Account Services |
| Loans | Loan Department |
| Digital Banking | Digital Support |
| Fraud | Fraud and Risk |
| Other | Customer Service |

### FR6. Find the right policy (BR5)
* The bank has 6 to 8 short policy files, for example card blocking, refunds, loan repayment and app login problems.
* Each file is split into small sections and stored in the vector store.
* The system finds the 3 sections that best match the complaint.
* If none of them match well enough, no reply is drafted (see FR7).

### FR7. Draft a reply (BR5)
* The AI model gets the complaint and the 3 policy sections and writes a short, polite reply.
* It must use only the policy text it was given and must name the policy it used, for example "Policy CARD 02".
* If there is no good policy match, the screen shows: "No matching policy found. Please write the reply yourself."

### FR8. Review screen (BR6)
* Shows the complaint, category, urgency, suggested team, the reason, the reply draft and the policy text used.
* Every result is labeled **AI suggestion, needs approval**.
* The officer can **Approve**, **Edit** any field or **Reject** and sort it by hand.
* Nothing is forwarded until the officer picks one of these.

### FR9. Log every decision (BR7)
* For each complaint the log saves: complaint ID, time, the AI suggestion, the final decision, what the officer changed and who did it.

### FR10. Team lead view (BR7)
* A table of all logged complaints with filters for category, urgency and date.
* Summary numbers: complaints this week, number of High urgency cases and how often staff changed the AI suggestion.

## 5. Screens

| Screen | Main parts |
|--------|------------|
| 1. Submit | Text box, Triage button, error message area |
| 2. Review | Complaint, results, reply draft, policy used, Approve, Edit and Reject buttons |
| 3. Log | Table, filters, summary numbers (Team Lead only) |

## 6. API Endpoints

| Method | Path | Input | Output |
|--------|------|-------|--------|
| POST | `/triage` | complaint text | complaint ID, category, urgency, team, reason, reply draft, policy used |
| POST | `/decision` | complaint ID, action, final values | saved confirmation |
| GET | `/log` | filters (optional) | list of logged complaints and summary numbers |

## 7. Prompt Design

**Sorting prompt**
* Tells the model it is helping a bank complaint desk.
* Gives the fixed category and urgency lists.
* Includes 3 short examples of complaints with the correct answer.
* Asks for JSON only, with no extra text.
* Uses temperature 0 so the same complaint gets the same answer.

**Reply prompt**
* Gives the complaint and the 3 policy sections.
* Says to use only that policy text and to say clearly if the policy does not cover the case.
* Asks for a short, polite reply in plain English that names the policy used.

## 8. Error Handling

| Problem | What the system does |
|---------|----------------------|
| AI service is down | Shows an error, saves the complaint and lets the officer sort it by hand |
| AI answer is not valid | Asks once more, then marks **Needs manual review** |
| No policy match | Skips the reply draft and tells the officer |
| Complaint too long | Asks the officer to shorten it |

## 9. Non Functional Requirements

* One complaint is processed in under 10 seconds.
* The API key is kept in an environment file and never stored in the code.
* Only sample data is used.

## 10. Traceability (BR to FR)

| Business Requirement | Covered by |
|----------------------|------------|
| BR1 Category | FR1, FR3 |
| BR2 Urgency | FR3 |
| BR3 Fraud always High | FR4 |
| BR4 Suggest team | FR5 |
| BR5 Policy based reply | FR6, FR7 |
| BR6 Human approval | FR8 |
| BR7 Log | FR9, FR10 |
| BR8 No real personal data | FR2 |
