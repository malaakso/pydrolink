# Hydrolink API

The API is a simple RPC style API with JSON payloads. API endpoints represent actions to sync various data from the server to the client. Each API invocation requires a token to be included in the POST payload, obtained initially by calling the login endpoint with user name and password. API is not very uniform, evident for example as booleans in three different formats: As strings "t" and "f", as strings "true" and "false", and as proper booleans.

# Login

HTTP POST to https://hydrolink.fi/api/v2/login with application/json payload `{"username": "myuser", "password": "mypass"}`. Response with application/json payload `{"token": "supersecrettoken"}`. Each API call expects this json object in the payload. Token seems to be valid for a very long time. When API returns 401 Unauthorized, it is necessary to login again.

# Apartment information

HTTP POST to https://hydrolink.fi/api/v2/getResidentCompanyData. Response

    {
    "name": "Company name",
    "streetAddress": "Company address",
    "zipCode": "02610",
    "town": "Espoo",
    "warmWaterPrice": "8,51",
    "coldWaterPrice": "4,12",
    "apartmentName": "Apartment identifier",
    "meters": [
        {
            "id": 165255,
            "code": "111",
            "warm": true,
            "apartmentId": 81065
        },
        {
            "id": 165256,
            "code": "41",
            "warm": false,
            "apartmentId": 81065
        },
        {
            "id": 165257,
            "code": "112",
            "warm": true,
            "apartmentId": 81065
        }
    ],
    "temperatureMeters": [],
    "leakageMeters": [
        {
            "id": 1079,
            "code": "202",
            "apartmentId": 81065
        },
        {
            "id": 1080,
            "code": "203",
            "apartmentId": 81065
        }
    ],
    "energyMeters": [],
    "billingStart": null,
    "billingPeriodMonths": null
    }

Besides water meters with their IDs and "codes" (i.e. local identifiers), this includes also energy meters, temperature sensors and leakage meters if installed. Water prices are in currency per m^3.

# Current readings

HTTP POST to https://hydrolink.fi/api/v2/current. Response

    [
    {
        "warm": "t",
        "code": "111",
        "meter_id": "165255",
        "value": "175518",
        "created": "2025-01-30 16:13:00",
        "secondary_address": "03118470"
    },
    {
        "warm": "f",
        "code": "41",
        "meter_id": "165256",
        "value": "283702",
        "created": "2025-01-30 16:15:00",
        "secondary_address": "03116267"
    },
    {
        "warm": "t",
        "code": "112",
        "meter_id": "165257",
        "value": "2856",
        "created": "2025-01-30 16:21:00",
        "secondary_address": "03118471"
    }
    ]

where "warm": "t" indicates a meter for warm water and "warm": "f" for cold water. The property "value" is the current reading in liters, reported at time corresponding to "created". 

# Alarms

HTTP POST to https://hydrolink.fi/api/v2/getAlarms. Response

    [
    {
        "overflow": "false",
        "battery_change": "false",
        "removed": "false",
        "bwflow": "false",
        "waterloss": "false",
        "mag_fraud": "false",
        "meter_id": "165255",
        "waterloss_calculated": "false",
        "opt_fraud": "false",
        "created": "0"
    },
    {
        "overflow": "false",
        "battery_change": "false",
        "removed": "false",
        "bwflow": "false",
        "waterloss": "false",
        "mag_fraud": "false",
        "meter_id": "165256",
        "waterloss_calculated": "false",
        "opt_fraud": "false",
        "created": "0"
    },
    {
        "overflow": "false",
        "battery_change": "false",
        "removed": "false",
        "bwflow": "false",
        "waterloss": "false",
        "mag_fraud": "false",
        "meter_id": "165257",
        "waterloss_calculated": "false",
        "opt_fraud": "false",
        "created": "0"
    }
    ]

shows various alarms for the corresponding meters.

# Historical data

HTTP POST https://hydrolink.fi/api/v2/getResidentMeterData. Response contains daily and monthly readings for each meter and is very large.

    {
    "username": "myuser",
    "meters": [
        {
            "id": 165255,
            "code": "111",
            "secondaryAddress": "03118470",
            "warm": true,
            "latestValue": 175518,
            "latestTimestamp": 1738246380000,
            "dailyReadings": [
                {
                    "subtraction": 114,
                    "updatedAt": 165498143546,
                    "created": 1654896960000,
                    "kind": "WARM_WATER",
                    "timesIncremented": 79
                }, ...
            ],
            "monthlyReadings": [
                {
                    "subtraction": 3824,
                    "updatedAt": 1659301435306,
                    "created": 1656624720000,
                    "kind": "WARM_WATER",
                    "timesIncremented": 2475
                }, ...
            ]
        },
        {
            "id": 165256,
            "code": "41",
            "secondaryAddress": "03116267",
            "warm": false,
            "latestValue": 283702,
            "latestTimestamp": 1738246500000,
            "dailyReadings": [ ...
            ],
            "monthlyReadings": [ ...
            ]
        },
        {
            "id": 165257,
            "code": "112",
            "secondaryAddress": "03118471",
            "warm": true,
            "latestValue": 2856,
            "latestTimestamp": 1738246860000,
            "dailyReadings": [ ...
            ],
            "monthlyReadings": [ ...
            ]
        }
    ],
    "temperatureMeters": [],
    "energyMeters": []
    }

Here UNIX timestamps are used instead of dates and times.
