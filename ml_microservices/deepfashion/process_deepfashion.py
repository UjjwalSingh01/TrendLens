import os
import re
from collections import defaultdict

def parse_deepfashion_files(file_dir):
    categories, attributes = {}, {}
    with open(os.path.join(file_dir, "list_category_cloth.txt")) as f:
        for i, line in enumerate(f):
            if i < 2: continue
            parts = re.split(r'\s+', line.strip())
            categories[int(parts[0])] = " ".join(parts[1:-1]).lower()

    with open(os.path.join(file_dir, "list_attr_cloth.txt")) as f:
        for i, line in enumerate(f):
            if i < 2: continue
            parts = re.split(r'\s+', line.strip())
            attributes[int(parts[0])] = " ".join(parts[1:-1]).lower()

    image_categories = {}
    with open(os.path.join(file_dir, "list_category_img.txt")) as f:
        for i, line in enumerate(f):
            if i < 2: continue
            parts = re.split(r'\s+', line.strip())
            image_categories[parts[0]] = categories.get(int(parts[1]), "unknown")

    image_attributes = defaultdict(list)
    with open(os.path.join(file_dir, "list_attr_img.txt")) as f:
        for i, line in enumerate(f):
            if i < 2: continue
            parts = re.split(r'\s+', line.strip())
            for idx, val in enumerate(parts[1:], 1):
                if val == "1":
                    image_attributes[parts[0]].append(attributes.get(idx, ""))

    return {
        "categories": categories,
        "attributes": attributes,
        "image_categories": image_categories,
        "image_attributes": dict(image_attributes),
    }
