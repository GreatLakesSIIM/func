import requests
import datetime

def post_SOLE_accepted_delegation():
    current_time = datetime.datetime.now()
    url = "http://hackathon.siim.org/sole/bulk-syslog-events"

    payload = f'{{\"Events\": [\r\n{{\r\n\"Pri\" : \"136\",\r\n\"Version\": \"1\",\r\n\"Timestamp\": \"{current_time}\",\r\n\"Hostname\": \"Real.Hospital.org\",\r\n\"App-name\": \"func\",\r\n\"Procid\": \"1234\",\r\n\"Comment\": \"General Practitioner has accepted responsibility for followup\",\r\n\"Msg-id\": \"SOLE107\",\r\n\"Msg\": \"Crit 3 Notification Delegated\"\r\n}}\r\n]\r\n}}'
    headers = {
        'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'Postman-Token': "de5de528-3b84-4a60-b342-d33871f74535"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print('POSTED SOLE EVENT FOR NOTIFICTION DELEGATION')


url = "http://hackathon.siim.org/fhir/Communication/"

payload = '''
{
    "resourceType": "Communication",

    "partOf": [
        {
            "display": "General Practitioner has accepted responsibility for the followup"
        }
    ],
    "category": [
        {
            "coding": [
                {
                    "system": "http://acme.org/messagetypes",
                    "code": "Notification"
                }
            ],
            "text": "Notification"
        }
    ],
    "payload": [
        {
            "contentString": "General Practitioner has accepted the followup responsibilities for patient"
        },
        {
            "contentReference": {
                "display": "Followup accepted for Non-Actionable Lung Mass"
            }
        }
    ]
}
'''
headers = {
    'apikey': "25822b15-300b-4ba2-953c-e0c0e310cfef",
    'Content-Type': "application/fhir+json",
    'Cache-Control': "no-cache",
    'Postman-Token': "76dcd8d9-d530-4e2f-8016-f296867080cf"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(f'COMMUNICATION RESOURCE POSTED TO ORIGINAL FHIR SERVER {url}. GP HAS ACCEPTED RESPONSIBILITY')
post_SOLE_accepted_delegation()