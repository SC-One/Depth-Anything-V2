import os
import glob
import random
from .vkitti_exporter_files import get_image_pairs_str

def generate_file_pairs_vkitti(parent_dir):
    return get_image_pairs_str(parent_dir)

def generate_file_pairs_hypersim(parent_dir):
    """
    Generates pairs of tonemap images and corresponding depth HDF5 files from a parent directory structure.

    Args:
        parent_dir (str): Path to the parent directory containing subfolders with image data.

    Returns:
        list: List of strings with paired absolute file paths separated by space.
    """
    parent_dir = os.path.abspath(parent_dir)
    file_pairs = []

    # Iterate through each unique-named folder in the parent directory
    for folder_name in os.listdir(parent_dir):
        unique_folder = os.path.join(parent_dir, folder_name)
        if not os.path.isdir(unique_folder):
            continue

        # Check for images subdirectory
        images_dir = os.path.join(unique_folder, 'images')
        if not os.path.isdir(images_dir):
            continue

        preview_dirs = {}
        geometry_dirs = {}

        # Process each subdirectory in images folder
        for scene_dir in os.listdir(images_dir):
            scene_dir_path = os.path.join(images_dir, scene_dir)
            if not os.path.isdir(scene_dir_path):
                continue

            # Identify camera directories
            if scene_dir.endswith('_final_preview'):
                parts = scene_dir.split('_final_preview', 1)
                if len(parts) != 2 or 'scene_cam_' not in parts[0]:
                    continue
                cam_id = parts[0].split('scene_cam_', 1)[1]
                preview_dirs[cam_id] = scene_dir_path
            elif scene_dir.endswith('_geometry_hdf5'):
                parts = scene_dir.split('_geometry_hdf5', 1)
                if len(parts) != 2 or 'scene_cam_' not in parts[0]:
                    continue
                cam_id = parts[0].split('scene_cam_', 1)[1]
                geometry_dirs[cam_id] = scene_dir_path

        # Find matching camera pairs
        common_cams = set(preview_dirs.keys()) & set(geometry_dirs.keys())
        for cam_id in common_cams:
            # Collect files from both directories
            img_files = glob.glob(os.path.join(preview_dirs[cam_id], 'frame.*.tonemap.jpg'))
            depth_files = glob.glob(os.path.join(geometry_dirs[cam_id], 'frame.*.depth_meters.hdf5'))

            # Create frame number to file mapping
            img_map = {os.path.basename(f).split('.')[1]: f for f in img_files}
            depth_map = {os.path.basename(f).split('.')[1]: f for f in depth_files}

            # Pair matching frames
            common_frames = set(img_map.keys()) & set(depth_map.keys())
            for frame in common_frames:
                pair = f"{os.path.abspath(img_map[frame])} {os.path.abspath(depth_map[frame])}"
                file_pairs.append(pair)

    return sorted(file_pairs)

def split_data(pairs, val_percentage=0.2, random_seed=None, shuffle=False):
    """
    Split data into training and validation sets.
    
    Args:
        pairs: List of data pairs to split
        val_percentage: Percentage of data to use for validation (default: 0.2)
        random_seed: Seed for random number generator for reproducibility (default: None)
        shuffle: Whether to shuffle the data before splitting (default: False)
        
    Returns:
        train_pairs: List of pairs for training
        val_pairs: List of pairs for validation
    """
    if random_seed is not None:
        random.seed(random_seed)
    
    # Create a copy to avoid modifying the original list
    processed_pairs = pairs.copy()
    
    # Shuffle if requested
    if shuffle:
        random.shuffle(processed_pairs)
    
    # Calculate split index
    split_idx = int(len(processed_pairs) * (1 - val_percentage))
    
    # Split the data
    train_pairs = processed_pairs[:split_idx]
    val_pairs = processed_pairs[split_idx:]
    
    return train_pairs, val_pairs

# Example usage
if __name__ == "__main__":
    pairs = generate_file_pairs_hypersim("F:/Dataset/Partial_hypersim_extracted")
    for pair in pairs[0:0]:
        print(pair)
    print(pairs[0])
    print(pairs[1])
    print(pairs[-2])
    print(pairs[-1])