import numpy as np
import os
import itertools
import threading
import time

train_labels_path = "datasets/train/labels"
valid_labels_path = "datasets/valid/labels"
test_labels_path = "datasets/test/labels"

done = False


def convert_to_bbox(segmentations):
    # Function to convert segmentations to bounding box (BBox)
    bboxes = []
    for seg in segmentations:
        seg_array = np.array(seg).reshape(-1, 2)
        min_x, min_y = np.min(seg_array, axis=0)
        max_x, max_y = np.max(seg_array, axis=0)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        width = max_x - min_x
        height = max_y - min_y
        bbox = [center_x, center_y, width, height]
        bboxes.append(bbox)
    return bboxes


def animated_loading():
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done:
            break
        print("\rLoading " + c, end="")
        time.sleep(0.1)


def process_annotations(folder_path, success_message):
    global done

    done = False
    t = threading.Thread(target=animated_loading)
    t.start()

    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as file:
                content = file.readlines()

            if not content:
                continue

            segmentations = []
            class_ids = []
            for line in content:
                parts = line.strip().split()
                class_id = parts[0]
                seg = list(map(float, parts[1:]))
                segmentations.append(seg)
                class_ids.append(class_id)

            bboxes = convert_to_bbox(segmentations)
            bbox_file_content = []
            for class_id, bbox in zip(class_ids, bboxes):
                bbox_file_content.append(f"{class_id} {' '.join(map(str, bbox))}\n")

            with open(file_path, "w") as file:
                file.writelines(bbox_file_content)

    finally:
        done = True
        t.join()
        print(success_message)


# Process annotations in train/labels, valid/labels, and test/labels
process_annotations(train_labels_path, "Train Datasets Success!")
process_annotations(valid_labels_path, "Valid Datasets Success!")
process_annotations(test_labels_path, "Test Datasets Success!")
print("\rDone!")
