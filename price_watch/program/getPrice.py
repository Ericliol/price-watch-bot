
import json
import pandas as pd
import random 
import bs4 as bs
from urllib.request import Request, urlopen
from scrapingant_client import ScrapingAntClient
import urllib.error
import os
from fake_useragent import UserAgent
"""
the program should take input of a list of url, return a table containing the name of the 
product listed as well as the sell price at the time of execute
seach_result.json will be updated later in common.py
"""

DOLLAR_SIGN = '$'



SEARCH_STRING_LIST = ['facebook-product-data','Price','price','range-revamp-price__integer']
KEY_SEARCH_STRING_LIST = ['value','Value','price','Price','$',"AUD"]
NUMBER =  ['1','2','3','4','5','6','7','8','9','0']
PRICE_CHAR_LIST = NUMBER+['.']
TO_CLEAN_STRING_LIST = ['"','"',':',',',";",'/','|',"`"] + KEY_SEARCH_STRING_LIST

def run_getPrice(url_list:list) -> pd.DataFrame:
    '''
    take a list of url
    return a panda table of webpage domain, product name and price
    '''
    webpage = 'webpage not found'
    search_locaton = 0
    df_url_list = []
    web_page_list = []
    name_list = []
    prices_list = []
    # those list are used later to generate pandas dataframe

    with open(os.getcwd() +'\search_path.json', 'r') as f:
        data_dict = json.load(f)
    for url in url_list:
        for domain in data_dict:
            if domain in url:
                df_url_list.append(url)
                webpage = domain
                sub_dict = data_dict[domain]
                search_sting = sub_dict['search string']
                search_method_index = sub_dict['search method']
                search_locaton = sub_dict['search location']
                algorithm = sub_dict['algorithm']
                
        web_page_list.append(webpage)
        name, data = new_read_web(url,search_sting,search_method_index, algorithm)
        if "404" in name:
            name_list.append(name)
            prices_list.append(get_price_single_url(url))
        else:
            name_list.append(name)
            if search_locaton >=0:
                prices_list.append(get_price(data)[search_locaton])
            else:
                prices_list.append(get_price_small(data))
    if os.path.exists("program/websraper.html"):
        os.remove("program/websraper.html")
    return data_frame_gen(df_url_list,web_page_list,name_list,prices_list)



def new_read_web(url:str, search_sting:str, search_method_index:int, algorithm:str ):
    '''
    read web given url
    return product name a list of data
    '''
    soup = get_beautifulsoup(url,algorithm)
    if soup == 404:
        return "404","dummy"

    product_name = soup.title.string
   
    if "404" in product_name:
        return product_name,"dummy"
    else:
        if search_method_index == 0:
            search = soup.find(id=search_sting)
        elif  search_method_index == 1:
            search = soup.find(class_=search_sting)
        elif search_method_index == 2:
            search = soup.find(type=search_sting)
        elif search_method_index == 3:
            search_list = soup.find_all(class_=search_sting)
            sp = False
            for elem in search_list:
                if "Special Price" in elem.text:
                    sp = True
                    search = elem
            if sp == False:
                search = search_list[0]
        elif search_method_index == 4:
            search = str(soup.find("meta",attrs = search_sting))
            return product_name, search.split(' ') 
        # print(product_name,search_sting,search_method_index)
        try:
            list_by_split = search.text.replace(" ","\n").split("\n")
            try:
                while True:
                    list_by_split.remove("")
            except ValueError:
                pass
            return product_name, list_by_split
        except:
            return product_name, "error"

def random_ua():
    """
    return a ramdom useragent select fromt the useragent pool"""
    useragent = ''
    with open(os.getcwd() +'\\program\\user_agent.json', 'r') as f:
        user_agent_dict = json.load(f)
    randomize_browsers = user_agent_dict['randomize']
    browser = randomize_browsers[str(random.randint(1,len(randomize_browsers)))]
    randomize_useragent = user_agent_dict["browsers"][browser]
    useragent = random.choice(randomize_useragent)
    return useragent

def get_beautifulsoup(url:str, algorithm:str) -> bs.BeautifulSoup:
    '''
    given a url return a beautifulsoup object of the html of the webpage
    use cmd and curl method
    '''

    # ua = UserAgent(cache=True)
    #print(ua.random)
    #print(ua.chrome)

    
    if algorithm == "urlopen":
        headers = {
        'authority': 'httpbin.org', 
    	'cache-control': 'max-age=0', 
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
        'sec-ch-ua-mobile': '?0', 
        'upgrade-insecure-requests': '1', 
        'User-Agent': random_ua(), 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'sec-fetch-site': 'none', 
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-user': '?1', 
        'sec-fetch-dest': 'document', 
        'accept-language': 'en-US,en;q=0.9'
            }
        req = Request(url, headers=headers)
        try:
            webpage = urlopen(req).read()
            my_HTML = webpage.decode("utf8")  
        except urllib.error.HTTPError:
            return 404
    elif algorithm == "ScrapingAntClient":

        client = ScrapingAntClient(token='9938cafc0e6a4c04bc20152d68bb1f80')

        # Get the HTML page rendered content
        my_HTML = client.general_request(url).content
    with open('program/websraper.html', 'w', encoding="utf-8") as outfile:
        outfile.write(my_HTML)
    
    return open_webscraper()


