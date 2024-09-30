# Motion Control System GUI

This repository contains a Python application for a motion control system that utilizes a graphical user interface (GUI) designed with PySide6 (Qt for Python). The application is capable of managing real-time data communication through serial ports, processing JSON data, and providing an intuitive interface for users to control and monitor motion settings.

## Table of Contents

- [Features](#features)
- [Classes](#classes)
  - [JSONHandler](#jsonhandler)
  - [SerialThread](#serialthread)
  - [Widget](#widget)
- [Technologies Used](#technologies-used)
- [Author](#author)

## Features

- **Real-time Data Processing**: Handles incoming serial data and processes JSON formatted messages.
- **Intuitive GUI**: Provides an easy-to-navigate interface for controlling motion parameters, error monitoring, and system settings.
- **Modular Design**: Separate classes for JSON handling and serial communication, promoting clean code and reusability.
- **Live Monitoring**: Displays current state information, including yaw angles and error statuses with visual indicators.

## Classes

### JSONHandler

The `JSONHandler` class is responsible for parsing and storing data from JSON strings received via serial communication. It maintains multiple lists to track various parameters related to the motion control system.

### SerialThread

The `SerialThread` class handles serial communication in a separate thread. It continuously reads data from the specified serial port and emits the received data as a dictionary. This ensures non-blocking operations for the GUI.

### Widget

The `Widget` class is the main component of the application, responsible for creating and managing the GUI. It utilizes PySide6 to create a multi-tab interface that includes:

- **Controls Tab**: For setting motion parameters and starting/stopping the motion.
- **General Settings Tab**: To configure general system settings.
- **Control Settings Tab**: For advanced control parameters.
- **Expert Procedures Tab**: For more specialized tasks.

## Technologies Used

- **Python**: Programming language for application development.
- **PySide6**: Framework for building the GUI using Qt.
- **Serial Communication**: To interface with external hardware.
- **JSON**: For data interchange format.

## Author

**Gianmarco Ricci**  
