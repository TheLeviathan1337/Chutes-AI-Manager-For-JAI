from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
from helper import Helper

app = FastAPI()

load_dotenv()

PORT_NUMBER = os.getenv('PORT_NUMBER')
CHUTES_API_KEY = os.getenv('CHUTES_API_KEY')

Helper.load_model_configs()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/proxy/random")
async def proxy_random(request: Request):
    body = await request.json()

    stream_generator = await Helper.process_request(body, CHUTES_API_KEY, "Random")

    return StreamingResponse(
        stream_generator,
        media_type="text/event-stream"
    )

@app.post("/proxy/ordered")
async def proxy_sequential(request: Request):
    body = await request.json()

    stream_generator = await Helper.process_request(body, CHUTES_API_KEY, "Ordered")

    return StreamingResponse(
        stream_generator,
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(PORT_NUMBER))