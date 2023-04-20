
import unittest
import os
import sys
import json
import pandas as pd
import uuid
sys.path.insert(0, os.getcwd() + '/program')
sys.path.insert(0, os.getcwd() + '/test') 
import getPrice
from data_file_for_test import *

# url lists for testing purpose
TARGET_URL_LIST_JB = [TARGET_URL1,TARGET_URL2,TARGET_URL3,TARGET_URL4]
TARGET_URL_LIST_CHEM = [TARGET_URL_CHEM_1,TARGET_URL_CHEM_2]
TARGET_URL_LIST_DIGI = [TARGET_URL_DIGI_1,TARGET_URL_DIGI_2]
TARGET_URL_LIST_IKEA = [TARGET_URL_IKEA_1,TARGET_URL_IKEA_2]
TARGET_URL_LIST_GG = [TARGET_URL_GG_1,TARGET_URL_GG_2,TARGET_URL_GG_3]
TARGET_URL_LIST_UMART = [TARGET_URL_UMART_1,TARGET_URL_UMART_2]
TARGET_URL_LIST_REDBUBBLE = [TARGET_URL_RB_1,TARGET_URL_RB_2]
TARGET_URL_LIST_TED = [TARGET_URL_TEDS_1,TARGET_URL_TEDS_2, TARGET_URL_TEDS_3]
TARGET_URL_LIST_HYPOX = [TARGET_URL_HYPOX_1,TARGET_URL_HYPOX_2,TARGET_URL_HYPOX_3]
TARGET_URL_LIST_HM = [TARGET_URL_HM_1,TARGET_URL_HM_2]

# domain not work, cant get full html and cant figure out why
TARGET_URL_LIST_WW = [TARGET_URL_WW_1,TARGET_URL_WW_2]
TARGET_URL_LIST_BUNNINGS = [TARGET_URL_BUNNINGS_1]

TARGET_URL_LIST_MIX = [TARGET_URL_LIST_JB,TARGET_URL_DIGI_1,TARGET_URL_IKEA_2]
TARGET_URL_LIST_MIX_BIG = TARGET_URL_LIST_JB+TARGET_URL_LIST_DIGI+TARGET_URL_LIST_IKEA+TARGET_URL_LIST_CHEM

def make_logging(url_list,product_name_list,result_list,target_list):
    data = {
        "url_list"      : url_list,
        "product name"  : product_name_list,
        "price current" : result_list,
        "price was"     : target_list
    }
    df = pd.DataFrame(data)
    return df



""" the goal is to test the stableness of web sraping """
class TestGetPrice(unittest.TestCase):

    def add_entry_to_data_file(self ,url):
        """add entry to data file for test"""
        with open('test/UnitTest.json', 'r') as f:
            search_result = json.load(f)
        entry = {}
        entry["url"]=url
        entry["price"] = getPrice.get_price_single_url(url)
        entry["email"] = "test"
        entry["phone"] = "test"
        search_result[str(uuid.uuid4())] = entry
        # print(search_result)
        data = json.dumps(search_result, indent=4)
        with open('test/UnitTest.json', 'w') as outfile:
            outfile.write(data)
        return None

    def test_getPrice_within_rage(self):
        '''
        test fail if price difference above or below 25%
        '''
        with open('test/UnitTest.json', 'r') as f:
            search_result = json.load(f)
        for uuid in search_result:
            entry = search_result[uuid]
            url = entry["url"]
            price_b4 = entry["price"]
            price_current = getPrice.get_price_single_url(url)
            print(url,":::", price_current)
            # print(type(price_b4))
            if type(price_b4) == float:
                self.assertTrue(price_b4*0.5 <= price_current <= price_b4*1.5)
            else:
                self.assertTrue(price_current == price_b4)
            

if __name__ == '__main__':
    
    "run all test"
    unittest.main()
    
    
    t=TestGetPrice()
    "run particular test"
    # t.test_getPrice_within_rage()
    "add more url"
    # TARGET_URL_FOR_ADD = [TARGET_URL_PANASONIC_2]
    # for url in TARGET_URL_FOR_ADD:
    #     t.add_entry_to_data_file(url)
