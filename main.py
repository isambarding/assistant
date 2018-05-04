from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class Container(BoxLayout):
    pass


class AssistantApp(App):
    def build(self):
        self.title = 'Assistant'
        return Container()


if __name__ == "__main__":
    app = AssistantApp()
    app.run()
