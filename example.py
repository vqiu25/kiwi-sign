# Built in packages
import math
import sys

# Matplotlib will need to be installed if it isn't already. This is the only package allowed for this base part of the
# assignment.
from matplotlib import pyplot
from matplotlib.patches import Rectangle

# import our basic, light-weight png reader library
import imageIO.png

# Define constant and global variables
TEST_MODE = False  # Please, DO NOT change this variable!


def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows,
     rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value


def createInitializedGreyscalePixelArray(image_width, image_height, initValue=0):
    new_pixel_array = []
    for _ in range(image_height):
        new_row = []
        for _ in range(image_width):
            new_row.append(initValue)
        new_pixel_array.append(new_row)

    return new_pixel_array


###########################################
### You can add your own functions here ###
###########################################


def RGBtoGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height):
    result_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)
    for row in range(image_height):
        for col in range(image_width):
            result_array[row][col] = round(
                0.3 * px_array_r[row][col]
                + 0.6 * px_array_g[row][col]
                + 0.1 * px_array_b[row][col]
            )
    return result_array


def stretchContrast(px_array, image_width, image_height):
    result_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)
    size = image_width * image_height
    alpha = size * 0.05
    beta = size * 0.95

    pixelList = []
    # Find unique pixels
    for row in range(image_height):
        for col in range(image_width):
            if px_array[row][col] not in pixelList:
                pixelList.append(px_array[row][col])
    pixelList.sort()

    countList = [0 for i in range(len(pixelList))]
    # Count pixels
    for row in range(image_height):
        for col in range(image_width):
            countList[pixelList.index(px_array[row][col])] += 1

    # Cumulative
    for i in range(1, len(countList)):
        countList[i] += countList[i - 1]

    f_min = 0
    f_max = 255
    # Find f_min
    for i in range(len(countList)):
        if countList[i] > alpha:
            f_min = pixelList[i]
            break
    # Find f_max
    for j in range(len(countList) - 1, -1, -1):
        if countList[j] < beta:
            f_max = pixelList[j]
            break

    # print(f"(f_min)={f_min}, (f_max)={f_max}")

    # Perform linear mapping
    for row in range(image_height):
        for col in range(image_width):
            result = (255 / (f_max - f_min)) * (px_array[row][col] - f_min)
            if result < 0:
                result_array[row][col] = 0
            elif result > 255:
                result_array[row][col] = 255
            else:
                result_array[row][col] = result

    return result_array


def applyHorizontalFilter(px_array, image_width, image_height):

    filtered_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)

    horizontal_filter = [[3, 0, -3], [10, 0, -10], [3, 0, -3]]

    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            filtered_value = 0.0
            for fi in range(-1, 2):
                for fj in range(-1, 2):
                    filtered_value += (
                        px_array[i + fi][j + fj] *
                        horizontal_filter[fi + 1][fj + 1]
                    )
            filtered_array[i][j] = float(filtered_value / 32)

    return filtered_array


def applyVerticalFilter(px_array, image_width, image_height):

    filtered_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)

    vertical_filter = [[3, 10, 3], [0, 0, 0], [-3, -10, -3]]

    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            filtered_value = 0.0
            for fi in range(-1, 2):
                for fj in range(-1, 2):
                    filtered_value += (
                        px_array[i + fi][j + fj] *
                        vertical_filter[fi + 1][fj + 1]
                    )
            filtered_array[i][j] = float(filtered_value / 32)

    return filtered_array


def applyFilter(horizontal, vertical, image_width, image_height):
    result_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            result_array[i][j] = abs(horizontal[i][j]) + abs(vertical[i][j])

    return result_array


def applyMeanFilter(px_array, image_width, image_height, window_size):
    result_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)
    window_half = window_size // 2

    for row in range(window_half, image_height - window_half):
        for col in range(window_half, image_width - window_half):
            result = 0
            for i in range(-window_half, window_half+1):
                for j in range(-window_half, window_half+1):
                    result += px_array[row + i][col + j]
            result_array[row][col] = abs(float(result / 25))

    return result_array


