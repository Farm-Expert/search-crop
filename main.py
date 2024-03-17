from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

import search_crop as sc
import crop_json as cj

df=pd.read_csv("crop.csv")
df['Sno'] = np.arange(len(df))

class Item1(BaseModel):
    search: str


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

