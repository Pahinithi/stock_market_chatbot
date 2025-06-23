from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    data: Optional[Dict[str, Any]] = None
    success: bool = True
    error: Optional[str] = None

class IndexInfo(BaseModel):
    region: str
    exchange: str
    index: str
    currency: str

class StockData(BaseModel):
    index: str
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: float
    close_usd: Optional[float] = None

class DataSummary(BaseModel):
    total_indices: int
    total_records: int
    date_range: Dict[str, str]
    available_indices: List[str]
