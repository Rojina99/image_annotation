"""generate xml for bounding boxes from draw_box.py"""

import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

def write_xml(folder, img, objects, tl, br, savedir):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    image = cv2.imread(img)
    height, width, depth = image.shape
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = img.split('/')[-1]
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)

    for obj, topl, botr in zip(objects, tl, br):
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = obj
        ET.SubElement(ob, 'pose').text = 'unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(topl[0])
        ET.SubElement(bbox, 'ymin').text = str(topl[1])
        ET.SubElement(bbox, 'xmax').text = str(botr[0])
        ET.SubElement(bbox, 'ymax').text = str(botr[1])


    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print= True)
    image_file = img.split('/')[-1]
    if ".png" in image_file:
        save_path = os.path.join(savedir, image_file.replace('png', 'xml'))
    elif ".jpeg" in image_file:
        save_path = os.path.join(savedir, image_file.replace('jpeg', 'xml'))
    elif ".jpg" in image_file:
        save_path = os.path.join(savedir, image_file.replace('jpg', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)
    # return xml_str

if __name__ == '__main__':
    folder = 'images'
    # img = [im for im in os.scandir('images') if '000001' in im.name][0]
    ing = [im for im in os.walk('images') if '000001' in im.name][0]
    objects = ['fidget_spinner']
    tl = [(10, 10)]
    br= [(100, 100)]
    savedir = 'annotations'
    write_xml(folder, img, objects, tl, br, savedir)

