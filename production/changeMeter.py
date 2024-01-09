import requests
import base64
import json

import dossAuthentication

def createOperation(meterAssociationId, odometer, date, lat, lon):
    meterAssociationId = int(meterAssociationId)
    date = str(date)
   
    payload = { 
        "meterReadingId":0,
        "readingTime":date,
        "lifeTotal":0,
        "personId":6438,
        "person":None,
        "description":"created from API",
        "latitude":lat,
        "longitude":lon,
        "suspect":False,
        "suspectApproved":None,
        "workOrderId":None,
        "workOrder":None,
        "inspectionId":None,
        "inspection":None,
        "fluidUsageId":None,
        "fluidUsage":None,
        "meterAssociationId":meterAssociationId,
        "meterMethodId":1,
        "reading":odometer}
    
  
    json_params = json.dumps(payload)
    return json_params

def makeMeterChangeRequest(access_token, perams):
    url = 'https://d7.dossierondemand.com/api/assets/meterreadings/CreateMeterReading'

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url=url, data=perams, headers=headers, verify=False)
        return response
    
    except:
        print("error making request")
        return False

if __name__ == "__main__":

    access_token = dossAuthentication.getAccessToken()

    meter_id = 12388
    odometer = 466615.9
    date = "2024-01-08T14:55:08.000Z"
    lat = 41.6395946
    lon = -111.9164663

    payload = createOperation(meter_id, odometer, date, lat, lon)
    response2 = makeMeterChangeRequest(access_token=access_token, perams=payload)

    with open("CreateMeterReading.json", "w") as file:
        file.write(response2.text)


    print(response2)
    print(response2.text)
   