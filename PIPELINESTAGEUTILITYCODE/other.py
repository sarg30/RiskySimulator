from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

class MyLabel(ButtonBehavior, Label):
	cursor_blink = True
	cur = "[color=ff3333]|[/color]"

	def schedule_cursor(self, focus):
		if focus:
			self.cursor_event = Clock.schedule_interval(self.cursor, .5)
		else:
			Clock.unschedule(self.cursor_event)
			self.text = self.text.replace(self.cur, "")
	
	def format_text(self):
		self.text = self.text.replace("proud", "[color=3333ff]proud[/color]")
		return True
	
	def cursor(self, dt):
		if self.cursor_blink:
			self.text = self.text + self.cur
		else:
			self.text = self.text.replace(self.cur, "")
		self.cursor_blink = not self.cursor_blink
			
KV = """
<MyTextInput@ScreenManager>:
	Screen:
		MyLabel:
			font_size: "40sp"
			id: ml
			focus: False
			on_release:
				ti.focus = True
			markup: True
			text: ti.text
	Screen:
		TextInput:
			size_hint_x: 0.0
			id: ti
			on_focus:
				ml.schedule_cursor(self.focus)
			on_text:
				ml.format_text()
BoxLayout:
	orientation: "vertical"
	MyTextInput:
	Button:
		font_size: "40sp"
		text: "Some other widget!"
"""

class TestApp(App):
	def build(self):
		return Builder.load_string(KV)

TestApp().run()