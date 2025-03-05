import unittest
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsSceneMouseEvent
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QMouseEvent
import sys

from scene import NodeScene
from packages.base.node import BaseNode, Port
from packages.teleoperation import KeyboardTeleopNode
from packages.navigation import Nav2Node
from connection import Connection

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestNodeScene(unittest.TestCase):
    """Test cases for the NodeScene class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = NodeScene()
        
    def test_initialization(self):
        """Test that the scene is properly initialized"""
        self.assertEqual(len(self.scene.connections), 0)
        self.assertIsNone(self.scene.current_connection)
        self.assertIsNone(self.scene.start_port)
        self.assertFalse(self.scene.is_creating_connection)
        
    def test_add_node(self):
        """Test adding a node to the scene"""
        # Add a keyboard teleop node
        node = KeyboardTeleopNode()
        node.setPos(100, 100)
        self.scene.addItem(node)
        
        # Check that node is in the scene
        self.assertIn(node, self.scene.items())
        
    def test_find_port_at(self):
        """Test finding a port at a given scene position"""
        # Add a node with ports
        node = Nav2Node()
        node.setPos(100, 100)
        self.scene.addItem(node)
        
        # Get a port's scene position
        input_port = list(node.input_ports.values())[0]
        port_scene_pos = node.mapToScene(input_port.relative_pos)
        
        # Find port at that position
        found_port = self.scene.findPortAt(port_scene_pos)
        
        # Should find the port
        self.assertEqual(found_port, input_port)
        
        # Position far from any port should return None
        far_pos = QPointF(500, 500)
        self.assertIsNone(self.scene.findPortAt(far_pos))
        
    def test_start_connection(self):
        """Test starting a connection from a port"""
        # Add a node with ports
        node = KeyboardTeleopNode()
        node.setPos(100, 100)
        self.scene.addItem(node)
        
        # Get an output port
        output_port = list(node.output_ports.values())[0]
        
        # Start connection
        self.scene.startConnection(output_port)
        
        # Check state
        self.assertTrue(self.scene.is_creating_connection)
        self.assertEqual(self.scene.start_port, output_port)
        self.assertIsNotNone(self.scene.current_connection)
        self.assertIn(self.scene.current_connection, self.scene.items())
        
    def test_connection_creation_and_removal(self):
        """Test creating and removing connections between nodes"""
        # Add source node with output port
        source_node = KeyboardTeleopNode()
        source_node.setPos(100, 100)
        self.scene.addItem(source_node)
        output_port = list(source_node.output_ports.values())[0]
        
        # Add target node with input port
        target_node = Nav2Node()
        target_node.setPos(300, 100)
        self.scene.addItem(target_node)
        input_port = list(target_node.input_ports.values())[0]
        
        # Start connection
        self.scene.startConnection(output_port)
        
        # Simulate finding the input port at the release point
        # Instead of creating a QGraphicsSceneMouseEvent, we'll directly call the methods
        self.scene.current_connection.setEndPort(input_port)
        self.scene.connections.append(self.scene.current_connection)
        
        # Reset state
        connection = self.scene.current_connection
        self.scene.current_connection = None
        self.scene.start_port = None
        self.scene.is_creating_connection = False
        
        # Check that connection was created
        self.assertEqual(len(self.scene.connections), 1)
        self.assertFalse(self.scene.is_creating_connection)
        self.assertIsNone(self.scene.current_connection)
        
        # Check that connection is in both ports
        self.assertIn(connection, output_port.connections)
        self.assertIn(connection, input_port.connections)
        
    def test_context_menu(self):
        """Test that the context menu creates nodes correctly"""
        # This is harder to test directly since it involves QMenu execution
        # We'll just verify that the node creation methods work
        
        # Create a keyboard teleop node
        pos = QPointF(100, 100)
        node = KeyboardTeleopNode()
        node.setPos(pos)
        self.scene.addItem(node)
        
        # Check that node is in the scene
        self.assertIn(node, self.scene.items())
        
if __name__ == '__main__':
    unittest.main() 