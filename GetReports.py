import requests
#import ParseReport
import json
import SendEmail
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


#Start by getting all DiagnosticReports 

reports = fhirGet("DiagnosticReport")
#convert to python equivelent for parsing
pReports = json.loads(reports.text)
#all entries (reports)
pEntries = pReports["entry"]


ACR_indices = find_ACR3(pEntries, 'RADLEX', 'RID49482')


message = MIMEText("""\
<pre> 
You have a Follow-up Non-critical Actionable Finding.
Click accept.
<a href="https://google.com"><img border="0" alt="Accept" src="http://www.iconarchive.com/download/i104134/custom-icon-design/flatastic-9/Accept.ico" width="100" height="100"></a>
<a href="https://bing.com"><img border="0" alt="Deny" src="https://cdn.pixabay.com/photo/2016/02/02/05/53/cancel-1174809_960_720.png" width="100" height="100"></a>
</pre>
""",'html')

#loop through reports
for i in range(len(ACR_indices)):
    entry_i = ACR_indices[i]
    report = pEntries[entry_i]
    #make sure report has patient subject
    pcp = reportToPcp(report)
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




    title = "Actionable Finding for patient: " + patientName(pcp["patient"])
    ## dont actually spam them with emails...yet
#SendEmail.sendEmail(email,message,title)