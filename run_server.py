from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 既存のフロントエンドURL
        "https://newrepository1.vercel.app"  # 新しいフロントエンドURL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydanticモデルの定義
class RunParams(BaseModel):
    category: str
    start_price: str
    sokketu: str

@app.post("/run")
async def run_script(params: RunParams):
    # pydanticモデルとして受け取ることで、params.category, params.start_price, params.sokketuが使える
    category = params.category
    start_price = params.start_price
    sokketu = params.sokketu

    # Pythonスクリプトを直接呼び出す
    subprocess.run([
        "python", 
        "upload_script.py", 
        category, 
        start_price, 
        sokketu
    ], shell=True)

    return {"status": "ok", "message": "スクリプトを実行しました"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
