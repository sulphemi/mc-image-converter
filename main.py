from PIL import Image;
from collections import defaultdict;
import os;
import math;


def blocks_to_rgb() -> dict:
    folder = "./blocks/";
    color_map = defaultdict(list);

    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img_path = os.path.join(folder, filename);
            img = Image.open(img_path);
            width, height = img.size;

            # check if the image's aspect ratio is not 1:1
            if (width != height):
                continue;

            # convert image to RGBA to check transparency
            img = img.convert("RGBA");
            pixels = img.getdata();

            # Check if image has pixels whose transparency is not fully opaque
            if any(pixel[3] != 255 for pixel in pixels):
                continue;

            # calculate the average rgb of the image as a tuple
            avg_rgb = tuple(sum(x[i] for x in pixels) // len(pixels) for i in range(3));

            # append the filename to color_map[rgb]
            color_map[avg_rgb].append(filename);

    return color_map;


def color_diff(rgb1: tuple[int], rgb2: tuple[int]) -> int:
    # Return the Euclidean distance between the two colors
    return int(math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2))));


match_memo = {};
def find_match(color_map: dict, rgb: tuple[int]) -> str:
    # find the one with minimum color distance
    if (rgb in match_memo):
        return match_memo[rgb];
    curr_min = 99999999999;
    curr_match = None;

    for i in color_map:
        if ((d := color_diff(i, rgb)) < curr_min):
            curr_min = d;
            curr_match = color_map[i];

    match_memo[rgb] = curr_match;
    return curr_match;


def create_image_grid(directory, image_filenames):
    # determine the number of rows and columns in the grid
    rows = len(image_filenames)
    cols = len(image_filenames[0])

    # Open the first image to get its size
    sample_image = Image.open(os.path.join(directory, image_filenames[0][0]));
    width, height = sample_image.size;

    # create a new image with the appropriate size
    big_image = Image.new('RGB', (cols * width, rows * height));

    # paste each image into the big image
    for row in range(rows):
        for col in range(cols):
            img = Image.open(os.path.join(directory, image_filenames[row][col]));
            big_image.paste(img, (col * width, row * height));

    return big_image;


def main():
    color_map = blocks_to_rgb();

    image_path = "./Untitled304.png";
    img = Image.open(image_path);

    pixels = img.load();
    width, height = img.size;

    grid = [[None for _ in range(width)] for _ in range(height)];

    for y in range(height):
        for x in range(width):
            print(x, y);
            pixel = (pixels[x, y])[:3];
            grid[y][x] = find_match(color_map, pixel)[0];


    directory = './blocks/';
    big_image = create_image_grid(directory, grid);
    big_image.save('out.png');

if (__name__ == "__main__"):
    main();