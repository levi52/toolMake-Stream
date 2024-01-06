# 基础内容

```shell
# 1. 当前虚拟环境生成
pip freeze > requirements.txt

# 2. 单一项目
pip install pipreqs
# 当前目录生成
pipreqs . --encoding=utf8 --force

# 生成目录结构
tree /f > list.txt
```

data studio连接数据库

```
leviopengauss
192.168.42.129
26000
postgres
dboper
dboper@123
```

创建数据表

```sql
create table EncryptFile
(
fname VARCHAR(255) not null,
enfname VARCHAR(255) not null,
fpath VARCHAR(255) not null,
enfpath VARCHAR(255) not null,
entime VARCHAR(255) not null
);
```

数据库

```shell
pip install psycopg2
```

```python
import psycopg2

database_info = {
    "database": "toolMake",
    "user": "dboper",
    "password": "dboper@123",
    "host": "192.168.42.129",
    "post": "26000"
}


def connect_db(database_info):
    database = database_info["database"]  # 选择数据库名称
    user = database_info["user"]
    password = database_info["password"]
    host = database_info["host"]  # 数据库ip
    port = database_info["port"]
    mydb = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)  # 连接数据库
    return mydb


mydb = connect_db(database_info)
cur = mydb.cursor()  # 创建光标
cur.execute("select * from EncryptFile;")  # 执行SQL指令
results = cur.fetchall()  # 获取所有结果
result = cur.fetchone()  # 获取一条结果
print(results)  # 将获取的结果打印

mydb.commit()  # 提交当前事务
cur.close()  # 关闭光标
mydb.close()  # 关闭数据库连接

```

```python
INSERT INTO  EncryptFile VALUES ('recording1.wav','recording1.wav','recording1.wav','recording1.wav','levi','xxxx-xx-xx'); 
```

```python

```

```

```

```python

```

```python

```

# toolMake

## 项目介绍

使用PyQt5设计程序UI界面，使用PyAudio实现音频采集，使用OpenCV实现视频采集，使用RC4算法对采集的音频或视频加密，使用psycopg2连接OpenGauss数据库，存储文件信息

## 项目结构

```
toolMake
│  MainWindow.py	// 程序界面以及操作函数
│  MainWindow.ui	// 使用QtDesigner设计的UI界面
│  README.md	// 说明文件
│  toolMakeW.py	// 主程序
│  requirements.txt	// 第三方库
│
├─asserts	// 静态资源
│  └─icon	// 程序图标
│          audio.svg
│          audios.svg
│          camera.svg
│          chat.svg
│          close.svg
│          icon.qrc
│          maximize.svg
│          Minimize.svg
│          Open-file.svg
│          pause.svg
│          play.svg
│          stop circle.svg
│          Tool.svg
│          video.svg
│          window-maximize.svg
│      
├─media	// 音频，视频文件
│      recording1-encrypt.wav
│      recording1.wav
│      recording2-encrypt.wav
│      recording2.wav
│      
└─
```

## 程序说明

![image-20231226222034179](C:\Users\86152\Documents\PycharmProjects\toolMakeApp\toolMake\assets\image-20231226222034179.png)
### 发送视频帧

```python
    def send_frame(self, sock):
            while self.cap.isOpened() and True:
                    success, self.sframe = self.cap.read()
                    # RGB转BGR
                    if not success:
                            print("play finished")
                            break
                    self.sframe = cv2.cvtColor(self.sframe, cv2.COLOR_RGB2BGR)
                    # img = QImage(self.sframe.data, self.sframe.shape[1], self.sframe.shape[0], QImage.Format_RGB888)
                    # self.chat_label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    # _, self.encoded_frame = cv2.imencode('.jpg', self.sframe)
                    _, self.encoded_frame = cv2.imencode('.jpg', self.sframe, [cv2.IMWRITE_JPEG_QUALITY, 10])
                    print("send frame:" + str(len(self.encoded_frame)))
                    sock.sendall(self.encoded_frame.tobytes())
                    # print(len(self.encoded_frame.tobytes()))
                    if self.stopChatEvent.is_set():
                            break

            self.cap.release()
            self.stopChatEvent.clear()
```
### 接收视频帧

