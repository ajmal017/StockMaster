import requests, bs4 

# Scrapes the stock exchange end-of-the-day information and returns it as a list of dictionaries
# to be passed into a template as context later 
def info_scraper():
    list_struct = []
    index = 1 
    while index < 8:
        url = 'http://www.nepalstock.com/main/todays_price/index/' + str(index)
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        info_table = soup.find_all("tr")
        info_table = info_table[2:len(info_table) - 4]
        for item in info_table:
            dict_struct = {}
            dict_struct['company'] = {'company_name': item.contents[3].contents[0]}
            dict_struct['number_of_transactions'] = int(item.contents[5].contents[0])
            dict_struct['maximum'] = float(item.contents[7].contents[0])
            dict_struct['minimum'] = float(item.contents[9].contents[0])
            dict_struct['closing'] = float(item.contents[11].contents[0])
            dict_struct['traded_shares'] = float(item.contents[13].contents[0])
            dict_struct['amount'] = float(item.contents[15].contents[0])
            dict_struct['previous_closing'] = float(item.contents[17].contents[0])
            dict_struct['difference_rs'] = float(item.contents[19].contents[0].strip())
            list_struct.append(dict_struct)

        index += 1
    return list_struct

