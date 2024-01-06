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



# 开发环境

# 参考文档列表
  * [文档1](链接)
  * [文档2](链接)

©️
