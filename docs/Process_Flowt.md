# Process Flow
## Complaint Triage Assistant for Retail Banking

**Author:** Samiha Tasnim Diba
**Version:** 0.1 (draft)

This shows the full path of one complaint, from the moment it arrives to the moment it reaches the right team. GitHub shows this as a diagram automatically.

```mermaid
flowchart TD
    A[Complaint arrives] --> B[Officer pastes complaint and clicks Triage]
    B --> C{Text valid?}
    C -- No --> C1[Show error and ask to fix] --> B
    C -- Yes --> D[Hide card numbers, account numbers, phone and email]
    D --> E[AI sorts category and urgency]
    E --> F{Valid answer?}
    F -- No, after one retry --> M[Mark Needs manual review]
    F -- Yes --> G{Fraud words found?}
    G -- Yes --> H[Force urgency to High]
    G -- No --> I[Keep AI urgency]
    H --> J[Pick team from routing table]
    I --> J
    J --> K[Find 3 best matching policy sections]
    K --> L{Good policy match?}
    L -- No --> N[No draft, officer writes reply]
    L -- Yes --> O[AI drafts reply using only that policy]
    O --> P[Review screen]
    N --> P
    M --> P
    P --> Q{Officer decision}
    Q -- Approve --> S[Save to log]
    Q -- Edit --> R[Officer changes fields] --> S
    Q -- Reject --> T[Officer sorts it by hand] --> S
    S --> U{Urgency High?}
    U -- Yes --> V[Send to team and alert team lead now]
    U -- No --> W[Add to team queue]
```

## Key Points

* **A person decides every time.** The AI only suggests. Nothing moves until the officer approves, edits or rejects.
* **Fraud is handled by a fixed rule, not only by the AI.** Even if the AI gets it wrong, fraud words always raise urgency to High.
* **Team routing uses a table, not the AI.** This makes it predictable and easy to check.
* **No good policy, no draft.** The system would rather say nothing than make up a policy.
