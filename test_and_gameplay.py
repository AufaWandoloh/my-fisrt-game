from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
import os

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
            text="Play",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )
        next_button.bind(on_press=self.go_to_story)  # เปลี่ยนเป็น go_to_story
        self.add_widget(next_button)

    def go_to_story(self, instance):
        # เปลี่ยนหน้าจอไปยัง StoryScreen
        self.manager.current = "story1"


class StoryScreen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ข้อความเรื่องราวในสเตจ 1
        story_text = """In a distant land, a powerful enchanter was trapped in a 
        demonic labyrinth by a malicious spell."""
        self.display_story(story_text)

        # ปุ่ม Next
        next_button = Button(
            text="Next",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )
        next_button.bind(on_press=self.go_to_next_screen)
        self.add_widget(next_button)

    def display_story(self, text):
        story_label = Label(
            text=text,
            font_size=24,
            size_hint=(None, None),
            size=(Window.width - 50, Window.height - 100),
            pos=(25, Window.height // 2),
            halign="center",
            valign="middle",
        )
        self.add_widget(story_label)

    def go_to_next_screen(self, instance):
        self.manager.current = "story2"  # เปลี่ยนไปยัง StoryScreen2


class StoryScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ข้อความเรื่องราวในสเตจ 2
        story_text = """To escape, the enchanter must navigate the maze, 
        avoid enemies, and find the magical exit."""
        self.display_story(story_text)

        # ปุ่ม Next
        next_button = Button(
            text="Next",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
        )
        next_button.bind(on_press=self.go_to_next_screen)
        self.add_widget(next_button)

    def display_story(self, text):
        story_label = Label(
            text=text,
            font_size=24,
            size_hint=(None, None),
            size=(Window.width - 50, Window.height - 100),
            pos=(25, Window.height // 2),
            halign="center",
            valign="middle",
        )
        self.add_widget(story_label)

    def go_to_next_screen(self, instance):
        self.manager.current = "game"  # เปลี่ยนไปยัง StoryScreen3


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = TheEnchantersFateGame()
        self.add_widget(self.game)

        # เพิ่ม UI ที่มุมขวาบน
        self.add_ui()

    def add_ui(self):
        """เพิ่ม UI สำหรับปุ่มเริ่มใหม่และปิดเสียง"""
        # ปุ่มเริ่มใหม่
        restart_button = Button(
            text="Restart",
            font_size=20,
            size_hint=(None, None),
            size=(120, 50),
            pos=(Window.width - 150, 20),
        )
        restart_button.bind(on_press=self.restart_game)
        self.add_widget(restart_button)

        # ปุ่มปิดเสียง
        mute_button = Button(
            text="Music on",
            font_size=20,
            size_hint=(None, None),
            size=(120, 50),
            pos=(Window.width - 150, 80),
        )
        mute_button.bind(on_press=self.toggle_sound)
        self.add_widget(mute_button)

    def restart_game(self, instance):
        """รีเซ็ตเกมใหม่ในด่านปัจจุบัน"""
        self.game.restart_level()

    def toggle_sound(self, instance):
        """เปิดหรือปิดเสียงเพลงพื้นหลัง"""
        app = App.get_running_app()
        if hasattr(app, "bg_music") and app.bg_music:
            if app.bg_music.state == "play":
                app.bg_music.stop()
                instance.text = "Music off"
            else:
                app.bg_music.play()
                instance.text = "Music on"


# เกม The Enchanter's Fate
class TheEnchantersFateGame(Widget):
    def __init__(self, level=1, **kwargs):
        super().__init__(**kwargs)
        self.level = level  # เก็บข้อมูลด่านปัจจุบัน
        self.grid_size = 11  # ขนาดของแผนที่
        self.cell_size = 50  # ขนาดของแต่ละช่องในตาราง
        self.obstacles = []  # อุปสรรคของแต่ละด่าน
        self.position = []  # ตำแหน่งเริ่มต้นของผู้เล่น
        self.exit_position = []  # ตำแหน่งของประตู
        self.enemy_position = []  # ตำแหน่งศัตรูสำหรับแต่ละด่าน

        # ตั้งค่าอุปสรรคและตำแหน่งสำหรับด่านเริ่มต้น
        self.setup_level()

        # ตั้งค่าขนาดหน้าต่าง
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        self.offset_x = (Window.width - self.grid_size * self.cell_size) // 2
        self.offset_y = (Window.height - self.grid_size * self.cell_size) // 2

        # วาดองค์ประกอบต่างๆ
        self.draw_grid()
        self.draw_obstacles()
        self.draw_character()
        self.draw_exit()
        self.draw_enemy()

        # เพิ่มข้อความคำแนะนำ
        self.add_instructions()

        # ผูกการกดปุ่มกับฟังก์ชันการเคลื่อนที่
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.game_over = False  # ตัวแปรสำหรับตรวจสอบว่าเกมจบแล้วหรือไม่
        self.key_pressed = False

    def setup_level(self):
        """ตั้งค่าด่านตามค่า self.level"""
        if self.level == 1:
            self.position = [2, 0]
            self.exit_position = (2, 10)
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
                (3, 7),
                (3, 10),
                (4, 1),
                (4, 5),
                (4, 7),
                (5, 1),
                (5, 2),
                (5, 5),
                (5, 6),
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
            ]
            self.enemy_position = [(8, 10)]  # ตำแหน่งศัตรูด่าน 1
        elif self.level == 2:
            self.position = [5, 4]
            self.exit_position = (9, 10)
            self.obstacles = [
                (1, 2),
                (1, 3),
                (1, 4),
                (1, 7),
                (1, 8),
                (1, 9),
                (2, 4),
                (3, 3),
                (3, 4),
                (3, 5),
                (3, 6),
                (3, 8),
                (3, 9),
                (5, 1),
                (6, 3),
                (6, 2),
                (7, 4),
                (7, 5),
                (7, 6),
                (7, 7),
                (7, 10),
                (8, 2),
                (9, 2),
                (9, 4),
                (9, 8),
                (9, 9),
                (10, 4),
            ]
            self.enemy_position = [(10, 10)]  # ตำแหน่งศัตรูด่าน 2
        elif self.level == 3:
            self.position = [0, 8]
            self.exit_position = (10, 8)
            self.obstacles = [
                (0, 3),
                (1, 1),
                (1, 3),
                (1, 4),
                (1, 5),
                (1, 9),
                (2, 1),
                (2, 9),
                (3, 1),
                (3, 9),
                (4, 1),
                (4, 2),
                (4, 3),
                (4, 4),
                (4, 5),
                (4, 9),
                (5, 9),
                (6, 7),
                (6, 9),
                (7, 7),
                (7, 9),
                (8, 7),
                (8, 9),
                (9, 1),
                (9, 2),
                (9, 3),
                (9, 5),
                (9, 7),
                (9, 9),
                (10, 1),
                (10, 5),
            ]
            self.enemy_position = [(6, 10)]

        else:
            self.position = [0, 0]
            self.exit_position = (10, 10)
            self.obstacles = []  # อุปสรรคสำหรับด่านอื่นๆ
            self.enemy_position = []  # ไม่มีศัตรูในด่านอื่น

    def restart_level(self):
        """เริ่มใหม่ในด่านปัจจุบัน"""
        self.game_over = False  # รีเซ็ตสถานะเกม
        self.setup_level()  # ตั้งค่าด่านใหม่

        # ล้างและวาดองค์ประกอบใหม่
        self.canvas.clear()
        self.draw_grid()
        self.draw_obstacles()
        self.draw_character()
        self.draw_exit()
        self.draw_enemy()
        self.add_instructions()

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

    def draw_enemy(self):
        """วาดศัตรูทั้งหมดในด่าน"""
        with self.canvas:
            for enemy in self.enemy_position:
                Color(0, 1, 0)  # สีเขียวสำหรับศัตรู
                Rectangle(
                    pos=(
                        enemy[0] * self.cell_size + self.offset_x,
                        enemy[1] * self.cell_size + self.offset_y,
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

    def move_enemy(self):
        """เคลื่อนที่ศัตรูแต่ละตัว"""
        steps = 2  # ศัตรูเดินได้ 2 ก้าวต่อรอบ
        prev_position = getattr(
            self, "prev_position", self.position
        )  # ตำแหน่งก่อนหน้าของผู้เล่น

        for idx, enemy in enumerate(self.enemy_position):
            for step in range(steps):  # ลูปเดิน 2 ครั้งสำหรับแต่ละศัตรู
                if step == 0:
                    # ก้าวแรก: เดินตามทิศทางการเคลื่อนที่ของผู้เล่น (จากตำแหน่งก่อนหน้า)
                    dx = prev_position[0] - enemy[0]
                    dy = prev_position[1] - enemy[1]
                else:
                    # ก้าวที่สอง: เดินเข้าหาผู้เล่นตามตำแหน่งปัจจุบัน
                    dx = self.position[0] - enemy[0]
                    dy = self.position[1] - enemy[1]

                # พยายามเดินในแนวตั้งก่อน
                if dx != 0:
                    step_x = 1 if dx > 0 else -1
                    new_x = enemy[0] + step_x
                    new_y = enemy[1]
                    if (new_x, new_y) not in self.obstacles:
                        self.enemy_position[idx] = (new_x, new_y)
                        enemy = (new_x, new_y)
                        continue

                # ถ้าไม่ได้ ให้เดินในแนวนอน
                if dy != 0:
                    step_y = 1 if dy > 0 else -1
                    new_x = enemy[0]
                    new_y = enemy[1] + step_y
                    if (new_x, new_y) not in self.obstacles:
                        self.enemy_position[idx] = (new_x, new_y)
                        enemy = (new_x, new_y)

        # บันทึกตำแหน่งปัจจุบันของผู้เล่นไว้เป็นตำแหน่งก่อนหน้าในการเคลื่อนที่ครั้งถัดไป
        self.prev_position = list(self.position)

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

        # วาดองค์ประกอบใหม่
        self.canvas.clear()
        self.draw_grid()
        self.draw_obstacles()
        self.draw_character()
        self.draw_exit()
        self.draw_enemy()
        self.move_enemy()

        # ตรวจสอบว่าผู้เล่นไปถึงประตูแล้วหรือยัง
        if self.position == list(self.exit_position):
            self.level += 1  # เพิ่มด่าน
            self.setup_level()

            # ล้างและวาดองค์ประกอบใหม่สำหรับด่านใหม่
            self.canvas.clear()
            self.draw_grid()
            self.draw_obstacles()
            self.draw_character()
            self.draw_exit()
            self.draw_enemy()

        # ตรวจสอบสถานะการแพ้ (หลังจากศัตรูเคลื่อนที่)
        if tuple(self.position) in self.enemy_position:
            self.game_over = True
            lose_label = Label(
                text="YOU LOSE!",
                font_size=50,
                bold=True,
                color=(1, 0, 0, 1),
                size_hint=(None, None),
                pos=(Window.width // 2 - 100, Window.height // 2 - 25),
            )
            self.add_widget(lose_label)

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


class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(StoryScreen1(name="story1"))
        sm.add_widget(StoryScreen2(name="story2"))
        sm.add_widget(GameScreen(name="game"))

        # ตรวจสอบไฟล์เสียง
        sound_path = "agua_hiperrealista.wav"
        if os.path.exists(sound_path):
            self.bg_music = SoundLoader.load(sound_path)
            if self.bg_music:
                self.bg_music.loop = True  # ตั้งให้เสียงเล่นวนลูป
                self.bg_music.play()  # เล่นเสียง
        else:
            print(f"ไม่พบไฟล์เสียง: {sound_path}")

        return sm

    def on_stop(self):
        # หยุดเสียงเมื่อปิดเกม
        if hasattr(self, "bg_music") and self.bg_music:
            self.bg_music.stop()


if __name__ == "__main__":
    GameApp().run()