def open_webscraper():
    with open("program/websraper.html", "r",encoding='utf-8') as f:
        return bs.BeautifulSoup(f, 'html.parser')

def get_price_small(data:list) -> float:
    '''
    for small data list
    return price
    '''
    try:
        maybe_prices_cleaned = []
        # print(data)
        for elem in data:
            for string in TO_CLEAN_STRING_LIST:
                elem = elem.replace(string,'')
            maybe_prices_cleaned.append(elem)
        data = [line.strip().strip(',') for line in maybe_prices_cleaned]
        
        return float(data[0])
    except:
        return'price not found'

def get_price(data:list) -> list:
    '''
    take a data list which contains the price
    return a list price
    '''
    if data == "error":
        return ["error accured"]
    maybe_prices = [str(line) for line in data if any(string in str(line) and string != str(line) for string in KEY_SEARCH_STRING_LIST)]
    maybe_prices_cleaned = []
    
    for elem in maybe_prices:
        if len(elem) > 100:
            elems_small = elem.split(",")
            for elem_small in elems_small:
                for string in KEY_SEARCH_STRING_LIST:
                    if string in elem_small:
                        elem_small = elem_small.replace(string,'')
                        for string in TO_CLEAN_STRING_LIST:
                            elem_small = elem_small.replace(string,'')
                        maybe_prices_cleaned.append(elem_small)
        else:
            for string in TO_CLEAN_STRING_LIST:
                
                elem = elem.replace(string,'')
            maybe_prices_cleaned.append(elem)
    
    maybe_prices_striped = [line.strip().strip(',') for line in maybe_prices_cleaned]
    
    try:
        while True:
            maybe_prices_striped.remove("")
    except ValueError:
        pass
    price_list = [float(item) for item in maybe_prices_striped if all(string in PRICE_CHAR_LIST for string in item)]
    
    for item in data:
        item = item.replace(",","")
        try:
            
            price_list.append(float(item))
        except:
            continue

    return price_list

def data_frame_gen(url_list,web_page_list,name_list, prices_list) -> pd.DataFrame:
    """
    given the data of lists of webpage name and price
    return the data frame genterated by pandas
    """
    data = {
        "url"         : url_list,
        "web page"    : web_page_list,
        "product name": name_list,
        "price"       : prices_list
    }
    df = pd.DataFrame(data)
    return df
    
def load_data_from_old_search_result(email):
    """
    load data from search_result.json file
    geven a user email
    retrun a list of url and price
    if email address not found, returns None
    """
    with open('program/search_result.json', 'r') as f:
        data = json.load(f)
    if email in data:
        url_list = []
        price_list = []
        user_entries = data[email]
        for entry in user_entries:
            url_list.append(entry['url'])
            price_list.append(entry['price'])
        return url_list, price_list
    else:
        return "invaild",None

def load_data_from_csv():
    """
    load data from data.csv file
    retrun a list of url and price
    """
    df = pd.read_csv('program/data.csv', index_col='url')
    data_list = df['price'].to_string().split('\n')[1:]
    url_list = [line.split()[0] for line in data_list]
    privious_price = [float(line.split()[1]) for line in data_list]
    return url_list,privious_price

def get_price_single_url(url:str) -> int:
    pprice = "unable"
    with open('program/search_path.json', 'r') as f:
        data_dict = json.load(f)
  

    for domain in data_dict:
        if domain in url:
            sub_dict = data_dict[domain]
            search_sting = sub_dict['search string']
            search_method_index = sub_dict['search method']
            search_locaton = sub_dict['search location']
            algorithm = sub_dict['algorithm']

            name, data = new_read_web(url,search_sting,search_method_index,algorithm)
            # print(name,data)
            if "404" not in name:
                if search_locaton >=0:
                    pprice = get_price(data)[search_locaton]
                else:
                    pprice = get_price_small(data)
            else:
                return "404 error"
    if os.path.exists("program/websraper.html"):
        os.remove("program/websraper.html")
    return pprice


"""the testing loop"""

# tester_input = input("hi tester! input url to get price, input E to exit---  ")
# while tester_input != "E":
#     print(get_price_single_url(tester_input))
#     tester_input = input("hi tester! input url to get price, input E to exit---  ")



# bs_object = get_beautifulsoup("https://www.kmart.com.au/product/lego-icons-vespa-125-10298-43124664/?sku=43124664&region_id=400001&gclid=Cj0KCQjw1tGUBhDXARIsAIJx01ndXyB4jXzcxfeutAXRwOU9Pwu4QwB18gIN2404C_cg0leyPcaO_nIaAjdfEALw_wcB&gclsrc=aw.ds")


"""domain wont work"""
"https://www.woolworths.com.au"
"https://www.davidjones.com"
"https://www.kmart.com.au"


# get_beautifulsoup("https://www.davidjones.com/product/rm-williams-shearling-rider-jacket-24760388?nav=881495")
# curl https://www.davidjones.com/product/calvin-klein-monogram-sleeve-badge-crew-sweat-25050870?nav=945217 > C:\Users\ericy\uq\work\price_watch\program\curl.html
