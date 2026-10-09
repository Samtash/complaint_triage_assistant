# Complaint_triage_assistant

An AI helper for a retail bank's complaint desk. A staff member pastes in a customer complaint, and the tool:

1. Hides personal data like card numbers, phone numbers and emails
2. Sorts the complaint by **category** and **urgency**
3. Forces High urgency when it spots fraud words
4. Suggests the right **team**
5. Drafts a reply using only the bank's own policy files *(in progress)*

A person checks and approves every result. The AI only suggests.

> **Status: work in progress.** I'm building this step by step, the way a business analyst would: requirements first, then the build, then testing against the requirements.

---

## Why I built this

Banks get complaints through many channels. Someone has to read each one, decide what it's about and how urgent it is, then send it to the right team. When volume is high, urgent cases like fraud can wait in the same queue as simple questions.

I wanted to see if AI could do the first sorting safely, with clear rules around it and a person always in control.

## Business analysis documents

I wrote these before writing any code:

| Document | What it covers |
|----------|----------------|
| [BRD](docs/BRD.md) | The business problem, goals, scope, stakeholders, 8 business requirements, success targets and risks |
| [FSD](docs/FSD.md) | 10 functional requirements, screens, API, prompt design, error handling and a BR to FR traceability table |
| [Use Cases](docs/Use_Cases.md) | 4 use cases with main flows and what happens when things go wrong |
| [Process Flow](docs/Process_Flow.md) | A diagram of one complaint's full path |
| [Build Notes](docs/Build_Notes.md) | What I checked, fixed and found while building |

## Key design decisions

* **A person decides every time.** Nothing moves until a staff member approves, edits or rejects the AI suggestion.
* **Team routing uses a fixed table, not the AI.** This keeps it predictable and easy to check.
* **Fraud is backed by a rule, not just the AI.** If fraud words show up, urgency is forced to High even if the AI says otherwise.
* **Personal data is hidden before anything goes to the AI.**
* **No matching policy means no reply draft.** The tool should never make up a bank policy. *(Step 5)*

## How I labeled urgency

| Urgency | Meaning |
|---------|---------|
| High | Fraud or theft, a lost or stolen card or phone, or the customer can't use their money and has an urgent deadline |
| Medium | Money taken by mistake (double charge, failed transfer, ATM error), or a real problem that needs fixing soon |
| Low | A question, a request or a small issue |

## Example

Request to `POST /triage`:

```json
{"complaint": "There is a payment of 15,000 taka at a shop in Chittagong on my card. I have never been to Chittagong."}
```

Response:

```json
{
  "category": "Fraud",
  "urgency": "High",
  "team": "Fraud and Risk",
  "reason": "An unauthorized transaction occurred on the card in a location the customer has never visited.",
  "fraud_rule_applied": false,
  "status": "Success"
}
```

Phone numbers are hidden too: "Call me back on 01711223344" becomes "Call me back on [phone]".

## Project structure

```
complaint_triage_assistant
├── app
│   ├── main.py          API endpoint (POST /triage)
│   ├── masking.py       Hides card numbers, phones and emails
│   ├── rules.py         Categories, fraud words and team table
│   └── classifier.py    Calls Gemini to sort the complaint
├── docs                 BRD, FSD, use cases, process flow, build notes
├── policies             8 sample bank policy files
├── test_data            50 sample complaints with my labels
└── requirements.txt
```

## Tech used

* Python and FastAPI
* Google Gemini (`gemini-3.5-flash-lite`) through the `google-genai` SDK
* GitHub Copilot as a coding assistant. I reviewed, tested and debugged everything it wrote. See [Build Notes](docs/Build_Notes.md).

## Run it yourself

1. Clone the repo and open the folder
2. Set up Python:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Get a free API key from Google AI Studio and make a file called `.env` in the main folder with this line:

```
GEMINI_API_KEY=your_key_here
```

4. Start the tool:

```
uvicorn app.main:app --reload
```

5. Open http://127.0.0.1:8000/docs, click **POST /triage**, then **Try it out**, and paste a complaint.

## Progress

| Step | What | Status |
|------|------|--------|
| 1 | BRD, FSD, use cases and process flow | ✅ Done |
| 2 | Sample bank policy files | ✅ Done |
| 3 | 50 labeled test complaints | ✅ Done |
| 4 | Basic triage: masking, sorting, fraud rule and team routing | ✅ Done |
| 5 | Policy lookup (RAG) and reply drafting | 🔄 Next |
| 6 | Screens: submit, review and log | ⏳ Planned |
| 7 | Test all 50 complaints and report accuracy | ⏳ Planned |
| 8 | Screenshots and demo video | ⏳ Planned |

## What I've found so far

* The fraud rule only matches exact words. "I have never been to Chittagong" and "the card that I reported lost" didn't trigger it. The AI got both right, but the safety net has gaps. I plan to widen the word list.
* The AI may rate urgency too high. It called a broken card High, and I labeled it Medium. Step 7 will show if this is a pattern.
* The first version of the code hid API errors behind a vague message. I traced the real cause and added clear error handling.

More detail in [Build Notes](docs/Build_Notes.md).

## Limits

* Sample data only. All complaints and policies were written for this project. No real customer or bank data.
* English only for now. Bangla support is a future idea.
* This is a portfolio project, not connected to any real bank system.

---

Built by **Samiha Tasnim Diba**, CSE, North South University
[GitHub](https://github.com/Samtash) · [LinkedIn](https://linkedin.com/in/samiha-tasnim-diba-29a426257)
