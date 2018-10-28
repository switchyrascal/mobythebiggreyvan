# Install by adding a button using the macro dialog
# Use by selecting part you want to move then the part you want to replace,
# and press the button
import FreeCADGui

class ReplacePart():
    def __init__(self, gui):
        sel = gui.Selection.getSelection()
        if 2 != len(sel):
            print('Move first selection to second selection position')
            print('Select 2 objects exactly')
        else :
            self.replace_part(sel[1], sel[0])
            gui.updateGui()

    def replace_part(self, src, dst):
        print('Moving "' + src.Label + '" to "' + dst.Label + '"')
        dst.Placement = src.Placement
        for property, expression in src.ExpressionEngine:
            if property.startswith('Placement'):
                dst.setExpression(property, expression)
        if src.ViewObject and dst.ViewObject:
            dst.ViewObject.DiffuseColor = src.ViewObject.DiffuseColor
            dst.ViewObject.DisplayMode = src.ViewObject.DisplayMode
            dst.ViewObject.LineColor = src.ViewObject.LineColor
            dst.ViewObject.PointColor = src.ViewObject.PointColor
            dst.ViewObject.ShapeColor = src.ViewObject.ShapeColor
            dst.ViewObject.Transparency = src.ViewObject.Transparency
        label = src.Label
        src.Label = label + ' old'
        dst.Label = label

ReplacePart(FreeCADGui)
