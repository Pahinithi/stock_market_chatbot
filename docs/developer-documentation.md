# Stock Market Chatbot - Developer Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Setup & Installation](#setup--installation)
4. [Docker Containerization](#docker-containerization)
5. [Starting the Application](#starting-the-application)
6. [API Documentation](#api-documentation)
7. [Frontend Documentation](#frontend-documentation)
8. [Data Structure](#data-structure)

## 🎯 Project Overview

The Stock Market Chatbot is a full-stack application that combines FastAPI backend with Streamlit frontend to provide AI-powered stock market analysis using Google's Gemini API.

### Key Features
- 🤖 AI-powered chatbot using Gemini API
- 📊 Real-time stock market data analysis
- 📈 Interactive charts and visualizations
- 🌍 Global indices coverage
- 🔄 RESTful API endpoints
- 💬 Interactive chat interface

### Technology Stack
- **Backend**: FastAPI, Python 3.11+
- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Data**: CSV files (Pandas)
- **Charts**: Plotly
- **Environment**: Conda

## 🏗️ Architecture

```
keerthanan/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── data/                   # CSV data files
│   │   ├── indexInfo.csv
│   │   ├── indexData.csv
│   │   └── indexProcessed.csv
│   ├── utlits/                 # Utility modules
│   │   ├── __init__.py
│   │   ├── functions.py        # Core business logic
│   │   └── schemas.py          # Pydantic models
│   └── frontend/
│       └── streamlit_app.py    # Streamlit frontend
├── docs/
│   └── developer-documentation.md
├── requirements.txt
├── .env                        # Environment variables
└── .gitignore
```

### Component Overview

#### Backend (FastAPI)
- **main.py**: FastAPI application with all endpoints
- **functions.py**: Business logic, API integrations, data processing
- **schemas.py**: Pydantic models for request/response validation

#### Frontend (Streamlit)
- **streamlit_app.py**: Complete UI with chat, charts, and data analysis

#### Data Layer
- **indexInfo.csv**: Metadata about stock indices
- **indexData.csv**: Historical OHLCV data
- **indexProcessed.csv**: Processed data with USD conversions

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11 or higher
- Conda (recommended) or pip
- Google Gemini API key

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd keerthanan
   ```

2. **Create conda environment**
   ```bash
   conda create -n chatbot python=3.11
   conda activate chatbot
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.13 | Web framework |
| uvicorn | 0.34.3 | ASGI server |
| pandas | 2.3.0 | Data manipulation |
| python-dotenv | 1.1.0 | Environment variables |
| google-generativeai | 0.8.5 | Gemini API client |
| pydantic | 2.11.7 | Data validation |
| python-multipart | 0.0.20 | File uploads |
| streamlit | 1.46.0 | Frontend framework |
| plotly | 6.1.2 | Interactive charts |
| requests | 2.32.4 | HTTP client |

## 🎬 Starting the Application

You have two options to start the application:

### Option 1: Using start script (Recommended)

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Start both servers
./start.sh
```

### Option 2: Manual start

```bash
# Terminal 1 - Start FastAPI server
fastapi dev app/main.py

# Terminal 2 - Start Streamlit app
streamlit run app/frontend/streamlit_app.py
```

### Access Points
- **FastAPI Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit App**: http://localhost:8501

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, no authentication is required. API key is handled server-side.

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### 2. Chat Endpoint
```http
POST /chat
```
**Request Body:**
```json
{
  "message": "Tell me about NYA index",
  "context": "optional_context"
}
```
**Response:**
```json
{
  "response": "AI generated response",
  "data": {
    "stock_data": [...],
    "index_info": [...]
  },
  "success": true,
  "error": null
}
```

#### 3. Data Summary
```http
GET /data/summary
```
**Response:**
```json
{
  "total_indices": 14,
  "total_records": 1234567,
  "date_range": {
    "earliest": "1965-12-31",
    "latest": "2024-01-01"
  },
  "available_indices": ["NYA", "IXIC", "HSI", ...]
}
```

#### 4. Get All Indices
```http
GET /indices
```
**Response:**
```json
[
  {
    "region": "United States",
    "exchange": "New York Stock Exchange",
    "index": "NYA",
    "currency": "USD"
  }
]
```

#### 5. Get Stock Data
```http
GET /stock-data/{index_symbol}?limit=10
```
**Response:**
```json
[
  {
    "index": "NYA",
    "date": "2024-01-01",
    "open": 15000.0,
    "high": 15100.0,
    "low": 14900.0,
    "close": 15050.0,
    "adj_close": 15050.0,
    "volume": 1000000
  }
]
```

#### 6. Get Indices by Region
```http
GET /indices/region/{region}
```

#### 7. Direct Gemini Query
```http
POST /query-gemini
```

## 🎨 Frontend Documentation

### Streamlit App Structure

#### Pages
1. **💬 Chat**: Interactive chat interface
2. **📊 Data Analysis**: Summary statistics and data overview
3. **📈 Charts**: Interactive stock charts
4. **ℹ️ About**: Application information

#### Key Components

##### Chat Interface
- Real-time chat with AI
- Message history persistence
- Data display integration
- Error handling

##### Data Visualization
- **Candlestick Charts**: Professional stock charts
- **Line Charts**: Multiple chart types
- **Interactive Tables**: Sortable data tables
- **Metrics Dashboard**: Key statistics

##### API Integration
- Health check validation
- Error handling
- Real-time data fetching
- Response processing

### Customization


## 📊 Data Structure

### CSV Files

#### indexInfo.csv
| Column | Type | Description |
|--------|------|-------------|
| Region | String | Geographic region |
| Exchange | String | Stock exchange name |
| Index | String | Index symbol |
| Currency | String | Trading currency |

#### indexData.csv
| Column | Type | Description |
|--------|------|-------------|
| Index | String | Index symbol |
| Date | Date | Trading date |
| Open | Float | Opening price |
| High | Float | Highest price |
| Low | Float | Lowest price |
| Close | Float | Closing price |
| Adj Close | Float | Adjusted closing price |
| Volume | Integer | Trading volume |

#### indexProcessed.csv
Same as indexData.csv plus:
| Column | Type | Description |
|--------|------|-------------|
| CloseUSD | Float | Close price in USD |

## 🐳 Docker Containerization

### Overview
The application is fully containerized using Docker, providing a consistent deployment environment across different platforms.

### Containerfile Features
- **Base Image**: Python 3.11-slim for optimized size and security
- **Multi-service**: Runs both FastAPI backend and Streamlit frontend
- **Security**: Non-root user execution
- **Health Checks**: Automated health monitoring
- **Port Exposure**: FastAPI (8000) and Streamlit (8501)

### Building the Container

```bash
# Build the Docker image
docker build -f Containerfile -t kee-latest .

# Build with custom tag
docker build -f Containerfile -t keerthanan:latest .
```

### Running the Container

#### Basic Run
```bash
# Run with default ports
docker run -p 8000:8000 -p 8501:8501 kee-latest
```

#### With Environment Variables
```bash
# Run with environment file
docker run --env-file ./.env -p 8000:8000 -p 8501:8501 -d --rm kee-latest
```

#### Custom Port Mapping
```bash
# Map to different host ports
docker run -p 8080:8000 -p 8502:8501 kee-latest
```
