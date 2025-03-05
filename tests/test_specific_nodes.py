import unittest
from PySide6.QtWidgets import QApplication, QGraphicsScene
import sys

from packages.teleoperation import KeyboardTeleopNode, JoystickTeleopNode
from packages.navigation import Nav2Node, SlamToolboxNode
from packages.robot_control import ROS2ControllersNode, TwistMuxNode

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestSpecificNodes(unittest.TestCase):
    """Test cases for the specific node classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = QGraphicsScene()
        
    def test_keyboard_teleop_node(self):
        """Test KeyboardTeleopNode initialization and ports"""
        node = KeyboardTeleopNode()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "Keyboard Teleop")
        self.assertEqual(len(node.input_ports), 0)
        self.assertEqual(len(node.output_ports), 1)
        self.assertIn("cmd_vel", node.output_ports)
        
    def test_joystick_teleop_node(self):
        """Test JoystickTeleopNode initialization and ports"""
        node = JoystickTeleopNode()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "Joystick Teleop")
        self.assertEqual(len(node.input_ports), 1)
        self.assertEqual(len(node.output_ports), 1)
        self.assertIn("joy", node.input_ports)
        self.assertIn("cmd_vel", node.output_ports)
        
    def test_nav2_node(self):
        """Test Nav2Node initialization and ports"""
        node = Nav2Node()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "Nav2")
        self.assertEqual(len(node.input_ports), 3)
        self.assertEqual(len(node.output_ports), 2)
        self.assertIn("scan", node.input_ports)
        self.assertIn("odom", node.input_ports)
        self.assertIn("goal_pose", node.input_ports)
        self.assertIn("cmd_vel", node.output_ports)
        self.assertIn("path", node.output_ports)
        
    def test_slam_toolbox_node(self):
        """Test SlamToolboxNode initialization and ports"""
        node = SlamToolboxNode()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "SLAM Toolbox")
        self.assertEqual(len(node.input_ports), 2)
        self.assertEqual(len(node.output_ports), 2)
        self.assertIn("scan", node.input_ports)
        self.assertIn("odom", node.input_ports)
        self.assertIn("map", node.output_ports)
        self.assertIn("tf", node.output_ports)
        
    def test_ros2_controllers_node(self):
        """Test ROS2ControllersNode initialization and ports"""
        node = ROS2ControllersNode()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "ROS2 Controllers")
        self.assertEqual(len(node.input_ports), 2)
        self.assertEqual(len(node.output_ports), 1)
        self.assertIn("joint_states", node.input_ports)
        self.assertIn("cmd_vel", node.input_ports)
        self.assertIn("joint_commands", node.output_ports)
        
    def test_twist_mux_node(self):
        """Test TwistMuxNode initialization and ports"""
        node = TwistMuxNode()
        self.scene.addItem(node)
        
        # Check title and ports
        self.assertEqual(node.title, "Twist Mux")
        self.assertEqual(len(node.input_ports), 3)
        self.assertEqual(len(node.output_ports), 1)
        self.assertIn("cmd_vel1", node.input_ports)
        self.assertIn("cmd_vel2", node.input_ports)
        self.assertIn("cmd_vel3", node.input_ports)
        self.assertIn("cmd_vel", node.output_ports)
        
    def test_node_colors(self):
        """Test that nodes have the correct colors"""
        # Teleop nodes should have blue colors
        teleop_node = KeyboardTeleopNode()
        self.assertEqual(teleop_node.body_color.name(), "#4682b4")  # Steel blue
        
        # Navigation nodes should have green colors
        nav_node = Nav2Node()
        self.assertEqual(nav_node.body_color.name(), "#4bb44b")  # Green
        
        # Robot control nodes should have red colors
        control_node = ROS2ControllersNode()
        self.assertEqual(control_node.body_color.name(), "#b45a5a")  # Reddish
        
if __name__ == '__main__':
    unittest.main() 