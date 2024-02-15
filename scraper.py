import re
# from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import random
#
# user_agents = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
# ]
user_agents = [
    'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S) Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; moto g(7) play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; SM-J737VPP) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0: Win64: x64) AppleWebKit/537.36 (KHTML: like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/109.0.5414.112 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Lenovo TB-J706F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; ALE-L21) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto g(9) plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; TECNO BG6 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.60 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; VOG-L29; HMSCore 6.13.0.302; GMSCore 22.36.16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/14.0.2.311 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A326U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; moto e30 Build/ROP31.166-112) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.145 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; MRD-LX1F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.185 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; M2103K19G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.1; Lenovo TB-8504X Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Safari/537.36'
]
# Replace 'your_proxy_api_key' with your actual proxy API key
# proxy_api_key = 'your_proxy_api_key'
# proxy_url = f'http://username:{proxy_api_key}@proxy.example.com:port'



# Use the `proxies` parameter to specify the proxy
params={
      'api_key': 'b71706ed-0477-49f5-a81f-984203d78c3a',
      'url': 'https://www.realtor.com/',
      # 'cookies': "sessionId=cffbc7e688864b6811f676e181bc29e6;userToken=d6a1e2453d44f89",
      'js': "true",
      'residential': 'true'
  }

# We need townhomes and mobiles for california 51+100
loop_on_states = ["New-Yourk","Massachussets", "Florida","New-Jersey", "California","Texas","Ohio"]
years = ["1+1", "2+2", "3+3", "4+5", "6+10", "11+20","21+50", "51+100"]
types = ["single-family-home","condo","townhome","multi-family-home","mfd-mobile-home"]
# session = requests.Session()
for s in loop_on_states:
    for y in years:
        links = []
        is_pool = []
        year_built = []
        bedrooms = []
        bathrooms = []
        sizes = []
        prices = []
        states = []
        p_types = []
        for t in types:

            try:
                for p in range(1, 40):

                    time.sleep(20)
                    url = f'https://www.realtor.com/realestateandhomes-search/{s}/type-{t}/beds-1-6/baths-1-6/sqft-500-3500/age-{y}/price-200000-1000000/sby-2/pg-{p}'
                    print(url)
                    headers = {
                        'api_key': 'b71706ed-0477-49f5-a81f-984203d78c3a',
                        'User-Agent': random.choice(user_agents),
                        'Referer': 'https://www.google.com/',
                        'Accept-Language': 'en-US',
                        # 'proxy' : "premium"
                    }

                    # Add the `proxies` parameter to the request
                    response = requests.get(url, headers=headers, params=params, )
                    time.sleep(20)
                    print(response.status_code)
                    if response.status_code != 200:
                        break
                    content = BeautifulSoup(response.text, 'html.parser')

                    # print(content.prettify())
                    houses = content.find_all(class_='hpwkPm')
                    print("1")
                    if len(houses) == 0:
                        # time.sleep(5)
                        houses = content.find_all(class_='BasePropertyCard_propertyCardWrap__MvslD')
                        print("2")
                        if len(houses) == 0:
                            houses = content.find_all(class_='BasePropertyCard_propertyCard__MOMVx')
                            print("3")
                            if len(houses) == 0:
                                houses = content.find_all(class_='PropertyCardstyles__StyledCard-rui__sc-7yjdgx-0')
                                print("4")
                                if len(houses) == 0:
                                    houses = content.find_all(class_='Cardstyles__StyledCard-rui__sc-6oh8yg-0')
                                    print("5")
                    # while houses is None:
                    #     time.sleep(5)
                    #     houses = content.find_all(class_='hpwkPm')
                        # print('No houses found')
                    print("Num of Houses:",len(houses))
                    for j, house in enumerate(houses):
                        # print("j:", j, "for", p)
                        # time.sleep(3)
                        house_link = house.find('a', href=True)['href']
                        link = "https://www.realtor.com" + str(house_link)
                        try:
                            num_bedrooms = house.find(class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0').text
                        except:
                            num_bedrooms = ""
                        # time.sleep(3)
                        try:
                            num_bathrooms = house.find(class_='PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0').text
                        except:
                            num_bathrooms = ""
                        # time.sleep(3)
                        try:
                            size = house.find(class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0').text
                        except:
                            size = ""
                        # time.sleep(3)
                        try:
                            price = house.find(class_='price-wrapper').string
                        except:
                            price = ""
                        # .card-description
                        # time.sleep(3)
                        links.append(link)
                        sizes.append(size)
                        bathrooms.append(num_bathrooms)
                        bedrooms.append(num_bedrooms)
                        prices.append(price)
                        is_pool.append(0)
                        year_built.append(y)
                        states.append(s)
                        p_types.append(t)

            except Exception as e:
                print(f"An error occured: {e}")
        properties = {
            'links': links,
            'sizes': sizes,
            'bathrooms': bathrooms,
            'bedrooms': bedrooms,
            'is_pool': is_pool,
            'prices': prices,
            'year_built': year_built,
            'states': states,
            'types': p_types
        }

    # print(properties)
        df = pd.DataFrame(properties)
        df.to_csv(f't_{s}_w_sp_{y}.csv')

# print(links)
# time.sleep(3)
# for i,link in enumerate(links[0:2]):
#     time.sleep(5)
#     session_page = requests.Session()
#     page = session_page.get(links[i], headers=headers, params=params).text
#     doc = BeautifulSoup(page, 'html.parser')
#     print(doc.prettify())
#     rooms = doc.find(class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0',attrs='property-meta-beds')
#     number_room = rooms.span.text
#
#     baths = doc.find(class_='PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0',
#                          attrs='property-meta-baths').span.text
#     size = doc.find(class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0',
#                         attrs='property-meta-sqft').span.text
#     arce_lot = doc.find(class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0',
#                             attrs='property-meta-lot-size').span.text
#     # try:
#     #     address = content.find(class_='LDPHomeFactsstyles__StyledAddressContainer-sc-11rfkby-0')
#     #     print("address is ", address)
#     #     a = address.find(class_='LDPHomeFactsstyles__H1-sc-11rfkby-3')
#     #     full_address = a.text
#     # except AttributeError:
#     #     full_address = ""
#     # if house_type is not None:
#     #     house_type = content.find('div', class_='iNkwaK').text
#     # else:
#     #     house_type = ''
#     # try:
#     #     house_type = content.find('div', class_='base__StyledType-rui__sc-108xfm0-0 iNkwaK listing-key-fact-item__value').text
#     # except AttributeError:
#     #     house_type = ""
#     # try:
#         # year_built = content.find(class_='ListingKeyFactsstyles__StyledListingKeyFacts-rui__sc-196zwd6-0').find(string=re.compile('^\\d{4}$'))
#     # except AttributeError:
#     #     year_built = ""
#     year_built = doc.find(string=re.compile('^\\d{4}$'))
#     try:
#         price = doc.find(class_='Pricestyles__StyledPrice-rui__btk3ge-0').text
#     except AttributeError:
#         price = ""
#     properties.append([year_built, arce_lot, size, baths, number_room, link])
#
# print(properties)
#
# d = pd.DataFrame(properties)
# d.to_csv("mycsv3.csv")

# with open('test.html', 'w') as f:
#
#     f.write(str(content))

# rooms = content.find(class_='PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0', attrs='property-meta-beds')
# number_room = rooms.span.text
#
# baths = content.find(class_='PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0', attrs='property-meta-baths').span.text
# size = content.find(class_='PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0', attrs='property-meta-sqft').span.text
# arce_lot = content.find(class_='PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0', attrs='property-meta-lot-size').span.text
# address = content.find(class_='LDPHomeFactsstyles__StyledAddressContainer-sc-11rfkby-0')
# a = address.find(class_='LDPHomeFactsstyles__H1-sc-11rfkby-3')
# full_address = a.text
#
# house_type = content.find('div', class_='base__StyledType-rui__sc-108xfm0-0 iNkwaK listing-key-fact-item__value').string
#
# year_built = content.find(class_='ListingKeyFactsstyles__StyledListingKeyFacts-rui__sc-196zwd6-0').find(string = re.compile('^\\d{4}$'))
# price = content.find(class_='Pricestyles__StyledPrice-rui__btk3ge-0').string
