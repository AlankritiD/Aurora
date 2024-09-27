from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime

from app import get_time_of_day

ragas = {
    "Raga Yaman": {
        "time": "Evening",
        "link": "https://www.youtube.com/watch?v=ed4SIvGjqNI"
    },
    "Raga Bhimpalasi": {
        "time": "Afternoon",
        "link": "https://www.youtube.com/watch?v=uEqYzdz3Zvg"
    },
    "Raga Desh": {
        "time": "Night",
        "link": "https://www.youtube.com/watch?v=Ix-BoQQDYkw"
    },
    "Raga Todi": {
        "time": "Morning",
        "link": "https://www.youtube.com/watch?v=ybSdS6x5A-w" 
    },
    "Raga Bageshree": {
        "time": "Night",
        "link": "https://www.youtube.com/watch?v=rUoWx__itDo"
    }
}
# Recommend a raga based on the time of day
def recommend_raga():
    time_of_day = get_time_of_day()
    recommended_ragas = [raga for raga, info in ragas.items() if info["time"] == time_of_day]

    if recommended_ragas:
        return recommended_ragas
    else:
        return None



# Set window size (for testing purposes on desktop)
Window.size = (360, 640)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Layout for the login page
        layout = FloatLayout()
        background = Image(source='new mobile.jpeg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
        
        # Title Label (Aurora)
        self.title_label = Label(text="AURORA",
                                 font_size=40,
                                 color=(1, 0.835, 0.502, 1),  # RGB equivalent of #FFD580
                                 size_hint=(.4, .2),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout.add_widget(self.title_label)

        # Username input
        self.username_input = TextInput(hint_text="USERNAME",
                                        multiline=False,
                                        background_color=(1, 0.835, 0.502, 1),  # RGB equivalent of #FFD580
                                        size_hint=(.6, .1),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.username_input)

        # Password input
        self.password_input = TextInput(hint_text="PASSWORD",
                                        multiline=False,
                                        password=True,
                                        background_color=(1, 0.835, 0.502, 1),  # RGB equivalent of #FFD580
                                        size_hint=(.6, .1),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.45})
        layout.add_widget(self.password_input)

        # Login button
        self.login_button = Button(text="LOGIN",
                                   font_size=24,
                                   color=(1, 0.835, 0.502, 1),  # RGB equivalent of #FFD580
                                   size_hint=(.3, .1),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.login_button.bind(on_press=self.validate_login)
        layout.add_widget(self.login_button)

        # Set the layout as the screen's content
        self.add_widget(layout)

    # Login Validation
    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username == "user" and password == "password":
            self.manager.current = 'raga_screen'
        else:
            popup = Popup(title='Login Failed', content=Label(text='Invalid username or password'),
                          size_hint=(0.8, 0.2))
            popup.open()

class RagaScreen(Screen):
    def __init__(self, **kwargs):
        super(RagaScreen, self).__init__(**kwargs)

        # Layout for the Raga screen
        layout = FloatLayout()
        
        # Add background image (optional)
        background = Image(source='new app.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
        
        # Label for showing current time
        self.time_label = Label(text='', font_size='20sp', color=(1, 1, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.8})
        layout.add_widget(self.time_label)

        # Label for showing recommended raga
        self.raga_label = Label(text='', font_size='21sp', color=(1, 1, 1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.raga_label)

        # Add a placeholder for the recommended raga display
        self.raga_container = FloatLayout(size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.raga_container)

        # Button to refresh recommended raga
        refresh_button = Button(text='Refresh Raga', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3},  # Adjusted pos_hint
                                background_color=(0, 0, 0, 0), color=(1, 1, 1, 1))
        refresh_button.bind(on_press=self.refresh_raga)
        layout.add_widget(refresh_button)

        # Add layout to the screen **once**
        self.add_widget(layout)

        # Schedule time updates every second and refresh raga based on time
        Clock.schedule_interval(self.update_time, 1)
        self.refresh_raga()  # Refresh the raga initially

        # Recommended ragas displayed here
        recommended_ragas = recommend_raga()
        if recommended_ragas:
            for raga in recommended_ragas:
                # Display the raga name
                raga_display_label = Label(text=f"Recommended Raga: {raga}",
                                           font_size=24,
                                           size_hint=(.8, .2),
                                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
                self.raga_container.add_widget(raga_display_label)

                # **Create the button to redirect to YouTube**
                link_button = Button(text="Click here to listen",
                                     font_size=20,
                                     size_hint=(0.8, 0.1),  # **Adjusted size to cover background**
                                     pos_hint={'center_x': 0.6, 'center_y': 0.4})  # **Shifted down**
                link_button.bind(on_press=lambda instance, r=raga: self.open_youtube(r))
                self.raga_container.add_widget(link_button)
        else:
            no_raga_label = Label(text="No raga available for this time.",
                                  font_size=24,
                                  size_hint=(.8, .2),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
            self.raga_container.add_widget(no_raga_label)


    # Method to open YouTube link in a web browser
    def open_youtube(self, raga_name):
        import webbrowser
        # Fetch the YouTube link for the given raga
        raga_link = ragas[raga_name]["link"]
        webbrowser.open(raga_link)


    # Function to get the current time
    def update_time(self, *args):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.text = f"Current Time: {current_time}"

    # Function to get the time of the day and recommend a raga
    def get_time_of_day(self):
        now = datetime.now()
        current_hour = now.hour
        if 5 <= current_hour < 12:
            return "Morning"
        elif 12 <= current_hour < 17:
            return "Afternoon"
        elif 17 <= current_hour < 21:
            return "Evening"
        else:
            return "Night"

    # Refresh raga based on time of day
    def refresh_raga(self, *args):
        time_of_day = self.get_time_of_day()  # Corrected line
        recommended_ragas = [raga for raga, info in ragas.items() if info["time"] == time_of_day]
        '''if recommended_ragas:
            self.raga_label.text = f"Recommended Raga for {time_of_day}:\n{', '.join(recommended_ragas)}"
        else:
            self.raga_label.text = "No raga available for this time." '''
# Main App
class RagaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(RagaScreen(name='raga_screen'))
        return sm

if __name__ == '__main__':
    RagaApp().run()