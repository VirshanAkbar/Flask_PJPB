from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

app = FastAPI()

user_list = ["Adhy", "Rayhan", "Wimpi", "Virshan", "oye123"]  # Available users (no auth)
lock_state = 0  # 0 = unlocked, 1 = locked

@app.get("/", response_class=HTMLResponse)
async def index():
    return "<h1> Hapunten, Euweuh Website! </h1>"

@app.get("/{username}/lock")
async def get_lock_state(username: str):
    if username in user_list:
        return PlainTextResponse(str(lock_state))
    else:
        return PlainTextResponse("User Not Found!", status_code=404)

@app.get("/{username}/lock/status")
@app.post("/{username}/lock/status")
async def status_lock(username: str):
    if username in user_list:
        if lock_state == 1:
            return PlainTextResponse("1")
        elif lock_state == 0:
            return PlainTextResponse("0")
        else:
            return PlainTextResponse("Ngawur!", status_code=400)
    else:
        return PlainTextResponse("User Not Found!", status_code=404)

@app.get("/{username}/lock/locking")
@app.post("/{username}/lock/locking")
async def lock(username: str, state: str = Form(None)):
    global lock_state
    if username not in user_list:
        return PlainTextResponse("Ngawur!!", status_code=404)

    if state is not None:
        if state not in ['0', '1']:
            return JSONResponse({"error": "Invalid state, use 0 for unlock or 1 for lock"}, status_code=400)

        lock_state = int(state)
        print(f"Lock is now {'LOCKED' if lock_state else 'UNLOCKED'}")
        return JSONResponse({"status": f"Lock is now {'LOCKED' if lock_state else 'UNLOCKED'}"}, status_code=200)

    return JSONResponse({"state": lock_state})
