from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import utils as lock_storage  # Handles reading/writing JSON

router = APIRouter()

# Load lock states from file on startup
lock_states: Dict[str, int] = lock_storage.load_lock_states()

@router.websocket("/{username}/lock/locking")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    lock_states.setdefault(username, 0)
    lock_storage.save_lock_states(lock_states)

    try:
        while True:
            data = await websocket.receive_text()
            cleaned = data.strip()

            if cleaned in ["0", "1"]:
                lock_states[username] = int(cleaned)
                lock_storage.save_lock_states(lock_states)
                status = "LOCKED" if cleaned == "1" else "UNLOCKED"
                await websocket.send_text(f"Lock state changed to: {status}")
            elif cleaned == "status":
                state = lock_states[username]
                status = "LOCKED" if state == 1 else "UNLOCKED"
                await websocket.send_text(f"Current state is: {status} ({state})")
            else:
                await websocket.send_text("Invalid command. Use '0' to unlock, '1' to lock, or 'status'.")
    except WebSocketDisconnect:
        print(f"Client '{username}' disconnected")

@router.websocket("/{username}/lock/status")
async def websocket_status(websocket: WebSocket, username: str):
    await websocket.accept()
    lock_states.setdefault(username, 0)

    try:
        # Send current state once and close (stateless request-style)
        state = lock_states[username]
        status = "LOCKED" if state == 1 else "UNLOCKED"
        await websocket.send_text(f"{state}")
    except WebSocketDisconnect:
        print(f"Status check client '{username}' disconnected")
