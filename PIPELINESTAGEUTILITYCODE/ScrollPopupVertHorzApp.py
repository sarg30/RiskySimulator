from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class ScrollablePopup(BoxLayout):
    contentBox = ObjectProperty()
    scrollView = ObjectProperty()


    def scrollToTop(self):
        self.scrollView.scroll_y = 1 # force scrolling to top

    def scrollToBottom(self):
        self.scrollView.scroll_y = 0 # force scrolling to bottom

    def initText(self, text):
        self.contentBox.content.text = text

    def write(self):
        text = u"[b]Lorem ipsum dolor sit amet[/b], consectetur adipiscing elit. Phasellus odio nisi, pellentesque molestie adipiscing vitae, aliquam at tellus.\nFusce quis est ornare erat pulvinar elementum ut sed felis. Donec vel neque mauris. In sit amet nunc sit amet diam dapibus lacinia.\nIn sodales placerat mauris, ut euismod augue laoreet at. Integer in neque non odio fermentum volutpat nec nec nulla.\nDonec et risus non mi viverra posuere. Phasellus cursus augue purus, eget volutpat leo. Phasellus sed dui vitae ipsum mattis facilisis vehicula eu justo.\nQuisque neque dolor, egestas sed venenatis eget, porta id ipsum. Ut faucibus, massa vitae imperdiet rutrum, sem dolor rhoncus magna, non lacinia nulla risus non dui.\nNulla sit amet risus orci. Nunc libero justo, interdum eu pulvinar vel, pulvinar et lectus. Phasellus sed luctus diam. Pellentesque non feugiat dolor.\nCras at dolor velit, gravida congue velit. Aliquam erat volutpat. Nullam eu nunc dui, quis sagittis dolor. Ut nec dui eget odio pulvinar placerat.\nPellentesque mi metus, tristique et placerat ac, pulvinar vel quam. Nam blandit magna a urna imperdiet molestie. Nullam ut nisi eget enim laoreet sodales sit amet a felis.\n"

        for i in range(0, 4):
            text += text

        self.initText(text)

class ScrollPopup(BoxLayout):
    popup = None

    def openPopup(self):
        self.popup = ScrollablePopup(title="Scrollable popup")
        text = u"[b]Lorem ipsum dolor sit amet[/b], consectetur adipiscing elit. Phasellus odio nisi, pellentesque molestie adipiscing vitae, aliquam at tellus.\nFusce quis est ornare erat pulvinar elementum ut sed felis. Donec vel neque mauris. In sit amet nunc sit amet diam dapibus lacinia.\nIn sodales placerat mauris, ut euismod augue laoreet at. Integer in neque non odio fermentum volutpat nec nec nulla.\nDonec et risus non mi viverra posuere. Phasellus cursus augue purus, eget volutpat leo. Phasellus sed dui vitae ipsum mattis facilisis vehicula eu justo.\nQuisque neque dolor, egestas sed venenatis eget, porta id ipsum. Ut faucibus, massa vitae imperdiet rutrum, sem dolor rhoncus magna, non lacinia nulla risus non dui.\nNulla sit amet risus orci. Nunc libero justo, interdum eu pulvinar vel, pulvinar et lectus. Phasellus sed luctus diam. Pellentesque non feugiat dolor.\nCras at dolor velit, gravida congue velit. Aliquam erat volutpat. Nullam eu nunc dui, quis sagittis dolor. Ut nec dui eget odio pulvinar placerat.\nPellentesque mi metus, tristique et placerat ac, pulvinar vel quam. Nam blandit magna a urna imperdiet molestie. Nullam ut nisi eget enim laoreet sodales sit amet a felis.\n"

        for i in range(0, 4):
            text += text

        self.popup.initText(text)
        self.popup.open()

class ScrollPopupVertHorzApp(App):
    def build(self): # implicitly looks for a kv file of name kivylistview1111.kv which is
                     # class name without App, in lowercases

        Config.set('graphics', 'width', '900')
        Config.set('graphics', 'height', '600')
        Config.write()

        return ScrollablePopup()

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

if __name__ == '__main__':
    ScrollPopupVertHorzApp().run()