from fastapi import FastAPI, HTTPException
from sockets import router as socket_router
import utils as lock_storage  # Import the same module used in sockets.py

app = FastAPI()

# Include the WebSocket router
app.include_router(socket_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Lock Control API"}

@app.get("/{username}/lock")
async def get_lock_state(username: str):
    lock_states = lock_storage.load_lock_states()

    if username in lock_states:
        state = lock_states[username]
        # status = "LOCKED" if state == 1 else "UNLOCKED"
        # return {"username": username, "state": state, "status": status}
        status = "lock" if state == 1 else "unlock"
        return status
    else:
        raise HTTPException(status_code=404, detail="User not found")

