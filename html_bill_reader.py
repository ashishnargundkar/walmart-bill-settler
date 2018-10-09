from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from lxml import html

PRODUCT_NAME_XPATH_TEMPLATE = "/html/body/div[1]/div/div/main/div/div[2]/ul/li/ul/li[{}]/div[2]/div[1]/a"

if __name__ == "__main__":
    SCOPES = "https://www.googleapis.com/auth/spreadsheets"

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '1MpuwUjxAmK3n75tG2X0KQC6aA-ePmPhJ1xQAmVU53nY'
    RANGE_NAME = 'aug_25_2018!A2:B'

    values = list()
    with open("/Users/apnargundkar/Documents/walmart_bills/Walmart - Account - Order Details.html") as f:
        html_resp = html.fromstring(f.read())
        items = html_resp.xpath("/html/body/div[1]/div/div/main/div/div[2]/ul/li/ul/li")
        for i in range(len(items)):
            name = items[i].xpath("div[2]/div[1]/a")[0].text_content()
            price = items[i].xpath("div[2]/div[2]/span/span")[0].text_content()

            values.append([name, price])
            print(name, price)

    body = {
        "values": values,
    }

    value_input_option = "USER_ENTERED"
    result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption=value_input_option, body=body).execute()

