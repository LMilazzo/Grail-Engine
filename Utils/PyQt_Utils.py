
# >>> CLEAR LAYOUT >>>
def clear_layout(self, layout):
    if layout is None:
        return
    
    # while layout.count() effectively clears everything from top to bottom
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        
        if widget is not None:
            # Safely delete the widget
            widget.deleteLater()
        elif item.layout() is not None:
            # Recursively clear sub-layouts
            self.clear_layout(item.layout())
            # After internal items are gone, delete the sub-layout itself
            item.layout().deleteLater()
            # After handling the contents, delete the layout item itself
            del item
# <<< Clear Layout <<<