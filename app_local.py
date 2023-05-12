import cv2
import os
import numpy as np
from src.matcher import Matcher
from src.retrieval import RetLocal
from src.utils.check_dir import check_dir, clean_dir
from pathlib import Path
from multiprocessing import Process, Queue


def loop(retriever, camera):
    clean_dir(retriever.query_image_dir)
    q = Queue()

    while True:
        ret, frame = camera.read()

        if not ret:
            continue

        if retriever.isAgilityCar:
            width = frame.shape[1]//2
            frame = frame[:,:width]

        key = cv2.waitKey(1)

        if key == ord("c"):
            r = Process(target=retriever.localise, args=(q, frame))
            r.start()
            retriever.current_map = q.get()
            r.join()
            retriever.counter += 1

        elif key == ord("q"):
            break

        vis = retriever.join_map(frame)
        cv2.imshow("Retrieval", vis)


def test():
    outputpkl = 'F:/Train_dataset/results.pkl'

    with open(outputpkl, 'rb') as fp:
        results = pickle.load(fp)


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    retriever = RetLocal(camera)

    loop(retriever, camera)
    retriever.terminate(camera)
