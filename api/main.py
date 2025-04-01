from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import os

app = FastAPI()

# Configuração do CORS para permitir requisições de origens específicas
origins = [
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar o arquivo CSV e criar um DataFrame
def carregar_operadoras():
    file_path = "downloads/relatorio_cadop.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Arquivo CSV não encontrado.")
    try:
        df = pd.read_csv(file_path, encoding="utf-8", delimiter=";")
        df.fillna(0, inplace=True)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo CSV: {e}")

df_operadoras = carregar_operadoras()

# Rota para buscar operadoras com base em um texto de busca
@app.get("/buscar-operadoras/")
async def buscar_operadoras(query: str = Query(..., description="Texto para busca nas operadoras")):
    if not query.strip():
        raise HTTPException(status_code=400, detail="O parâmetro 'query' não pode ser vazio.")
    query_lower = query.lower()
    try:
        resultados = df_operadoras[df_operadoras.apply(lambda row: row.astype(str).str.contains(query_lower, case=False).any(), axis=1)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao filtrar os dados: {e}")
    return JSONResponse(content=resultados.head(10).to_dict(orient="records"))
