# create_dummy_model.py
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# Create simple model
iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

# Convert to ONNX
initial_type = [('float_input', FloatTensorType([None, 4]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Save model
with open("binance.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
    
print("Model created successfully!")