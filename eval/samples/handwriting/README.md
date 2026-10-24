# Handwriting samples: synthetic only

Add your six photos of handwriting on invented notices here, each with a UTF-8
ground-truth text file using the same base name, for example `hand_01.heic` and
`hand_01.txt` (or `hand_01.gt.txt`, but not both). Copy every visible word, date,
amount, and reference number exactly; do not correct or expand the handwriting
when transcribing it. Use invented details only, with no actual personal data.

`python -m eval.reader_bakeoff` discovers these pairs automatically. Missing,
duplicate, empty, or orphan ground truths stop the run instead of silently dropping
hard samples. Until images are present, the handwriting row is N/A with n=0;
it must never be described as supported or as 0% measured error.

Dates in numeric US/ISO form or English month-name dates, dollar-prefixed amounts,
and IDs labeled Reference, Case, ID, Citation, Ticket, or Account become key-token
targets. Read the detected target inventory in the report to confirm it covers
your intended dates, amounts, and numbers before using the recall result.

This file explains the local handwriting fixture convention and the limits of
automatic discovery. It does not contain handwriting examples or claim they have
already been tested.
