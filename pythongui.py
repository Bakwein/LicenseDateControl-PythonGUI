import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit, QLabel, QPushButton, QLineEdit, QGridLayout, QListWidget, QTableWidget, QHeaderView, QTableWidgetItem, QFileDialog
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtGui import QColor
import sqlite3
from datetime import datetime
import pandas as pd
from plyer import notification
'''
BİTTİ1 -1 AYDAN AZ SÜRE VARSA SARI 1 HAFTADAN AZ VARSA KIRMIZI 
BİTTİ2 - isim kontrolü olacak aynıysa önceki düzenlenecek farklıysa dict'e eklenecek ama bu zaten normal dicte ekleme ile de otomatik güncelleniyor olabilir buna bir bak
BİTTİ3 - EXCEL RENKLİ BACKGROUNDA YAZI RENGİ KONTROL

BİTTİ GİBİ - BOYUT OLAYLARINA BAKILACAK

TARİH FORMATLARINA KONTROL LAZİM - DÜZENLE KISMINDA
HATA KISMI DÜZENLENECEK

VERİYİ TUTULACAK HALE GETİRME
(DÜZENLE SİL VERİ TABANI GÜNCELLENECEK)



'''

'''
EXE HALE GETİRME
pip install pyinstaller
pyinstaller --onefile --noconsole your_script_name.py



'''

class DateTimePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 400) #boyut
        self.dct = dict()
        self.colNo = 0
        self.rowNo = 0
        self.initUI()
        

    def initUI(self):
        
        #database
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        #table
        c.execute(''' 
                  CREATE TABLE IF NOT EXISTS tablo_verileri (
                  isim TEXT,
                  start TEXT,
                  end TEXT
                  ) ''')
        
        #tablo doldurma
        c.execute('SELECT * FROM tablo_verileri')
        veriler = c.fetchall()
        # #self.dct[isim_str] = {'name': isim_str, 'start': start_date_str, 'end': ending_date_str}
        for veri in veriler:
            self.dct[veri[0]] = {'name': veri[0], 'start': str(veri[1]), 'end': str(veri[2]) }
        #con.close()
            


        #layout = QVBoxLayout()
        layout = QGridLayout()

        # Labeller
        self.isim = QLabel("İsim", self)
        self.label = QLabel("Başlangıç tarihi:", self)
        self.label2 = QLabel("Bitiş Tarihi:", self)
        #self.listLabel = QLabel("Listeler:", self)

        #label2 yerini değiştirme


        #isim giris
        self.isimTextbox = QLineEdit("")

        # begging_date oluşturma
        self.beggining_date = QDateTimeEdit(self)
        self.beggining_date.setCalendarPopup(True) # açılır pencere
        self.beggining_date.setDateTime(QDateTime.currentDateTime())
        self.beggining_date.setDisplayFormat("dd.MM.yyyy")
        self.beggining_date.setFixedSize(110,40)

        #ending_date
        self.ending_date = QDateTimeEdit(self)
        self.ending_date.setCalendarPopup(True) # açılır pencere
        self.ending_date.setDateTime(QDateTime.currentDateTime())
        self.ending_date.setDisplayFormat("dd.MM.yyyy")
        self.ending_date.setFixedSize(110,40)
    

        #buton

        self.button = QPushButton("Ekle")
        #sinyal olayi 
        self.button.clicked.connect(self.butonBasildi)

        self.listeGoster = QPushButton("Excel dosyası yükle-?")
        #üstüne mi yazsın yoksa tamamen silip yeni veri seti o mu olsun
        self.listeGoster.clicked.connect(self.excelImport)


        self.listeDuzenle = QPushButton("Excel dosyası olarak çıktı al")
        self.listeDuzenle.clicked.connect(self.excelOutput)

        #listeleme
        #self.liste = QListWidget()

        #colNum = 5
        self.colNo = 5
        #rowNum = 34 # bu  sonra len olarak belirlenecek
        self.rowNo = 30
        #tablo
        self.table = QTableWidget()
        self.table.setRowCount(self.rowNo)
        self.table.setColumnCount(self.colNo)
        # isim - bas - bit - sil - düzenle (son 2 buton)
        self.table.setHorizontalHeaderLabels(['İsim', 'Başlangıç Tarihi', 'Bitiş Tarihi', 'Düzenle', 'Sil'])
        

        #header ayari
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for col in range(self.colNo):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        
        



        
        # left  table align
        # BU BELKİ KALDIRILABİLİR???
        '''
        ver_header = self.table.verticalHeader()
        ver_header.setStretchLastSection(True)
        for ver1 in range(self.rowNo):
            ver_header.setSectionResizeMode(ver1, QHeaderView.ResizeMode.Stretch)  
        '''


        #tablo ilk doldurma
        self.tabloElemanlariEkle()

        #self.tabloBoya()


        #alignment
        #self.label2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.ending_date.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Satır yüksekliğini otomatik ayarla

        #self.datetime_edit.dateTimeChanged.connect(self.onDateTimeChanged) # sinyale göre haraket belirler

        # Layout'a widgetları ekleme
        layout.addWidget(self.isim, 0, 0)
        layout.addWidget(self.isimTextbox, 1 , 0,1, 2)
        layout.addWidget(self.label, 2, 0)
        layout.addWidget(self.beggining_date, 3, 0)
        layout.addWidget(self.label2, 2, 1)
        layout.addWidget(self.ending_date, 3, 1)
        layout.addWidget(self.button, 4, 0)
        

        #araya belki bir çizgi??

        #layout.addWidget(self.listLabel, 0,3 )
        layout.addWidget(self.listeGoster, 0,3)
        layout.addWidget(self.listeDuzenle, 0, 4)
        #layout.addWidget(self.liste, 2, 3, 4, 2)
        layout.addWidget(self.table, 1, 3, 4, 2)
        
        


        # Ana pencereye layout'u ekleme
        self.setLayout(layout)

        # Pencereyi ayarlama
        self.setWindowTitle('Date Control')
        self.show()
        
    '''
    def onDateTimeChanged(self, datetime):
        # Seçilen tarih ve saati QLabel'da gösterme
        self.label.setText(f"Selected datetime: {datetime.toString()}")
        '''
    def butonBasildi(self):
        #print("button kontrol")
        #print(self.beggining_date)

        #texti alma
        isim_str = self.isimTextbox.text()
        #print(isim_str)

        #başlangıç tarihini alma
        begging_date = self.beggining_date.dateTime()
        '''
        begging_date_year, begging_date_month, begging_date_day = begging_date.date().year(), begging_date.date().month(), begging_date.date().day()
        print(begging_date_year, begging_date_month, begging_date_day, "*")
        '''
        day_zero1 = f'{begging_date.date().day():02}'
        month_zero1 = f'{begging_date.date().month():02}'
        start_date_str = day_zero1 + '.' + month_zero1 + '.' + str(begging_date.date().year())

        #bitiş tarihini alma
        ending_date = self.ending_date.dateTime()
        #print(ending_date)
        '''
        ending_date_year, ending_date_month, ending_date_day = ending_date.date().year(), ending_date.date().month(), ending_date.date().day()
        print(ending_date_year, ending_date_month, ending_date_day, "***")
        '''
        day_zero = f'{ending_date.date().day():02}'
        month_zero = f'{ending_date.date().month():02}'
        ending_date_str = day_zero + '.'+month_zero + '.' + str(ending_date.date().year())

        self.kontrolluEkle(isim_str=isim_str, start_date_str=start_date_str, ending_date_str=ending_date_str)
        #self.dct[isim_str] = {'name': isim_str, 'start': start_date_str, 'end': ending_date_str}

        #veri tabanı ekleme
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        c.execute('DELETE FROM tablo_verileri')
        for key,value in self.dct.items():
            c.execute('''
            INSERT INTO tablo_verileri (isim, start, end)
            VALUES (?,?,?)
            ''',(key,value['start'], value['end']))
        con.commit()
        con.close()
        


    def excelImport(self):
        #r = random.randint(5,20)
        #self.table.setRowCount(r)
        #print(self.dct)
        pass

    def excelOutput(self):
        #print("excel!")
        df = pd.DataFrame(self.dct).T
        df.columns = ("İsim", "Başlangıç Tarihi", "Bitiş Tarihi")
        if df.size == 0:
            return
        df.fillna('', inplace=True)
        #print(df)
        #options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Excel dosyasını kaydet", "", "Excel Files (*.xlsx);;All Files (*)")
        if filename:
            df.to_excel(filename, index=False)
            workbook = load_workbook(filename)
            sheet = workbook.active
            for y in range(len(self.dct)):
                #def calculateDif(self, get_item_date):
                item_text = self.table.item(y,2).text()
                dif = self.calculateDif(item_text)
                print(dif,"yo")

                if dif.days < 10:
                    print("red")
                    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                    for i in ['A', 'B', 'C']:
                            #print(i + str(y), "boom")
                            sheet[i + str(y+2)].fill = red_fill
                elif dif.days < 30:
                    print("yellow")
                    yellow_fill = PatternFill(start_color="FFFF33", end_color="FFFF33",fill_type="solid")
                    for i in ['A', 'B', 'C']:
                        sheet[i+str(y+2)].fill = yellow_fill

            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter  # Kolon harfini al
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)  # İhtiyaca göre genişliği ayarla
                sheet.column_dimensions[column].width = adjusted_width
                
            workbook.save(filename)
            print("excel dosyası kaydedildi ve renklendirildi.")


        

    def kontrolluEkle(self, isim_str, start_date_str, ending_date_str):
        #kontroller olacak burada

        self.dct[isim_str] = {'name': isim_str, 'start': start_date_str, 'end': ending_date_str}
        self.tabloElemanlariEkle()

    def tabloElemanlariEkle(self):
        #print(self.dct, type(self.dct))
        if len(self.dct) != 0:
            y_ = 0
            self.dictSirala()
            for key,value in self.dct.items():
                self.table.setItem(y_, 0, QTableWidgetItem(key))
                self.table.setItem(y_, 1, QTableWidgetItem(value["start"]))
                self.table.setItem(y_, 2, QTableWidgetItem(value["end"]))

                #düzenle butonu
                but1 = QPushButton("Düzenle")
                but1.clicked.connect(lambda _, r=3, c=y_: self.tabloButtonDuzenle(r,c))
                self.table.setCellWidget(y_, 3, but1)

                #silme butonu
                but2 = QPushButton("Sil")
                but2.clicked.connect(lambda _, r=4, c=y_: self.tabloButtonSil(r,c))
                self.table.setCellWidget(y_, 4, but2)

                y_+=1

            

    
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            self.tabloGunKontrol()
        




    def tabloGuncelle(self):
        pass

    def dictSirala(self):
       self.dct = dict(sorted(self.dct.items()))

    def isValidDate(self, date):
        date_format = "%d.%m.%Y"
        try:
            datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False


    def tabloButtonDuzenle(self, r, c): # c sütun no
        keys_list = list(self.dct.keys())
        old_key = keys_list[c]
        #print(old_key, "OOOO")

        bas_tarih = self.table.item(c,1).text()
        son_tarih = self.table.item(c,2).text()

        if not (self.isValidDate(bas_tarih) and self.isValidDate(son_tarih)):
            print("HATAAAAAAA")
            #Bu kısma çözüm lazim - çözüm dediğim hatayı göstersin
            return 
            

        


        new_key = self.table.item(c,0).text()
        del self.dct[old_key]
        self.dct[new_key] = {'name': new_key, 
                             'start': bas_tarih,
                             'end': son_tarih
                             }
              
        self.tabloTemizleme()
        self.tabloElemanlariEkle()
        


    def tabloButtonSil(self, r, c):
        #print(r,c, "*****")
        name_ = self.table.item(c,0).text()
        #print(name_)
        del self.dct[name_]
        self.tabloTemizleme()
        self.tabloElemanlariEkle()
        #print(r,c)


    def tabloTemizleme(self):
        self.table.clearContents()

    def calculateDif(self, get_item_date):
        date_format = "%d.%m.%Y"
        ret_date = datetime.strptime(get_item_date, date_format)
        date = ret_date.date()
        current_date = datetime.now().date()
        dif = date - current_date
        return dif

    def tabloGunKontrol(self):
        len_ =  len(self.dct)
        isNotificationRequired = False
        for e in range(len_):
            get_item = self.table.item(e, 2)
            get_item_date = get_item.text()
            if not self.isValidDate(get_item_date):
                return
            dif = self.calculateDif(get_item_date=get_item_date)
            if dif.days < 10:
                # 10 günden az - hem boya hem uyarı olayını ayarla
                isNotificationRequired = True
                self.tabloKirmiziBoya(num=e)
            elif dif.days < 30:
                self.tabloSariBoya(num=e)
        if isNotificationRequired:
            #print("noti!")
            notification.notify(
                title = "Uyarı!",
                message = "10 günden az bir tarih bulundu!",
                app_name = "Tarih Kontrol Uygulaması",
                timeout = 5
            )


    def tabloSariBoya(self,num):
        for s in range(3):
            #print(num,s,"sari")
            item = self.table.item(num, s)
            item.setBackground(QColor(255, 255, 51))
            item.setForeground(QColor(0,0,0))

        
    def tabloKirmiziBoya(self,num):
        for s in range(3):
            item = self.table.item(num,s)
            item.setBackground(QColor(255, 0, 51))
            item.setForeground(QColor(0,0,0))

    def tablo_yazdir(self):
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        c.execute('SELECT * FROM tablo_verileri')
        rows = c.fetchall()
        for row in rows:
            print(row)
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DateTimePicker()
    sys.exit(app.exec())
