import argparse
import os
import random
import shutil

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Shuffles a YOLO dataset where all images and labels are in the train folder, and splits them into valid, and test sets.')

    # Input directory argument
    parser.add_argument('--data_dir', type=str, help='Base directory to load images')

    parser.add_argument('--train_split', type=float, help='Percentage of images to split into the test set',
                        default=0.6)
    parser.add_argument('--val_split', type=float, help='Percentage of images to split into the val set',
                        default=0.1)
    parser.add_argument('--test_split', type=float, help='Percentage of images to split into the test set',
                        default=0.3)
    parser.add_argument('--random_seed', type=int, help='Random seed to ensure it generates same set of random numbers to ensure model consistency',
                        default=42)


    # Parse arguments
    args = parser.parse_args()
    
    shuffle_and_split_dataset(args.data_dir, args.train_split, args.val_split, args.test_split, args.random_seed)


def shuffle_and_split_dataset(data_dir, train_ratio, valid_ratio, test_ratio, random_seed):
    """
    Args:
        data_dir (str): Path to the original dataset directory with images and labels in train subfolder.
        train_ratio (float): Proportion of data for training.
        valid_ratio (float): Proportion of data for validation.
        test_ratio (float): Proportion of data for testing.
        seed (int): Random seed for reproducibility.
    """
    # Set random seed for reproducibility
    random.seed(seed)

    # Define paths
    image_dir = os.path.join(data_dir, 'train', 'images')
    label_dir = os.path.join(data_dir, 'train', 'labels')

    # Validate input directories
    if not (os.path.exists(image_dir) and os.path.exists(label_dir)):
        raise FileNotFoundError("Train images or labels directory not found!")

    # Create output directories
    for split in ['valid', 'test']:
         os.makedirs(os.path.join(data_dir, split, 'images'), exist_ok=True)
         os.makedirs(os.path.join(data_dir, split, 'labels'), exist_ok=True)

    # Get list of image files
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Shuffle the image files
    random.shuffle(image_files)

    # Split dataset
    total_images = len(image_files)
    train_size = int(train_ratio * total_images)
    valid_size = int(valid_ratio * total_images)

    train_files = image_files[:train_size]
    valid_files = image_files[train_size:train_size + valid_size]
    test_files = image_files[train_size + valid_size:]

    # Function to copy files to destination
    def move_files(file_list, split):
        for file_name in file_list:
            # Move image
            src_image = os.path.join(image_dir, file_name)
            dst_image = os.path.join(data_dir, split, 'images', file_name)
            shutil.move(src_image, dst_image)

            # Move corresponding label
            label_name = os.path.splitext(file_name)[0] + '.txt'
            src_label = os.path.join(label_dir, label_name)
            dst_label = os.path.join(data_dir, split, 'labels', label_name)
            if os.path.exists(src_label):
                shutil.move(src_label, dst_label)
            else:
                print(f"Warning: Label file {label_name} not found for image {file_name}")

    # Copy files to respective directories
    move_files(valid_files, 'valid')
    move_files(test_files, 'test')
    
    print(f" Split is successful!!")


    # Define paths
    for split in ['train', 'valid', 'test']:
        image_dir = os.path.join(data_dir, split, 'images')
        label_dir = os.path.join(data_dir, split, 'labels')
        image_count = len([entry for entry in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, entry))])
        label_count = len([entry for entry in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, entry))])
        print(f"{split}: {image_count} images, {label_count} labels")

if __name__ == "__main__":
    main()
    
