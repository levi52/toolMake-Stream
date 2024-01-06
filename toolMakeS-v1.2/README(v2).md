# toolMake

## 界面展示

### 设置

用于设置通信时IP和端口信息，openGauss数据库连接信息

### 音频采集

左按钮点击开始采集，再次点击结束，右按钮用于解密文件

![image-20231227201935200](assets\image-20231227201935200.png)

### 视频采集

左按钮用于开始采集，中按钮用于暂停采集，右按钮用于结束采集

![image-20231227201957296](assets\image-20231227201957296.png)

### 传输

左侧部分用于选择角色，第一个按钮用于选择要传输的文件，第二个用于创建连接，第三个用于断开连接，第四个用于开启视频通话，第五个用于结束视频通话

![image-20231227202022000](assets\image-20231227202022000.png)

## 程序说明

### UI

界面绘制函数，使用QTDesigner设计制作。

在对应文件夹控制台输入如下代码，可以将UI文件转为python代码

```shell
pyuic5 -o windowUI.py MainWindow.ui
```

```python
def setupUi(self, MainWindow):
    ...
```

初始化部分数据

```python
# 数据
        self.isCamera = True
        self.isPause = False
        self.cameraFlag = 0
        self.pauseFlag = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.recording = False
        self.key = "levi"
        # self.database_info = {
        #         "database": "toolMake",
        #         "user": "dboper",
        #         "password": "dboper@123",
        #         "host": "192.168.42.129",
        #         "port": "26000"
        # }
        self.database_info = {
            "database": "",
            "user": "",
            "password": "",
            "host": "",
            "port": ""
        }
        # 音频参数
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
```

按键使能

```python
# 按钮点击
        self.camera_btn.clicked.connect(self.open_camera)
        self.stop_video_btn.clicked.connect(self.stop_camera)
        self.pause_video_btn.clicked.connect(self.pause_camera)
        self.start_audio_btn.clicked.connect(self.audio_click_handler)
        self.play_audio_btn.clicked.connect(self.open_audio)
        self.start_chat_btn.clicked.connect(self.start_video_chat)
        self.stop_chat_btn.clicked.connect(self.stop_video_chat)
        self.submit_btn.clicked.connect(self.setting_info)
        self.open_file_btn.clicked.connect(self.open_file)
        self.file_con_btn.clicked.connect(self.file_con)
        self.file_stop_btn.clicked.connect(self.file_stop)
```

### 设置

在UI的函数中，已初始化部分信息，可以修改

```python
self.db_host.setText("xxx")
        self.db_port.setText("xxx")
        self.db_user.setText("xxx")
        self.db_pwd.setText("xxx")
        self.db_name.setText("xxx")
        self.ip_lineEdit.setText("xxx")
        self.voice_port_lineEdit.setText("xxx")
        self.video_port_lineEdit.setText("xxx")
        self.text_port_lineEdit.setText("xxx")
```



```python
# 设置端口信息
    def setting_info(self):
        self.audio_ip = self.ip_lineEdit.text()
        self.audio_port = self.voice_port_lineEdit.text()
        self.video_ip = self.ip_lineEdit.text()
        self.video_port = self.video_port_lineEdit.text()
        self.file_ip = self.ip_lineEdit.text()
        self.file_port = self.text_port_lineEdit.text()
        self.database_info["database"] = self.db_name.text()
        self.database_info["host"] = self.db_host.text()
        self.database_info["port"] = self.db_port.text()
        self.database_info["user"] = self.db_user.text()
        self.database_info["password"] = self.db_pwd.text()
        print("initialize")
```

### 数据库部分

```python
# 数据库连接
    def connect_db(self, database_info):
        database = database_info["database"]  # 选择数据库名称
        user = database_info["user"]
        password = database_info["password"]
        host = database_info["host"]  # 数据库ip
        port = database_info["port"]
        mydb = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)  # 连接数据库
        return mydb

    # 上传数据
    def data_upload(self, input_file, file_size, file_type, file_data):
        print("数据上传中...")
        mydb = self.connect_db(self.database_info)
        cur = mydb.cursor()  # 创建光标
        # 创建数据库表
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS t_files (
                             id SERIAL PRIMARY KEY,
                             file_name VARCHAR(255) NOT NULL,
                             file_size BIGINT NOT NULL,
                             storage_time TIMESTAMP NOT NULL,
                             file_type VARCHAR(50) NOT NULL,
                             file_data BYTEA NOT NULL
                        )
                    """)
        mydb.commit()
        print('表创建成功！')
        fname = input_file.split('/')[-1]
        entime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cur.execute(
            "INSERT INTO t_files (file_name, file_size, storage_time, file_type, file_data) VALUES (%s, %s, %s, %s, %s::bytea)",
            (fname, file_size, entime, file_type, psycopg2.Binary(file_data))
        )
        mydb.commit()
        cur.close()  # 关闭光标
        mydb.close()  # 关闭数据库连接
        print("数据上传成功")
```

