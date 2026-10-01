from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI()

# Unga Firebase Database Link (kadaisila .json irukkanum)
FIREBASE_URL = "https://college-bus-tracker-87ca3-default-rtdb.firebaseio.com/locations.json"

async def send_to_firebase(payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(FIREBASE_URL, json=payload)

@app.get("/track")
async def track_bus(id: str = None, lat: float = None, lon: float = None, background_tasks: BackgroundTasks = None):
    # Traccar app la irundhu varum data
    if lat and lon:
        payload = {
            "bus_id": id,  # Idhu driver phone oda Device Identifier
            "latitude": lat,
            "longitude": lon
        }
        # Background la Firebase ku send panrom, appo thaan app ku fast ah response pogum
        background_tasks.add_task(send_to_firebase, payload)
        
    return {"status": "success"}