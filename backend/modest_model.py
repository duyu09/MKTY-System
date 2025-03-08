'''
- 文件描述：明康慧医MKTY智慧医疗系统后端服务小规模模型端模块（MQ消费者端）
- 负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：modest_model.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''

# 说明：截至该系统用于毕设答辩之时，BiomedCLIP模型仍基于OpenCLIP，对transformers库的支持尚未完全完成，因此暂时无法使用transformers库自动方便地下载到本地并加载模型，需要用户自行下载模型。
# 模型地址：https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224

# 翻译模型是采用自动下载的方式。

from modest_model_util import info_print, get_mq_channel, start_print, load_model_and_tokenizer_BiomedCLIP, load_model_and_tokenizer_MarianMT, translate
from PIL import Image
import torch
import io
import base64

# 变量配置
mq_connection_parameters = {  # MQ连接参数
    'host': 'localhost',
    'port': 5672,
    "heartbeat": 40
}
MQ_NAME = 'modest_model_inference'  # MQ队列名称
VERSION = 'v1.0.0'  # 版本号
MODEL_PATH = r"./BiomedCLIP-PubMedBERT_256-vit_base_patch16_224"  # CLIP模型路径
MODE = "dev"  # 运行模式，可选值为`dev`、`prod`，默认为`dev`

start_print(VERSION)
model, tokenizer, preprocess, device = load_model_and_tokenizer_BiomedCLIP(MODEL_PATH)  # 加载模型和分词器
mt_model, mt_tokenizer = load_model_and_tokenizer_MarianMT(src="zh", trg="en")  # 加载翻译模型和分词器

params = {"model": model, "tokenizer": tokenizer, "preprocess": preprocess, "device": device, "mt_model": mt_model, "mt_tokenizer": mt_tokenizer}

def predict(message: dict, model, tokenizer, preprocess, device, mt_model, mt_tokenizer, remove_header: bool=True):
    '''
    - 函数功能：MQ回调函数（模型推理在这里完成）
    - 输入参数：message, model, tokenizer, preprocess, device
      - `message`（`dict`，消息体。按照要求，该参数为第一个形参，接收来自MQ的消息，本函数中消息为一个字典，键`texts`表示一个文本数组，键`image_base64`表示图像的base64字符串，键`language`表示文本的语言，可以为`zh`、`en`等，若为`zh`则启用翻译）
      - `model`（模型对象）
      - `tokenizer`（分词器对象）
      - `preprocess`（图像预处理器函数对象）
      - `device`（设备对象）
      - `mt_model`（翻译模型对象）
      - `mt_tokenizer`（翻译模型对应的分词器对象）
      - 告知函数图像数据字符串`image_base64`中是否有头部，若有头部须先去除再转换
    - 返回参数：`numpy.ndarray`（预测结果）
    '''
    labels = message["texts"]
    image_base64 = message["image_base64"]
    language = message["language"]
    if language == "zh":
        labels = translate(mt_model, mt_tokenizer, list(labels))
    if remove_header:
        image_base64 = image_base64[image_base64.find(",")+1:]  # 去掉base64头部
    image_data = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_data))  # 处理图像，将字节流看作文件
    image = preprocess(image).unsqueeze(0).to(device)

    texts = tokenizer([label for label in labels]).to(device)  # 文本编码

    with torch.no_grad():  # 推理
        image_features, text_features, logit_scale = model(image, texts)
        logits = (logit_scale * image_features @ text_features.t()).detach().softmax(dim=-1)
    
    logits_result = logits.cpu().numpy().tolist()  # 返回列表形式的概率分布数组
    translated_labels = labels
    
    if MODE == "dev":
        info_print(logits_result)
        info_print(translated_labels)
    return {"logits": logits_result[0], "labels": translated_labels}



channel = get_mq_channel(mq_connection_parameters, predict, params, queue_name=MQ_NAME)
info_print("已启动小规模模型推理端")
channel.start_consuming()
