# Business Requirements Document
## Complaint Triage Assistant for Retail Banking

**Author:** Samiha Tasnim Diba
**Version:** 0.1 (draft)
**Date:** October 2026

---

## 1. Background

Retail banks get customer complaints through many channels: email, the mobile app, the call center and branch forms. A staff member usually reads each one, decides what it is about and how urgent it is, then forwards it to the right team.

When volume is high this gets slow. Urgent cases like fraud or a stolen card can sit in the same queue as a simple balance question. Staff also spend time writing replies that mostly repeat bank policy.

This project tests whether an AI assistant can do the first sorting and draft a reply, while a person stays in control of every final decision.

## 2. Business Objectives

| ID | Objective |
|----|-----------|
| BO1 | Cut the time it takes to sort a new complaint |
| BO2 | Make sure urgent complaints reach the right team first |
| BO3 | Give staff a policy based reply draft so they write less from scratch |
| BO4 | Keep a human in charge of every decision the system suggests |

## 3. Scope

**In scope (version 1)**
* Text complaints in English
* Sorting each complaint by category and urgency
* Suggesting which team should handle it
* Drafting a reply based on the bank's own policy documents
* A simple review screen where staff approve or edit the result

**Out of scope (version 1)**
* Voice calls and scanned letters
* Sending replies to customers automatically
* Connecting to real bank systems
* Real customer data (only sample complaints are used)
* Bangla language support (planned for a later version)

## 4. Stakeholders

| Stakeholder | What they need |
|-------------|----------------|
| Customers | Fast and correct answers, urgent problems handled first |
| Complaint desk staff | Less manual sorting, good reply drafts they can trust |
| Team leads | A clear view of what came in and how it was handled |
| Compliance team | Replies that follow policy and a record of every decision |
| IT team | A tool that is simple to run and safe with data |

## 5. Business Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| BR1 | The system must sort each complaint into one category: Cards, Accounts, Loans, Digital Banking, Fraud or Other | Must |
| BR2 | The system must give each complaint an urgency level: High, Medium or Low | Must |
| BR3 | Any complaint that mentions fraud, a lost card or money taken without permission must always be marked High | Must |
| BR4 | The system must suggest which team should handle the complaint | Must |
| BR5 | The system must draft a reply using only the bank's policy documents and show which policy it used | Must |
| BR6 | A staff member must approve or edit every result before it is used | Must |
| BR7 | The system must keep a log of each complaint, the suggestion and the final staff decision | Should |
| BR8 | The system must not store real personal data | Must |

## 6. Success Measures

| Measure | Target |
|---------|--------|
| Category accuracy on a test set of 50 labeled sample complaints | 85% or higher |
| Fraud and lost card complaints marked High | 100% |
| Time to process one complaint | Under 10 seconds |
| Reply drafts that point to the correct policy | 90% or higher |

## 7. Assumptions

* Sample complaints are written to match common real complaint types. No real customer data is used.
* Bank policy documents are short sample policies written for this project.
* Staff will review every result, so the system is a helper and not a decision maker.

## 8. Risks and How They Are Handled

| Risk | Handling |
|------|----------|
| The AI marks an urgent complaint as low urgency | A fixed rule forces High for fraud related words (BR3), and staff review every result (BR6) |
| The reply draft states the wrong policy | The draft shows the policy text it used so staff can check it (BR5) |
| Privacy problems with customer data | Only sample data is used in version 1 (BR8) |
| Staff trust the AI too much | The screen clearly marks every result as a suggestion that needs approval |

## 9. Related Documents

* Functional Specification Document (FSD)
* Use Cases
* Process Flow Diagram
* Test Results