### RC4

#### 加密文件

```python
# 加密文件
    def encrypt_file(self, input_file):
        with open(input_file, "rb") as f:
            text_data = f.read()
        f.close()
        prefix = input_file.split('.')[0]
        suffix = input_file.split('.')[-1]
        sBox = self.s_box(self.key)
        encrypted_text = self.rc4_encrypt(text_data, sBox)
        output_file = prefix + "-encrypt." + suffix
        with open(output_file, "wb") as f:
            f.write(encrypted_text)
        f.close()
        print("文件已加密并保存为", output_file.split('/')[-1])
        return output_file
```

#### 解密文件

```python
# 解密文件
    def decrypt_file(self, input_file_path):
        # 文件名
        audioName = str(input_file_path).split('/')[-1]
        # 前缀
        prefix = audioName.split('.')[0]
        # 后缀
        suffix = audioName.split('.')[-1]
        with open(input_file_path, "rb") as f:
            encrypted_text_data = f.read()
        f.close()
        sBox = self.s_box(self.key)
        decrypted_text = self.rc4_encrypt(encrypted_text_data, sBox)
        pathName = os.path.dirname(input_file_path)
        print(pathName)
        audio_output_file = pathName + "/" + prefix + "-decrypt." + suffix
        with open(audio_output_file, "wb") as f:
            f.write(decrypted_text)
        f.close()
        print("The file has been decrypted and saved as ", audio_output_file)
        return audio_output_file
```

#### SBOX

```python
# 生成rc4算法S-Box
    def s_box(self, key):
        # S-盒
        sBox = list(range(256))
        # K-盒
        kBox = [ord(char) for char in key]
        j = 0
        for i in range(256):
            j = (j + sBox[i] + kBox[i % len(kBox)]) % 256
            sBox[i], sBox[j] = sBox[j], sBox[i]
        return sBox
    
    # rc4算法加密
    def rc4_encrypt(self, media_data, sBox):
        res = bytearray()
        i = j = 0
        for byte in media_data:
            i = (i + 1) % 256
            j = (j + sBox[i]) % 256
            sBox[i], sBox[j] = sBox[j], sBox[i]
            t = (sBox[i] + sBox[j]) % 256
            k = sBox[t]
            res.append(byte ^ k)
        return res
```

### LSB

#### 加水印

```python
# 加水印
    def lsb_encrypt(self, audio_path):
        # 文件名
        audioName = str(audio_path).split('/')[-1]
        # 前缀
        prefix = audioName.split('.')[0]
        # 后缀
        suffix = audioName.split('.')[-1]
        wav = wave.open(audio_path, 'rb')
        nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
        time = nframes / framerate
        # 以字节方式读取音频数据
        frames = wav.readframes(nframes)
        # 以灰度图模式读取水印图
        # rimg = cv2.imread('Chip(1).bmp', cv2.IMREAD_GRAYSCALE)  
        rimg = cv2.imread('python(1).bmp', cv2.IMREAD_GRAYSCALE)
        # 从二维矩阵转为一维并二值化
        rimg = rimg.flatten() > 128
        fname = os.path.dirname(audio_path) + "/" + prefix + "-lsp." + suffix
        wav_embedded = wave.open(fname, 'wb')
        wav_embedded.setparams(wav.getparams())
        data = np.frombuffer(frames, dtype=np.uint8)
        # 次低位嵌入水印
        data_embedded = data.copy()
        for i in range(len(rimg)):
            data_embedded[i] -= data_embedded[i] % 4 - data_embedded[i] % 2
            data_embedded[i] += rimg[i] * 2
        # 写入音频数据
        wav_embedded.writeframes(data_embedded.tobytes())
        print('完成')
        # 关闭文件
        wav.close()
        wav_embedded.close()
```

#### 提取水印

