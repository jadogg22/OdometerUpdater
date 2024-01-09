import os 
import json

def getTechs(response):
    json_data = json.loads(response.text)

    techs = {}
    for person in json_data:
        if person["isTechnician"] == True:
            personId = person["personId"]
            techs[personId] = {
                "firstName": person["firstName"],
                "lastName": person["lastName"],
                "employeeNumber": person["employeeNumber"]

            }
    return techs

def getStatsForTechs(response, techs):
    json_data = json.loads(response.text)

    for person in json_data:
        personId = person["personId"]
        if personId in techs:
            print("We got one") 
            techs[personId]["mtdTaskActualHours"] = person["mtdTaskActualHours"]
            techs[personId]["taskEstimatedHours"] = person["taskEstimatedHours"]
            techs[personId]["mtdMinutesOverAverageRepair"] = person["mtdMinutesOverAverageRepair"]
            techs[personId]["mtdTaskActualHours"] = person["mtdTaskActualHours"]

    return techs
