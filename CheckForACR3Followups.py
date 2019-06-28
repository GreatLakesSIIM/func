import requests
import datetime


def find_ACR3_comm(res_entry, code_sys, code_value):
    inc_findings_inds = []
    for i in range(len(res_entry)):
        if 'category' in res_entry[i]['resource']:
            codes = res_entry[i]['resource']['category'][0]['coding']
            for entry in codes:
                if 'system' in entry and 'code' in entry:
                    if entry['system'] == code_sys and entry['code'] == code_value:
                        print('Incidental Finding found!')
                        inc_findings_inds.append(i)
    return inc_findings_inds

headers = {
    'apikey': "c2e5d31b-8ba0-4d22-a41e-a2396c2de76d",
    'Accept': "application/json",
    'Cache-Control': "no-cache",
    'Content-Type': "application/json",
    'Postman-Token': "de5de528-3b84-4a60-b342-d33871f74535"
    }
print(1)
all_comms = requests.get(url='http://hapi.fhir.org/baseDstu3/Communication/', headers=headers).json()['entry']
print(2)
ACR3_inds = find_ACR3_comm(all_comms, 'RADLEX', 'RID49482')
print(ACR3_inds)
for i in ACR3_inds:
    print(i)
    pcp_email = res_entry[i]['resource']['email']
    pcp_id = res_entry[i]['resource']['pcp_id']
    patient_name = res_entry[i]['resource']['patient_name']



    message_text = f'''\
    <pre> 
    You have a Follow-up Non-critical Actionable Finding.
    email: {pcp_email}
    pcp id: {pcp_id}
    patient name: {patient_name}

    Click accept.
    <a href="https://google.com"><img border="0" alt="Accept" src="http://www.iconarchive.com/download/i104134/custom-icon-design/flatastic-9/Accept.ico" width="100" height="100"></a>
    <a href="https://bing.com"><img border="0" alt="Deny" src="https://cdn.pixabay.com/photo/2016/02/02/05/53/cancel-1174809_960_720.png" width="100" height="100"></a>
    </pre>
    '''
    message = MIMEText(message_text,'html')

    title = "Actionable Finding for patient: " + patientName(pcp["patient"])
        ## dont actually spam them with emails...yet
        #SendEmail.sendEmail(email,message,title)
    print(message_text)