#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 22:10:01 2018

@author: Caroline Pacheco do E. Silva
"""

import os
from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring
import numpy as np
from os.path import join
import sys

## coco classes
YOLO_CLASSES = ('Pedestrian_Pedestrian', 'Pedestrian_Bicycle', 'Vehicle_Car',
 'Vehicle_Motorcycle', 'TrafficLight_Red', 'Vehicle_Bus', 'TrafficLight_Yellow',
  'Vehicle_Unknown', 'TrafficLight_Arrow', 'TrafficLight_Green', 'TrafficLight_RedArrow',
   'TrafficSign_Else', 'TrafficLight_YellowArrow', 'TrafficLight_GreenArrow', 'TrafficSign_Speed')


width = 1920
height = 1080

## converts the normalized positions  into integer positions
def unconvert(class_id, width, height, x, y, w, h):

    xmax = int((x*width) + (w * width)/2.0)
    xmin = int((x*width) - (w * width)/2.0)
    ymax = int((y*height) + (h * height)/2.0)
    ymin = int((y*height) - (h * height)/2.0)
    class_id = int(class_id)
    return (class_id, xmin, xmax, ymin, ymax)


## path
outputs = sys.argv[1]

## converts coco into xml
def xml_transform(classes):
    class_path  = outputs
    #print(class_path)
    ids = list()
    l=os.listdir(class_path)

    check = '.DS_Store' in l
    if check == True:
        l.remove('.DS_Store')

    ids=[x.split('.')[0] for x in l]

    annopath = join(outputs, '%s.txt')

    outpath = join(outputs, '%s.xml')

    for i in range(len(ids)):
        img_id = ids[i]
        node_root = Element('annotation')

        target = (annopath % img_id)
        if os.path.exists(target):
            label_norm= np.loadtxt(target).reshape(-1, 5)

            for i in range(len(label_norm)):
                labels_conv = label_norm[i]
                new_label = unconvert(labels_conv[0], width, height, labels_conv[1], labels_conv[2], labels_conv[3], labels_conv[4])
                node_object = SubElement(node_root, 'object')
                node_name = SubElement(node_object, 'name')
                node_name.text = classes[new_label[0]]

                if (node_name.text == "Pedestrian_Pedestrian" or  node_name.text == "Pedestrian_Bicycle"):
                    node_name.text = "Pedestrian"
                elif (node_name.text == "Vehicle_Car" or  node_name.text == "Vehicle_Motorcycle" or node_name.text == "Vehicle_Bus" or node_name.text == "Vehicle_Unknown"):
                    node_name.text = "Vehicle"
                elif (node_name.text == "TrafficLight_Red" or  node_name.text == "TrafficLight_Yellow" or node_name.text == "TrafficLight_Arrow" or node_name.text == "TrafficLight_Green" or node_name.text == "TrafficLight_RedArrow" or node_name.text == "TrafficLight_YellowArrow" or node_name.text == "TrafficLight_GreenArrow"):
                    node_name.text = "TrafficLight"
                elif (node_name.text == "TrafficSign_Else" or  node_name.text == "TrafficSign_Speed"):
                    node_name.text = "TrafficSign"

                node_bndbox = SubElement(node_object, 'bndbox')
                node_xmin = SubElement(node_bndbox, 'xmin')
                node_xmin.text = str(new_label[1])
                node_ymin = SubElement(node_bndbox, 'ymin')
                node_ymin.text = str(new_label[3])
                node_xmax = SubElement(node_bndbox, 'xmax')
                node_xmax.text =  str(new_label[2])
                node_ymax = SubElement(node_bndbox, 'ymax')
                node_ymax.text = str(new_label[4])

                xml = tostring(node_root, pretty_print=True)
                dom = parseString(xml)

        #print(xml)
        f =  open(outpath % img_id, "wb")
        #f = open(os.path.join(outpath, img_id), "w")
        #os.remove(target)
        f.write(xml)
        f.close()


xml_transform(YOLO_CLASSES)