def simpleThreshold(px_array, image_width, image_height, threshold):
    result_array = createInitializedGreyscalePixelArray(
        image_width, image_height, 0)

    for row in range(image_height):
        for col in range(image_width):
            if px_array[row][col] < threshold:
                result_array[row][col] = 0
            else:
                result_array[row][col] = 255

    return result_array


def dilation(px_array, image_width, image_height, kernel):
    result_array = createInitializedGreyscalePixelArray(image_width, image_height, 0)

    kernel_half = len(kernel)//2

    for row in range(image_height):
        for col in range(image_width):
            hit = False
            # If the pixel is not 0 then skip it
            if px_array[row][col] > 0 and kernel[2][2] == 1:
                result_array[row][col] = 255
                continue

            for i in range(-kernel_half, kernel_half+1):
                for j in range(-kernel_half, kernel_half+1):
                    # Going through the neighbours, ignore pixels outside of the border
                    if (0 <= row + i < image_height and 0 <= col + j < image_width):
                        # If the pixel is not 0 and kernel is 1 then it is a hit, once hit break
                        if (kernel[i + kernel_half][j + kernel_half]== 1 and px_array[row + i][col + j] > 0):
                            hit = True
                            break
                if hit:
                    break

            if hit:
                result_array[row][col] = 255

    return result_array


def erosion(px_array, image_width, image_height, kernel):
    result_array = createInitializedGreyscalePixelArray(image_width,image_height,)

    kernel_half = len(kernel)//2

    for row in range(image_height):
        for col in range(image_width):
            fit = True

            for i in range(-kernel_half, kernel_half+1):
                for j in range(-kernel_half, kernel_half+1):
                    if (0 <= row + i < image_height and 0 <= col + j < image_width):
                        # If the pixel is 0 but kernel is 1 then not fit, once not fit break
                        if (kernel[i + kernel_half][j + kernel_half] == 1 and px_array[row + i][col + j] == 0):
                            fit = False
                            break
                    else:
                        if (kernel[i + kernel_half][j + kernel_half] == 1):
                            fit = False
                            break
                if not fit:
                    break

            if fit:
                result_array[row][col] = 255

    return result_array


def connectedComponents(px_array, image_width, image_height):
    components = []
    visited = createInitializedGreyscalePixelArray(image_width, image_height, False)
    queue = []

    for row in range(image_height):
        for col in range(image_width):
            if not visited[row][col] and px_array[row][col] != 0:
                queue.append((row, col))
                visited[row][col] = True
                min_x, min_y, max_x, max_y = col, row, 0, 0

                # BFS, enqueue if pixel not 0 and not visited
                while queue:
                    row, col = queue.pop(0)
                    min_x = min(min_x, col)
                    min_y = min(min_y, row)
                    max_x = max(max_x, col)
                    max_y = max(max_y, row)

                    # Left
                    try:
                        if not visited[row][col-1] and px_array[row][col-1] != 0:
                            queue.append((row, col-1))
                            visited[row][col-1] = True
                    except IndexError:
                        pass

                    # Right
                    try:
                        if not visited[row][col+1] and px_array[row][col+1] != 0:
                            queue.append((row, col+1))
                            visited[row][col+1] = True
                    except IndexError:
                        pass

                    # Up
                    try:
                        if not visited[row-1][col] and px_array[row-1][col] != 0:
                            queue.append((row-1, col))
                            visited[row-1][col] = True
                    except IndexError:
                        pass

                    # Down
                    try:
                        if not visited[row+1][col] and px_array[row+1][col] != 0:
                            queue.append((row+1, col))
                            visited[row+1][col] = 1
                    except IndexError:
                        pass

                # Check for coin
                diameter_x = max_x-min_x
                diameter_y = max_y-min_y
                # Minimum size threshold to filter out little noise
                threshold_size = 100
                # x and y should be within 5% of each other
                margin = 0.05
                if diameter_x*(1-margin) <= diameter_y < diameter_x*(1+margin) and diameter_x > threshold_size and diameter_y > threshold_size:
                    components.append((min_x, min_y, max_x, max_y))

    return components


