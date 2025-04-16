'''
- 文件描述：明康慧医MKTY智慧医疗系统后端服务工具方法模块
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：util.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''

import os
import io
import base64
import uuid
import mimetypes
import time
import pika
import ast
import traceback
import mysql.connector.cursor
import mysql.connector
import mysql.connector.pooling
from PIL import Image
from datetime import datetime
from rich.console import Console
from rich.rule import Rule
from functools import wraps
from argon2 import PasswordHasher, exceptions

# 定义常用文件扩展名及其对应的 MIME 类型
common_mime_types = {
    '.webp': 'image/webp',
    '.csv': 'text/csv',
    '.mp4': 'video/mp4',
    '.avi': 'video/x-msvideo',
    '.zip': 'application/zip',
    '.rar': 'application/vnd.rar',
    '.7z': 'application/x-7z-compressed',
    '.svg': 'image/svg+xml',
    '.ico': 'image/vnd.microsoft.icon',
    '.bmp': 'image/bmp',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.ico': 'image/icon',
    '.tiff': 'image/tiff',
    '.flac': 'audio/flac',
    '.ogg': 'audio/ogg',
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.m4a': 'audio/mp4',
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}

for ext, mime in common_mime_types.items():
    mimetypes.add_type(mime, ext)

console = Console(markup=False)

def info_print(msg: str, level: str="info") -> None:
    '''
    - 函数功能：打印日志。日志格式为：`[当前时间 日志级别] [日志内容]`
    - 负责人：杜宇
    - 输入参数：msg, level
      - `msg`（`str`，要打印的日志信息）
      - `level`（`str`，日志级别，不同级别日志的标头颜色不同以区分。可选值为`initial`、`info`、`warning`、`error`，默认为`info`）
    - 返回参数：`None`
    '''
    level = level.lower()
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-4]
    if level == "info":
        console.print(f"[{current_time} INFO]", style="green", highlight=False, end=" ")
        console.print(f"[{msg}]", highlight=False, width=console.width-19)
    elif level == "warning":
        console.print(f"[{current_time} WARNING]", style="yellow", highlight=False, end=" ")
        console.print(f"[{msg}]", highlight=False, width=console.width-22)
    elif level == "error":
        console.print(f"[{current_time} ERROR] [{msg}]", style="red bold", height=False, highlight=False)  # ERROR全部字体均为红色加粗
    elif level == "initial":
        console.print(f"[{current_time} INITIAL]", style="blue", highlight=False, end=" ")
        console.print(f"[{msg}]", highlight=False, width=console.width-22)
        
def start_print(version: str) -> None:
    '''
    - 函数功能：后台程序启动时打印欢迎信息。欢迎信息包括：本系统英文简称`M.K.T.Y.`的艺术字，以及系统名称、著作权信息、GitHub开源地址、版本号等initial日志。
    - 负责人：杜宇
    - 输入参数：`version`（`str`，版本号字符串，例如：`v1.1.0`）
    - 返回参数：`None`
    '''
    console.print(r"██\      ██\     ██\   ██\   ████████\  ██\     ██\ ", style="bold blue", highlight=False)
    console.print(r"███\    ███ |    ██ | ██  |  \__██  __| \██\   ██  |", style="bold blue", highlight=False)
    console.print(r"████\  ████ |    ██ |██  /      ██ |     \██\ ██  / ", style="bold blue", highlight=False)
    console.print(r"██\██\██ ██ |    █████  /       ██ |      \████  /  ", style="bold blue", highlight=False)
    console.print(r"██ \███  ██ |    ██  ██<        ██ |       \██  /   ", style="bold blue", highlight=False)
    console.print(r"██ |\█  /██ |    ██ |\██\       ██ |        ██ |    ", style="bold blue", highlight=False)
    console.print(r"██ | \_/ ██ |██\ ██ | \██\ ██\  ██ |██\     ██ |██\ ", style="bold blue", highlight=False)
    console.print(r"\__|     \__|\__|\__|  \__|\__| \__|\__|    \__|\__|", style="bold blue", highlight=False)
    console.print(Rule(style="bold blue"))
    console.print("明康慧医(MKTY)智慧医疗系统 后端服务", style="bold blue", justify="center", highlight=False)
    console.print(Rule(style="bold blue"))
    info_print("Minh Khoe Tue Y Smart Healthcare System Backend Module", level="initial")
    info_print("COPYRIGHT (c) 2025 DuYu (No.202103180009), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)", level="initial")
    info_print(r"https://github.com/duyu09/MKTY-System", level="initial")
    info_print(f"Version: {version}", level="initial")

def util_file2base64(file_path: str, add_header: bool=True) -> str:
    '''
    - 函数功能：将文件转换为base64字符串
    - 负责人：杜宇
    - 输入参数：file_path, add_header
      - `file_path`（`str`，文件路径）
      - `add_header`（`bool`，控制是否在base64字符串前添加`data:xxx/xxx;base64,`头部，文件类型由`file_path`中的拓展名自动决定。）
    - 返回参数：`base64_string`（`str`，base64编码后的文件数据字符串）
    '''
    with open(file_path, "rb") as file:
        base64_string = base64.b64encode(file.read()).decode('utf-8')
    if add_header:
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'  # 默认 MIME 类型
        base64_string = f"data:{mime_type};base64," + base64_string
    return base64_string

def util_base642file(base64_string: str, file_path: str, remove_header: bool=True) -> None:
    '''
    - 函数功能：将base64字符串转换为文件
    - 负责人：杜宇
    - 输入参数：base64_string, file_path, remove_header
      - `base64_string`（`str`，base64编码后的文件数据字符串）
      - `file_path`（`str`，文件路径）
      - `remove_header`（`bool`，告知函数字符串`base64_string`中是否有头部，若有头部须先去除再转换）
    - 返回参数：`None`
    '''
    if remove_header:
        base64_string = base64_string[base64_string.find(",") + 1:]
    file_data = base64.b64decode(base64_string)
    with open(file_path, "wb") as file:
        file.write(file_data)
        
def util_uuid() -> str:
    '''
    - 函数功能：生成`GUID`字符串
    - 负责人：杜宇
    - 输入参数：无参数
    - 返回参数：`guid_string`（`str`，生成的GUID字符串）
    '''
    guid_string = str(uuid.uuid4())
    return guid_string

def util_current_time() -> int:
    '''
    - 函数功能：获取当前服务器上以秒为单位的Unix时间戳
    - 负责人：杜宇
    - 输入参数：无参数
    - 返回参数：`time`（`int`，当前以秒为单位的Unix时间戳）
    '''
    return int(time.time())


def getDataBaseConnectionPool(host: str, user: str, password: str, database: str, pool_size: int=20, pool_name: str="mkty") -> mysql.connector.pooling.MySQLConnectionPool:
    """
    - 函数功能：建立数据库连接池
    - 负责人：杜宇
    - 输入参数：host, user, password, database
      - `host`（`str`，数据库主机地址）
      - `user`（`str`，数据库用户名）
      - `password`（`str`，数据库密码）
      - `database`（`str`，数据库名称）
    - 返回参数：`conn_pool`（`mysql.connector.pooling.MySQLConnectionPool`，数据库连接池对象）
    """
    info_print("正在建立数据库连接池")
    conn_pool = None
    try:
        conn_pool = mysql.connector.pooling.MySQLConnectionPool(host=host, user=user, password=password, database=database, pool_name=pool_name, pool_size=pool_size)
        if conn_pool is None:
            raise Exception("数据库连接池创建失败")
    except Exception as e:
        info_print(f"数据库连接池创建失败：{str(e)}", level="error")
        info_print("初始化失败，进程将自动结束。", level="error")
        exit(1)
    info_print(f"已建立数据库连接：{user}@{host}\{database}")
    info_print(f"已创建数据库连接池，连接池名称：{conn_pool.pool_name}, 连接池大小：{conn_pool.pool_size}")
    return conn_pool

def getCursor(connection_pool: mysql.connector.pooling.MySQLConnectionPool):
    """
    - 修饰器功能：从连接池中获取一个连接，并为flask请求处理函数注入分配的数据库游标对象，要求被修饰函数必须有一个`cursor`形参来接收游标对象，被修饰函数操作后无需关闭游标，此修饰器负责收尾工作。
    - 负责人：杜宇
    - 输入参数：`connection_pool`（`mysql.connector.pooling.MySQLConnectionPool`，数据库连接池对象）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            connection = connection_pool.get_connection()
            connection.autocommit = True
            cursor = connection.cursor(dictionary=True, buffered=True)
            funcReturn = None
            try:
                funcReturn = func(*args, **kwargs, cursor=cursor)
            except Exception as e:
                info_print(str(e), level="error")
                info_print(str(connection.is_connected()), level="error")
                traceback.print_exc()
            finally:
                # info_print("关闭数据库游标")
                connection.commit()
                cursor.close()
                del cursor
                connection.close()
                return funcReturn
        return wrapper
    return decorator

def util_encrypt_password(password: str) -> str:
    """
    - 函数功能：使用Argon2算法，对密码明文字符串进行加密，算法参数均使用默认值。
    - 负责人：杜宇
    - 输入参数：`password`（`str`，明文密码）
    - 返回参数：`hashed_password`（`str`，密码密文（加密后的密码））
    """
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password

def util_verify_password(hashed_password: str, password: str) -> bool:
    """
    - 函数功能：针对Argon2算法，对密码明文字符串与密文进行验证，验证密码是否正确。
    - 负责人：杜宇
    - 输入参数：`hashed_password`（`str`，密码密文（加密后的密码）），`password`（`str`，密码明文）
    - 返回参数：`bool`，密码验证结果，`True`表示密码正确，`False`表示密码错误。
    """
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except exceptions.VerifyMismatchError:
        return False

class RpcClient(object):
    """
    - 类功能：建立RabbitMQ RPC客户端（MQ生产者端）
    - 负责人：杜宇
    - 实例初始化参数：`mq_connection_parameters`（`dict`，RabbitMQ连接参数），`queue_name`（`str`，队列名称，默认为`modest_model_inference`）
    """
    def __init__(self, mq_connection_parameters, queue_name="modest_model_inference"):
        info_print("正在连接RabbitMQ服务器: {host}:{port}".format(**mq_connection_parameters) + "；队列: " + queue_name)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**mq_connection_parameters))
        self.channel = self.connection.channel()
        self.queue_name = queue_name

        result = self.channel.queue_declare(queue='', exclusive=True, durable=False, auto_delete=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.responses = {}  # 存储任务ID和对应的响应

    def on_response(self, ch, method, props, body):
        info_print("收到来自RabbitMQ的响应")
        if props.correlation_id in self.responses:
            self.responses[props.correlation_id] = body

    def call(self, data):
        """
        - 方法功能：向RabbitMQ发送任务，任务发送后返回任务ID，供后续查询任务状态
        - 负责人：杜宇
        - 输入参数：`data`（`Any`，要发送的任务数据，可以是任何可用`repr`序列化的Python数据类型）
        - 返回参数：`corr_id`（`str`，任务ID（GUID字符串））
        """
        corr_id = util_uuid()
        self.responses[corr_id] = None  # 初始化任务状态

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=corr_id,
            ),
            body=repr(data).encode("utf-8"))
        
        self.connection.process_data_events()
        return corr_id  # 返回任务ID

    def get_response(self, corr_id):
        """
        - 方法功能：查询任务状态，并返回任务结果，若任务结束并返回结果后，将删除任务状态
        - 负责人：杜宇
        - 输入参数：`corr_id`（`str`，任务ID）
        - 返回值：`response`（`Any`，可能是任何序列化后的Python对象，内容及类型取决于消费者发回的数据，若任务未结束，则返回`None`）
        """
        response = self.responses.get(corr_id)
        if response is None:
            self.connection.process_data_events()
            return None
        else:
            response = response.decode("utf-8")
            response = ast.literal_eval(response)
            del self.responses[corr_id]
        return response

def save_base64_image(base64_str: str, output_file: str) -> str | None:
    """
    - 函数功能：将带头部的base64图片数据保存为指定格式的文件（ **刻意避免使用临时文件方法以提升效率，故内部未调用已有的`util_file2base64`函数及`util_base642file`函数** ）
    - 负责人：杜宇
    - 输入参数:
      - base64_str (`str`, 带头部的base64字符串)
      - output_file (`str`, 输出文件路径，文件扩展名决定输出格式)  
    - 返回参数：成功返回`None`，失败返回错误信息(`str`)
    """
    try:
        if not output_file or not isinstance(output_file, str):  # 检查输出文件路径是否有效
            return "输出文件路径无效"
        ext = os.path.splitext(output_file)[1].lower()  # 获取文件扩展名并验证
        if not ext:
            return "无法从输出文件名中确定文件格式"
        format_map = {  # 支持的图片格式映射
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.gif': 'GIF',
            '.bmp': 'BMP',
            '.webp': 'WEBP'
        }
        if ext not in format_map:
            return f"不支持的输出格式: {ext}"
        if base64_str.startswith('data:'):  # 从Base64字符串中分离头部提取实际数据
            header, base64_str = base64_str.split(',', 1)
        image_data = base64.b64decode(base64_str)
        with Image.open(io.BytesIO(image_data)) as img:  # 使用Pillow在内存中处理图片
            if img.mode is not 'RGB':  # 一律转换为RGB或RGBA模式
                img = img.convert('RGB')
            output_buffer = io.BytesIO()  # 输出字节流
            img.save(output_buffer, format=format_map[ext])  # 保存为指定格式
            with open(output_file, 'wb') as f:
                f.write(output_buffer.getvalue())
        return None
    except Exception as e:
        return f"发生错误: {str(e)}"

