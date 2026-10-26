# Notice Decoder — submission draft

Live app: https://notice-decoder-ns5o.onrender.com

Release branch: https://github.com/anushka-j10/congressionalApp/tree/fix/notice-reliability

These answers are ready to adapt to the form's actual word limits. AJ must review the first-person statements and complete the personal TODO block in [AI_USAGE.md](AI_USAGE.md). This document is a draft, not a submitted entry or a claim of eligibility.

## App description

Notice Decoder helps people understand a photographed notice. Users upload one printed English page, review the reading against the photo, and choose whether it is a parking ticket, court notice, utility bill or school letter. The app identifies the issuing office, deadline, amount, requested action and contact information, shows source text, and offers a plain-English explanation. It also offers checked Spanish or Tagalog translations, English fallback when checks fail, and read-aloud when the device has a suitable voice. Selected parking authorities in nine Northeast states have links to official resources. The app does not pay tickets, submit appeals, determine legal rights or guarantee that a result is correct.

## The problem and who it helps

After a health emergency, my parents asked me to read a parking ticket and work out what they needed to do. Even as a native English speaker, I found it difficult. Growing up in Jersey City, I have seen how confusing notices can create an extra burden in a diverse community, especially when someone is already dealing with stress or a language barrier. I created Notice Decoder to make the next step easier to understand and to keep the original wording within reach. My intended users include families in Jersey City and NJ-08 who need help reading an unfamiliar notice on their phones. This is my motivation and intended audience; I have not established community-wide impact through a user study.

## Technical challenges and how I addressed them

One challenge was preventing a fluent explanation from hiding a reading error. The pipeline separates image reading, user review, fact extraction, deterministic checks and explanation. Model-proposed facts must carry source snippets. Checks test source matches, numeric consistency and supported date/amount/action rules. Results that fail are withheld or marked for review. The interface calls a passed result a “Text match,” because matching reviewed text is not proof that the original fact was read or interpreted correctly.

Another challenge was missing information. The app can leave a field unidentified instead of making up a deadline. Unknown document types require manual selection. The explanation layer checks numbers against extracted facts; translation checks protect key values and can return English when a translated result fails. Device voice availability and unreviewed Spanish/Tagalog wording remain limits.

I directed an evaluation that compared the full pipeline with plain translation (B1), extraction without validators (B2), and individual validator ablations. The later development run had 0/120 critical false-verified field opportunities for the full pipeline versus 2/120 for each baseline, but the full pipeline abstained on 20/92 present critical fields. The once-run original held-out test, on an earlier version and scorer, had 4/30 critical false-verified fields and 6/24 present-field abstentions. A later exploratory Northeast stress test found 21/144 strict false-verified field opportunities and only 10/36 complete case passes. These different sets and scorer versions are not a controlled before/after comparison. They exposed wrong years, relative-date errors and incomplete instructions that still need work. Full results and failures are retained in the repository rather than hidden by the demo.

## AI disclosure

Codex wrote much of the code under my direction, including proposed validators and an evaluation scorer that I authorized for review. I contributed the idea and family context, product and design decisions, evaluation plan and requirements, test-notice design direction, the independent handwritten held-out answer key, and review of outputs. Codex also generated the development notices, Northeast stress replicas, tests and documentation drafts. The classifier signal file was reserved for my own work, but its shipped lists are empty, so the release uses manual type selection. The app uses Tesseract for its default reading step and an OpenAI model for extraction and language processing. My detailed personal contribution record is in AI_USAGE.md and must be completed by me before submission.

## Evidence and final review

- [Measured results and definitions](README.md#measured-results), [complete failures](FAILURES.md), [original held-out report](HELDOUT_RESULTS.md).
- [Release checks](RELEASE_CHECKLIST.md), [deployed evidence](results/release-2026-10-26/REPORT.md), [demo script](DEMO_SCRIPT.md).
- [2.0 work brief](NOTICE_DECODER_2_0_PROMPT.md) separates remaining reliability work from shipped functionality.
- AJ: verify the current form's requirements, word limits and deadline, attach the actual demo video, review the personal disclosure, and submit the entry yourself. No submission has been made by this assistant.
