#!/bin/bash
echo "Running ML Pipeline..."
# This will run the training script in the ML folder (Step 3)
docker-compose run --rm ml_pipeline python scripts/train_model.py
echo "Copying new model to Android assets..."
cp ../kinetic-guard-ml/models/LATEST/model.onnx ../kinetic-guard-android/app/src/main/assets/models/gesture_v1.0.0.onnx
echo "Model deployed!"