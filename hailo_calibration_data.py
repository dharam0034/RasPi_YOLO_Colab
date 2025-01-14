from PIL import Image
import os
import argparse
from tqdm import tqdm
import random

def parse_arguments():
    parser = argparse.ArgumentParser(description="YOLO trainer with PIL")
    parser.add_argument("--data_dir", type=str, required=True, help="The dataset path")
    parser.add_argument("--target_dir", type=str, default="calib", help="The target directory to save processed images")
    parser.add_argument("--image_size", type=int, default=640, help="Input image size")
    parser.add_argument("--num_images", type=int, default=1024, help="Number of calibration images")
    parser.add_argument("--split", type=str, default='val', help="data split to use")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Ensure target directory exists
    target_dir_path = os.path.join(args.data_dir, args.target_dir)
    os.makedirs(target_dir_path, exist_ok=True)

    split_file = os.path.join(args.data_dir, f"{args.split}.txt")

    with open(split_file, "r") as f:
        # Remove the leading ./ and join with root_dir
        all_image_paths = [
            os.path.join(args.data_dir, line.strip().lstrip("./"))
            for line in f.readlines()
        ]

    random.shuffle(all_image_paths)
    images_list = all_image_paths[:args.num_images]

    print("Creating calibration data for Hailo export")
    for idx, filename in tqdm(enumerate(images_list)):
        filepath = os.path.join(args.data_dir, filename)

        # Open the image using PIL
        with Image.open(filepath) as img:
            # Convert image to RGB (in case it's not)
            img = img.convert("RGB")

            # Resize while maintaining aspect ratio
            img.thumbnail((args.image_size, args.image_size))

            # Calculate cropping dimensions for center crop
            left = (img.width - args.image_size) / 2
            top = (img.height - args.image_size) / 2
            right = left + args.image_size
            bottom = top + args.image_size

            # Perform center crop
            crop_img = img.crop((left, top, right, bottom))

            # Save the cropped image as a .jpg in the target directory
            output_filepath = os.path.join(target_dir_path, f"processed_{idx}.jpg")
            crop_img.save(output_filepath, format="JPEG")


if __name__ == "__main__":
    main()
