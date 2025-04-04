# ML Model Performance Dashboard

A dashboard for tracking machine learning model performance over time.

## Features

- Upload ML models with their associated files
- Automatic model evaluation
- Performance tracking and visualization
- Metadata storage
- HTMX-powered interface with minimal JavaScript
- Async backend operations

## Requirements

All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Install dependencies
2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open http://localhost:8000 in your browser

## Model Upload Requirements

- Each uploaded model must include a `main.py` file
- The `main.py` file must contain a function with the signature:
  ```python
  def main(training_data: pandas.DataFrame) -> Any
  ```
- The function should return the trained model object

## Project Structure

- `main.py`: FastAPI application and routes
- `models.py`: SQLAlchemy database models
- `database.py`: Database configuration
- `templates/`: HTML templates
- `static/`: CSS and other static files
- `uploaded_models/`: Directory where uploaded models are stored
