from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import os
import arabic_reshaper
from bidi.algorithm import get_display

# دالة إصلاح العربية
def fix_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# تسجيل الخطوط
LabelBase.register(name="CopticFont", fn_regular="FreeSerif.ttf")
LabelBase.register(name="ArabicFont", fn_regular="Amiri-Regular.ttf")

# حجم النافذة (اختياري للكمبيوتر فقط)
Window.size = (900, 600)

# جميع الحروف القبطية
copti_letters = [
    "Ⲁ", "Ⲃ", "Ⲅ", "Ⲇ", "Ⲉ", "Ⲋ", "Ⲍ", "Ⲏ", "Ⲑ", "Ⲓ", "Ⲕ", "Ⲗ", "Ⲙ", "Ⲛ",
    "Ⲝ", "Ⲟ", "Ⲡ", "Ⲣ", "Ⲥ", "Ⲧ", "Ⲩ", "Ⲫ", "Ⲭ", "Ⲯ", "Ⲱ", "Ϣ", "Ϥ", "Ϧ", "Ϩ", "Ϫ", "Ϭ", "Ϯ"
]

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        grid = GridLayout(cols=6, spacing=10, padding=20)
        for letter in copti_letters:
            btn = Button(
                text=f"{letter}\n{letter.lower()}",
                font_size=36,
                font_name="CopticFont",
                background_color=(0.2, 0.5, 0.8, 1),
                color=(1, 1, 1, 1)
            )
            btn.letter = letter
            btn.bind(on_release=self.open_letter)
            btn.bind(on_touch_down=self.hover_sound)
            grid.add_widget(btn)
        self.add_widget(grid)

    def hover_sound(self, instance, touch):
        if instance.collide_point(*touch.pos):
            sound_path = os.path.join("audio", f"{instance.letter}_sound.mp3")
            if os.path.exists(sound_path):
                sound = SoundLoader.load(sound_path)
                if sound:
                    sound.play()

    def open_letter(self, instance):
        App.get_running_app().current_index = copti_letters.index(instance.letter)
        App.get_running_app().sm.current = "letter"
        App.get_running_app().sm.get_screen("letter").set_letter(instance.letter)

class LetterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=2, padding=20)

        self.image = Image(size_hint_y=0.6)
        self.sound_btn = Button(
            text=fix_arabic(" تشغيل الشرح الصوتي"),
            size_hint_y=None,
            height=50,
            font_size=20,
            font_name="ArabicFont"
        )
        self.sound_btn.bind(on_release=self.play_rule_audio)

        self.nav_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.prev_btn = Button(text=fix_arabic("️ السابق"), font_name="ArabicFont")
        self.home_btn = Button(text=fix_arabic(" القائمة الرئيسية"), font_name="ArabicFont")
        self.next_btn = Button(text=fix_arabic("️ التالي"), font_name="ArabicFont")

        self.prev_btn.bind(on_release=self.go_prev)
        self.next_btn.bind(on_release=self.go_next)
        self.home_btn.bind(on_release=self.go_home)

        self.nav_layout.add_widget(self.prev_btn)
        self.nav_layout.add_widget(self.home_btn)
        self.nav_layout.add_widget(self.next_btn)

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.sound_btn)
        self.layout.add_widget(self.nav_layout)
        self.add_widget(self.layout)

    def set_letter(self, letter):
        self.letter = letter
        image_path = os.path.join("images", f"{letter}.jpg")
        if os.path.exists(image_path):
            self.image.source = image_path
        else:
            self.image.source = ""

    def play_rule_audio(self, *_):
        audio_path = os.path.join("audio", f"{self.letter}_rule.wav")
        if os.path.exists(audio_path):
            sound = SoundLoader.load(audio_path)
            if sound:
                sound.play()

    def go_prev(self, *_):
        app = App.get_running_app()
        if app.current_index > 0:
            app.current_index -= 1
            self.set_letter(copti_letters[app.current_index])

    def go_next(self, *_):
        app = App.get_running_app()
        if app.current_index < len(copti_letters) - 1:
            app.current_index += 1
            self.set_letter(copti_letters[app.current_index])

    def go_home(self, *_):
        App.get_running_app().sm.current = "main"

class CopticApp(App):
    def build(self):
        self.current_index = 0
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(LetterScreen(name="letter"))
        return self.sm

if __name__ == "__main__":
    CopticApp().run()
