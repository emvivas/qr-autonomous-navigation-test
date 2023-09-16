# Quantum Robotics. Autonomous Navigation Test |  University Rover Challenge.

This project is a simulation of autonomous navigation of a rover on Mars surface, using A* search algorithm and auxiliary markers. The goal is for rover to find goal marker, avoiding obstacles and using auxiliary markers as clues.

## Requirements

To run this project you need to have Python 3 and pygame library installed. You can install pygame using command:

```python
pip install pygame
```

## Execution

To run this project you need to execute file main.py with command:

```python
python main.py
```

When running program, user will be asked to enter number of auxiliary markers and size of Mars terrain. Program will create window with simulation of rover and Mars terrain. Rover will move randomly until it finds an auxiliary marker, and then it will use A* algorithm to search for shortest path to goal. Program will show status of rover, number of markers and title of program in window.


## System's UML Class Diagram

![System Class Diagram](https://github.com/vivasrguez/qr-autonomous-navigation-test/assets/85045551/ef8bed7f-8d76-4a8d-bcce-455f3de8c717)


## Graphical interface

Graphical interface of program uses pygame library to create visual elements. Elements are as follows:

- Mars terrain is an orange grid, where each cell represents a possible position of rover.
- Rover is a black image that represents explorer vehicle.
- Goal is a blue image that represents goal marker.
- Auxiliary markers are green images that represent clues that help rover find goal.
- Path is series of gray rectangles that represent positions visited by rover.

## Author

This project has been created by Emiliano Vivas Rodríguez, a student passionate about robotics and artificial intelligence. You can contact me through this email: a01424732@tec.mx
