import numpy as np
import h5py
from src.extract_features import confs, main
from src.utils.base_model import BaseModel
from pathlib import Path

#featureDir = 'F:/Retrieval_dataset/_static/features_HLOC/global-feats-netvlad.h5'


class Matcher:
    def __init__(self, featureDir):

        self.features = []
        self.images = []
        hf = h5py.File(featureDir,'r')
        for img in hf.keys():
            self.features.append(hf[img]['global_descriptor'][:])
            self.images.append(img)

        self.retrieval_conf = confs['netvlad']

    def top_one(self, images, output, counter):

        global_descriptors = main(self.retrieval_conf, images, output)

        live = h5py.File(Path(output) / Path("global-feats-netvlad.h5"), 'r')
        query = live[f"image_query_{counter}.jpg"]['global_descriptor'][:]

        dists = np.linalg.norm(self.features - query, axis=1)
        ids = np.argsort(dists)[:1]

        scores = [(dists[id], self.images[id]) for id in ids]
        place = scores[0][1]
        place = place[:-6]
        print(place)
        return place





#print(retrieval_conf)

if __name__ == "__main__":

    images = Path("F:/Train_dataset/live/")
    output = Path("F:/Retrieval_dataset/_static/uploaded")

    m1 = matcher(featureDir)
    m1.match(images, output)
    #print(global_descriptors)
