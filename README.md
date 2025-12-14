# 3D Word Cloud - Garvit

A 3D interactive word cloud generator that visualizes topics from news articles in an immersive spherical display.

## Features
- **Frontend**: Built with React, TypeScript, and Three.js (React Three Fiber) for high-performance 3D rendering.
- **Backend**: Powered by FastAPI, leveraging NLTK and Scikit-learn for advanced NLP tasks like TF-IDF and LDA topic modeling.
- **Interactive UI**: Real-time URL analysis and dynamic 3D word placement based on keyword relevance.

## Prerequisites
- **Python 3.10+** (for the backend API)
- **Node.js 18+** (for the frontend application)

## Quick Start
The project includes an automated setup script to install all dependencies and start both servers concurrently.
1. Run the setup script:
   ```bash
   ./setup.sh
   ```
2. Open your browser to `http://localhost:5173`.
3. Enter a standard article URL (e.g., Wikipedia) to generate your cloud.
