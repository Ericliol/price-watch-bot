import requests
from xml.dom import INVALID_ACCESS_ERR
from program.getPrice import *
import json

"""
Given a URL, and current price on the page, and save 'data' to  search_path.json
"""

def find_price(url,price):
    """
    test for find the price location in website html,
    given a url and price, 
    find the parent tab where parent is located
    return the search string and search method
    """
    try:
        float(price)
    except ValueError:
        return "price invalid", "price invalid"
    soup = get_beautifulsoup(url)
    #print(soup.text)

    price_found = soup.find_all(text = str(price))
    if price_found == []:
        price_modifi = string_add_comma(str(price))
        price_found = soup.find_all(text=price_modifi)
    if price_found == []:
        price_found = soup.find_all(text="$")
    if price_found == []:
        price_found = soup.find_all(content=str(price))

    data_string = str(price_found[0].parent.parent)
    data_string_splited = data_string.replace(">","<").split('<')

    # print(data_string_splited,"look")
    search_method = None
    search_string = None
    for string in data_string_splited:
        if "id" in string:
            sub_string_after_id = string[string.index("id"):]
            search_method = 0
            first = sub_string_after_id.index('"') + 1
            last = sub_string_after_id.index('"',first)
            search_string=sub_string_after_id[first:last]
            break
        elif "class" in string:
            sub_string_after_class = string[string.index("class"):]
            search_method = 1
            first = sub_string_after_class.index('"') + 1
            last = sub_string_after_class.index('"',first)
            search_string=sub_string_after_class[first:last]
            break
    if os.path.exists("/tmp/websraper.html"):
        os.remove("/tmp/websraper.html")
    print(search_string,search_method)
    return search_string,search_method

def string_add_comma(string):
    '''
    return a string with comma, group by three char
    eg:
    input = '1223457'
    return = '1,223,457'
    '''
    a = (len(string)-1)//3
    alist = []
    while a > 0 :
        alist.append(a*(-3))
        a = a-1
    for a in alist:
        string = string[:a] + ',' + string[a:]
    print(string)
    return string

def search_domain_in_data(url):
    """
    given a url, return True if the domain is in the search_path json
    """
    with open('program/search_path.json', 'r') as f:
        data_dict = json.load(f)
    for domain in data_dict:
        if domain in url:
            return True
    return False


def handler(event, context):   

    print('request: ', event)

    # Test 1
    # response = requests.get("https://api.cyberlark.com.au/housing/stampduty?state=SA&investment_type=investment&property_value=950000&property_type=established&first_home_buyer=true&foreign_buyer=false")
    # print(response.text)

    # # Test 2
    # gg_1 = "https://www.thegoodguys.com.au/linsar-70-inches-4k-uhd-smart-webos-tv-ls70uhdnf"
    # print(find_price(gg_1,1099))

    # price = get_price_single_url(gg_1)
    # print(price)

    try:
        url = event['queryStringParameters']['url']
        print(url)

        price = get_price_single_url(url)
        print(price)

    
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Hello, You Url is {} Price is: {}\n'.format(url, price)
        }
    except:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Sorry, we cant get the price for your url {}\n'.format(url)
        }


#gg_1 = "https://www.thegoodguys.com.au/linsar-70-inches-4k-uhd-smart-webos-tv-ls70uhdnf"
#hm_1 = "https://www.harveynorman.com.au/samsung-65-inch-the-frame-ls03a-4k-qled-smart-tv.html"
#RW_1 = "https://www.raywhite.com/qld/bowen-hills/2674982/"
# print(find_price(gg_1,1099))
#print(find_price(hm_1,2195))
