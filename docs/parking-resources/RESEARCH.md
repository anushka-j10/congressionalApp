# Northeast parking-ticket resources — 2026-10-26

This is a researched, bundled directory, not a live web-search agent. It supplies general navigation instructions separately from OCR, extraction, verified fields, and model-generated explanations. It does not determine that payment is due, decide a plea, calculate a new deadline, or submit a payment.

## Coverage

Nine Northeast states: Connecticut, Maine, Massachusetts, New Hampshire, New Jersey, New York, Pennsylvania, Rhode Island, Vermont. There are **12 explicitly scoped routes**, not comprehensive municipal coverage and not 50-state coverage. Users choose the **issuing state**, which can differ from their home state, and then the issuer. No issuer is preselected, inferred from OCR, or guessed from a state. State and issuer are held in page memory only.

| State | Covered issuer / scope | Official source and route |
| --- | --- | --- |
| NJ | New Jersey municipal-court parking tickets | [Jersey City Municipal Court](https://www.jerseycitynj.gov/CityHall/law/municipalcourt) links to NJMCdirect. The app links directly to that court-hosted portal; eligibility and court-appearance requirements must be checked. |
| NJ | Jersey City Municipal Court | [Court page](https://www.jerseycitynj.gov/CityHall/law/municipalcourt): payment, hearing requests, contact details. |
| NY | New York City Department of Finance only | [Parking-ticket services](https://www.nyc.gov/site/finance/vehicles/services.page): CityPay and dispute routes. This is not a statewide NY payment route. |
| PA | Philadelphia Parking Violations Branch only | [Pay a parking ticket](https://www.phila.gov/services/cars-parking-transportation/pay-or-dispute-a-ticket/pay-a-parking-ticket/): online payment link and other methods; dispute navigation. |
| CT | Hartford Parking Authority only | [City payment instructions](https://www.hartfordct.gov/Residents/Transportation/Car-HPA/Pay-A-Parking-Ticket) direct users to Hartford Parking Authority. |
| CT | New Haven city parking citations only | [Accounts Receivable](https://www.newhavenct.gov/government/departments-divisions/finance/divisions/accounts-receivable) contains “City of New Haven parking citations – Pay or Appeal Here.” Other payment entries on that page must not be used for parking. |
| MA | Boston Parking Clerk only | [Payment instructions](https://www.boston.gov/departments/parking-clerk/how-pay-parking-ticket): online ticket/notice lookup and other methods. [Massachusetts RMV](https://www.mass.gov/how-to/pay-your-traffic-ticket) explicitly directs parking payments to the issuing city/town, rather than the RMV traffic-citation service. |
| ME | Participating municipalities only | [Lewiston Police official page](https://www.lewistonmaine.gov/141/Welcome) links to the [Maine partner portal](https://me.accessgov.com/maine-municipal/Forms/Page/parking/memuniparkingtickets/1). The portal requires selecting the exact participating municipality. This is not all Maine tickets. |
| NH | Nashua only | [Parking Tickets & Violations](https://www.nashuanh.gov/978/Parking-Tickets-Violations): online payment and appeal FAQ links. |
| NH | Hanover only | [Payments and Appeals](https://www.hanovernh.org/785/Payments-and-Appeals): separate payment and appeal instructions, parking portal. This official municipal site uses .org. |
| RI | Providence Municipal Court only | [Parking Ticket Payments](https://www.providenceri.gov/municipal-court/parking-ticket-payments/): parking-fine link distinct from red-light/speed fines. |
| VT | Burlington city Parking Services only | [Parking Services](https://www.burlingtonvt.gov/314/Parking): “Pay or Appeal Tickets” and parking-office contacts. |

## Unlisted issuers

Private lots, campus tickets, airport tickets, unlisted municipalities, unsupported states, and uncertain issuers receive contact guidance, not a guessed payment URL. Four official municipal website directories are offered where checked:

- [Connecticut](https://portal.ct.gov/en/government/cities-and-towns)
- [Massachusetts](https://www.mass.gov/lists/massachusetts-city-and-town-websites)
- [Rhode Island](https://www.ri.gov/towns/)
- [Vermont](https://www.vermont.gov/towns-and-Cities)

These directories locate an office; they are not payment portals. The app does not convert a moving-violation/traffic-citation portal into a generic parking-payment route.

## Source verification and limits

Sources were researched on October 26, 2026 through official government/municipal pages. The NJMCdirect destination was followed from Jersey City's source page and opened in a real browser: the page displayed the Traffic/Parking ticket option, court ID/name, prefix, ticket number and additional search criteria. No ticket data was entered and no payment was attempted. Lewiston’s official link resolved to the exact Maine partner URL in the directory.

Hartford and New Haven returned 403 to the web text-fetch tool, but both loaded in the browser and displayed the expected parking-payment instructions. Other cited source pages were read through the web tool; this is not an end-to-end payment test of every external provider. The Maine portal requires JavaScript. An initial legacy NJMCdirect domain lookup timed out; the implementation uses the court-hosted destination linked by the official city page instead.

No amounts, fees, deadline rules, legal consequences or appeal deadlines were copied into the directory. The user's original notice and issuing office remain the source for those details. The page shows a source link and research date. Official websites and payment providers can change; there is no background revalidation service. Follow-up maintenance must reopen the source and destination, verify issuer scope, update the research date, and run the route tests.

Spanish and Tagalog interface/direction copy is proposed and has not been reviewed by native speakers. Official agency names and destination-site labels remain recognizable in English. No claim of translation accuracy is made.

## Implementation boundary

- `frontend/parking-data.js`: only the researched HTTPS destinations, source URLs, scope and instruction keys.
- `frontend/parking.js`: exact state + issuer selection; clears issuer when state changes; safe text-node rendering; opens links with `noopener noreferrer` and `no-referrer`.
- `frontend/onboarding.js`: state choice before the four tutorial steps. “Another state” and “I’m not sure yet” let users continue. The reader can also change the state later.
- The service worker caches these public modules with the app shell. External government sites still need connectivity.
- No new API calls, model calls, notice persistence, geolocation, ticket-number fields, payment forms or secret access were introduced. The existing language preference remains the only persistent preference.

## Validation

Commands from the repository root:

```sh
node --test tests/*.mjs > docs/parking-resources/node.txt
../../work/m4-audit-venv/bin/python -m pytest -q > docs/parking-resources/pytest.txt
git diff --check
```

- **42 JavaScript tests passed, 0 failed**, including 9 directory/controller tests. Tests cover all 12 routes, state changes, cross-state rejection, unknown/private issuers, unsupported states, translations, offline shell inclusion and no storage/network calls in this controller.
- **422 Python tests passed**, with 1 existing Starlette/AnyIO deprecation warning. Extraction prompts, validators and scoring were not changed; no held-out or model evaluation was run.
- **18 phone-layout combinations passed**: state selection and NJ directions, at 320/390/430 CSS pixels, in English/Spanish/Tagalog. No horizontal overflow; measured new controls and links were at least 44 px high. Raw results: `phone-checks.json`. These were browser-sized layout fixtures, not physical-device testing.
- Actual app served with `OPENAI_API_KEY='' OPENAI_MODEL='' APP_ENV=development RENDER=false ../../work/m4-audit-venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8023 --no-access-log`. Its real module flow passed state selection → tutorial → reader → NJMCdirect directions, Spanish/Tagalog updates, and removing stale links on state/issuer changes. `app-smoke.json` records the language and reset checks. No notice upload or paid model call was needed.

The blue side border and top tab on the photo panel were removed. The panel now has one continuous neutral border and uniform rounded corners.
