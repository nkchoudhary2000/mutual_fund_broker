from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api import auth, mutual_fund, portfolio
from app.db.session import Base, engine
from app.services.nav_updater import start_nav_scheduler

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Mount static files (optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template directory
templates = Jinja2Templates(directory="templates")

# Start scheduler
start_nav_scheduler()

# Serve login page
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Serve register page
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/mutual-funds", response_class=HTMLResponse)
async def mutual_funds_page(request: Request):
    return templates.TemplateResponse("mutual_funds.html", {"request": request})

# Routers for backend logic
app.include_router(auth.router)
app.include_router(mutual_fund.router)
app.include_router(portfolio.router)
