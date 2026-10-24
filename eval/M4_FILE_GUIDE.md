# M4 new-file explanations

- **`eval/generate_m4.py`**: Renders invented notices and deterministic clean/degraded variants with Pillow. It preserves the earlier corpus and never opens held-out files.

- **`eval/m4-config.json`**: Pins the model snapshot, generation settings, today, variants and three repetitions. It also records the explicit type-selection, unchanged OCR and first-page-only evaluation protocol.

- **`eval/protocol.py`**: Loads only declared synthetic inputs and records provenance. Its held-out gate requires a matching freeze tag/code hash and consumes a one-use ledger before reading test inputs.

- **`eval/engine.py`**: Runs the actual backend pipeline and captures invented outputs for inspection. Its B2 validation/abstention bypass is offline-only and cannot be enabled through the public API.

- **`eval/scoring.py`**: Contains Codex-generated proposed scoring logic for student review. It separates wrong Verified facts, safe flags, coverage, missing truth, service failures and repeated-run variance.

- **`eval/run.py`**: Provides one-command evaluation with incremental JSON and Markdown reports. It refuses silent overwrite or held-out retries and never logs credentials or raw provider errors.

- **`eval/heldout/README.md`**: Explains how the student supplies ten untouched synthetic tests. It forbids test inspection/tuning before the chosen fix loop ends and code is frozen.

- **`eval/heldout/expected-fields.template.json`**: Defines the expected annotation format without supplying any test sample. Its null values are placeholders, not measured missing-field results.

- **`tests/test_m4_eval.py`**: Checks the proposed scorer and evaluation protocol against concrete safety/counting cases. Its temporary held-out-gate tests do not open the actual test directory.

- **`tests/test_m4_robustness.py`**: Exercises hostile-input boundaries, unsupported values, retry and API privacy with deterministic doubles. It openly retains an expected-failure regression for the reproduced source-context gap pending student choice.

- **`.github/workflows/checks.yml`**: Defines Python, Node and synthetic dry-run checks for GitHub CI. It uses no API credentials, paid requests or held-out inputs and has not yet run remotely.

- **`eval/M4_FILE_GUIDE.md`**: Explains the purpose of each new evaluation artifact. Repeated image/annotation descriptions reflect their shared generated format, not independent real-world evidence.

- **`FAILURES.md`**: Records observed development/adversarial failures and ranked fix options. No fix or before/after improvement is claimed before the student chooses.

- **`docs/EVIDENCE.md`**: Collects measured tables, protocol, limitations and disclosed authorship for the student. It does not write the contest narrative or invent held-out/fix results.

- **`eval/m4/dev/court_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/court_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/court_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/court_02.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/court_02__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/court_02__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/court_03.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/court_03__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/court_03__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/court_04.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/court_04__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/court_04__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/court_05.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/court_05__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/court_05__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/manifest.json`**: Lists the declared synthetic samples in this development set. Only these entries are evaluated; held-out inputs are never discovered here.

- **`eval/m4/dev/parking_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/parking_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/parking_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/parking_02.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/parking_02__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/parking_02__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/parking_03.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/parking_03__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/parking_03__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/parking_04.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/parking_04__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/parking_04__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/parking_05.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/parking_05__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/parking_05__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/school_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/school_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/school_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/school_02.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/school_02__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/school_02__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/school_03.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/school_03__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/school_03__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/school_04.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/school_04__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/school_04__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/unknown_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/unknown_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/unknown_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/utility_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/utility_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/utility_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/utility_02.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/utility_02__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/utility_02__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/utility_03.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/utility_03__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/utility_03__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/utility_04.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/utility_04__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/utility_04__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/dev/utility_04__page2.png`**: Contains the second page of the synthetic multi-page coverage case. The current one-photo app does not merge it, so the evaluation explicitly records that limitation.

