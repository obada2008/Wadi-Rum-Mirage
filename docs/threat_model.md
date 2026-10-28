# Threat model

- Untrusted input: user-submitted text, URLs, and any prompts contained in them.
- Defensive measures: no URL fetching; no shell execution; text rendered via `textContent` instead of HTML; body max 5,000 characters; no database persistence; no third-party inference calls.
- The UI is served from a local FastAPI process and should not be publicly exposed without HTTPS, rate limits, request size limits, abuse protections, and privacy review.
- Heuristic detection may miss attackers using paraphrases, spaced characters, multi-turn conversations, or subtle implications.
- No claim of verified identity, actual phishing conviction, or calibrated risk probability.
- Exported reports contain user-submitted URL data and should not be posted publicly without review.
