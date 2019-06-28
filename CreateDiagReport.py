import requests
import datetime

def post_SOLE_report_approved():
    url = "http://hackathon.siim.org/sole/bulk-syslog-events"

    payload = "{\"Events\": [\r\n{\r\n\"Pri\" : \"136\",\r\n\"Version\": \"1\",\r\n\"Timestamp\": \"2015-03-17T00:05\",\r\n\"Hostname\": \"Real.Hospital.org\",\r\n\"App-name\": \"func\",\r\n\"Procid\": \"1234\",\r\n\"Comment\": \"Diagnostic Report created\",\r\n\"Msg-id\": \"RID45924\",\r\n\"Msg\": \"Report approved\"\r\n}\r\n]\r\n}"
    headers = {
        'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
        'Accept': "application/json",
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'Postman-Token': "63ba42c8-ea34-48b6-85e5-7ab9f9faf1fb"
        }

    response = requests.request("PUT", url, data=payload, headers=headers)
    print('SOLE report approved')


patient_ref = "14953"
current_time = datetime.datetime.now()

url = "http://hackathon.siim.org/fhir/DiagnosticReport"

payload = f'{{\n    \"resourceType\": \"DiagnosticReport\",\n    \"meta\": {{\n        \"versionId\": \"3\",\n        \"lastUpdated\": \"{current_time}\"\n    }},\n    \"text\": {{\n        \"status\": \"generated\",\n        \"div\": \"<div xmlns=\\\"http://www.w3.org/1999/xhtml\\\">No mass, hemorrhage or hydrocephalus. Basal ganglia and posterior fossa structures are normal. No established major vessel vascular territory infarct. No intra or extra axial collection. The basal cisterns and foramen magnum are patent.\\t    The air cells of the petrous temporal bone are non-opacified. No fracture demonstrated.\\n\\t\\t      Scans through the base of the brain are unremarkable. The oropharynx and nasopharynx are within normal limits. The airway is patent. The epiglottis and epiglottic folds are normal. The thyroid, submandibular, and parotid glands enhance homogenously. The vascular and osseous structures in the neck are intact. There is no lymphadenopathy. The visualized lung apices show a mass lesion of the left apex, homogenously enhancing 1.4 cm x 2.6 cm.</div>\"\n    }},\n    \"identifier\": [\n        {{\n            \"use\": \"usual\",\n            \"system\": \"http://www.siim.org/\",\n            \"value\": \"a82375098312098375982\"\n        }}\n    ],\n    \"status\": \"final\",\n    \"code\": {{\n        \"coding\": [\n            {{\n                \"system\": \"http://hl7.org/fhir/v2/0074\",\n                \"code\": \"ARC-3\"\n            }},\n            {{\n                \"system\": \"RADLEX\",\n                \"code\": \"RID49482\"\n            }}\n        ]\n    }},\n    \"subject\": {{\n        \"reference\": \"Patient/{patient_ref}\"\n    }},\n    \"effectiveDateTime\": \"2019-06-26\",\n    \"issued\": \"2019-06-26T12:30:00\",\n    \"performer\": [\n        {{\n            \"reference\": \"Organization/siim\",\n            \"display\": \"Society Of Imaging Informatics in Medicine\"\n        }}\n    ],\n    \"media\": [\n        {{\n            \"comment\": \"Thunderclap headache, suspicious for subarachnoid hemorrhage.\"\n        }}\n    ],\n    \"conclusion\": \"No acute intracranial process.Homogenously enhancing left lung mass, absent on prior CT\"\n}}'

headers = {
    'apikey': "25822b15-300b-4ba2-953c-e0c0e310cfef",
    'Content-Type': "application/fhir+json",
    'Cache-Control': "no-cache",
    'Postman-Token': "ce99ed9f-f377-4e66-b0d4-6ff99ffcf21e"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(response)
print(f'DIAGNOSIS REPORT CREATED FOR {patient_ref}')
