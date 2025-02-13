# Expencel - Web App for Daily Expense Management

Expencel is a Flask-based web app that provides a simple and efficient way to record daily expenses and conduct detailed analysis on the collected data. The platform not only allows users to log their daily expenses but also offers several advanced features for analyzing and visualizing the data intuitively. Additionally, it incorporates an LLM-powered chatbot using LangChain to assist users in conducting detailed analyses, especially on unstructured text.

## Table of contents
* [Key Features](#key-features)
* [Usage Instructions](#usage-instructions)
* [Screenshots](#screenshots)
* [TODO](#todo)

## Key Features

- **LLM chat**: A chatbot implemented with LangChain assists users in conducting detailed analyses, especially on unstructured text.

- **Expense Logging**: Users can easily input their daily expenses, including details such as the amount, category, and date.

- **Data Operations**: The web app enables users to perform various operations on the data, such as summing expenses for a specific category or for a defined period of time.

- **Chart Creation**: Using Matplotlib , the web app allows users to create intuitive charts to visualize expense trends over time or distributions by category.

## Usage Instructions

To use the application:

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Run the Flask application using `python app.py`.
4. Access the web app through your browser at `http://localhost:5000`.

## Screenshots

![llm](https://github.com/danielecursano/expencel/blob/main/images/llm.png)
![home](https://github.com/danielecursano/expencel/blob/main/images/home.png)
![rows](https://github.com/danielecursano/expencel/blob/main/images/rows.png)
![add](https://github.com/danielecursano/expencel/blob/main/images/add.png)

## TODO
- Implement tools which can be used my a LLM (ex. add new data)
