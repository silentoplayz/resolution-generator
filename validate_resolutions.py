import math

valid_resolutions = []
invalid_resolutions = []


def get_integer_input(prompt, min_value=None, max_value=None, default_value=None):
    """
    Helper function to get integer input from the user.

    Args:
        prompt (str): The prompt message to display to the user.
        min_value (int, optional): The minimum allowed value. Defaults to None.
        max_value (int, optional): The maximum allowed value. Defaults to None.
        default_value (int, optional): The default value to return if no input is provided. Defaults to None.

    Returns:
        int: The integer value entered by the user.

    Raises:
        ValueError: If the input is not a valid integer.
    """
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
    valid_resolutions_set = set()  # Set to store unique valid resolutions
    invalid_resolutions_set = set()  # Set to store unique invalid resolutions

    min_ratio, max_ratio = 0, float("inf")  # Default values for aspect ratio range
    if aspect_ratio_range:
        min_ratio, max_ratio = map(aspect_ratio_to_float, aspect_ratio_range.split("-"))  # Convert aspect ratio range to float values

    # Loop through all possible resolutions within the specified range
    for width in range(start_resolution, end_resolution + 1, increment):
        for height in range(width, end_resolution + 1, increment):  # Start from width to avoid duplicates
            aspect_ratio = get_aspect_ratio(width, height)  # Calculate aspect ratio for current resolution
            orientation = get_orientation(width, height)  # Determine orientation (landscape or portrait) for current resolution

            # Check if resolution is within the specified pixel limits
            if width * height <= max_pixel_limit and width * height >= min_pixel_limit:
                # Check if resolution meets the specified filters
                if (
                    (not filter_aspect_ratio or aspect_ratio == filter_aspect_ratio)  # Check if aspect ratio matches the filter or no filter is specified
                    and (not orientation_filter or orientation == orientation_filter)  # Check if orientation matches the filter or no filter is specified
                    and is_within_aspect_ratio_range(width, height, min_ratio, max_ratio)  # Check if aspect ratio is within the specified range
                ):
                    valid_resolutions_set.add((width, height))  # Add valid resolution to set
                    if width != height:
                        valid_resolutions_set.add((height, width))  # Add the same resolution with swapped width and height to handle both orientations
            else:
                invalid_resolutions_set.add((width, height))  # Add invalid resolution to set
                if width != height:
                    invalid_resolutions_set.add((height, width))  # Add the same resolution with swapped width and height to handle both orientations

    valid_resolutions = list(valid_resolutions_set)  # Convert set of valid resolutions to a list
    invalid_resolutions = list(invalid_resolutions_set)  # Convert set of invalid resolutions to a list


def upscale_downscale_percentage_for_sort(base_resolution, target_resolution):
    """Calculate the upscale percentage from the base resolution to the target resolution.

    Args:
        base_resolution (tuple): The base resolution as a tuple of width and height.
        target_resolution (tuple): The target resolution as a tuple of width and height.

    Returns:
        float: The percentage by which the base resolution needs to be upscaled to reach the target resolution.
    """
    base_pixels = base_resolution[0] * base_resolution[1]
    target_pixels = target_resolution[0] * target_resolution[1]
    upscale_percent = ((target_pixels / base_pixels) * 100) - 100
    return upscale_percent


def sort_resolutions(method, order):
    """Sort the valid and invalid resolutions based on the specified method and order.

    Args:
        method (str): The method to use for sorting. Can be "width", "height", "average", "pixels", "aspect_ratio", or "upscale".
        order (str): The order in which to sort. Can be "asc", "desc", or "closest".

    Returns:
        None
    """
    global valid_resolutions, invalid_resolutions
    base_res = (start_resolution, start_resolution)

    # Define a dictionary mapping each sorting method to its corresponding key function
    key_map = {
        "width": lambda x: x[0],  # Sort based on width
        "height": lambda x: x[1],  # Sort based on height
        "average": lambda x: (x[0] + x[1]) / 2,  # Sort based on average of width and height
        "pixels": lambda x: x[0] * x[1],  # Sort based on total number of pixels
        "aspect_ratio": lambda x: abs(aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])) - 1) if order == "closest" else aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])),  # Sort based on aspect ratio, either as absolute difference from 1 or as the actual aspect ratio
        "upscale": lambda x: upscale_downscale_percentage_for_sort(base_res, x),  # Sort based on percentage of upscale/downscale required to reach the base resolution
    }

    # Sort the valid resolutions based on the specified method and order
    valid_resolutions.sort(key=key_map[method], reverse=(order != "asc" and order != "closest"))

    # Sort the invalid resolutions based on the specified method and order
    invalid_resolutions.sort(key=key_map[method], reverse=(order != "asc" and order != "closest"))


def upscale_downscale_percentage(base_resolution, target_resolution):
    """Calculate the upscale/downscale percentage from the base resolution to the target resolution.

    Args:
        base_resolution (tuple): The base resolution as a tuple of width and height.
        target_resolution (tuple): The target resolution as a tuple of width and height.

    Returns:
        tuple: A tuple containing the upscale percentage and downscale percentage.
    """
    base_pixels = base_resolution[0] * base_resolution[1]
    target_pixels = target_resolution[0] * target_resolution[1]
    end_pixels = end_resolution * end_resolution

    upscale_percent = ((target_pixels / base_pixels) * 100) - 100
    downscale_percent = 100 - ((target_pixels / end_pixels) * 100)

    return upscale_percent, downscale_percent


