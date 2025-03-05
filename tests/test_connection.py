import unittest
from PySide6.QtWidgets import QApplication, QGraphicsScene
from PySide6.QtCore import QPointF
import sys

from packages.base.node import BaseNode, Port
from connection import Connection

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestConnection(unittest.TestCase):
    """Test cases for the Connection class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = QGraphicsScene()
        
        # Create source node with output port
        self.source_node = BaseNode(title="Source Node")
        self.scene.addItem(self.source_node)
        self.source_node.setPos(100, 100)
        self.output_port = self.source_node.add_output_port("output")
        
        # Create target node with input port
        self.target_node = BaseNode(title="Target Node")
        self.scene.addItem(self.target_node)
        self.target_node.setPos(300, 100)
        self.input_port = self.target_node.add_input_port("input")
        
    def test_initialization(self):
        """Test that a connection is properly initialized"""
        # Create connection with just start port
        connection = Connection(self.output_port)
        self.scene.addItem(connection)
        
        # Check initial state
        self.assertEqual(connection.start_port, self.output_port)
        self.assertIsNone(connection.end_port)
        self.assertIn(connection, self.output_port.connections)
        
    def test_complete_connection(self):
        """Test creating a complete connection between ports"""
        # Create connection with both ports
        connection = Connection(self.output_port, self.input_port)
        self.scene.addItem(connection)
        
        # Check state
        self.assertEqual(connection.start_port, self.output_port)
        self.assertEqual(connection.end_port, self.input_port)
        self.assertIn(connection, self.output_port.connections)
        self.assertIn(connection, self.input_port.connections)
        
    def test_set_end_port(self):
        """Test setting the end port after creation"""
        # Create connection with just start port
        connection = Connection(self.output_port)
        self.scene.addItem(connection)
        
        # Set end port
        connection.setEndPort(self.input_port)
        
        # Check state
        self.assertEqual(connection.end_port, self.input_port)
        self.assertIn(connection, self.input_port.connections)
        
    def test_update_path(self):
        """Test that the connection path updates correctly"""
        # Create connection
        connection = Connection(self.output_port, self.input_port)
        self.scene.addItem(connection)
        
        # Get initial path
        initial_path = connection.path()
        
        # Move target node
        self.target_node.setPos(400, 200)
        
        # Update path
        connection.updatePath()
        
        # Path should have changed
        self.assertNotEqual(initial_path, connection.path())
        
    def test_disconnect_from_ports(self):
        """Test disconnecting a connection from its ports"""
        # Create connection
        connection = Connection(self.output_port, self.input_port)
        self.scene.addItem(connection)
        
        # Disconnect
        connection.disconnectFromPorts()
        
        # Check state
        self.assertNotIn(connection, self.output_port.connections)
        self.assertNotIn(connection, self.input_port.connections)
        self.assertIsNone(connection.start_port)
        self.assertIsNone(connection.end_port)
        
if __name__ == '__main__':
    unittest.main() 