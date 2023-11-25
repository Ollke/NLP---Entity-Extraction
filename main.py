import os
import string
import spacy
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from spacy.lang.en.stop_words import STOP_WORDS

app = FastAPI()

# Carregua os modelos de idioma
nlp_en = spacy.load("en_core_web_sm")
nlp_pt = spacy.load("pt_core_news_sm")


# Modelo de dados Pydantic para a entrada JSON
class JSONRequest(BaseModel):
    text: str
    model: str = "en"
    preprocessing: bool = False

@app.post("/")
async def root(jsonBase: JSONRequest):
    text = jsonBase.text

    if(jsonBase.preprocessing):
        r = requests.post("https://preprocessing-k6ozgp36va-uc.a.run.app", json={
            "text": text,
            "model": jsonBase.model,
            "remove_special_chars": True,
            "lemmatize": True,
            "remove_stopwords": True
        })
        
        if(r.status_code == 200):
            text = r.json()["response"]
        else:
            raise HTTPException(status_code=r.status_code)
        

    # Carregue o modelo de idioma
    if(jsonBase.model.lower() == "en"):
        doc = nlp_en(text)
    elif(jsonBase.model.lower() == "pt"):
        doc = nlp_pt(text)
    else:
        raise HTTPException(status_code=406, detail="Model not found")
    
    entitys = []
    for entity in doc.ents:
        entitys.append({"entidade":entity.text,"categoria":entity.label_})

    return JSONResponse(content={
        "text": jsonBase.text,
        "model": jsonBase.model,
        "response": entitys
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
