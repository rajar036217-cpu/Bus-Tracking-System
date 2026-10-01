from fastapi import FastAPI, BackgroundTasks, Request
import httpx

app = FastAPI()

FIREBASE_URL = "https://college-bus-tracker-87ca3-default-rtdb.firebaseio.com/locations.json"

async def send_to_firebase(payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(FIREBASE_URL, json=payload)

@app.api_route("/track", methods=["GET", "POST"])
async def track_bus(request: Request, background_tasks: BackgroundTasks, id: str = None, lat: float = None, lon: float = None):
    # Traccar sometimes URL vazhiya anuppum
    if id and lat and lon:
        payload = {"bus_id": id, "latitude": lat, "longitude": lon}
        background_tasks.add_task(send_to_firebase, payload)
        return {"status": "success from URL params"}
        
    # Traccar POST vazhiya JSON anuppumbodhu idhu work aagum
    try:
        # Request kulla varum JSON-ah padikirom
        if request.method == "POST":
            # Form data illana raw text vaanga:
            body_bytes = await request.body()
            import urllib.parse
            import json
            
            # Traccar sila neram form encoded aaga anuppum
            parsed_data = urllib.parse.parse_qs(body_bytes.decode('utf-8'))
            
            if 'lat' in parsed_data and 'lon' in parsed_data:
                lat_val = float(parsed_data['lat'][0])
                lon_val = float(parsed_data['lon'][0])
                bus_id = parsed_data.get('id', ['unknown'])[0]
                
                payload = {"bus_id": bus_id, "latitude": lat_val, "longitude": lon_val}
                background_tasks.add_task(send_to_firebase, payload)
                return {"status": "success from Form data"}
                
    except Exception as e:
        print(f"Error parsing data: {e}")
        pass
        
    return {"status": "received but no valid location data found"}