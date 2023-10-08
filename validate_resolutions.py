import math

def get_integer_input(prompt, min_value=None, max_value=None):
    """Helper function to get integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Please enter a value between {min_value} and {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")

def get_aspect_ratio_input(prompt):
    """Helper function to get a valid aspect ratio input from the user."""
    while True:
        ratio = input(prompt)
        if not ratio:
            return ""
        parts = ratio.split(":")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            print("Please enter a valid aspect ratio format (e.g., 16:9) or leave blank.")
            continue
        return ratio

def get_aspect_ratio(width, height):
    """Helper function to calculate the aspect ratio."""
    gcd = math.gcd(width, height)
    return f"{width//gcd}:{height//gcd}"

# Get user input for the constraints
start_resolution = get_integer_input("Enter the starting resolution (e.g., 512): ")
end_resolution = get_integer_input("Enter the ending resolution (e.g., 2048): ", min_value=start_resolution)
increment = get_integer_input("Enter the increment/multiple (e.g., 64): ")
max_pixel_limit = get_integer_input("Enter the Maximum Pixel Limit (e.g., 1048576): ")

# Get user input for filtering options
filter_aspect_ratio = get_aspect_ratio_input("Enter a specific aspect ratio to filter by (e.g., 16:9) or leave blank: ")

# Get user input for sorting method
print("\nChoose a sorting method:")
print("1. Sort by width")
print("2. Sort by total number of pixels (width x height)")
while True:
    sorting_choice = get_integer_input("Enter your choice (1 or 2): ")
    if sorting_choice in [1, 2]:
        break
    print("Invalid choice. Please select either 1 or 2.")

# Initialize lists to store valid and invalid resolutions
valid_resolutions = []
invalid_resolutions = []

# Iterate through possible widths and heights based on user input
for width in range(start_resolution, end_resolution + 1, increment):
    for height in range(start_resolution, end_resolution + 1, increment):
        # Check if the product does not exceed the user-defined max_pixel_limit
        if width * height <= max_pixel_limit:
            aspect_ratio = get_aspect_ratio(width, height)
            if not filter_aspect_ratio or aspect_ratio == filter_aspect_ratio:
                valid_resolutions.append((width, height))
                # Also add the resolution in the reverse order (height x width) if it meets the criteria
                if not filter_aspect_ratio or aspect_ratio == get_aspect_ratio(height, width):
                    valid_resolutions.append((height, width))
        else:
            invalid_resolutions.append((width, height))
            # Also add the resolution in the reverse order (height x width)
            invalid_resolutions.append((height, width))

# Remove duplicates from the valid resolutions list
valid_resolutions = list(set(valid_resolutions))

# Sort the resolutions based on user choice
if sorting_choice == 1:
    valid_resolutions = sorted(valid_resolutions)
    invalid_resolutions = sorted(invalid_resolutions)
elif sorting_choice == 2:
    valid_resolutions = sorted(valid_resolutions, key=lambda x: x[0] * x[1])
    invalid_resolutions = sorted(invalid_resolutions, key=lambda x: x[0] * x[1])

# Save the results to a text file
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
        aspect_ratio = get_aspect_ratio(resolution[0], resolution[1])
        total_pixels = resolution[0] * resolution[1]
        file.write(f"{resolution[0]}x{resolution[1]} ({aspect_ratio}, {total_pixels} pixels)\n")
    
    file.write("\nInvalid Resolutions:\n")
    for resolution in invalid_resolutions:
        aspect_ratio = get_aspect_ratio(resolution[0], resolution[1])
        total_pixels = resolution[0] * resolution[1]
        file.write(f"{resolution[0]}x{resolution[1]} ({aspect_ratio}, {total_pixels} pixels)\n")

print("Results saved to resolutions.txt")
