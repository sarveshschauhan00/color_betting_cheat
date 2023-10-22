import numpy as np
import tensorflow as tf
import pandas as pd

# Generate synthetic dataset
def generate_sequence():
    # Step 1: Data Preparation
    path = "live_data/"
    path += 'sapre.csv'
    df = pd.read_csv(path)
    data = df['number'].to_list()
    data = data[-14:]
    return data

# Load the model
model = tf.keras.models.load_model('model_sapre.h5')

# Prepare input data
seq_length = 14
input_sequence = generate_sequence()
print(input_sequence)

input_sequence = np.array([input_sequence])
input_sequence = np.reshape(input_sequence, (input_sequence.shape[0], input_sequence.shape[1], 1))

# Make a prediction
predicted_probabilities = model.predict(input_sequence)[0]
predicted_class = np.argmax(predicted_probabilities)

# Get the predicted number
predicted_number = predicted_class

print(f"Predicted number: {predicted_number}")
