from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import tinytuya
from kivy.uix.screenmanager import Screen
import threading
from kivy.properties import ObjectProperty
from kivy.core.window import Window
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
        
with open('main.kv') as f:
    Builder.load_string(f.read())

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

        self.sm = ScreenManager()
        
        threading.Thread(target = self.init_lights).start()
        
        #loading = LoadingScreen(name = 'loading')
        self.lights = LightScreen(self.dlist, name = 'lighting')
        Window.bind(on_keyboard=self.on_keyboard)
        
        self.screen_list = [self.lights]
        
        #self.sm.add_widget(loading)
        self.sm.add_widget(self.lights)
        
        return self.sm

MainApp().run()
