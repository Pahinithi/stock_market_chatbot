#!/bin/bash

# Start FastAPI server in the background
echo "Starting FastAPI server..."
uvicorn app.main:app --reload &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 2

# Start Streamlit app
echo "Starting Streamlit app..."
streamlit run app/frontend/streamlit_app.py

# When Streamlit is closed, also kill the FastAPI server
kill $FASTAPI_PID