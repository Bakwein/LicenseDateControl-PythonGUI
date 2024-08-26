import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit, QLabel, QPushButton, QLineEdit, QGridLayout, QListWidget, QTableWidget, QHeaderView, QTableWidgetItem, QFileDialog, QDateTimeEdit
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from PyQt6.QtCore import QDateTime, Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
from datetime import datetime
import pandas as pd
from plyer import notification
import os
import shutil
'''

24.08

BİTTİ1 -1 AYDAN AZ SÜRE VARSA SARI 1 HAFTADAN AZ VARSA KIRMIZI 

BİTTİ2 - isim kontrolü olacak aynıysa önceki düzenlenecek farklıysa dict'e eklenecek ama bu zaten normal dicte ekleme ile de otomatik güncelleniyor olabilir buna bir bak

BİTTİ3 - EXCEL RENKLİ BACKGROUNDA YAZI RENGİ KONTROL

25.08

BİTTİ4- VERİYİ TUTULACAK HALE GETİRME (DÜZENLE SİL VERİ TABANI GÜNCELLENECEK)

BİTTİ5- 30 SINIRINA EKSTRA DURUMLAR EKLENECEK -> y_ olayından çözülebilir -> oldu ama kontrol lazim

BİTTİ6-SEARCH GETİRİLECEK

BİTTİ7- FİLTRELEME OLAYLARI GETİRİLEBİLİR - İSİME GÖRE, BİTİŞ TARİHİNE GÖRE BUTON

BİTTİ8- SİLDİKTEN, DÜZENLEDİKTEN SONRA, ARA YAPTIKTAN BİLDİRİM GİTMESİN

BİTTİ9-FİLTERLARDAN SONRA EXCEL TABLOSU NASIL ELDE EDİLİYOR KONTROL LAZİM

26.08

BİTTİ10- DÜZENLE KISMINDA HATA KISMI DÜZENLENECEK

BİTTİ11-DÜZENLE YAPILANCA VERİLER ARA KISMINA GELECEK

BİTTİ 12 - FİLTRELEDİKTEN SONRA TABLO BOYUTU KISMINA BAK?

BİTTİ 13 - SIRALA BUTONLARI AKTİFLİK GÖSTERİLEBİLİR

BİTTİ 14 GİBİ- EXCEL DOSYASI YÜKLE GETİRİLECEK

BİTTİ 15 GİBİ - DB DOSYASI YÜKLE

--------------

--------------

?tabloElemanlariEkle return değerleri kontrolleri lazim

?HATA KISIMLARINA KONTROL LAZİM - ekstra hata kontrolleri ile sistem daha tutarlı hale getirilebilir

?HATA OLMADIĞINDA HATA MESAJLARINI SIFIRLA - update gerekebilir

?oldu mu?TABLO UZUNLUK OLAYINDA HALA HATA VAR !!!!!!
--------------

?TARİH FORMATLARINA KONTROL LAZİM  - 
kontrol func.
#kontroller olacak burada - sorun varsa false olsun

SİLME VE DÜZENLEME DURUMLARI İÇİN YEDEK DB ARADA ALİNABİLİR. - gunlük tutulacak

FİLTERDE SİLİNCE,düzenlenince FİLTEDEYKEN İŞLEM YAPILINCA TÜM ELEMANLARI GÖSTERİYOR 

DÜZENLE YAPILINCA VERİ EN ALTA GİDİYOR BUTON AKTİFLİĞİNE GÖRE SIRALA DÜZENLEYİNCE SONA EKLEME

'''

'''
EXE HALE GETİRME - EXE OLAYI BOZUK
pip install pyinstaller
pyinstaller --onefile --noconsole pythongui.py

pyinstaller --onefile --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets pythongui.py


pyinstaller --onefile --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets --hidden-import plyer.platforms.win.notification  --noconsole pythongui.py

pyinstaller --onefile --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets --hidden-import=plyer.platforms.win.notification --hidden-import=plyer.platforms.macosx.notification --noconsole pythongui.py


'''

'''
Sorunlar/Sorular /Soylenecekler:

SORUNLAR
-excel ekleme nedenim tablonun güzel gözükmemeseydi. Uzun bir giriş olduğunda problem oluyor ve ayar yapamiyorum otomatik doldurma fonksiyonu nedenini anlamadığım şekilde düzgün çalışmıyor


SORULAR
-10 gün <= mi < mi?


SOYLENECEKLER

-FİLTERDE SİLİNCE,düzenlenince FİLTEDEYKEN İŞLEM YAPILINCA TÜM ELEMANLARI GÖSTERİYOR 

-aynı filtreleme alt kısımda da olsun mu?

'''

class DateTimePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 400) #boyut
        self.dct = dict()
        self.colNo = 0
        self.rowNo = 0
        self.isDatePressed = True
        self.isEditModeOn = True
        self.editDict = {}
        self.initUI()
        
    def initUI(self):
        #klasörler
        current_dir = os.getcwd()
        db_klasor = '/db_yedekleme'
        
        if not os.path.exists(current_dir + db_klasor):
            os.makedirs(current_dir + db_klasor)

        excel_klasor = '/excel_dosyalari'
        if not os.path.exists(current_dir + excel_klasor):
            os.makedirs(current_dir + excel_klasor)
        


        



        #database
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        #table
        #3 ' olacak
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
        #colNum = 5
        self.colNo = 5
        #rowNum = 34 # bu  sonra len olarak belirlenecek
        self.rowNo = len(veriler)

        #layout = QVBoxLayout()
        layout = QGridLayout()

        # Labeller
        self.isim = QLabel("İsim", self)
        self.label = QLabel("Başlangıç tarihi:", self)
        self.label2 = QLabel("Bitiş Tarihi:", self)
        #self.listLabel = QLabel("Listeler:", self)

        #label2 yerini değiştirme

        self.uyari = QLabel("""*Database veya Excel Verisi Yüklediğinizde Eski Database "db_yedekleme" Klasöründe Yedeklenir""", self)
        self.uyari.setStyleSheet("color: lightblue;")

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

        self.listeGoster = QPushButton("*Excel Dosyası Yükle")
        #üstüne mi yazsın yoksa tamamen silip yeni veri seti o mu olsun
        self.listeGoster.clicked.connect(self.excelImport)

        self.dbEkle = QPushButton("*Yeni Database Yükle")
        self.dbEkle.clicked.connect(self.newDatabase)

        self.listeDuzenle = QPushButton("Tabloyu Excel Olarak Çıktı Al")
        self.listeDuzenle.clicked.connect(self.excelTabloOutput)


        self.listeAll = QPushButton("Tüm Verileri Excel Olarak Çıktı Al")
        self.listeAll.clicked.connect(self.excelOutput)

        #listeleme
        #self.liste = QListWidget()
        
        #tablo
        self.table = QTableWidget()
        self.table.setRowCount(self.rowNo)
        self.table.setColumnCount(self.colNo)
        # isim - bas - bit - sil - düzenle (son 2 buton)
        self.table.setHorizontalHeaderLabels(['İsim', 'Başlangıç Tarihi', 'Bitiş Tarihi', 'Düzenle', 'Sil'])

        #header ayari
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
        for col in range(self.colNo):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        
        #self.button.clicked.connect(self.butonBasildi)
        
        #Search elemenleri
        self.searchLabel = QLabel("İsim Ara", self)
        self.searchTextbox = QLineEdit("")
        self.searchButton = QPushButton("Tabloda Ara")
        self.searchButton.clicked.connect(self.aramaBasildi)
        self.searchButton2 = QPushButton("Tümünde Ara")
        self.searchButton2.clicked.connect(self.aramaBasildi2)
        
        self.resetButton1 = QPushButton("Aramayı Temizle")
        self.resetButton1.clicked.connect(self.aramaTemizlemeBasildi)

        #Filtreleme 
        self.filterLabel = QLabel("Filtreleme/Sıralama")
        self.dateSort = QPushButton("Kalan Güne Göre Sırala")
        self.dateSort.clicked.connect(self.dateSortFunc)
        self.nameSort = QPushButton("İsme Göre Sırala")
        self.nameSort.clicked.connect(self.NameSortFunc)

        #bunlara da date sort lazim
        self.onlylast10 = QPushButton("Son 10 Gün") 
        self.onlylast10.clicked.connect(self.son10Goruntule)
        self.between10to30 = QPushButton("Son 1 Ay")
        self.between10to30.clicked.connect(self.between1030Basildi)
        self.normal = QPushButton("1 Aydan Fazla")
        self.normal.clicked.connect(self.normalBasildi)
        self.all = QPushButton("Tümünü Görüntüle")
        self.all.clicked.connect(self.aramaTemizlemeBasildi)

        #Hata yazma label'ı
        self.hataLabel = QLabel("", self)
        self.hataLabel.setStyleSheet("color: red;")

        #self.hataLabel.setText("Hata: Geçersiz giriş!")

        #düzenleme modu
        self.editMode = QPushButton("Düzenleme Modunu Aç/Kapa")
        self.editMode.clicked.connect(self.editModeBasildi)

        
        # left  table align
        # BU BELKİ KALDIRILABİLİR???
        '''
        ver_header = self.table.verticalHeader()
        ver_header.setStretchLastSection(True)
        for ver1 in range(self.rowNo):
            ver_header.setSectionResizeMode(ver1, QHeaderView.ResizeMode.Stretch)  
        '''

        #tablo ilk doldurma
        self.tabloElemanlariEkle(True)
        self.dateSortFunc()
        self.editModeBasildi()

        #self.tabloBoya()

        #alignment
        #self.label2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.ending_date.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Satır yüksekliğini otomatik ayarla

        #self.datetime_edit.dateTimeChanged.connect(self.onDateTimeChanged) # sinyale göre haraket belirler
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Layout'a widgetları ekleme
        layout.addWidget(self.isim, 0, 0)
        layout.addWidget(self.isimTextbox, 1 , 0,1, 2)
        layout.addWidget(self.label, 2, 0)
        layout.addWidget(self.beggining_date, 3, 0)
        layout.addWidget(self.label2, 2, 1)
        layout.addWidget(self.ending_date, 3, 1)
        layout.addWidget(self.button, 4, 0, 1,1)
        
        #araya belki bir çizgi??

        #layout.addWidget(self.listLabel, 0,3 )
        layout.addWidget(self.dbEkle, 0,3)
        layout.addWidget(self.listeGoster, 0,4)
        layout.addWidget(self.listeDuzenle, 0, 5)
        layout.addWidget(self.listeAll, 0 ,6)
        #layout.addWidget(self.liste, 2, 3, 4, 2)
        layout.addWidget(self.table, 2, 3, 5, 5 )
        layout.addWidget(self.uyari, 1,3, 1,3)
        #arama yerlestirme
        layout.addWidget(self.searchLabel, 5, 0)
        layout.addWidget(self.searchTextbox, 6, 0,1,2)
        layout.addWidget(self.searchButton, 7,0)
        layout.addWidget(self.searchButton2, 8,0)
        layout.addWidget(self.resetButton1, 7,1)

        layout.addWidget(self.filterLabel, 7, 3)
        layout.addWidget(self.dateSort, 8, 3)
        layout.addWidget(self.nameSort, 8, 4)
        layout.addWidget(self.onlylast10, 9, 3)
        layout.addWidget(self.between10to30, 9, 4)
        layout.addWidget(self.normal, 9, 5)
        layout.addWidget(self.all, 9,6)
        layout.addWidget(self.hataLabel,7,5,1,2)
        layout.addWidget(self.editMode,1,6)

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
        noti = False
        temp_isDatePressed = self.isDatePressed

        #texti alma
        isim_str = self.isimTextbox.text()
        if isim_str == "":
            self.hataLabel.setText("Hata: İsim boş olamaz!")
            return

        table_size = self.table.rowCount()
        #print(table_size, "*")

        #boyle bir isim var mi
        xd = self.tabloVerileriEldeEt()
        xd_keys = xd.keys()
        if isim_str not in xd_keys:
            if (table_size + 1 > self.rowNo):
                self.rowNo += 1
                self.table.setRowCount(self.rowNo)

        #başlangıç tarihini alma
        begging_date = self.beggining_date.dateTime()
        #print(type(begging_date), "!**!",)

        day_zero1 = f'{begging_date.date().day():02}'
        month_zero1 = f'{begging_date.date().month():02}'
        start_date_str = day_zero1 + '.' + month_zero1 + '.' + str(begging_date.date().year())

        #bitiş tarihini alma
        ending_date = self.ending_date.dateTime()
        #print(ending_date)

        day_zero = f'{ending_date.date().day():02}'
        month_zero = f'{ending_date.date().month():02}'
        ending_date_str = day_zero + '.'+month_zero + '.' + str(ending_date.date().year())

        dif_ = self.calculateDif(ending_date_str)
        #print(dif_.year, "?????")
        if(dif_.days <= 10):
            noti = True
        
        ret = self.kontrolluEkle(isim_str=isim_str, start_date_str=start_date_str, ending_date_str=ending_date_str, noti=noti)

        self.isDatePressed = temp_isDatePressed
        #self.dct[isim_str] = {'name': isim_str, 'start': start_date_str, 'end': ending_date_str}
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()

        if not ret:
            self.hataLabel.setText("Hata: Lütfen verileri doğru formatta giriniz!")
            return 
        
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        c.execute('DELETE FROM tablo_verileri')
        for key,value in self.dct.items():
            #3 ' unutma
            c.execute('''
            INSERT INTO tablo_verileri (isim, start, end)
            VALUES (?,?,?)
            ''',(key,value['start'], value['end']))
        con.commit()
        con.close()
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def excelImport(self):
        #r = random.randint(5,20)
        #self.table.setRowCount(r)
        #print(self.dct)
        #pass
        opt = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyasını Seç", "","Excel Files (*.xlsx);;All Files (*)", options=opt)
        if file_path:
            df = pd.read_excel(file_path, engine="openpyxl")
            #print(df, "*****!****")
            #self.tabloTemizleme()
            #print(df.columns)
            df.columns = ['name', 'start', 'end']
            all_elem = df.to_dict('records')
            new_dct = {}
            for elem in all_elem: 
                #print(elem, " O.o")
                #print(elem['name'], elem["start"], elem["end"], sep="--")
                new_dct[elem['name']] = {'name': elem['name'], 'start': elem['start'], 'end': elem['end']}
            #print("\n\n")
            #print(new_dct, " !!!!!!!")
            self.dct = new_dct
            #print(self.dct, " :O")
            #self.tabloBoyutInput(len(self.dct))
            #self.tablo_guncelle(self.dct)
            #print("&&", len(self.dct), "&&")
            self.tabloBoyutInput(len(self.dct))
            #self.tabloTemizleme()
            self.tablo_guncelle(new_dct=self.dct, noti=True)
            
            #self.editModeBasildi()
            
            now = datetime.now()
            date_time_str = now.strftime('%Y%m%d_%H%M%S')
            full_path = os.path.join(os.getcwd()+ f'/db_yedekleme/EXCEL_BACKUP_tablo_verileri_backup_{date_time_str}.db')
            shutil.copy('./tablo_verileri.db',full_path)

            con = sqlite3.connect('tablo_verileri.db')
            c = con.cursor()
            #şimdiki tablo_verileri'ni sakla!!!!!
           
            #name = f'tablo_verileri_{date_time_str}'


            c.execute('DELETE FROM tablo_verileri')
            for key,value in self.dct.items():
                #3 ' unutma
                c.execute('''
                INSERT INTO tablo_verileri (isim, start, end)
                VALUES (?,?,?)
                ''',(key,value['start'], value['end']))
            con.commit()
            con.close()

        self.duzenle_kapali()
        self.hataLabel.setText("")
        self.dateSort.setStyleSheet("")
        self.nameSort.setStyleSheet("")


    def getTableLength(self):
        l = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row,0)
            if item is not None and item.text().strip():
                l+=1
        return l

    def tabloVerileriEldeEt(self):
        ret_dct = {}
        #print(self.table.rowCount(),"*",self.getTableLength())
        
        for row in range(self.getTableLength()):
            name_item = self.table.item(row, 0)
            start_date_item = self.table.item(row, 1)
            end_date_item = self.table.item(row, 2)
            #print(name_item, start_date_item, end_date_item, "*")
            if name_item == None or start_date_item == None or end_date_item == None:
                break
            name = name_item.text()
            start_date = start_date_item.text()
            end_date = end_date_item.text()
            
            #print(name, start_date, end_date, "yoo!")
            ret_dct[name] = {'name': name, 'start': start_date, 'end': end_date}
        return ret_dct
    
    def excelOutput(self):
        ret_dict = self.dct 
        if not self.isDatePressed:
            ret_dict = dict(sorted(ret_dict.items()))
        else:
            ret_dict = dict(sorted(ret_dict.items(), key=lambda item: self.calculateDif(item[1]['end'])))
        df = pd.DataFrame(ret_dict).T
        df.columns = ("İsim", "Başlangıç Tarihi", "Bitiş Tarihi")
        if df.size == 0:
            self.hataLabel.setText("Hata: Yazılacak Bilgi Yok!")
            return
        df.fillna('', inplace=True)
        filename, _ = QFileDialog.getSaveFileName(self, "Excel dosyasını kaydet", "", "Excel Files (*.xlsx);;All Files (*)")
        if filename:
            df.to_excel(filename, index=False)
            workbook = load_workbook(filename)
            sheet = workbook.active
            keys = list(ret_dict.keys())

            for y in range(len(ret_dict)):
                #item_text = self.table.item(y,2).text()
                item_text = self.dct[keys[y]]['end']
                #print(item_text, " boom!")
                dif = self.calculateDif(item_text)
                if dif.days <= 10:
                    #print("red")
                    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                    for i in ['A', 'B', 'C']:
                        #print(i + str(y), "boom")
                        sheet[i + str(y+2)].fill = red_fill
                elif dif.days < 30:
                    #print("yellow")
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
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def excelTabloOutput(self):
        #print("excel!")
        tablo_dct = self.tabloVerileriEldeEt()
        if len(tablo_dct) == 0:
            self.hataLabel.setText("Hata: Tabloda veri yok!")
            return
        df = pd.DataFrame(tablo_dct).T
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
            for y in range(len(tablo_dct)):
                #def calculateDif(self, get_item_date):
                item_text = self.table.item(y,2).text()
                dif = self.calculateDif(item_text)
                #print(dif,"yo")

                if dif.days <= 10:
                    #print("red")
                    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
                    for i in ['A', 'B', 'C']:
                            #print(i + str(y), "boom")
                            sheet[i + str(y+2)].fill = red_fill
                elif dif.days < 30:
                    #print("yellow")
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
            #print("excel dosyası kaydedildi ve renklendirildi.")
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def kontrolluEkle(self, isim_str, start_date_str, ending_date_str, noti):
        ret = True
        #kontroller olacak burada - sorun varsa false olsun

        self.dct[isim_str] = {'name': isim_str, 'start': start_date_str, 'end': ending_date_str}
        ret2 = self.tabloElemanlariEkle(noti)
        if not ret2:
            ret = False
        return ret

    def  tabloElemanlariEkle(self, noti):
        #print(self.dct, type(self.dct))
        self.aramaTemizlemeBasildi()
        if len(self.dct) != 0:
            y_ = 0
            self.NameSortFunc()
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
                if (y_ > self.rowNo):
                    self.rowNo = y_
                    self.table.setColumnCount(self.rowNo)
                    
            
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            ret = self.tabloGunKontrol(self.dct, noti)
            if not ret :
                return False
            return True

    def toDate(str):
        return datetime.strptime(str, '%d.%m.%Y')
    
    def changeColorSort(self, isDate):
        if isDate:
            self.dateSort.setStyleSheet("background-color: lightgreen; color:black; border-style: outset; border-width:2px; border-radius:5px; border-color: beige;")
            self.nameSort.setStyleSheet("")
            self.isDatePressed = True
        else:
            self.dateSort.setStyleSheet("")
            self.nameSort.setStyleSheet("background-color: lightgreen; color:black; border-style: outset; border-width:2px; border-radius:5px; border-color: beige; ")
            self.isDatePressed = False




    def dateSortFunc(self):
        self.changeColorSort(True)
        #DCT DEĞİL TABLOYU ALSIN
        new_dct = self.tabloVerileriEldeEt()

        new_dct = dict(sorted(new_dct.items(), key=lambda item: self.calculateDif(item[1]['end'])))
        self.tabloTemizleme()
        self.tablo_guncelle(new_dct)
        self.duzenle_kapali()
        self.hataLabel.setText("")
        #print("AAAAAAA")
    #self.toDate(item[2])

    def NameSortFunc(self):
       self.changeColorSort(False)
       new_dct = self.tabloVerileriEldeEt()
       new_dct= dict(sorted(new_dct.items()))
       self.tabloTemizleme()
       self.tablo_guncelle(new_dct)
       self.duzenle_kapali()
       self.hataLabel.setText("")

    def isValidDate(self, date):
        date_format = "%d.%m.%Y"
        try:
            datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False


    def tabloButtonDuzenle(self, r, c): # c sütun no
        #temp_dict = self.tabloVerileriEldeEt()
        #keys_list = list(self.tabloVerileriEldeEt().keys())
        keys_list = list(self.editDict.keys())
        print(keys_list, r , c)
        old_key = keys_list[c]
        print(old_key, "OOOO")

        name = self.table.item(c,0).text()
        print("name:", name)
        bas_tarih = self.table.item(c,1).text()
        son_tarih = self.table.item(c,2).text()

        if not (self.isValidDate(bas_tarih) and self.isValidDate(son_tarih) and len(name) != 0):
            #print(self.isValidDate(bas_tarih), self.isValidDate(son_tarih),len(name), "**" )
            #print("HATAAAAAAA")
            #Bu kısma çözüm lazim - çözüm dediğim hatayı göstersin
            if len(name) == 0:
                self.hataLabel.setText("Hata: İsim boş olamaz!")
            elif not self.isValidDate(bas_tarih):
                self.hataLabel.setText("Hata: Başlangıç Tarihi Formatı Yanlış!")
            else:
                self.hataLabel.setText("Hata: Bitiş Tarihi Formatı Yanlış!")
            return 

        new_key = self.table.item(c,0).text()
        del self.dct[old_key]
        #del temp_dict[old_key]
        print("old key", old_key, "new_key", new_key, "****")
        self.dct[new_key] = {'name': new_key, 
                             'start': bas_tarih,
                             'end': son_tarih
                             }
        '''
        temp_dict[new_key] = {'name': new_key, 
                             'start': bas_tarih,
                             'end': son_tarih
                             }
            '''
        #self.tabloTemizleme()
        ret = self.tabloElemanlariEkle(False)
        #ret = self.tablo_guncelle(temp_dict)
        if not ret:
            self.hataLabel.setText("Hata: Lütfen verileri doğru formatta giriniz!")
            return 
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        #veri tabanından veriyi güncelleme

        #Ara kısmını güncelle
        self.isimTextbox.setText(new_key)
        
        datime_obj1 = QDateTime.fromString(bas_tarih,"dd.MM.yyyy")
        self.beggining_date.setDateTime(datime_obj1)

        datetime_obj2 = QDateTime.fromString(son_tarih,"dd.MM.yyyy")
        self.ending_date.setDateTime(datetime_obj2)



        self.editDict = self.tabloVerileriEldeEt()
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        c.execute('''UPDATE tablo_verileri
                       SET isim = ?, start = ?, end = ?
                       WHERE isim = ?
        ''',(new_key,bas_tarih,son_tarih,old_key ))
        con.commit()
        con.close()
        self.duzenle_acik()

        #self.database_yazdir()
        
       
    def tabloButtonSil(self, r, c):
        #print(r,c, "*****")
        name_ = self.table.item(c,0).text()
        #print(name_)
        del self.dct[name_]
        self.tabloTemizleme()
        ret = self.tabloElemanlariEkle(False)
        #print(r,c)
        if not ret:
            self.hataLabel.setText("Hata: Tablo oluştururken hata meydana geldi!")
            return 
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()
        c.execute(''' DELETE FROM tablo_verileri
                      WHERE isim = ?
                  ''',(name_,))
        con.commit()
        con.close()

        #self.rowNo-=1
        #self.table.setRowCount(self.rowNo)
        print(self.rowNo, self.colNo, "AOAOAO")


    def tabloTemizleme(self):
        self.table.clearContents()

    def calculateDif(self, get_item_date):
        date_format = "%d.%m.%Y"
        ret_date = datetime.strptime(get_item_date, date_format)
        date = ret_date.date()
        current_date = datetime.now().date()
        dif = date - current_date
        return dif

    def tabloGunKontrol(self, dct, noti):
        print(self.table.rowCount(), "rowww")
        len_ =  len(dct)
        print(len_, " lllllleeeeennn")
        isNotificationRequired = False
        for e in range(len_):
            print(e)
            get_item = self.table.item(e, 2)
            get_item_date = get_item.text()
            if not self.isValidDate(get_item_date):
                return False
            dif = self.calculateDif(get_item_date=get_item_date)
            if dif.days <= 10:
                # 10 günden az - hem boya hem uyarı olayını ayarla
                isNotificationRequired = True
                self.tabloKirmiziBoya(num=e)
            elif dif.days < 30:
                self.tabloSariBoya(num=e)
        if isNotificationRequired and noti:
            #print("noti!")
            notification.notify(
                title = "Uyarı!",
                message = "10 günden az bir tarih bulundu!",
                app_name = "Tarih Kontrol Uygulaması",
                timeout = 5
            )
        return True


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

    def tablo_guncelle(self, new_dct,noti=False):
        #if len(new_dct) == 0:
        #    return
        y_ = 0
        
        self.tabloTemizleme()
        self.rowNo = len(new_dct)
        self.table.setRowCount(self.rowNo)
        print("**********************************")
        for key,value in new_dct.items():
            print(key,value, "!!!!!!!!!!!")
            self.table.setItem(y_, 0, QTableWidgetItem(key))
            self.table.setItem(y_, 1, QTableWidgetItem(value["start"]))
            self.table.setItem(y_, 2, QTableWidgetItem(value["end"]))
            #düzenle
            but1 = QPushButton("Düzenle")
            but1.clicked.connect(lambda _, r=3, c=y_: self.tabloButtonDuzenle(r,c))
            self.table.setCellWidget(y_, 3, but1)
            #sil butonu
            but2 = QPushButton("Sil")
            but2.clicked.connect(lambda _, r=4, c=y_: self.tabloButtonSil(r,c))
            self.table.setCellWidget(y_, 4, but2)
            y_+=1

                
            
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        ret = self.tabloGunKontrol(new_dct, noti)
        return ret
        
        
    def database_yazdir(self):
        con = sqlite3.connect('tablo_verileri.db')
        c = con.cursor()

        c.execute("SELECT * FROM tablo_verileri")
        rows= c.fetchall()
        print("****")
        for row in rows:
            print(row)
        print("****")
        con.close()

    def aramaBasildi(self):
        arama_text = self.searchTextbox.text()
        #print(arama_text, "hmhmhm")
        if arama_text == "":
            self.hataLabel.setText("Hata: Arama boş olamaz!")
            return
        #print("niye giriyor??????")
        tablo_dict = self.tabloVerileriEldeEt()
        if not len(tablo_dict):
            self.hataLabel.setText("Hata: Tablo boşken arama yapılamaz!")
            return
        self.tabloTemizleme()
        new_dict = {}
        for key, value in tablo_dict.items():
            if arama_text in key:
                new_dict[key]=value 
        self.tabloBoyutInput(len(new_dict))
        self.tablo_guncelle(new_dct=new_dict)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        #self.tabloBoyutGuncelle()
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def aramaBasildi2(self):
        arama_text = self.searchTextbox.text()
        #print(arama_text, "hmhmhm")
        if arama_text == "":
            self.hataLabel.setText("Hata: Arama boş olamaz!")
            return
        #print("niye giriyor??????")
        tablo_dict = self.dct
        if not len(tablo_dict):
            self.hataLabel.setText("Hata: Veri olmadan arama yapılamaz!")
            return
        self.tabloTemizleme()
        new_dict = {}
        for key, value in tablo_dict.items():
            if arama_text in key:
                new_dict[key]=value
        self.tabloBoyutInput(len(new_dict))
        self.tablo_guncelle(new_dct=new_dict)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        self.duzenle_kapali()
        self.hataLabel.setText("")


    def aramaTemizlemeBasildi(self):
        self.tabloBoyutReset()
        self.tabloTemizleme()
        self.tablo_guncelle(self.dct)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        self.duzenle_kapali()
        self.hataLabel.setText("")


    def son10Goruntule(self):
        ret_dict = {}
        tablo_dict = self.dct
        for key,value in tablo_dict.items():
            ending_date = value['end']
            dif = self.calculateDif(ending_date)
            #print(dif.days)
            if dif.days <= 10:
                #print("AAAAA")
                ret_dict[key]=value
        self.tabloBoyutInput(len(ret_dict))
        self.tablo_guncelle(ret_dict)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        self.duzenle_kapali()
        self.hataLabel.setText("")
        
    
    def between1030Basildi(self):
        ret_dict = {}
        tablo_dict = self.dct
        for key,value in tablo_dict.items():
            ending_date = value['end']
            dif = self.calculateDif(ending_date)
            #print(dif.days)
            if dif.days > 10 and dif.days <= 30:
                #print("AAAAA")
                ret_dict[key]=value
        self.tabloBoyutInput(len(ret_dict))
        self.tablo_guncelle(ret_dict)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def normalBasildi(self):
        ret_dict = {}
        tablo_dict = self.dct
        for key,value in tablo_dict.items():
            ending_date = value['end']
            dif = self.calculateDif(ending_date)
            #print(dif.days)
            if dif.days > 30:
                ret_dict[key]=value
        self.tabloBoyutInput(len(ret_dict))
        self.tablo_guncelle(ret_dict)
        if self.isDatePressed:
            self.dateSortFunc()
        else:
            self.NameSortFunc()
        self.duzenle_kapali()
        self.hataLabel.setText("")

    def newDatabase(self):
        #BURAYA KONTROL GEREKECEK
        opt = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Veritabanı dosyasını seç", "", "Database Files (*.db);;All Files (*)", options=opt)
        if file_path:

            con = sqlite3.connect(file_path)
            df = pd.read_sql_query("SELECT * FROM tablo_verileri", con)
            con.close()
            self.tabloTemizleme()
            df.columns = ['name', 'start', 'end']
            all_elem = df.to_dict('records')
            new_dct = {}
            for elem in all_elem:
                new_dct[elem['name']] = {'name': elem['name'], 'start': elem['start'], 'end': elem['end']}
            self.dct = new_dct
            self.tabloBoyutInput(len(self.dct))
            
            self.tablo_guncelle(new_dct=self.dct, noti=True)

            now = datetime.now()
            date_time_str = now.strftime('%Y%m%d_%H%M%S')
            full_path = os.path.join(os.getcwd()+ f'/db_yedekleme/DB_BACKUP_tablo_verileri_backup_{date_time_str}.db')
            shutil.copy('./tablo_verileri.db',full_path)

            con = sqlite3.connect("tablo_verileri.db")
            c = con.cursor()

            c.execute('DELETE FROM tablo_verileri')
            for key,value in self.dct.items():
                c.execute('''
                INSERT INTO tablo_verileri (isim, start, end)
                VALUES (?,?,?)
                ''',(key,value['start'], value['end']))
            con.commit()
            con.close()
    
        self.duzenle_kapali()
        self.hataLabel.setText("")
        self.dateSort.setStyleSheet("")
        self.nameSort.setStyleSheet("")


    def tabloBoyutGuncelle(self):
        boyut = self.getTableLength()
        self.table.setRowCount(boyut)
        #self.table.setColumnCount(self.rowNo)


    def tabloBoyutReset(self):
        boyut = len(self.dct)
        self.table.setRowCount(boyut)

    def tabloBoyutInput(self, boyut):
        self.table.setRowCount(boyut)
        for row in range(boyut):
            for col in range(self.table.columnCount()):
                print(row, col)
                if not self.table.item(row,col):
                    self.table.setItem(row,col,QTableWidgetItem(""))

    def duzenle_acik(self):
        for row in range(self.table.rowCount()):
            but = self.table.cellWidget(row,3)
            if but:
                but.setEnabled(True)

    def duzenle_kapali(self):
        for row in range(self.table.rowCount()):
            but = self.table.cellWidget(row,3)
            if but:
                but.setEnabled(False)

    def button_mode(self, bool):
        self.button.setEnabled(bool)
        self.searchButton.setEnabled(bool)
        self.searchButton2.setEnabled(bool)
        self.resetButton1.setEnabled(bool)
        self.dbEkle.setEnabled(bool)
        self.listeGoster.setEnabled(bool)
        self.listeDuzenle.setEnabled(bool)
        self.listeAll.setEnabled(bool)
        self.dateSort.setEnabled(bool)
        self.nameSort.setEnabled(bool)
        self.onlylast10.setEnabled(bool)
        self.between10to30.setEnabled(bool)
        self.normal.setEnabled(bool)
        self.all.setEnabled(bool)
        for row in range(self.table.rowCount()):
            but = self.table.cellWidget(row,3)
            if but:
                but.setEnabled(not bool)

    def editModeBasildi(self):
        if self.isEditModeOn:
            self.isEditModeOn = False
            self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.button_mode(True)
            self.editMode.setStyleSheet("")

            
        else:
            self.isEditModeOn = True
            self.editMode.setStyleSheet("background-color: lightgreen; color:black; border-style: outset; border-width:2px; border-radius:5px; border-color: beige;")
            self.table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
            self.button_mode(False)
            self.editDict = self.tabloVerileriEldeEt()
            


    

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = DateTimePicker()
        sys.exit(app.exec())
    except Exception as ex:
        print(ex, "exception detected.")