def write_resolution_to_file(file, resolution, base_res, end_res):
    # Get the aspect ratio as a string
    aspect_ratio_str = get_aspect_ratio(resolution[0], resolution[1])
    # Convert the aspect ratio string to a float
    aspect_ratio_float = format_float(aspect_ratio_to_float(aspect_ratio_str))
    # Calculate the total number of pixels in the resolution
    total_pixels = resolution[0] * resolution[1]
    # Format the total pixel count with commas for better readability
    formatted_pixels = format_pixel_count(total_pixels)
    # Calculate the number of megapixels
    megapixels = total_pixels / 1_000_000
    # Determine the orientation of the resolution (landscape or portrait)
    orientation = get_orientation(resolution[0], resolution[1])
    # Calculate the percentage of upscale and downscale from the base resolution
    upscale_percent, downscale_percent = upscale_downscale_percentage(base_res, resolution)

    # Format the upscale and downscale percentages based on their values
    if upscale_percent % 1 == 0:  # Check if it's a whole number
        upscale_display = f"{int(upscale_percent)}% upscale of {base_res[0]}x{base_res[1]}"
    else:
        upscale_display = f"{upscale_percent:.3f}% upscale of {base_res[0]}x{base_res[1]}"

    if downscale_percent % 1 == 0:  # Check if it's a whole number
        downscale_display = f"{int(downscale_percent)}% downscale of {end_res[0]}x{end_res[1]}"
    else:
        downscale_display = f"{downscale_percent:.3f}% downscale of {end_res[0]}x{end_res[1]}"

    # Format the aspect ratio with commas for better readability
    formatted_aspect_ratio = ":".join([format_pixel_count(int(part)) for part in aspect_ratio_str.split(":")])

    # Write the formatted information to the file
    file.write(
        f"Resolution: {resolution[0]}x{resolution[1]} | Aspect Ratio: {formatted_aspect_ratio} ({orientation}) | Aspect Ratio Decimal: {aspect_ratio_float} | {formatted_pixels} Pixels ({megapixels:.2f} MP) | {upscale_display.rstrip('0').rstrip('.')} | {downscale_display.rstrip('0').rstrip('.')}\n"
    )


def display_and_save_results():
    # Set the base and end resolutions
    base_res = (start_resolution, start_resolution)
    end_res = (end_resolution, end_resolution)
    
    # Open the file in write mode
    with open("resolutions.txt", "w") as file:
        # Write the constraints used section
        file.write("Constraints Used:\n")
        file.write(f"Starting Resolution: {format_pixel_count(start_resolution)}\n")
        file.write(f"Ending Resolution: {format_pixel_count(end_resolution)}\n")
        file.write(f"Increment/Multiple: {format_pixel_count(increment)}\n")
        file.write(f"Maximum Pixel Limit: {format_pixel_count(max_pixel_limit)}\n")
        if filter_aspect_ratio:
            file.write(f"Aspect Ratio Filter: {filter_aspect_ratio}\n")
        file.write("\n")

        # Write the valid resolutions section
        file.write("Valid Resolutions:\n")
        for resolution in valid_resolutions:
            write_resolution_to_file(file, resolution, base_res, end_res)

        # Write the invalid resolutions section
        file.write("\nInvalid Resolutions (Exceeding Maximum Pixel Limit):\n")
        for resolution in invalid_resolutions:
            write_resolution_to_file(file, resolution, base_res, end_res)


def menu(title, options, actions):
    while True:
        # Print the menu title
        print(f"\n{title}")
        
        # Print the menu options
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        # Get the user's choice
        choice = get_integer_input("Enter your choice: ", 1, len(options))
        
        # Check if the choice is a valid action
        if choice in actions:
            # Execute the chosen action
            actions[choice]()
        else:
            # Exit the menu loop if the choice is not a valid action
            break


def main_menu():
    # List of menu options
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
    
    # Dictionary of menu actions corresponding to each option
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
    
    # Display the menu and execute the selected action
    menu("Choose a sorting method:", menu_options, menu_actions)


def sort_menu(method):
    # List of menu options
    menu_options = ["Ascending", "Descending", "Back to main menu"]
    
    # Insert additional option for "aspect_ratio" method
    if method == "aspect_ratio":
        menu_options.insert(1, "Closest to 1:1 first")

    # Dictionary of menu actions corresponding to each option
    if method == "aspect_ratio":
        menu_actions = {
            1: lambda: (sort_resolutions(method, "asc"), display_and_save_results(), print_saved_message()),
            2: lambda: (sort_resolutions(method, "closest"), display_and_save_results(), print_saved_message()),
            3: lambda: (sort_resolutions(method, "desc"), display_and_save_results(), print_saved_message()),
            4: main_menu
        }
    else:
        menu_actions = {
            1: lambda: (sort_resolutions(method, "asc"), display_and_save_results(), print_saved_message()),
            2: lambda: (sort_resolutions(method, "desc"), display_and_save_results(), print_saved_message()),
            3: main_menu
        }

    # Display the menu and execute the selected action
    menu(f"Sort by {method}:", menu_options, menu_actions)


def print_saved_message():
    # Print a message indicating that the results have been saved
    print("Results have been saved to resolutions.txt!")


def get_user_input():
    # Get user input for various parameters
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

    # Populate the resolutions list based on user input
    populate_resolutions()


if __name__ == "__main__":
    # Get user input and display the main menu
    get_user_input()
    main_menu()
