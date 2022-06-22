import os
from PyQt5 import QtWidgets,QtGui,QtCore
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import *
from mp3music import Ui_HDMuzikcehennemi
from playlist import Ui_Playlist
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
        self.ui.comboSanatci.activated.connect(self.sanatcisarkilari)
        self.ui.playlistButton.clicked.connect(self.playList)
        self.ui.comboBox_playlist.activated.connect(self.calmalistesi)

        self.ui.comboSanatci.hide()
        self.ui.playlistButton.hide()
        self.ui.comboBox_playlist.hide()
    
        
        qpixmap=QPixmap("img/sound-icon.png")
        qpixmap=qpixmap.scaled(30, 30)
        self.ui.label_2.setPixmap(qpixmap)
        
        #vertical slider settings
        volume=self.player.volume()
        self.ui.Volumeslider.setRange(0,100)
        self.ui.Volumeslider.setValue(round(int(volume)/2))
        self.ui.Volumeslider.valueChanged.connect(self.volume_slider)

        #horizontal slider settings
        self.ui.horizontalSlider.setRange(0,0)
        self.ui.horizontalSlider.sliderMoved.connect(self.set_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        
        #the path of music list
        self.rootpath="C:\\Users\gundu\OneDrive\Masaüstü\Yazılım\Python\QtDesigner\Mp3mucis\Ezgi"
        self.musiclist=os.listdir(self.rootpath) 

        #cretating a database named sarkilar means(musics)
        self.baglanti=sqlite3.connect("sarkilar.db")
        self.islem=self.baglanti.cursor()
        self.baglanti.commit()
        self.table=self.islem.execute("create table if not exists sarki(sarkiAdi text,sanatci text, muzikUrl text)")
        self.baglanti.commit()
       
        #adding song to the database table named sarki
        listOfTables = self.islem.execute("SELECT count(muzikUrl) FROM sarki").fetchall()
        if listOfTables==[(0,)]:
            for i in range(len(self.musiclist)):
                ekle="insert into sarki(sarkiAdi, sanatci, muzikUrl) values(?,?,?)"
                self.islem.execute(ekle,("","",self.musiclist[i]))
                
            self.baglanti.commit()

        #selecting singers name only one time and adding them to a list named liste
        Sanatciisimleri=self.islem.execute("Select DISTINCT sanatci from sarki").fetchall()
        liste=[] #empty list
        for i in range(len(Sanatciisimleri)): 
            liste.append(Sanatciisimleri[i][0])
        
        #taking table names of playlists that we already created in gui
        calma_listeleri=self.islem.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        #adding the name of playlist into the empty list named calmalist
        calmalist=[]
        for i in range(1,len(calma_listeleri)):
            calmalist.append(calma_listeleri[i][0])

        #adding the singers name and the playlists into the diffirent combo boxes
        self.ui.comboBox.addItem("Sanatçılar",liste)
        self.ui.comboBox.addItem("Çalma Listeleri",calmalist)

    #showing the second window when we push the plus button tto create a new playlist 
    def playList(self):
       win2=playlist()
       win2.show()
       win2.exec_()

    #volume slider settings
    def volume_slider(self):
        volume=self.ui.Volumeslider.value()
        self.player.setVolume(volume)
        self.ui.volumelabel.setText(str(volume)+"%")

        if volume==0:

            qpixmap=QPixmap("img/soundoff-icon.png")
            qpixmap=qpixmap.scaled(30, 30)
            self.ui.label_2.setPixmap(qpixmap)
        else:
            qpixmap=QPixmap("img/sound-icon.png")
            qpixmap=qpixmap.scaled(30, 30)
            self.ui.label_2.setPixmap(qpixmap)



    def position_changed(self,position):
        self.ui.horizontalSlider.setValue(position)
    
    def duration_changed(self,duration):
        self.ui.horizontalSlider.setRange(0,duration)

    def set_position(self,position):
        self.player.setPosition(position)

    #combobox function that connecting to the indexes that we want to see
    def liste(self,index):
        if index==0:
            self.ui.playlistButton.hide()
            self.ui.listWidget.clear()
            self.ui.comboSanatci.clear()
            self.ui.comboSanatci.hide()
            self.ui.comboBox_playlist.hide()
            for i in range(len(self.musiclist)):
                self.ui.listWidget.addItem(self.musiclist[i])


        elif index==1:
            self.ui.comboBox_playlist.hide()
            self.ui.playlistButton.hide()
            self.ui.comboSanatci.clear()
            self.ui.comboSanatci.show()
            self.ui.listWidget.clear()
            self.ui.comboSanatci.addItems(self.ui.comboBox.itemData(index)) 

        elif index==2:
            self.ui.listWidget.clear()
            self.ui.comboBox_playlist.clear()
            self.ui.comboSanatci.hide()
            self.ui.playlistButton.show()
            self.ui.comboBox_playlist.show()
            self.ui.comboBox_playlist.addItems(self.ui.comboBox.itemData(index))

            
        
    #list of singer on combobox
    def sanatcisarkilari(self):
        #this functions shows the songs of the singers that we clicked on
        currentsinger=self.ui.comboSanatci.currentText()
        self.ui.listWidget.clear()
        sanatcilar=self.islem.execute("select * from sarki").fetchall()
        
        
        for i in range(len(sanatcilar)):
            if sanatcilar[i][1]==currentsinger:
                self.ui.listWidget.addItem(sanatcilar[i][2])

    #playlist function  
    def calmalistesi(self):
        self.ui.listWidget.clear()  
        current_list=self.ui.comboBox_playlist.currentText()
        all_playlists=self.islem.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        for i in range(len(all_playlists)):
            if current_list==all_playlists[i][0]:
                currentplaylist=self.islem.execute('SELECT * FROM {}'.format(current_list)).fetchall()
                for i in range(len(currentplaylist)):
                    self.ui.listWidget.addItem(currentplaylist[i][0])
                
    
    #music play function
    def Playmusic(self,item):
            sarki=item.text()
            full_file_path=os.path.join(self.rootpath,sarki)
            url=QUrl.fromLocalFile(full_file_path)
            content=QMediaContent(url)
            self.player.setMedia(content)
            
            self.player.play()
            self.ui.musicName.setText(sarki)
            
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("img/pause.png"))
            self.ui.playbutton.setIcon(icon)
        
    

    #music pause function
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

