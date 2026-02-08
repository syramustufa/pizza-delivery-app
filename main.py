from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Fake DB
pizzas = {}
orders = []
users = {"admin": "123"}   # username: password
sessions = set()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- AUTH ----------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        sessions.add(username)
        return RedirectResponse("/", 303)
    return {"error": "Invalid login"}

# ---------- HOME ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "pizzas": pizzas, "orders": orders}
    )

# ---------- PIZZA CRUD ----------
@app.post("/pizza")
def add_pizza(
    name: str = Form(...),
    price: int = Form(...),
    quantity: int = Form(...)
):
    pizzas[name] = {
        "price": price,
        "quantity": quantity
    }
    return RedirectResponse("/", 303)

@app.put("/pizza")
async def edit_pizza(data: dict):
    name = data["name"]
    if name in pizzas:
        pizzas[name]["price"] = data["price"]
        pizzas[name]["quantity"] = data["quantity"]
        return {"success": True}
    return {"error": "Pizza not found"}

@app.delete("/pizza/{name}")
def delete_pizza(name: str):
    pizzas.pop(name, None)
    return {"success": True}

# ---------- ORDER SYSTEM ----------
@app.post("/order")
async def order_pizza(data: dict):
    name = data["name"]
    qty = data["qty"]

    if name not in pizzas:
        return {"error": "Pizza not found"}

    if pizzas[name]["quantity"] < qty:
        return {"error": "Not enough stock"}

    pizzas[name]["quantity"] -= qty
    orders.append({"pizza": name, "qty": qty})
    return {"success": True}

