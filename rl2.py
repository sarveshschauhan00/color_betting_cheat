import pandas as pd
import numpy as np
import tensorflow as tf

# Generate synthetic dataset
def generate_data(start=0, end=5000):
    # Step 1: Data Preparation
    path = "data/"
    # paths = ['new_sapre.csv', 'new_parity.csv', 'new_emerd.csv', 'new_bcone.csv']
    paths = ['sapre.csv', 'parity.csv', 'emerd.csv', 'bcone.csv']
    path += paths[0]
    # path += 'sample.csv'
    df = pd.read_csv(path)
    df = df[start:end]
    data = df['number'].to_list()
    return data

# Train the model
def train_model(model, X_train, y_train, epochs=50):
    model.fit(X_train, y_train, epochs=epochs, batch_size=32)
    model.save('model_sapre.h5')

def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(0, len(data)-seq_length):
        ref = data[i:i+seq_length]
        sequences.append(ref)
        labels.append(data[i+seq_length])

    return np.array(sequences), np.array(labels)

# Define the model
def build_model(seq_length):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=10, output_dim=10, input_length=seq_length),  # Embedding layer for integer sequences
        tf.keras.layers.LSTM(64),  # LSTM layer
        tf.keras.layers.Dense(20, activation='softmax')  # Dense layer with softmax activation
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Decide whether to predict or not based on threshold
def decide_to_predict(confidence_threshold, model, input_data):
    predicted_probabilities = model.predict(np.array([input_data]))[0]
    predicted_class = np.argmax(predicted_probabilities)
    confidence = predicted_probabilities[predicted_class]
    
    return predicted_class, confidence

# Main function
def main():
    ls = []
    total_correct = 0
    data = generate_data(start=0, end=500)
    # print(data)
    seq_length = 14
    X, y = create_sequences(data, seq_length)

    # Reshape X for LSTM input
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # split = int(0.8 * len(X))
    split = len(X) - 50
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = build_model(seq_length)
    train_model(model, X_train, y_train)

    confidence_threshold = 0  # Set your desired threshold here
    correct_predictions = 0
    wrong_predictions = 0
    correct = []
    incorrect = []
    for i in range(len(X_test)):
        predicted_class, confidence = decide_to_predict(confidence_threshold, model, X_test[i])
        if confidence >= confidence_threshold:
            if predicted_class == y_test[i]:
                correct_predictions += 1
                correct.append(confidence)
            else:
                wrong_predictions += 1
                incorrect.append(confidence)
    print(correct)
    print(incorrect)
    total_correct += correct_predictions
    print(f'Number of correct predictions: {correct_predictions}')
    print(f'Number of wrong predictions: {wrong_predictions}')

if __name__ == '__main__':
    main()