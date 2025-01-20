from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from random import randint


class HelltakerGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = 10  # ขนาดของแผนที่ (10x10)
        self.cell_size = 50  # ขนาดของแต่ละช่องในตาราง
        self.obstacles = self.generate_obstacles()  # สร้างตำแหน่งหิน
        self.position = self.generate_starting_position()  # ตำแหน่งผู้เล่น
        self.exit_position = (self.grid_size // 2, self.grid_size - 1)  # ตำแหน่งประตู
        self.instructions = None  # สำหรับข้อความแสดงผล

        # ตั้งค่าขนาดหน้าต่าง (ไม่ fullscreen)
        Window.size = (800, 600)  # กำหนดขนาดหน้าต่าง
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # สีพื้นหลังของหน้าต่าง

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

    def generate_obstacles(self):
        """สร้างตำแหน่งของหิน"""
        obstacles = []
        for _ in range(10):  # จำนวนหิน 10 ก้อน
            while True:
                x, y = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
                if (x, y) not in obstacles and (x, y) != (
                    self.grid_size // 2,
                    self.grid_size - 1,
                ):
                    obstacles.append((x, y))
                    break
        return obstacles

    def draw_obstacles(self):
        """วาดหินในแผนที่"""
        with self.canvas:
            Color(0.4, 0.4, 0.4)  # สีเทา
            for x, y in self.obstacles:
                Rectangle(
                    pos=(
                        x * self.cell_size + self.offset_x,
                        y * self.cell_size + self.offset_y,
                    ),
                    size=(self.cell_size, self.cell_size),
                )

    def generate_starting_position(self):
        """สร้างตำแหน่งเริ่มต้นของผู้เล่นที่ไม่ทับกับหิน"""
        while True:
            x, y = randint(0, self.grid_size - 1), randint(0, self.grid_size - 1)
            if (x, y) not in self.obstacles:
                return [x, y]

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
            pos=(Window.width // 2 - 100, 20),  # ตำแหน่งข้อความอยู่ตรงกลางด้านล่าง
        )
        self.add_widget(self.instructions)

    def check_win(self):
        """ตรวจสอบว่าผู้เล่นชนะแผนที่หรือไม่"""
        if self.position == list(self.exit_position):
            self.instructions.text = "YOU WIN!"
            self.game_won = True  # ตั้งค่าให้เกมชนะ

    def move(self, dx, dy):
        """ฟังก์ชันเคลื่อนที่ตัวละคร"""
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
        if key == 119:  # W
            self.move(0, 1)
        elif key == 115:  # S
            self.move(0, -1)
        elif key == 97:  # A
            self.move(-1, 0)
        elif key == 100:  # D
            self.move(1, 0)


class HelltakerApp(App):
    def build(self):
        return HelltakerGame()


if __name__ == "__main__":
    HelltakerApp().run()
