from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from canteen_orm import FastFoodInfo
import random
random.seed(a=2,version=2)    

class AbstactFoodList(ABC):
    """
    The FoodList interface declares a set of methods for managing
    food items in the list
    """

    @abstractmethod
    def attachFoodItem(self):
        pass

    @abstractmethod
    def detachFoodItem(self):
        pass

    @abstractmethod
    def notify(self):
        pass

class FastFoodList(AbstactFoodList):
    """
    The fast foodlist class.
    This acts like a tower 🗼 for the objects
    it attaches,deattaches and broadcast data to the observer
    objects(i.e: FastFood object)

    """
    initial=FastFoodInfo.select().count()
    if initial:
        state:int=initial
    else:
        state:int=0
    fastfood_list:List[FastFood]=[]

    def attachFoodItem(self,fooditem:FastFood):

        FastFoodInfo.create(fastfood_id=fooditem.fastfood_id,foodname=fooditem.foodname,price=fooditem.price)
        self.fastfood_list.append(fooditem)
        self.state+=1

    def detachFoodItem(self,fastfood_id:int):
        query=FastFoodInfo.delete().where(FastFoodInfo.fastfood_id==fastfood_id)
        query.execute()
        sync_with_db(self)
        self.state-=1
        
    def notify(self,update:FoodItem)->None:
        for fastfood in self.fastfood_list:
            fastfood.update(self,update)
    

    def get_fastfoods(self):
        return self.fastfood_list

class FoodItem(ABC):
    """
    The Food Item interface declares
    
    """
    @abstractmethod
    def update(self,food:AbstactFoodList):
        pass

class FastFood(FoodItem):
    """
    Fast Food observer class actually,
    This acts like a listener 👂 or subscriber it updates itself
    according to the broadcast data.
    """
    def __init__(self,fastfood_id:int=random.randrange(1,100000),foodname:str=None,price:int=None):
        self.fastfood_id=fastfood_id
        self.foodname=foodname
        self.price=price
        


    def update(self,fastfoodlist:FastFoodList,update:FastFood)->None:
        if self.fastfood_id==update.fastfood_id:
            self.foodname=update.foodname
            self.price=update.price
            q=FastFoodInfo.update({FastFoodInfo.foodname:update.foodname,FastFoodInfo.price:update.price}).where(FastFoodInfo.fastfood_id==update.fastfood_id)
            q.execute()
            print(f"{self.foodname} with {self.fastfood_id} updated")
        if fastfoodlist.state>=10:
            print("List Full")
        
    def __str__(self):
        return f"ID: {self.fastfood_id} FoodName: {self.foodname} price: {self.price}"

def sync_with_db(fastfoods:FastFoodList):
    "A function to sync fastfood class to the database"
    fastfoods.fastfood_list=[FastFood(i.fastfood_id,i.foodname,i.price) for i in FastFoodInfo.select()]   
