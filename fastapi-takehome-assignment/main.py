from fastapi import FastAPI
from uuid import uuid4
from pydantic import BaseModel,Field
from fastapi import HTTPException,status
from fastapi import Query
from fastapi import Header 
from fastapi.middleware.cors import CORSMiddleware

import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
API_KEY=os.getenv("API_KEY" ,"dev-secret-key")  #set the api key as dev-secret-key


#make a if statemnt to show http status code when key is missing or not crrect 
def check_api_key(x_api_key:str|None):
  if x_api_key is None:
      raise HTTPException(status_code=401,detail="Missing API key")
  if x_api_key != API_KEY:
      raise HTTPException(status_code=403,detail="Invalid API key")
  

#creating/defining  product schema :validation rules 
class CosmeticCreate(BaseModel): #this is what one needs to fil to create a cosmetic 
    name:str =Field(...,min_length=1, max_length=100) 
    brand:str =Field(...,min_length=1, max_length=100)
    price:float =Field(...,gt=0)
    quantity:int =Field(...,ge=0)

class Cosmetic(CosmeticCreate): #this is what exists in the database 
     id:str

#in memory database 
cosmetic_db:dict[str,Cosmetic]={}

#seed sample data=put sample data in database 
def seed():
     samples =[
          CosmeticCreate(name="Matte lipstick",
                         brand="Fenty",
                         price=150.0,
                         quantity=10),
          CosmeticCreate(name="Setting Spray",
                         brand="Kiss Beauty",
                         price=250.0,
                         quantity=5),
          CosmeticCreate(name="Foundation",
                         brand="Mabyeline",
                         price=200.0,
                         quantity=15),    
          CosmeticCreate(name="Liquid Blush", brand="Rhode", price=180.0, quantity=12),
            CosmeticCreate(name="Brow Gel", brand="Glossier", price=95.0, quantity=20),
            CosmeticCreate(name="Highlighter Palette", brand="Fenty", price=220.0, quantity=8),
            CosmeticCreate(name="Lip Oil", brand="Rhode", price=140.0, quantity=30),
            CosmeticCreate(name="Concealer", brand="NARS", price=175.0, quantity=18),
            CosmeticCreate(name="Eyeshadow Palette", brand="Huda Beauty", price=350.0, quantity=6),
            CosmeticCreate(name="Mascara", brand="Maybelline", price=85.0, quantity=45),
            CosmeticCreate(name="Setting Powder", brand="Laura Mercier", price=210.0, quantity=14),
            CosmeticCreate(name="Cream Bronzer", brand="Fenty", price=195.0, quantity=10),
            CosmeticCreate(name="Lip Liner", brand="MAC", price=65.0, quantity=25),
            CosmeticCreate(name="Setting Spray", brand="Urban Decay", price=230.0, quantity=9),
            CosmeticCreate(name="Eyeliner Pen", brand="Kiss Beauty", price=70.0, quantity=33),
            CosmeticCreate(name="Contour Stick", brand="NARS", price=160.0, quantity=11),
            CosmeticCreate(name="Lash Serum", brand="Grande Cosmetics", price=280.0, quantity=7),
            CosmeticCreate(name="Face Primer", brand="Milk Makeup", price=190.0, quantity=16),
            CosmeticCreate(name="Cheek Tint", brand="Rhode", price=155.0, quantity=22),
            CosmeticCreate(name="Setting Powder Duo", brand="Mabyeline", price=110.0, quantity=19),
     ]
     for s in samples:
       cid =str(uuid4()) #generates a uique id for every cosmetic
       cosmetic_db[cid] =Cosmetic(id=cid,**s.model_dump())

seed()

@app.get("/")
def root():
     return {"status": "ok"}

#error handling show 404 if cosmetic not found 
@app.get("/cosmetics/{cosmetic_id}")
def get_cosmetic(cosmetic_id: str):
    cosmetic = cosmetic_db.get(cosmetic_id)
    if cosmetic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cosmetic '{cosmetic_id}' not found."
        )
    return cosmetic

#get comstics with pagination
@app.get("/cosmetics")
def list_cosmetics(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    items = list(cosmetic_db.values())

    start = (page - 1) * page_size
    end = start + page_size

    paginated_items = items[start:end]
    total = len(items)
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
 

#post cosmetic will work only with correct api key
@app.post("/cosmetics", status_code=201)
def create_cosmetic(
    payload: CosmeticCreate,
    x_api_key: str | None = Header(default=None)
):
    check_api_key(x_api_key)

    cid = str(uuid4())
    cosmetic = Cosmetic(id=cid, **payload.model_dump())
    cosmetic_db[cid] = cosmetic
    return cosmetic

#delete cosmetic only with matching api key 
@app.delete("/cosmetics/{cosmetic_id}", status_code=204)
def delete_cosmetic(
    cosmetic_id: str,
    x_api_key: str | None = Header(default=None)
):
    check_api_key(x_api_key)

    if cosmetic_id not in cosmetic_db:
        raise HTTPException(status_code=404, detail=f"Cosmetic '{cosmetic_id}' not found.")

    del cosmetic_db[cosmetic_id]
    return None