from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import tinytuya
import threading

class LoadingScreen(Screen):
    pass

class LightScreen(Screen):    
    def __init__(self, dl, **kwargs):
        self.dlist = dl
            
        self.toggle_ct = True
        self.color_dict = {}
        super(LightScreen, self).__init__(**kwargs)
    
    def toggle_white(self):
        for item in self.dlist.values():
            device = tinytuya.BulbDevice(item['gwId'], item['ip'], item['key'])
            device.set_version(3.3)
            
            if self.toggle_ct:
                self.color_dict[item['gwId']] = device.colour_rgb()
                device.set_colour(255,255,255)
            else:
                device.set_colour(*self.color_dict[item['gwId']])
        
        self.toggle_ct = not self.toggle_ct

class MainApp(MDApp):
    MAPPER = {
        "Living Room 1": "Smart LED Light Bulb 5",
        "Living Room 2": "Smart LED Light Bulb 6",
        "Laundry Hall 1": "Smart LED Light Bulb 3",
        "Laundry Hall 2": "Smart LED Light Bulb 4",
    }
    
    dlist = ObjectProperty({})
    
    def init_lights(self):
        dlist = tinytuya.deviceScan(False, 20)
        pop_list = []
        for k, v in dlist.items():
            if not v.get('key'):
                pop_list.append(k)
                
        for key in pop_list:
            dlist.pop(key)
            
        self.sm.switch_to(self.screen_list[-1])
        self.dlist.update(dlist)
        
        return dlist
    
    def callback_off(self, instance):
        for item in self.dlist.values():
            bulbs_names = ["Tenergy Smart LED Light Bulb 5", "Tenergy Smart LED Light Bulb 6"]        
            if item['name'] in bulbs_names:
                device = tinytuya.BulbDevice(item['gwId'], item['ip'], item['key'])
                device.set_version(3.3)
                device.turn_off()
                
    
    def callback_on(self, instance):
        for item in self.dlist.values():
            bulbs_names = ["Tenergy Smart LED Light Bulb 5", "Tenergy Smart LED Light Bulb 6"]
            if item['name'] in bulbs_names:
                device = tinytuya.BulbDevice(item['gwId'], item['ip'], item['key'])
                device.set_version(3.3)
                device.turn_on()

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if modifier == ['alt'] and codepoint == 'c':
            self.lights.toggle_white()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        #self.sm = ScreenManager()
        
        threading.Thread(target = self.init_lights).start()
        
        #loading = LoadingScreen(name = 'loading')
        #self.lights = LightScreen(self.dlist, name = 'lighting')
        #Window.bind(on_keyboard=self.on_keyboard)
        
        #self.screen_list = [self.lights]
        
        #self.sm.add_widget(loading)
        #self.sm.add_widget(self.lights)

        grid_layout = MDGridLayout(cols=1, padding=100)

        btn_1 = MDRectangleFlatButton(
            text="Toggle white light mode? (On/Off)",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        label_1 = MDLabel(
            text="Which room?",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            halign="center",
        )

        btn_2 = MDRectangleFlatButton(
            text="Living Room",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        btn_3 = MDRectangleFlatButton(
            text="Front Door",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        btn_4 = MDRectangleFlatButton(
            text="Foyer",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        btn_5 = MDRectangleFlatButton(
            text="Kitchen",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        btn_6 = MDRectangleFlatButton(
            text="Bedroom",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        btn_7 = MDRectangleFlatButton(
            text="Laundry Hall",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(1, 1)
        )

        grid_layout.add_widget(btn_1)
        grid_layout.add_widget(label_1)
        grid_layout.add_widget(btn_2)
        grid_layout.add_widget(btn_3)
        grid_layout.add_widget(btn_4)
        grid_layout.add_widget(btn_5)
        grid_layout.add_widget(btn_6)
        grid_layout.add_widget(btn_7)
        
        return MDScreen(grid_layout)

MainApp().run()