```python
# 提取水印
    def extractWater(self, input_file):
        # 读取音频文件
        wav = wave.open(input_file, 'rb')
        # 获取音频文件的信息
        nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
        time = nframes / framerate
        # 读取音频数据
        frames = wav.readframes(nframes)
        # 将字节数据转换为numpy数组，并进行归一化处理
        audio_data = np.frombuffer(frames, dtype=np.int16) / 32768.0
        # 创建时间轴
        time_axis = np.linspace(0, time, num=len(audio_data))
        # 将字节数据转换为numpy数组
        data = np.frombuffer(frames, dtype=np.uint8)
        # 计算NC值的函数
        def NC(template, img):
            template = template.astype(np.uint8)
            img = img.astype(np.uint8)
            result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
            nc = (result[0][0] + 1) / 2
            return nc
        # 设置水印图像的宽高
        rimg_height = 100
        rimg_width = 100
        # 以灰度图模式读取水印图像
        # rimg_original = cv2.imread('Chip(1).bmp', cv2.IMREAD_GRAYSCALE)
        rimg_original = cv2.imread('python(1).bmp', cv2.IMREAD_GRAYSCALE)
        # 读取携密音频的数据
        data_rimg = data[:rimg_height * rimg_width * 2]  # 保证数据足够提取水印
        # 提取水印
        rimg = np.zeros(rimg_height * rimg_width, dtype=np.uint8)
        for i in range(len(rimg)):
            rimg[i] = (data_rimg[i] % 4 - data_rimg[i] % 2) / 2 * 255
        # 从一维转为二维矩阵
        rimg = np.reshape(rimg, (rimg_height, rimg_width))
        # 计算NC值
        nc = NC(rimg_original, rimg)
        print(f'NC = {nc * 100} %')
        # 保存提取出的水印图像
        cv2.imwrite('watermark.png', rimg)
```

### 音频采集

#### 录音按键

```python
# 录音按钮
    def audio_click_handler(self):
        if self.recording:
            self.recording = False
            self.start_audio_btn.setIcon(QIcon("asserts/icon/audios.svg"))
        else:
            self.recording = True
            self.start_audio_btn.setIcon(QIcon("asserts/icon/stop circle.svg"))
            threading.Thread(target=self.record).start()
```

#### 录音
```python
# 录音
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.audio_time.setText(f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        exists = True
        self.audio_index = 1
        while exists:
            if os.path.exists(f"./media/recording{self.audio_index}.wav"):
                self.audio_index += 1
            else:
                exists = False
        sound_file = wave.open(f"./media/recording{self.audio_index}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()
        input_file = f"media/recording{self.audio_index}.wav"
        output_file = self.encrypt_file(input_file)
        # self.hide_watermark(input_file, 'watermark2.bmp')
        # self.lsp_crypt(input_file)
        file_size = os.path.getsize(input_file)
        with open(input_file, "rb") as f:
            file_data = f.read()
        print(file_size)
        f.close()
        self.data_upload(input_file, file_size, "wav", file_data)
```

### 视频采集

#### 打开摄像头

```python
# 打开摄像头
    def open_camera(self):
        self.fileName = ""
        if not self.isCamera:
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self, 'Choose file', '',
                                                                       "MP4Files(*.mp4);;AVI Files(*.avi)")
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            # 下面两种rtsp格式都是支持的
            #  cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cameraFlag = 1
            self.cap = cv2.VideoCapture(0)
            exists = True
            self.video_index = 1
            while exists:
                if os.path.exists(f"./media/video{self.video_index}.avi"):
                    self.video_index += 1
                else:
                    exists = False
            self.video_output = cv2.VideoWriter(f'./media/video{self.video_index}.avi', self.fourcc, 30.0,
                                                (640, 480))

        # 创建视频显示线程
        if (self.fileName != "") or (self.cameraFlag == 1):
            th = threading.Thread(target=self.Display)
            th.start()

    # 关闭摄像头
    def stop_camera(self):
        input_file = f"media/video{self.video_index}.avi"
        output_file = self.encrypt_file(input_file)
        file_size = os.path.getsize(input_file)
        with open(input_file, "rb") as f:
            file_data = f.read()
        print(file_size)
        self.data_upload(input_file, file_size, "avi", file_data)
        self.cameraFlag = 0
        self.stopEvent.set()

    # 暂停摄像
    def pause_camera(self):
        self.continueEvent1.set()

    # 显示摄像头画面
    def Display(self):
        self.camera_btn.setEnabled(False)
        self.stop_video_btn.setEnabled(True)
        self.pause_video_btn.setEnabled(True)
        while self.cap.isOpened() and True:
            success, frame = self.cap.read()
            self.video_output.write(frame)
            # RGB转BGR
            if success == False:
                print("play finished")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(img))

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            if True == self.continueEvent1.is_set():
                self.pause_video_btn.setIcon(QIcon("asserts/icon/play.svg"))
                self.continueEvent1.clear()
                self.pauseFlag = 1
                while self.pauseFlag == 1:
                    if True == self.continueEvent1.is_set():
                        self.pause_video_btn.setIcon(QIcon("asserts/icon/pause.svg"))
                        self.continueEvent1.clear()
                        self.pauseFlag = 0
            if True == self.stopEvent.is_set():
                break
        self.cap.release()
        self.stopEvent.clear()
        self.video_label.clear()
        self.stop_video_btn.setEnabled(False)
        self.camera_btn.setEnabled(True)
        self.video_label.setText("Video")
```

