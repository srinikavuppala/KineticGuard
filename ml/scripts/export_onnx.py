import onnx.helper
import joblib
import onnxmltools
from onnxconverter_common.data_types import FloatTensorType
from pathlib import Path

# THE SMART BANDAGE: Fix XGBoost 3.x boolean bug
_original_make_attribute = onnx.helper.make_attribute


def _patched_make_attribute(key, value):
    if isinstance(value, (list, tuple)):
        value = [int(v) if isinstance(v, bool) else v for v in value]
    elif isinstance(value, bool):
        value = int(value)
    return _original_make_attribute(key, value)


onnx.helper.make_attribute = _patched_make_attribute


def export_to_onnx():
    print("Loading trained brain...")
    model = joblib.load(Path('models/v1.0.0/gesture_model.pkl'))

    print("Converting to ONNX format for Android...")
    initial_type = [('float_input', FloatTensorType([None, 210]))]

    onnx_model = onnxmltools.convert_xgboost(model, initial_types=initial_type)

    save_path = Path('models/v1.0.0/gesture_model.onnx')
    onnxmltools.utils.save_model(onnx_model, save_path)

    print(f"Android brain saved to {save_path}")
    print(f"File size: {save_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    export_to_onnx()