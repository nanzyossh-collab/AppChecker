from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import mainthread
import re, os

KV = """
<RootWidget>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    BoxLayout:
        size_hint_y: None
        height: dp(48)
        Label:
            text: "Moonton Safe Checker (Format Validator)"
            bold: True
    BoxLayout:
        size_hint_y: None
        height: dp(40)
        Button:
            text: "Load combo.txt"
            on_release: root.load_file()
        Button:
            text: "Load proxy.txt (optional)"
            on_release: root.load_proxy()
    BoxLayout:
        size_hint_y: None
        height: dp(40)
        Button:
            text: "Validate"
            on_release: root.validate()
        Button:
            text: "Save results"
            on_release: root.save_results()
    Label:
        text: root.status_text
        size_hint_y: None
        height: dp(30)
    ScrollView:
        GridLayout:
            id: results_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            row_default_height: dp(24)
            row_force_default: True
"""

class RootWidget(BoxLayout):
    status_text = StringProperty("No file loaded")
    combo_lines = ListProperty([])
    proxy_lines = ListProperty([])
    valid = ListProperty([])
    invalid = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def load_file(self):
        # For Android we rely on the file being placed in app's working dir /sdcard/Download
        path = os.path.join(os.getenv('EXTERNAL_STORAGE', '/sdcard'), 'Download', 'combo.txt')
        if not os.path.exists(path):
            self.status_text = f"combo.txt not found in {path}"
            return
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        self.combo_lines = lines
        self.status_text = f"Loaded {len(lines)} lines from combo.txt"

    def load_proxy(self):
        path = os.path.join(os.getenv('EXTERNAL_STORAGE', '/sdcard'), 'Download', 'proxy.txt')
        if not os.path.exists(path):
            self.status_text = f"proxy.txt not found in Download"
            return
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        self.proxy_lines = lines
        self.status_text = f"Loaded {len(lines)} proxies"

    @mainthread
    def validate(self):
        self.valid = []
        self.invalid = []
        email_pass_re = re.compile(r'^[^:@\s]+@[^:@\s]+\.[^:@\s]+:[^\s:]+$')
        for ln in self.combo_lines:
            if email_pass_re.match(ln):
                self.valid.append(ln)
            else:
                self.invalid.append(ln)
        self.status_text = f"Valid: {len(self.valid)}  Invalid: {len(self.invalid)}"
        grid = self.ids.results_grid
        grid.clear_widgets()
        for v in self.valid[:200]:
            from kivy.uix.label import Label
            grid.add_widget(Label(text=f"[V] {v}", markup=True))
        for i in self.invalid[:200]:
            from kivy.uix.label import Label
            grid.add_widget(Label(text=f"[X] {i}", markup=True))

    def save_results(self):
        out_dir = os.path.join(os.getenv('EXTERNAL_STORAGE', '/sdcard'), 'Download')
        valid_path = os.path.join(out_dir, 'valid_format.txt')
        invalid_path = os.path.join(out_dir, 'invalid_format.txt')
        with open(valid_path, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(self.valid))
        with open(invalid_path, 'w', encoding='utf-8') as f:
            f.write('\\n'.join(self.invalid))
        self.status_text = f"Saved {len(self.valid)} valid / {len(self.invalid)} invalid to Download"

class MoontonSafeApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MoontonSafeApp().run()
