import certifi
import os

from kivy.properties import StringProperty
from pytube import YouTube
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.progressbar import ProgressBar
from pytube.exceptions import PytubeError, VideoUnavailable

os.environ['SSL_CERT_FILE'] = certifi.where()


class MyGridLayout(GridLayout):
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    vid_title = StringProperty('')
    vid_views = StringProperty('')
    vid_owner = StringProperty('')
    vid_length = StringProperty('')

    # vid_thumbnail = StringProperty('https://www.canva.com/design/DAFEfjiUSho/view')

    def __init__(self, **kwargs):
        # call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)
        self.padding = '10dp'
        self.spacing = '10dp'

        self.cols = 1

        self.subgrid = GridLayout()
        self.subgrid.cols = 2

        self.subgrid.add_widget(Label(text="Youtube Link: ", font_size='20dp'))

        self.name = TextInput(multiline=False, text='')
        self.subgrid.add_widget(self.name)
        self.add_widget(self.subgrid)

        # submit button
        self.submit = Button(text="Submit", font_size='25dp')
        self.submit.bind(on_press=self.youtube_link)
        self.add_widget(self.submit)

        self.title = Label(text=str(self.vid_title), font_size='15dp')
        self.add_widget(self.title)

        self.views = Label(text=str(self.vid_views), font_size='15dp')
        self.add_widget(self.views)

        self.owner = Label(text=str(self.vid_owner), font_size='15dp')
        self.add_widget(self.owner)

        self.length = Label(text=str(self.vid_length), font_size='15dp')
        self.add_widget(self.length)

        self.download = Button(text="Download", font_size='25dp')  # highest quality available only
        self.download.bind(on_press=self.download_button_event)
        self.add_widget(self.download)

    def youtube_link(self, instance):

        try:
            # name = yt link
            name = self.name.text
            video_object = YouTube(name)

        except PytubeError:
            err_popup_pe = Popup(title='Exception: Pytube Error',
                                 content=Label(text='Please input a valid Youtube link...'),
                                 auto_dismiss=True,
                                 size_hint=(None, None),
                                 size=('300dp', '100dp'))
            err_popup_pe.open()

        except VideoUnavailable:
            err_popup_vu = Popup(title='Exception: VideoUnavailable',
                                 content=Label(text='The chosen video is unavailable...'),
                                 auto_dismiss=True,
                                 size_hint=(None, None),
                                 size=('300dp', '100dp'))
            err_popup_vu.open()

        else:
            instruction = Popup(title='Important Instruction',
                                content=Label(text='Once you press download\nplease wait for the next popup...'),
                                auto_dismiss=True,
                                size_hint=(None, None),
                                size=('300dp', '150dp'))
            instruction.open()

            title = video_object.title
            views = video_object.views
            owner = video_object.author
            length = video_object.length
            secs = video_object.length
            mins = length / 60
            hours = mins / 60

            # length processing
            final_length = f'{int(hours)} hour(s) {int(mins % 60)} minute(s) {int(secs % 60)} second(s)'

            self.vid_title = title
            self.vid_views = str(f'{views:,}')  # comma separator
            self.vid_owner = owner
            self.vid_length = str(str(final_length))

            self.title.text = str(f'Title: {self.vid_title}')
            self.views.text = str(f'Views: {self.vid_views}')
            self.owner.text = str(f'Owner: {self.vid_owner}')
            self.length.text = str(f'Length: {self.vid_length}')

    def download_button_event(self, instance):

        try:
            name = self.name.text
            video_object = YouTube(name)

        except PytubeError:
            instruction = Popup(title='Exception: Missing Input',
                                content=Label(text='Please input a valid youtube link\nbefore downloading...'),
                                auto_dismiss=True,
                                size_hint=(None, None),
                                size=('300dp', '150dp'))
            instruction.open()

        else:
            from android.storage import primary_external_storage_path
            dir = primary_external_storage_path()
            download_dir_path = os.path.join(dir, 'Download')

            link = self.name.text
            video_object = YouTube(link, on_complete_callback=self.on_complete)
            video_object.streams.get_highest_resolution().download(output_path=download_dir_path)

    def on_complete(self, instance, file_path):
        download_complete = Popup(title='Download Complete',
                                  content=Label(text='The file is on your\nlocal downloads folder...'),
                                  auto_dismiss=True,
                                  size_hint=(None, None),
                                  size=('300dp', '200dp'))
        download_complete.open()

        self.name.text = ""
        self.title.text = ""
        self.views.text = ""
        self.owner.text = ""
        self.length.text = ""


class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
