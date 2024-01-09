import requests
import os
import dossAuthentication
import parseResponse

# query {"page":1,"amount":25,"filter":{"filters":[{"field":"disposition.status.name","operator":"eq","value":"Active"}]},"groupBy":[],"orderBy":[{"field":"isTechnician","dir":"asc"}],"expands":[{"name":"Disposition","expands":[{"name":"Status"}]},{"name":"Site"},{"name":"Shift"},{"name":"LaborRate"},{"name":"DefaultLaborActivity"},{"name":"Supervisor"}]}
def getMechanics(access_token):
    #url = "https://d7.dossierondemand.com/api/personnel/personnel?operation=eyJwYWdlIjoxLCJhbW91bnQiOjIwLCJmaWx0ZXIiOnsiZmlsdGVycyI6W3siZmllbGQiOiJzdXBlcnZpc29yLmZpcnN0TmFtZSIsImFsdGVybmF0ZUZpZWxkIjoic3VwZXJ2aXNvcklkIiwib3BlcmF0b3IiOiJlcSIsInZhbHVlIjoiQmxha2UifV0sImxvZ2ljIjoiYW5kIn0sImdyb3VwQnkiOltdLCJvcmRlckJ5IjpbeyJmaWVsZCI6InN1cGVydmlzb3IuZmlyc3ROYW1lIiwiZGlyIjoiZGVzYyJ9XSwiZXhwYW5kcyI6W3sibmFtZSI6IkRpc3Bvc2l0aW9uIiwiZXhwYW5kcyI6W3sibmFtZSI6IlN0YXR1cyJ9XX0seyJuYW1lIjoiU2l0ZSJ9LHsibmFtZSI6IlNoaWZ0In0seyJuYW1lIjoiTGFib3JSYXRlIn0seyJuYW1lIjoiRGVmYXVsdExhYm9yQWN0aXZpdHkifSx7Im5hbWUiOiJTdXBlcnZpc29yIn1dLCJhZ2dyZWdhdGVzIjpbXSwiZ2xvYmFsQWdncmVnYXRlcyI6W119"
    url =  "https://d7.dossierondemand.com/api/personnel/personnel?operation=eyJwYWdlIjoxLCJhbW91bnQiOjI1LCJmaWx0ZXIiOnsiZmlsdGVycyI6W3siZmllbGQiOiJkaXNwb3NpdGlvbi5zdGF0dXMubmFtZSIsIm9wZXJhdG9yIjoiZXEiLCJ2YWx1ZSI6IkFjdGl2ZSJ9XX0sImdyb3VwQnkiOltdLCJvcmRlckJ5IjpbeyJmaWVsZCI6ImlzVGVjaG5pY2lhbiIsImRpciI6ImFzYyJ9XSwiZXhwYW5kcyI6W3sibmFtZSI6IkRpc3Bvc2l0aW9uIiwiZXhwYW5kcyI6W3sibmFtZSI6IlN0YXR1cyJ9XX0seyJuYW1lIjoiU2l0ZSJ9LHsibmFtZSI6IlNoaWZ0In0seyJuYW1lIjoiTGFib3JSYXRlIn0seyJuYW1lIjoiRGVmYXVsdExhYm9yQWN0aXZpdHkifSx7Im5hbWUiOiJTdXBlcnZpc29yIn1dfQo="

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'}
    
    response = requests.get(url=url, headers=headers, verify=False)
    return response

# {"page":1,"amount":25,"filter":{"filters":[{"field":"status","operator":"eq","value":"Active"},{"field":"year","operator":"currentyearnumber"},{"field":"month","operator":"currentmonthnumber"}]},"groupBy":[],"orderBy":[{"field":"lastName","dir":"asc"},{"field":"firstName","dir":"asc"},{"field":"year","dir":"desc"},{"field":"month","dir":"desc"}]}

# Once we start getting fancy we can probably change the currentyearnumber field to spesific months that we're looking for.
def getStatsforMechanics(access_token):
    url = "https://d7.dossierondemand.com/api/analytics/personkpis?operation=eyJwYWdlIjoxLCJhbW91bnQiOjI1LCJmaWx0ZXIiOnsiZmlsdGVycyI6W3siZmllbGQiOiJzdGF0dXMiLCJvcGVyYXRvciI6ImVxIiwidmFsdWUiOiJBY3RpdmUifSx7ImZpZWxkIjoieWVhciIsIm9wZXJhdG9yIjoiY3VycmVudHllYXJudW1iZXIifSx7ImZpZWxkIjoibW9udGgiLCJvcGVyYXRvciI6ImN1cnJlbnRtb250aG51bWJlciJ9XX0sImdyb3VwQnkiOltdLCJvcmRlckJ5IjpbeyJmaWVsZCI6Imxhc3ROYW1lIiwiZGlyIjoiYXNjIn0seyJmaWVsZCI6ImZpcnN0TmFtZSIsImRpciI6ImFzYyJ9LHsiZmllbGQiOiJ5ZWFyIiwiZGlyIjoiZGVzYyJ9LHsiZmllbGQiOiJtb250aCIsImRpciI6ImRlc2MifV19"

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'}
    
    response = requests.get(url=url, headers=headers, verify=False)
    return response

if __name__ == "__main__":
    access_token = dossAuthentication.getAccessToken()
    print(access_token)
    response = getMechanics(access_token)
    print(response)

    response2 = getStatsforMechanics(access_token)


    with open("response2.txt", "w") as file:
        file.write(response2.text)

 
