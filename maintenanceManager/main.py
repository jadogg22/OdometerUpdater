import dossAuthentication
import getMechanicStats
import parseResponse

if __name__ == "__main__":
    access_token = dossAuthentication.getAccessToken()

    response = getMechanicStats.getMechanics(access_token)
    techDict = parseResponse.getTechs(response)

    response2 = getMechanicStats.getStatsforMechanics(access_token)
    data = parseResponse.getStatsForTechs(response2, techDict)

    for key in data:
        first = data[key]["firstName"]
        last = data[key]["lastName"]
        hours = data[key]["mtdTaskActualHours"]
        print(f'{first} {last}, had : {hours} hours')