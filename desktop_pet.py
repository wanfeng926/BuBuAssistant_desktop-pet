import os
import sys
import random
import http.client
import json
import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class BuBuAssistant(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(BuBuAssistant, self).__init__(parent)
        self.init()
        self.initPall()
        self.initCondition()
        self.initPetImage()
        self.petAction()
        self.petTalk()

    # 初始化桌宠图片
    def initPetImage(self):

        # 对话框定义
        self.talkLabel = QLabel(self)
        self.talkLabel.setGeometry(5, 30, 100, 100)
        # 对话框样式设计
        self.talkLabel.setStyleSheet("font:10pt '楷体';border-width: 1px;")

        self.image = QLabel(self)
        self.image.setGeometry(0, 60, 100, 100)
        # buff图片定义
        self.buff = QLabel(self)
        self.happybuff()

        self.idleAction()
        self.resize(160, 160)
        self.randomPosition()
        self.show()

        self.randomIdle = []
        self.HighIntimacy()
        
        self.chatState = []
        for i in os.listdir("./resources/chat"):
            self.chatState.append("./resources/chat/" + i)

        self.kissState = []
        for i in os.listdir("./resources/kiss"):
            self.kissState.append("./resources/kiss/" + i)

        self.hugState = []
        for i in os.listdir("./resources/hug"):
            self.hugState.append("./resources/hug/" + i)

        self.eatState = []
        for i in os.listdir("./resources/eat"):
            self.eatState.append("./resources/eat/" + i)

        self.beatState = []
        for i in os.listdir("./resources/beat"):
            self.beatState.append("./resources/beat/" + i)


        self.dialog = []
        with open("./files/dialog.txt", "r", encoding="utf-8") as f:
            text = f.read()
            self.dialog = text.split("\n")
    

    # 初始化桌宠位置
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = QRect(0,0,150,150)
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(QPoint(int(width), int(height)))

    # 窗体初始化
    def init(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()

    # 初始化托盘
    def initPall(self):
        icons = os.path.join('./icons/tigerIcon.png')
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(icons))
        showing = QAction(u'显示', self, triggered=self.showwin)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    # 将数据写回文件，并关闭程序
    def quit(self):
        with open("./files/condition.json", "w", encoding="utf-8") as f:
            json.dump({"Intimacy": self.intimacy,"Health": self.health,"Mood":self.mood}, f)
        self.close()
        sys.exit()

    # 显现
    def showwin(self):
        self.setWindowOpacity(1)

    # 高亲密度时将亲密图片加入
    def HighIntimacy(self):
        if self.intimacy > 50:
            self.randomIdle = []
            for i in os.listdir("./resources/randomIdle"):
                self.randomIdle.append("./resources/randomIdle/" + i)
            for i in os.listdir("./resources/highIntimacy"):
                self.randomIdle.append("./resources/highIntimacy/" + i)
        else:
            self.randomIdle = []
            for i in os.listdir("./resources/randomIdle"):
                self.randomIdle.append("./resources/randomIdle/" + i)

    # 初始化数据
    def initCondition(self):
        self.state = 0
        self.timer = QTimer()
        self.stateTimer = QTimer()
        self.talkTimer = QTimer()
        self.hasChat = False
        self.frame_count = 0  # 初始化帧计数器
        self.total_frames = 0  # GIF 总帧数
        self.play_times = 0 # gif播放次数
        self.fontDB = QFontDatabase()
        self.fontID = self.fontDB.addApplicationFont("./font/LanaPixel.ttf")
        self.fontFamily = self.fontDB.applicationFontFamilies(self.fontID)[0]
        with open('./files/condition.json','r',encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)
            self.intimacy = data.get('Intimacy')
            self.health = data.get('Health')
            self.mood = data.get('Mood')

    def happybuff(self):
        self.play_times = 1
        self.mov = QMovie("./icons/heart.gif")
        self.mov.setScaledSize(QSize(128, 128))
        self.buff.setMovie(self.mov)
        self.total_frames = self.mov.frameCount()  # 获取 GIF 总帧数
        self.mov.frameChanged.connect(self.updateFrameCount)
        self.mov.start()

    def sadbuff(self):
        self.play_times = 6
        self.mov = QMovie("./icons/rain.gif")
        self.mov.setScaledSize(QSize(128, 128))
        self.buff.setMovie(self.mov)
        self.total_frames = self.mov.frameCount()  # 获取 GIF 总帧数
        self.mov.frameChanged.connect(self.updateFrameCount)
        self.mov.start()

    def updateFrameCount(self):
        self.frame_count += 1
        if self.frame_count >= self.total_frames * self.play_times:  # 播放 3 遍后停止并移除 GIF
            self.mov.stop()
            self.buff.setMovie(None)  # 移除 GIF
            self.frame_count = 0  # 重置帧计数器

    def idleAction(self):
        self.movie = QMovie("./resources/idle/idle.gif")
        # 宠物大小
        self.movie.setScaledSize(QSize(100, 100))
        # 将动画添加到label中
        self.image.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    def randomState(self):
        self.movie = QMovie(random.choice(self.randomIdle))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()

    def clickState(self):
        self.movie = QMovie("./resources/click/excited.gif")
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()

    def chatSt(self):
        self.movie = QMovie(random.choice(self.chatState))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()

    def kissSt(self):
        self.movie = QMovie(random.choice(self.kissState))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()

    def hugSt(self):
        self.movie = QMovie(random.choice(self.hugState))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()        

    def eatSt(self):
        self.movie = QMovie(random.choice(self.eatState))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()

    def wcSt(self):
        self.movie = QMovie("./resources/wc/wc.gif")
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()        

    def beatSt(self):
        self.movie = QMovie(random.choice(self.beatState))
        self.movie.setScaledSize(QSize(100, 100))
        self.image.setMovie(self.movie)
        self.movie.start()            


    def Action(self):
        if self.state == 0:
            rand = random.randint(0, 100)
            if rand >= 10:
                self.idleAction()
            else:
                self.randomState()
        elif self.state == 1:
            self.clickState()
        elif self.state == 2:
            self.chatSt()
        elif self.state == 3:
            self.hugSt()
        elif self.state == 4:
            self.eatSt()
        elif self.state == 5:
            self.wcSt()
        elif self.state == 6:
            self.beatSt()
        elif self.state == 7:
            self.kissSt()

    def talk(self):
        rnd = random.randint(0, 100)
        if rnd < 5:
            self.talkLabel.setText(random.choice(self.dialog))
        else:
            self.talkLabel.setText("")
        self.talkLabel.setStyleSheet(
            "font: bold;"
            f"font:11pt {self.fontFamily};"
            "color:black;"
            "background-color: white"
            "url(:/)"
        )
        self.talkLabel.adjustSize()

    # 隔5s执行一遍Action函数
    def petAction(self):
        self.timer.timeout.connect(self.Action)
        self.timer.start(7500)
        self.state = 0
    
    def petTalk(self):
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(5000)


    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        if not self.hasChat:
            if event.button() == Qt.LeftButton:
                self.state = 1
                self.Action()
        self.is_follow_mouse = True
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        self.setCursor(QCursor(Qt.OpenHandCursor))

    # 鼠标拖动桌宠
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        if not self.hasChat:
            self.state = 0
            self.Action()
        self.setCursor(QCursor(Qt.ArrowCursor))
        event.accept()

    def enterEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        event.accept()
    
    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        event.accept()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        chat = menu.addAction("聊天")
        bubu = menu.addMenu("互动")
        kiss = bubu.addAction("贴贴")
        hug = bubu.addAction("抱抱")
        eat = bubu.addAction("吃好吃")
        wc = bubu.addAction("上厕所")
        beat = bubu.addAction("欺负")
        personal = bubu.addMenu("布布信息")
        personal.addAction(f"亲密度：{self.intimacy}")
        personal.addAction(f"健康值：{self.health}")
        personal.addAction(f"心情值：{self.mood}")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.quit()
        if action == hide:
            self.setWindowOpacity(0)
        if action == chat:
            self.chatWidget()
        if action == kiss:
            self.kissBehavior()
        if action == hug:
            self.hugBehavior()
        if action == eat:
            self.eatBehavior()
        if action == wc:
            self.wcBehavior()
        if action == beat:
            self.beatBehavior()

    # 恢复状态
    def resume(self):
        self.state = 0
    
    def kissBehavior(self):
        self.state = 7
        self.Action()
        if self.mood < 100:
            plusMood = random.randint(5, 15)
            self.mood = min(self.mood + plusMood, 100)
        if self.intimacy < 100:
            self.intimacy += 1
        self.HighIntimacy()
        self.happybuff()
        self.stateTimer.setSingleShot(True)
        self.stateTimer.timeout.connect(self.resume)
        self.stateTimer.start(3000)

    def hugBehavior(self):
        self.state = 3
        self.Action()
        if self.mood < 100:
            self.mood = min(self.mood + 5, 100)
        if self.intimacy < 100:
            self.intimacy += 1
        self.HighIntimacy()
        self.happybuff()
        self.stateTimer.setSingleShot(True)
        self.stateTimer.timeout.connect(self.resume)
        self.stateTimer.start(3000)

    def eatBehavior(self):
        self.state = 4 
        self.Action()
        index = random.choice([-1, 1])
        if self.mood < 100:
            randomMood = random.randint(1, 15)
            randomMood *= index
            if(randomMood > 0):
                self.mood = min(self.mood + randomMood, 100)
            else:
                self.mood = max(self.mood + randomMood, 0)
        if self.intimacy < 100:
            self.intimacy += 1
        if self.health < 100:
            randomHealth = random.randint(1, 5)
            randomHealth *= index
            if(randomHealth > 0):
                self.health = min(self.health + randomHealth, 100)
            else:
                self.health = max(self.health + randomHealth, 0)
        self.HighIntimacy()
        self.happybuff()
        self.stateTimer.setSingleShot(True)
        self.stateTimer.timeout.connect(self.resume)
        self.stateTimer.start(3000)

    def wcBehavior(self):
        self.state = 5 
        self.Action()
        if self.mood < 100:
            randomMood = random.randint(1, 15)
            randomMood *= random.choice([-1, 1])
            if(randomMood > 0):
                self.mood = min(self.mood + randomMood, 100)
            else:
                self.mood = max(self.mood + randomMood, 0)
        if self.intimacy < 100:
            self.intimacy += 1
        if self.health < 100:
            randomHealth = random.randint(1, 5)
            randomHealth *= random.choice([-1, 1])
            if(randomHealth > 0):
                self.health = min(self.health + randomHealth, 100)
            else:
                self.health = max(self.health + randomHealth, 0)
        self.HighIntimacy()
        self.happybuff()
        self.stateTimer.setSingleShot(True)
        self.stateTimer.timeout.connect(self.resume)
        self.stateTimer.start(3000)

    def beatBehavior(self):
        self.state = 6 
        self.Action()
        if self.mood > 0:
            randomMood = random.randint(1, 15)
            self.mood = max(self.mood - randomMood, 0)
        if self.intimacy > 0:
            self.intimacy = max(self.intimacy - 5, 0)
        if self.health > 0:
            randomHealth = random.randint(1, 5)
            self.health = max(self.health - randomHealth, 0)
        self.sadbuff()
        self.HighIntimacy()
        self.stateTimer.setSingleShot(True)
        self.stateTimer.timeout.connect(self.resume)
        self.stateTimer.start(3000)

    def chatWidget(self):
        self.state = 2
        self.hasChat = True
        self.Action()
        self.chat = ChatWindow()
        self.chat.clsBtn.clicked.connect(self.chatWidgetClose)
        self.chat.show()

    def chatWidgetClose(self):
        self.state = 0
        self.hasChat = False
        self.Action()
        self.chat.close()

class ChatWindow(QWidget):
    signal_result = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.signal_result.connect(self.update_ui)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.resize(280, 500)
        # 两个按钮
        icons = os.path.join('./icons/return.png')
        self.clsBtn = QPushButton(self)
        self.clsBtn.setIcon(QIcon(icons))
        self.sndBtn = QPushButton('发送', self)
        self.clsBtn.setGeometry(0, 0, 40, 30)
        self.clsBtn.setStyleSheet('QPushButton{border:none;background:transparent;}')
        self.sndBtn.setGeometry(210, 460, 60, 30)
        self.sndBtn.setStyleSheet('QPushButton{background:green;}')
        # 输入框
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 460, 195, 30)

        # 头像
        self.avatar1 = QPixmap("./icons/bubu.jpg")
        self.avatar2 = QPixmap("./icons/yier.jpg")

        # 显示框
        # self.textBrowser = QTextBrowser(self)
        # self.textBrowser.setGeometry(5, 35, 270, 420)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(5, 35, 270, 420)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 268, 418))

        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # 标签栏
        self.label = QLabel('布布', self)
        self.label.setGeometry(120, 5, 40, 20)

        self.chatMessages = [{"role": "Assistant","content": "你好呀！"}]

        # 聊天总数
        self.chatSum = 0

        self.sndBtn.clicked.connect(self.sendMessage)
        self.sndBtn.clicked.connect(self.set_bubble)
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.adjustScrollToMaxValue) #监听窗口滚动条范围

    def update_ui(self, result):
        self.chatMessages.append({"role": "Assistant", "content": result})
        Bubble.set_return(self, self.avatar1, result, Qt.LeftToRight)
        QApplication.processEvents()
        self.set_bubble()

    def sendMessage(self):
        self.message = self.textEdit.toPlainText()
        self.textEdit.clear()
        self.textEdit.setFocus()
        self.chatSum += 1
        self.chatMessages.append({"role": "Human","content": self.message})
        Bubble.set_return(self, self.avatar2, self.message, Qt.RightToLeft)   # 调用new_widget.py中方法生成右气泡
        QApplication.processEvents()
        thread = threading.Thread(target=self.AiTalk)
        thread.start() 

    def set_bubble(self):
        font = QFont()
        font.setPointSize(10)
        fm = QFontMetrics(font)
        if self.chatSum % 2 == 0:
            text_width = fm.width(self.message) + 115    #根据字体大小生成适合的气泡宽度
        else:
            text_width = fm.width(self.answer) + 115
        if text_width > 150:                  #宽度上限
            text_width=int(self.textBrowser.document().size().width())+50  #固定宽度
        self.widget.setMinimumSize(text_width,int(self.textBrowser.document().size().height()) + 60) #规定气泡大小
        self.widget.setMaximumSize(text_width,int(self.textBrowser.document().size().height()) + 60) #规定气泡大小
        self.scrollArea.verticalScrollBar().setValue(10)

    
    # 窗口滚动到最底部
    def adjustScrollToMaxValue(self):
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def AiTalk(self):
        self.chatSum += 1
        conn = http.client.HTTPSConnection("api.atomecho.cn")
        payload = json.dumps({
            "param": {
                "model": "3bf4d1af-38ce-4e94-939e-b1002b0b8455",
                "stream": False
            },
            "messages": self.chatMessages
        })
        headers = {
            'S-Auth-Secret': 'sk-014d100316a1063cde1d16f1b30bc6ac',# 替换成自己的Secret
            'S-Auth-ApiKey': 'a88326d1eba6a568d585e47f9f5e7ba8',# 替换成自己的ApiKey
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/open/text-chat/v1", payload, headers)
        res = conn.getresponse()
        data = res.read()

        self.answer = json.loads(data.decode("utf-8")).get('data').get('content')
        self.signal_result.emit(self.answer)


class Bubble:
    def set_return(self,ico,text,dir):  #头像，文本，方向
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setLayoutDirection(dir)
        # 水平布局
        self.horizontalLayout = QHBoxLayout(self.widget)
        # 头像垂直布局
        self.vertical = QVBoxLayout()
        self.label = QLabel(self.widget)
        self.label.setMaximumSize(QSize(30, 30))
        self.label.setPixmap(ico)
        self.label.setScaledContents(True)
        self.vertical.addWidget(self.label)
        self.vertical.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # 将头像加入水平布局
        self.horizontalLayout.addLayout(self.vertical)
        # 文本框
        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setLayoutDirection(Qt.LeftToRight)
        self.textBrowser.setStyleSheet("padding:10px;\n"
                                       "background-color: rgba(71,121,214,20);\n"
                                       "font: 10pt \"黑体\";\n"
                                       "border-radius: 10px;")
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QSize(0, 0))
        self.textBrowser.setMaximumSize(QSize(16777215, 16777215))
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = BuBuAssistant()
    sys.exit(app.exec_())
