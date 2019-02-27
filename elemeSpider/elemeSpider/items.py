# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymysql

db = pymysql.connect('10.102.24.254', 'wuyifa', 'wuyifa1234', 'lifeplus')
cursor = db.cursor()


class ElemespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShopInfoItem(scrapy.Item):
    shop_id = scrapy.Field()
    shop_address = scrapy.Field()
    shop_latitude = scrapy.Field()
    shop_longitude = scrapy.Field()
    shop_name = scrapy.Field()
    shop_description = scrapy.Field()
    shop_sending_price = scrapy.Field()
    shop_order_lead_time = scrapy.Field()

    def Judge_Id(self):
        """
        判断商铺ID是否存在
        """
        print(self['shop_id'])
        row = cursor.execute(
            "SELECT * FROM tb_eleme_shop WHERE shop_id = '{}' limit 1".format(self['shop_id']))
        return row

    def Save_data(self):
        """
        将商铺信息存入数据库
        """
        try:
            print((
                self['shop_id'], self['shop_address'], self['shop_latitude'], self['shop_longitude'], self['shop_name'], self['shop_description']))
            cursor.execute("INSERT INTO tb_eleme_shop (shop_id, address, latitude, longitude, shop_name, description, uptosend_price, order_lead_time) VALUES ('{}','{}','{}','{}','{}', '{}', '{}', '{}')".format(
                self['shop_id'], self['shop_address'], self['shop_latitude'], self['shop_longitude'], self['shop_name'], self['shop_description'], self['shop_sending_price'], self['shop_order_lead_time']))
            db.commit()
        except BaseException as e:
            print(e)
        return


class FoodInfoItem(scrapy.Item):
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    food_name = scrapy.Field()
    food_price = scrapy.Field()
    food_id = scrapy.Field()
    original_price = scrapy.Field()
    packing_fee = scrapy.Field()
    month_sales = scrapy.Field()
    description = scrapy.Field()
    restaurant_id = scrapy.Field()

    def Judge_Id(self):
        """
        判断商品ID是否存在
        """
        row = cursor.execute(
            "SELECT * FROM tb_eleme_food WHERE food_id = '{}' limit 1".format(self['food_id']))
        return row

    def Save_data(self):
        """
        将商品信息存入数据库
        """
        try:
            print((
                self['food_id'], self['food_name'], self['category_id'], self['category_name'], self['food_price'], self['original_price'], self['packing_fee'], self['month_sales'], self['description'], self['restaurant_id']))
            cursor.execute("INSERT INTO tb_eleme_food (food_id, food_name, category_id, category_name, food_price, original_price, packing_fee, month_sales, description, restaurant_id) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                self['food_id'], self['food_name'], self['category_id'], self['category_name'], self['food_price'], self['original_price'], self['packing_fee'], self['month_sales'], self['description'], self['restaurant_id']))
            db.commit()
        except BaseException as e:
            print(e)
        return