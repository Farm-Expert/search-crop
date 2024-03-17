from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

import search_crop as sc
import crop_json as cj
genai.configure(api_key="AIzaSyBDqOhWlvNqG9Crmb7Ip01vNYtMSHKtx1A")


df=pd.read_csv("crop.csv")
df['Sno'] = np.arange(len(df))

model=genai.GenerativeModel("gemini-pro")

history=[]
chat=model.start_chat(history=history)

chat.send_message("your name is Agro Expert.I want you to respond to my every question under 20 words. Give answers related to agriculture farming or crops. I will not accept answers that are not related to these guide")

def read(message):
    res=""
    for chunk in message:
        chunk.text.replace('*',"")
        print(chunk.text)
        res=res+chunk.text
    res.replace('*',"")
    return {"res":res}

def chatting(text):
    try:
        print(f"inside try {text}")
        res=chat.send_message(F"tell me {text} in strictly under 20 words. Give answers related to farming, agriculture or crops. if not conformed, then give approximate answers. Avoide using * in your response",generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        stop_sequences=['space'],
        max_output_tokens=200,
        temperature=0.4))
        return read(res)
    except:
        print(text)
        return {"Error": "I am not able to understand your question. Please ask again."}


class Item1(BaseModel):
    search: str

class TextMessages(BaseModel):
    message:str


app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def first():
    return("successfully loaded")

@app.post("/search_crop")
async def create_item(item: Item1):
    crop=item.search
    p=sc.search(crop)
    if p==-1:
        json_compatible_item_data = jsonable_encoder({"status":"fail"})
        return JSONResponse(content=json_compatible_item_data)
    k=df[df['label']==p[0]]['Sno'].values[0]
    crop_detail=[]
    crop_img=[]
    crop_name=[]
    pi=[]
    for i in range(4):
        crop_detail.append(cj.find(p[i]))
        crop_img.append(crop_detail[i]["img"])
        crop_name.append(crop_detail[i]["name"].upper())
    crop_desc=crop_detail[0]["desc"]
    pi=df[df['Sno']==k].values[0].tolist()
    re={"crop":pi, "ci":crop_img, "cn":crop_name, "cd":crop_desc,"status":"success"}
    json_compatible_item_data = jsonable_encoder(re)
    return JSONResponse(content=json_compatible_item_data)

@app.post('/chat')
def sendtext(mes:TextMessages):
    return chatting(mes.message)