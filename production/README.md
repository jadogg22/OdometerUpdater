# Omnitracks to Dosseir Odometer updater

We started out needing this api because the shop every morning needed to go into omnitracks, download a specific exel file, make sure all of the data was good, edit somethings so they were compatible with dosseir side and then finially upload it to their website.

We thought "there must be a better way..." 

so they talked to me, the IT guy.

Well, I've finally got it implemented into doing what it should be doing. There is still alot of work that could be done... but it seems like we are going to be switching to another system here shortly. soooo I may not get back around to it. there are so many more things that they are looking at me getting into. So to start things off we odviasly just have the main file. This program is ment to just be ran, gets all the avalible updates in omnitracks and automatically update dosseir with those new updates.

I'll begin documentation with the Omnitracks side 

## Omnitracks

Omnitracks is a business that has been around for a long time, there website shows it and once I started diving into their backend their age started showing. There system is based of off a SOAP endpoint. Up untill this point I have never heard of anything other then a rest or like in the weird circomstances a crud endpoint. SOAP is an acronym for Simple Object Access Protocol. With no teacher or really that much documentation It didn't seem very simple at all.

### the WSDL

So there is a online document called the wsdl that is suposed to document what the endpoints are and what specific functions you can call, When plugging it into soap api, it pulls up everything and you have a general idea of whats happening but it doesnt work for some reason. 

```python
wsdl = 'https://services.omnitracs.ca/otsWebWS/services/OTSWebSvcs/wsdl/OTSWebSvcs.wsdl'
endpoint = "https://services.omnitracs.com:443/otsWebWS/services/OTSWebSvcs"

```

It took me way to long to notice but for some reason the actual endpoint it sends to you is a .ca instead of a .com from some reason and gives you authentication errors if thats not right. Its super confusing but we got it.

### Creating the request

Here is the meat and potatos of what your looking for if you want to get into basically nothing really changes for what we need to send to the endpoint to make it work It is just a simple soap envelope. If you send this you will get a transaction block back

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://websvcs.otswebws">
   <soapenv:Header>
      <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
         <wsse:UsernameToken wsu:Id="UsernameToken-9B758C98C9802FFE5717036231336251">
            <wsse:Username>XXXXXXXXXXX</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">XXXXXXXXXX</wsse:Password>
            <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">T7NJwUXXXXir1NZjM43QC0w==</wsse:Nonce>
            <wsu:Created>2023-12-26T20:38:53.624Z</wsu:Created>
         </wsse:UsernameToken>
      </wsse:Security>
   </soapenv:Header>
   <soapenv:Body>
      <web:dequeue2>
         <subscriberId>7</subscriberId>
         <transactionIdIn>0</transactionIdIn>
      </web:dequeue2>
   </soapenv:Body>
</soapenv:Envelope>
```

the hardest part was creating the custom security blcok where we just need to add the the nonce which is litterly a client side random number, it can be anything its to prevent replay attacks, also the id needs to be unique so again just a random 10 chars. then just addind the created tag and we're off to the races.

Finally we add the username_token to the soap_body and then we use the subscriber ID to tell them which queue to use and then the last peice of information is good to know as well. Transaction ID when it is zero, does not deque anything and just sends it. Then we can take the last transaction ID that we get and send it again as the transaction ID and boom we get another set that starts right after where we were! eazy.

Really this turned out to be eazy once I figured out how soap works.

### parsing,

I dont really have a lot to add, we just parse the data an then turn it into a dictionary of unique tractor ID's and then use that dictionary to know what to update. probably not the most efficient way at doing this but honestly this was the most tetious part that I didnt love doing soooo. we're going to move on

## Dosseir

Mannn, these guys took forever to get back to me it was right around xmas break and so they were all prolly busy, Really at first all I really needed was some help getting an access token to use there "well documented api" once I finially got ahold of somebody they said it was a little bit more of a proccess and zoom called me. THis turned out to be clutch because he helped me figure out the system quite a bit so first of they have a special endpoint that is dedicated to the receiving the token. so lets go over that.

### Authentication

The first step to being able to access their api is getting a bearer token the endpoint is https://authentication.d7.dossierondemand.com/connect/token and you do a post request with the following json and you will get an access token back

```python
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'DossierApi',
        'client_id': 'sharpTransportationClient',
        'client_secret': secret
    }
