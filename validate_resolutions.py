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
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
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
            print("Please enter a valid aspect ratio format (e.g., 16:9) or leave blank.")
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
    width, height = map(int, ratio.split(':'))
    return width / height

def format_float(value):
    """Formats a float to a string, removing unnecessary trailing zeros and decimal points."""
    str_value = "{:.4f}".format(value)
    return str_value.rstrip('0').rstrip('.') if '.' in str_value else str_value

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

    min_ratio, max_ratio = 0, float('inf')  # Default values
    if aspect_ratio_range:
        min_ratio, max_ratio = map(aspect_ratio_to_float, aspect_ratio_range.split('-'))

    for width in range(start_resolution, end_resolution + 1, increment):
        for height in range(width, end_resolution + 1, increment):  # Start from width to avoid duplicates
            aspect_ratio = get_aspect_ratio(width, height)
            orientation = get_orientation(width, height)
            if width * height <= max_pixel_limit and width * height >= min_pixel_limit:
                if (not filter_aspect_ratio or aspect_ratio == filter_aspect_ratio) and \
                   (not orientation_filter or orientation == orientation_filter) and \
                   is_within_aspect_ratio_range(width, height, min_ratio, max_ratio):
                    valid_resolutions_set.add((width, height))
                    if width != height:
                        valid_resolutions_set.add((height, width))
            else:
                invalid_resolutions_set.add((width, height))
                if width != height:
                    invalid_resolutions_set.add((height, width))

    valid_resolutions = list(valid_resolutions_set)
    invalid_resolutions = list(invalid_resolutions_set)

def sort_and_display(method, order):
    global valid_resolutions, invalid_resolutions
    if method == "width":
        if order == "asc":
            valid_resolutions.sort(key=lambda x: x[0])
            invalid_resolutions.sort(key=lambda x: x[0])
        else:
            valid_resolutions.sort(key=lambda x: x[0], reverse=True)
            invalid_resolutions.sort(key=lambda x: x[0], reverse=True)
    elif method == "height":
        if order == "asc":
            valid_resolutions.sort(key=lambda x: x[1])
            invalid_resolutions.sort(key=lambda x: x[1])
        else:
            valid_resolutions.sort(key=lambda x: x[1], reverse=True)
            invalid_resolutions.sort(key=lambda x: x[1], reverse=True)
    elif method == "average":
        if order == "asc":
            valid_resolutions.sort(key=lambda x: (x[0] + x[1]) / 2)
            invalid_resolutions.sort(key=lambda x: (x[0] + x[1]) / 2)
        else:
            valid_resolutions.sort(key=lambda x: (x[0] + x[1]) / 2, reverse=True)
            invalid_resolutions.sort(key=lambda x: (x[0] + x[1]) / 2, reverse=True)
    elif method == "pixels":
        if order == "asc":
            valid_resolutions.sort(key=lambda x: x[0] * x[1])
            invalid_resolutions.sort(key=lambda x: x[0] * x[1])
        else:
            valid_resolutions.sort(key=lambda x: x[0] * x[1], reverse=True)
            invalid_resolutions.sort(key=lambda x: x[0] * x[1], reverse=True)
    elif method == "aspect_ratio":
        if order == "closest":
            valid_resolutions.sort(key=lambda x: abs(aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])) - 1))
            invalid_resolutions.sort(key=lambda x: abs(aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])) - 1))
        elif order == "asc":
            valid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])))
            invalid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])))
        else:
            valid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])), reverse=True)
            invalid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])), reverse=True)
    elif method == "aspect_ratio_decimal":
        if order == "asc":
            valid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])))
            invalid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])))
        else:
            valid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])), reverse=True)
            invalid_resolutions.sort(key=lambda x: aspect_ratio_to_float(get_aspect_ratio(x[0], x[1])), reverse=True)
    display_and_save_results()

def display_and_save_results():
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
            orientation = get_orientation(resolution[0], resolution[1])
            file.write(f"Resolution: {resolution[0]}x{resolution[1]}, Aspect Ratio: {aspect_ratio_str} ({orientation}), Decimal: {aspect_ratio_float}, Pixels: {formatted_pixels}\n")
        
        file.write("\nInvalid Resolutions (Exceeding Maximum Pixel Limit):\n")
        for resolution in invalid_resolutions:
            aspect_ratio_str = get_aspect_ratio(resolution[0], resolution[1])
            aspect_ratio_float = format_float(aspect_ratio_to_float(aspect_ratio_str))
            total_pixels = resolution[0] * resolution[1]
            formatted_pixels = format_pixel_count(total_pixels)
            orientation = get_orientation(resolution[0], resolution[1])
            file.write(f"Resolution: {resolution[0]}x{resolution[1]}, Aspect Ratio: {aspect_ratio_str} ({orientation}), Decimal: {aspect_ratio_float}, Pixels: {formatted_pixels}\n")
    print("Results saved to resolutions.txt")

