import os
import tensorflow as tf
from tensorflow.keras.callbacks import LearningRateScheduler, EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam


class ClassifierNetwork:

    def __init__(self):
        print("[Classifier Network] start to initialize...")
        self.model = Sequential([
            Input(shape=(128,)),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        self.default_weights_path = os.getcwd() + "\weights\classifier_keras_weights.h5"
        print("[Classifier Network] finish initialize...")

    def load_weights(self, path=None):
        print("[Classifier Network] start loading weights...")
        weights_path = self.default_weights_path if path is None else path
        self.model.load_weights(weights_path)
        print("[Classifier Network] finish loading weights...")

    def compile(self):
        self.model.compile(loss='binary_crossentropy',
                            optimizer=Adam(0.002), metrics=['accuracy'])

    def fit(self, X_train, y_train, split=0.2):
        return self.model.fit(X_train, y_train, validation_split=split,
                               callbacks=[self._scheduler_callback,
                                          self._stop_callback],
                               epochs=20, verbose=1)

    def _scheduler_callback(self):
        def binary_classifier_scheduler(epoch, lr):
            if (epoch % 5 == 0):
                return lr * tf.math.exp(-0.1)

            return lr

        return LearningRateScheduler(binary_classifier_scheduler, verbose=1)

    def _stop_callback(self):
        return EarlyStopping(monitor='loss', patience=3)