```python
    def recv_frame(self, sock):
            while True:
                    data = sock.recv(20000)
                    if not data:  # 检查接收到的数据是否为空
                            print("No data received.")
                            break
                    print("recv frame:" + str(len(data)))
                    self.cframe = np.frombuffer(data, dtype=np.uint8)
                    # 检查解码是否成功
                    if cv2.imdecode(self.cframe, cv2.IMREAD_COLOR) is None:
                            print("Failed to decode image.")
                            continue  # 继续下一次循环，尝试再次接收数据
                    self.cframe = cv2.imdecode(self.cframe, cv2.IMREAD_COLOR)
                    # self.cframe = cv2.cvtColor(self.cframe, cv2.COLOR_RGB2BGR)
                    img = QImage(self.cframe.data, self.cframe.shape[1], self.cframe.shape[0], QImage.Format_RGB888)
                    self.chat_label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    if self.stopChatEvent.is_set():
                            break
            self.cap.release()
            self.stopChatEvent.clear()
```
### 开始通话

```python
    def start_video_chat(self):
            if self.server_btn.isChecked():
                    # 创建语音套接字
                    self.server_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 绑定IP端口
                    self.server_audio.bind(("", int(self.audio_port)))
                    # 监听
                    self.server_audio.listen(128)
                    # 连接成功
                    self.sock_audio, client_addr = self.server_audio.accept()
                    print("Client connected:", client_addr)
                    # 创建视频套接字
                    self.server_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 绑定IP端口
                    self.server_video.bind(("", int(self.video_port)))
                    # 监听
                    self.server_video.listen(128)
                    # 连接成功
                    self.sock_video, client_vaddr = self.server_video.accept()
                    print("Client connected:", client_vaddr)
                    ps = pyaudio.PyAudio()
                    pr = pyaudio.PyAudio()
                    # 发送接收语音线程
                    sender = threading.Thread(target=self.send_audio, args=(self.sock_audio, ps))
                    recver = threading.Thread(target=self.recv_audio, args=(self.sock_audio, pr))
                    # 发送接收视频线程
                    self.cap = cv2.VideoCapture(0)
                    vds = threading.Thread(target=self.send_frame, args=(self.sock_video,))
                    vdr = threading.Thread(target=self.recv_frame, args=(self.sock_video,))
                    vds.start()
                    vdr.start()
                    sender.start()
                    recver.start()
            elif self.client_btn.isChecked():
                    # 创建语音套接字
                    self.client_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # 连接
                    self.client_audio.connect((self.audio_ip, int(self.audio_port)))
                    # 创建视频套接字
                    self.client_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_video.connect((self.video_ip, int(self.video_port)))
                    ps = pyaudio.PyAudio()
                    pr = pyaudio.PyAudio()
                    # 发送接收语音线程
                    sender = threading.Thread(target=self.send_audio, args=(self.client_audio, ps))
                    recver = threading.Thread(target=self.recv_audio, args=(self.client_audio, pr))
                    # 发送接收视频线程
                    self.cap = cv2.VideoCapture(0)
                    vds = threading.Thread(target=self.send_frame, args=(self.client_video,))
                    vdr = threading.Thread(target=self.recv_frame, args=(self.client_video,))
                    vds.start()
                    vdr.start()
                    sender.start()
                    recver.start()
```
### 挂断

```python
    def stop_video_chat(self):
            # self.stopChatEvent.set()
            if self.server_btn.isChecked():
                    self.sock_audio.shutdown(socket.SHUT_RDWR)
                    self.sock_video.shutdown(socket.SHUT_RDWR)
                    self.sock_audio.close()
                    self.sock_video.close()
                    self.server_audio.close()
                    self.server_video.close()
            elif self.client_btn.isChecked():
                    self.client_audio.shutdown(socket.SHUT_RDWR)
                    self.client_video.shutdown(socket.SHUT_RDWR)
                    self.client_audio.close()
                    self.client_video.close()
            self.chat_label.clear()
            self.chat_label.setText("video")
            self.stopChatEvent.set()
```



### 发送语音

```python
    def send_audio(self, sock, ps):
            stream = ps.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                             frames_per_buffer=self.CHUNK)
            while True:
                    data = stream.read(self.CHUNK)
                    print("send audio:" + str(len(data)))
                    try:
                            sock.send(data)
                    except Exception as e:
                            print(f"Send error: {e}")
                            break
                    time.sleep(0.01)  # prevent CPU usage from shooting up due to tight loops
```
### 接收语音

```python
    def recv_audio(self, sock, pr):
            stream = pr.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                             frames_per_buffer=self.CHUNK)
            while True:
                    try:
                            data = sock.recv(self.CHUNK)
                            print("recv audio:" + str(len(data)))
                            stream.write(data)
                    except Exception as e:
                            print(f"Receive error: {e}")
                            break
                    time.sleep(0.01)  # prevent CPU usage from shooting up due to tight loops
```
# 开发环境

# 参考文档列表
  * [文档1](链接)
  * [文档2](链接)

©️