def main_menu():
    while True:
        print("\nChoose a sorting method:")
        print("1. Sort by width")
        print("2. Sort by height")
        print("3. Sort by average of width and height")
        print("4. Sort by total number of pixels")
        print("5. Sort by aspect ratio")
        print("6. Choose new parameters")
        print("7. Exit program")
        
        choice = get_integer_input("Enter your choice: ", 1, 7)
        
        if choice == 1:
            width_menu()
        elif choice == 2:
            height_menu()
        elif choice == 3:
            average_menu()
        elif choice == 4:
            pixel_menu()
        elif choice == 5:
            aspect_ratio_menu()
        elif choice == 6:
            get_user_input()
        elif choice == 7:
            print("Exiting program.")
            break

def width_menu():
    while True:
        print("\nSort by width:")
        print("1. Ascending")
        print("2. Descending")
        print("3. Back to main menu")
        
        choice = get_integer_input("Enter your choice: ", 1, 3)
        
        if choice == 1:
            sort_and_display("width", "asc")
            break
        elif choice == 2:
            sort_and_display("width", "desc")
            break
        elif choice == 3:
            break

def height_menu():
    while True:
        print("\nSort by height:")
        print("1. Ascending")
        print("2. Descending")
        print("3. Back to main menu")
        
        choice = get_integer_input("Enter your choice: ", 1, 3)
        
        if choice == 1:
            sort_and_display("height", "asc")
            break
        elif choice == 2:
            sort_and_display("height", "desc")
            break
        elif choice == 3:
            break

def average_menu():
    while True:
        print("\nSort by average of width and height:")
        print("1. Ascending")
        print("2. Descending")
        print("3. Back to main menu")
        
        choice = get_integer_input("Enter your choice: ", 1, 3)
        
        if choice == 1:
            sort_and_display("average", "asc")
            break
        elif choice == 2:
            sort_and_display("average", "desc")
            break
        elif choice == 3:
            break

def pixel_menu():
    while True:
        print("\nSort by total number of pixels:")
        print("1. Ascending")
        print("2. Descending")
        print("3. Back to main menu")
        
        choice = get_integer_input("Enter your choice: ", 1, 3)
        
        if choice == 1:
            sort_and_display("pixels", "asc")
            break
        elif choice == 2:
            sort_and_display("pixels", "desc")
            break
        elif choice == 3:
            break

def aspect_ratio_menu():
    while True:
        print("\nSort by aspect ratio:")
        print("1. Closest to 1:1 first")
        print("2. Ascending (by ratio)")
        print("3. Descending (by ratio)")
        print("4. Ascending (by decimal)")
        print("5. Descending (by decimal)")
        print("6. Back to main menu")
        
        choice = get_integer_input("Enter your choice: ", 1, 6)
        
        if choice == 1:
            sort_and_display("aspect_ratio", "closest")
        elif choice == 2:
            sort_and_display("aspect_ratio", "asc")
        elif choice == 3:
            sort_and_display("aspect_ratio", "desc")
        elif choice == 4:
            sort_and_display("aspect_ratio_decimal", "asc")
        elif choice == 5:
            sort_and_display("aspect_ratio_decimal", "desc")
        elif choice == 6:
            break

def get_user_input():
    global start_resolution, end_resolution, increment, max_pixel_limit, min_pixel_limit, filter_aspect_ratio, orientation_filter, aspect_ratio_range
    start_resolution = get_integer_input("Enter the starting resolution (e.g., 512): ", default_value=512)
    end_resolution = get_integer_input("Enter the ending resolution (e.g., 2048): ", min_value=start_resolution, default_value=2048)
    increment = get_integer_input("Enter the increment/multiple (e.g., 64): ", default_value=64)
    max_pixel_limit = get_integer_input("Enter the Maximum Pixel Limit (e.g., 1048576): ", default_value=1048576)
    min_pixel_limit = get_integer_input("Enter the Minimum Pixel Limit (e.g., 262144): ", default_value=262144)
    filter_aspect_ratio = get_aspect_ratio_input("Enter a specific aspect ratio to filter by (e.g., 16:9) or leave blank: ", default_value="")
    orientation_filter = input("Filter by orientation (Horizontal, Vertical, Square) or leave blank: ").capitalize()
    aspect_ratio_range = input("Enter a custom aspect ratio range (e.g., 4:3-16:9) or leave blank: ")
    populate_resolutions()

if __name__ == "__main__":
    get_user_input()
    main_menu()
