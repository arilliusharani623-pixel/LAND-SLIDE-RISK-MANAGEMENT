from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    rainfall: float = Field(..., ge=0, le=2000, description="Rainfall in millimetres")
    slope: float = Field(..., ge=0, le=90, description="Slope angle in degrees")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil saturation percentage")
    elevation: float = Field(..., ge=-500, le=9000, description="Elevation in metres")


class PredictionResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    prediction_timestamp: datetime
    model_type: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_type: str
    feature_count: int
    features: list[str]
