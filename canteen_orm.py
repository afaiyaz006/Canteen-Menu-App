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
print(FastFoodInfo.select().order_by(FastFoodInfo.id.desc()).get().id)