class playlist(QDialog):
    def __init__(self):
        super(playlist,self).__init__()
        self.ui2=Ui_Playlist()
        self.ui2.setupUi(self)
        self.ui2.listWidget.itemDoubleClicked.connect(self.addMusic)
        self.ui2.makeplaylist.clicked.connect(self.playlistMaker)
        

        self.rootpath="C:\\Users\gundu\OneDrive\Masaüstü\Yazılım\Python\QtDesigner\Mp3mucis\Ezgi"
        self.musiclist=os.listdir(self.rootpath)
         
        for i in range(len(self.musiclist)):
                self.ui2.listWidget.addItem(self.musiclist[i])
                
                

        self.list=[]  
    #creating a new playlist and adding them into a empty list   
    def addMusic(self,item):
        music=item.text()
        count=0
        for i in self.list:
            if music==i:
                count=+1
        if count==0:
            self.ui2.listWidget_2.addItem(music)
            self.list.append(music)

        return self.list
    #adding the playlist into the database as a new table that named by the user    
    def playlistMaker(self):
        nameplaylist=self.ui2.listnameedit.text()
        self.baglanti=sqlite3.connect("sarkilar.db")
        self.islem=self.baglanti.cursor()
        self.baglanti.commit()
        self.table=self.islem.execute("create table if not exists {} (muzikUrl text)".format(nameplaylist))
        self.baglanti.commit()

        for i in range(len(self.list)):
            ekle="insert into {}(muzikUrl) values(?)".format(nameplaylist)
            self.islem.execute(ekle,(self.list[i],))
                
            self.baglanti.commit()
        
        self.close()
        


        

def app():
    
    app=QtWidgets.QApplication(sys.argv)
    win=myApp()
    win.show()
    sys.exit(app.exec_())
app()