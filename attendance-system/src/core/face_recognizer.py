import numpy as np

from networks.classifier import ClassifierNetwork


class FaceRecognizer:
    def __init__(self):
        print("[Classifier Network] starting....")
        self.network = ClassifierNetwork()
        print("[Classifier Network] finish initialization....")
        self.network.load_weights()
        print("[Classifier Network] weights load successfully")
    
    def compare(self, input_embedding, anchor_embedding):
        difference = self._get_embedding_difference(input_embedding, anchor_embedding)
        return self.network.model.predict(difference)[0][0]

    def _get_embedding_difference(self, input_embedding, anchor_embedding):
        return np.array([np.array(anchor_embedding - input_embedding).reshape(-1)])
    