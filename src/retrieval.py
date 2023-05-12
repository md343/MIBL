import cv2
import os
import numpy as np
from src.matcher import Matcher
from src.utils.check_dir import check_dir, clean_dir
from pathlib import Path

class Retrieval:
    def __init__(self):

        working_dir = os.getcwd()

        self.query_image_dir = check_dir(Path(working_dir+"/query/image/"))

        self.query_feature_dir = check_dir(Path(working_dir+"/query/features/"))
        clean_dir(self.query_feature_dir)

        self.map_dir = check_dir(Path(working_dir+"/static/maps/"))

        self.dataset_features = str(Path(working_dir+'/static/features/global-feats-netvlad.h5'))

        self.Mat = Matcher(self.dataset_features)

        self.counter = 0

        self.isAgilityCar = False

        self.location = "empty"
        self.location_str = str(self.map_dir.joinpath(f"{self.location}.jpg"))
        self.current_map = cv2.imread(self.location_str)

    def config_check(self, ret, frame):
        if not ret:
            print("CAM NOT FOUND")
        width = frame.shape[1]
        if width > 1000:
            self.isAgilityCar = True

    def join_map(self, frame):
        width = frame.shape[1]
        height = frame.shape[0]

        resized = cv2.resize(self.current_map, (width,height), interpolation = cv2.INTER_CUBIC)
        vis = np.concatenate((frame, resized),axis=1)

        return vis


class RetLocal(Retrieval):
    def __init__(self, camera):
        super().__init__()

        ret, frame = camera.read()

        self.config_check(ret, frame)

    def localise(self, q, frame):
        filename = os.path.join(self.query_image_dir, f"image_query_{self.counter}.jpg")
        if self.counter != 0:
            prev_counter = self.counter-1
            os.remove(os.path.join(self.query_image_dir, f"image_query_{prev_counter}.jpg"))

        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")

        #os.system(f'rm -rf {query_feature_dir}*')
        self.location = self.Mat.top_one(self.query_image_dir, self.query_feature_dir, self.counter)
        loc_dir = str(self.map_dir.joinpath(f"{self.location}.jpg"))

        if os.path.exists(loc_dir):
            self.location_str=loc_dir
            current_map = cv2.imread(self.location_str)
        else:
            self.location = "empty"
            self.location_str = str(self.map_dir.joinpath(f"{self.location}.jpg"))
            current_map = cv2.imread(self.location_str)
            print("MAP NOT FOUND")

        q.put(current_map)

    def terminate(self, camera):
        camera.release()
        cv2.destroyAllWindows()


class RetRemote(Retrieval):
    def __init__(self):
        super().__init__()

        self.camera = cv2.VideoCapture(0)
        ret, frame = self.camera.read()

        self.config_check(ret, frame)


    def localise(self):
        ret, frame = self.camera.read()
        if self.isAgilityCar:
            width = frame.shape[1]
            frame = frame[:,:width//2]

        filename = os.path.join(self.query_image_dir, f"image_query_{self.counter}.jpg")
        if self.counter != 0:
            prev_counter = self.counter-1
            os.remove(os.path.join(self.query_image_dir, f"image_query_{prev_counter}.jpg"))

        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")

        self.location = self.Mat.top_one(self.query_image_dir, self.query_feature_dir, self.counter)
        loc_dir = str(self.map_dir.joinpath(f"{self.location}.jpg"))

        self.counter += 1

        if os.path.exists(loc_dir):
            self.location_str=loc_dir
            self.current_map = cv2.imread(self.location_str)
        else:
            self.location = "empty"
            self.location_str = str(self.map_dir.joinpath(f"{self.location}.jpg"))
            self.current_map = cv2.imread(self.location_str)
            print("MAP NOT FOUND")

    def terminate(self):
        self.camera.release()
        cv2.destroyAllWindows()
