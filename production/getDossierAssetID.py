import requests
import json
import base64
import os


def getKeyValues(dictionaries, primaryAssetIdentifier):
    for d in dictionaries:
        if d["physicalMeter"]["meterAssociation"]["asset"]["primaryAssetIdentifier"] == primaryAssetIdentifier: 
            meterAssociationId = d["physicalMeter"]["meterAssociationId"]
            asset_id = d["physicalMeter"]["meterAssociation"]["assetId"]
            
            return (meterAssociationId, asset_id)
        else:
            print(d)
    print("could not find the asset ID in doss")
    return False, False

def createPerams(omniAssetID):

    decoded = '{"page":1,"amount":10,"orderBy":[{"field":"physicalMeter.meterAssociation.asset.primaryAssetIdentifier","dir":"asc"},{"field":"readingTime","dir":"desc"},{"field":"reading","dir":"desc"}],"filter":{"logic":"and","filters":[{"field":"physicalMeter.meterAssociation.asset.disposition.status.name","operator":"eq","value":"Active"},{"field":"physicalMeter.meterAssociation.asset.primaryAssetIdentifier","operator":"eq","value":"' + omniAssetID + '","alternateValue":null}]},"expands":[{"name":"Person"},{"name":"PhysicalMeter","expands":[{"name":"MeterAssociation","expands":[{"name":"Asset","expands":[{"name":"AssetType"}]},{"name":"Meter","expands":[{"name":"MeterTypeMeasure","expands":[{"name":"Measure"}]}]}]}]}],"groupBy":[],"aggregates":[],"globalAggregates":[]}'
    decoded_bytes = decoded.encode("utf-8")
    encoded =  base64.b64encode(decoded_bytes)

    params = {"operation": encoded.decode("utf-8")}
    return params


def makeMeterReadingRequest(access_token, omniAssetID):
  
    # getting

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'}
    
    url = "https://d7.dossierondemand.com/api/assets/meterreadings"

    params = createPerams(omniAssetID)

    try:
        return requests.get(url=url, params=params, headers=headers, verify=False)
    except:
        print("error getting the response")

def parseResponse(response, omniAssetID):

    if response and response.status_code == 200:
        # The request was successful
        try:
            webJson = json.loads(response.text)
            
            #if it returns false there is no meter and we need to create a new one for that spesific truck.
            return getKeyValues(webJson, omniAssetID)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else: 
        print(f"bad Response {response.status_code}")

           





