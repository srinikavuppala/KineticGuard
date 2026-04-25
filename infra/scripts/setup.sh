#!/bin/bash
echo "===================================="
echo " Kinetic Guard - Initial Setup"
echo "===================================="

if [ -f ".env" ]; then
    echo "[WARNING] .env file already exists. Skipping copy to prevent overwriting secrets."
else
    echo "[INFO] Creating .env file from .env.example..."
    cp .env.example .env
    echo "[SUCCESS] .env file created! Please open it and update your passwords."
fi

echo ""
echo "Setup complete! You can now run: docker-compose up --build"