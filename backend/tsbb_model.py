'''
- 文件描述：明康慧医MKTY智慧医疗系统智能服务层时间序列预测模型推理与BigBird模型推理端（tsbb级联模型推理队列MQ消费者端）
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：large_model.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''
import torch
from tsbb_model_util import info_print, get_mq_channel, start_print, load_model_and_tokenizer_bigbird, load_model_and_tokenizer_ts, translate, load_model_and_tokenizer_MarianMT

# 变量配置
MQ_CONNECTION_PARAMETERS = {  # MQ连接参数
    'host': 'localhost',
    'port': 5672,
    "heartbeat": 0
}
MQ_NAME = 'tsbb_model_inference'  # MQ队列名称
VERSION = 'v1.0.0'  # 版本号
BB_MODEL_PATH = r"D:\MKTY\MKTY-System\backend\bigbird-pegasus-large-pubmed"  # bigbird大语言模型路径
TS_MODEL_PATH = r"D:\MKTY\MKTY-System\backend\timesformer"  # 时间序列模型路径
MODE = "dev"  # 运行模式，可选值为`dev`、`prod`，默认为`dev`

start_print(VERSION)

def predict(message: dict, bigbird_tokenizer, bigbird_model, ts_model, mt_model, mt_tokenizer):
    '''
    - 函数功能：接收MQ生产者端消息并执行模型推理计算
    - 负责人：杜宇
    - 输入参数：message, bigbird_tokenizer, bigbird_model, ts_model
      - `message`（`dict`，输入消息，包含文本内容）
      - `bigbird_tokenizer`（分词器对象）
      - `bigbird_model`（模型对象）
      - `ts_model`（时间序列模型对象）
    - 返回参数：预测结果
    '''
    def get_text_feature(text: str, tokenizer, model) -> torch.Tensor:
        '''
        - 函数功能：用`bigbird`提取文本特征
        - 负责人：杜宇
        - 输入参数：text, tokenizer, model
          - `text`（`str`，输入文本）
          - `tokenizer`（分词器对象）
          - `model`（模型对象）
        - 返回参数：特征向量(`torch.Tensor`，语句`CLS` token 对应的嵌入)
        '''
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():  # 禁用梯度计算，进行推理时加速
            outputs = model.model.encoder(**inputs)
        last_hidden_state = outputs.last_hidden_state
        cls_token_embedding = last_hidden_state[0][0]  # 获取 [CLS] token 对应的嵌入
        # sentence_embedding = last_hidden_state.mean(dim=1)[0]  # 对所有 token 嵌入求均值，得到句子的全局表示
        return cls_token_embedding # sentence_embedding
    task_type = message.get("taskType")
    task_language = message.get("taskLanguage")
    if task_type == 0:
        time_series = message.get("timeSeries")
        text = message.get("text")
        pass
    elif task_type == 1:
        texts_list = message.get("textsList", [])
        if task_language == "zh":
            texts_list = translate(mt_model, mt_tokenizer, texts_list)
        text_features = [get_text_feature(text, bigbird_tokenizer, bigbird_model).numpy().tolist() for text in texts_list]
        return text_features

bb_model, bb_tokenizer = load_model_and_tokenizer_bigbird(BB_MODEL_PATH)
ts_model = load_model_and_tokenizer_ts(TS_MODEL_PATH)
mt_model, mt_tokenizer = load_model_and_tokenizer_MarianMT(src="zh", trg="en")  # 加载翻译模型和分词器

params = {
    "bigbird_model": bb_model,
    "bigbird_tokenizer": bb_tokenizer,
    "ts_model": ts_model,
    "mt_model": mt_model,
    "mt_tokenizer": mt_tokenizer
}

channel = get_mq_channel(MQ_CONNECTION_PARAMETERS, predict, params, queue_name=MQ_NAME)
info_print("已启动BigBird与MKTY医学时序预测模型推理端")
channel.start_consuming()
