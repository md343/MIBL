import cv2
import os
import numpy as np
from src.matcher import Matcher
from src.retrieval import RetLocal
from src.utils.check_dir import check_dir, clean_dir
from pathlib import Path
from multiprocessing import Process, Queue
import pickle

working_dir = os.getcwd()
map_dir = check_dir(Path(working_dir+"/static/maps/"))

img_dir = Path('F:\Train_dataset\_dataset')

def join_map(img, loc):

    width = img.shape[1]
    height = img.shape[0]

    resized = cv2.resize(loc, (width,height), interpolation = cv2.INTER_CUBIC)
    vis = np.concatenate((img, resized),axis=1)

    return vis

def test():
    outputpkl = 'F:/Train_dataset/results.pkl'

    with open(outputpkl, 'rb') as fp:
        results = pickle.load(fp)

    return results

count = {}
if __name__ == "__main__":
    r = test()
    delay = 500
    for img in r.keys():
        #print(img)
        #print(r[img])
        # if r[img] in count.keys():
        #     count[r[img]] = count[r[img]] + 1
        # else:
        #     count[r[img]] = 1
        img_str = str(img_dir.joinpath(img))

        if r[img] == "CES" or r[img] == "CES_corridor":
            #print(r[img])
            continue

        key = cv2.waitKey(delay)
        if key == ord("c"):
            if delay == 500:
                delay == 50
            else:
                delay == 500

        location_str = str(map_dir.joinpath(f"{r[img]}.jpg"))

        imgr = cv2.imread(img_str)
        locr = cv2.imread(location_str)

        vis = join_map(imgr, locr)
        if key == ord("s"):
            cv2.imwrite('F:/Train_dataset/vis.jpg', vis)
        cv2.imshow("Retrieval", vis)

#print(count)

cv2.destroyAllWindows()
