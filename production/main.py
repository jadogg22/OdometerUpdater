import os
from dotenv import load_dotenv

import soapClient
import soapParse

import dossAuthentication
import getDossierAssetID
import changeMeter

import logging
import itertools
import sys

spinners = itertools.cycle(['-', '\\', '|', '/'])  

def getRequiredData(access_token, key):
    try:
        print(f"getting info for {str(key)}")
        response = getDossierAssetID.makeMeterReadingRequest(access_token, key)
    except:
        print("trouble making the request")
        return False

    try:
        if not response.text:
            print("Nothing returned in response")
            return False
        else:
            return response
    except:
        print("honestly how")

if __name__ == '__main__':
    logging.basicConfig(
    filename='errorLogs.log',  # Specify the log file name
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define log message format
    )
    ## Main Omnitracks to dossier ##

    # Setup for the soapClient
    load_dotenv()
    omniUsername = os.environ["omniUsername"]
    omniPassword = os.environ["omniPassword"]

    equipment_data = {}
    lastTran = 0

    # Because this is a que based system, There are only a few ways to know when the queue is finished
    #1. It sends a completly empty transactionblock, This will force transactions to be false and that way we can break out of the loop because there is no data to add to our dic
    #2. Each transaction block sends 500 transactions if there are less we are finished. In this case then transactions are there the last transaction = 
    while True:
        sys.stdout.write('Fetching Batch request ')
        sys.stdout.flush()
        response = soapClient.createRequest(omniUsername, omniPassword, lastTran)
        sys.stdout.write('\b' * 16)  

        sys.stdout.write('Parsing Response ') 
        sys.stdout.flush()
        transaction_id = lastTran 
        transactions, lastTran = soapParse.parseXML(response.text)
        sys.stdout.write('\b' * 16)

        if transactions == False:
            break

        sys.stdout.write('Creating Data ')
        sys.stdout.flush()
        for _ in range(5):
            sys.stdout.write(next(spinners))
            sys.stdout.flush() 
            print("\b", end="", flush=True)
        equipment_data = soapParse.createData(equipment_data, transactions) 

        if lastTran == False:
            break
        
####### Doss Side #######

    access_token = dossAuthentication.getAccessToken()
        
    #Using the dictionary just created, get the meter ID and doss asset ID for each of the omni asset ID's

    for key in equipment_data:
        print(f"Truck ID:{key}")

        response = getRequiredData(access_token=access_token, key=key)
        if response:
            meter_id, dossAssetID = getDossierAssetID.parseResponse(response, str(key))
            if meter_id:

                odometer = equipment_data[key]["odometer"]
                date = equipment_data[key]["eventTS"]
                lat = equipment_data[key]["lat"]
                lon = equipment_data[key]["lon"]

                    # Finally create the meter reading
                payload = changeMeter.createOperation(meter_id, odometer, date, lat, lon)
                if payload:
                    response2 = changeMeter.makeMeterChangeRequest(access_token=access_token, perams=payload)

                    try:
                        if response2.status_code != 201:
                            logging.error(f"error updating tractor {key}, {response2}:{response2.text}")
                    except Exception as e:
                        logging.error(f"an exeption happend: {str(e)}", exc_info=True)
            else:
                logging.error(f"no info for {key}")
        
                        




    
