from styx_msgs.msg import TrafficLight
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

#from collections import defaultdict
#from io import StringIO
#from matplotlib import pyplot as plt
#from PIL import Image

PATH_TO_CKPT = './simulator/frozen_inference_graph.pb' #
#PATH_TO_CKPT = './site/frozen_inference_graph.pb' # 

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier

        detection_graph = tf.Graph()
        with detection_graph.as_default():
          od_graph_def = tf.GraphDef()
          with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')


    def load_image_into_numpy_array(self, image):
      (im_width, im_height) = image.size
      return np.array(image.getdata()).reshape(
          (im_height, im_width, 3)).astype(np.uint8)

    def detect_tl(self, image):
        with detection_graph.as_default():
          with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            image_np = self.load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            # print ('Scores:', scores)
            # print ('Classes:', classes)
            # print ('Num detections', num)
            scores = np.squeeze(scores)
            classes = np.squeeze(classes).astype(np.int32)
            for n in range(num):
                if scores[i] > 0.5:
                    return scores[i], classes[i]
            return None, None

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        [det_prob, tl_class] = self.detect_tl(image)
        if tl_class == 1:
            print ('Red light; Prob:',det_prob)
            return TrafficLight.RED
        elif tl_class == 2:
            print ('Yellow light; Prob:',det_prob)
            return TrafficLight.YELLOW
        elif tl_class == 3:
            print ('Green light; Prob:',det_prob)
            return TrafficLight.GREEN
        else:
            return TrafficLight.UNKNOWN
