import os


class TripletGenerator:

    def __init__(self):
        self.lfw_dataset_path = os.getcwd() + '\data\lfw_224_clean'

    def lfw_dataset_source(self, path):
        self.lfw_dataset_path = os.getcwd() + path

    def dataset_info(self):
        names = self._get_names_list()
        names_multiple_images = self._get_names_multiple_images()
        names_single_images = self._get_names_single_images()

        info = {
            "count_names": len(names),
            "count_names_multiple_images": len(names_multiple_images),
            "count_name_single_image": len(names_single_images),
        }

        return info

    def create_triplets(self):
        (anchors, positives) = self._get_positive_pairs()
        negatives = [self._get_image_path(name, "{}_0001.jpg".format(name)) for name in self._get_names_single_images()]

        length = min(len(positives), len(negatives))

        return (anchors[:length], positives[:length], negatives[:length])

    def _get_positive_pairs(self):
        anchors = []
        positives = []
        inputs = self._get_names_multiple_images()

        for name in inputs:
            name_path = self._get_name_path(name)
            name_listdir = os.listdir(name_path)
            listdir_length = len(name_listdir)
            for idx in range(listdir_length // 2):
                anchor = self._get_image_path(name, name_listdir[idx * 2])
                anchors.append(anchor)
                positive = self._get_image_path(
                    name, name_listdir[idx * 2 + 1])
                positives.append(positive)

        return (anchors, positives)

    def _get_names_single_images(self):
        diff = set(self._get_names_list()) - \
            set(self._get_names_multiple_images())
        return list(diff)

    def _get_names_multiple_images(self):
        """
        @description
        Get name list of person with more than one image
        """
        names = self._get_names_list()
        names_multiple_images = []
        for name in names:
            name_path = self._get_name_path(name)
            listdir_length = len(os.listdir(name_path))

            if listdir_length > 1:
                names_multiple_images.append(name)

        return names_multiple_images

    def _get_image_path(self, name="", filename=""):
        return "{}\\{}".format(self._get_name_path(name), filename)

    def _get_name_path(self, name=""):
        return "{}\\{}".format(self.lfw_dataset_path, name)

    def _get_names_list(self):
        return os.listdir(self.lfw_dataset_path)


if __name__ == "__main__":
    triplet_generator = TripletGenerator()
    print(triplet_generator.dataset_info())
    print(triplet_generator.create_triplets())
