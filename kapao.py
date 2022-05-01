import sys
from pathlib import Path
FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix() + '/kpo')  # add kapao/ to path

from kpo.utils.torch_utils import select_device, time_sync
from kpo.utils.general import check_img_size
from kpo.utils.datasets import LoadImages
from kpo.utils.augmentations import letterbox
from kpo.models.experimental import attempt_load
from kpo.val import run_nms, post_process_batch

import torch
import yaml
import numpy as np

class Kapao():
    def __init__(self):
        self.imgsz = 1024
        self.device = ''
        self.data = ''
        self.half = True
        self.scales = [1]
        self.flips = [-1]
        self.conf_thres = 0.5
        self.iou_thres = 0.45
        self.no_kp_dets = True
        self.conf_thres_kp = 0.5
        self.iou_thres_kp = 0.45
        self.conf_thres_kp_person = 0.2
        self.overwrite_tol = 50
        self.model = None

    def load_model(self, weights='./kpo/models/kapao_s_coco.pt'):
        self.device = select_device(self.device, batch_size=1)
        print('Using device: {}'.format(self.device))

        self.model = attempt_load(weights, map_location=self.device)  # load FP32 model
        half = self.half & (self.device.type != 'cpu')
        if half:  # half precision only supported on CUDA
            self.model.half()
        self.stride = int(self.model.stride.max())  # model stride
        imgsz = check_img_size(self.imgsz, s=self.stride)  # check image size

        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, imgsz, imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once

    def init(self):
        self.data = './kpo/data/coco-kp.yaml'
        with open(self.data) as f:
            self.data = yaml.safe_load(f)  # load data dict

        # add inference settings to data dict
        self.data['imgsz'] = self.imgsz
        self.data['conf_thres'] = self.conf_thres
        self.data['iou_thres'] = self.iou_thres
        self.data['use_kp_dets'] = not self.no_kp_dets
        self.data['conf_thres_kp'] = self.conf_thres_kp
        self.data['iou_thres_kp'] = self.iou_thres_kp
        self.data['conf_thres_kp_person'] = self.conf_thres_kp_person
        self.data['overwrite_tol'] = self.overwrite_tol
        self.data['scales'] = self.scales
        self.data['flips'] = [None if f == -1 else f for f in self.flips]

        self.load_model()

    def predict(self, image):
        img = letterbox(image, self.imgsz, stride=self.stride, auto=True)[0]
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        out = self.model(img, augment=True, kp_flip=self.data['kp_flip'], scales=self.data['scales'], flips=self.data['flips'])[0]
        person_dets, kp_dets = run_nms(self.data, out)
        bboxes, poses, _, _, _ = post_process_batch(self.data, img, [], [[image.shape[:2]]], person_dets, kp_dets)
        return bboxes, poses





