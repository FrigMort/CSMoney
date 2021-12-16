#import >>>
from fake_useragent import UserAgent
import requests
import json
import datetime
import requests
from requests.models import encode_multipart_formdata


###-----Make class for parse cs money------###
class Parse():
    def __init__(self, limit = 60, max_price = 10000, discount = 10):
        self.limit = limit
        self.max_price = max_price
        self.ua = UserAgent()
        self.discount = discount
        self.discountResult = list()
        
    ###----------Mainfunc---------###
    def get_date(self):
           ###----Time on moment of parse------###
        self.time_now = datetime.datetime.now()
        dat = open('output\date.txt', 'w')
        dat.write(str(self.time_now) + '\n')
        ### https://inventories.cs.money/5.0/load_bots_inventory/730? have attributes for scroll page in down, and selfoffset counter that###
        self.offset = 0
        self.cout = 0 #---Cout of page----#
        while True:
            for item in range(self.offset, self.offset + self.limit, 60):###-----SMTH like scrolling
                url = f"https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit={self.limit}&maxPrice={self.max_price}&minPrice=1&offset={item}&withStack=true"
                self.respoce = requests.get( #Make get query on csmoney#
                url = url,
                headers={'user-agent':f'{self.ua.random}'}###context query###
                )
                self.offset += self.limit###---------wrote about it upper
                self.lData = self.respoce.json() ###------convert responce into JsonDates
                self.items = self.lData.get('items')

                for i in self.items:
                    if i.get('overprice') is not None and i.get('overprice')< -self.discount :###filter from file
                        
                        ###------What we're get ???
                        item_full_name = i.get('fullName')
                        item_pict = i.get('steamImg')
                        item_float = i.get('float')
                        item_id = i.get('id')
                        item_3d = i.get('3d')
                        item_OverPrice = i.get('overprice')
                        ###--------Make list with filterPicks
                        self.discountResult.append(
                                {

                                    'Nameof' : item_full_name,
                                    'Picture': item_pict,
                                    'float': item_float,
                                    'inspect': item_3d,
                                    'itemID': item_id,
                                    'item_OverPrice' : item_OverPrice
                                }
                        ) 
                self.cout +=1
                print(f'Page #{self.cout}')###----Print cout of pages
                if len(self.items) < 60:
                    break
            with open('output\discount.json', "w", encoding='utf-8') as f: ###-----Write ours filterDates
                json.dump(self.discountResult, f, indent=4, ensure_ascii=False)





        
    ###------If we want write all
    def write_allDate(self):
        with open( 'output\result.json', "w", encoding= 'utf-8') as file:
            json.dump(self.respoce.json(), file, indent= 4, ensure_ascii=False)

    

if __name__ == '__main__':
    strtprs = Parse()
    strtprs.get_date()
    strtprs.write_allDate()
    