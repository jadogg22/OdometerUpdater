import base64
import datetime
import random
import string
import requests

def generate_randomChar(length=16):
    """Generate a random nonce."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_username_token(username, password):
    """Generate the WS-Security UsernameToken."""

    id = generate_randomChar(10)

    # Generate a random Nonce, It can really be anything.
    nonce = generate_randomChar()

    # Timestamp for WSU namespace
    today_datetime = datetime.datetime.today()
    created = today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
 
    return f"""
        <wsse:UsernameToken wsu:Id="UsernameToken-{id}"> 
            xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
            <wsse:Username>{username}</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{password}</wsse:Password>
            <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">
                {base64.b64encode(nonce.encode('utf-8')).decode('utf-8')}
            </wsse:Nonce>
            <wsu:Created>{created}</wsu:Created>
        </wsse:UsernameToken>
    """

def createRequest(username, password, lastTransaction):

    subscriber_id = 7
    transaction_id = lastTransaction 

    endpoint = "https://services.omnitracs.com:443/otsWebWS/services/OTSWebSvcs"

    # Generate the WS-Security UsernameToken
    username_token = generate_username_token(username, password)

    # Set the headers for the request
    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "",
        "Accept-Encoding": "gzip,deflate",
        "Connection": "Keep-Alive"
    }

    # Construct the SOAP envelope
    soap_body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://websvcs.otswebws">
            <soapenv:Header>
                <wsse:Security soapenv:mustUnderstand="1" 
                    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                    xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    {username_token}
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <web:dequeue2>
                    <subscriberId>{subscriber_id}</subscriberId>
                    <transactionIdIn>{transaction_id}</transactionIdIn>
                </web:dequeue2>
            </soapenv:Body>
        </soapenv:Envelope>
    """ 

    request = requests.post(endpoint, data=soap_body, headers=headers, verify=True)  # Set verify to True in production

    return request
