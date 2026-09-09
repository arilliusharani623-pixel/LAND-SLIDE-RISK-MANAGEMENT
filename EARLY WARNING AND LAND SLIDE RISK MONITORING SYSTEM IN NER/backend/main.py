import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .model_loader import ModelLoadError, load_model, model_features
from .predictor import PredictionError, predict_risk
from .schemas import HealthResponse, ModelInfoResponse, PredictionRequest, PredictionResponse

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.model = load_model(settings.model_path)
        app.state.model_error = None
    except ModelLoadError as exc:
        app.state.model = None
        app.state.model_error = str(exc)
        logger.error("Application started without a model: %s", exc)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error while processing %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def require_model() -> Any:
    if app.state.model is None:
        raise HTTPException(status_code=503, detail=app.state.model_error or "Model is unavailable")
    return app.state.model


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_name}


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="healthy" if app.state.model is not None else "degraded", model_loaded=app.state.model is not None)


@app.get("/model-info", response_model=ModelInfoResponse)
async def model_info() -> ModelInfoResponse:
    model = require_model()
    features = model_features(model)
    return ModelInfoResponse(model_type=type(model).__name__, feature_count=len(features), features=features)


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    model = require_model()
    try:
        score, level = predict_risk(model, request.model_dump())
    except PredictionError as exc:
        logger.warning("Prediction rejected: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return PredictionResponse(risk_score=score, risk_level=level, prediction_timestamp=datetime.now(timezone.utc), model_type=type(model).__name__)
