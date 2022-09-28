from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.metrics import dp

class WidgetsTest(BoxLayout):
    count = NumericProperty(0)
    def button_click(self):
        self.count += 1

class StackLayoutTest(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = []
        for i in range(0, 100):
            b.append(Button(text=str(i+1), size_hint=(None, None), width=dp(100), height=dp(100)))
            self.add_widget(b[i])

# class GridLayoutTest(GridLayout):
#     pass

class AnchorLayoutTest(AnchorLayout):
    pass

class MainWidget(BoxLayout):
    pass

class MainApp(App):
    pass

if __name__ == "__main__":
    MainApp().run()
