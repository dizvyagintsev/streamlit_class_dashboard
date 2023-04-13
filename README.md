# Streamlit Class Dashboard

`streamlit_class_dashboard` is a simple and efficient library that helps you quickly create interactive dashboards for your Python classes using Streamlit. It allows you to test and visualize your class methods without spending hours on building user interfaces.

## Features

- Automatically generate Streamlit dashboards for your Python classes.
- Supports int, float, and str types for arguments and return values.
- Handles default values and optional arguments.
- Easy to use with the `Dashboard` decorator.

## Getting Started

Install the library using `pip`: `pip install streamlit_class_dashboard`


## Usage

Here's a basic example to get you started:

```python
from streamlit_class_dashboard import Dashboard

@Dashboard
class Dinosaur:
    def __init__(self, name: str = "T-Rex", speed: float = 30.0, age: int = 65_000_000):
        self.name = name
        self.speed = speed
        self.age = age

    def roar(self, volume: int = 100) -> str:
        return f"{self.name} roars at volume {volume} dB!"

    def run(self, distance: float = 100.0) -> str:
        return f"{self.name} runs {distance} meters in {distance / self.speed} seconds!"
```

This will create a dashboard with input fields for the `Vehicle` class attributes and methods. You can interact with the dashboard, see the results of the methods, and modify the inputs with default values.
![example.png](images%2Fexample.png)

## Roadmap
Here are some features and improvements I plan to work on:

- Support more complex types like dataframes, lists, and dictionaries.
- Add a feature for users to register custom functions for visualizing specific data types.
- Improve code quality and structure by refactoring.
- Write comprehensive test suites to ensure the stability of the library.
- Enhance the library's flexibility by supporting custom dashboard layouts and styling.
- Implement better error handling and informative messages for edge cases and invalid inputs.

## Note
`streamlit_class_dashboard` is still in the early stages of development. There may be bugs, and the code may require refactoring. I appreciate your understanding and contributions to improve this library.

Feel free to open issues and submit pull requests on our GitHub repository.



