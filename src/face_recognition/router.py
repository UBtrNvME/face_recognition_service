from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@router.get("/find_similar", response_class=HTMLResponse)
async def find_simiar(request: Request):
    return templates.TemplateResponse("find_similar.html", {"request": request})
