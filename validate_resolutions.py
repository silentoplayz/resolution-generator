import math

valid_resolutions = []
invalid_resolutions = []


def get_integer_input(prompt, min_value=None, max_value=None, default_value=None):
    """Helper function to get integer input from the user."""
    while True:
        value_str = input(prompt)
        if not value_str and default_value is not None:
            return default_value
        try:
            value = int(value_str)
            if (min_value is not None and value < min_value) or (
                max_value is not None and value > max_value
            ):
                print(f"Please enter a value between {min_value} and {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def get_aspect_ratio_input(prompt, default_value=""):
    """Helper function to get a valid aspect ratio input from the user."""
    while True:
        ratio = input(prompt)
        if not ratio:
            return default_value
        parts = ratio.split(":")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            print(
                "Please enter a valid aspect ratio format (e.g., 16:9) or leave blank."
            )
            continue
        return ratio


def get_aspect_ratio(width, height):
    """Helper function to calculate the aspect ratio."""
    gcd = math.gcd(width, height)
    return f"{width//gcd}:{height//gcd}"


def get_orientation(width, height):
    """Determines the orientation of a resolution based on its width and height."""
    if width > height:
        return "Horizontal"
    elif width < height:
        return "Vertical"
    else:
        return "Square"


def aspect_ratio_to_float(ratio):
    """Converts an aspect ratio string (e.g., '16:9') to a float (e.g., 1.7777)."""
    width, height = map(int, ratio.split(":"))
    return width / height


def format_float(value):
    """Formats a float to a string, removing unnecessary trailing zeros and decimal points."""
    str_value = "{:.4f}".format(value)
    return str_value.rstrip("0").rstrip(".") if "." in str_value else str_value


def format_pixel_count(value):
    """Formats a number with commas."""
    return "{:,}".format(value)


def is_within_aspect_ratio_range(width, height, min_ratio, max_ratio):
    """Check if the given width and height are within the specified aspect ratio range."""
    current_ratio = aspect_ratio_to_float(get_aspect_ratio(width, height))
    return min_ratio <= current_ratio <= max_ratio


def populate_resolutions():
    global valid_resolutions, invalid_resolutions
    valid_resolutions_set = set()
    invalid_resolutions_set = set()

    min_ratio, max_ratio = 0, float("inf")  # Default values
    if aspect_ratio_range:
        min_ratio, max_ratio = map(aspect_ratio_to_float, aspect_ratio_range.split("-"))

    for width in range(start_resolution, end_resolution + 1, increment):
        for height in range(
            width, end_resolution + 1, increment
        ):  # Start from width to avoid duplicates
            aspect_ratio = get_aspect_ratio(width, height)
            orientation = get_orientation(width, height)
            if width * height <= max_pixel_limit and width * height >= min_pixel_limit:
                if (
                    (not filter_aspect_ratio or aspect_ratio == filter_aspect_ratio)
                    and (not orientation_filter or orientation == orientation_filter)
                    and is_within_aspect_ratio_range(
                        width, height, min_ratio, max_ratio
                    )
                ):
                    valid_resolutions_set.add((width, height))
                    if width != height:
                        valid_resolutions_set.add((height, width))
            else:
                invalid_resolutions_set.add((width, height))
                if width != height:
                    invalid_resolutions_set.add((height, width))

    valid_resolutions = list(valid_resolutions_set)
    invalid_resolutions = list(invalid_resolutions_set)


def upscale_downscale_percentage_for_sort(base_resolution, target_resolution):
    """Calculate the upscale percentage from the base resolution to the target resolution."""
    base_pixels = base_resolution[0] * base_resolution[1]
    target_pixels = target_resolution[0] * target_resolution[1]
    upscale_percent = ((target_pixels / base_pixels) * 100) - 100
    return upscale_percent


def sort_resolutions(method, order):
    global valid_resolutions, invalid_resolutions
    base_res = (start_resolution, start_resolution)

    key_map = {
        "width": lambda x: x[0],
        "height": lambda x: x[1],
        "average": lambda x: (x[0] + x[1]) / 2,
        "pixels": lambda x: x[0] * x[1],
        "aspect_ratio": lambda x: abs(
            aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])) - 1
        )
        if order == "closest"
        else aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])),
        "upscale": lambda x: upscale_downscale_percentage_for_sort(base_res, x),
    }
    valid_resolutions.sort(
        key=key_map[method], reverse=(order != "asc" and order != "closest")
    )
    invalid_resolutions.sort(
        key=key_map[method], reverse=(order != "asc" and order != "closest")
    )


