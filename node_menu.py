from PySide6.QtWidgets import QMenu, QLineEdit, QVBoxLayout, QWidget, QWidgetAction
from PySide6.QtCore import Qt, Signal, QEvent, QObject
from PySide6.QtGui import QAction

class NodeSearchMenu(QMenu):
    """
    Custom menu with search functionality for node selection.
    """
    nodeSelected = Signal(str)  # Signal emitted when a node is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the search widget
        self.search_widget = QWidget()
        self.search_layout = QVBoxLayout(self.search_widget)
        self.search_layout.setContentsMargins(5, 5, 5, 5)
        self.search_layout.setSpacing(0)
        
        # Create the search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search nodes...")
        self.search_bar.textChanged.connect(self.filter_nodes)
        self.search_layout.addWidget(self.search_bar)
        
        # Add the search widget to the menu
        search_action = QWidgetAction(self)
        search_action.setDefaultWidget(self.search_widget)
        self.addAction(search_action)
        
        # Add a separator
        self.addSeparator()
        
        # Store all node actions
        self.all_node_actions = {}
        self.category_menus = {}
        
        # Install event filter to handle key navigation
        self.installEventFilter(self)
        
    def add_node_category(self, category_name):
        """Add a category submenu"""
        category_menu = self.addMenu(category_name)
        self.category_menus[category_name] = category_menu
        return category_menu
        
    def add_node_action(self, category, node_name, node_class):
        """Add a node action to the specified category"""
        if category not in self.category_menus:
            category_menu = self.add_node_category(category)
        else:
            category_menu = self.category_menus[category]
            
        action = category_menu.addAction(node_name)
        self.all_node_actions[node_name] = {
            'action': action,
            'category': category,
            'node_class': node_class
        }
        return action
        
    def filter_nodes(self, text):
        """Filter nodes based on search text"""
        # If search is empty, show all categories and nodes
        if not text:
            for category, menu in self.category_menus.items():
                menu.menuAction().setVisible(True)
                
            for node_info in self.all_node_actions.values():
                node_info['action'].setVisible(True)
            return
            
        # Hide all category menus initially
        for category, menu in self.category_menus.items():
            menu.menuAction().setVisible(False)
            
        # Show only matching nodes and their categories
        text = text.lower()
        for node_name, node_info in self.all_node_actions.items():
            visible = text in node_name.lower()
            node_info['action'].setVisible(visible)
            
            # If any node in a category is visible, make the category visible
            if visible:
                category = node_info['category']
                self.category_menus[category].menuAction().setVisible(True)
                
    def eventFilter(self, obj, event):
        """Handle keyboard events for the menu"""
        if event.type() == QEvent.KeyPress:
            # Focus on search bar when typing starts
            if event.key() not in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape):
                if not self.search_bar.hasFocus():
                    self.search_bar.setFocus()
                    # Send the key event to the search bar
                    self.search_bar.event(event)
                    return True
                    
        return super().eventFilter(obj, event)
        
    def showEvent(self, event):
        """Focus the search bar when the menu is shown"""
        super().showEvent(event)
        self.search_bar.setFocus() 