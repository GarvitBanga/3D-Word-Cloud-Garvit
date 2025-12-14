#!/bin/bash
set -e
echo "=== 3D Word Cloud Setup ==="
echo "[1/3] Backend"
pip install -r Backend/requirements.txt
echo "[2/3] Frontend"
cd Frontend
npm install
npm install three @types/three @react-three/fiber @react-three/drei axios framer-motion
cd ..
echo "[3/3] Running..."
trap "kill 0" EXIT
python3 Backend/main.py &
cd Frontend && npm run dev -- --host &
wait