```

### I got to key...

Were do you go now that we got the key, well. While on the zoom call the guy told me to just do what I want to do on the website open up the develpoer network side of things and then capture the trafic. typically they are get requests that look something like 
https://d7.dossierondemand.com/api/assets/meterreadings?operation=eyJwYWdlIjoxLCJhbW91bnQiOjEsIm9yZGVyQnkiOlt7ImZpZWxkIjoicGh5c2ljYWxNZXRlcklkIiwiZGlyIjoiZGVzYyJ9LHsiZmllbGQiOiJyZWFkaW5nVGltZSIsImRpciI6ImRlc2MifSx7ImZpZWxkIjoicmVhZGluZyIsImRpciI6ImRlc2MifV0sImZpbHRlciI6eyJsb2dpYyI6ImFuZCIsImZpbHRlcnMiOlt7ImZpZWxkIjoicGh5c2ljYWxNZXRlci5tZXRlckFzc29jaWF0aW9uLmFzc2V0SWQiLCJvcGVyYXRvciI6ImVxIiwidmFsdWUiOjI1NzEwfSx7ImZpZWxkIjoicGh5c2ljYWxNZXRlci5tZXRlckFzc29jaWF0aW9uLm1ldGVySWQiLCJvcGVyYXRvciI6ImVxIiwidmFsdWUiOjE1N30seyJsb2dpYyI6Im9yIiwiZmlsdGVycyI6W3siZmllbGQiOiJzdXNwZWN0Iiwib3BlcmF0b3IiOiJuZXEiLCJ2YWx1ZSI6dHJ1ZX0seyJmaWVsZCI6InN1c3BlY3RBcHByb3ZlZCIsIm9wZXJhdG9yIjoiZXEiLCJ2YWx1ZSI6dHJ1ZX1dfV19LCJleHBhbmRzIjpbeyJuYW1lIjoiUGh5c2ljYWxNZXRlci5NZXRlckFzc29jaWF0aW9uLk1ldGVyLk1ldGVyVHlwZU1lYXN1cmUuTWVhc3VyZSJ9XX0=

The operation is just a base64 encoded additional instructions to get more inforamtion from the server. it looks like this one 

```json

{"page":1,"amount":1,"orderBy":[{"field":"physicalMeterId","dir":"desc"},{"field":"readingTime","dir":"desc"},{"field":"reading","dir":"desc"}],"filter":{"logic":"and","filters":[{"field":"physicalMeter.meterAssociation.assetId","operator":"eq","value":25710},{"field":"physicalMeter.meterAssociation.meterId","operator":"eq","value":157},{"logic":"or","filters":[{"field":"suspect","operator":"neq","value":true},{"field":"suspectApproved","operator":"eq","value":true}]}]},"expands":[{"name":"PhysicalMeter.MeterAssociation.Meter.MeterTypeMeasure.Measure"}]}
```
now figuring out how these filters was really beyond me. I had some Ideas butttt it took me forever figuring it out. basically dossier has their own numbers for the spesific truck that they want to update the odometer for. Even worse, if you want to update the odometer I couldn't find out how to actually update with just then number, you have to use an addtional meter id before you can update the odometer. just for information the value of 25710 is the asset id that we would know as 7870, and the value 157 is the "type" of meter that it is. kinda wierd. but lets move onto how we're going to solve the problem.

### Getting the MeterAccociaitionID

So since they use some wierd value as part of the updating odomter proccess it took a while to figure out how to actually get a good request in the server that would give me everything that I needed. I was able to access the Meter readings endpoing in the getDossierAssetID module to return what I needed with an abomination of a filter that I created 

```json

'{"page":1,"amount":10,"orderBy":[{"field":"physicalMeter.meterAssociation.asset.primaryAssetIdentifier","dir":"asc"},{"field":"readingTime","dir":"desc"},{"field":"reading","dir":"desc"}],"filter":{"logic":"and","filters":[{"field":"physicalMeter.meterAssociation.asset.disposition.status.name","operator":"eq","value":"Active"},{"field":"physicalMeter.meterAssociation.asset.primaryAssetIdentifier","operator":"eq","value":"' + omniAssetID + '","alternateValue":null}]},"expands":[{"name":"Person"},{"name":"PhysicalMeter","expands":[{"name":"MeterAssociation","expands":[{"name":"Asset","expands":[{"name":"AssetType"}]},{"name":"Meter","expands":[{"name":"MeterTypeMeasure","expands":[{"name":"Measure"}]}]}]}]}],"groupBy":[],"aggregates":[],"globalAggregates":[]}'
```

i used string interpoation to add the omniAssetID to search their data base for what I needed to update. honestly I hardly undersand it but it works soooo. we'll just parse this data for the meterID

Once we have the meterID and the rest of the data from omnitracks we are ready to start updating the actual values in their system. 

### Makeing the meter reading

well I tested it a couple of times and it seems to be working basically we just access the createmeterreadings endpoint and give it some json as a post request and we get back a 200 response an the actual newly created "meter reading" object. this is pythonafied json. its aweful I know but send this to the server with the appropreate values and your set 

```python
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
    
```

There you go we've now gone through everything this program does :)


### TODO

1. if dosseir ever gives a error we can usally figure out what it is and continue on with what we're updateing. 

2. better logging

3. uuuh certificate verifation. I looked into it. dunno how. 

