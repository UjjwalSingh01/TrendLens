import os
import re
from collections import defaultdict

def parse_deepfashion_files(file_dir):
    """Parse all DeepFashion files to extract comprehensive clothing metadata"""
    # 1. Parse category definitions
    categories = {}
    with open(os.path.join(file_dir, "list_category_cloth.txt"), "r") as f:
        for i, line in enumerate(f):
            if i < 2: continue  # Skip headers
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 3:
                cat_id = int(parts[0])
                cat_name = " ".join(parts[1:-1]).lower()
                categories[cat_id] = cat_name

    # 2. Parse attribute definitions
    attributes = {}
    with open(os.path.join(file_dir, "atr_cloth.txt"), "r") as f:
        for i, line in enumerate(f):
            if i < 2: continue  # Skip headers
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 3:
                attr_id = int(parts[0])
                attr_name = " ".join(parts[1:-1]).lower()
                attributes[attr_id] = attr_name

    # 3. Parse image-category mappings
    image_categories = {}
    with open(os.path.join(file_dir, "list_category_img.txt"), "r") as f:
        for i, line in enumerate(f):
            if i < 2: continue  # Skip headers
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 3:
                img_name = parts[0]
                cat_id = int(parts[1])
                image_categories[img_name] = categories.get(cat_id, "unknown")

    # 4. Parse image-attribute mappings
    image_attributes = defaultdict(list)
    with open(os.path.join(file_dir, "atr_img.txt"), "r") as f:
        for i, line in enumerate(f):
            if i < 2: continue  # Skip headers
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 2:
                img_name = parts[0]
                # Attributes are binary flags (1 = present)
                for attr_id, present in enumerate(parts[1:], 1):
                    if present == "1" and attr_id in attributes:
                        image_attributes[img_name].append(attributes[attr_id])

    # 5. Parse bounding boxes
    image_bboxes = {}
    with open(os.path.join(file_dir, "list_bbox.txt"), "r") as f:
        for i, line in enumerate(f):
            if i < 2: continue  # Skip headers
            parts = re.split(r'\s+', line.strip())
            if len(parts) >= 5:
                img_name = parts[0]
                # x1, y1, x2, y2
                bbox = tuple(map(int, parts[1:5]))
                image_bboxes[img_name] = bbox

    # 6. Parse landmarks (optional)
    image_landmarks = {}
    if os.path.exists(os.path.join(file_dir, "list_landmarks.txt")):
        with open(os.path.join(file_dir, "list_landmarks.txt"), "r") as f:
            for i, line in enumerate(f):
                if i < 2: continue
                parts = re.split(r'\s+', line.strip())
                if len(parts) > 1:
                    img_name = parts[0]
                    # Landmarks: [x1, y1, vis1, x2, y2, vis2, ...]
                    landmarks = list(map(int, parts[1:]))
                    image_landmarks[img_name] = landmarks

    return {
        "categories": categories,
        "attributes": attributes,
        "image_categories": image_categories,
        "image_attributes": dict(image_attributes),
        "image_bboxes": image_bboxes,
        "image_landmarks": image_landmarks
    }