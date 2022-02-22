from re import L
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

def myfunc(stuff):
    for i in range (len(stuff)):
        print(stuff[i])


#myfunc("fuckoff")
class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout,self).__init__(**kwargs)
        
        self.cols =2
        self.add_widget(Label(text="name"))
        self.name = TextInput(multiline = False)
        self.add_widget(self.name)

        self.add_widget(Label(text="pizza"))
        self.pizza = TextInput(multiline = False)
        self.add_widget(self.pizza)

class MyApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