# This is our code skeleton that performs the coin detection.


def main(input_path, output_path):
    # This is the default input image, you may change the 'image_name' variable to test other images.
    image_name = "easy_case_6"
    input_filename = f"./Images/easy/{image_name}.png"
    if TEST_MODE:
        input_filename = input_path

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    image_width, image_height, px_array_r, px_array_g, px_array_b = readRGBImageToSeparatePixelArrays(input_filename)

    ###################################
    ### STUDENT IMPLEMENTATION Here ###
    ###################################

    px_array = RGBtoGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    px_array = stretchContrast(px_array, image_width, image_height)

    horizontalFiltered = applyHorizontalFilter(px_array, image_width, image_height)
    verticalFiltered = applyVerticalFilter(px_array, image_width, image_height)
    px_array = applyFilter(horizontalFiltered, verticalFiltered, image_width, image_height)

    window_size = 5
    px_array = applyMeanFilter(px_array, image_width, image_height, window_size)
    px_array = applyMeanFilter(px_array, image_width, image_height, window_size)
    px_array = applyMeanFilter(px_array, image_width, image_height, window_size)

    px_array = simpleThreshold(px_array, image_width, image_height, 22)

    kernel = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]

    # Close the image
    px_array = dilation(px_array, image_width, image_height, kernel)
    px_array = erosion(px_array, image_width, image_height, kernel)

    px_array = dilation(px_array, image_width, image_height, kernel)
    px_array = dilation(px_array, image_width, image_height, kernel)
    px_array = dilation(px_array, image_width, image_height, kernel)
    px_array = dilation(px_array, image_width, image_height, kernel)

    px_array = erosion(px_array, image_width, image_height, kernel)
    px_array = erosion(px_array, image_width, image_height, kernel)
    px_array = erosion(px_array, image_width, image_height, kernel)
    px_array = erosion(px_array, image_width, image_height, kernel)

    ############################################
    ### Bounding box coordinates information ###
    # bounding_box[0] = min x
    # bounding_box[1] = min y
    # bounding_box[2] = max x
    # bounding_box[3] = max y
    ############################################

    bounding_box_list = connectedComponents(px_array, image_width, image_height)
    px_array = pyplot.imread(input_filename)

    fig, axs = pyplot.subplots(1, 1)
    axs.imshow(px_array, aspect="equal")

    # Loop through all bounding boxes
    for bounding_box in bounding_box_list:
        bbox_min_x = bounding_box[0]
        bbox_min_y = bounding_box[1]
        bbox_max_x = bounding_box[2]
        bbox_max_y = bounding_box[3]

        bbox_xy = (bbox_min_x, bbox_min_y)
        bbox_width = bbox_max_x - bbox_min_x
        bbox_height = bbox_max_y - bbox_min_y
        rect = Rectangle(
            bbox_xy,
            bbox_width,
            bbox_height,
            linewidth=2,
            edgecolor="r",
            facecolor="none",
        )
        axs.add_patch(rect)

    pyplot.axis("off")
    pyplot.tight_layout()
    default_output_path = f"./output_images/{image_name}_with_bbox.png"
    if not TEST_MODE:
        # Saving output image to the above directory
        pyplot.savefig(default_output_path, bbox_inches="tight", pad_inches=0)

        # Show image with bounding box on the screen
        pyplot.imshow(px_array, cmap="gray", aspect="equal")
        pyplot.show()
    else:
        # Please, DO NOT change this code block!
        pyplot.savefig(output_path, bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    num_of_args = len(sys.argv) - 1

    input_path = None
    output_path = None
    if num_of_args > 0:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        TEST_MODE = True

    main(input_path, output_path)
