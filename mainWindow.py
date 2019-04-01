import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from companyRank import rank
from threading import Thread
from time import sleep
class window(QWidget):
    def __init__(self,height,width):
        super(window,self).__init__()
        self.windowDef(height,width)
    def windowDef(self,height,width):
        self.setGeometry(0,0,height,width)
        frame= self.frameGeometry()
        center= QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.setWindowTitle("BaiduCompete Demo")
        self.setWindowIcon(QIcon("icon.jpg"))

class mainWindow(window):
    def __init__(self,lenght=400,width=200):
        window.__init__(self,lenght,width)
    def mainShow(self):
        buttonRank=QPushButton("竞价排名",self)
        buttonRank.resize(340,60)
        buttonRank.move(30,30)
        buttonState=QPushButton("网站状态",self)
        buttonState.resize(340,60)
        buttonState.move(30,110)
        buttonRank.clicked.connect(self.toRank)
        buttonState.clicked.connect(self.toState)
        self.show()

    def toRank(self):
        self.close()
        self.rankPage=rankWindowShow(400,600)
        self.rankPage.rankShow()
    def toState(self):
        self.close()
        self.statePage=stateWindowShow(400,400)
        self.statePage.stateShow()


class stateWindowShow(window):
    def __init__(self,lenght,width):
        window.__init__(self,lenght,width)
    def stateShow(self):
        self.show()
    def toMain(self):
        self.tempMain= mainWindow()
        self.tempMain.mainShow()

class rankWindowShow(window):
    text=[]
    rankNum=[]
    alive=[]

    def __init__(self,lenght,width):
        window.__init__(self,lenght,width)

    def rankShow(self):
        buttonStart=QPushButton("开始",self)
        buttonStart.move(50,50)
        #buttonEnd=QPushButton("停止",self)
        #buttonEnd.move(250,50)
        buttonMain = QPushButton("返回", self)
        buttonMain.move(150,50)
        buttonMain.clicked.connect(self.toMain)
        buttonStart.clicked.connect(self.start)

        vbox=QVBoxLayout()
        vbox.setSpacing(0)
        boxWidge=QWidget()

        boxButton=QHBoxLayout()

        boxButton.addWidget(buttonStart)
        boxButton.addWidget(buttonMain)
        #boxButton.addWidget(buttonEnd)
        boxWidge.setLayout(boxButton)

        tipLine=QLabel("              请输入公司名称或网址：",self)
        self.textLine=QLineEdit(self)
        vbox.addWidget(tipLine)
        vbox.addWidget(self.textLine)

        for i in range(15):
            lableA=QLabel("关键词:",self)
            line=QLineEdit(self)
            lableB = QLabel("排名:无", self)

            self.text.append(line)
            self.rankNum.append(lableB)

            hbox=QHBoxLayout()
            tempWidge=QWidget()

            hbox.addWidget(lableA)
            hbox.addWidget(line)
            hbox.addWidget(lableB)

            tempWidge.setLayout(hbox)
            vbox.addWidget(tempWidge)
        vbox.addWidget(boxWidge)
        self.setLayout(vbox)
        self.show()
        for i in range(20):
            self.alive.append(False)
    def getText(self,i):
        r=rank()
        while 1:
            name = self.textLine.text()
            keywords = self.text[i].text()
            # 如果关键字空，回到初始状态
            if keywords == ''or name=='':
                self.rankNum[i].setText("排名:无")
            else:
                res=r.main(keywords,name)
                if res!=None:
                    self.rankNum[i].setText("排名:"+str(res))
                    #db.database_of_rank(keywords,name)
                else:
                    self.rankNum[i].setText("排名:无")
                if self.alive[i]==False:
                    return
            sleep(3)

    def toMain(self):
        self.close()
        self.tempMain= mainWindow()
        self.tempMain.mainShow()

    def start(self):
        '''
        启动多线程实时显示信息
        '''
        # 防止重复创建线程
        for i in range(15):
            if not (self.alive[i]):
                self.alive[i] = True
                Thread(target=self.getText, args=(i,)).start()

    def stop(self):
        for i in range(15):
            self.alive[i] = False


if __name__ == "__main__":
    app=QApplication(sys.argv)
    a=mainWindow()
    a.mainShow()
    sys.exit(app.exec_())