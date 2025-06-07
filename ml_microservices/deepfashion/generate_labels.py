import os
from .process_deepfashion import parse_deepfashion_files

def generate_labels():
    """Generate comprehensive clothing labels from DeepFashion"""
    # FIXED: Get correct deepfashion directory
    deepfashion_dir = os.path.join(os.path.dirname(__file__), "deepfashion")
    
    if not os.path.exists(deepfashion_dir):
        raise FileNotFoundError(f"DeepFashion directory not found at {deepfashion_dir}")
    
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
    output_path = os.path.join(os.path.dirname(__file__), "clip_labels.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(sorted(all_labels)))
    
    print(f"Generated {len(all_labels)} clothing labels")

if __name__ == "__main__":
    generate_labels()