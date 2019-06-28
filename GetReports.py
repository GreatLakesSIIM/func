import requests
import json
import SendEmail
import datetime
from email.mime.text import MIMEText

baseUrl = "http://hackathon.siim.org/fhir/"
headers = {
    'apikey': "e84abb04-c381-4fc8-9a92-3d72ff719133",
    'Accept': "application/json",
    'User-Agent': "PostmanRuntime/7.15.0",
    'Cache-Control': "no-cache",
    'Host': "hackathon.siim.org",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

def fhirGet(reference,params = {}):
    url = baseUrl + reference
    return requests.request("GET", url, headers=headers,params=params)
    
def patientName(patient):
    if("name" not in patient):
        return None
    return patient["name"][0]["given"][0]
    

def reportToPcp(report):
    if("subject" not in report["resource"]):
        return None
    #get patient reference 
    patientRef = report["resource"]["subject"]["reference"]
    #load patient from fhir
    patient = fhirGet(patientRef)
    #get practitioner "generalPractitioner"
    pPatient = json.loads(patient.text)
    if("generalPractitioner" not in pPatient):
        return None
    pcpRef = pPatient["generalPractitioner"][0]["reference"]
    #get general practitioner from fhir
    fPcp = fhirGet(pcpRef)
    pcp = json.loads(fPcp.text)
    pcp["patient"] = pPatient
    return pcp

def find_ACR3(res_entry, code_sys, code_value):
    inc_findings_inds = []
    for i in range(len(res_entry)):
        codes = res_entry[i]['resource']['code']['coding']
        for entry in codes:
            if entry['system'] == code_sys and entry['code'] == code_value:
                print('Incidental Finding found!')
                inc_findings_inds.append(i)
    return inc_findings_inds


def post_SOLE_report_signed():
    current_time = datetime.datetime.now()
    url = "http://hackathon.siim.org/sole/bulk-syslog-events"

    payload = f'{{\"Events\": [\r\n{{\r\n\"Pri\" : \"136\",\r\n\"Version\": \"1\",\r\n\"Timestamp\": \"{current_time}\",\r\n\"Hostname\": \"Real.Hospital.org\",\r\n\"App-name\": \"func\",\r\n\"Procid\": \"1234\",\r\n\"Comment\": \"Followup needed for Diagnostic Report found with ACR-3 code RID49482\",\r\n\"Msg-id\": \"GLakes001\",\r\n\"Msg\": \"Report Signed\"\r\n}}\r\n]\r\n}}'
    headers = {
        'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'Postman-Token': "237ead16-b88e-4267-a885-3e13636ab31a"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print('REPORT SIGN SOLE POSTED')

def post_SOLE_report_delegated():
    current_time = datetime.datetime.now()
    url = "http://hackathon.siim.org/sole/bulk-syslog-events"

    payload = f'{{\"Events\": [\r\n{{\r\n\"Pri\" : \"136\",\r\n\"Version\": \"1\",\r\n\"Timestamp\": \"{current_time}\",\r\n\"Hostname\": \"Real.Hospital.org\",\r\n\"App-name\": \"func\",\r\n\"Procid\": \"1234\",\r\n\"Comment\": \"Followup Accepted for non-actionable finding\",\r\n\"Msg-id\": \"SOLE107\",\r\n\"Msg\": \"Crit 3 Notification Delegated\"\r\n}}\r\n]\r\n}}'
    headers = {
        'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'Postman-Token': "de5de528-3b84-4a60-b342-d33871f74535"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print('REPORT DELEGATED SOLE POSTED')

def post_SOLE_order_filled(proc_id):
    current_time = datetime.datetime.now()
    url = "http://hackathon.siim.org/sole/bulk-syslog-events"

    payload = f'{{\"Events\": [\r\n{{\r\n\"Pri\" : \"136\",\r\n\"Version\": \"1\",\r\n\"Timestamp\": \"{current_time}\",\r\n\"Hostname\": \"Real.Hospital.org\",\r\n\"App-name\": \"func\",\r\n\"Procid\": \"1234\",\r\n\"Comment\": \"Communication sent to general practitioner {proc_id}\",\r\n\"Msg-id\": \"SOLE101\",\r\n\"Msg\": \"Order Filled\"\r\n}}\r\n]\r\n}}'
    headers = {
        'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'Postman-Token': "d65e38b3-599f-497a-9a90-c05145d4ec72"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print('ORDER FILLED SOLE POSTED')

#Start by getting all DiagnosticReports 

reports = fhirGet("DiagnosticReport")
#convert to python equivelent for parsing
pReports = json.loads(reports.text)
#all entries (reports)
pEntries = pReports["entry"]


ACR_indices = find_ACR3(pEntries, 'RADLEX', 'RID49482')
print(ACR_indices)
post_SOLE_report_signed()

#loop through reports
for i in range(len(ACR_indices)):
    entry_i = ACR_indices[i]
    report = pEntries[entry_i]
    #make sure report has patient subject
    pcp = reportToPcp(report)
    patient_name = patientName(pcp["patient"])
    #print(patient_name)
    if(pcp == None):
        print("failed with report ")
        continue
    #print(json.dumps(pcp))
    if("telecom" not in pcp):
        print("Pcp has no form of valid communication to contact")
        continue
    #get Email
    email = ""
    for com in pcp["telecom"]:
        if(com["system"] == "email"):
            email = com["value"]
    #do stuff with new information

    url = "http://hapi.fhir.org/baseDstu3/Communication/"
    lastupdated = datetime.datetime.now()

    payload = '''
{
    "resourceType": "Communication",

    "partOf": [
        {
            "display": "Followup accepted on Non-actionable Findings"
        }
    ],
    "meta": {
        "versionId": "1",
        "lastUpdated": "'''+ lastupdated +'''"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "RADLEX",
                    "code": "RID49482"
                }
            ],
            "text": "Alert",
            "pcp_email": "''' + email + '''",
            "pcp_id": "''' + pcp['id'] + '''",
            "patient_name": "''' + patient_name + '''"
        }
    ],
    "payload": [
        {
            "contentString": "General Practitioner ''' + pcp['id'] + ''' has accepted the followup responsibilities for patient ''' + patient_name + '''"
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
    print(f'COMMUNICATION RESOURCE POSTED TO REMOTE FHIR SERVER {url} FOR PROVIDER {pcp["id"]}')
    post_SOLE_order_filled(pcp['id'])

