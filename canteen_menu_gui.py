from flask import Flask,render_template,request
from canteen_menu_api import FastFoodList, sync_with_db,FastFood
import time
import random

random.seed(a=int(time.time()),version=2) 
app = Flask(__name__)

def read():
    fastfood_data=FastFoodList()
    sync_with_db(fastfood_data)
    return fastfood_data

def create(fastfood:FastFood,fastfood_data:FastFoodList):
    fastfood_id=random.randrange(1,10000000)
    fastfood_data.attachFoodItem(fooditem=FastFood(fastfood_id=fastfood_id,foodname=fastfood.foodname,price=fastfood.price))
    sync_with_db(fastfood_data)

def update(fastfood:FastFood,fastfood_data:FastFoodList):
    fastfood_data.notify(fastfood)
    sync_with_db(fastfood_data)

def delete(fastfood_id:int,fastfood_data:FastFoodList):
    fastfood_data.detachFoodItem(fastfood_id)
    sync_with_db(fastfood_data)
@app.route("/")
def home():
    fastfoods=read()
    return render_template('home.html',fastfoods=fastfoods.fastfood_list)

@app.route("/create",methods=["GET", "POST"])
def create_food_item():
    
    fastfoods=read()
    
    if request.method == "POST":
        foodname=request.form["foodname"]
        price=request.form["price"]
        try:
            foodname=str(foodname)
            price=int(price)
            if foodname and price:
                create(FastFood(foodname=foodname,price=price),fastfoods)
            else:
                print("Invalid data")
        except Exception as e:
            print(f"Invalid {e}")
            
        finally:
            sync_with_db(fastfoods)
            return render_template('create.html',fastfoods=fastfoods.fastfood_list)
    
    else:
        return render_template('create.html',fastfoods=fastfoods.fastfood_list)


@app.route("/delete",methods=["GET", "POST"])
def delete_food():
    fastfoods=read()
    
    if request.method == "POST":
        fastfood_id=request.form["fastfood_id"]
        
        try:
            delete(fastfood_id,fastfoods)
        except Exception as e:
            print(f"Invalid {e}")
            
        finally:
            sync_with_db(fastfoods)
            return render_template('delete.html',fastfoods=fastfoods.fastfood_list)
    else:
        return render_template('delete.html',fastfoods=fastfoods.fastfood_list)

@app.route("/update",methods=["GET", "POST"])
def update_food():
    fastfoods=read()
    
    if request.method == "POST":
        
        try:
            fastfood_id=int(request.form["fastfood_id"])
            fastfood_name=str(request.form["fastfood_name"])
            fastfood_price=int(request.form["fastfood_price"])
            updated_food_description=FastFood(fastfood_id=fastfood_id,foodname=fastfood_name,price=fastfood_price)
            print(updated_food_description.fastfood_id)
            update(updated_food_description,fastfoods)
        except Exception as e:
            print(f"Invalid {e}")
            
        finally:
            sync_with_db(fastfoods)
            return render_template('update.html',fastfoods=fastfoods.fastfood_list)
    else:
        return render_template('update.html',fastfoods=fastfoods.fastfood_list)  

if __name__ =="__main__":
    app.run(debug=True,port=8080)