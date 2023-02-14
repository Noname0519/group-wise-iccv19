import os
import xml.etree.ElementTree as ET

def is_segm(xml_path):
    x = ET.parse(xml_path)
    s = x.find("segmented").text

    if int(s) != 0:
        return xml_path

    return False

def write_in(path, content):
    if not os.path.exists(path):
        f = open(path, "w")
        f.write(content + '\n')
    else:
        f = open(path, "a")
        f.write(content+'\n')
    f.close()


root_dir = "/root/autodl-tmp/cmy/dataset/PASCAL_VOC_2012/VOCdevkit/VOC2012/"
# Label file
annotations_root = os.path.join(root_dir, "Annotations")

# Get the xml file related to segmentation
# Segmentation
txt_name = "train.txt"
txt_path = os.path.join(root_dir, "ImageSets", "Segmentation", txt_name)  # train.txt

# /root/autodl-tmp/cmy/dataset/PASCAL_VOC_2012/VOCdevkit/VOC2012/ImageSets/Segmentation/train.txt
assert os.path.exists(txt_path), "Not found {} file.".format(txt_name)

# Load the xml file into the list
with open(txt_path) as xr:
    xml_list = [os.path.join(annotations_root, line.strip() + ".xml")
                     for line in xr.readlines()]

s_xml_list = list()
# Get the segmentation file list

for x in xml_list:
    ret = is_segm(x)
    # This image can be used for segmentation
    if ret is not False:
        s_xml_list.append(ret)
    else:
        continue

# Process the segmentation related xml list
for s in s_xml_list:
    print("s: "+s)
    # Check object->name
    tree = ET.parse(s)
    obj_list = tree.findall("object")

    file_name = tree.find("filename")

    for obj in obj_list:
        cls = obj.find("name").text
        print("cls: ", cls)
        # Write the xml file
        #cls_file = str(cls) + "_xml" + ".txt"

        # Write the image file
        img_file = str(cls) + ".txt"
        gt_file = str(cls) + "_gt.txt"
        img_path = root_dir + 'SegmentationClass/'
        gt_path = root_dir + 'JPEGImages/'

        # imgs = [x for x in os.listdir(img_path) if (x[-3:] == 'png') or (x[-3:] == 'jpg')]
        # gts = [x for x in os.listdir(gt_path) if (x[-3:] == 'png') or (x[-3:] == 'jpg')]

        img_name = os.path.join(img_path, file_name.text[:-3] + 'png')

        gt_name = os.path.join(gt_path, file_name.text[:-3] + 'png')

        img_dic = os.path.join("data/", img_file)
        write_in(img_dic, img_name)
        gt_dic = os.path.join("data/", gt_file)
        write_in(gt_dic, gt_name)
        # cls_dic = os.path.join("data/", cls_file)
        # print("cls_dic: ", cls_dic)




