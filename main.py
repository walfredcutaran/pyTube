import certifi
import os

from kivy.properties import StringProperty
from pytube import YouTube
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from pytube.exceptions import PytubeError, VideoUnavailable
from android.storage import primary_external_storage_path

os.environ['SSL_CERT_FILE'] = certifi.where()

class MyGridLayout(GridLayout):
    vid_title = StringProperty('')
    vid_views = StringProperty('')
    vid_owner = StringProperty('')
    vid_length = StringProperty('')

    def __init__(self, **kwargs):
        # call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        self.cols = 1
        self.add_widget(Label(text="pyTube", font_size=60, color=(209/255.0, 73/255.0, 73/255.0)))

        self.subgrid = GridLayout()
        self.subgrid.cols = 2

        self.subgrid.add_widget(Label(text="Youtube Link: ", font_size=20))

        self.name = TextInput(multiline=False, text='')
        self.subgrid.add_widget(self.name)
        self.add_widget(self.subgrid)

        # submit button
        self.submit = Button(text="Submit")
        self.submit.bind(on_press=self.youtube_link)
        self.add_widget(self.submit)

        self.title = Label(text=str(self.vid_title), font_size=20)
        self.add_widget(self.title)

        self.views = Label(text=str(self.vid_views), font_size=20)
        self.add_widget(self.views)

        self.owner = Label(text=str(self.vid_owner), font_size=20)
        self.add_widget(self.owner)

        self.length = Label(text=str(self.vid_length), font_size=20)
        self.add_widget(self.length)

        self.download = Button(text="Download")  # highest quality available only
        self.download.bind(on_press=self.download_button_event)

    def youtube_link(self, instance):

        try:
            name = self.name.text
            video_object = YouTube(name)

        except PytubeError:
            err_popup_pe = Popup(title='Exception: Pytube Error', content=Label(text='Please input a valid Youtube link...'),
                                 auto_dismiss=True,
                                 size_hint=(None, None),
                                 size=(300, 200))
            err_popup_pe.open()

        except VideoUnavailable:
            err_popup_vu = Popup(title='Exception: VideoUnavailable',
                                 content=Label(text='The chosen video is unavailable...'),
                                 auto_dismiss=True,
                                 size_hint=(None, None),
                                 size=(300, 200))
            err_popup_vu.open()

        else:
            title = video_object.title
            views = video_object.views
            owner = video_object.author
            length = video_object.length
            secs = video_object.length
            mins = length / 60
            hours = mins / 60

            # length processing
            final_length = f'{int(hours)} hour(s) {int(mins%60)} minute(s) {int(secs%60)} second(s)'

            self.vid_title = title
            self.vid_views = str(f'{views:,}')  # comma separator
            self.vid_owner = owner
            self.vid_length = str(str(final_length))

            self.title.text = str(f'Title: {self.vid_title}')
            self.views.text = str(f'Views: {self.vid_views}')
            self.owner.text = str(f'Owner: {self.vid_owner}')
            self.length.text = str(f'Length: {self.vid_length}')

            self.add_widget(self.download)

            # clear input box
            self.name.text = ""

    def download_button_event(self, instance):
        print("download button pressed")
        dir = primary_external_storage_path()
        download_dir_path = os.path.join(dir, 'Download')

class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()


# Alpha v0.2