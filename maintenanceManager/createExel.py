import pandas as pd
import json
import dossAuthentication
import getMechanicStats
import parseResponse

def getStatsForTechs(response, techs, df):
    json_data = json.loads(response.text)

    for person in json_data:
        personId = person["personId"]
        if personId in techs:
            print("We got one") 

            techs[personId]["firstName"] = person["firstName"]
            techs[personId]["lastName"] = person["lastName"]
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

            df.loc[len(df)] = techs[personId]
            
    df.to_excel("techsData.xlsx", index=False)

    return True

if __name__ == "__main__":
    df = pd.DataFrame(columns=[
    "firstName",
    "lastName",
    "taskEstimatedHours",
    "taskActualHours",
    "mtdTaskEstimatedHours",
    "mtdTaskActualHours",
    "ytdTaskEstimatedHours",
    "ytdTaskActualHours",
    "mtdMinutesOverAverageRepair",
    "mtdPurchaseOrderCosts",
    "mtdMinutesOverOEMRepair",
    "mtdMinutesOverThirdPartyRepair",
    "mtdMinutesOverCompanyRepair",
    "ytdMinutesOverOEMRepair",
    "ytdMinutesOverAverageRepair",
    "ytdMinutesOverThirdPartyRepair",
    "ytdMinutesOverCompanyRepair",
    "ytdHoursOverOEMRepair",
    "ytdHoursOverThirdPartyRepair",
    "ytdHoursOverCompanyRepair",
    "ytdHoursOverAverageRepair"
])
    access_token = dossAuthentication.getAccessToken()

    response = getMechanicStats.getMechanics(access_token)
    techDict = parseResponse.getTechs(response)

    response2 = getMechanicStats.getStatsforMechanics(access_token)
    data = getStatsForTechs(response2, techDict, df)