#### 关闭摄像头

```python
# 关闭摄像头
    def stop_camera(self):
        input_file = f"media/video{self.video_index}.avi"
        output_file = self.encrypt_file(input_file)
        file_size = os.path.getsize(input_file)
        with open(input_file, "rb") as f:
            file_data = f.read()
        print(file_size)
        self.data_upload(input_file, file_size, "avi", file_data)
        self.cameraFlag = 0
        self.stopEvent.set()
```

#### 暂停

```python
# 暂停摄像
    def pause_camera(self):
        self.continueEvent1.set()
```

#### 显示

```python
# 显示摄像头画面
    def Display(self):
        self.camera_btn.setEnabled(False)
        self.stop_video_btn.setEnabled(True)
        self.pause_video_btn.setEnabled(True)
        while self.cap.isOpened() and True:
            success, frame = self.cap.read()
            self.video_output.write(frame)
            # RGB转BGR
            if success == False:
                print("play finished")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(img))

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            if True == self.continueEvent1.is_set():
                self.pause_video_btn.setIcon(QIcon("asserts/icon/play.svg"))
                self.continueEvent1.clear()
                self.pauseFlag = 1
                while self.pauseFlag == 1:
                    if True == self.continueEvent1.is_set():
                        self.pause_video_btn.setIcon(QIcon("asserts/icon/pause.svg"))
                        self.continueEvent1.clear()
                        self.pauseFlag = 0
            if True == self.stopEvent.is_set():
                break
        self.cap.release()
        self.stopEvent.clear()
        self.video_label.clear()
        self.stop_video_btn.setEnabled(False)
        self.camera_btn.setEnabled(True)
        self.video_label.setText("Video")
```

### 通话

#### 发送视频帧

```python
# 发送视频帧
    def send_frame(self, sock):
        while self.cap.isOpened() and True:
            success, self.sframe = self.cap.read()
            # RGB转BGR
            if not success:
                print("play finished")
                break
            self.sframe = cv2.cvtColor(self.sframe, cv2.COLOR_RGB2BGR)
            img = QImage(self.sframe.data, self.sframe.shape[1], self.sframe.shape[0], QImage.Format_RGB888)
            self.chat_label.setPixmap(QPixmap.fromImage(img))
            cv2.waitKey(1)
            # _, self.encoded_frame = cv2.imencode('.jpg', self.sframe)
            _, self.encoded_frame = cv2.imencode('.jpg', self.sframe, [cv2.IMWRITE_JPEG_QUALITY, 10])
            print("send frame:" + str(len(self.encoded_frame)))
            sock.sendto(self.encoded_frame.tobytes(), (self.video_ip, int(self.video_port)))
            # print(len(self.encoded_frame.tobytes()))
            if self.stopChatEvent.is_set():
                sock.sendto("123".encode(), (self.video_ip, int(self.video_port)))
                break
        self.cap.release()
        self.stopChatEvent.clear()
```

#### 接收视频帧

