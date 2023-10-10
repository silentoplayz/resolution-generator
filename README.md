# Resolution Generator

This script generates a list of valid resolutions based on user-defined constraints, such as pixel limits, aspect ratio filters, and more. It provides options to sort the resolutions in various ways for further analysis.

## Table of Contents

- [Features](#features)
- [How to Use](#how-to-use)
- [User Input](#user-input)
- [License](#license)

## Features

- Generates a list of valid resolutions within specified constraints.
- Provides options to sort resolutions based on different criteria.
- Allows filtering by aspect ratio, orientation, and custom aspect ratio range.
- Exports the results to a text file for further analysis.

## How to Use

# **Clone the Repository**: Clone this repository to your local machine.

# **Run the Script**: Execute the script using Python.

```python python script.py```
Follow the Menu: The script will guide you through the following options:

# Choose resolution parameters.
Filter by aspect ratio (optional).
Filter by orientation (optional).
Specify a custom aspect ratio range (optional).
Sort resolutions based on different criteria.
Save the results to a text file.
View Results: The script will generate a list of valid resolutions, and you can view and analyze the results in the resolutions.txt file.

# User Input
The script allows you to customize the following parameters:
```Starting Resolution
Ending Resolution
Increment/Multiple
Maximum Pixel Limit
Minimum Pixel Limit
Aspect Ratio Filter (optional)
Orientation Filter (optional)
Custom Aspect Ratio Range (optional)
```

# Info
Enter a specific aspect ratio to filter by (e.g., 16:9) or leave blank:

Explanation: You can filter resolutions by a specific aspect ratio. For example, if you want to see only resolutions with a 16:9 aspect ratio, enter "16:9." To see all resolutions regardless of aspect ratio, leave this blank.
Example: To filter by 16:9, enter "16:9."
Filter by orientation (Horizontal, Vertical, Square) or leave blank:

Explanation: You can filter resolutions by their orientation. For example, if you want to see only horizontal resolutions, enter "Horizontal." To see all resolutions regardless of orientation, leave this blank.
Example: To filter by vertical resolutions, enter "Vertical."
Enter a custom aspect ratio range (e.g., 4:3-16:9) or leave blank:

Explanation: You can specify a custom range of aspect ratios to filter resolutions. Use the format "X:Y-Z:W," where X:Y is the minimum aspect ratio, and Z:W is the maximum aspect ratio. For example, "4:3-16:9" will include resolutions with aspect ratios from 4:3 to 16:9. To see all resolutions regardless of aspect ratio range, leave this blank.
Example: To filter resolutions between 16:10 and 21:9, enter "16:10-21:9."

License
This project is licensed under the MIT License - see the LICENSE file for details.
