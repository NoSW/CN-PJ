# CN-PJ

2020秋季学期计算机网络课程Socket编程大作业

## 题目

### **题目1：设计一个类http协议**

*   服务器端保存一份学生名单，包括学号、照片、姓名等。名单的存放方式随意
*   客户端针对学生名单进行各类请求，如增加，删除，查看等，每种请求通过头部字段进行具体的要求。 *建议加入图形界面

### **题目2：设计一个简单的文件传输协议**

*   实现客户与服务器之间简单的文件传递，如get/put等
  
*   客户可以查询服务器存放文件的目录，自定义文件存放的目录等

*   建议加入图形界面

### **题目3：简单的小说阅读器的设计**

*   服务器端保存小说文本（txt格式的即可） *客户可以打开对应的文本，翻页，翻章，跳页，书签，下载，关闭等
*   建议最好有图形界面，因为是txt格式，所谓的“页”可以通过规定每次内容包含的字节来规定

## **项目要求**

*   基本功能
*   多线程
*   图形界面

## **文件结构**

```
- server                        # （假装是）服务器运行目录
    - data                      # 服务器存储的数据
        - 00001
            - 00001.jpg
            - 00001.csv
        - 00002
            - 00002.jpg
            - 00002.csv
        .
        .
        .
    - handler.py                # 处理数据的增、删、查、改
    - shttp.py                  # Simple(Similar) Hypertext Transport Protocol, 仿HTTP构造的报文
    - thread.py                 # 定义一个线程池
    - main.py
- client                        # 客户端运行目录  
    - handler.py                # 处理各种请求（接、发数据包）
    - shttp.py                  # 构造、解析shttp
    - main.py                   # GUI界面
```

## **功能实现**

### **（服务端）数据存储**

本次PJ重点在socket编程，数据存储的各种问题（ACID等）一概忽略，（想用mysql存储数据来着，后面可能补个），采用直观明了了文件夹组织数据，并实现数据项的增加、删除、更新、查找  
以学生管理系统为例，每个数据项包含 `xxxxx.csv`（学号 姓名 是否存在照片） 和 `xxxxx.jpg`（照片）

### **SHTTP**

```
The format of my like-http is as follows:

1. Request message
    _______________________________________         ---+                    ----+
    |    [method]    |SPACE|[version]|CRLF|            | Request line           |
    |________________|_____|_________|____|__       ---+                        |
    |        host         |SPACE|[value]|CRLF|         |                        |
    |_____________________|_____|_______|____|         |                        |
    |    Authorization    |SPACE|[value]|              |                        |
    |_____________________|_____|_______|              |                        |
    |        Date         |SPACE|[value]|              | Header line            | 100 Bytes (fixed)
    |_____________________|_____|_______|              |                        |
    |  Content-Length     |SPACE|[value]|              |                        |
    |_____________________|_____|_______|           ---+                        |
    |SPACE| CRLF |                                     | Blank line             |
    |____ |______|____________ ______________       ---+                    ----+  
    |               Entity body              |         | request data
    |________________________________________|      ---+

    - method
        - DELETE    delete an object on the server
        - GET       request an object
        - HEAD      similar to the `GET` method, but it leaves out the requested object
        - POST      update an object
        - PUT       upload objects to the server

2. Response message
    __________________________________________      ---+                    ----+
    |    [version]   |SPACE|[status code]|CRLF|        | Status line            |
    |________________|_____|_____________|____|     ---+                        |
    |       host          |SPACE|[value]|CRLF |        |                        |
    |_____________________|_____|_______|___ _|        |                        |
    |       Date          |SPACE|[value]|              | Header line            |
    |_____________________|_____|_______|              |                        | 100 Bytes (fixed)
    |   Content-Length    |SPACE|[VALUE]|              |                        |
    |_____________________|_____|_______|           ---+                        |
    |SPACE| CRLF|                                      | Blank line             |
    |____ |_____|_____________________________      ---+                    ----+
    |               Entity body              |         | request data
    |________________________________________|      ---+

    - status code
        - 200 OK                Request succeeded and the information is returned in the response
        - 301 Moved Permanently Requested object has been permanently moved
        - 400 Bad Request       A generic error code indicating that the request could not be understood by the server.
        - 401 Unauthorized      Does not have permission
        - 404 Not Found         The requested document does not exist on this server       
        - 505 Not Supported     The requested SHTTP protocol version is not supported by the server

```


### **服务端响应**

  - 等待客户端连接
  - 连接成功，分配线程
  - 接收来自客户端的报文
  - 解析出请求类型（增删查改）
  - 调用handler处理请求
  - 构造响应报文
  - 发送响应报文

### **客户端请求**

请求类型，见图形界面。  
复用服务端的`shttp.py`、实现图形界面的`main.py`、与服务端交互的`handler.py`

### **图形界面**

按钮：

1. 选择操作类型
   1. get a student's information
   2. add a new student
   3. delete a student
   4. update a student\'s infomation
2. 输入id
3. 输入name
4. 上传照片 (upload)
5. 运行 (run)
