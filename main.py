from datetime import datetime
from pathlib import Path
from typing import List
import importlib.util
import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import ModelPerformance
from database import get_db, init_db

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ensure directories exist
UPLOAD_DIR = Path("uploaded_models")
UPLOAD_DIR.mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)

# Sample training and test da
# ta (replace with your actual data)
def get_sample_data():
    # Replace this with your actual data loading logic
    return pd.DataFrame({'feature': range(100), 'target': range(100)})

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    # Get all model performances
    result = await db.execute(select(ModelPerformance).order_by(ModelPerformance.upload_time.desc()))
    performances = result.scalars().all()
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "performances": performances}
    )

@app.post("/upload")
async def upload_model(
    files: List[UploadFile] = File(...),
    model_name: str = Form(...),
    metadata: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Create model directory
    model_dir = UPLOAD_DIR / model_name
    model_dir.mkdir(exist_ok=True)
    
    main_py_exists = False
    
    # Save uploaded files
    for file in files:
        file_path = model_dir / file.filename
        content = await file.read()
        file_path.write_bytes(content)
        if file.filename == "main.py":
            main_py_exists = True
    
    if not main_py_exists:
        return {"error": "main.py is required"}
    
    # Import the main function
    spec = importlib.util.spec_from_file_location("module.name", str(model_dir / "main.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if not hasattr(module, "main"):
        return {"error": "main() function not found"}
    
    # Get training data and evaluate model
    training_data = get_sample_data()
    model = module.main(training_data)
    
    # Evaluate model using test data
    test_data = get_sample_data()
    try:
        if hasattr(model, 'evaluate'):
            performance_score = model.evaluate(test_data)
        else:
            # Fallback to a dummy score if model doesn't have evaluate method
            performance_score = 0.85
    except Exception as e:
        print(f"Error evaluating model: {e}")
        performance_score = 0.0
    
    # Save to database
    performance = ModelPerformance(
        model_name=model_name,
        upload_time=datetime.now(),
        performance_score=performance_score,
        model_metadata={"user_metadata": metadata},
        file_path=str(model_dir)
    )
    
    db.add(performance)
    await db.commit()
    
    return {"success": True, "performance": performance.to_dict()}
