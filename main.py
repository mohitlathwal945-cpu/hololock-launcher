import os, glob, math, webbrowser
from PIL import Image, ImageChops
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

def calculate_palm_similarity(p1, p2):
    try:
        img1 = Image.open(p1).convert('L').resize((64, 64))
        img2 = Image.open(p2).convert('L').resize((64, 64))
        diff = ImageChops.difference(img1, img2)
        return math.sqrt(sum(v * (i ** 2) for i, v in enumerate(diff.histogram())) / 4096.0)
    except: return None

class HologramPalmLauncher(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#040712')
        self.main_layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        self.title_label = Label(text='::: SYSTEM CORE: BIOMETRIC GATEWAY :::', font_size='14sp', bold=True, size_hint_y=0.15, color=get_color_from_hex('#00E5FF'))
        self.holo_canvas = Label(text='✋\n[ PLACE PALM ABOVE CORE ]', font_size='18sp', bold=True, size_hint_y=0.55, color=get_color_from_hex('#00E5FF'))
        self.scan_button = Button(text='⚡ INITIATE SYSTEM AUTOSCAN ⚡', font_size='16sp', bold=True, size_hint_y=0.3, background_color=get_color_from_hex('#00E5FF'), color=get_color_from_hex('#040712'))
        self.scan_button.bind(on_press=self.start_scan)
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.holo_canvas)
        self.main_layout.add_widget(self.scan_button)
        self.frames = ['- SCANNING: 0° -', '/ SCANNING: 45° /', '| SCANNING: 90° |', '\\\\ SCANNING: 135° \\\\']
        self.idx = 0
        return self.main_layout

    def start_scan(self, instance):
        self.scan_button.disabled = True
        self.anim = Clock.schedule_interval(self.loop_anim, 0.15)
        Clock.schedule_once(self.verify, 2.5)

    def loop_anim(self, dt):
        self.holo_canvas.text = f"✋\n{self.frames[self.idx]}"
        self.idx = (self.idx + 1) % len(self.frames)

    def verify(self, dt):
        Clock.unschedule(self.anim)
        path = '/storage/emulated/0/Download/'
        scans = glob.glob(os.path.join(path, 'current_scan*.*'))
        master = os.path.join(path, 'master_palm.jpg')
        if not os.path.exists(master) or not scans:
            self.holo_canvas.text = '>> ARTIFACTS MISSING <<'
            self.scan_button.disabled = False
            return
        score = calculate_palm_similarity(master, max(scans, key=os.path.getmtime))
        if score is not None and score < 45.0:
            self.holo_canvas.text = '🌟 ACCESS GRANTED 🌟'
            self.main_layout.remove_widget(self.scan_button)
            dock = GridLayout(cols=2, spacing=15, size_hint_y=0.3)
            b1 = Button(text='YOUTUBE', background_color=get_color_from_hex('#D50000'))
            b1.bind(on_press=lambda i: webbrowser.open('https://www.youtube.com'))
            dock.add_widget(b1)
            self.main_layout.add_widget(dock)
        else:
            self.holo_canvas.text = '🚨 ACCESS DENIED 🚨'
            self.scan_button.disabled = False

if __name__ == "__main__":
    HologramPalmLauncher().run()
