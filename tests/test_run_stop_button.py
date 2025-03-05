import unittest
from PySide6.QtWidgets import QApplication, QGraphicsScene
from PySide6.QtCore import QPointF, Qt, QEvent
from PySide6.QtGui import QMouseEvent
import sys

from packages.base.node import BaseNode
from packages.teleoperation import KeyboardTeleopNode
from packages.navigation import Nav2Node
from packages.robot_control import ROS2ControllersNode

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestRunStopButton(unittest.TestCase):
    """Test cases for the run/stop button functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = QGraphicsScene()
        
    def test_button_toggle(self):
        """Test that clicking the button toggles the run state"""
        # Create a node
        node = KeyboardTeleopNode()
        self.scene.addItem(node)
        
        # Initially, the node should not be running
        self.assertFalse(node.is_running)
        
        # Get the button position
        button_rect = node.get_button_rect()
        button_center = QPointF(
            button_rect.x() + button_rect.width() / 2,
            button_rect.y() + button_rect.height() / 2
        )
        
        # Create a mouse press event on the button
        press_event = QMouseEvent(
            QEvent.MouseButtonPress,
            button_center,
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        
        # Process the event
        node.mousePressEvent(press_event)
        
        # The node should now be running
        self.assertTrue(node.is_running)
        
        # Click again to stop
        node.mousePressEvent(press_event)
        
        # The node should now be stopped
        self.assertFalse(node.is_running)
        
    def test_on_start_stop_methods(self):
        """Test that on_start and on_stop methods are called"""
        # Create a test node class that tracks method calls
        class TestNode(BaseNode):
            def __init__(self):
                super().__init__(title="Test Node")
                self.start_called = False
                self.stop_called = False
                
            def on_start(self):
                self.start_called = True
                
            def on_stop(self):
                self.stop_called = True
        
        # Create the test node
        node = TestNode()
        self.scene.addItem(node)
        
        # Toggle to running
        node.toggle_run_state()
        
        # Check that on_start was called
        self.assertTrue(node.start_called)
        self.assertFalse(node.stop_called)
        
        # Toggle to stopped
        node.toggle_run_state()
        
        # Check that on_stop was called
        self.assertTrue(node.start_called)
        self.assertTrue(node.stop_called)
        
    def test_different_node_types(self):
        """Test that the button works for different node types"""
        # Create different types of nodes
        teleop_node = KeyboardTeleopNode()
        nav_node = Nav2Node()
        control_node = ROS2ControllersNode()
        
        # Add to scene
        self.scene.addItem(teleop_node)
        self.scene.addItem(nav_node)
        self.scene.addItem(control_node)
        
        # Toggle each node
        teleop_node.toggle_run_state()
        nav_node.toggle_run_state()
        control_node.toggle_run_state()
        
        # Check that all are running
        self.assertTrue(teleop_node.is_running)
        self.assertTrue(nav_node.is_running)
        self.assertTrue(control_node.is_running)
        
        # Toggle each node again
        teleop_node.toggle_run_state()
        nav_node.toggle_run_state()
        control_node.toggle_run_state()
        
        # Check that all are stopped
        self.assertFalse(teleop_node.is_running)
        self.assertFalse(nav_node.is_running)
        self.assertFalse(control_node.is_running)
        
if __name__ == '__main__':
    unittest.main() 