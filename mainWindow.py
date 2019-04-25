import sys
from threading import Thread
from time import sleep

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lxml import etree
from companyRank import rank
from confirmSite import search


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
        self.setWindowTitle("Compete Demo")
        self.setWindowIcon(QIcon("icon.jpg"))

class mainWindow(window):
    def __init__(self,lenght=400,width=300):
        window.__init__(self,lenght,width)
    def mainShow(self):
        buttonRank=QPushButton("竞价排名",self)
        buttonRank.resize(340,60)
        buttonRank.move(30,30)
        buttonState=QPushButton("网站状态",self)
        buttonState.resize(340,60)
        buttonState.move(30,110)
        button58 = QPushButton("58同城", self)
        button58.resize(340, 60)
        button58.move(30, 190)
        buttonRank.clicked.connect(self.toRank)
        buttonState.clicked.connect(self.toState)
        button58.clicked.connect(self.to58)
        self.show()

    def toRank(self):
        self.close()
        self.rankPage=rankWindowShow(400,600)
        self.rankPage.rankShow()
    def toState(self):
        self.close()
        self.statePage=stateWindowShow(400,400)
        self.statePage.stateShow()
    def to58(self):
        self.close()
        self._58Page = _58WindowShow(400, 600)
        self._58Page._58Show()
class stateWindowShow(window):
    text=[]
    itemState=[]
    def __init__(self,lenght,width):
        window.__init__(self,lenght,width)
    def stateShow(self):
        vbox=QVBoxLayout()
        self.item=QLineEdit()
        vbox.addWidget(self.item)
        for i in range(5):
            lableA = QLabel("公司:", self)
            line = QLineEdit(self)
            lableB = QLabel("状态:未知", self)
            self.text.append(line)
            self.itemState.append(lableB)
            hbox = QHBoxLayout()
            tempWidge = QWidget()
            hbox.addWidget(lableA)
            hbox.addWidget(line)
            hbox.addWidget(lableB)
            tempWidge.setLayout(hbox)
            vbox.addWidget(tempWidge)
        buttonStart = QPushButton("检测", self)
        buttonStart.move(50, 50)
        buttonMain = QPushButton("返回", self)
        buttonMain.move(150, 50)
        buttonMain.clicked.connect(self.toMain)
        buttonStart.clicked.connect(self.state)

        boxWidge = QWidget()

        boxButton = QHBoxLayout()

        boxButton.addWidget(buttonStart)
        boxButton.addWidget(buttonMain)

        boxWidge.setLayout(boxButton)

        vbox.addWidget(boxWidge)
        self.setLayout(vbox)
        self.show()
    def state(self):
        keyword=self.item.text()
        try:
            result=search(keyword)
            index=0
            for i in range(5):
                self.text[i].setText("")
            for item in result:
                self.text[index].setText(item)
                if result[item]==False:
                    self.itemState[index].setText("状态:良好")
                else:
                    self.itemState[index].setText("状态:故障")
                index+=1
        except:
            pass
    def toMain(self):
        self.close()
        self.tempMain= mainWindow()
        self.tempMain.mainShow()


class rankWindowShow(window):
    text=[]
    rankNum=[]
    alive=[]
    def __init__(self,lenght,width):
        window.__init__(self,lenght,width)

    def rankShow(self):
        buttonStart=QPushButton("生成排名",self)
        #buttonEnd=QPushButton("停止",self)
        #buttonEnd.move(250,50)
        buttonMain = QPushButton("返回主界面", self)
        buttonchange = QPushButton("切换到360排名", self)
        #两个按钮
        buttonMain.clicked.connect(self.toMain)
        buttonStart.clicked.connect(self.start)

        vbox=QVBoxLayout()
        #主布局方式
        boxWidge=QWidget()
        #主布局
        boxButton=QHBoxLayout()
        #按钮布局
        boxButton.addWidget(buttonStart)
        boxButton.addWidget(buttonchange)
        boxButton.addWidget(buttonMain)

        boxWidge.setLayout(boxButton)
        #设置按钮布局

        tipAndButton=QWidget()
        tipBox=QHBoxLayout()
        #输入框布局及布局方式

        tipLine=QLabel("公司名称或网址:",self)
        #提示信息
        self.textLine = QLineEdit(self)
        #输入框
        tipBox.addWidget(tipLine)
        tipBox.addWidget(self.textLine)
        tipAndButton.setLayout(tipBox)
        vbox.addWidget(tipAndButton)

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