- **`eval/m4/dev/utility_05.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/dev/utility_05__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/dev/utility_05__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_01.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_01__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_01__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_02.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_02__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_02__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_03.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_03__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_03__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_04.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_04__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_04__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_05.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_05__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_05__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_06.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_06__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_06__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_07.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_07__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_07__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/attack_08.json`**: Stores invented source text, field truth, ambiguity/absence labels and image variants for this notice. This annotation is evaluation data and is never sent to the model as the answer.

- **`eval/m4/adversarial/attack_08__clean.png`**: Contains the clean Pillow rendering of this invented notice. It has no real person or agency logo and is paired with a degraded image.

- **`eval/m4/adversarial/attack_08__degraded.jpg`**: Contains the seeded rotated, skewed, blurred, shadowed and compressed copy of its paired synthetic notice. It approximates image damage and is not a real phone photograph.

- **`eval/m4/adversarial/manifest.json`**: Lists the declared synthetic samples in this development set. Only these entries are evaluated; held-out inputs are never discovered here.


- **`eval/rescore.py`**: Rebuilds development tables from saved outputs without API calls. It rejects heldout data, preserves original summaries, and verifies that model payloads did not change.

- **`results/m4-dev-before.json`**: Preserves the original synthetic inference outputs and initial scoring, including the later identified counting issues. It is retained for audit and is not the current headline table.

- **`results/m4-dev-before.md`**: Preserves the original synthetic inference outputs and initial scoring, including the later identified counting issues. It is retained for audit and is not the current headline table.

- **`results/m4-dev-review.json`**: Contains the corrected proposed scoring of unchanged synthetic model outputs. It records reproducible current counts with explicit measurement limitations and inference/scoring provenance.

- **`results/m4-dev-review.md`**: Contains the corrected proposed scoring of unchanged synthetic model outputs. It records reproducible current counts with explicit measurement limitations and inference/scoring provenance.

- **`results/m4-adversarial-before.json`**: Preserves the original synthetic inference outputs and initial scoring, including the later identified counting issues. It is retained for audit and is not the current headline table.

- **`results/m4-adversarial-before.md`**: Preserves the original synthetic inference outputs and initial scoring, including the later identified counting issues. It is retained for audit and is not the current headline table.

- **`results/m4-adversarial-review.json`**: Contains the corrected proposed scoring of unchanged synthetic model outputs. It records reproducible current counts with explicit measurement limitations and inference/scoring provenance.

- **`results/m4-adversarial-review.md`**: Contains the corrected proposed scoring of unchanged synthetic model outputs. It records reproducible current counts with explicit measurement limitations and inference/scoring provenance.

- **`results/m4-round1-dev.json`**: Records the complete repeated evaluation after selected fix 1. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round1-dev.md`**: Records the complete repeated evaluation after selected fix 1. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round1-adversarial.json`**: Records the complete repeated evaluation after selected fix 1. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round1-adversarial.md`**: Records the complete repeated evaluation after selected fix 1. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round2-dev.json`**: Records the complete repeated evaluation after selected fix 2. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round2-dev.md`**: Records the complete repeated evaluation after selected fix 2. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round2-adversarial.json`**: Records the complete repeated evaluation after selected fix 2. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`results/m4-round2-adversarial.md`**: Records the complete repeated evaluation after selected fix 2. It retains actual outputs/counts and pinned settings rather than replacing earlier evidence.

- **`eval/freeze.json`**: Records the selected source fingerprint and freeze date without secrets or heldout content. The one-use heldout gate checks this fingerprint and the eval-freeze tag before reading any test sample.

- **`results/m4-round1-live-dev.json`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round1-live-dev.md`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round1-live-adversarial.json`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round1-live-adversarial.md`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round2-live-dev.json`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round2-live-dev.md`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round2-live-adversarial.json`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.

- **`results/m4-round2-live-adversarial.md`**: Contains the successful full live evaluation after this selected fix. Provider coverage is checked before using these counts; earlier unavailable attempts remain separate.
