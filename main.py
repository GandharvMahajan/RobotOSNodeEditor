import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from scene import NodeScene
from view import NodeView

# Import node classes from their respective packages
from packages.base import BaseNode
from packages.teleoperation import TeleoperationNode
from packages.navigation import NavigationNode
from packages.robot_control import RobotControlNode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Based Editor")
        self.resize(800, 600)
        scene = NodeScene()
        view = NodeView(scene)
        self.setCentralWidget(view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())