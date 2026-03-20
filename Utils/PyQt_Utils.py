
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

# >>> RECURSIVE WIDGET REMOVAL >>> 
def remove_widget_from_layout_rec(layout, object_name: str):
    
    # Iterate objects in given layout
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        
        # Iterate Widgets in current layout
        if item.widget():
            widget = item.widget()
            #print(widget.objectName()) DEBUG LISTING
            if widget.objectName() == object_name:
                layout.removeWidget(widget)
                widget.deleteLater()
                return True
            
        # Recursive call to next sub layout
        elif item.layout():
            if remove_widget_from_layout_rec(item.layout(), object_name):
                return True
    
    # Nothing left to iterate
    return False

# <<< RECURSIVE WIDGET REMOVAL <<<
