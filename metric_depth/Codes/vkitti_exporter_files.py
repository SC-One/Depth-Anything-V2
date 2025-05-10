import os
from pathlib import Path
from typing import List

def get_image_pairs_str(parent_dir: str) -> List[str]:
    """
    Recursively find all rgb_*.jpg under parent_dir, replace the `/rgb/…rgb_*.jpg`
    with the matching `/depth/…depth_*.png`, and return lines like:
        "path/to/rgb_00001.jpg path/to/depth_00001.png"
    """
    base = Path(parent_dir)
    result_list: List[str] = []

    for rgb_path in base.rglob("rgb_*.jpg"):
        rgb_str = str(rgb_path)
        # only consider those in an "rgb" folder
        if os.sep + "rgb" + os.sep not in rgb_str:
            continue

        # build the depth path by string‑replacement
        depth_str = (
            rgb_str
            .replace(os.sep + "rgb" + os.sep, os.sep + "depth" + os.sep)
            .replace("rgb_", "depth_")      # filename swap
            .rsplit(".", 1)[0] + ".png"     # .jpg -> .png
        )
        if Path(depth_str).exists():
            result_list.append(f"{rgb_str} {depth_str}")

    return result_list

if __name__ == "__main__":
    parent = "G:/Dataset/vikitti/vkitti_2.0.3"
    pairs = get_image_pairs_str(parent)
    pairs.sort()

    with open("all_pairs.txt", "w", encoding="utf-8") as f:
        for line in pairs:
            f.write(line + "\n")

    print(f"Found {len(pairs)} pairs. Sample:\n", pairs[:5])
