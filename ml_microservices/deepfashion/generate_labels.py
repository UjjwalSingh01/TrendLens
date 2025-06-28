import os
from deepfashion.process_deepfashion import parse_deepfashion_files

def generate_labels():
    deepfashion_dir = os.path.join(os.path.dirname(__file__), "labels")
    data = parse_deepfashion_files(deepfashion_dir)
    labels = set()
    labels.update(data["categories"].values())
    labels.update(data["attributes"].values())
    for img, attrs in data["image_attributes"].items():
        cat = data["image_categories"].get(img, "")
        for attr in attrs:
            labels.add(f"{attr} {cat}")
    output_path = os.path.join(os.path.dirname(__file__), "..", "models", "clip_labels.txt")
    with open(output_path, "w") as f:
        f.writelines([l.strip() + "\n" for l in sorted(labels)])
    print(f"✅ Generated {len(labels)} labels")