class _58WindowShow(window):

    def __init__(self,lenght,width):
        window.__init__(self, lenght, width)

    def _58rank(self,keyword):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}

        url = ("https://bj.58.com/huangyezonghe/?key=%s&cmcskey=%s&final=1&jump=1&specialtype=gls&classpolicy=huangyezonghe_Bs" % (keyword, keyword))  # 网址
        html = requests.get(url, headers=headers, timeout=(3, 7)).text
        s = requests.session()
        s.keep_alive = False  # 防止源代码过长，超时导致SSL错误
        html = etree.HTML(html)
        jingpinBox = html.xpath("//*[@class='jingpin']/parent::*/parent::*/p[1]/a")
        dingzhiBox = html.xpath("//*[@class='ico ding']/parent::*/parent::*/p[1]/a")
        totalBox = html.xpath("//*[@class='seller']/a")
        jingpin = []
        dingzhi = []
        other = []
        for i in jingpinBox:
            if i != None:
                jingpin.append(i.text)
        for i in dingzhiBox:
            if i != None:
                dingzhi.append(i.text)
        for i in range(len(totalBox) - len(dingzhiBox) - len(jingpinBox)):
            if i != None:
                other.append(totalBox[len(dingzhiBox) + len(jingpinBox) - 1 + i].text)
        return jingpin,dingzhi,other
    def toMain(self):
        self.close()
        self.tempMain= mainWindow()
        self.tempMain.mainShow()
    def _58Show(self):

        operateLayout=QHBoxLayout()
        self.mainLayout=QVBoxLayout()
        opbox=QWidget()
        textWidge=QWidget()
        textPart=QHBoxLayout()
        self.lineText=QLineEdit()
        tipText=QLabel("请输入关键词：")
        textButton=QPushButton("生成")
        textButton.clicked.connect(self._58showRank)
        textPart.addWidget(tipText)
        textPart.addWidget(self.lineText)
        textPart.addWidget(textButton)
        textWidge.setLayout(textPart)
        leaveButton = QPushButton("返回")
        prevButton=QPushButton("前一页")
        nextButton=QPushButton("后一页")
        switchPageButton=QPushButton("GO")
        switchPage=QLabel("转到第")
        page=QLabel("页")
        leaveButton.clicked.connect(self.toMain)
        switchPageLineText=QLineEdit()
        switchPageLineText.setFixedWidth(60)
        operateLayout.addWidget(leaveButton)
        operateLayout.addWidget(prevButton)
        operateLayout.addWidget(nextButton)
        operateLayout.addWidget(switchPage)
        operateLayout.addWidget(switchPageLineText)
        operateLayout.addWidget(page)
        operateLayout.addWidget(switchPageButton)
        _58formModle=QStandardItemModel(30,2)

        _58formModle.setHorizontalHeaderLabels(["类型","公司名称"])

        self._58form=QTableView()
        self._58form.setEditTriggers(QTableView.NoEditTriggers)
        self._58form.horizontalHeader().setStretchLastSection(True)
        self._58form.setColumnWidth(0, 40)
        self._58form.setModel(_58formModle)

        opbox.setLayout(operateLayout)
        self.mainLayout.addWidget(textWidge)
        self.mainLayout.addWidget(self._58form)
        self.mainLayout.addWidget(opbox)
        self.setLayout(self.mainLayout)
        self.show()
    def _58showRank(self):
        text=self.lineText.text()
        jingpin,dingzhi,other=self._58rank(text)
        Model=QStandardItemModel(len(jingpin),2)
        Model.setHorizontalHeaderLabels(["类型", "公司名称"])
        lenght=len(jingpin)
        for row in range(lenght):
            Model.setItem(row, 0, QStandardItem("精品广告"))
            Model.setItem(row, 1, QStandardItem(jingpin[row]))
        lenght=len(dingzhi)
        for row in range(lenght):
            Model.setItem(row+len(jingpin), 0, QStandardItem("顶置广告"))
            Model.setItem(row+len(jingpin), 1, QStandardItem(dingzhi[row]))
        lenght=len(other)
        for row in range(lenght):
            Model.setItem(row+len(jingpin)+len(dingzhi), 0, QStandardItem("普通广告"))
            Model.setItem(row+len(jingpin)+len(dingzhi), 1, QStandardItem(other[row]))
        self._58form.setModel(Model)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    a=mainWindow()
    a.mainShow()
    sys.exit(app.exec_())