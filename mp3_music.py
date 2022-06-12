import os
from PyQt5 import QtWidgets,QtGui,QtCore
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import *
from cv2 import resize
from mp3music import Ui_HDMuzikcehennemi
import sqlite3
from PyQt5.QtGui import QPixmap


class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp,self).__init__()
        self.ui=Ui_HDMuzikcehennemi()
        self.ui.setupUi(self)
        self.player=QMediaPlayer()
        self.ui.listWidget.itemDoubleClicked.connect(self.Playmusic)
        self.ui.playbutton.clicked.connect(self.pauseMusic)
        self.ui.comboBox.activated.connect(self.liste)
        self.ui.comboSanatci.activated.connect(self.sanatciListesi)
        self.ui.comboSanatci.hide()
        
        qpixmap=QPixmap("img/sound-icon.png")
        qpixmap=qpixmap.scaled(30, 30)
        self.ui.label_2.setPixmap(qpixmap)
        volume=self.player.volume()
        self.ui.Volumeslider.setRange(0,100)
        self.ui.Volumeslider.setValue(float(volume)/2)
        self.ui.Volumeslider.valueChanged.connect(self.volume_slider)

        self.ui.horizontalSlider.setRange(0,0)
        self.ui.horizontalSlider.sliderMoved.connect(self.set_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        
        self.rootpath="C:\\Users\gundu\OneDrive\Masaüstü\Yazılım\Python\QtDesigner\Mp3mucis\Ezgi"
        self.musiclist=os.listdir(self.rootpath) 
    
        self.baglanti=sqlite3.connect("sarkilar.db")
        self.islem=self.baglanti.cursor()
        self.baglanti.commit()
        self.table=self.islem.execute("create table if not exists sarki(sarkiAdi text,sanatci text, muzikUrl text)")
        self.baglanti.commit()
       
        listOfTables = self.islem.execute("SELECT count(muzikUrl) FROM sarki").fetchall()
        if listOfTables==[(0,)]:
            for i in range(len(self.musiclist)):
                ekle="insert into sarki(sarkiAdi, sanatci, muzikUrl) values(?,?,?)"
                self.islem.execute(ekle,("","",self.musiclist[i]))
                
            self.baglanti.commit()

        Sanatciisimleri=self.islem.execute("Select DISTINCT sanatci from sarki").fetchall()
        liste=[]
        for i in range(len(Sanatciisimleri)): 
            liste.append(Sanatciisimleri[i][0])
  
        self.ui.comboBox.addItem("Sanatçılar",liste)

    def volume_slider(self):
        volume=self.ui.Volumeslider.value()
        self.player.setVolume(volume)
        self.ui.volumelabel.setText(str(volume)+"%")

    def position_changed(self,position):
        self.ui.horizontalSlider.setValue(position)
    
    def duration_changed(self,duration):
        self.ui.horizontalSlider.setRange(0,duration)

    def set_position(self,position):
        self.player.setPosition(position)

    def liste(self,index):
        if index==0:
            
            self.ui.listWidget.clear()
            self.ui.comboSanatci.clear()
            self.ui.comboSanatci.hide()
            for i in range(len(self.musiclist)):
                self.ui.listWidget.addItem(self.musiclist[i])
        elif index==1:
            self.ui.listWidget.clear()
            self.ui.comboSanatci.clear()
            self.ui.comboSanatci.hide()
        elif index==2:
            self.ui.comboSanatci.clear()
            self.ui.comboSanatci.show()
            self.ui.listWidget.clear()
            self.ui.comboSanatci.addItems(self.ui.comboBox.itemData(index)) 
            
        

    def sanatciListesi(self):
        
        currentsinger=self.ui.comboSanatci.currentText()
        self.ui.listWidget.clear()
        sanatcilistesi2=self.islem.execute("select * from sarki").fetchall()
        
        
        for i in range(len(sanatcilistesi2)):
            if sanatcilistesi2[i][1]==currentsinger:
                self.ui.listWidget.addItem(sanatcilistesi2[i][2])

        
            
    

    def Playmusic(self,item):
            sarki=item.text()
            print(sarki)
            full_file_path=os.path.join(self.rootpath,sarki)
            url=QUrl.fromLocalFile(full_file_path)
            content=QMediaContent(url)
            self.player.setMedia(content)
            
            self.player.play()
            self.ui.musicName.setText(sarki)
            
            

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("img/pause.png"))
            self.ui.playbutton.setIcon(icon)
        
    


    def pauseMusic(self):
            if self.player.state()==QMediaPlayer.PlayingState:
                self.player.pause()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/play (1).png"))
                self.ui.playbutton.setIcon(icon)
            else:
                self.player.play()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/pause.png"))
                self.ui.playbutton.setIcon(icon)



def app():
    app=QtWidgets.QApplication(sys.argv)
    win=myApp()
    win.show()
    sys.exit(app.exec_())
app()