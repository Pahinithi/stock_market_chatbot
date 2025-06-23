from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any

# Import local modules
from app.utlits.schemas import ChatRequest, ChatResponse, IndexInfo, StockData, DataSummary
from app.utlits.functions import (
    load_csv_data, 
    get_data_summary, 
    process_chat_message,
    get_stock_data_by_index,
    get_index_info_by_region,
    query_gemini
)

# Initialize FastAPI app
app = FastAPI(
    title="Stock Market Chatbot API",
    description="A chatbot API for stock market data analysis using Gemini AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Stock Market Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "data_summary": "/data/summary",
            "indices": "/indices",
            "stock_data": "/stock-data/{index_symbol}",
            "region_indices": "/indices/region/{region}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user messages using Gemini AI
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Process the chat message
        result = process_chat_message(request.message)
        
        return ChatResponse(
            response=result["response"],
            data=result.get("data"),
            success=result["success"],
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/data/summary", response_model=DataSummary)
async def get_data_summary_endpoint():
    """
    Get summary statistics of the available data
    """
    try:
        summary = get_data_summary()
        if summary is None:
            raise HTTPException(status_code=500, detail="Failed to get data summary")
        
        return DataSummary(**summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting data summary: {str(e)}")

@app.get("/indices", response_model=List[IndexInfo])
async def get_all_indices():
    """
    Get information about all available stock market indices
    """
    try:
        data = load_csv_data()
        if data is None or "index_info" not in data:
            raise HTTPException(status_code=500, detail="Failed to load index data")
        
        return [IndexInfo(**index) for index in data["index_info"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting indices: {str(e)}")

@app.get("/stock-data/{index_symbol}", response_model=List[StockData])
async def get_stock_data(index_symbol: str, limit: int = 10):
    """
    Get stock data for a specific index symbol
    """
    try:
        if limit > 100:
            limit = 100  # Limit to prevent performance issues
        
        stock_data = get_stock_data_by_index(index_symbol.upper(), limit)
        
        if not stock_data:
            raise HTTPException(
                status_code=404, 
                detail=f"No data found for index: {index_symbol}"
            )
        
        return [StockData(**data) for data in stock_data]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stock data: {str(e)}")

@app.get("/indices/region/{region}", response_model=List[IndexInfo])
async def get_indices_by_region(region: str):
    """
    Get indices for a specific region
    """
    try:
        index_info = get_index_info_by_region(region)
        
        if not index_info:
            raise HTTPException(
                status_code=404, 
                detail=f"No indices found for region: {region}"
            )
        
        return [IndexInfo(**index) for index in index_info]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting region indices: {str(e)}")

@app.get("/raw-data")
async def get_raw_data():
    """
    Get raw data from all CSV files (limited for performance)
    """
    try:
        data = load_csv_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Failed to load data")
        
        return {
            "index_info": data["index_info"],
            "index_data_sample": data["index_data"][:100],  # Limit sample
            "index_processed_sample": data["index_processed"][:100]  # Limit sample
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting raw data: {str(e)}")

@app.post("/query-gemini")
async def direct_gemini_query(request: ChatRequest):
    """
    Direct query to Gemini API without data context
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = query_gemini(request.message, request.context or "")
        
        return {
            "response": response,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Gemini: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
