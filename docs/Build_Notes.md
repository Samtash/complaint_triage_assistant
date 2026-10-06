# Build Notes

## Step 4: Basic triage (FR1 to FR5)

* Built with GitHub Copilot (Agent mode) from my FSD. Its own tests used fake AI answers only, so I ran the first live tests myself.
* The code used gemini-2.5-flash, which my key could not use. I listed the models my key can access and switched.
* My first API key failed with 401. I tested the key outside the app to prove the key was the problem, made a new key and it worked.
* The app then failed with a vague "classification failed" error. I called the function directly and found the real cause: Google returned 503 (high demand). I switched to gemini-3.5-flash-lite.
* The code hid API errors and only retried on bad formatting. I added logging and made API failures fall back to manual review, as the FSD requires.
* Phone masking works: the number became [phone].
* Finding: the fraud rule only matches exact words. "I have never been to Chittagong" and "the card that I reported lost" did not trigger it. The AI was right both times, but the safety net has gaps.
* Finding: the AI rated a broken card as High. I labeled it Medium.
* PowerShell saved requirements.txt as UTF-16. I changed it to UTF-8.
