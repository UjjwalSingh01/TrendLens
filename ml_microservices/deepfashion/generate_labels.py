import os
from .process_deepfashion import parse_deepfashion_files

def generate_labels():
    """Generate comprehensive clothing labels from DeepFashion"""
    deepfashion_dir = os.path.dirname(os.path.abspath(__file__))
    data = parse_deepfashion_files(deepfashion_dir)
    
    # Combine categories and attributes
    all_labels = set()
    
    # Add all category names
    all_labels.update(data["categories"].values())
    
    # Add all attribute names
    all_labels.update(data["attributes"].values())
    
    # Add combined category-attribute pairs
    for img, attrs in data["image_attributes"].items():
        category = data["image_categories"].get(img, "")
        for attr in attrs:
            # Create combinations like "floral dress", "long-sleeve shirt"
            all_labels.add(f"{attr} {category}")
    
    # Write to file
    output_path = os.path.join(os.path.dirname(deepfashion_dir), "clip_labels.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(sorted(all_labels)))
    
    print(f"Generated {len(all_labels)} clothing labels")

if __name__ == "__main__":
    generate_labels()