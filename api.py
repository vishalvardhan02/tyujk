from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import gunicorn

df = pd.read_csv("Water_quality.csv")

params = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity']
filled = []

class model(BaseModel):
    ph: str
    Hardness: str
    Solids: str
    Chloramines: str
    Sulfate: str
    Conductivity: str
    Organic_carbon: str
    Trihalomethanes: str
    Turbidity: str

app = FastAPI()

@app.get("/")
def homeFunction():
    return "Hello"

@app.post("/Auto_fill")
def autoFill(parameters: model):
    random_fill = 1
    upper = {"ph":2, "Hardness":10, "Solids":10000, "Chloramines":2, "Sulfate":10, "Conductivity":10,"Organic_carbon":3, "Trihalomethanes":10, "Turbidity":2}
    x = {"ph":parameters.ph, "Hardness":parameters.Hardness, "Solids":parameters.Solids, "Chloramines":parameters.Chloramines, "Sulfate": parameters.Sulfate, "Conductivity":parameters.Conductivity, "Organic_carbon":parameters.Organic_carbon, "Trihalomethanes":parameters.Organic_carbon, "Turbidity":parameters.Turbidity}
    for i in params:
        if(x[i]!=""):
            filled.append(i)
            random_fill = 0
    if(random_fill==1):
        random = dict()
        dft = df.sample(1)
        for i in dft:
            random[i] = float(dft[i].values[0])
        cv = {}
        cv['output'] = random
        return cv
    else:
        final_df = df
        final_df = final_df.drop("Potability", axis=1)
        for i in filled:
            if(x[i]==""):
                continue
            value = round(float(x[i]))-1
            if(value>10):
                while(value%10!=0):
                    value -=value%10
            if(value>1000):
                while(value%1000!=0):
                    value -=value%1000
            final_df = final_df[(final_df[i]>=value) & (final_df[i]<value+upper[i])]
        random = list(final_df.values)
        out = {}
        for i in range(len(random)):
            out[i] = list(random[i])
        c = {}
        c['output'] = out
        return c
