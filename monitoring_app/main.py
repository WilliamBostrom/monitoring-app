from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from menus.menu import get_main_menu, handle_menu_choice

"""
För starta webbserver
 uvicorn main:app --reload

 pyenv shell 3.12.11

 """
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

class MenuChoice(BaseModel):
  choice: int
  type: str | None = None 
  threshold: int | None = None 


@app.get("/menu")
def get_menu():
  return {"options": get_main_menu()}

@app.post("/set_alarm/{choice}")
async def handle_menu(choice: int, request: Request):
    data = await request.json()
    result = handle_menu_choice(choice, frontend=True, data=data)
    return result

@app.post("/select")
def select_option(data: MenuChoice):
  return {"result": handle_menu_choice(data.choice, frontend=True)}

if __name__ == "__main__":
  from menus.menu import menu
  menu()

