import unittest
from PySide6.QtWidgets import QApplication, QGraphicsScene
from PySide6.QtCore import QPointF
import sys

from packages.base.node import BaseNode, Port

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestBaseNode(unittest.TestCase):
    """Test cases for the BaseNode class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = QGraphicsScene()
        self.node = BaseNode(title="Test Node")
        self.scene.addItem(self.node)
        
    def test_initialization(self):
        """Test that a node is properly initialized"""
        self.assertEqual(self.node.title, "Test Node")
        self.assertEqual(len(self.node.input_ports), 0)
        self.assertEqual(len(self.node.output_ports), 0)
        self.assertTrue(self.node.flags() & BaseNode.ItemIsMovable)
        self.assertTrue(self.node.flags() & BaseNode.ItemIsSelectable)
        
    def test_add_ports(self):
        """Test adding ports to a node"""
        # Add input port
        input_port = self.node.add_input_port("test_input")
        self.assertIsInstance(input_port, Port)
        self.assertEqual(input_port.name, "test_input")
        self.assertTrue(input_port.is_input)
        self.assertEqual(len(self.node.input_ports), 1)
        self.assertIn("test_input", self.node.input_ports)
        
        # Add output port
        output_port = self.node.add_output_port("test_output")
        self.assertIsInstance(output_port, Port)
        self.assertEqual(output_port.name, "test_output")
        self.assertFalse(output_port.is_input)
        self.assertEqual(len(self.node.output_ports), 1)
        self.assertIn("test_output", self.node.output_ports)
        
    def test_port_positions(self):
        """Test that ports are positioned correctly"""
        input_port = self.node.add_input_port("test_input")
        output_port = self.node.add_output_port("test_output")
        
        # Input port should be on the left side
        self.assertEqual(input_port.relative_pos.x(), 0)
        self.assertGreater(input_port.relative_pos.y(), self.node.header_height)
        
        # Output port should be on the right side
        self.assertEqual(output_port.relative_pos.x(), self.node.width)
        self.assertGreater(output_port.relative_pos.y(), self.node.header_height)
        
    def test_port_at_position(self):
        """Test finding a port at a given position"""
        input_port = self.node.add_input_port("test_input")
        output_port = self.node.add_output_port("test_output")
        
        # Test position at input port
        port_pos = input_port.relative_pos
        found_port = self.node.port_at_position(port_pos)
        self.assertEqual(found_port, input_port)
        
        # Test position at output port
        port_pos = output_port.relative_pos
        found_port = self.node.port_at_position(port_pos)
        self.assertEqual(found_port, output_port)
        
        # Test position not at any port
        no_port = self.node.port_at_position(QPointF(self.node.width / 2, self.node.height / 2))
        self.assertIsNone(no_port)
        
    def test_node_height_adjustment(self):
        """Test that node height adjusts based on number of ports"""
        initial_height = self.node.height
        
        # Add several ports
        for i in range(5):
            self.node.add_input_port(f"input_{i}")
            
        # Height should have increased
        self.assertGreater(self.node.height, initial_height)
        
if __name__ == '__main__':
    unittest.main() 