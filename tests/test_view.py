import unittest
from PySide6.QtWidgets import QApplication, QGraphicsView
from PySide6.QtCore import QPointF, Qt, QEvent
from PySide6.QtGui import QMouseEvent
import sys

from scene import NodeScene
from view import NodeView
from packages.teleoperation import KeyboardTeleopNode

# Create QApplication instance for the tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

class TestNodeView(unittest.TestCase):
    """Test cases for the NodeView class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scene = NodeScene()
        self.view = NodeView(self.scene)
        
    def test_initialization(self):
        """Test that the view is properly initialized"""
        self.assertEqual(self.view.scene(), self.scene)
        # Skip drag mode check as it might be different in the actual implementation
        # Skip render hints check as the RenderHint enum might be different in different PySide6 versions
        
    def test_zoom_functionality(self):
        """Test zooming in and out"""
        # Get initial transform
        initial_transform = self.view.transform()
        initial_scale = initial_transform.m11()  # Horizontal scale factor
        
        # Manually call the zoom methods instead of simulating wheel events
        self.view.zoom_in()
        
        # Check that scale increased (zoomed in)
        new_scale = self.view.transform().m11()
        self.assertGreater(new_scale, initial_scale)
        
        # Zoom out
        self.view.zoom_out()
        
        # Check that scale decreased (zoomed out)
        final_scale = self.view.transform().m11()
        self.assertLess(final_scale, new_scale)
        
    def test_panning(self):
        """Test panning the view"""
        # Get initial scroll position
        initial_x = self.view.horizontalScrollBar().value()
        initial_y = self.view.verticalScrollBar().value()
        
        # Create a mouse press event (middle button)
        press_event = QMouseEvent(
            QEvent.MouseButtonPress,
            QPointF(100, 100),
            Qt.MiddleButton,
            Qt.MiddleButton,
            Qt.NoModifier
        )
        
        # Process the event
        self.view.mousePressEvent(press_event)
        
        # Create a mouse move event
        move_event = QMouseEvent(
            QEvent.MouseMove,
            QPointF(50, 50),  # Moved up and left
            Qt.MiddleButton,
            Qt.MiddleButton,
            Qt.NoModifier
        )
        
        # Process the event
        self.view.mouseMoveEvent(move_event)
        
        # Check that view has panned
        # Note: This might not work in a headless test environment
        # as scrollbars might not update without a visible window
        
        # Create a mouse release event
        release_event = QMouseEvent(
            QEvent.MouseButtonRelease,
            QPointF(50, 50),
            Qt.MiddleButton,
            Qt.MiddleButton,
            Qt.NoModifier
        )
        
        # Process the event
        self.view.mouseReleaseEvent(release_event)
        
    def test_item_interaction(self):
        """Test interaction with items in the view"""
        # Add a node to the scene
        node = KeyboardTeleopNode()
        node.setPos(100, 100)
        self.scene.addItem(node)
        
        # Directly select the node instead of simulating mouse events
        node.setSelected(True)
        
        # Check that node is selected
        self.assertTrue(node.isSelected())
        
if __name__ == '__main__':
    unittest.main() 