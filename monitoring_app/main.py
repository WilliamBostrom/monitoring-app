from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from menus.menu import get_main_menu, handle_menu_choice
from alarms.alarm_manager import alarm_manager
from alarms.alarm import Alarm
from menus.larm_menu import create_alarm



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

@app.get("/menu")
def get_menu():
  return {"options": get_main_menu()}

@app.post("/set_alarm/{choice}")
async def handle_menu(choice: int, request: Request):
    data = await request.json()
    result = handle_menu_choice(choice, frontend=True, data=data)
    return result

@app.post("/select")
async def select_option(request: Request):
  try:
    data = await request.json()
    choice = data.get("choice")
    if choice is None:
      return {"error": "choice parameter missing"}
    result = handle_menu_choice(choice, frontend=True)
    return {"result": result}
  except Exception as e:
    return {"error": str(e)}

@app.get("/alarms")
def get_alarms():
  return {"alarms": alarm_manager.get_alarms()}

@app.post("/alarms")
async def create_alarm_endpoint(request: Request):
  data = await request.json()
  alarm_type = data.get("type")
  threshold = data.get("threshold")
  if not alarm_type or not threshold:
    return {"error": "Både type och threshold krävs"}
  
  new_alarm = create_alarm(alarm_type=alarm_type, threshold=threshold, frontend=True)
  if new_alarm:
    return alarm_manager.add_alarm(new_alarm)
  return {"error": "ogiltig data"}

@app.delete("/alarms/{alarm_id}")
def delete_alarm(alarm_id):
  try:
    alarm_id_int = int(alarm_id)
    success = alarm_manager.remove_alarm(alarm_id_int)
    if success:
      return {"message": "Alarm borttaget"}
    return {"error": "Alarm inte funnet"}
  except ValueError:
    return {"error": "Ogiltigt alarm ID"}

@app.get("/alarms/status")
def get_status_alarm():
  triggered = alarm_manager.check_alarms()
  return {
      "triggered_alarms": triggered,
      "total_alarms": len(alarm_manager.alarms),
      "monitoring_active": alarm_manager.monitoring_active
  }

@app.post("/alarms/monitoring/start")
def start_alarm_monitoring():
    alarm_manager.start_monitoring()
    return {"message": "Alarm monitoring startad"}

@app.post("/alarms/monitoring/stop")
def stop_alarm_monitoring():
    alarm_manager.stop_monitoring()
    return {"message": "Alarm monitoring stoppad"}

if __name__ == "__main__":
  from menus.menu import menu
  menu()

