import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Stock Market Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the FastAPI server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_data_summary():
    """Get data summary from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/data/summary")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_all_indices():
    """Get all available indices"""
    try:
        response = requests.get(f"{API_BASE_URL}/indices")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_stock_data(index_symbol, limit=50):
    """Get stock data for a specific index"""
    try:
        response = requests.get(f"{API_BASE_URL}/stock-data/{index_symbol}?limit={limit}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def send_chat_message(message):
    """Send chat message to API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return {"response": f"Error: {str(e)}", "success": False}

def create_candlestick_chart(data):
    """Create candlestick chart from stock data"""
    if not data:
        return None
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=df['Index'].iloc[0] if 'Index' in df.columns else 'Stock'
    )])
    
    fig.update_layout(
        title=f"Stock Price Chart - {df['Index'].iloc[0] if 'Index' in df.columns else 'Stock'}",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white"
    )
    
    return fig

def create_line_chart(data, column='Close'):
    """Create line chart from stock data"""
    if not data:
        return None
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    fig = px.line(
        df, 
        x='Date', 
        y=column,
        title=f"{column} Price Over Time - {df['Index'].iloc[0] if 'Index' in df.columns else 'Stock'}"
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{column} Price",
        template="plotly_white"
    )
    
    return fig

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Market Chatbot</h1>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ FastAPI server is not running. Please start the server first using: `fastapi dev app/main.py`")
        st.stop()
    
    # Sidebar
    st.sidebar.title("🔧 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["💬 Chat", "📊 Data Analysis", "📈 Charts", "ℹ️ About"]
    )
    
    if page == "💬 Chat":
        show_chat_page()
    elif page == "📊 Data Analysis":
        show_data_analysis_page()
    elif page == "📈 Charts":
        show_charts_page()
    elif page == "ℹ️ About":
        show_about_page()

def show_chat_page():
    """Chat interface page"""
    st.header("💬 Chat with Stock Market AI")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about stock markets, indices, or market data..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = send_chat_message(prompt)
                
                if response and response.get("success", False):
                    bot_response = response["response"]
                    
                    # Display response
                    st.markdown(bot_response)
                    
                    # Display additional data if available
                    if response.get("data"):
                        data = response["data"]
                        if "stock_data" in data:
                            st.subheader("📊 Recent Stock Data")
                            df = pd.DataFrame(data["stock_data"])
                            st.dataframe(df, use_container_width=True)
                        
                        if "index_info" in data:
                            st.subheader("📋 Index Information")
                            df = pd.DataFrame(data["index_info"])
                            st.dataframe(df, use_container_width=True)
                else:
                    error_msg = response.get("response", "Sorry, I encountered an error. Please try again.") if response else "Sorry, I couldn't connect to the server."
                    st.error(error_msg)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response if response and response.get("success", False) else error_msg})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

def show_data_analysis_page():
    """Data analysis page"""
    st.header("📊 Data Analysis")
    
    # Get data summary
    summary = get_data_summary()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Indices", summary["total_indices"])
        
        with col2:
            st.metric("Total Records", f"{summary['total_records']:,}")
        
        with col3:
            st.metric("Earliest Date", summary["date_range"]["earliest"])
        
        with col4:
            st.metric("Latest Date", summary["date_range"]["latest"])
        
        # Available indices
        st.subheader("📋 Available Indices")
        indices = get_all_indices()
        if indices:
            df = pd.DataFrame(indices)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No indices data available")
    else:
        st.error("Could not fetch data summary")

def show_charts_page():
    """Charts and visualization page"""
    st.header("📈 Stock Charts")
    
    # Get available indices
    indices = get_all_indices()
    if not indices:
        st.warning("No indices data available")
        return
    
    # Index selection
    index_options = [idx["index"] for idx in indices]
    selected_index = st.selectbox("Select an index:", index_options)
    
    if selected_index:
        # Get stock data
        stock_data = get_stock_data(selected_index, 100)
        
        if stock_data:
            # Create tabs for different chart types
            tab1, tab2, tab3 = st.tabs(["📊 Candlestick Chart", "📈 Line Chart", "📋 Data Table"])
            
            with tab1:
                st.subheader("Candlestick Chart")
                fig = create_candlestick_chart(stock_data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not create candlestick chart")
            
            with tab2:
                st.subheader("Line Chart")
                chart_type = st.selectbox("Select chart type:", ["Close", "Open", "High", "Low"])
                fig = create_line_chart(stock_data, chart_type)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not create line chart")
            
            with tab3:
                st.subheader("Data Table")
                df = pd.DataFrame(stock_data)
                st.dataframe(df, use_container_width=True)
        else:
            st.warning(f"No data available for {selected_index}")

def show_about_page():
    """About page"""
    st.header("ℹ️ About")
    
    st.markdown("""
    ## Stock Market Chatbot
    
    This is an AI-powered chatbot that helps you analyze stock market data using Google's Gemini AI.
    
    ### Features:
    - 🤖 **AI Chat**: Ask questions about stock markets, indices, and market trends
    - 📊 **Data Analysis**: View comprehensive data summaries and statistics
    - 📈 **Interactive Charts**: Visualize stock data with candlestick and line charts
    - 🌍 **Global Indices**: Access data from major global stock exchanges
    
    ### Available Data:
    - **14 Global Indices** including NYSE, NASDAQ, HSI, Nikkei 225, and more
    - **Historical Price Data** with OHLCV (Open, High, Low, Close, Volume)
    - **Real-time Analysis** powered by Gemini AI
    
    ### Technology Stack:
    - **Backend**: FastAPI with Python
    - **AI**: Google Gemini API
    - **Frontend**: Streamlit
    - **Data**: CSV files with stock market data
    - **Charts**: Plotly for interactive visualizations
    
    ### How to Use:
    1. **Chat**: Ask questions about stock markets, specific indices, or market trends
    2. **Data Analysis**: View summary statistics and available indices
    3. **Charts**: Select an index to view interactive price charts
    4. **API**: Access the backend API directly at `http://localhost:8000`
    
    ### API Endpoints:
    - `GET /health` - Health check
    - `POST /chat` - Chat with AI
    - `GET /data/summary` - Data summary
    - `GET /indices` - All indices
    - `GET /stock-data/{index}` - Stock data for specific index
    
    ### Available Indices:
    """)
    
    indices = get_all_indices()
    if indices:
        for idx in indices:
            st.markdown(f"- **{idx['index']}**: {idx['exchange']} ({idx['region']}) - {idx['currency']}")

if __name__ == "__main__":
    main()
