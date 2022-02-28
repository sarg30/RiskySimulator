from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder


class MyGridLayout(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class MyApp(App):
    def build(self):
        return MyGridLayout()
Builder.load_file('texting.kv')
if __name__ =='__main__':
    MyApp().run()

