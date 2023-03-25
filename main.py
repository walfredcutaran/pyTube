import certifi
import os
import socket
import threading
import time

from kivy.clock import Clock, mainthread
from pytube import Stream
from pytube import YouTube
from pytube.exceptions import PytubeError, VideoUnavailable
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

os.environ['SSL_CERT_FILE'] = certifi.where()

kv = '''
#: import MDFadeSlideTransition kivymd.uix.transition.transition.MDFadeSlideTransition
MDScreenManager:
    transition: MDFadeSlideTransition()
    HomeScreen:
    DownloadScreen:
    VideoInfoScreen:
    DownloadProgressScreen:

<HomeScreen>
    canvas:
        Color:
            rgba: .09, .07, .17, 1
        Rectangle:
            size: self.size
            pos: self.pos
    name: 'home'
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDTopAppBar:
                    id: toolbar
                    title: "PyTube"
                    elevation: 3
                    pos_hint: {"top": 1}
                    md_bg_color: "#443C68"
                    left_action_items:
                        [['menu', lambda x: nav_drawer.set_state("open")]]
                        
        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 20, 20, 0)
            spacing: 25
            padding: 26, 25, 25, 16
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    title: "Ferbs"
                    title_color: "#635985"
                    text: "Navigation Drawer"
                    spacing:'10dp'
                    padding: "12dp", 0, 0, "46dp"
                MDNavigationDrawerDivider:
                MDNavigationDrawerItem
                    id: home_nav
                    icon: "home"
                    text: "Home"
                    on_press:
                        root.manager.current = 'home'
                        nav_drawer.set_state("close")
                MDNavigationDrawerItem
                    icon: "camera"
                    text: "Camera"
                    selected_color: "7e37ca"
                    on_press:
                        root.manager.current = 'camera'
                        nav_drawer.set_state("close")
                MDNavigationDrawerItem
                    icon: "format-letter-case"
                    text: "Text Editor"
                    selected_color: "7e37ca"
                    on_press:
                        root.manager.current = 'text_editor'
                        nav_drawer.set_state("close")
                MDNavigationDrawerDivider:
                MDNavigationDrawerItem
                    icon: "information"
                    text: "Instruction"
                    selected_color: "7e37ca"
                    on_press:
                        app.show_info_dialog()
                        nav_drawer.set_state("close")
    MDTextField:
        id: text_code
        mode: "rectangle"
        font_name: "MonoLisa-Medium"
        font_size: 30
        text: app.yt_link
        fill_color_normal: "#393053"
        fill_color_focus: "#635985"
        text_color_normal: "#ffffff"
        text_color_focus: "#ffffff"
        line_color_normal: "#635985"
        line_color_focus: "#ffffff"
        size_hint_x: .80
        size_hint_y: .10
        hint_text: "Youtube link here..."
        hint_text_color_focus: "#ffffff"
        hint_text_color_normal: "#635985"
        multiline: False
        pos_hint: {"center_x": .5, "center_y": .70}                    
                        
                        
    BoxLayout:
        orientation: 'vertical'
        MDBottomAppBar:
            md_bg_color: "#443C68"
            MDTopAppBar:
                icon: 'camera'
                elevation: 0
                mode: 'end'
                type: 'bottom'
                left_action_items: [["information-outline", lambda x: app.test_browser()]]
                icon_color: .39, .35, .52, 1
                on_action_button: root.manager.current = 'camera'
        
        MDFloatLayout:
            MDFillRoundFlatIconButton
                md_bg_color: "#635985"
                font_name: "Poppins Medium 500"
                text: "Download"
                font_size: 60
                pos_hint:{'center_x': 0.5, 'center_y': 0.35}
                size_hint: 0.2, 0.1
                on_release: 
                    app.test_input() # get yt link
                    app.download_screen()                   
                    root.manager.current = 'download_screen'
                
            MDFillRoundFlatIconButton
                md_bg_color: "#635985"
                font_name: "Poppins Medium 500"
                text: "Video Info"
                font_size: 60
                pos_hint:{'center_x': 0.5, 'center_y': 0.2}
                size_hint: 0.2, 0.1
                on_release:
                    app.test_input_2()

<DownloadScreen>
    name: 'download_screen'
    canvas:
        Color:
            rgba: .09, .07, .17, 1
        Rectangle:
            size: self.size
            pos: self.pos
            
    AsyncImage:
        allow_stretch: True
        keep_ratio: True
        pos_hint:{'center_x': 0.5, 'center_y': 0.8}
        size_hint: None, None
        height: 350
        width: 350
        id: image_holder
        source: 'x.png'
            
    MDLabel:
        id: video_title
        adaptive_size: True
        font_name: "Poppins Medium 500"
        pos_hint: {"center_x": .5, "center_y": .5}
        text: "MDLabel"
        color: (1,1,1,1)
        font_size: 20
        size_hint_x: .5
        allow_selection: True
        allow_copy: True
    
    MDLabel:
        id: video_views
        adaptive_size: True
        font_name: "Poppins Medium 500"
        pos_hint: {"center_x": .5, "center_y": .4}
        text: "MDLabel"
        color: (1,1,1,1)
        font_size: 20
        size_hint_x: .5
        padding: "4dp", "4dp"
        allow_selection: True
        allow_copy: True    

    MDLabel:
        id: video_owner
        adaptive_size: True
        font_name: "Poppins Medium 500"
        pos_hint: {"center_x": .5, "center_y": .3}
        text: "MDLabel"
        color: (1,1,1,1)
        font_size: 20
        size_hint_x: .5
        padding: "4dp", "4dp"
        allow_selection: True
        allow_copy: True     

    MDLabel:
        id: video_length
        adaptive_size: True
        font_name: "Poppins Medium 500"
        pos_hint: {"center_x": .5, "center_y": .2}
        text: "MDLabel"
        color: (1,1,1,1)
        font_size: 20
        size_hint_x: .5
        padding: "4dp", "4dp"
        allow_selection: True
        allow_copy: True 
                    
    MDBoxLayout:
        orientation: 'horizontal'
        MDRectangleFlatIconButton
            md_bg_color: "#635985"
            font_name: "Poppins Medium 500"
            text: 'Back'
            text_color: "white"
            line_color: "#393053"
            font_size: 40
            size_hint: 1, .1
            on_release: root.manager.current = 'home'
            
        MDRectangleFlatIconButton
            md_bg_color: "#635985"
            font_name: "Poppins Medium 500"
            text: 'Download'
            text_color: "white"
            line_color: "#393053"
            font_size: 40
            size_hint: 1, .1
            on_release: app.start_download()


<VideoInfoScreen>
    name: 'video_info_screen'
    
<DownloadProgressScreen>
    name: 'download_progress_screen'
    canvas:
        Color:
            rgba: .09, .07, .17, 1
        Rectangle:
            size: self.size
            pos: self.pos
        
    MDLabel:
        id: progress_label
        adaptive_size: True
        font_name: "Poppins Medium 500"
        pos_hint: {"center_x": .5, "center_y": .5}
        text: "MDLabel"
        color: (1,1,1,1)
        font_size: 60
        size_hint_x: .5
        padding: "4dp", "4dp"
        allow_selection: True
        allow_copy: True 
    
        
'''
class HomeScreen(MDScreen):
    pass

