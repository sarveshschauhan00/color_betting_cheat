import pandas as pd
import numpy as np
import tensorflow as tf
from apscheduler.schedulers.blocking import BlockingScheduler

# Generate synthetic dataset
def generate_data(file_name):
    # Step 1: Data Preparation
    path = "data/"
    path += file_name
    # path += 'sample.csv'
    df = pd.read_csv(path)
    df = df[-400:]
    data = df['number'].to_list()
    return data

# Train the model
def train_model(model, X_train, y_train, model_name, epochs=50):
    model.fit(X_train, y_train, epochs=epochs, batch_size=32)
    model.save(model_name + '.h5')

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


def main():
    file_names = ['sapre.csv', 'parity.csv', 'bcone.csv', 'emerd.csv']
    model_names = ['model_sapre', 'model_parity', 'model_bcone', 'model_emerd']

    for i in range(4):
        data = generate_data(file_names[i])
        # print(data)
        seq_length = 14
        X, y = create_sequences(data, seq_length)

        # Reshape X for LSTM input
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        X_train = X
        y_train = y

        model = build_model(seq_length)
        train_model(model, X_train, y_train, model_names[i])

scheduled_times = []

for i in range(24):
    for j in range(0, 60, 3):
        scheduled_times.append([i, j])

scheduled_times = scheduled_times[::50]
print(scheduled_times)


# scheduler = BlockingScheduler()
# for i in range(len(scheduled_times)):
#     scheduler.add_job(main, 'cron', hour=scheduled_times[i][0], minute=scheduled_times[i][1]+1, second=30)  # Set the time for execution
# scheduler.start()

main()