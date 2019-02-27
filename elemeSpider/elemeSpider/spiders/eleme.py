# -*- coding: utf-8 -*-
import scrapy
import json
import pymysql
from elemeSpider.items import ShopInfoItem, FoodInfoItem

db = pymysql.connect('10.102.24.254', 'wuyifa', 'wuyifa1234', 'lifeplus')
cursor = db.cursor()


class ElemeSpider(scrapy.Spider):
    name = 'eleme'
    allowed_domains = ['www.ele.me']
    start_urls = ['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw3xbqqpjvn&latitude=31.203607&limit=24&longitude=121.638529&offset=24&terminal=web']
    offset = 24

    def parse(self, response):
        shop_list = json.loads(response.text)
        for shop in shop_list:
            item = ShopInfoItem()
            item['shop_id'] = shop['id']
            item['shop_address'] = shop['address']
            item['shop_latitude'] = shop['latitude']
            item['shop_longitude'] = shop['longitude']
            item['shop_name'] = shop['name']
            item['shop_description'] = shop['piecewise_agent_fee']['rules'][0]['fee']
            item['shop_sending_price'] = shop['piecewise_agent_fee']['rules'][0]['price']
            item['shop_order_lead_time'] = shop['order_lead_time']
            row = item.Judge_Id()
            if row:
                continue
            item.Save_data()
            url = 'https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={}&terminal=web'.format(
                item['shop_id'])
            yield scrapy.Request(url, callback=self.food_parse)
        self.offset += 24
        url = 'https://www.ele.me/restapi/shopping/restaurants?geohash=wk6wepfvne2q&latitude=25.092277&limit=24&longitude=104.901517&offset={}&terminal=web'.format(
            self.offset)
        yield scrapy.Request(url, callback=self.parse)

    def food_parse(self, response):
        food_list = json.loads(response.text)
        item = FoodInfoItem()
        for category in food_list:
            foods = category['foods']
            item['category_name'] = category['name']
            for food in foods:
                item['food_id'] = food['specfoods'][0]['food_id']
                row = item.Judge_Id()
                if row:
                    continue
                item['food_name'] = food['specfoods'][0]['name']
                item['category_id'] = food['category_id']
                item['food_price'] = food['specfoods'][0]['price']
                item['original_price'] = food['specfoods'][0]['original_price']
                if not item['original_price']:
                    item['original_price'] = 0
                item['packing_fee'] = food['specfoods'][0]['packing_fee']
                item['month_sales'] = food['month_sales']
                item['description'] = food['description']
                item['restaurant_id'] = food['restaurant_id']
                item.Save_data()
