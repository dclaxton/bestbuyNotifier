import properties
import json
import time
import datetime
from bestbuy import BestBuyAPI
from twilio.rest import Client

def checkStock():
    #Get the Item SKU's we want to search for
    query = "sku in(" + properties.skus + ")"
    #Query the API and get the json response
    response = bb.products.search(query=query, format="json")
    #Dump the response object to a string
    json_object = json.dumps(response, indent = 4)
    #load the parsed string to a dict object
    response_parsed = json.loads(json_object)
    #Will return T/F, checks to see if the product can be ordered online
    greyInStock = response_parsed['products'][0]['onlineAvailability']
    colorInStock = response_parsed['products'][1]['onlineAvailability']
    return greyInStock,colorInStock

def main():
    #Loop every 10 minutes to check, if they are in stock, shoot a text to my phone
    while True:
        grey,color = checkStock()
        if grey or color:
            twil_client.messages \
                .create(
                    body="Switches are in stock on BestBuy.com",
                    messaging_service_sid=properties.twilio_msg_sid,
                    to=properties.twilio_personal_number,
                    from_=properties.twilio_msg_service_number
                )
            print("Found one in stock!")
        else: 
            print("No luck this time: " + datetime.datetime.now().strftime("%d-%m-%y %H:%M"))
        time.sleep(300)

if __name__ == "__main__":
    twil_client = Client(properties.twilio_spi_key, properties.twilio_auth_token)
    bb = BestBuyAPI(properties.api_key)
    main()
