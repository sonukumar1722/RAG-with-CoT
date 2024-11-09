from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_text()
            
            # Process the message (Here’s a placeholder response)
            response = f"Received: {data}"
            print(response)
            
            # Send a response back to frontend
            await websocket.send_text(json.dumps({"response": response}))
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
