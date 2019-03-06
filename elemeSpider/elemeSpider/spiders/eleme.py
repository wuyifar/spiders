# -*- coding: utf-8 -*-
import scrapy
import json
import pymysql
from elemeSpider.items import ShopInfoItem, FoodInfoItem
import redis

db = pymysql.connect('10.102.24.254', 'wuyifa', 'wuyifa1234', 'lifeplus')
cursor = db.cursor()

pool = redis.ConnectionPool(
    host='localhost', port=6379, decode_responses=True, db=1)
r = redis.Redis(connection_pool=pool)

class ElemeSpider(scrapy.Spider):
    name = 'eleme'
    allowed_domains = ['www.ele.me']
    start_urls = ['https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wkezmjyb91xd&latitude=26.618594&limit=24&longitude=106.752487&offset=0&terminal=web']
    offset = 24

    def parse(self, response):
        """
        商铺接口返回响应处理
        """
        shop_list = json.loads(response.text)
        if not len(shop_list):
            return
        for shop in shop_list:
            item = ShopInfoItem()
            item['shop_id'] = shop['authentic_id']
            item['shop_address'] = shop['address']
            item['shop_latitude'] = shop['latitude']
            item['shop_longitude'] = shop['longitude']
            item['shop_name'] = shop['name']
            item['shop_description'] = shop['piecewise_agent_fee']['rules'][0]['fee']
            item['shop_sending_price'] = shop['piecewise_agent_fee']['rules'][0]['price']
            item['shop_order_lead_time'] = shop['order_lead_time']
            shop_id = shop['id']
            row = item.Judge_Id()  # 判断商家是否已存在
            if row:
                continue
            item.Save_data()  # 商品保存
            r.set(shop_id, item['shop_id'])
            url = 'https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={}&terminal=web'.format(
                shop_id)  # 商品接口的拼接
            yield scrapy.Request(url, callback=self.food_parse)  # 返回新的商品接口
        url2 = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wkezmjyb91xd&latitude=26.618594&limit=24&longitude=106.752487&offset={}&terminal=web'.format(
            self.offset)  # 新的商铺接口拼接
        yield scrapy.Request(url2, callback=self.parse)  # 返回新的商铺接口
        self.offset += 24

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
                try:
                    item['original_price'] = food['specfoods'][0]['original_price']
                except BaseException as e:
                    item['original_price'] = 0
                if not item['original_price']:
                    item['original_price'] = 0
                item['packing_fee'] = food['specfoods'][0]['packing_fee']
                item['month_sales'] = food['month_sales']
                item['description'] = food['description']
                item['restaurant_id'] = r.get(food['restaurant_id'])
                item.Save_data()
