from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI()

FIREBASE_URL = "https://college-bus-tracker-87ca3-default-rtdb.firebaseio.com/locations.json"

async def send_to_firebase(payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(FIREBASE_URL, json=payload)

# GET and POST rendu method-um accept panra mathiri mathiyachu
@app.api_route("/track", methods=["GET", "POST"])
async def track_bus(id: str = None, lat: float = None, lon: float = None, background_tasks: BackgroundTasks = None):
    if lat and lon:
        payload = {
            "bus_id": id,
            "latitude": lat,
            "longitude": lon
        }
        background_tasks.add_task(send_to_firebase, payload)
        
    return {"status": "success"}