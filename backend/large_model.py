'''
- 文件描述：明康慧医MKTY智慧医疗系统智能服务层大模型推理端模块（大规模模型推理队列MQ消费者端）
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：large_model.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''

from large_model_util import info_print, get_mq_channel, start_print, load_model_and_tokenizer_mkty3b

# 变量配置
mq_connection_parameters = {  # MQ连接参数
    'host': 'localhost',
    'port': 5672,
    "heartbeat": 0
}
MQ_NAME = 'large_model_inference'  # MQ队列名称
VERSION = 'v1.0.0'  # 版本号
MODEL_PATH = r"./mkty"  # MKTY-3B-Chat大语言模型路径
MODE = "dev"  # 运行模式，可选值为`dev`、`prod`，默认为`dev`

start_print(VERSION)
model, tokenizer = load_model_and_tokenizer_mkty3b(MODEL_PATH)  # 加载MKTY-3B-Chat模型和分词器

params = { "model": model, "tokenizer": tokenizer, "max_new_tokens": 2000 }

def predict(message: dict, model, tokenizer, max_new_tokens=2000):
    '''
    - 函数功能：MQ回调函数（模型推理在这里完成）
    - 负责人：杜宇
    - 输入参数：message, model, tokenizer
      - `message`（`dict`，消息体。按照要求，该参数为第一个形参，接收来自MQ的消息，本函数中消息为一个字典，键`prompt`表示当前会话提示词，键`context`表示会话历史，为一个数组，数组中每个元素的形式为`{"role": "user", "content": prompt}`或`{"role": "assistant", "content": response}`）
      - `model`（模型对象）
      - `tokenizer`（分词器对象）
      - `max_new_tokens`（`int`，生成的最大新token数，默认为2000）
    - 返回参数：`str`（生成的语句）
    '''
    if MODE == "dev":
        info_print("接收到调用明康慧医大模型请求。")
    prompt = message["prompt"]  # str
    context = message["context"]  # list[dict]
    context.append({"role": "user", "content": prompt})  # 加入当前会话
    text = tokenizer.apply_chat_template(
        context,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    if MODE == "dev":
        info_print(response)
    return response
    
channel = get_mq_channel(mq_connection_parameters, predict, params, queue_name=MQ_NAME)
info_print("已启动MKTY-3B-Chat大规模语言模型推理端")
channel.start_consuming()
