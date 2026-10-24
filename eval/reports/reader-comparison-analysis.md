# A2 comparison status and recommendation

Local measurement is complete. The vision preflight returned HTTP 429 (rate/quota limit), so the four-way live comparison is incomplete and hybrid accuracy is unmeasured. No production reader was selected and no extraction work was started.

## Measured reader × condition

| Reader | Condition | Pages | CER | Primary-text key recall | Shown-candidate recall |
| --- | --- | ---: | ---: | ---: | ---: |
| tesseract | clean | 8 | 0.00% | 100.00% | N/A |
| tesseract | degraded | 56 | 29.09% | 64.29% | N/A |
| tesseract | handwriting | 0 | N/A | N/A | N/A |
| tesseract | legacy_m1 | 8 | 0.05% | 100.00% | N/A |
| preprocessed | clean | 8 | 0.00% | 100.00% | N/A |
| preprocessed | degraded | 56 | 0.59% | 100.00% | N/A |
| preprocessed | handwriting | 0 | N/A | N/A | N/A |
| preprocessed | legacy_m1 | 8 | 0.27% | 100.00% | N/A |
| vision | clean | 0 | Not run | Not run | Not run |
| vision | degraded | 0 | Not run | Not run | Not run |
| vision | handwriting | 0 | Not run | Not run | Not run |
| hybrid | clean | 0 | Not run | Not run | Not run |
| hybrid | degraded | 0 | Not run | Not run | Not run |
| hybrid | handwriting | 0 | Not run | Not run | Not run |

Clean plus degraded printed recall: original Tesseract **154/224 (68.75%)**; OpenCV plus Tesseract **224/224 (100%)**. The preprocessed option meets the numerical 95% threshold on this frozen synthetic corpus. Formal reader selection and the extraction gate remain pending the student decision and remaining text-confirmation work.

All seven degraded variants now retain 28/28 key targets each: rotation, perspective, blur, shadow, noise, compression, and the combined phone mix. Degraded CER remains 0.59%, so perfect critical-token recall must not be described as perfect OCR or proof that required-action wording is always correct.

## Recommendation for review

Among the measured options, use the preprocessed local reader as the provisional printed-notice candidate: it improves critical-token recall without sending images to an external provider or adding a per-call model charge. Do not claim it is better than vision or hybrid, because their live comparison is blocked. Do not claim handwriting support: no handwriting photo/truth pairs have been provided.

The proposed hybrid remains available for comparison after quota is resolved. It reports agreement only on identical normalized strings, preserves every actual alternative, and treats reader failures as disputed rather than inventing agreement. Its separate candidate metric gives credit only to alternatives returned for display, with one-to-one target matching.

## Verification

111 tests pass, including the original API privacy tests and a real preprocessed-request no-files-left check; there is one pre-existing Python 3.9 asyncio deprecation warning. JavaScript syntax checks and Python dependency consistency checks pass. The A1 corpus manifest hash and original M1 PNG/JSON fingerprints remain unchanged.

The mobile renderer was verified at 390px with clearly labeled synthetic test doubles: $45.01 and $45.00 are both visible as disputed candidates, the primary amount is highlighted, and script-looking notice text remains inert. The screenshot is a renderer test, not a live provider result or a physical-phone test.

## First review and pending work

Review DESIGN_NOTES.md and the local metrics JSON, then test a real printed page on the phone after selecting the reader. Resolve API quota before retrying vision/hybrid, and add the six invented handwriting photo/truth pairs for a handwriting measurement. The editable A3 confirmation screen, confidence/handwriting-region work, field extraction, validators, translation, and deployment are not part of this checkpoint.

Dedicated OCR services are listed with sourced costs/privacy and estimated setup times in handwriting-cloud-options.md; none was set up. Current defaults remain unchanged; TEXT_READER=preprocessed or hybrid must be explicitly selected after review.
