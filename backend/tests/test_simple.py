"""Test simple para verificar que FastAPI funciona."""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI está funcionando"}

@app.get("/test")
def test():
    return {"status": "ok", "backend": "Python FastAPI"}

if __name__ == "__main__":
    print("🚀 Iniciando servidor de prueba en puerto 8001...")
    print("📍 Abre: http://localhost:8001/")
    print("📍 Abre: http://localhost:8001/test")
    uvicorn.run(app, host="0.0.0.0", port=8001)

