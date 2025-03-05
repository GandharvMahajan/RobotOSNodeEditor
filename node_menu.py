from PySide6.QtWidgets import QMenu, QLineEdit, QVBoxLayout, QWidget, QWidgetAction
from PySide6.QtCore import Qt, Signal, QEvent, QObject
from PySide6.QtGui import QFont, QAction

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
        self.section_titles = {}
        self.submenus = {}
        
        # Install event filter to handle key navigation
        self.installEventFilter(self)
        
    def add_section_title(self, title):
        """Add a section title with a separator line"""
        if title in self.section_titles:
            return self.section_titles[title]
            
        # Add a separator before the title (except for the first title)
        if self.section_titles:
            self.addSeparator()
            
        # Create a disabled action for the title
        title_action = QAction(title, self)
        title_action.setEnabled(False)
        
        # Make the title bold and slightly larger
        font = title_action.font()
        font.setBold(True)
        title_action.setFont(font)
        
        self.addAction(title_action)
        self.section_titles[title] = title_action
        
        # Add a separator after the title
        separator = self.addSeparator()
        
        return title_action
        
    def add_submenu(self, section, submenu_name):
        """Add a submenu under a section"""
        # Create the key for this submenu
        key = f"{section}/{submenu_name}"
        
        # Return existing submenu if it exists
        if key in self.submenus:
            return self.submenus[key]
            
        # Make sure the section exists
        if section not in self.section_titles:
            self.add_section_title(section)
            
        # Create the submenu
        submenu = QMenu(submenu_name, self)
        self.addMenu(submenu)
        self.submenus[key] = submenu
        
        return submenu
        
    def add_node_action(self, category, node_name, node_class, submenu=None):
        """Add a node action under the specified category and optional submenu"""
        if submenu:
            # Format: "Section/Submenu"
            parts = category.split('/')
            if len(parts) == 2:
                section, submenu_name = parts
                # Get or create the submenu
                menu = self.add_submenu(section, submenu_name)
                
                # Add the action to the submenu
                action = menu.addAction(node_name)
            else:
                # Invalid format, use as a section
                if category not in self.section_titles:
                    self.add_section_title(category)
                action = QAction(node_name, self)
                self.addAction(action)
        else:
            # Add as a direct action under a section
            if category not in self.section_titles:
                self.add_section_title(category)
                
            # Add the node action
            action = QAction(node_name, self)
            self.addAction(action)
        
        # Store the action info
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
            # Show all section titles
            for title, action in self.section_titles.items():
                action.setVisible(True)
                
            # Show all submenus
            for key, submenu in self.submenus.items():
                submenu.menuAction().setVisible(True)
                
            # Show all node actions
            for node_info in self.all_node_actions.values():
                node_info['action'].setVisible(True)
                
            # Show all separators
            for action in self.actions():
                if action.isSeparator():
                    action.setVisible(True)
                    
            return
            
        # Convert search text to lowercase for case-insensitive search
        text = text.lower()
        
        # Track which categories have visible nodes
        visible_categories = set()
        visible_submenus = set()
        
        # First pass: determine which nodes match the search
        for node_name, node_info in self.all_node_actions.items():
            visible = text in node_name.lower()
            node_info['action'].setVisible(visible)
            
            if visible:
                category = node_info['category']
                if '/' in category:
                    # This is a submenu item
                    visible_submenus.add(category)
                    # Also mark the parent section as visible
                    visible_categories.add(category.split('/')[0])
                else:
                    # This is a direct section item
                    visible_categories.add(category)
                
        # Second pass: show/hide section titles and separators
        for title, action in self.section_titles.items():
            action.setVisible(title in visible_categories)
            
        # Show/hide submenus
        for key, submenu in self.submenus.items():
            submenu.menuAction().setVisible(key in visible_submenus)
            
        # Hide separators if no nodes are visible in a category
        prev_was_separator = False
        for action in self.actions():
            if action.isSeparator():
                # Don't show consecutive separators
                if prev_was_separator:
                    action.setVisible(False)
                prev_was_separator = True
            else:
                prev_was_separator = False
                
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