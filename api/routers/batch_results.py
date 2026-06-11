import json
import os
from fastapi import APIRouter

router = APIRouter()

RESULTS_PATH = os.environ.get("RESULTS_PATH", "/output/results.json")

@router.get("/results")
def get_batch_results():
    with open(RESULTS_PATH, "r") as f:
        return json.load(f)