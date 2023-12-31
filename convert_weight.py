# coding: utf-8
# for more details about the yolo darknet weights file, refer to
# https://itnext.io/implementing-yolo-v3-in-tensorflow-tf-slim-c3c55ff59dbe

from __future__ import division, print_function

import os
import sys
import tensorflow as tf
import numpy as np

from model import yolov3
from utils.misc_utils import parse_anchors, load_weights

num_class = 80
img_size = 416
weight_path = '/content/YoloV3_Model/data/darknet_weights/yolov3.weights'
save_path = '/content/detection-video/models/yolov3/yolov3.ckpt'
anchors = parse_anchors('/content/YoloV3_Model/data/yolo_anchors.txt')

model = yolov3(80, anchors)
with tf.compat.v1.Session() as sess:
    inputs = tf.compat.v1.placeholder(tf.float32, [1, img_size, img_size, 3])

    with tf.compat.v1.variable_scope('yolov3'):
        feature_map = model.forward(inputs)

    saver = tf.compat.v1.train.Saver(var_list=tf.compat.v1.global_variables(scope='yolov3'))

    load_ops = load_weights(tf.compat.v1.global_variables(scope='yolov3'), weight_path)
    sess.run(load_ops)

    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    saver.save(sess, save_path=save_path)
    print('TensorFlow model checkpoint has been saved to {}'.format(save_path))



