# Use Cases
## Complaint Triage Assistant for Retail Banking

**Author:** Samiha Tasnim Diba
**Version:** 0.1 (draft)
**Based on:** BRD and FSD version 0.1

---

## UC1. Submit and Triage a Complaint

| Field | Details |
|-------|---------|
| Actor | Complaint Officer |
| Goal | Get a quick suggestion for category, urgency, team and reply |
| Before | The officer is logged in and has a complaint to process |
| Related | BR1, BR2, BR4, BR5, BR8 |

**Main flow**
1. The officer pastes the complaint and clicks **Triage**.
2. The system checks the text length.
3. The system hides card numbers, account numbers, phone numbers and emails.
4. The system sorts the complaint by category and urgency.
5. The system picks the team from the routing table.
6. The system finds the matching policy sections and drafts a reply.
7. The system opens the Review screen.

**Other flows**
* 2a. Text is empty or too short: the system shows an error and waits for the officer to fix it.
* 4a. The AI answer is not valid twice in a row: the system marks the complaint **Needs manual review** and opens the Review screen without results.
* 6a. No policy matches well: the system skips the reply and tells the officer to write one.
* Any step: the AI service is down. The system saves the complaint and lets the officer sort it by hand.

**After**
The complaint has a suggestion waiting for review.

---

## UC2. Review and Approve a Suggestion

| Field | Details |
|-------|---------|
| Actor | Complaint Officer |
| Goal | Check the AI suggestion and make the final decision |
| Before | UC1 is done and the Review screen is open |
| Related | BR6, BR7 |

**Main flow**
1. The officer reads the complaint, the suggested category, urgency and team, the reason and the reply draft.
2. The officer reads the policy text the reply is based on.
3. The officer clicks **Approve**.
4. The system saves the decision in the log and sends the complaint to the team's queue.

**Other flows**
* 3a. Something is wrong: the officer clicks **Edit**, changes any field, then approves. The system logs what changed.
* 3b. The whole suggestion is wrong: the officer clicks **Reject** and sorts the complaint by hand. The system logs it as rejected.

**After**
The complaint has a final decision made by a person and is in the right team's queue.

---

## UC3. Escalate a Fraud Complaint

| Field | Details |
|-------|---------|
| Actor | System, then Complaint Officer |
| Goal | Make sure fraud cases are never treated as low priority |
| Before | A complaint mentions fraud, a stolen card or money taken without permission |
| Related | BR3, BR6 |

**Main flow**
1. During UC1 the fraud rule finds a fraud word in the complaint.
2. The system sets urgency to **High**, even if the AI model said something lower.
3. The Review screen shows "Urgency raised by fraud rule."
4. The officer reviews and approves.
5. The system sends the complaint to Fraud and Risk and alerts the team lead right away.

**Other flows**
* 4a. The officer sees it is not really fraud, for example "I want to report that I found my lost card." The officer lowers the urgency and the log records why.

**After**
Every possible fraud case is reviewed first, and any change to its urgency is on record.

---

## UC4. Review the Complaint Log

| Field | Details |
|-------|---------|
| Actor | Team Lead |
| Goal | See what came in, how it was handled and how well the AI is doing |
| Before | The team lead is logged in |
| Related | BR7 |

**Main flow**
1. The team lead opens the Log screen.
2. The system shows all complaints with their final category, urgency, team and decision.
3. The team lead filters by date, category or urgency.
4. The system shows summary numbers: total complaints, High urgency cases and how often staff changed the AI suggestion.

**Other flows**
* 2a. No complaints in the chosen dates: the system shows "No complaints found."

**After**
The team lead knows the current workload and whether the AI suggestions need improving.
