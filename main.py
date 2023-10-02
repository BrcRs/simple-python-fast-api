from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI() # similar to Flask


# let's create an endpoint, a point of entry in a communication channel when 
# two systems are interacting. It refers to touchpoints of the com. between an 
# API and a server.
# Ex: /hello, /get-item
# In localhost/hello, the base url is localhost, and the endpoint /hello

# run with uvicorn main:app --reload
# --reload will make the server reload the web app whenever there is a change

# by going to /docs you will notice automatically generated documentation, which is a feature of FASTAPI
# + it allows to test the API

# @app.get("/")
# def home():
#     return {"Data": "Test"}

# @app.get("/about")
# def about():
#     return {"data": "About"}

inventory = {
    # 1: {
    #     "name": "Milk",
    #     "price": 3.99,
    #     "brand": "Regular"
    # }
}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the item you would like to view", ge=1, lt=4)): # Path(etc) allows to add constraints on arguments
    return inventory[item_id]

# the query parameter
# e.g.: facebok.com/home?redirect=tim&msg=fail

@app.get("/get-by-name")
def get_item(name: str = Query(None, title="Name", description="Name of item.")): # by default a query parameter if not seen in route
# when default paramter is given the argument is no longer mandatory
    for item_id in inventory:
        # if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not Found"}
    # raise HTTPException(status_code=404)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    # let's insert an item into the inventory
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item already exists")
    
    # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    inventory[item_id] = item # works directly
    return inventory[item_id]

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    # let's insert an item into the inventory
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")
    
    # inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    if item.name != None:
        inventory[item_id].name = item.name 
    if item.price != None:
        inventory[item_id].price = item.price 
    if item.brand != None:
        inventory[item_id].brand = item.brand 

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")
    
    del inventory[item_id]
    return {"Success": "Item deleted"}