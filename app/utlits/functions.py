import os
import pandas as pd
import google.generativeai as genai
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load data
def load_csv_data():
    """Load all CSV files and return as dictionaries"""
    try:
        # Load index information
        index_info_df = pd.read_csv("app/data/indexInfo.csv")
        
        # Load stock data (sample for performance)
        index_data_df = pd.read_csv("app/data/indexData.csv", nrows=10000)
        
        # Load processed data (sample for performance)
        index_processed_df = pd.read_csv("app/data/indexProcessed.csv", nrows=10000)
        
        return {
            "index_info": index_info_df.to_dict('records'),
            "index_data": index_data_df.to_dict('records'),
            "index_processed": index_processed_df.to_dict('records')
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_data_summary():
    """Get summary statistics of the data"""
    try:
        index_info_df = pd.read_csv("app/data/indexInfo.csv")
        index_data_df = pd.read_csv("app/data/indexData.csv")
        index_processed_df = pd.read_csv("app/data/indexProcessed.csv")
        
        return {
            "total_indices": len(index_info_df),
            "total_records": len(index_data_df) + len(index_processed_df),
            "date_range": {
                "earliest": index_data_df['Date'].min(),
                "latest": index_data_df['Date'].max()
            },
            "available_indices": index_info_df['Index'].tolist()
        }
    except Exception as e:
        print(f"Error getting data summary: {e}")
        return None

def query_gemini(prompt: str, context: str = "") -> str:
    """Query Gemini API with the given prompt and context"""
    try:
        # Create the full prompt with context
        full_prompt = f"""
        Context about stock market data:
        {context}
        
        User Question: {prompt}
        
        Please provide a helpful response based on the available stock market data. 
        If the question is about specific data that's not available in the context, 
        please mention that and provide general information about stock markets.
        """
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def get_stock_data_by_index(index_symbol: str, limit: int = 10) -> List[Dict]:
    """Get stock data for a specific index"""
    try:
        df = pd.read_csv("app/data/indexData.csv")
        filtered_df = df[df['Index'] == index_symbol].head(limit)
        return filtered_df.to_dict('records')
    except Exception as e:
        print(f"Error getting stock data: {e}")
        return []

def get_index_info_by_region(region: str) -> List[Dict]:
    """Get index information for a specific region"""
    try:
        df = pd.read_csv("app/data/indexInfo.csv")
        filtered_df = df[df['Region'].str.contains(region, case=False, na=False)]
        return filtered_df.to_dict('records')
    except Exception as e:
        print(f"Error getting index info: {e}")
        return []

def create_context_for_chat() -> str:
    """Create context string for the chatbot"""
    try:
        index_info_df = pd.read_csv("app/data/indexInfo.csv")
        
        context = "Available stock market indices:\n"
        for _, row in index_info_df.iterrows():
            context += f"- {row['Index']} ({row['Exchange']}, {row['Region']}, {row['Currency']})\n"
        
        context += f"\nTotal indices available: {len(index_info_df)}"
        context += "\n\nData includes historical price information (Open, High, Low, Close, Volume) for these indices."
        
        return context
    except Exception as e:
        print(f"Error creating context: {e}")
        return "Stock market data is available for various global indices."

def process_chat_message(message: str) -> Dict[str, Any]:
    """Process chat message and return response with relevant data"""
    try:
        # Create context
        context = create_context_for_chat()
        
        # Get response from Gemini
        response = query_gemini(message, context)
        
        # Extract any specific data requests
        data = None
        
        # Check if user is asking about specific index
        if any(word in message.lower() for word in ['nya', 'ixic', 'hsi', 'n225', 'gspc']):
            # Extract index symbol (simplified)
            words = message.lower().split()
            for word in words:
                if word in ['nya', 'ixic', 'hsi', 'n225', 'gspc']:
                    stock_data = get_stock_data_by_index(word.upper(), 5)
                    if stock_data:
                        data = {"stock_data": stock_data}
                    break
        
        # Check if user is asking about specific region
        regions = ['united states', 'china', 'japan', 'europe', 'germany', 'hong kong']
        for region in regions:
            if region in message.lower():
                index_info = get_index_info_by_region(region)
                if index_info:
                    data = {"index_info": index_info}
                break
        
        return {
            "response": response,
            "data": data,
            "success": True
        }
    except Exception as e:
        return {
            "response": f"Sorry, I encountered an error: {str(e)}",
            "data": None,
            "success": False,
            "error": str(e)
        }
