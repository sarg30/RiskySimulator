from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

Builder.load_string('''
#:import ScrollEffect  kivy.effects.scroll.ScrollEffect
#:import Button kivy.uix.button.Button
<Label>:
    font_name:'Arial'
    font_size:'18sp'
<GridLayout>:
    cols:3
    rows:1
    ScrollView:
        id:scroller
        effect_cls: ScrollEffect
        Label:
            id: ti
            size_hint: (None, None)
            width: scroller.width
            #height: max(self.minimum_height, scroller.height)
            font_size: '45sp'
            cursor_color: (.17, .18, .17, 1)
            background_color: [255,255,255,1]
            foreground_color:(.17, .18, .17, 1)
            font_name: 'Arial'
            selection_color: (1,1,1,0.125)
            on_text: app.text_changed()
''')

class ScrollBothApp(App):
    def build(self):
        self.grid = GridLayout()
        return self.grid

    def text_changed(self, *args):
        width_calc = self.grid.ids.scroller.width
        for line_label in self.grid.ids.ti._lines_labels:
            width_calc = max(width_calc, line_label.width)   # add 20 to avoid automatically creating a new line
        self.grid.ids.ti.width = width_calc



ScrollBothApp().run()