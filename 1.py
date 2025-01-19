from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

# ตั้งค่าขนาดหน้าจอ
Window.size = (800, 600)


# หน้าจอหลักที่แสดงชื่อเกมและปุ่มเริ่ม
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # เพิ่มภาพพื้นหลัง
        self.background = Image(
            source=r"c:\Users\aufaw_nq8olti\OneDrive\รูปภาพ\ภาพหน้าจอ\moxi.png",
            size=Window.size,
            pos=(0, 0),
        )
        self.add_widget(self.background)

        # สร้างปุ่มเริ่มเกม
        start_button = Button(
            text="Start Game",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

    def start_game(self, instance):
        # เมื่อกดปุ่มเริ่มเกมให้เปลี่ยนไปที่หน้าจอเกม
        self.manager.current = "game"


# หน้าจอเกม
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text="This is the game screen!",
            font_size=32,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.label)


class GameApp(App):
    def build(self):
        # สร้าง ScreenManager เพื่อจัดการหน้าจอ
        sm = ScreenManager()

        # เพิ่มหน้าจอเมนูและหน้าจอเกม
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))

        return sm


if __name__ == "__main__":
    GameApp().run()
