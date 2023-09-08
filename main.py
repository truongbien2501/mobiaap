from ftplib import FTP
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from io import BytesIO
# kivy.require('2.0.0')
class FTPApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.text_box = TextInput(multiline=True)
        layout.add_widget(self.text_box)
        
        # Tạo một text để hiển thị nội dung
        # self.my_text = Label(text='')
        button_layout = BoxLayout(orientation='horizontal')
        # Tạo một button
        button1 = Button(text='Thu điện!')
        button1.bind(on_press=self.nhandien_button_click)  # Khi button được nhấn, gọi hàm on_button_click
        
        # Tạo một button
        button2 = Button(text='Chuyển điện')
        button2.bind(on_press=self.send_button_click)  # Khi button được nhấn, gọi hàm on_button_click
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)

        # Thêm button và text vào layout
        # layout.add_widget(self.my_text)
        layout.add_widget(button_layout)

        return layout
    def ftp_sever(self,tram):
        # Thông tin máy chủ FTP và đường dẫn đến file
        ftp_host = '113.160.225.111'
        ftp_user = 'kttvttbdb'
        ftp_password = '618778'
        file_path = 'Dulieu-Bantinkttvttb/5-Quang Ngai/PHAN MEM/DIENBAO'

        # Kết nối đến máy chủ FTP
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        ftp.cwd(file_path)
   
        contents = None

        try:
            with BytesIO() as file:
                ftp.retrbinary('RETR ' + tram, file.write)
                contents = file.getvalue().decode('utf-8')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
                
        ftp.quit()
        return contents
    def write_ftp_sever(self,tram,noidung):
        # Thông tin máy chủ FTP và đường dẫn đến file
        ftp_host = '113.160.225.111'
        ftp_user = 'kttvttbdb'
        ftp_password = '618778'
        file_path = 'datattb'

        # Kết nối đến máy chủ FTP
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        ftp.cwd(file_path)
        # file = open(r'C:\Users\Administrator\Desktop\tap huan FES\chep so.xls','rb')
        ftp.storbinary('STOR ' + tram, noidung)
        # file.close()                                   
        ftp.quit()

    def nhandien_button_click(self, instance):
        ac= self.ftp_sever('DATA54292.TXT')
        sg = self.ftp_sever('DATA53992.TXT')
        contents = sg[:sg.index('=')+1] + '\n' + ac[ac.index('71542'):ac.index('=')+1]
        self.text_box.text = contents
        # self.my_text.text = contents   # Thay đổi nội dung của text khi button được nhấn

        
    def send_button_click(self, instance):
        
        noidung = self.text_box.text.encode('utf-8')  # Chuyển chuỗi thành dữ liệu bytes
        noidung_file = BytesIO(noidung)
        
        self.write_ftp_sever('DATA592.txt',noidung_file)
            # Tạo một thông báo
            # Tạo một thông báo
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Dữ liệu đã được chuyển đi!'))
        
        # Thêm nút tắt thông báo
        dismiss_button = Button(text='Đóng')
        content.add_widget(dismiss_button)
        
        # Tạo popup với nội dung và nút tắt thông báo
        popup = Popup(title='Thông báo', content=content, size_hint=(None, None), size=(400, 200))
        
        # Thiết lập hàm callback khi nút tắt được nhấn
        dismiss_button.bind(on_release=popup.dismiss)
        
        # Hiển thị thông báo
        popup.open()
        
if __name__ == '__main__':
    FTPApp().run()
