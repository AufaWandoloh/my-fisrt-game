from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image

# ตั้งค่าขนาดหน้าต่าง
Window.size = (800, 600)


# หน้าจอเมนู
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # สร้าง Label สำหรับแสดงชื่อเกม
        title_label = Label(
            text="The Enchanter's Fate",
            font_size=48,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        self.add_widget(title_label)

        # สร้างปุ่ม Next
        next_button = Button(
            text="Next",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )
        next_button.bind(on_press=self.go_to_game)
        self.add_widget(next_button)

    def go_to_game(self, instance):
        # เปลี่ยนหน้าจอไปยังเกม
        self.manager.current = "game"


# หน้าจอเกม (TheEnchantersFateGame)
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = TheEnchantersFateGame()
        self.add_widget(self.game)


# เกม The Enchanter's Fate
class TheEnchantersFateGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = 11  # ขนาดของแผนที่ (10x10)
        self.cell_size = 50  # ขนาดของแต่ละช่องในตาราง
        self.obstacles = [
            (0, 5),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 5),
            (1, 6),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 3),
            (3, 5),
            (3, 6),
            (3, 7),
            (3, 9),
            (3, 10),
            (4, 1),
            (4, 7),
            (5, 1),
            (5, 2),
            (5, 7),
            (5, 8),
            (5, 9),
            (6, 9),
            (7, 0),
            (7, 1),
            (7, 3),
            (7, 4),
            (7, 5),
            (7, 6),
            (7, 7),
            (7, 9),
            (8, 3),
            (9, 3),
            (9, 9),
            (10, 9),
        ]  # ตำแหน่งของหิน
        self.position = [2, 0]  # ตำแหน่งผู้เล่นเริ่มต้น
        self.exit_position = (2, 10)  # ตำแหน่งประตู

        # ตั้งค่าขนาดหน้าต่าง
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        # คำนวณตำแหน่งตารางให้อยู่ตรงกลาง
        self.offset_x = (Window.width - self.grid_size * self.cell_size) // 2
        self.offset_y = (Window.height - self.grid_size * self.cell_size) // 2

        # วาดองค์ประกอบต่างๆ
        self.draw_grid()
        self.draw_obstacles()
        self.draw_character()
        self.draw_exit()

        # เพิ่มข้อความคำแนะนำ
        self.add_instructions()

        # ผูกการกดปุ่มกับฟังก์ชันการเคลื่อนที่
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.game_over = False  # ตัวแปรสำหรับตรวจสอบว่าเกมจบแล้วหรือไม่
        self.key_pressed = False

    def draw_grid(self):
        """วาดตารางหมากรุก"""
        with self.canvas:
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if (row + col) % 2 == 0:
                        Color(0.8, 0.2, 0.2)  # สีแดงอ่อน
                    else:
                        Color(0.6, 0.1, 0.1)  # สีแดงเข้ม
                    Rectangle(
                        pos=(
                            col * self.cell_size + self.offset_x,
                            row * self.cell_size + self.offset_y,
                        ),
                        size=(self.cell_size, self.cell_size),
                    )

    def draw_obstacles(self):
        """วาดหินในแผนที่"""
        for x, y in self.obstacles:
            obstacle_image = Image(
                source="big rock.png",  # แก้ไขให้เป็นไฟล์ PNG ที่ใช้
                pos=(
                    x * self.cell_size + self.offset_x,
                    y * self.cell_size + self.offset_y,
                ),
                size=(self.cell_size, self.cell_size),
            )
            self.add_widget(obstacle_image)

    def draw_character(self):
        """วาดตัวละคร"""
        with self.canvas:
            Color(0, 0, 1)  # สีฟ้าสำหรับตัวละคร
            Rectangle(
                pos=(
                    self.position[0] * self.cell_size + self.offset_x,
                    self.position[1] * self.cell_size + self.offset_y,
                ),
                size=(self.cell_size, self.cell_size),
            )

    def draw_exit(self):
        """วาดตำแหน่งประตู"""
        with self.canvas:
            Color(1, 1, 0)  # สีเหลืองสำหรับประตู
            Rectangle(
                pos=(
                    self.exit_position[0] * self.cell_size + self.offset_x,
                    self.exit_position[1] * self.cell_size + self.offset_y,
                ),
                size=(self.cell_size, self.cell_size),
            )

    def add_instructions(self):
        """เพิ่มข้อความคำแนะนำ"""
        self.instructions = Label(
            text="W A S D FOR WALK",
            font_size=30,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos=(Window.width // 2 - 100, 20),
        )
        self.add_widget(self.instructions)

    def check_win(self):
        """ตรวจสอบว่าผู้เล่นชนะแผนที่หรือไม่"""
        if self.position == list(self.exit_position):
            self.game_over = True
            win_label = Label(
                text="YOU WIN!",
                font_size=50,
                bold=True,
                color=(0, 1, 0, 1),
                size_hint=(None, None),
                pos=(Window.width // 2 - 100, Window.height // 2 - 25),
            )
            self.add_widget(win_label)

    def move(self, dx, dy):
        """ฟังก์ชันเคลื่อนที่ตัวละคร"""
        if self.game_over:
            return

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if (
            0 <= new_x < self.grid_size
            and 0 <= new_y < self.grid_size
            and (new_x, new_y) not in self.obstacles
        ):
            self.position = [new_x, new_y]

        # วาดตัวละครใหม่
        self.canvas.clear()
        self.draw_grid()
        self.draw_obstacles()
        self.draw_character()
        self.draw_exit()
        self.check_win()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        """ฟังก์ชันตรวจจับการกดปุ่ม"""
        if not self.key_pressed:  # ถ้าปุ่มยังไม่ได้ถูกกด
            self.key_pressed = True
            if key == 119:  # W
                self.move(0, 1)
            elif key == 115:  # S
                self.move(0, -1)
            elif key == 97:  # A
                self.move(-1, 0)
            elif key == 100:  # D
                self.move(1, 0)

    def on_key_up(self, window, key, scancode):
        """ฟังก์ชันตรวจจับการปล่อยปุ่ม"""
        self.key_pressed = False  # รีเซ็ตสถานะเมื่อปล่อยปุ่ม


# ตัวจัดการหน้าจอ
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    GameApp().run()
