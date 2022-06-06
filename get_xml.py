from itertools import count
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import glob
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

counter = 1
valid = False
for filename in sorted(glob.glob('/Users/isabel/Downloads/DATASETS/OFA_Dataset/Ell/*.txt')):
    with open(os.path.join("OFA_Dataset/Ell", filename), 'r') as f:
        text = f.read()
        text = text[:-1]
        a = text.split("\t")
        
        centerx = float(a[0])
        centery = float(a[1])
        minor = float(a[2])
        major = float(a[3])

        xmin = centerx - major
        ymax = centery + minor
        xmax = centerx + major
        ymin = centery - minor

        if(counter == 16235):
            counter = 1
            valid = True

        counter_str = str(counter)
        if(valid):
            if(len(counter_str) == 1):
                n = 'Validation_0000'+str(counter)
            
            if(len(counter_str) == 2):
                n = 'Validation_000'+str(counter)

            if(len(counter_str) == 3):
                n = 'Validation_00'+str(counter)
            
            if(len(counter_str) == 4):
                n = 'Validation_0'+str(counter)
            
            if(len(counter_str) == 5):
                n = 'Validation_'+str(counter)
            
            n_path = '/Users/isabel/Downloads/DATASETS/OFA_Dataset/Ref/'+n+'.jpeg'
            save_name = '/Users/isabel/Downloads/DATASETS/newxmls/'+n+'.xml'

        else:
            if(len(counter_str) == 1):
                n = 'Training_0000'+str(counter)
            
            if(len(counter_str) == 2):
                n = 'Training_000'+str(counter)

            if(len(counter_str) == 3):
                n = 'Training_00'+str(counter)
            
            if(len(counter_str) == 4):
                n = 'Training_0'+str(counter)
            
            if(len(counter_str) == 5):
                n = 'Training_'+str(counter)

            n_path = '/Users/isabel/Downloads/DATASETS/OFA_Dataset/Ref/'+n+'.jpeg'
            save_name = '/Users/isabel/Downloads/DATASETS/newxmls/'+n+'.xml'
        
        root = ET.Element("annotation")

        folder = ET.SubElement(root, 'folder')
        folder.text = "Ref"

        filenam = ET.SubElement(root, 'filename')
        s = n+'.jpeg'
        filenam.text = s

        path = ET.SubElement(root, 'path')
        path.text = n_path

        source = ET.SubElement(root, 'source')
        ET.SubElement(source, 'database').text = "Unknown"

        size = ET.SubElement(root, 'size')
        ET.SubElement(size, 'width').text = '480'
        ET.SubElement(size, 'height').text = '480'
        ET.SubElement(size, 'depth').text = '1'

        segmented = ET.SubElement(root, 'segmented')
        segmented.text = "0"

        object = ET.SubElement(root, 'object')
        ET.SubElement(object, 'name').text = 'mouse'
        ET.SubElement(object, 'pose').text = 'Unspecified'
        ET.SubElement(object, 'truncated').text = '0'
        ET.SubElement(object, 'difficult').text = '0'

        bndbox = ET.SubElement(object, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(round(xmin))
        ET.SubElement(bndbox, 'ymin').text = str(round(ymin))
        ET.SubElement(bndbox, 'xmax').text = str(round(xmax))
        ET.SubElement(bndbox, 'ymax').text = str(round(ymax))

        tree = ET.ElementTree(root)
        tree.write(save_name)
        print(counter)
        counter += 1




