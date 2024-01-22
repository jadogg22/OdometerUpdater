import xml.etree.ElementTree as ET
import re
import base64
import datetime
import ownerOperated

def decode_base64(encoded_content):
    try:
        # Decode the base64-encoded content
        return base64.b64decode(encoded_content).decode('utf-8')

    except ValueError:
        print("Not able ot decode data")
        return False


def extract_odometer_driver_data(decoded_content):

    root = ET.fromstring(decoded_content)
    count = 0
    # Extract information and create a dictionary
    result_dict = {}
    for tran_elem in root.findall(".//tran"):
        count += 1
        try:
            
            tran_id = tran_elem.get("ID")
            event_ts = tran_elem.find(".//eventTS").text

            position_info = tran_elem.find(".//position")
            lat = position_info.get("lat")
            lon = position_info.get("lon")

            odometer = tran_elem.find(".//odometer").text
            equipment_id = tran_elem.find(".//equipment").get("ID")
            driver_id = tran_elem.find(".//driverID").text

            #this is an edge case for owner operated equipment
            if ownerOperated.isOwnerOperated(driver_id):
                continue
            
            #create the dictionary to add.
            result_dict[tran_id] = {
                "eventTS": event_ts,
                "lat": lat,
                "lon": lon,
                "odometer": float(odometer),
                "driverID": driver_id,
                "equipment_id": equipment_id
            }
        except Exception as e:
            continue
   

# checks for a low amount of transactions 
    if count <= 490:
        tran_id = False

    return result_dict, tran_id


def parseXML(xml):
    root = ET.fromstring(xml)

    transactions_element = root.find('.//transactions')
    

    transactions_data = transactions_element.text if transactions_element is not None else None #

    if transactions_data is not None:
        decoded_data = decode_base64(transactions_data)
        if decoded_data is not False:
            transactions, lastTran = extract_odometer_driver_data(decoded_data)
            return transactions, lastTran

    else:
        print("Error getting the transactions from XML")
        return False, False

def createData(equipment_data, data):

    for transaction in data:
        equipment_ID = data[transaction].get('equipment_id')
        odometer = data[transaction].get("odometer")

        if equipment_ID is None or odometer is None:    
            print(f"{equipment_ID} and {odometer} not valid, continueing")
            continue
        


        if equipment_ID not in equipment_data or odometer > equipment_data[equipment_ID]['odometer']:

            equipment_data[equipment_ID] = {
            'eventTS': data[transaction].get('eventTS'),
            'odometer': odometer,
            'driverID': data[transaction].get('driverID'),
            'lat': float(data[transaction].get('lat')),
            'lon': float(data[transaction].get('lon')),
            }
    
    return equipment_data



