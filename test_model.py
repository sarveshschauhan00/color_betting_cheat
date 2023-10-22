import tensorflow as tf
import pandas as pd
import numpy as np

loaded_model = tf.keras.models.load_model('model_sapre.h5')


def load_test_data(file_path):
    df = pd.read_csv(file_path)
    data = df['number'].to_list()
    return data

def create_sequences(data, seq_length):
    sequences = []
    labels = []
    for i in range(0, len(data)-seq_length):
        ref = data[i:i+seq_length]
        sequences.append(ref)
        labels.append(data[i+seq_length])

    return np.array(sequences), np.array(labels)

# Decide whether to predict or not based on threshold
def decide_to_predict(confidence_threshold, model, input_data):
    predicted_probabilities = model.predict(np.array([input_data]))[0]
    predicted_class = np.argmax(predicted_probabilities)
    confidence = predicted_probabilities[predicted_class]
    
    return predicted_class, confidence


def main():
    loaded_model = tf.keras.models.load_model('model_bcone.h5')
    
    test_data = load_test_data('data/emerd.csv')
    seq_length = 14
    X_test, y_test = create_sequences(test_data, seq_length)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    confidence_threshold = 0
    correct_predictions = 0
    wrong_predictions = 0
    correct = []
    incorrect = []
    for i in range(len(X_test)):
        predicted_class, confidence = decide_to_predict(confidence_threshold, loaded_model, X_test[i])

        if predicted_class == y_test[i]:
            correct_predictions += 1
            correct.append(confidence)
        else:
            wrong_predictions += 1
            incorrect.append(confidence)

    # print(correct)
    # print(incorrect)
    print(f'Number of correct predictions: {correct_predictions}')
    print(f'Number of wrong predictions: {wrong_predictions}')

if __name__ == '__main__':
    main()



