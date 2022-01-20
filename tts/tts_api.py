from fastapi import FastAPI
import uvicorn
import os
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/tts")
async def tts(text):
    os.system(f'tts --text "{text}"')
    print(f'tts --text "{text}"')
    return FileResponse("tts_output.wav")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)