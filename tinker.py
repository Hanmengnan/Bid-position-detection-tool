from tkinter import *
from time import sleep
from threading import Thread
from companyRank import rank
from Mongotest import rankDB

class baidu():
    def __init__(self):
        self.top = Tk()
        self.top.title('百度实时竞价排名')
        headline = Label(self.top, text='请输入公司名或网址名')
        slider = Label(self.top, text='滑动滑块设置刷新间隔(秒)')
        # 设定滑块
        self.s1 = Scale(
            self.top,
            from_=0.5,
            to=5,
            orient=HORIZONTAL,  # 设置横向
            resolution=0.1,  # 设置步长
            # tickinterval = 0.5,
            length=300,
            command=self.change)
        self.textin = Entry(self.top)
        # 序号和结果列表
        nums = []
        frs = []
        self.keyword = []
        self.rank=[]
        self.text=[]
        for i in range(20):
            frs.append(Frame(self.top))
            if i<9:
                index='0'+str(i+1)
            else:
                index=str(i+1)
            nums.append(Label(frs[i], text='关键字' + index))
            self.text.append(StringVar())
            self.text[i].set('排名:无')
            self.rank.append(Label(frs[i],textvariable=self.text[i]))
            self.keyword.append(Entry(frs[i], width=17))
            nums[i].pack(side=LEFT)
            self.keyword[i].pack(side=LEFT)
            self.rank[i].pack(side=LEFT)
        # 默认时间间隔
        self.interval = 1
        # 线程存活状态
        self.alive=[]
        for i in range(20):
            self.alive.append(False)
        #两个按钮的容器
        F1=Frame(self.top)
        # 确定按钮
        B1 = Button(F1, text='开始', command=self.start,height=2,width=6,fg='green')
        # 停止按钮
        B2 = Button(F1, text='停止', command=self.stop,height=2,width=6,fg='red')
        # 图标排列
        headline.pack()
        self.textin.pack()
        B1.pack(side=LEFT)
        B2.pack(side=LEFT)
        slider.pack()
        self.s1.pack()
        for i in range(20):
            frs[i].pack()
        F1.pack()
        self.top.resizable(0,0)

        mainloop()

    def check(self,i):
        '''
        单个线程函数实时显示排名
        '''
        r = rank()
        db=rankDB()
        while 1:
            name = self.textin.get()
            keywords = self.keyword[i].get()
            # 如果关键字空，回到初始状态
            if keywords == '':
                self.text[i].set("排名:无")
            res=r.main(keywords,name)
            if res!=None:
                self.text[i].set("排名:"+str(res))
                db.database_of_rank(keywords,name)
            else:
                self.text[i].set("排名:无")
            if self.alive[i]==False:
                return
            sleep(self.interval)

    def start(self):
        '''
        启动多线程实时显示信息
        '''
        # 防止重复创建线程
        for i in range(20):
            print(i)
            if not(self.alive[i]):
                self.alive[i] = True
                Thread(target=self.check,args=(i,)).start()


    def stop(self):
        for i in range(20):
            self.alive[i] = False

    def change(self, var):
        '''
        由滑块交互更改时间间隔
        '''
        self.interval = float(var)


if __name__ == "__main__":
    baidu()