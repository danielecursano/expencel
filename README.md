# Expencel - Web App for Daily Expense Management

Expencel is a Flask-based web app that provides a simple and efficient way to record daily expenses and conduct detailed analysis on the collected data. The platform not only allows users to log their daily expenses but also offers several advanced features for analyzing and visualizing the data intuitively.

## Table of contents
* [Key Features](#key-features)
* [Usage Instructions](#usage-instructions)
* [Complexity Analysis](#complexity-analysis)
* [Screenshots](#screenshots)

## Key Features

- **Expense Logging**: Users can easily input their daily expenses, including details such as the amount, category, and date.

- **Data Operations**: The web app enables users to perform various operations on the data, such as summing expenses for a specific category or for a defined period of time.

- **Chart Creation**: Using Matplotlib , the web app allows users to create intuitive charts to visualize expense trends over time or distributions by category.

## Usage Instructions

To use the application:

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Run the Flask application using `python app.py`.
4. Access the web app through your browser at `http://localhost:5000`.

## Complexity Analysis

`src/structs.py` contains the implementation of the algorithms to find cells in a given range of dates. The method used in the webapp is a binary search that runs in `O(log n)` that finds an element in the range and then slides left and right to find the `k` elements remaining. So the final complexity is `O(log n + k)`. There is another way to get the same result which is a for loop that scans every element so the worst case is `O(n)`. <br>In the end, if `k << n` the binary search method is faster.

## Screenshots

![home](https://github.com/danielecursano/expencel/blob/main/images/home.png)
![sheet](https://github.com/danielecursano/expencel/blob/main/images/sheet.png)
![add](https://github.com/danielecursano/expencel/blob/main/images/newcell.png)
![pie_chart](https://github.com/danielecursano/expencel/blob/main/images/pie.png)
