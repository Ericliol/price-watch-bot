'''put all function together and interact with user'''
from searchPrice import *
from getPrice import *

def update_search_path(url,search_string,search_method):
    with open('program/search_path.json', 'r') as f:
        data_dict = json.load(f)
    domain = url_to_domain(url)
    path_dict = {}
    path_dict["algorithm"] = "BeautifulSoup"
    path_dict["version"] = 1
    path_dict["search string"] = search_string
    path_dict["search method"] = search_method
    path_dict["search location"] = 0

    data_dict[domain] = path_dict
    data = json.dumps(data_dict, indent=4)
    with open('program/search_path.json', "w") as outfile:
        outfile.write(data)
    return None

def update_search_result(email, df:pd.DataFrame):
    """
    given a user email and dataframe contains products and prices the
    user looking for
    update the search_result.json file accordingly
    """
    with open('program/search_result.json', 'r') as f:
        search_result = json.load(f)
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    search_result[email] = parsed
    search_result = json.dumps(search_result, indent=4)
    with open('program/search_result.json', "w") as outfile:
        outfile.write(search_result)
    return None

def url_to_domain(url:str):
    """
    input a url return the doamin of that URL
    """
    start = url.index("www")
    if ".au" in url:
        index = url.index(".au")+3
    elif ".au" in url:
        index = url.index(".com")+4
    return url[start:index]

def main():
    # target_url_list,privious_price_list = load_data_from_old_search_result()

    user_email = input("hi user what is your email/username?  (eg: example)")
    target_url_list,privious_price_list = load_data_from_old_search_result(user_email)
    while target_url_list == "invaild":
        print("invaild email")
        user_email = input("hi user what is your email? ")
    user_input = input(WELCOME_MESSAGE)
    while user_input != "E":
        if user_input == "Q":
            data_frame = run_getPrice(target_url_list)
            new_price_list = data_frame.loc[:,"price"]
            # print(new_price_list)
            price_differ = [price_old_i - price_new_i for price_old_i, price_new_i in zip(privious_price_list,new_price_list) ]
            update_search_result(user_email,data_frame)
            print(data_frame)
            print(price_differ)
        elif user_input == "D":
            for index, url in enumerate(target_url_list):
                print(index, url)
            user_choice_to_del = input("which url do u wish to remove from watch list? input index ")
            try:
                user_choice_to_del = int(user_choice_to_del)
                target_url_list.pop(user_choice_to_del)
                data_frame = run_getPrice(target_url_list)
                update_search_result(user_email,data_frame)
                print(data_frame)
            except:
                print(INVALID_INPUT+" index need to be integer")
        elif user_input == "A":
            new_url = input("new target url? ")
            if search_domain_in_data(new_url):
                target_url_list.append(new_url)
            else:
                price = input("looks like a new domain, what is the product price? ")
                search_string,search_method = find_price(new_url,price)
                update_search_path(new_url,search_string,search_method)
                target_url_list.append(new_url)

            data_frame = run_getPrice(target_url_list)
            update_search_result(user_email,data_frame)
            
        else:
            print(INVALID_INPUT)
        
        user_input = input(WELCOME_MESSAGE)
    print(EXIT_MESSAGE)

if __name__=='__main__':
    main()