```python
# 接收视频帧
    def recv_frame(self, sock):
        while True:
            data, _ = sock.recvfrom(921600)
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

#### 开始通话

```python
# 开始视频通话
    def start_video_chat(self):
        if self.server_btn.isChecked():
            # # 创建语音套接字UDP
            # self.server_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # # 绑定IP端口
            # self.server_audio.bind(("", int(self.audio_port)))
            # 创建语音套接字
            self.server_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 绑定IP端口
            self.server_audio.bind(("", int(self.audio_port)))
            # 监听
            self.server_audio.listen(128)
            # 连接成功
            self.sock_audio, client_addr = self.server_audio.accept()
            print("Client connected:", client_addr)
            # 创建视频套接字UDP
            self.server_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 绑定IP端口
            self.server_video.bind(("", int(self.video_port)))
            # ps = pyaudio.PyAudio()
            pr = pyaudio.PyAudio()
            # 发送接收语音线程
            # sender = threading.Thread(target=self.send_audio, args=(self.sock_audio, ps))
            recver = threading.Thread(target=self.recv_audio, args=(self.sock_audio, pr))
            # 发送接收视频线程
            # self.cap = cv2.VideoCapture(0)
            # vds = threading.Thread(target=self.send_frame, args=(self.server_video,))
            vdr = threading.Thread(target=self.recv_frame, args=(self.server_video,))
            # vds.start()
            vdr.start()
            # sender.start()
            recver.start()
        elif self.client_btn.isChecked():
            # 创建语音套接字
            # self.client_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 创建语音套接字
            self.client_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接
            self.client_audio.connect((self.audio_ip, int(self.audio_port)))
            # 创建视频套接字
            self.client_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ps = pyaudio.PyAudio()
            # pr = pyaudio.PyAudio()
            # 发送接收语音线程
            sender = threading.Thread(target=self.send_audio, args=(self.client_audio, ps))
            # recver = threading.Thread(target=self.recv_audio, args=(self.client_audio, pr))
            # 发送接收视频线程
            self.cap = cv2.VideoCapture(0)
            vds = threading.Thread(target=self.send_frame, args=(self.client_video,))
            # vdr = threading.Thread(target=self.recv_frame, args=(self.client_video,))
            vds.start()
            # vdr.start()
            sender.start()
            # recver.start()
```

#### 结束通话

```python
# 结束视频通话
    def stop_video_chat(self):
        self.stopChatEvent.set()
        if self.server_btn.isChecked():
            self.server_audio.shutdown(socket.SHUT_RDWR)
            self.server_video.shutdown(socket.SHUT_RDWR)
            self.server_audio.close()
            self.server_video.close()
        elif self.client_btn.isChecked():
            self.client_audio.shutdown(socket.SHUT_RDWR)
            self.client_video.shutdown(socket.SHUT_RDWR)
            self.client_audio.close()
            self.client_video.close()
        self.chat_label.clear()
        self.chat_label.setText("video")
        # self.stopChatEvent.set()
```

#### 发送语音

```python
# 发送语音
    def send_audio(self, sock, ps):
        stream = ps.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                         frames_per_buffer=self.CHUNK)
        while True:
            data = stream.read(self.CHUNK)
            print("send audio:" + str(len(data)))
            try:
                # sock.sendto(data, (self.audio_ip, int(self.audio_port)))
                sock.send(data)
            except Exception as e:
                print(f"Send error: {e}")
                break
            # time.sleep(0.01)
```

#### 接收语音

```python
# 接收语音
    def recv_audio(self, sock, pr):
        stream = pr.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                         frames_per_buffer=self.CHUNK)
        while True:
            try:
                # data, _ = sock.recvfrom(self.CHUNK)
                data = sock.recv(self.CHUNK)
                print("recv audio:" + str(len(data)))
                stream.write(data)
            except Exception as e:
                print(f"Receive error: {e}")
                break
            # time.sleep(0.01)
```

### 文件传输

#### 发送

```python
# 文件连接
    def file_con(self):
        if self.server_btn.isChecked():
            self.file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 绑定IP端口
            self.file_server.bind(("", int(self.file_port)))
            # 监听
            self.file_server.listen(128)
            # 连接成功
            self.sock_file, client_addr = self.file_server.accept()
            print("Client :", client_addr)
            self.sock_file.send(self.send_filename.encode())
            with open(self.send_filePath, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        self.sock_file.send(b'')
                        break
                    self.sock_file.send(data)
            print("文件发送完成")
            f.close()
        elif self.client_btn.isChecked():
            self.file_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接
            self.file_client.connect((self.file_ip, int(self.file_port)))
            fileName = self.file_client.recv(1024).decode()
            print(fileName)
            with open(fileName, "wb") as f:
                while True:
                    data = self.file_client.recv(1024)
                    if data == b'':
                        break
                    f.write(data)
            print("接收完毕")
```

#### 结束

```python
# 文件结束
    def file_stop(self):
        if self.server_btn.isChecked():
            self.sock_file.close()
            self.file_server.close()
            print("server stop")
        elif self.client_btn.isChecked():
            self.file_client.close()
            print("client stop")
```

#### 打开文件

```python
# 打开文件
    def open_file(self):
        self.send_filePath, oth = QFileDialog.getOpenFileName(self, "Open File")
        print(self.send_filePath)
        if self.send_filePath:
            self.send_filename = str(self.send_filePath).split('/')[-1]
            print(self.send_filename)
```



