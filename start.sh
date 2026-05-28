#!/bin/bash
coral source add github || true
coral source add slack || true
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
