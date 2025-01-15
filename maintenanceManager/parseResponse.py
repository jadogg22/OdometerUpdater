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

def getStatsForTechs(response, techs, df):
    json_data = json.loads(response.text)

    for person in json_data:
        personId = person["personId"]
        if personId in techs:
            print("We got one") 

            techs[personId]["taskEstimatedHours"] = person["taskEstimatedHours"]
            techs[personId]["taskActualHours"] = person["taskActualHours"]
            techs[personId]["mtdTaskEstimatedHours"] = person["mtdTaskEstimatedHours"]
            techs[personId]["mtdTaskActualHours"] = person["mtdTaskActualHours"]
            techs[personId]["ytdTaskEstimatedHours"] = person["ytdTaskEstimatedHours"]
            techs[personId]["ytdTaskActualHours"] = person["ytdTaskActualHours"]
            techs[personId]["taskEstimatedHours"] = person["taskEstimatedHours"]
            techs[personId]["mtdMinutesOverAverageRepair"] = person["mtdMinutesOverAverageRepair"]
            techs[personId]["mtdTaskActualHours"] = person["mtdTaskActualHours"]
            techs[personId]["mtdPurchaseOrderCosts"] = person["mtdPurchaseOrderCosts"]
            techs[personId]["mtdMinutesOverOEMRepair"] = person["mtdMinutesOverOEMRepair"]
            techs[personId]["mtdMinutesOverThirdPartyRepair"] = person["mtdMinutesOverThirdPartyRepair"]
            techs[personId]["mtdMinutesOverCompanyRepair"] = person["mtdMinutesOverCompanyRepair"]
            techs[personId]["ytdMinutesOverOEMRepair"] = person["ytdMinutesOverOEMRepair"]
            techs[personId]["mtdMinutesOverAverageRepair"] = person["mtdMinutesOverAverageRepair"]
            techs[personId]["ytdMinutesOverThirdPartyRepair"] = person["ytdMinutesOverThirdPartyRepair"]
            techs[personId]["ytdMinutesOverCompanyRepair"] = person["ytdMinutesOverAverageRepair"]
            techs[personId]["ytdHoursOverOEMRepair"] = person["ytdHoursOverOEMRepair"]
            techs[personId]["ytdHoursOverThirdPartyRepair"] = person["ytdHoursOverThirdPartyRepair"]
            techs[personId]["ytdHoursOverCompanyRepair"] = person["ytdHoursOverCompanyRepair"]
            techs[personId]["ytdHoursOverAverageRepair"] = person["ytdHoursOverAverageRepair"]

    return techs


