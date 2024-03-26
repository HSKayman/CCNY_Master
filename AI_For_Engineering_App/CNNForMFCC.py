import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import librosa

def preprocess_data(audio_files, labels):
    mfcc_features = []
    for file in audio_files:
        audio, sample_rate = librosa.load(file, sr=None)
        mfcc = librosa.feature.mfcc(audio, sr=sample_rate, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        mfcc_features.append(mfcc_processed)
    
    # Convert the list of MFCC features to a numpy array
    mfcc_features = np.array(mfcc_features)
    mfcc_features = np.expand_dims(mfcc_features, -1)
    
    # Encode the labels as integers
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)
    encoded_labels = tf.keras.utils.to_categorical(encoded_labels)
    
    return mfcc_features, encoded_labels

audio_files = ['', '']  # Add your paths
labels = ['word1', 'word2']  # Add corresponding labels

X, y = preprocess_data(audio_files, labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Conv2D(32, kernel_size=(2, 2), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(y.shape[1], activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")
