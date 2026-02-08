from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# In-memory database
db = {}

class Pizza(BaseModel):
    name: str
    desc: str

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Home page (HTML)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "pizzas": db}
    )

# Create pizza
@app.post("/pizza")
def create_pizza(pizza: Pizza):
    db[pizza.name] = pizza.desc
    return {"message": "Pizza added", "data": db}

# Get all pizzas
@app.get("/pizza")
def get_all_pizzas():
    return db

# Update pizza
@app.put("/pizza")
def update_pizza(pizza: Pizza):
    db[pizza.name] = pizza.desc
    return {"message": "Pizza updated", "data": db}

# Delete pizza
@app.delete("/pizza")
def delete_pizza(name: str):
    if name in db:
        del db[name]
        return {"message": "Pizza deleted", "data": db}
    return {"error": "Pizza not found"}
