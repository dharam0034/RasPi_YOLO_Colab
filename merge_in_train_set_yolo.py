import argparse
import os
import shutil
from pathlib import Path

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Merge the valid and test folders of YOLO dataset into train folder. The result is all images and labels are in the train folder.')

    # Input directory argument
    parser.add_argument('--data_dir', type=str, help='Base directory to load images')

    # Parse arguments
    args = parser.parse_args()

    # Define dataset directory and folder paths
    dataset_dir = args.data_dir  # Replace with your dataset path
    test_folder = os.path.join(dataset_dir, "test")
    valid_folder = os.path.join(dataset_dir, "valid")
    train_folder = os.path.join(dataset_dir, "train")
    
    # List of source folders
    source_folders = [test_folder, valid_folder]
    
    print(f"Original dataset has ... ")
    
    # Define paths
    for split in ['train', 'valid', 'test']:
        image_dir = os.path.join(args.data_dir, split, 'images')
        label_dir = os.path.join(args.data_dir, split, 'labels')
        image_count = len([entry for entry in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, entry))])
        label_count = len([entry for entry in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, entry))])
        print(f"{split}: {image_count} images, {label_count} labels")


    # Move files from test and valid to train
    move_files(source_folders, train_folder)

    print(f"After moving the test and valid sets into the train set .. ")

    
    # Define paths
    for split in ['train', 'valid', 'test']:
        image_dir = os.path.join(args.data_dir, split, 'images')
        label_dir = os.path.join(args.data_dir, split, 'labels')
        image_count = len([entry for entry in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, entry))])
        label_count = len([entry for entry in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, entry))])
        print(f"{split}: {image_count} images, {label_count} labels")

def move_files(source_folders, dest_folder, file_types=('*.jpg', '*.jpeg', '*.png')):
    """
    Move images and their corresponding labels from source folders to destination folder.
    
    Args:
        source_folders (list): List of source folder paths (e.g., ['dataset/test', 'dataset/valid'])
        dest_folder (str): Destination folder path (e.g., 'dataset/train')
        file_types (tuple): Tuple of image file extensions to process
    """
    # Convert destination folder to Path object
    dest_path = Path(dest_folder)
    dest_images = dest_path / 'images'
    dest_labels = dest_path / 'labels'
    
    # Create destination directories if they don't exist
    dest_images.mkdir(parents=True, exist_ok=True)
    dest_labels.mkdir(parents=True, exist_ok=True)
    
    for source_folder in source_folders:
        source_path = Path(source_folder)
        source_images = source_path / 'images'
        source_labels = source_path / 'labels'
        
        # Check if source directories exist
        if not source_images.exists() or not source_labels.exists():
            print(f"Skipping {source_folder}: images or labels directory not found")
            continue
        
        # Get all image files
        image_files = []
        for ext in file_types:
            image_files.extend(source_images.glob(ext))   ##########################
        
        # Move each image and its corresponding label
        for img_path in image_files:
            # Get corresponding label file
            label_path = source_labels / f"{img_path.stem}.txt"
            
            # Check if label file exists
            if not label_path.exists():
                print(f"Warning: Label file not found for {img_path.name}")
                continue
            
            # Move image
            shutil.move(str(img_path), dest_images / img_path.name)
            #print(f"Moved image: {img_path.name}")
            
            # Move label
            shutil.move(str(label_path), dest_labels / label_path.name)
            #print(f"Moved label: {label_path.name}")
            
        print(f"Completed moving files from {source_folder}")


if __name__ == "__main__":
    main()
    