def upscale_downscale_percentage(base_resolution, target_resolution):
    """Calculate the upscale/downscale percentage from the base resolution to the target resolution."""
    base_pixels = base_resolution[0] * base_resolution[1]
    target_pixels = target_resolution[0] * target_resolution[1]
    end_pixels = end_resolution * end_resolution

    upscale_percent = ((target_pixels / base_pixels) * 100) - 100
    downscale_percent = 100 - ((target_pixels / end_pixels) * 100)

    return upscale_percent, downscale_percent


def display_and_save_results():
    base_res = (start_resolution, start_resolution)
    end_res = (end_resolution, end_resolution)
    with open("resolutions.txt", "w") as file:
        file.write("Constraints Used:\n")
        file.write(f"Starting Resolution: {start_resolution}\n")
        file.write(f"Ending Resolution: {end_resolution}\n")
        file.write(f"Increment/Multiple: {increment}\n")
        file.write(f"Maximum Pixel Limit: {max_pixel_limit}\n")
        if filter_aspect_ratio:
            file.write(f"Aspect Ratio Filter: {filter_aspect_ratio}\n")
        file.write("\n")

        file.write("Valid Resolutions:\n")
        for resolution in valid_resolutions:
            aspect_ratio_str = get_aspect_ratio(resolution[0], resolution[1])
            aspect_ratio_float = format_float(aspect_ratio_to_float(aspect_ratio_str))
            total_pixels = resolution[0] * resolution[1]
            formatted_pixels = format_pixel_count(total_pixels)
            megapixels = total_pixels / 1_000_000  # Calculate Megapixel value
            orientation = get_orientation(resolution[0], resolution[1])
            upscale_percent, downscale_percent = upscale_downscale_percentage(
                base_res, resolution
            )

            # Format the upscale and downscale percentages based on their values
            if upscale_percent % 1 == 0:  # Check if it's a whole number
                upscale_display = (
                    f"{int(upscale_percent)}% upscale of {base_res[0]}x{base_res[1]}"
                )
            else:
                upscale_display = (
                    f"{upscale_percent:.3f}% upscale of {base_res[0]}x{base_res[1]}"
                )

            if downscale_percent % 1 == 0:  # Check if it's a whole number
                downscale_display = (
                    f"{int(downscale_percent)}% downscale of {end_res[0]}x{end_res[1]}"
                )
            else:
                downscale_display = (
                    f"{downscale_percent:.3f}% downscale of {end_res[0]}x{end_res[1]}"
                )

            file.write(
                f"Resolution: {resolution[0]}x{resolution[1]} | Aspect Ratio: {aspect_ratio_str} ({orientation}) | Aspect Ratio Decimal: {aspect_ratio_float} | {formatted_pixels} Pixels ({megapixels:.2f} MP) | {upscale_display} | {downscale_display}\n"
            )

        file.write("\nInvalid Resolutions (Exceeding Maximum Pixel Limit):\n")
        for resolution in invalid_resolutions:
            aspect_ratio_str = get_aspect_ratio(resolution[0], resolution[1])
            aspect_ratio_float = format_float(aspect_ratio_to_float(aspect_ratio_str))
            total_pixels = resolution[0] * resolution[1]
            formatted_pixels = format_pixel_count(total_pixels)
            megapixels = total_pixels / 1_000_000  # Calculate Megapixel value
            orientation = get_orientation(resolution[0], resolution[1])

            upscale_percent, downscale_percent = upscale_downscale_percentage(
                base_res, resolution
            )

            # Format the upscale and downscale percentages based on their values
            if upscale_percent % 1 == 0:  # Check if it's a whole number
                upscale_display = (
                    f"{int(upscale_percent)}% upscale of {base_res[0]}x{base_res[1]}"
                )
            else:
                upscale_display = (
                    f"{upscale_percent:.3f}% upscale of {base_res[0]}x{base_res[1]}"
                )

            if downscale_percent % 1 == 0:  # Check if it's a whole number
                downscale_display = (
                    f"{int(downscale_percent)}% downscale of {end_res[0]}x{end_res[1]}"
                )
            else:
                downscale_display = (
                    f"{downscale_percent:.3f}% downscale of {end_res[0]}x{end_res[1]}"
                )

            file.write(
                f"Resolution: {resolution[0]}x{resolution[1]} | Aspect Ratio: {aspect_ratio_str} ({orientation}) | Aspect Ratio Decimal: {aspect_ratio_float} | {formatted_pixels} Pixels ({megapixels:.2f} MP) | {upscale_display} | {downscale_display}\n"
            )


