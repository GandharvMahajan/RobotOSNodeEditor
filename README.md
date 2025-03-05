# PysideNodeApp

A node-based application built with PySide6 for creating and connecting nodes in a visual graph editor.

## Features

- Create different types of nodes (Teleoperation, Navigation, Robot Control)
- Connect nodes through input and output ports
- Drag and drop interface for node placement
- Zoom and pan functionality for the node view
- Modular architecture with separate packages for different node types

## Project Structure

```
PysideNodeApp/
├── packages/
│   ├── base/              # Base node definitions
│   ├── teleoperation/     # Teleoperation node types
│   ├── navigation/        # Navigation node types
│   └── robot_control/     # Robot control node types
├── tests/                 # Comprehensive test suite
├── connection.py          # Connection class for connecting nodes
├── scene.py               # NodeScene class for managing the node graph
├── view.py                # NodeView class for displaying the node graph
└── main.py                # Application entry point
```

## Requirements

- Python 3.6+
- PySide6

## Installation

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Testing

Run the test suite with:

```
python -m tests.run_tests
```

## License

MIT 