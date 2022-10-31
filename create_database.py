from peewee import *
import datetime


db = SqliteDatabase('canteen_database.db')

class FastFoodInfo(Model):
    fastfood_id=IntegerField()
    foodname=CharField()
    price=IntegerField()

    class Meta:
        database=db


db.connect()
db.create_tables([FastFoodInfo])
FastFoodInfo.create(fastfood_id=0,foodname="test",price=0)