class DownloadScreen(MDScreen):
    pass

class VideoInfoScreen(MDScreen):
    pass

class DownloadProgressScreen(MDScreen):
    pass


class PyTube(MDApp):
    # permissions
    # from android.permissions import request_permissions, Permission
    # request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    yt_link = StringProperty("")  # content in text field

    video_title = StringProperty("")  # content in text field
    video_views = StringProperty("")  # content in text field
    video_owner = StringProperty("")  # content in text field
    video_length = StringProperty("")  # content in text field

    video_download_progress = StringProperty("") # download progress

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # kv file init
        self.main_widget = Builder.load_string(kv)


    def download_screen(self):
        try:
            link = self.yt_link
            video_object = YouTube(link)

            title = video_object.title
            views = video_object.views
            owner = video_object.author
            length = video_object.length
            secs = video_object.length
            mins = length / 60
            hours = mins / 60
            image = video_object.thumbnail_url

            # https://www.youtube.com/watch?v=NMThdHhrLoM
            final_length = f'{int(hours)} hour(s) {int(mins % 60)} minute(s) {int(secs % 60)} second(s)'

            self.main_widget.get_screen('download_screen').ids.video_title.text = title
            self.main_widget.get_screen('download_screen').ids.video_views.text = str(views)
            self.main_widget.get_screen('download_screen').ids.video_owner.text = owner
            self.main_widget.get_screen('download_screen').ids.video_length.text = final_length
            self.main_widget.get_screen('download_screen').ids.image_holder.source = image

        except VideoUnavailable as err:
            self.vu_error_dialog = MDDialog(
                title=str(VideoUnavailable),
                text=str(err),
            ).open()

        except PytubeError as err:
            self.pe_error_dialog = MDDialog(
                title=str(PytubeError),
                text=str(err),
            ).open()

    # @mainthread
    def start_download(self):
        try:
            link = self.yt_link
            video_object = YouTube(link)
            print(link)
            for timeout in [1, 5, 10, 15]:
                print("checking internet connection..")
                socket.setdefaulttimeout(timeout)
                host = socket.gethostbyname("www.google.com")
                s = socket.create_connection((host, 80), 2)
                s.close()
                print('internet on.')
            """
                for timeout in [1, 5, 10, 15]:
                print("checking internet connection..")
                socket.setdefaulttimeout(timeout)
                host = socket.gethostbyname(name)
                s = socket.create_connection((host, 80), 2)
                s.close()
                print('internet on.')
            """

        except PytubeError as err:
            self.pe_error_dialog_2 = MDDialog(
                title=str(PytubeError),
                text=str(err),
            ).open()
            self.root.current = 'home'

        else:
            # from android.storage import primary_external_storage_path
            # dir = primary_external_storage_path()
            # download_dir_path = os.path.join(dir, 'Download')

            # test download https://www.youtube.com/watch?v=NMThdHhrLoM

            video = YouTube(link, on_progress_callback=self.on_download_progress_check, on_complete_callback=self.on_complete)
            global file_size

            file_size = video_object.streams.get_highest_resolution().filesize

            video.streams.get_by_itag(22).download(output_path="C:/Users/Walfred Cutaran/Downloads")
            # self.root.current = 'download_progress_screen'

    def on_download_progress_check(stream=None, chunk=None, file_handle=None, remaining=None):
        # Gets the percentage of the file that has been downloaded.
        percent = (100 * (file_size - remaining)) / file_size
        print("{:00.0f}% downloaded".format(percent))

    def on_complete(self, instance, file_path):
        self.download_complete = MDDialog(
            title=str("Attention!"),
            text=str("Download finished... \nfile located at local downloads folder..."),
        ).open()

        self.main_widget.get_screen('download_screen').ids.video_title.text = ""
        self.main_widget.get_screen('download_screen').ids.video_views.text = ""
        self.main_widget.get_screen('download_screen').ids.video_owner.text = ""
        self.main_widget.get_screen('download_screen').ids.video_length.text = ""
        self.main_widget.get_screen('download_screen').ids.image_holder.source = "x.png"
        self.main_widget.get_screen('home').ids.text_code.text = ""
        self.root.current = 'home'
        # get_audio_only

    # def dialog_close(self, *args):
    #    self.error_dialog.dismiss(force=True)

    def text_input(self, widget):
        self.yt_link = widget.text

    def test_input_2(self):
        str_text = self.main_widget.get_screen('home').ids.text_code.text
        video_object = YouTube(str_text)


        print(video_object.streams.get_highest_resolution().filesize, "bytes")
        print(video_object.streams.get_highest_resolution().bitrate)



    def test_input(self):
        str_text = self.main_widget.get_screen('home').ids.text_code.text
        self.yt_link = str_text

        print(str_text)

    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Orange"

        return self.main_widget


if __name__ == '__main__':
    PyTube().run()


'''
implement multi threading
text field -> download -> download screen w/ progress bar -> prompt if download finished -> back buttons
download -> download as mp3 -> prompt yes or no -> or -> download as mp4 -> prompt yes or no
text field -> video info -> video info screen -> back buttons
'''
