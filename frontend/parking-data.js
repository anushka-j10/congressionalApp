// Curated official sources; research and coverage limits: docs/parking-resources/RESEARCH.md.
export const parkingData = {
  "checked_on": "2026-10-26",
  "states": [
    {
      "code": "CT",
      "name": "Connecticut"
    },
    {
      "code": "ME",
      "name": "Maine"
    },
    {
      "code": "MA",
      "name": "Massachusetts"
    },
    {
      "code": "NH",
      "name": "New Hampshire"
    },
    {
      "code": "NJ",
      "name": "New Jersey"
    },
    {
      "code": "NY",
      "name": "New York"
    },
    {
      "code": "PA",
      "name": "Pennsylvania"
    },
    {
      "code": "RI",
      "name": "Rhode Island"
    },
    {
      "code": "VT",
      "name": "Vermont"
    }
  ],
  "routes": [
    {
      "state": "NJ",
      "id": "nj-municipal",
      "issuer": "New Jersey municipal court",
      "url": "https://portalnjmcdirect-cloud.njcourts.gov/prweb/PRServletPublicAuth/app/MuniPay_/wQ2guhy8lqKPggD8pVI7RLYVZ9vxwNMF%2A/%21STANDARD?AppName=NJMC&fromBrowserHistory=true",
      "instruction_key": "parking_route_nj",
      "source_url": "https://www.jerseycitynj.gov/CityHall/law/municipalcourt"
    },
    {
      "state": "NJ",
      "id": "jersey-city",
      "issuer": "Jersey City Municipal Court",
      "url": "https://www.jerseycitynj.gov/CityHall/law/municipalcourt",
      "instruction_key": "parking_route_jersey",
      "source_url": "https://www.jerseycitynj.gov/CityHall/law/municipalcourt"
    },
    {
      "state": "NY",
      "id": "nyc",
      "issuer": "New York City Department of Finance",
      "url": "https://www.nyc.gov/site/finance/vehicles/services.page",
      "instruction_key": "parking_route_nyc",
      "source_url": "https://www.nyc.gov/site/finance/vehicles/services.page"
    },
    {
      "state": "PA",
      "id": "philadelphia",
      "issuer": "Philadelphia Parking Violations Branch",
      "url": "https://www.phila.gov/services/cars-parking-transportation/pay-or-dispute-a-ticket/pay-a-parking-ticket/",
      "instruction_key": "parking_route_philadelphia",
      "source_url": "https://www.phila.gov/services/cars-parking-transportation/pay-or-dispute-a-ticket/pay-a-parking-ticket/"
    },
    {
      "state": "CT",
      "id": "hartford",
      "issuer": "Hartford Parking Authority",
      "url": "https://www.hartfordct.gov/Residents/Transportation/Car-HPA/Pay-A-Parking-Ticket",
      "instruction_key": "parking_route_hartford",
      "source_url": "https://www.hartfordct.gov/Residents/Transportation/Car-HPA/Pay-A-Parking-Ticket"
    },
    {
      "state": "CT",
      "id": "new-haven",
      "issuer": "City of New Haven",
      "url": "https://www.newhavenct.gov/government/departments-divisions/finance/divisions/accounts-receivable",
      "instruction_key": "parking_route_new_haven",
      "source_url": "https://www.newhavenct.gov/government/departments-divisions/finance/divisions/accounts-receivable"
    },
    {
      "state": "MA",
      "id": "boston",
      "issuer": "City of Boston Parking Clerk",
      "url": "https://www.boston.gov/departments/parking-clerk/how-pay-parking-ticket",
      "instruction_key": "parking_route_boston",
      "source_url": "https://www.boston.gov/departments/parking-clerk/how-pay-parking-ticket"
    },
    {
      "state": "ME",
      "id": "maine-participating",
      "issuer": "parking_maine_issuer",
      "url": "https://me.accessgov.com/maine-municipal/Forms/Page/parking/memuniparkingtickets/1",
      "instruction_key": "parking_route_maine",
      "source_url": "https://www.lewistonmaine.gov/141/Welcome"
    },
    {
      "state": "NH",
      "id": "nashua",
      "issuer": "City of Nashua",
      "url": "https://www.nashuanh.gov/978/Parking-Tickets-Violations",
      "instruction_key": "parking_route_nashua",
      "source_url": "https://www.nashuanh.gov/978/Parking-Tickets-Violations"
    },
    {
      "state": "NH",
      "id": "hanover",
      "issuer": "Town of Hanover",
      "url": "https://www.hanovernh.org/785/Payments-and-Appeals",
      "instruction_key": "parking_route_hanover",
      "source_url": "https://www.hanovernh.org/785/Payments-and-Appeals"
    },
    {
      "state": "RI",
      "id": "providence",
      "issuer": "Providence Municipal Court",
      "url": "https://www.providenceri.gov/municipal-court/parking-ticket-payments/",
      "instruction_key": "parking_route_providence",
      "source_url": "https://www.providenceri.gov/municipal-court/parking-ticket-payments/"
    },
    {
      "state": "VT",
      "id": "burlington",
      "issuer": "City of Burlington Parking Services",
      "url": "https://www.burlingtonvt.gov/314/Parking",
      "instruction_key": "parking_route_burlington",
      "source_url": "https://www.burlingtonvt.gov/314/Parking"
    }
  ],
  "directories": {
    "CT": "https://portal.ct.gov/en/government/cities-and-towns",
    "MA": "https://www.mass.gov/lists/massachusetts-city-and-town-websites",
    "RI": "https://www.ri.gov/towns/",
    "VT": "https://www.vermont.gov/towns-and-Cities"
  }
};

// No fuzzy matching, model-provided URLs, or cross-state fallback.
export function parkingRoute(state, issuer) {
  return parkingData.routes.find(route => route.state === state && route.id === issuer) || null;
}
export function knownParkingState(state) {
  return parkingData.states.some(item => item.code === state);
}
