from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter


class NodeView(QGraphicsView):
    def __init__(self, scene):
        super().__init__()  # Initialize without scene first
        
        # Enable antialiasing for smoother drawing
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Set up the view behavior
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Initialize panning variables
        self._panning = False
        self._panStart = None
        
        # Zoom parameters
        self.zoomInFactor = 1.015  # Reduced to 1.5% per step
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.minScale = 0.1  # Minimum zoom level (10%)
        self.maxScale = 5.0  # Maximum zoom level (500%)
        
        # Set up scrollbar behavior
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Set up context menu handling
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        
        # Set the scene after configuring the view
        self.setScene(scene)
        
        # Set scene rect with some padding
        self.updateSceneRect()
        
        # Connect to scene changes
        if scene:
            scene.changed.connect(self.onSceneChanged)
            
        # Center the view
        self.centerOn(0, 0)

    def updateSceneRect(self):
        """Update the scene rectangle to encompass all items plus padding"""
        if self.scene():
            # Get the current scene rect
            rect = self.scene().itemsBoundingRect()
            
            # Add padding
            padding = 100
            rect.adjust(-padding, -padding, padding, padding)
            
            # Set the new scene rect
            self.scene().setSceneRect(rect)
            
            # Update scrollbar visibility
            self.updateScrollBarVisibility()

    def updateScrollBarVisibility(self):
        """Update scrollbar visibility based on content"""
        # Get the viewport and scene rects
        viewport_rect = self.viewport().rect()
        scene_rect = self.scene().sceneRect()
        
        # Transform viewport rect to scene coordinates
        visible_rect = self.mapToScene(viewport_rect).boundingRect()
        
        # Show scrollbars only if content extends beyond visible area
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded if scene_rect.width() > visible_rect.width() 
            else Qt.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded if scene_rect.height() > visible_rect.height() 
            else Qt.ScrollBarAlwaysOff
        )

    def onSceneChanged(self, region):
        """Handle scene changes"""
        self.updateSceneRect()

    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        self.updateScrollBarVisibility()

    def wheelEvent(self, event):
        # Get the current scale
        current_scale = self.transform().m11()
        
        # Calculate zoom factor based on wheel delta
        zoom_factor = 1.2
        
        # Determine zoom direction
        if event.angleDelta().y() > 0:
            # Zoom in
            self.scale(zoom_factor, zoom_factor)
        else:
            # Zoom out
            self.scale(1.0 / zoom_factor, 1.0 / zoom_factor)
            
        # Prevent event from propagating further
        event.accept()
        
    def zoom_in(self):
        """Zoom in by a fixed factor (for testing)"""
        zoom_factor = 1.2
        self.scale(zoom_factor, zoom_factor)
        
    def zoom_out(self):
        """Zoom out by a fixed factor (for testing)"""
        zoom_factor = 1.2
        self.scale(1.0 / zoom_factor, 1.0 / zoom_factor)

    def mousePressEvent(self, event):
        # Get the item under the mouse
        item_under_mouse = self.itemAt(event.pos())
        
        # If clicking on an item, pass the event to the scene
        if item_under_mouse:
            super().mousePressEvent(event)
            return
            
        # Handle right-click for context menu (only if not on a node)
        if event.button() == Qt.RightButton:
            if self.scene():
                scene_pos = self.mapToScene(event.pos())
                self.scene().showContextMenu(scene_pos)
            event.accept()
            return
            
        # Handle middle button for panning
        elif event.button() == Qt.MiddleButton:
            self._panning = True
            self._panStart = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
            
        # Pass other events to the base handler
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._panStart:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._panStart)
            self._panStart = event.pos()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self._panStart = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)