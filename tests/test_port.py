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

class TestPort(unittest.TestCase):
    """Test cases for the Port class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = QGraphicsScene()
        self.node = BaseNode(title="Test Node")
        self.scene.addItem(self.node)
        self.input_port = self.node.add_input_port("test_input")
        self.output_port = self.node.add_output_port("test_output")
        
    def test_initialization(self):
        """Test that a port is properly initialized"""
        # Test input port
        self.assertEqual(self.input_port.name, "test_input")
        self.assertTrue(self.input_port.is_input)
        self.assertEqual(self.input_port.node, self.node)
        self.assertEqual(len(self.input_port.connections), 0)
        
        # Test output port
        self.assertEqual(self.output_port.name, "test_output")
        self.assertFalse(self.output_port.is_input)
        self.assertEqual(self.output_port.node, self.node)
        self.assertEqual(len(self.output_port.connections), 0)
        
    def test_get_scene_pos(self):
        """Test getting the port's position in scene coordinates"""
        # Set node position
        self.node.setPos(100, 100)
        
        # Get scene positions
        input_scene_pos = self.input_port.get_scene_pos()
        output_scene_pos = self.output_port.get_scene_pos()
        
        # Check that scene positions are offset by node position
        self.assertEqual(input_scene_pos.x(), 100 + self.input_port.relative_pos.x())
        self.assertEqual(input_scene_pos.y(), 100 + self.input_port.relative_pos.y())
        self.assertEqual(output_scene_pos.x(), 100 + self.output_port.relative_pos.x())
        self.assertEqual(output_scene_pos.y(), 100 + self.output_port.relative_pos.y())
        
    def test_contains_point(self):
        """Test checking if a point is within the port circle"""
        # Point at port center should be contained
        self.assertTrue(self.input_port.contains_point(self.input_port.relative_pos))
        
        # Point slightly offset should still be contained (within radius)
        offset = QPointF(self.input_port.radius / 2, self.input_port.radius / 2)
        self.assertTrue(self.input_port.contains_point(self.input_port.relative_pos + offset))
        
        # Point far away should not be contained
        far_point = QPointF(self.input_port.relative_pos.x() + 50, self.input_port.relative_pos.y() + 50)
        self.assertFalse(self.input_port.contains_point(far_point))
        
    def test_connection_management(self):
        """Test adding and removing connections from a port"""
        # Create a second node
        node2 = BaseNode(title="Test Node 2")
        self.scene.addItem(node2)
        node2.setPos(300, 100)
        input_port2 = node2.add_input_port("input2")
        
        # Create a connection
        connection = Connection(self.output_port, input_port2)
        self.scene.addItem(connection)
        
        # Check that connection is in both ports' connection lists
        self.assertIn(connection, self.output_port.connections)
        self.assertIn(connection, input_port2.connections)
        
        # Test disconnect_all
        self.output_port.disconnect_all()
        
        # Check that connection is removed from both ports
        self.assertNotIn(connection, self.output_port.connections)
        self.assertNotIn(connection, input_port2.connections)
        
    def test_get_connected_nodes(self):
        """Test getting nodes connected to a port"""
        # Create a second node
        node2 = BaseNode(title="Test Node 2")
        self.scene.addItem(node2)
        node2.setPos(300, 100)
        input_port2 = node2.add_input_port("input2")
        
        # Create a connection
        connection = Connection(self.output_port, input_port2)
        self.scene.addItem(connection)
        
        # Check connected nodes
        connected_to_output = self.output_port.get_connected_nodes()
        connected_to_input = input_port2.get_connected_nodes()
        
        self.assertEqual(len(connected_to_output), 1)
        self.assertEqual(len(connected_to_input), 1)
        self.assertEqual(connected_to_output[0], node2)
        self.assertEqual(connected_to_input[0], self.node)
        
if __name__ == '__main__':
    unittest.main() 