def menu(title, options, actions):
    while True:
        print(f"\n{title}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = get_integer_input("Enter your choice: ", 1, len(options))
        if choice in actions:
            actions[choice]()
        else:
            break


def main_menu():
    menu_options = [
        "Sort by width",
        "Sort by height",
        "Sort by average of width and height",
        "Sort by total number of pixels",
        "Sort by aspect ratio",
        "Sort by upscale percentage",
        "Choose new parameters",
        "Exit program",
    ]
    menu_actions = {
        1: lambda: sort_menu("width"),
        2: lambda: sort_menu("height"),
        3: lambda: sort_menu("average"),
        4: lambda: sort_menu("pixels"),
        5: lambda: sort_menu("aspect_ratio"),
        6: lambda: sort_menu("upscale"),
        7: get_user_input,
        8: exit,
    }
    menu("Choose a sorting method:", menu_options, menu_actions)


def sort_menu(method):
    menu_options = ["Ascending", "Descending", "Back to main menu"]
    if method == "aspect_ratio":
        menu_options.insert(1, "Closest to 1:1 first")
    menu_actions = {
        1: lambda: (sort_resolutions(method, "asc"), display_and_save_results(), print_saved_message()),
        2: lambda: (sort_resolutions(method, "desc" if method != "aspect_ratio" else "closest"), display_and_save_results(), print_saved_message()),
        3: main_menu
    }
    menu(f"Sort by {method}:", menu_options, menu_actions)

def print_saved_message():
    print("Results have been saved to resolutions.txt!")


def get_user_input():
    global start_resolution, end_resolution, increment, max_pixel_limit, min_pixel_limit, filter_aspect_ratio, orientation_filter, aspect_ratio_range
    start_resolution = get_integer_input(
        "Enter the starting resolution (e.g., 512): ", default_value=512
    )
    end_resolution = get_integer_input(
        "Enter the ending resolution (e.g., 2048): ",
        min_value=start_resolution,
        default_value=2048,
    )
    increment = get_integer_input(
        "Enter the increment/multiple (e.g., 64): ", default_value=64
    )
    max_pixel_limit = get_integer_input(
        "Enter the Maximum Pixel Limit (e.g., 1048576): ", default_value=1048576
    )
    min_pixel_limit = get_integer_input(
        "Enter the Minimum Pixel Limit (e.g., 262144): ", default_value=262144
    )
    filter_aspect_ratio = get_aspect_ratio_input(
        "Enter a specific aspect ratio to filter by (e.g., 16:9) or leave blank: ",
        default_value="",
    )
    orientation_filter = input(
        "Filter by orientation (Horizontal, Vertical, Square) or leave blank: "
    ).capitalize()

    while True:
        aspect_ratio_range = input(
            "Enter a custom aspect ratio range (e.g., 4:3-16:9) or leave blank: "
        )
        if not aspect_ratio_range or is_valid_aspect_ratio_range(aspect_ratio_range):
            break
        print("Invalid aspect ratio range format. Please use the format '4:3-16:9'.")

    populate_resolutions()


if __name__ == "__main__":
    get_user_input()
    main_menu()
