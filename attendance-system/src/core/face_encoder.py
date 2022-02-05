import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img

from networks.inception_resnet_v1 import InceptionResNetV1
from utils.preprocessing import l2_normalize, prewhiten


class FaceEncoder:

    def __init__(self):
        print("[Encoder Network] starting....")
        self.network = InceptionResNetV1()
        print("[Encoder Network] finish initialization....")
        self.network.load_weights()
        print("[Encoder Network] weights load successfully")

    def get_embedding(self, image_path=None, image_array=None):
        array = None
        if image_path is not None:
            image = load_img(image_path, target_size=(160, 160))
            array = img_to_array(image)
        if image_array is not None:
            array = image_array

        preprocessed_image = self._preprocessing(array)
        embedding = self.network.model.predict(preprocessed_image)
        return self._normalize_embedding(embedding)

    def _normalize_embedding(self, embedding):
        return l2_normalize(embedding[0, :])

    def _preprocessing(self, image_array=None):
        image = np.expand_dims(image_array, axis=0)
        return prewhiten(image)
