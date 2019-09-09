from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUiType

ui,_ = loadUiType('kutuphane.ui')

login,_ = loadUiType('login.ui')

import psycopg2

from datetime import datetime
from datetime import timedelta

from xlrd import *
from xlsxwriter import *    

import time
from pyzbar.pyzbar import decode
import cv2
import numpy as np

import sys 

class Login(QWidget,login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Giris_Ekrani)
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    def Giris_Ekrani(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""SELECT * FROM yöneticiler""")
        data = self.cursor.fetchall()
        for row in data:
            if username == row[0] and password == row[1]:
                self.label_2.setText("Başarılı Giriş")
                self.window2 = MainApp()
                self.close()
                self.window2.show()
                
            else:
                self.label_2.setText("Hatalı Giriş")    
    
                
        

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.Dark_Orange_Theme()
        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()
        self.Show_All_Lend_Operations()

        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()
        self.Show_Book_Combobox()

        self.Show_All_Books()

    def Handel_UI_Changes(self):   
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)
    def Handel_Buttons(self):
        self.pushButton_31.clicked.connect(self.Barkod_Oku)
        self.pushButton_12.clicked.connect(self.Excel_Lend)
        self.pushButton_30.clicked.connect(self.Excel_All_Book)
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_25.clicked.connect(self.Hiding_Themes)

        self.pushButton.clicked.connect(self.Open_Lend_Operations)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_8.clicked.connect(self.Add_New_Book)
        self.pushButton_13.clicked.connect(self.Search_Books)
        self.pushButton_9.clicked.connect(self.Edit_Books)
        self.pushButton_14.clicked.connect(self.Delete_Books)
        self.pushButton_32.clicked.connect(self.Show_All_Books)

        self.pushButton_20.clicked.connect(self.Add_Category)
        self.pushButton_19.clicked.connect(self.Add_Author)
        self.pushButton_18.clicked.connect(self.Add_Publisher)
        self.pushButton_27.clicked.connect(self.Delete_Category)
        self.pushButton_29.clicked.connect(self.Delete_Author)
        self.pushButton_28.clicked.connect(self.Delete_Publisher)
        
        self.pushButton_15.clicked.connect(self.Add_New_User)
        self.pushButton_16.clicked.connect(self.Login)
        self.pushButton_17.clicked.connect(self.Edit_User)
        self.pushButton_26.clicked.connect(self.Delete_User)

        self.pushButton_23.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_21.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_22.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_24.clicked.connect(self.QDark_Theme)
        
        self.pushButton_11.clicked.connect(self.Show_All_Lend_Operations)
        self.pushButton_6.clicked.connect(self.Add_Lend_Operation)
        self.pushButton_7.clicked.connect(self.Lend_Remove)
        self.tableWidget.cellClicked.connect(self.ogrenci_bilgileri_goster)

        self.tableWidget_4.cellClicked.connect(self.Category_Selected)
        self.tableWidget_3.cellClicked.connect(self.Author_Selected)
        self.tableWidget_2.cellClicked.connect(self.Publisher_Selected)
    def Kontrol(self):
        satir_sayisi = self.tableWidget.rowCount()
        bugun = datetime.now()
        bugun= datetime.strftime(bugun,"%x")

        
        for i in range(satir_sayisi-1):
            teslim_tarihi = self.tableWidget.item(i,7)
            teslim_tarihi = teslim_tarihi.text()
            id = self.tableWidget.item(i,0)
            
            print(id.text())
            if bugun > teslim_tarihi:
                self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
                self.cursor = self.connection.cursor()
                self.tableWidget.setItem(i,3,QTableWidgetItem("Gecikti"))
                self.cursor.execute("""UPDATE  islemler SET kitap_durum = 'Gecikti' WHERE id =%s""",[(int(id.text()))])
                self.connection.commit()
                self.connection.close()
              

            elif bugun == teslim_tarihi:
                self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
                self.cursor = self.connection.cursor()
                self.tableWidget.setItem(i,3,QTableWidgetItem("teslim günü"))
                self.cursor.execute("""UPDATE  islemler SET kitap_durum = 'teslim günü' WHERE id=%s""",[(int(id.text()))])
                self.connection.commit()
                self.connection.close()
              
              
            else:
                self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
                self.cursor = self.connection.cursor()
                self.tableWidget.setItem(i,3,QTableWidgetItem("Süresi Var"))
                self.cursor.execute("""UPDATE  islemler SET kitap_durum = 'Bekleniyor' WHERE id=%s""",[(int(id.text()))])
                self.connection.commit()
                self.connection.close()
            
        
            self.connection.close()     
    def Barkod_Oku(self):
        def barcodeReader(image, bgr):
            
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            barcodes = decode(gray_img)

            for decodedObject in barcodes:

                points = decodedObject.polygon
    
                pts = np.array(points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        
            for bc in barcodes:
                cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        bgr, 2)
                if bc.data.decode("utf-8") is not None:
                    return bc.data.decode("utf-8")
     
        bgr = (8, 70, 208)
        cap = cv2.VideoCapture(0)

        while (True):

            ret, frame = cap.read()
            barcode = barcodeReader(frame, bgr)
            print(type(barcode)) 
            cv2.imshow('Barcode reader', frame)
            if barcode is not None:
                self.lineEdit_4.setText(barcode)
                break
            code = cv2.waitKey(10)
            if code == ord('q') :
                break  
                
    def ogrenci_bilgileri_goster(self,row,column):

        item = self.tableWidget.item(row,5)
        item1 = self.tableWidget.item(row,0)
        item2 = self.tableWidget.item(row,1)

        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        sql = """SELECT concat(ogrenci_adi,' ',ogrenci_soyadi) AS isim,
                    ogrenci_email,
                    ogrenci_tel,
                    ogrenci_tc
                FROM
                    ogrenciler
                WHERE ogrenci_tc=%s"""
        self.cursor.execute(sql,[(item.text())])
        data = self.cursor.fetchone()
        self.label_39.setText(item2.text())
        self.label_41.setText(item1.text())
        self.label_7.setText(data[0])
        self.label_23.setText(data[1])
        self.label_24.setText(data[2])
        self.label_28.setText(data[3])
        self.connection.commit()
        self.connection.close()
        
    def Show_Themes(self):
        self.groupBox_4.show()
    def Hiding_Themes(self):
        self.groupBox_4.hide()

    ####################################
    ######### opening tabs #############

    def Open_Lend_Operations(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    ########################################
    ######### Day Operations ###############

    def Add_Lend_Operation(self):
        try:
            ogrenci_tc = self.lineEdit_2.text()
            ogrenci_kitap = self.comboBox_3.currentText()
            gun = self.comboBox_2.currentText()
            bugun = datetime.now()
            bugun_text = datetime.strftime(bugun,'%x')
            fark = timedelta(days=int(gun))
            teslim_tarihi = bugun + fark
            teslim_tarihi_text = datetime.strftime(teslim_tarihi,'%x')
            durum = "Bekleniyor"
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""SELECT * FROM kitaplar WHERE kitap_adi = %s""",[(ogrenci_kitap)])
            isbn = self.cursor.fetchone()
            print(isbn)
            self.connection.close()
            adet = int(isbn[6])
            print(adet)
            if adet>0:
                self.connection = psycopg2.connect(user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                port = "5432",
                                                database = "postgres")
                self.cursor = self.connection.cursor()
                sql = """INSERT INTO islemler(ogrenci_tc,kitap_isbn,kitap_durum,alindi_tarihi,teslim_tarihi) VALUES(%s,%s,%s,%s,%s)"""
                self.cursor.execute(sql,(ogrenci_tc,isbn[0],durum,bugun_text,teslim_tarihi_text))
                self.connection.commit()
                self.connection.close()
                self.connection = psycopg2.connect(user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                port = "5432",
                                                database = "postgres")
                self.cursor = self.connection.cursor()
                sql  = """UPDATE kitaplar SET kitap_adet = kitap_adet - 1 WHERE isbn = %s"""
                self.cursor.execute(sql,[(isbn[0])])
                self.connection.commit()
                self.connection.close()
                self.Show_All_Lend_Operations()
                self.lineEdit_2.setText("")
                QMessageBox.about(self,"Bilgilendirme","Kitap öğrenciye teslim edildi.")
                self.Show_All_Books()
            else:
                self.lineEdit_2.setText("")
                QMessageBox.warning(self,"Uyarı","{} adlı kitaptan kalmamıştır.".format(isbn[1]))
                
        except psycopg2.errors.ForeignKeyViolation:
            QMessageBox.warning(self,"Uyarı","{} kimlik nolu öğrenci sistemde bulunmamaktadır.".format(ogrenci_tc))
    def Show_All_Lend_Operations(self):
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        sql="""SELECT
                    id,
                    kitap_isbn,
                    kitap_adi,
                    kitap_durum,
                    concat(ogrenci_adi,' ',ogrenci_soyadi) AS isim,
                    ogrenciler.ogrenci_tc,
                    alindi_tarihi,
                    teslim_tarihi
                FROM islemler
                    INNER JOIN kitaplar
                ON islemler.kitap_isbn = kitaplar.isbn
                    INNER JOIN  ogrenciler
                ON ogrenciler.ogrenci_tc = islemler.ogrenci_tc"""

        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        
        for row,form in enumerate(data):
            for column,item in enumerate(form):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.label_29.setText("Toplam {} kayıt".format(row_position))
        self.connection.close()
        self.Kontrol()

    def Lend_Remove(self):

        o_id = int(self.label_41.text())
        o_kitap =str(self.label_39.text()) 
        self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""DELETE FROM islemler WHERE id=%s""",[o_id])
        self.connection.commit()
        self.connection.close()
        self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""UPDATE kitaplar SET kitap_adet = kitap_adet + 1 WHERE isbn=%s""",[(o_kitap)])
        self.connection.commit()
        self.connection.close()
        self.Show_All_Lend_Operations()
        self.label_41.setText("")
        self.label_39.setText("")
        self.Show_All_Books()
    ###############################
    ######### Books ###############
    
    def Show_All_Books(self):
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        sql = """SELECT isbn,kitap_adi,kitap_yazar,kitap_kategori,kitap_yayinevi,kitap_aciklama,kitap_sayfa,kitap_adet FROM kitaplar"""     
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row,form in enumerate(data):
            for column,item in enumerate(form):
                self.tableWidget_5.setItem(row,column,QTableWidgetItem(str(item)))
                column+=1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        self.label_46.setText("Toplam {} kayıt".format(row_position))
        self.connection.close()

    def Add_New_Book(self):

        isbn = self.lineEdit_4.text()
        kitap_adi = self.comboBox.currentText()
        kitap_yazar = self.comboBox_7.currentText()
        kitap_kategori = self.comboBox_6.currentText()
        kitap_yayinevi = self.comboBox_8.currentText()
        kitap_aciklama = self.textEdit_2.toPlainText()
        kitap_sayfa = self.lineEdit_6.text()
        kitap_adet  = self.spinBox.value()

        if len(isbn) == 13 and len(kitap_yazar) > 0 and len(kitap_kategori) > 0 and len(kitap_yayinevi) > 0 and kitap_adet >0 and len(kitap_adi) > 0:

            try:
                self.connection = psycopg2.connect(user = "postgres",
                                                   password = "1234",
                                                   host = "localhost",
                                                   port = "5432",
                                                   database = "postgres")
                self.cursor = self.connection.cursor()
                self.cursor.execute("""INSERT INTO kitaplar(isbn,kitap_adi,kitap_yazar,kitap_kategori,kitap_yayinevi,kitap_aciklama,kitap_sayfa,kitap_adet) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",(isbn,kitap_adi,kitap_yazar,kitap_kategori,kitap_yayinevi,kitap_aciklama,kitap_sayfa,int(kitap_adet)))
                self.connection.commit()
                self.connection.close()

                QMessageBox.about(self,"Bilgilendirme","Yeni kitap başarıyla eklendi.")

                self.Show_All_Books()
                self.Show_Book_Combobox()
                self.lineEdit_4.setText("")
                self.textEdit_2.setPlainText("")
                self.lineEdit_6.setText("")
                self.spinBox.setValue(1)
                
            except psycopg2.errors.UniqueViolation:
                self.connection = psycopg2.connect(user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                port = "5432",
                                                database = "postgres")
                self.cursor = self.connection.cursor()
                QMessageBox.about(self,"Bilgilendirme","Eklemek istediğiniz kitap listede mevcut.Girdiğiniz adet kadar eklenecektir.")
                sql  = """UPDATE kitaplar SET kitap_adet = kitap_adet + %s WHERE isbn = %s"""
                
                self.cursor.execute(sql,(kitap_adet,isbn))
                self.connection.commit()
                self.connection.close()
                self.statusBar().showMessage("İşlem başarıyla gerçekleşti.")

                isbn = self.lineEdit_4.setText("")
                kitap_adi = self.comboBox.setCurrentIndex(0)
                kitap_yazar = self.comboBox_7.setCurrentIndex(0)
                kitap_kategori = self.comboBox_6.setCurrentIndex(0)
                kitap_yayinevi = self.comboBox_8.setCurrentIndex(0)
                kitap_aciklama = self.textEdit_2.setText("")
                kitap_sayfa = self.lineEdit_6.setText("")
                kitap_adet  = self.spinBox.setValue(1)
        else:
            QMessageBox.warning(self,"Dikkat","-ISBN numarası 13 haneli olmak zorundadır.\n-Kitap adı,kategori,yazar ve yayinevi girilmesi zorunlu alanlardır.\n")
    def Search_Books(self):

        try:
            aranan_kitap = self.comboBox_5.currentText()
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            sql = """SELECT * FROM kitaplar WHERE kitap_adi = %s"""
            self.cursor.execute(sql,[(aranan_kitap)])
            data = self.cursor.fetchone()
            print(data)
            self.lineEdit_7.setText(data[0])
            self.lineEdit.setText(data[1])
            self.comboBox_11.setCurrentText(data[3])
            self.comboBox_9.setCurrentText(data[2])
            self.comboBox_10.setCurrentText(data[7])
            self.textEdit.setText(data[4])
            self.lineEdit_9.setText(str(data[5]))
            self.spinBox_2.setValue(data[6])
        except TypeError:
            QMessageBox.about(self,"Hata","Aradığınız kitap listede bulunmamaktadır.")
        
    def Edit_Books(self):
        
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        aranan_kitap = self.comboBox_5.currentText()
        
        isbn = self.lineEdit_7.text()
        kitap_adi = self.lineEdit.text()
        kitap_yazar = self.comboBox_11.currentText()
        kitap_kategori = self.comboBox_9.currentText()
        kitap_yayinevi = self.comboBox_10.currentText()
        kitap_aciklama = self.textEdit.toPlainText()
        kitap_sayfa = self.lineEdit_9.text()
        kitap_adet  = self.spinBox_2.value()

        if len(isbn) == 13:

            sql  = """UPDATE kitaplar SET isbn = %s ,kitap_adi=%s ,kitap_yazar=%s ,kitap_kategori=%s ,kitap_yayinevi=%s ,kitap_aciklama=%s ,kitap_sayfa=%s ,kitap_adet=%s WHERE kitap_adi=%s"""
            self.cursor.execute(sql,(isbn,kitap_adi,kitap_yazar,kitap_kategori,kitap_yayinevi,kitap_aciklama,kitap_sayfa,kitap_adet,aranan_kitap))
            self.connection.commit()
            self.statusBar().showMessage("Kitap başarıyla güncellendi.")
            QMessageBox.about(self,"Başlık","Kitap başarıyla güncellendi")

        else:
            QMessageBox.warning(self,"Dikkat","ISBN numarası 13 haneli olmak zorundadır.")
            
        self.connection.close()
        self.Show_All_Books()
        

    def Delete_Books(self):
        if len(self.lineEdit.text()) > 0 and len(self.lineEdit_7.text()) > 0:
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            silinecek_kitap = self.comboBox_5.currentText()
            warning = QMessageBox.warning(self,"Kitap Sil","{} isimli kitabı silmek istediğinize  emin misiniz ?".format(silinecek_kitap),QMessageBox.Yes,QMessageBox.No)
            if warning == QMessageBox.Yes:
                sql = """DELETE FROM kitaplar WHERE kitap_adi=%s"""
                self.cursor.execute(sql,[(silinecek_kitap)])
                self.connection.commit()
                self.connection.close()
                self.statusBar().showMessage("Kitap başarıyla silindi.")
                self.Show_All_Books()
        else:
            QMessageBox.warning(self,"Uyarı","Tc kimlik numarası 11 haneli olmak zorundadır.")

    ########################################
    ############## USERS ###################

    def Add_New_User(self):

        ogrenci_tc = self.lineEdit_21.text()
        ogrenci_adi= self.lineEdit_34.text()
        ogrenci_soyadi = self.lineEdit_35.text()
        ogrenci_email = self.lineEdit_22.text()
        ogrenci_tel = self.lineEdit_23.text()
        
        if len(ogrenci_tc) == 11 and len(ogrenci_adi) > 0 and len(ogrenci_soyadi) > 0:
            
            try:
                
                self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")

                self.cursor = self.connection.cursor()
                self.cursor.execute("""INSERT INTO ogrenciler(ogrenci_tc,ogrenci_adi,ogrenci_soyadi,ogrenci_email,ogrenci_tel) 
                VALUES(%s,%s,%s,%s,%s)""",(str(ogrenci_tc),ogrenci_adi,ogrenci_soyadi,ogrenci_email,ogrenci_tel))
                self.connection.commit()
                QMessageBox.about(self,"Bilgilendirme","Yeni öğrenci başarıya eklendi.")
                self.lineEdit_21.setText("")
                self.lineEdit_34.setText("")
                self.lineEdit_35.setText("")
                self.lineEdit_22.setText("")
                self.lineEdit_23.setText("")
            
            except psycopg2.errors.UniqueViolation:
                
                QMessageBox.warning(self,"Uyarı","{} kimlik nolu öğrenci zaten kayıtlı.".format(ogrenci_tc))
                self.lineEdit_21.setText("")
                self.lineEdit_34.setText("")
                self.lineEdit_35.setText("")
                self.lineEdit_22.setText("")
                self.lineEdit_23.setText("")
        else:
            QMessageBox.warning(self,"Uyarı","-Lütfen zorunlu alanları doldurunuz.\n -Kimlik numarası 11 haneli olmak zorundadır.")


    def Login(self):

        ogrenci_tc = self.lineEdit_26.text()
        if len(ogrenci_tc) == 11:
            
            self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""SELECT * FROM ogrenciler""")
            data = self.cursor.fetchall()

            for i in data:
                if i[0] == ogrenci_tc :
                    
                    self.groupBox_5.setEnabled(True)
                    self.statusBar().showMessage("Giriş Başarılı")
                    
                    self.lineEdit_37.setText(i[0])
                    self.lineEdit_29.setText(i[1])
                    self.lineEdit_36.setText(i[2])
                    self.lineEdit_30.setText(i[3])
                    self.lineEdit_38.setText(i[4])     
        else:
            QMessageBox.warning(self,"Uyarı","Tc kimlik no 11 haneli olmak zorundadır.")

    def Edit_User(self):
        
        ogrenci_tc = self.lineEdit_37.text()
        ogrenci_adi= self.lineEdit_29.text()
        ogrenci_soyadi = self.lineEdit_36.text()
        ogrenci_email = self.lineEdit_30.text()
        ogrenci_tel = self.lineEdit_38.text()
        
        original_tc = self.lineEdit_26.text()

        if len(ogrenci_tc) == 11 and len(ogrenci_adi) > 0 and len(ogrenci_soyadi) > 0 and len(ogrenci_email) > 0:
     
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""UPDATE ogrenciler SET ogrenci_tc = %s ,ogrenci_adi = %s, ogrenci_soyadi = %s ,ogrenci_email = %s ,ogrenci_tel = %s WHERE ogrenci_tc = %s""",
            (ogrenci_tc,ogrenci_adi,ogrenci_soyadi,ogrenci_email,ogrenci_tel,original_tc))
            self.connection.commit()
            self.groupBox_5.setEnabled(False)
            QMessageBox.about(self,"Bilgilendirme","Öğrenci başarılı bir şekilde düzenlendi. ")

            self.lineEdit_37.setText("")
            self.lineEdit_29.setText("")
            self.lineEdit_36.setText("")
            self.lineEdit_30.setText("")
            self.lineEdit_38.setText("")

        else:
            QMessageBox.warning(self,"Dikkat","-TCKNo 11 haneli olmak zorundadır.\n-TCKNo,ad,soyad,email girilmesi zorunlu alanlardır.\n")
    def Delete_User(self):

        ogrenci_tc = self.lineEdit_26.text()

        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""DELETE FROM ogrenciler WHERE ogrenci_tc = %s""",[(ogrenci_tc)])
        self.connection.commit()
        self.connection.close()
        QMessageBox.about(self,"Bilgilendirme","Başarıyla silindi.")
        self.lineEdit_37.setText("")
        self.lineEdit_29.setText("")
        self.lineEdit_36.setText("")
        self.lineEdit_30.setText("")
        self.lineEdit_38.setText("")
        self.lineEdit_26.setText("")
        self.groupBox_5.setEnabled(False)

    ####################################
    ######### settings #################
    def Publisher_Selected(self,row,column):
        item = self.tableWidget_2.item(row,column)
        self.lineEdit_31.setText(item.text())
    def Author_Selected(self,row,column):
        item = self.tableWidget_3.item(row,0)
        self.lineEdit_32.setText(item.text())
    def Category_Selected(self,row,column):
        item = self.tableWidget_4.item(row,0)
        self.lineEdit_33.setText(item.text())

    def Delete_Category(self):
        kategori = self.lineEdit_33.text()
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""DELETE FROM kategori WHERE kategori=%s""",[kategori])
        self.connection.commit()
        self.connection.close()
        self.Show_Category()

    def Delete_Author(self):
        yazar = self.lineEdit_32.text()
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""DELETE FROM yazar WHERE yazar = %s""",[yazar])
        self.connection.commit()
        self.connection.close()
        self.Show_Author()
    def Delete_Publisher(self):
        yayinevi = self.lineEdit_31.text()
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""DELETE FROM yayinevi WHERE yayinevi=%s""",[yayinevi])
        self.connection.commit()
        self.connection.close()
        self.Show_Publisher()

    def Add_Category(self):
        try :
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            yeni_kategori = self.lineEdit_33.text()
            self.cursor.execute("""INSERT INTO kategori(kategori) VALUES(%s)""",(yeni_kategori,))
            self.connection.commit()
            self.Show_Category()
            self.Show_Category_Combobox()
            QMessageBox.about(self,"Bilgilendirme","Yeni kategori eklendi.")
        except psycopg2.errors.UniqueViolation:
            QMessageBox.warning(self,"Uyarı","Böyle bir kategori zaten mevcut.")
    def Show_Category(self):
        
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT kategori FROM kategori''')
        data = self.cursor.fetchall()
        

        if data :
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.tableWidget_4.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
    
    def Add_Author(self):
        try:
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            yeni_yazar = self.lineEdit_32.text()
            self.cursor.execute("""INSERT INTO yazar(yazar) VALUES(%s)""",(yeni_yazar,))
            self.connection.commit()
            self.Show_Author()
            self.Show_Author_Combobox()
            QMessageBox.about(self,"Bilgilendirme","Yeni yazar eklendi.")
        except psycopg2.errors.UniqueViolation:
            QMessageBox.warning(self,"Uyarı","Böyle bir yazar zaten mevcut.")
    def Show_Author(self):
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT yazar FROM yazar''')
        data = self.cursor.fetchall()

        if data :
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.tableWidget_3.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def Add_Publisher(self):
        try:
            self.connection = psycopg2.connect(user = "postgres",
                                            password = "1234",
                                            host = "localhost",
                                            port = "5432",
                                            database = "postgres")
            self.cursor = self.connection.cursor()
            yeni_yayinevi = self.lineEdit_31.text()
            self.cursor.execute("INSERT INTO yayinevi(yayinevi) VALUES(%s)",(yeni_yayinevi,))
            self.connection.commit()
            self.Show_Publisher()
            self.Show_Publisher_Combobox()
            QMessageBox.about(self,"Bilgilendirme","Yeni yayınevi eklendi.")
        except psycopg2.errors.UniqueViolation:
            QMessageBox.warning(self,"Uyarı","Böyle bir yayınevi zaten mevcut.")

    def Show_Publisher(self):
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT yayinevi FROM yayinevi''')
        data = self.cursor.fetchall()

        if data :
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
    
    ######### Create Excel #######
    ############################### 
    def Excel_All_Book(self):
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        sql = """SELECT isbn,kitap_adi,kitap_yazar,kitap_kategori,kitap_yayinevi,kitap_aciklama,kitap_sayfa,kitap_adet FROM kitaplar"""     
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        wb = Workbook('All_Books.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0,0,'ISBN')
        sheet1.write(0,1,'Kitap Adı')
        sheet1.write(0,2,'Yazar')
        sheet1.write(0,3,'Kategori')
        sheet1.write(0,4,'Yayınevi')
        sheet1.write(0,5,'Açıklama')
        sheet1.write(0,6,'Sayfa')
        sheet1.write(0,7,'Adet')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number,column_number,str(item))
                column_number+=1
            row_number+=1
        wb.close()
        self.connection.close()
        QMessageBox.about(self,"Bilgilendirme","Tüm kitaplar tablosunun excel raporu çıkartıldı.")
    def Excel_Lend(self):
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        sql="""SELECT
                    id,
                    kitap_isbn,
                    kitap_adi,
                    kitap_durum,
                    concat(ogrenci_adi,' ',ogrenci_soyadi) AS isim,
                    ogrenciler.ogrenci_tc,
                    alindi_tarihi,
                    teslim_tarihi
                FROM islemler
                    INNER JOIN kitaplar
                ON islemler.kitap_isbn = kitaplar.isbn
                    INNER JOIN  ogrenciler
                ON ogrenciler.ogrenci_tc = islemler.ogrenci_tc"""

        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        wb = Workbook('lend_Operations.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0,0,'ID')
        sheet1.write(0,1,'ISBN')
        sheet1.write(0,2,'Kitap Adı')
        sheet1.write(0,3,'Kitap Durum')
        sheet1.write(0,4,'İsim')
        sheet1.write(0,5,'Öğrenci Tc')
        sheet1.write(0,6,'Alındı Tarihi')
        sheet1.write(0,7,'Teslim Tarihi')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number,column_number,str(item))
                column_number+=1
            row_number+=1
        wb.close()
        self.connection.close()
        QMessageBox.about(self,"Bilgilendirme","Ödünç tablosunun excel raporu çıkartıldı.")
    ##################################################
    ######### show settings data in UI ###############
    def Show_Category_Combobox(self):
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT kategori FROM kategori ''')
        data = self.cursor.fetchall()

        self.comboBox_9.clear()
        for category in data :
            self.comboBox_9.addItem(category[0])
            self.comboBox_6.addItem(category[0])
        

    def Show_Author_Combobox(self):
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT yazar FROM yazar ''')
        data = self.cursor.fetchall()

        self.comboBox_7.clear()
        for author in data :
            self.comboBox_7.addItem(author[0])
            self.comboBox_11.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.connection = psycopg2.connect(user = "postgres",
                                        password = "1234",
                                        host = "localhost",
                                        port = "5432",
                                        database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT yayinevi FROM yayinevi ''')
        data = self.cursor.fetchall()

        self.comboBox_10.clear()
        for yayinevi in data :
            self.comboBox_10.addItem(yayinevi[0])
            self.comboBox_8.addItem(yayinevi[0])
    def Show_Book_Combobox(self):
        self.connection = psycopg2.connect(user = "postgres",
                                           password = "1234",
                                           host = "localhost",
                                           port = "5432",
                                           database = "postgres")
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT kitap_adi FROM kitaplar ''')
        data = self.cursor.fetchall()

        self.comboBox_3.clear()
        self.comboBox_5.clear()

        for kitap in data :
            self.comboBox_3.addItem(kitap[0])
            self.comboBox_5.addItem(kitap[0])
            self.comboBox.addItem(kitap[0])
    ########################################
    #########  UI Themes ###################
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open('themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


