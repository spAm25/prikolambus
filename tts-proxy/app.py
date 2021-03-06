from fastapi import FastAPI, HTTPException
from hashlib import sha3_512
import logging
import s3
import tts
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logging.basicConfig(filename="tts-proxy.log", encoding="utf-8", level=logging.INFO)
logger = logging.getLogger("fast-api")


origins = ["anekdot.neurals.ro","tts-proxy-api"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TtsRequest(BaseModel):
    text: str


@app.post("/tts")
async def generate_new_sound(body: TtsRequest):
    text_hash = sha3_512(body.text.encode('utf-8')).hexdigest()
    logger.info("Generate audio from text with hash {}".format(text_hash))
    if not s3.is_file_exist(text_hash):
        audio = tts.generate_file(body.text)
        s3.upload_file(audio, text_hash)
    return {'link':s3.get_cloud_file_link(text_hash),
        'hash':text_hash}

@app.get("/tts/{text_hash}")
async def get_sound_url(text_hash: str):
    link = s3.get_cloud_file_link(text_hash)

    if link:
        return {'link':link,
        'hash':text_hash}

    logger.error("File not found")
    raise HTTPException(status_code=404, detail="Item not found")