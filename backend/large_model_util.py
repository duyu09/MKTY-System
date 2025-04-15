'''
- 文件描述：明康慧医MKTY智慧医疗系统后端服务大模型推理端（大规模模型推理队列MQ消费者端）工具函数模块
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：large_model_util.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 修改为中国国内镜像源（首次使用，必须要联网下载“缓存文件”，另外，翻译模型首次使用也依赖联网。）

import pika
import ast
from rich.console import Console
from rich.rule import Rule
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer


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
    - 函数功能：大规模模型推理端程序启动时打印欢迎信息。欢迎信息包括：本系统英文简称`M.K.T.Y.`的艺术字，以及系统名称、著作权信息、GitHub开源地址、版本号等initial日志。
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
    console.print("明康慧医(MKTY)智慧医疗系统 大语言模型(MKTY-3B-Chat)推理高性能服务器端", style="bold blue", justify="center", highlight=False)
    console.print(Rule(style="bold blue"))
    info_print("Minh Khoe Tue Y Smart Healthcare System Large-scale Model Inference High-performance Server Module", level="initial")
    info_print("COPYRIGHT (c) 2025 DuYu (No.202103180009), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)", level="initial")
    info_print(r"https://github.com/duyu09/MKTY-System", level="initial")
    info_print(f"Version: {version}", level="initial")

def get_mq_channel(mq_connection_parameters: dict, callback: callable, callback_parameters: dict, queue_name: str = "task_queue", durable: bool = True) -> pika.adapters.blocking_connection.BlockingChannel:
    '''
    - 函数功能：连接到RabbitMQ服务器并返回一个通道对象
    - 负责人：杜宇
    - 输入参数：mq_connection_parameters, callback, queue_name, durable
      - `mq_connection_parameters`（`dict`，RabbitMQ连接参数）
      - `callback`（`function`，消息处理回调函数，要求回调函数的第一个参数须接收从MQ中接收到的信息，模型的推理调用在这个函数里完成）
      - `callback_parameters`（`dict`，回调函数的其它参数，它将传给回调函数的第二个形参）
      - `queue_name`（`str`，队列名称，默认为`task_queue`）
      - `durable`（`bool`，是否持久化队列，默认为`True`）
    - 返回参数：`pika.adapters.blocking_connection.BlockingChannel`（RabbitMQ通道对象）
    '''
    info_print("正在连接RabbitMQ服务器")
    connection = pika.BlockingConnection(pika.ConnectionParameters(**mq_connection_parameters))  # 连接到RabbitMQ服务器
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=durable)  # 声明一个队列
    channel.basic_qos(prefetch_count=1)  # 告诉RabbitMQ，一旦消费者处理了任务，就可以从队列中删除它
    def on_message_callback(ch, method, properties, body):
        # 处理耗时任务
        # print("Received:", body)
        decoded_body = ast.literal_eval(body.decode('utf-8'))
        result = callback(decoded_body, **callback_parameters)
        # 返回结果给普通服务器
        ch.basic_publish(exchange='', routing_key=properties.reply_to,
                      properties=pika.BasicProperties(correlation_id = properties.correlation_id),
                      body=bytes(repr(result), 'utf-8'))
        ch.basic_ack(delivery_tag = method.delivery_tag)
    channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback)
    info_print(f'已连接到RabbitMQ服务器: {mq_connection_parameters["host"]}:{mq_connection_parameters["port"]}，队列名: {queue_name}')
    return channel

def load_model_and_tokenizer_mkty3b(model_dir: str):
    '''
    - 函数功能：加载`MKTY-3B-Chat`大模型及其分词器。
    - 负责人：杜宇
    - 输入参数：model_dir
      - `model_dir`（`str`，模型目录路径）
    - 返回参数：model, tokenizer
      - `model`（模型对象）
      - `tokenizer`（分词器对象）
    '''
    info_print(f"正在加载模型和分词器")
    model_dir = os.path.abspath(model_dir)
    info_print(f"模型目录路径: {model_dir}")
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    return model, tokenizer


