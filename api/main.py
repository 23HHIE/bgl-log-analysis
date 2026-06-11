from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import batch_results, stream

app = FastAPI(title="BGL Log Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(batch_results.router)
app.include_router(stream.router)