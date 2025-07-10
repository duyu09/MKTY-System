'''
- 文件描述：明康慧医MKTY智慧医疗系统后端服务
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：run.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''
import os
import json
import math
import pickle
import numpy as np
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from gevent.pywsgi import WSGIServer
from util import (
    util_uuid,
    util_current_time,
    extract_text_from_file,
    split_text_into_pieces,
    compute_tfidf_features,
    util_base642file,
    util_file2base64,
    search_similar_pieces,
    info_print,
    start_print,
    getDataBaseConnectionPool,
    getCursor,
    util_encrypt_password,
    util_verify_password,
    RpcClient,
    save_base64_image,
    export_chat_to_pdf,
    send_email,
    average_cosine_similarity
)

# 全局变量配置
MODE = 'dev'  # 运行模式（dev=开发模式，prod=生产模式）
DATA_DIR = r'./data/'  # 数据文件夹
AVATAR_FORMAT = '.webp'  # 头像文件格式
VERSION = 'v1.1.0'  # 版本号
PORT = 5555  # 后端服务端口
HOST = '0.0.0.0'  # 后端服务主机地址
STRONG_PASSWORD = 'DUYU09'  # 强密码，用于加密token
EMAIL_SENDER = "qluduyu09@163.com"  # 邮件发送者
EMAIL_SENDER_AUTHORIZATION = ""  # 邮件发送者授权码
EMAIL_SENDER_SMTP_SERVER = "smtp.163.com"  # 邮件发送者SMTP服务器地址
EMAIL_SENDER_SMTP_PORT = 465  # 邮件发送者SMTP服务器端口
MD_MQ_CONNECTION_PARAMETERS = {  # 多模态辅诊端MQ连接参数
    'host': 'localhost',
    'port': 5672,
    'heartbeat': 0
}
MD_QUEUE_NAME = 'modest_model_inference'  # 多模态辅诊端MQ队列名称
LLM_MQ_CONNECTION_PARAMETERS = {  # 大规模模型推理端MQ连接参数
    'host': 'localhost',
    'port': 5672,
    'heartbeat': 0
}
LLM_QUEUE_NAME = 'large_model_inference'  # 大规模模型推理端MQ队列名称
TSBB_MQ_CONNECTION_PARAMETERS = {  # TSBB端MQ连接参数
    'host': 'localhost',
    'port': 5672,
    'heartbeat': 0
}
TSBB_QUEUE_NAME = 'tsbb_model_inference'  # TSBB端MQ队列名称
DATABASE_CONNECTION_POOL_PARAMETERS = {  # 数据库连接池参数
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mkty_02',
    'pool_size': 5,
    'pool_name': 'mkty'
}
KE_PIECE_LENGTH = 1024  # 知识实体分片长度

# 程序启动，首先打印必要信息
start_print(VERSION)
info_print("正在初始化后端服务")

# 建立数据库连接池
conn_pool = getDataBaseConnectionPool(**DATABASE_CONNECTION_POOL_PARAMETERS)

# 通过MQ分别与智能服务层各端建立连接
llm_rpc_client = RpcClient(LLM_MQ_CONNECTION_PARAMETERS, LLM_QUEUE_NAME)
md_rpc_client = RpcClient(MD_MQ_CONNECTION_PARAMETERS, MD_QUEUE_NAME)
tsbb_rpc_client = RpcClient(TSBB_MQ_CONNECTION_PARAMETERS, TSBB_QUEUE_NAME)

# 初始化Flask后台服务应用
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = STRONG_PASSWORD  # 强密码，用于加密token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 配置token永不过期
jwt = JWTManager(app)
working_directory = os.path.abspath(os.getcwd())
data_directory = os.path.abspath(DATA_DIR)
info_print(f"程序工作目录：{working_directory}")
info_print(f"后台数据目录：{data_directory}")
info_print("后台服务初始化完成")


@app.route('/')
def home01():
    return "This is Minh Khoe Tue Y Smart Healthcare System Backend Module.<br> Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)."

@app.route('/api')
def home02():
    return "This is Minh Khoe Tue Y Smart Healthcare System Backend Module.<br> Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)"

@app.route('/api/test', methods=['POST'])
@jwt_required()
def t_token():
    user_id = get_jwt_identity()
    return jsonify({'code': 0, 'msg': 'Token验证成功', 'userId': user_id})


@app.route('/api/loginVerification', methods=['POST'])
@getCursor(conn_pool)
def login_verification(cursor):
    '''
    - API功能：用户登录
    - 负责人：杜宇
    - 请求参数：userLoginKey, userLoginType, userPassword
      - `userLoginKey`: 用户登录标识（`str`，可以是用户ID或联系方式等）
      - `userLoginKeyType`: 用户登录标识类型（`int`，`0`=用户ID，`1`=联系方式）
      - `userPassword`: 用户密码（`str`，明文，后端负责加密与数据库密文进行校验） 
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=登录成功，`1`=登录失败）
      - `msg`: 自然语言提示信息（`str`）
      - `userLoginTime`: 用户请求登录时间（`int`，以秒为单位的Unix时间戳）
      - `userId`: 用户ID（`int`）
      - `accessToken`: 令牌（`str`，令牌中包含了`userId`的信息）
    '''
    user_data = request.json
    user_login_key = user_data.get('userLoginKey')
    user_login_key_type = user_data.get('userLoginKeyType')
    user_password = user_data.get('userPassword')
    user_login_time = util_current_time()
    if user_login_key is None or user_login_key == "" or user_password is None or user_password == "":
        return jsonify({'code': 1, 'msg': '用户登录标识或密码不可读取。'})
    if user_login_key_type is None or not (user_login_key_type in {0, 1}):
        return jsonify({'code': 1, 'msg': '未知用户登录标识类型。'})
    if user_login_key_type == 0:
        cursor.execute(f"SELECT * FROM userinfo WHERE userId='{user_login_key}'")
    else:
        cursor.execute(f"SELECT * FROM userinfo WHERE userContact='{user_login_key}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '登录失败，用户不存在或用户名有错误。'})
    else:
        user_id = result[0]['userId']
        user_ciphertext = result[0]['userCiphertext']
        if not util_verify_password(user_ciphertext, user_password):
            return jsonify({'code': 1, 'msg': '登录失败，密码错误。'})
        access_token = create_access_token(identity=user_id)
        return jsonify({'code': 0, 'msg': '登录成功', 'userLoginTime': user_login_time, 'accessToken': access_token, 'userId': user_id})

@app.route('/api/register', methods=['POST'])
@getCursor(conn_pool)
def register(cursor):
    '''
    - API功能：用户注册
    - 负责人：杜宇
    - 请求参数：userName, userType, userSex, userSexPermission, userAge, userAgePermission, userFrom, userFromPermission, userContact, userContactPermission, userDescription, userImportantInfo, userImportantInfoPermission, userPassword, userAvatar
      - `userName`: 用户姓名（`str`）
      - `userType`: 用户类型（`str`，其在数据库中不以数值存储，`0`=患者，`1`=医师，`2`=其他人员）
      - `userSex`: 用户性别（`int`，`0`=男，`1`=女）
      - `userSexPermission`: 用户性别权限（`int`，`0`=公开，`1`=私密）
      - `userAge`: 用户年龄（`int`，数值>=0）
      - `userAgePermission`: 用户年龄权限（`int`，`0`=公开，`1`=私密）
      - `userFrom`: 用户来源（`str`，患者用户填写城市；医师用户填写机构名称）
      - `userFromPermission`: 用户来源权限（`int`，`0`=公开，`1`=私密）
      - `userContact`: 用户联系方式（`str`，电话号码或邮箱，该项可用于登录，故不可重复）
      - `userContactPermission`: 用户联系方式权限（`int`，`0`=公开，`1`=私密）
      - `userDescription`: 用户自述（`str`）
      - `userImportantInfo`: 用户重要信息（`str`，分为患者重要信息和医师重要信息写入数据库）
      - `userImportantInfoPermission`: 用户重要信息权限（`int`，`0`=公开，`1`=私密）
      - `userPassword`: 密码密文（`str`，由前端负责加密）
      - `userAvatar`: 用户头像（`str`，图像base64字符串，经前端剪裁压缩）
    - 响应参数：code, msg, userId
      - `code`: 执行状态（`int`，`0`=注册成功，`1`=注册失败）
      - `msg`: 自然语言提示信息（`str`）
      - `userId`: 注册成功后系统生成的用户Id（`int`）
      - `userRegisterTime`: 用户注册时间（`int`，服务器时间，以秒为单位的Unix时间戳）
    '''
    user_data = request.json
    user_name= user_data.get('userName')
    user_type = user_data.get('userType')
    user_sex = user_data.get('userSex')
    user_sex_permission = user_data.get('userSexPermission')
    user_age = user_data.get('userAge')
    user_age_permission = user_data.get('userAgePermission')
    user_from = user_data.get('userFrom')
    user_from_permission = user_data.get('userFromPermission')
    user_contact = user_data.get('userContact')
    user_contact_permission = user_data.get('userContactPermission')
    user_description = user_data.get('userDescription')
    user_important_info = user_data.get('userImportantInfo')
    user_important_info_permission = user_data.get('userImportantInfoPermission')
    user_password = user_data.get('userPassword')
    user_avatar = user_data.get('userAvatar')
    
    if user_name is None or user_name == "" or user_password is None or user_password == "" or user_sex is None or not (user_sex in {0, 1}) or user_type is None or not (user_type in {0, 1, 2}):
        return jsonify({'code': 1, 'msg': '表单数据出现严重问题。'})
    
    cursor.execute(f"SELECT * FROM userinfo WHERE userContact='{user_contact}'")
    result = cursor.fetchall()
    if not (result is None or len(result) == 0):
        return jsonify({'code': 1, 'msg': '您提供的联系方式已存在，请您更换。'})
    
    user_id = 0
    user_avatar_id = util_uuid()
    img_path = os.path.abspath(os.path.join(DATA_DIR, 'avatar', (user_avatar_id + AVATAR_FORMAT)))
    util_base642file(user_avatar, img_path, remove_header=True)
    user_register_time = util_current_time()
    try:
        user_ciphertext = util_encrypt_password(user_password)
        sql = f"INSERT INTO userinfo (userCiphertext, userName, userType, userSex, userSexPermission, userAge, userAgePermission, userFrom, userFromPermission, userContact, userContactPermission, userDescription, patientImportantInfo, doctorImportantInfo, userImportantInfoPermission, userAvatarId, userRegisterTime) VALUES ('{user_ciphertext}', '{user_name}', '{user_type}', {user_sex}, {user_sex_permission}, {user_age}, {user_age_permission}, '{user_from}', {user_from_permission}, '{user_contact}', {user_contact_permission}, '{user_description}', '{user_important_info}', '{user_important_info}', {user_important_info_permission}, '{user_avatar_id}', {user_register_time})"
        cursor.execute(sql)
        user_id = cursor.lastrowid
    except Exception as e:
        return jsonify({'code': 1, 'msg': '数据库写入失败: ' + str(e)})
    return jsonify({'code': 0, 'msg': '注册成功', 'userId': user_id, 'userRegisterTime': user_register_time})

@app.route('/api/getUserAvatar', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_user_avatar(cursor):
    '''
    - API功能：获取用户头像的带头部Base64字符串
    - 负责人：杜宇
    - 请求参数：userId
      - `userId`: 用户ID（`int`，此处表示查看`userId`的头像，不表示token对应的`userId`）
    - 响应参数：code, msg, userAvatar
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `userAvatar`: 用户头像（`str`，图像base64字符串，带头部）
    '''
    user_data = request.json
    user_id = user_data.get('userId')
    if user_id is None or user_id == "" or user_id < 0:
        return jsonify({'code': 1, 'msg': '用户ID不可读取。'})
    cursor.execute(f"SELECT userAvatarId FROM userinfo WHERE userId='{user_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '该用户不存在。'})
    else:
        user_avatar_id = result[0]['userAvatarId']
        img_path = os.path.abspath(os.path.join(DATA_DIR, 'avatar', (user_avatar_id + AVATAR_FORMAT)))
        user_avatar = util_file2base64(img_path, add_header=True)
        return jsonify({'code': 0, 'msg': '获取成功', 'userAvatar': user_avatar})
    
@app.route('/api/getUserInfo', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_user_info(cursor):
    '''
    - API功能：获取用户信息，不包括头像Base64字符串以及密码。
    - 负责人：杜宇
    - 请求参数：userId
      - `userId`: 用户ID（`int`，此处表示查看userId的信息，不表示token对应的userId）
    - 响应参数：code, msg, userInfo
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `userInfo`: 用户信息（子`JSON`，若`userId`与请求发起者的`user_id`相同，则表示查看自己的信息，返回除密码外的全部字段；若不相同，则表示查看别人的信息，按权限返回。）
    '''
    user_data = request.json
    user_id = user_data.get('userId')
    operate_user_id = get_jwt_identity()  # 操作用户ID
    if user_id is None or user_id == "" or user_id < 0:
        return jsonify({'code': 1, 'msg': '用户ID不可读取。'})
    cursor.execute(f"SELECT * FROM userinfo WHERE userId='{user_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '该用户不存在。'})
    else:
        result_dict = result[0]
        result_dict.pop('userCiphertext')
        if user_id != operate_user_id:
            if result_dict['userSexPermission'] == 1:
                result_dict.pop('userSex')
            if result_dict['userAgePermission'] == 1:
                result_dict.pop('userAge')
            if result_dict['userFromPermission'] == 1:
                result_dict.pop('userFrom')
            if result_dict['userContactPermission'] == 1:
                result_dict.pop('userContact')
            if result_dict['userImportantInfoPermission'] == 1:
                result_dict.pop('patientImportantInfo')
                result_dict.pop('doctorImportantInfo')
        return jsonify({'code': 0, 'msg': '获取成功', 'userInfo': result_dict})
    
@app.route('/api/modifyUserInfo', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def modify_user_info(cursor):
    '''
    - API功能：修改用户信息（不包括头像和密码，被修改者userId是传入的token中携带的userId）
    - 负责人：杜宇
    - 请求参数：userName, userType, userSex, userSexPermission, userAge, userAgePermission, userFrom, userFromPermission, userContact, userContactPermission, userDescription, userImportantInfo, userImportantInfoPermission
      - `userName`: 用户姓名（字符串）
      - `userType`: 用户类型（0=患者，1=医师，2=其他人员）
      - `userSex`: 用户性别（0=男，1=女）
      - `userSexPermission`: 用户性别权限（0=公开，1=私密）
      - `userAge`: 用户年龄（整数，>=0）
      - `userAgePermission`: 用户年龄权限（0=公开，1=私密）
      - `userFrom`: 用户来源（字符串，患者用户填写城市；医师用户填写机构名称）
      - `userFromPermission`: 用户来源权限（0=公开，1=私密）
      - `userContact`: 用户联系方式（字符串，电话号码或邮箱，该项可用于登录，故不可重复）
      - `userContactPermission`: 用户联系方式权限（0=公开，1=私密）
      - `userDescription`: 用户自述（字符串）
      - `userImportantInfo`: 用户重要信息（字符串，分为患者重要信息和医师重要信息写入数据库）
      - `userImportantInfoPermission`: 用户重要信息权限（0=公开，1=私密）
    - 响应参数：code, msg
      - `code`: 0=修改成功，1=修改失败
      - `msg`: 自然语言提示信息
    '''
    user_id = get_jwt_identity()
    user_data = request.json
    user_name= user_data.get('userName')
    user_type = user_data.get('userType')
    user_sex = user_data.get('userSex')
    user_sex_permission = user_data.get('userSexPermission')
    user_age = user_data.get('userAge')
    user_age_permission = user_data.get('userAgePermission')
    user_from = user_data.get('userFrom')
    user_from_permission = user_data.get('userFromPermission')
    user_contact = user_data.get('userContact')
    user_contact_permission = user_data.get('userContactPermission')
    user_description = user_data.get('userDescription')
    user_important_info = user_data.get('userImportantInfo')
    user_important_info_permission = user_data.get('userImportantInfoPermission')
    
    if user_name is None or user_name == "" or user_sex is None or not (user_sex in {0, 1}) or user_type is None or not (user_type in {0, 1, 2}):
        return jsonify({'code': 1, 'msg': '表单数据出现严重问题。'})
    
    cursor.execute(f"SELECT * FROM userinfo WHERE userContact='{user_contact}'")
    result = cursor.fetchall()
    if not (result is None or len(result) == 0) and int(result[0]['userId']) != int(user_id):
        return jsonify({'code': 1, 'msg': '您提供的联系方式已存在，请您更换。'})
    update_query = """
    UPDATE userinfo
    SET userName='%s', userType='%s', userSex=%s, userSexPermission=%s, 
        userAge=%s, userAgePermission=%s, userFrom='%s', userFromPermission=%s, 
        userContact='%s', userContactPermission=%s, userDescription='%s', 
        doctorImportantInfo='%s', patientImportantInfo='%s', userImportantInfoPermission=%s 
    WHERE userId=%s
    """
    cursor.execute(update_query % (
    user_name, user_type, user_sex, user_sex_permission,
    user_age, user_age_permission, user_from, user_from_permission,
    user_contact, user_contact_permission, user_description,
    user_important_info, user_important_info, user_important_info_permission, user_id
    ))
    return jsonify({'code': 0, 'msg': '修改成功！'})

@app.route('/api/modifyUserAvatar', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def modify_user_avatar(cursor):
    '''
    - API功能：修改用户头像
    - 负责人：杜宇
    - 请求参数：userAvatar
      - `userAvatar`: 用户头像（`str`，带头部的图像base64字符串，经前端剪裁压缩）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=修改成功，`1`=修改失败）
      - `msg`: 自然语言提示信息（`str`）
        '''
    user_id = get_jwt_identity()
    user_data = request.json
    user_avatar = user_data.get('userAvatar')
    
    if user_avatar is None or user_avatar == "":
        return jsonify({'code': 1, 'msg': '头像数据不可读取。'})
    cursor.execute(f"SELECT userAvatarId FROM userinfo WHERE userId='{user_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '该用户不存在。'})
    old_avatar_id = result[0]['userAvatarId']
    old_img_path = os.path.abspath(os.path.join(DATA_DIR, 'avatar', (old_avatar_id + AVATAR_FORMAT)))
    
    user_avatar_id = util_uuid()
    img_path = os.path.abspath(os.path.join(DATA_DIR, 'avatar', (user_avatar_id + AVATAR_FORMAT)))
    util_base642file(user_avatar, img_path, remove_header=True)
    cursor.execute(f"UPDATE userinfo SET userAvatarId='{user_avatar_id}' WHERE userId={user_id}")
    
    if os.path.exists(old_img_path):  # 最后一步再删除旧头像，以防万一
        os.remove(old_img_path)
    else:
        info_print(f"头像图片文件不存在：{old_img_path}", level="warning")
    return jsonify({'code': 0, 'msg': '修改成功！'})
    
@app.route('/api/modifyUserPassword', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def modify_user_password(cursor):
    '''
    - API功能：修改用户密码
    - 负责人：杜宇
    - 请求参数：userOldPassword, userNewPassword
      - `userOldPassword`: 旧密码（`str`，密文，前端负责加密）
      - `userNewPassword`: 新密码（`str`，密文，前端负责加密）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=修改成功，`1`=修改失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    user_data = request.json
    user_old_password = user_data.get('userOldPassword')
    user_new_password = user_data.get('userNewPassword')
    
    if user_old_password is None or user_old_password == "" or user_new_password is None or user_new_password == "":
        return jsonify({'code': 1, 'msg': '密码不可读取。'})
    cursor.execute(f"SELECT * FROM userinfo WHERE userId='{user_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '出现未知错误。'})
    else:
        user_ciphertext = result[0]['userCiphertext']
        if not util_verify_password(user_ciphertext, user_old_password):
            return jsonify({'code': 1, 'msg': '旧密码错误。'})
        else:
            user_new_ciphertext = util_encrypt_password(user_new_password)
            cursor.execute(f"UPDATE userinfo SET userCiphertext='{user_new_ciphertext}' WHERE userId={user_id}")
            return jsonify({'code': 0, 'msg': '修改成功！'})
        
@app.route('/api/addMailItem', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def add_mail_item(cursor):
    '''
    - API功能：向用户发送留言
    - 负责人：杜宇
    - 请求参数：mailItemContent, mailItemReceiverUserId
      - `mailItemContent`: 留言内容（`str`）
      - `mailItemReceiverUserId`: 留言接收者userId（`int`）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=发送成功，`1`=发送失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    send_user_id = get_jwt_identity()
    mail_data = request.json
    mail_content = mail_data.get('mailItemContent')
    mail_receiver_id = mail_data.get('mailItemReceiverUserId')
    if mail_content is None or mail_content == "" or mail_receiver_id is None or int(mail_receiver_id) < 0:
        return jsonify({'code': 1, 'msg': '留言内容或接收者ID不可读取。'})
    mail_receiver_id = int(mail_receiver_id)
    cursor.execute(f"SELECT * FROM userinfo WHERE userId='{mail_receiver_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '留言接收者不存在。'})
    else:
        current_time = util_current_time()
        cursor.execute(f"INSERT INTO mailitem (mailItemContent, mailFromUserId, mailToUserId, mailItemStatus, mailItemSendTime) VALUES ('{mail_content}', {send_user_id}, {mail_receiver_id}, 0, {current_time})")
        return jsonify({'code': 0, 'msg': '发送成功！'})

@app.route('/api/getMailList', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_mail_list(cursor):
    '''
    - API功能：获取用户的留言列表
    - 负责人：杜宇
    - 请求参数：mode
      - `mode`: 获取模式（`int`，`0`=获取自己给别人的留言，`1`=获取别人发给自己的留言）
    - 响应参数：code, msg, mailList
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `mailList`: 留言列表（`json`，返回JSON数组，每个元素是一个`JSON`对象，包含了留言的全部信息。被删除的留言不返回）
    '''
    user_id = get_jwt_identity()
    mail_data = request.json
    mode = mail_data.get('mode')
    if mode is None or not (mode in {0, 1}):
        return jsonify({'code': 1, 'msg': '未知获取模式。'})
    if mode == 0:
        cursor.execute(f"SELECT * FROM mailitem WHERE mailFromUserId='{user_id}' AND mailItemStatus=0")
    else:
        cursor.execute(f"SELECT * FROM mailitem WHERE mailToUserId='{user_id}' AND mailItemStatus=0")
    result = cursor.fetchall()
    return jsonify({'code': 0, 'msg': '获取成功', 'mailList': result})
    
@app.route('/api/deleteMailItem', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def delete_mail_item(cursor):
    '''
    - API功能：删除用户的留言，只有自己发布的留言才有权删除。
    - 负责人：杜宇
    - 请求参数：mailItemId
      - `mailItemId`: 留言ID（`int`）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=删除成功，`1`=删除失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    mail_data = request.json
    mail_item_id = mail_data.get('mailItemId')
    if mail_item_id is None or mail_item_id < 0:
        return jsonify({'code': 1, 'msg': '留言ID不可读取。'})
    cursor.execute(f"SELECT * FROM mailitem WHERE mailItemId='{mail_item_id}'")
    result = cursor.fetchall()
    if result is None or len(result) == 0:
        return jsonify({'code': 1, 'msg': '留言不存在。'})
    else:
        cursor.execute(f"UPDATE mailitem SET mailItemStatus=1 WHERE mailItemId={mail_item_id} AND mailFromUserId={user_id}")
        return jsonify({'code': 0, 'msg': '删除成功！'})
    
    
@app.route('/api/multimodalDiagnosisSubmitTask', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def multimodal_diagnosis_submit_task(cursor):
    '''
    - API功能：提交多模态诊断任务
    - 负责人：杜宇
    - 请求参数：language, texts, imageBase64
      - `language`: 语言类型（`str`，`zh`=中文，`en`=英文）
      - `texts`: 文本数组（`list`，里面元素均为字符串）
      - `imageBase64`: 图像Base64字符串（`str`，带头部）
    - 响应参数：code, msg, taskId
      - `code`: 执行状态（`int`，`0`=提交成功，`1`=提交失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskId`: 任务ID（`str`，提交成功后消费者端生成的任务ID，是一个GUID字符串）
    '''
    task_data = request.json
    language = task_data.get('language')
    texts = task_data.get('texts')
    image_base64 = task_data.get('imageBase64')
    language = str(language).lower()
    if language not in {'zh', 'en'}:
        return jsonify({'code': 1, 'msg': '未知语言类型。'})
    if texts is None or len(texts) == 0:
        return jsonify({'code': 1, 'msg': '文本信息不可读取。'})
    if len(texts) == 1:
        return jsonify({'code': 1, 'msg': '不可以只有一个对比项。'})
    if image_base64 is None or image_base64 == "":
        return jsonify({'code': 1, 'msg': '图像信息不可读取。'})
    task_data = dict()
    task_data['texts'] = texts
    task_data['image_base64'] = image_base64
    task_data['language'] = language
    task_id = md_rpc_client.call(task_data)  # 通过MQ向多模态辅诊端提交任务
    return jsonify({'code': 0, 'msg': '提交成功！', 'taskId': task_id})


@app.route('/api/multimodalDiagnosisGetStatus', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def multimodal_diagnosis_get_status(cursor):
    '''
    - API功能：获取多模态诊断任务状态
    - 负责人：杜宇
    - 请求参数：taskId
      - `taskId`: 任务ID（`str`）
    - 响应参数：code, msg, taskStatus，taskResult
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskStatus`: 任务状态（`int`，`0`=任务完成，`1`=任务进行中，`2`=任务失败）
      - `taskResult`: 任务结果（子`JSON`，任务完成后返回）
    '''
    task_data = request.json
    task_id = task_data.get('taskId')
    if task_id is None or task_id == "":
        return jsonify({'code': 1, 'msg': '任务ID不可读取。'})
    result = md_rpc_client.get_response(task_id)  # 通过MQ获取多模态辅诊端的任务状态
    if result is None:
        return jsonify({'code': 0, 'msg': '任务进行中。', 'taskStatus': 1})
    else:
        return jsonify({'code': 0, 'msg': '任务完成', 'taskStatus': 0, 'taskResult': result})


@app.route('/api/addImportantItem', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def add_important_item(cursor):
    '''
    - API功能：向重要事项清单中添加一项诊疗事项
    - 负责人：杜宇
    - 请求参数：
      - `listItemContent`: 重要诊疗事项内容（`str`）
      - `listItemTimeMode`: 事项时间模式（`int`，`0`=一次性事项，`1`=周期性事项，`2`=无时间要求）
      - `listItemStartTime`: （一次性事项）治疗事项开始时间（`int`，以秒为单位的Unix时间戳）
      - `listItemEndTime`: （一次性事项）治疗事项结束时间（`int`，以秒为单位的Unix时间戳）
      - `listItemPriority`: 事项优先级（`int`，`0`=正常，`1`=非常重要（高优先级））
      - `listItemTimeWeek`: （周期性事项）星期数（`int`，其中`1`=星期一；···；`7`=星期日）
      - `listItemIsFinished`: 事项是否已完成（`int`，`0`=未完成，`1`=已完成）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=添加成功，`1`=添加失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    important_item_data = request.json
    list_item_content = important_item_data.get('listItemContent')
    list_item_time_mode = important_item_data.get('listItemTimeMode')
    list_item_priority = important_item_data.get('listItemPriority')
    list_item_is_finished = important_item_data.get('listItemIsFinished')
    list_item_time_week, list_item_start_time, list_item_end_time = 0, 0, 0
    if list_item_time_mode == 0:
        list_item_start_time = important_item_data.get('listItemStartTime')
        list_item_end_time = important_item_data.get('listItemEndTime')
    elif list_item_time_mode == 1:
        list_item_time_week = important_item_data.get('listItemTimeWeek')

    if list_item_content is None or list_item_content == "":
        return jsonify({'code': 1, 'msg': '重要事项内容不可读取。'})
    if list_item_time_mode is None or not (list_item_time_mode in {0, 1, 2}):
        return jsonify({'code': 1, 'msg': '未知时间模式。'})
    if list_item_priority is None or not (list_item_priority in {0, 1}):
        return jsonify({'code': 1, 'msg': '未知优先级。'})
    if list_item_is_finished is None or not (list_item_is_finished in {0, 1}):
        return jsonify({'code': 1,'msg': '未知完成状态。'})

    try:
        cursor.execute(
            f"INSERT INTO importantlist (userId, listItemContent, listItemTimeMode, listItemStartTime, listItemEndTime, listItemPriority, listItemTimeWeek, listItemStatus, listItemIsFinished) "
            f"VALUES ({user_id}, '{list_item_content}', {list_item_time_mode}, {list_item_start_time}, {list_item_end_time}, {list_item_priority}, {list_item_time_week}, {0}, {list_item_is_finished})"
        )
        return jsonify({'code': 0, 'msg': '添加成功！'})
    except Exception as e:
        return jsonify({'code': 1, 'msg': '后台数据库写入失败: ' + str(e)})


@app.route('/api/deleteImportantItem', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def delete_important_item(cursor):
    '''
    - API功能：删除诊疗事项清单中的一项诊疗事项
    - 负责人：杜宇
    - 请求参数：
      - `listItemId`: 重要事项ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=删除成功，`1`=删除失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    important_item_data = request.json
    list_item_id = important_item_data.get('listItemId')
    if list_item_id is None or list_item_id < 0:
        return jsonify({'code': 1,'msg': '重要事项ID不可读取。'})
    try:
        cursor.execute(f"UPDATE importantlist SET listItemStatus=1 WHERE userId={user_id} AND listItemId={list_item_id}")
        return jsonify({'code': 0,'msg': '删除成功！'})
    except Exception as e:
        return jsonify({'code': 1,'msg': '后台数据库写入失败:'+ str(e)})
    

@app.route('/api/getImportantList', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_important_list(cursor):
    '''
    - API功能：获取指定用户的重要事项清单
    - 负责人：杜宇
    - 请求参数：无（userId通过token读取）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `importantList`: 重要事项清单（`JSON`，返回JSON数组，每个元素是一个`JSON`对象，包含了重要事项的全部信息。被删除的事项不返回）
    '''
    user_id = get_jwt_identity()
    cursor.execute(f"SELECT * FROM importantlist WHERE userId={user_id} AND listItemStatus=0")
    result = cursor.fetchall()
    return jsonify({'code': 0,'msg': '获取成功','importantList': result})


@app.route('/api/finishImportantItem', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def finish_important_item(cursor):
    '''
    - API功能：标记完成（或未完成）重要事项清单中的一项诊疗事项
    - 负责人：杜宇
    - 请求参数：
      - `listItemId`: 诊疗事项ID（`int`）
      - `listItemIsFinished`: 是否完成（`int`，`0`=未完成，`1`=已完成）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=标记成功，`1`=标记失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    important_item_data = request.json
    list_item_id = important_item_data.get('listItemId')
    list_item_is_finished = important_item_data.get('listItemIsFinished')
    if list_item_id is None or list_item_id < 0:
        return jsonify({'code': 1,'msg': '重要事项ID不可读取。'})
    if list_item_is_finished is None or not (list_item_is_finished in {0, 1}):
        return jsonify({'code': 1,'msg': '未知完成状态。'})
    try:
        cursor.execute(f"UPDATE importantlist SET listItemIsFinished={list_item_is_finished} WHERE userId={user_id} AND listItemId={list_item_id}")
        return jsonify({'code': 0,'msg': '标记成功！'})
    except Exception as e:
        return jsonify({'code': 1,'msg': '后台数据库写入失败:'+ str(e)})
    
    
@app.route('/api/getCurrentTime', methods=['GET', 'POST'])
def get_current_time():
    '''
    - API功能：获取当前时间
    - 负责人：杜宇
    - 请求参数：无
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `currentTime`: 服务器当前时间（`int`，以秒为单位的Unix时间戳）
    '''
    current_time = util_current_time()
    return jsonify({'code': 0,'msg': '获取成功','currentTime': current_time})


@app.route('/api/llmInferenceSubmitTask', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def llm_inference_submit_task(cursor):
    '''
    - API功能：提交大语言模型(**MKTY-3B-Chat**)推理任务
    - 负责人：杜宇
    - 请求参数：prompt, context
      - `prompt`: 提示词（`str`）
      - `context`: 会话历史（`json list`，里面元素均为字典，字典包含`role`和`content`两个键，`role`为`user`或`assistant`，`content`为对话内容）
    - 响应参数：code, msg, taskId
      - `code`: 执行状态（`int`，`0`=提交成功，`1`=提交失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskId`: 任务ID（`str`，提交成功后消费者端生成的任务ID，是一个GUID字符串）
    '''
    task_data = request.json
    prompt = task_data.get('prompt')
    context = task_data.get('context')
    if prompt is None or len(prompt) == 0:
        return jsonify({'code': 1, 'msg': '提示词不可读取。'})
    if context is None or type(context) != type([]):
        return jsonify({'code': 1, 'msg': '会话历史不可读取。'})
    task_data = dict()
    task_data['prompt'] = prompt
    task_data['context'] = context
    task_id = llm_rpc_client.call(task_data)  # 通过MQ向大语言模型(MKTY-3B-Chat)推理端提交任务
    return jsonify({'code': 0,'msg': '提交成功！', 'taskId': task_id})


@app.route('/api/llmInferenceGetStatus', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def llm_inference_get_status(cursor):
    '''
    - API功能：获取大语言模型推理任务状态
    - 负责人：杜宇
    - 请求参数：taskId
      - `taskId`: 任务ID（`str`）
    - 响应参数：code, msg, taskStatus，taskResult
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskStatus`: 任务状态（`int`，`0`=任务完成，`1`=任务进行中，`2`=任务失败）
      - `taskResult`: 任务结果（子`JSON`，任务完成后返回）
    '''
    task_data = request.json
    task_id = task_data.get('taskId')
    if task_id is None or task_id == "":
        return jsonify({'code': 1, 'msg': '任务ID不可读取。'})
    result = llm_rpc_client.get_response(task_id)  # 通过MQ获取多模态辅诊端的任务状态
    if result is None:
        return jsonify({'code': 0, 'msg': '任务进行中。', 'taskStatus': 1})
    else:
        return jsonify({'code': 0, 'msg': '任务完成', 'taskStatus': 0, 'taskResult': result})
    
    
@app.route('/api/saveLlmSession', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def save_llm_session(cursor):
    '''
    - API功能：保存MKTY大语言模型会话
    - 负责人：杜宇
    - 请求参数：sessionId, sessionContent，isSessionDM
      - `sessionId`: 对话ID（`int`，规定若该字段值为`-1`，则表明建立新会话）
      - `sessionContent`: 对话内容（`json list`，规定：里面元素均为字典，字典包含`role`和`content`两个键，`role`为`user`或`assistant`，`content`为对话内容）
      - `isSessionDM`: 是否启用了LLM讨论机制（`int`，`0`=不启用，`1`=启用）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=保存成功，`1`=保存失败）
      - `msg`: 自然语言提示信息（`str`）
      - `sessionId`: 对话ID（`int`，若新建会话，则返回新会话的ID）
    '''
    session_data = request.json
    session_id = session_data.get('sessionId')
    session_content = session_data.get('sessionContent')
    is_session_dm = session_data.get('isSessionDM')
    if session_id is None:
        return jsonify({'code': 1, 'msg': '对话ID不可读取。'})
    if session_content is None or session_content == {}:
        return jsonify({'code': 1, 'msg': '对话内容不可读取。'})
    if is_session_dm is None:
        return jsonify({'code': 1, 'msg': '对话时间不可读取。'})
    if len(session_content) < 2:  # 对话内容最少1条
        return jsonify({'code': 1, 'msg': '对话过短，不可保存。'})
    user_id = get_jwt_identity()
    session_save_time = util_current_time()
    try:
        if session_id == -1:  # 新建会话
            cursor.execute(
                "INSERT INTO llmhistory (isSessionDM, sessionSaveTime, sessionUserId, sessionContent) "
                "VALUES (%s, %s, %s, %s)",
                (is_session_dm, session_save_time, user_id, json.dumps(session_content)))
            session_id = cursor.lastrowid
        else:  # 更新会话
            cursor.execute(
                "UPDATE llmhistory SET sessionContent=%s, sessionSaveTime=%s "
                "WHERE sessionId=%s AND sessionUserId=%s",
                (json.dumps(session_content), session_save_time, session_id, user_id))
        return jsonify({'code': 0, 'msg': '保存成功！', 'sessionId': session_id})
    except Exception as e:
        return jsonify({'code': 1, 'msg': '未能成功保存会话记录：'+ str(e)})
    

@app.route('/api/getLlmSession', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_llm_session(cursor):
    '''
    - API功能：获取指定ID的MKTY大语言模型会话内容
    - 负责人：杜宇
    - 请求参数：sessionId
      - `sessionId`: 会话ID（`int`）
    - 响应参数：code, msg, sessionContent
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `sessionContent`: 对话内容（`json`）
    '''
    session_data = request.json
    session_id = session_data.get('sessionId')
    if session_id is None:
        return jsonify({'code': 1,'msg': '对话ID不可读取。'})
    user_id = get_jwt_identity()
    try:
        cursor.execute(f"SELECT * FROM llmhistory WHERE sessionId={session_id} AND sessionUserId={user_id}")
        result = cursor.fetchall()
        if result is None or len(result) == 0:
            return jsonify({'code': 1,'msg': '该会话不存在或您无权读取该ID的会话内容。'})
        else:
            return jsonify({'code': 0,'msg': '获取成功','sessionContent': result[0]['sessionContent']})
    except Exception as e:
        return jsonify({'code': 1,'msg': '未能成功获取会话记录：'+ str(e)})
    

@app.route('/api/getLlmSessionList', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_llm_session_list(cursor):
    '''
    - API功能：获取指定用户的MKTY大语言模型会话列表
    - 负责人：杜宇
    - 请求参数：isSessionDM
      - `isSessionDM`: 是否启用了LLM讨论机制（`int`，`0`=不启用，`1`=启用）
    - 响应参数：code, msg, sessionList
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `sessionList`: 会话列表（`json`，返回JSON数组，每个元素是一个JSON对象，每个对象中包含：`sessionId`：会话Id、`sessionSaveTime`：会话最后一次保存时间（以秒为单位Unix时间戳，服务器时间）、`sessionTitle`：每项会话的标题，取该会话中用户第一次发言的前16余个字符。）
    '''
    session_data = request.json
    is_session_dm = session_data.get('isSessionDM')
    if is_session_dm is None:
        return jsonify({'code': 1,'msg': '对话时间不可读取。'})
    user_id = get_jwt_identity()
    try:
        cursor.execute(f"SELECT * FROM llmhistory WHERE isSessionDM={is_session_dm} AND sessionUserId={user_id}")
        result = cursor.fetchall()
        if is_session_dm == 0:
            result_return = [{'sessionId': item['sessionId'], 'sessionSaveTime': item['sessionSaveTime'], 'sessionTitle': json.loads(item['sessionContent'])[1]['content'][:16]} for item in result]
        elif is_session_dm == 1:
            result_return = [{'sessionId': item['sessionId'], 'sessionSaveTime': item['sessionSaveTime'], 'sessionTitle': json.loads(item['sessionContent'])[0][:16]} for item in result]
        return jsonify({'code': 0,'msg': '获取成功','sessionList': result_return})
    except Exception as e:
        return jsonify({'code': 1,'msg': '未能成功获取会话列表：'+ str(e)})
    

@app.route('/api/deleteLlmSession', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def delete_llm_session(cursor):
    '''
    - API功能：删除指定ID的MKTY大语言模型会话（**数据库级真删除**）
    - 负责人：杜宇
    - 请求参数：sessionId
      - `sessionId`: 会话ID（`int`）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=删除成功，`1`=删除失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    session_data = request.json
    session_id = session_data.get('sessionId')
    if session_id is None:
        return jsonify({'code': 1,'msg': '对话ID不可读取。'})
    user_id = get_jwt_identity()
    try:
        # 假删：cursor.execute(f"UPDATE llmhistory SET sessionStatus=1 WHERE sessionId={session_id} AND sessionUserId={user_id}")
        cursor.execute(f"DELETE FROM llmhistory WHERE sessionId={session_id} AND sessionUserId={user_id}")
        return jsonify({'code': 0,'msg': '删除成功！'})
    except Exception as e:
        return jsonify({'code': 1,'msg': '未能成功删除会话记录：'+ str(e)})
    

@app.route('/api/addForum', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def add_forum(cursor):
    '''
    - API功能：创建论坛（论坛列表的“增”操作）
    - 负责人：郭长霖
    - 请求参数：
      - `forumName`: 论坛名称（`str`）
      - `forumType`: 论坛类型（`int`，0=医学知识论坛，1=疾病论坛）
      - `forumPermission`: 论坛权限（`int`，0=不限人员类型，1=仅限医师创建、参与，2=仅限患者创建、参与）
    - 响应参数：
      - `code`: 响应码（0=正常执行，1=出现错误）
      - `msg`: 提示信息
      - `forumId`: 论坛ID（`int`）
      - `forumCreateTime`: 论坛创建时间（`int`）
    '''
    user_id = get_jwt_identity()
    data = request.json
    forum_name = data.get('forumName')
    forum_type = data.get('forumType')
    forum_perm = data.get('forumPermission')

    if not all([forum_name, forum_type in {0, 1}, forum_perm in {0, 1, 2}]):
        return jsonify({'code': 1, 'msg': '参数格式错误'})

    try:
        create_time = util_current_time()
        cursor.execute(
            "INSERT INTO forumsummary (forumName, forumType, forumPermission, forumCreator, forumCreateTime, forumStatus) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (forum_name, forum_type, forum_perm, user_id, create_time, 0)
        )
        forum_id = cursor.lastrowid
        return jsonify({
            'code':0,
            'msg':'创建成功',
            'forumId':forum_id,
            'forumCreateTime':create_time
        })
    except Exception as e:
        info_print(f"论坛创建失败：{str(e)}", "error")
        return jsonify({'code': 1, 'msg': '操作失败：' + str(e)})


@app.route('/api/getForumList', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_forum_list(cursor):
    '''
    - API功能：获取论坛列表（论坛列表的“查”操作）
    - 负责人：郭长霖
    - 请求参数：
      - `forumType`: 筛选类型（0=医学知识论坛；1=疾病论坛；2=所有论坛）
      - `forumPermission`: 筛选权限（0=不限人员类型；1=仅限医师创建、参与；2=仅限患者创建、参与；3=所有论坛）
    - 响应参数：
      - `code`: 响应码（`int`，0=正常执行；1=出现错误）
      - `msg`: 提示信息（`str`）
      - `forumList`: 查询结果（`JSON Array`）
    '''
    data = request.json
    f_type = data.get('forumType')
    f_perm = data.get('forumPermission')

    conditions = ["forumStatus=0"]
    params = []
    
    if f_type != 2:
        conditions.append("forumType=%s")
        params.append(f_type)
    if f_perm != 3:
        conditions.append("forumPermission=%s")
        params.append(f_perm)

    query = "SELECT * FROM forumsummary WHERE " + " AND ".join(conditions)
    
    try:
        cursor.execute(query, params)
        forums = cursor.fetchall()

        return jsonify({
            'code':0,
            'msg':'获取成功',
            'forumList':forums
        })
    except Exception as e:
        info_print(f"论坛列表查询失败：{str(e)}", "error")
        return jsonify({'code':1, 'msg':'查询失败：' + str(e)})


@app.route('/api/modifyForumType', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def modify_forum_type(cursor):
    '''
    - API功能：修改论坛类型（论坛列表的“改”操作，论坛一旦创建则不可修改权限）
    - 负责人：郭长霖
    - 请求参数：
      - `forumId`: 待修改论坛的ID（`int`）
      - `forumType`: 论坛类型代码（`int`，0=医学知识论坛；1=疾病论坛）
    - 响应参数：
      - `code`: 响应码（`int`，0=正常执行；1=出现错误）
      - `msg`: 提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    data = request.json

    forum_id = data.get('forumId')
    new_type = data.get('forumType')
    
    if forum_id is None or new_type is None:
        return jsonify({'code':1, 'msg':'缺少必要参数'})
    if not isinstance(forum_id, int):
        return jsonify({'code':1, 'msg':'forumId必须为整数'})
    if new_type not in {0, 1}:
        return jsonify({'code':1, 'msg':'无效论坛类型值'})

    try:
        cursor.execute(
            "SELECT forumCreator FROM forumsummary WHERE forumId=%s AND forumStatus=0",
            (forum_id,)
        )
        forum = cursor.fetchone()
        if not forum:
            return jsonify({'code':1, 'msg':'论坛不存在或已删除'})
        if forum['forumCreator'] != user_id:
            return jsonify({'code':1, 'msg':'只有创建者才有权修改论坛类型'}) 

        cursor.execute(
            "UPDATE forumsummary SET forumType=%s WHERE forumId=%s",
            (new_type, forum_id)
        )
        return jsonify({'code':0, 'msg':'论坛类型修改成功'})
    except Exception as e:
        info_print(f"论坛类型修改失败：{str(e)}", "error")
        return jsonify({'code':1, 'msg':'数据库操作失败：' + str(e)})


@app.route('/api/deleteForum', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def delete_forum(cursor):
    '''
    - API功能：删除论坛（论坛列表的“删”操作）
    - 负责人：郭长霖
    - 请求参数：
      - `forumId`: 待修改论坛的ID（`int`）
    - 响应参数：
      - `code`: 响应码（`int`，0=正常执行；1=出现错误）
      - `msg`: 提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    data = request.json
    
    forum_id = data.get('forumId')
    if forum_id is None:
        return jsonify({'code':1, 'msg':'缺少forumId参数'})
    if not isinstance(forum_id, int):
        return jsonify({'code':1, 'msg':'forumId必须为整数'})

    try:
        cursor.execute(
            "SELECT forumCreator FROM forumsummary WHERE forumId=%s AND forumStatus=0",
            (forum_id,)
        )
        forum = cursor.fetchone()
        if not forum:
            return jsonify({'code':1, 'msg':'论坛不存在或已删除'})
        if forum['forumCreator'] != user_id:
            return jsonify({'code':1, 'msg':'无删除权限'})

        cursor.execute(
            "UPDATE forumsummary SET forumStatus=1 WHERE forumId=%s",
            (forum_id,)
        )
        return jsonify({'code':0, 'msg':'删除成功'})
    except Exception as e:
        info_print(f"论坛删除失败：{str(e)}", "error")
        return jsonify({'code':1, 'msg':'数据库操作失败'})
    
@app.route('/api/getForumInfo', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_forum_info(cursor):
    '''
    - API功能：获取指定Id的论坛信息元数据
    - 负责人：杜宇
    - 请求参数：
      - `forumId`: 论坛ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `forumInfo`: 论坛信息元数据（`JSON`）
    '''
    user_id = get_jwt_identity()
    forum_data = request.json
    forum_id = forum_data.get('forumId')
    if forum_id is None or forum_id < 0:
        return jsonify({'code': 1,'msg': '论坛ID不可读取。'})
    try:
        cursor.execute(f"SELECT * FROM forumsummary WHERE forumId={forum_id} AND forumStatus=0")
        result = cursor.fetchall()
        if result is None or len(result) == 0:
            return jsonify({'code': 1,'msg': '该论坛不存在或您无权读取该ID的论坛内容。'})
        else:
            return jsonify({'code': 0,'msg': '获取成功','forumInfo': result[0]})
    except Exception as e:
        return jsonify({'code': 1,'msg': '未能成功获取论坛记录：'+ str(e)})

@app.route('/api/sendPost', methods=['POST'])
@jwt_required() 
@getCursor(conn_pool)
def send_post(cursor):
    '''
    - API功能：发送帖子
    - 负责人：杜宇
    - 请求参数：
      - `forumId`: 论坛ID（`int`）
      - `postContent`: 帖子内容（`str`）
      - `postImagesBase64List`: 帖子图片Base64格式数据列表（`str`，列表格式要求：每一项“元素”均为带头部的图片数据Base64字符串，字符串之间用SPLIT_CHARACTER(="$^")来隔开。**流程简要说明：** 后台拿到字符串后解析为多个base64并一律转为webp格式写入文件，最多包含3张图片，数据库中存储文件GUID，文件名为`"文件GUID".webp`，多个GUID也用`SPLIT_CHARACTER`隔开；**上传图片要求：** 拓展名仅支持`png`、`jpg`、`jpeg`、`webp`、`bmp`、`ico`、`gif`，且单个文件base64长度不可超过300KB，文件有效性不做检查）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=发送成功，`1`=发送失败）
      - `msg`: 自然语言提示信息（`str`）
      - `postId`: 帖子ID（`int`）
      - `postCreateTime`: 帖子创建时间（`int`，以秒为单位的Unix时间戳）
    '''
    SPLIT_CHARACTER = "$^"
    user_id = get_jwt_identity()
    session_data = request.json
    forum_id = session_data.get('forumId')
    post_content = session_data.get('postContent')
    post_images_base64_list_str = session_data.get('postImagesBase64List')
    if forum_id is None or forum_id < 0:
        return jsonify({'code': 1,'msg': '论坛ID不可读取。'})
    if post_content is None or post_content == "":
        return jsonify({'code': 1,'msg': '帖子内容不可读取。'})
    # 帖子可以不包含图片，故不作检查
    post_images_base64_list = post_images_base64_list_str.split(SPLIT_CHARACTER)
    if len(post_images_base64_list) > 3:
        return jsonify({'code': 1,'msg': '帖子图片数量超过限制。'})
    if not all(len(s) < 300 * 1024 for s in post_images_base64_list):
        return jsonify({'code': 1,'msg': '帖子图片大小超过限制。'})
    post_images_guid_list = []
    for image_base64 in post_images_base64_list:
        if image_base64 == "":
            continue
        image_guid = util_uuid()
        image_path = os.path.join(DATA_DIR, "post_images", (image_guid + ".webp"))
        save_base64_image(image_base64, image_path)
        post_images_guid_list.append(image_guid)
    post_images_guid_list = SPLIT_CHARACTER.join(post_images_guid_list)
    post_create_time = util_current_time()
    post_content_json = json.dumps({"content": post_content, "images": post_images_guid_list})
    try:
        cursor.execute(
            "INSERT INTO forumcontent (postForumId, postContent, postPosterId, postCreateTime, postPraiseNumber, postStatus) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (forum_id, post_content_json, user_id, post_create_time, 0, 0)
        )
        post_id = cursor.lastrowid
        return jsonify({'code': 0,'msg': '发送成功！','postId': post_id,'postCreateTime': post_create_time})
    except Exception as e:
        return jsonify({'code': 1,'msg': '后台数据库写入失败:'+ str(e)})
    

@app.route('/api/getPostList', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_post_list(cursor):
    '''
    - API功能：获取指定论坛的帖子列表（为了减轻服务端压力，该函数只返回特定论坛中包含帖子的ID列表，由前端轮询请求列表中各帖子的具体内容。）
    - 负责人：杜宇
    - 请求参数：
      - `forumId`: 论坛ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `postList`: 帖子Id列表（`JSON Array`，返回JSON数组，包含各帖子的Id。被删除的帖子不返回。）
    '''
    session_data = request.json
    forum_id = session_data.get('forumId')
    if forum_id is None or forum_id < 0:
        return jsonify({'code': 1,'msg': '论坛ID不可读取。'})
    try:
        cursor.execute(f"SELECT postId FROM forumcontent WHERE postForumId={forum_id} AND postStatus=0")
        result = cursor.fetchall()
        result = [] if result is None else [item['postId'] for item in result]
        return jsonify({'code': 0,'msg': '获取成功','postList': result})
    except Exception as e:
        return jsonify({'code': 1,'msg': '后台数据库读取失败:'+ str(e)})


@app.route('/api/getPostContent', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_post_content(cursor):
    '''
    - API功能：获取指定帖子ID的具体内容
    - 负责人：杜宇
    - 请求参数：
      - `postId`: 帖子ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `postPosterId`: 帖子发布者ID（`int`）
      - `postCreateTime`: 帖子创建时间（`int`，以秒为单位的Unix时间戳）
      - `postPraiseNumber`: 帖子点赞数（`int`）
      - `postContent`: 帖子内容（`JSON`，键`content`的值为帖子文本，键`images`值为JSON数组，里面均为带头部的图像Base64字符串。）
    '''
    SPLIT_CHARACTER = "$^"
    session_data = request.json
    post_id = session_data.get('postId')
    if post_id is None or post_id < 0:
        return jsonify({'code': 1,'msg': '帖子ID不可读取。'})
    try:
        cursor.execute("SELECT * FROM forumcontent WHERE postId=%s AND postStatus=0", (post_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            return jsonify({'code': 1,'msg': '该帖子不存在或已被删除。'})
        else:
            post_poster_id = result[0]['postPosterId']
            post_create_time = result[0]['postCreateTime']
            post_praise_number = result[0]['postPraiseNumber']
            post_id = result[0]['postId']
            post_content = result[0]['postContent']
            post_content = json.loads(post_content)
            post_images_guid_list = post_content['images'].split(SPLIT_CHARACTER)
            post_images_base64_list = []
            for image_guid in post_images_guid_list:
                if image_guid == "":
                    continue
                image_path = os.path.join(DATA_DIR, "post_images", (image_guid + ".webp"))
                if os.path.exists(image_path):
                    post_images_base64_list.append(util_file2base64(image_path, add_header=True))
            content = post_content['content']
            return jsonify({'code': 0,'msg': '获取成功','postContent': {'content': content,'images': post_images_base64_list}, 'postPosterId': post_poster_id,'postCreateTime': post_create_time,'postPraiseNumber': post_praise_number, 'postId': post_id})
    except Exception as e:
        return jsonify({'code': 1,'msg': '数据库读取失败:'+ str(e)})
    

@app.route('/api/deletePost', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def delete_post(cursor):
    '''
    - API功能：删除指定ID的帖子（数据库级假删除，但帖子中包含的图片文件为真删除，只有帖子发布者自己有权删除）
    - 负责人：杜宇
    - 请求参数：
      - `postId`: 帖子ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=删除成功，`1`=删除失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    SPLIT_CHARACTER = "$^"
    session_data = request.json
    post_id = session_data.get('postId')
    user_id = get_jwt_identity()
    if post_id is None or post_id < 0:
        return jsonify({'code': 1,'msg': '帖子ID不可读取。'})
    try:
        cursor.execute(f"SELECT * FROM forumcontent WHERE postId={post_id} AND postStatus=0 AND postPosterId={user_id}")
        result = cursor.fetchall()
        if len(result) == 0:
            return jsonify({'code': 1,'msg': '该帖子不存在或已被删除或您无权删除。'})
        else:
            post_content = result[0]['postContent']
            post_content = json.loads(post_content)
            post_images_guid_list = post_content['images'].split(SPLIT_CHARACTER)
            for image_guid in post_images_guid_list:
                if image_guid == "":
                    continue
                image_path = os.path.join(DATA_DIR, "post_images", (image_guid + ".webp"))
                if os.path.exists(image_path):
                    os.remove(image_path)
            cursor.execute(f"UPDATE forumcontent SET postStatus=1 WHERE postId={post_id} AND postPosterId={user_id}")
            return jsonify({'code': 0,'msg': '删除成功！'})
    except Exception as e:
        return jsonify({'code': 1,'msg': '数据库修改失败:'+ str(e)})


@app.route('/api/praisePost', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def praise_post(cursor):
    '''
    - API功能：给指定ID的帖子点赞（因时间关系，暂不考虑防刷赞等的情况）
    - 负责人：杜宇
    - 请求参数：
      - `postId`: 帖子ID（`int`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=点赞成功，`1`=点赞失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    session_data = request.json
    post_id = session_data.get('postId')
    if post_id is None or post_id < 0:
        return jsonify({'code': 1,'msg': '帖子ID不可读取。'})
    try:
        cursor.execute(f"SELECT * FROM forumcontent WHERE postId={post_id} AND postStatus=0")
        result = cursor.fetchall()
        if len(result) == 0:
            return jsonify({'code': 1,'msg': '该帖子不存在或已被删除。'})
        else:
            cursor.execute(f"UPDATE forumcontent SET postPraiseNumber=postPraiseNumber+1 WHERE postId={post_id}")
            return jsonify({'code': 0,'msg': '点赞成功！'})
    except Exception as e:
        return jsonify({'code': 1,'msg': '数据库修改失败:'+ str(e)})
    
    
@app.route('/api/exportChatToPDF', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def export_chat2pdf(cursor):
    '''
    - API功能：导出指定会话ID的聊天记录为PDF文件。
    - 负责人：杜宇
    - 请求参数：
      - `sessionId`: 会话ID（`int`）
    - 响应参数：
      - `None`，直接发送PDF文件二进制数据，供客户端下载。
    '''
    user_id = get_jwt_identity()
    session_data = request.json
    session_id = session_data.get('sessionId')
    cursor.execute("SELECT * FROM llmhistory WHERE sessionId=%s AND sessionUserId=%s", (session_id, user_id))
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM userinfo WHERE userId=%s", (user_id,))
    result_user_info = cursor.fetchall()
    if len(result) == 0:
        return jsonify({'code': 1,'msg': '会话不存在或您无权导出该ID会话内容。'})
    elif len(result_user_info) == 0:
        return jsonify({'code': 1,'msg': '读取用户信息意外错误。'})
    else:
        session_content = result[0]['sessionContent']
        session_content = json.loads(session_content)
        is_session_dm = result[0]['isSessionDM']  # 0=普通会话，1=LLM研讨机制
        username = result_user_info[0]['userName']
        if is_session_dm == 0:
            pdf_file_io_stream, pdf_filename = export_chat_to_pdf(username, session_content)
        else:
            pass
        return send_file(pdf_file_io_stream, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')


@app.route('/api/sendEmail', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def send_email_request(cursor):
    '''
    - API功能：发送指定内容到指定邮箱。暂未考虑防攻击措施。
    - 负责人：杜宇
    - 请求参数：
      - `content`: 邮件文本内容（`str`，可以是纯文本，也可以是`HTML`）
      - `receiver`: 收件人邮箱地址（`str`）
      - `subject`: 邮件标题（`str`）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=发送成功，`1`=发送失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    user_id = get_jwt_identity()
    session_data = request.json
    content = session_data.get('content')
    receiver = session_data.get('receiver')
    subject = session_data.get('subject')
    username = "明康慧医用户" + str(user_id)
    if content is None or content == "":
        return jsonify({'code': 1, 'msg': '邮件内容不可为空'})
    if receiver is None or receiver == "":
        return jsonify({'code': 1, 'msg': '收件人邮箱地址不可为空'})
    cursor.execute("SELECT * FROM userinfo WHERE userId=%s", (user_id,))
    result_user_info = cursor.fetchall()
    if len(result_user_info) == 0:
        return jsonify({'code': 1, 'msg': '读取用户信息意外错误。'})
    else:
        username = result_user_info[0]['userName']
    result = send_email(
    sender_email=EMAIL_SENDER,
    sender_name="明康慧医用户：" + str(username),
    recipient_email=receiver,
    subject="【明康慧医】" + str(subject),
    message_body=str(content),
    smtp_server=EMAIL_SENDER_SMTP_SERVER,
    smtp_port=EMAIL_SENDER_SMTP_PORT,
    password=EMAIL_SENDER_AUTHORIZATION
    )
    if result:
        return jsonify({'code': 0, 'msg': '发送成功！'})
    else:
        return jsonify({'code': 1, 'msg': '发送失败！'})


@app.route('/api/tsbbModelSubmitTask', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def tsbb_model_submit_task(cursor):
    '''
    - API功能：医学时间序列预测模型和BigBird模型推理任务提交（大模型讨论判敛和时序预测均通过此接口提交推理任务）
    - 负责人：杜宇
    - 请求参数：
      - `taskType`: 任务类型（`int`，0=医学时间序列预测，1=BigBird模型推理）
      - `taskLanguage`: 任务自然语言类型（`str`，仅支持中英文，`zh`=中文，`en`=英文）
      - `taskData`: 任务数据（`any`，当`taskType`为0时，其为JSON，键为“timeSeries”（时间序列浮点数数组）和“text”（医学文本字符串）；当`taskType`为1时，其为数组，元素为待推理文本字符串）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=提交成功，`1`=提交失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskId`: 任务ID（`str`，是一个GUID字符串）
    '''
    user_id = get_jwt_identity()
    session_data = request.json
    task_type = session_data.get('taskType')
    task_language = session_data.get('taskLanguage')
    task_data = session_data.get('taskData')
    if task_type is None:
        return jsonify({'code': 1, 'msg': '任务类型不可为空'})
    if task_type not in [0, 1]:
        return jsonify({'code': 1, 'msg': '任务类型参数不可读取'})
    if task_language not in ['zh', 'en']:
        return jsonify({'code': 1, 'msg': '任务语言参数不可读取'})
    task_submit_data = {
        "taskType": task_type,
        "taskLanguage": task_language
    }
    try:
        if task_type == 0:
            time_series = task_data.get("timeSeries")
            text = task_data.get("text")
            time_series = map(lambda x: float(x) if not math.isnan(x) else 0.0, time_series)
            task_submit_data["timeSeries"] = list(time_series)
            task_submit_data["text"] = text
        elif task_type == 1:
            texts_list = list(map(str, task_data))
            task_submit_data["textsList"] = texts_list
        task_id = tsbb_rpc_client.call(task_submit_data)
        return jsonify({'code': 0, 'msg': '任务提交成功！', 'taskId': task_id})
    except Exception as e:
        return jsonify({'code': 1, 'msg': '任务提交失败:'+ str(e)})


@app.route('/api/tsbbInferenceGetStatus', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def tsbb_inference_get_status(cursor):
    '''
    - API功能：获取指定任务的推理结果
    - 负责人：杜宇
    - 请求参数：
      - `taskId`: 任务ID（`str`，GUID字符串）
    - 响应参数：
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `taskStatus`: 任务状态（`int`，`0`=任务完成，`1`=任务进行中，`2`=任务失败）
      - `taskResult`: 任务结果（`any`，具体结构视任务类型而定）
    '''
    user_id = get_jwt_identity()
    session_data = request.json
    task_id = session_data.get('taskId')
    if task_id is None or task_id == "":
        return jsonify({'code': 1, 'msg': '任务ID不可读取'})
    try:
        result = tsbb_rpc_client.get_response(task_id)
        if result is None:
            return jsonify({'code': 0, 'msg': '任务正在进行', 'taskStatus': 1})
        else:
            task_type = result.get("taskType")
            if task_type == 0:
                pass
            elif task_type == 1:
                avg_similarity = average_cosine_similarity(result.get("data", []))
                return jsonify({'code': 0, 'msg': '获取成功！', 'taskResult': avg_similarity, 'taskStatus': 0})
    except Exception as e:
        return jsonify({'code': 1, 'msg': '获取失败：' + str(e), 'taskStatus': 2})


@app.route('/api/knowledge/create', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def create_knowledge_entity(cursor):
    '''
    - API功能：创建知识实体
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 请求参数：
      - `keName`（`str`，知识实体名称）
      - `keAbstract`（`str`，知识实体摘要）
      - `fileContent`（`str`，文件内容，base64编码）
      - `fileType`（`str`，文件类型）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
      - `keGUID`（`str`，知识实体唯一标识符）
    '''
    user_id = get_jwt_identity()
    data = request.json
        
    # 获取请求参数
    ke_name = data.get('keName')
    ke_abstract = data.get('keAbstract', '')
    file_content = data.get('fileContent')  # base64编码的文件内容
    file_type = data.get('fileType')  # 文件MIME类型
        
    if not ke_name or not file_content or not file_type:
        return jsonify({'code': 1, 'msg': '参数不完整'})
        
    # 生成GUID
    ke_guid = util_uuid()
        
    # 创建知识实体目录
    knowledge_dir = os.path.join(DATA_DIR, 'knowledge')
    if not os.path.exists(knowledge_dir):
        os.makedirs(knowledge_dir)
        
    entity_dir = os.path.join(knowledge_dir, ke_guid)
    os.makedirs(entity_dir)
        
    # 保存文件
    file_path = os.path.join(entity_dir, 'file')
    util_base642file(file_content, file_path)
        
    # 提取文本内容
    extension_map = {
        'text/plain': '.txt',
        'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
        'application/vnd.ms-powerpoint': '.ppt'
    }
    ext_file = extension_map.get(file_type, '')
    text_content = extract_text_from_file(file_path, ext_file)

    # 切分文本
    pieces = split_text_into_pieces(text_content, KE_PIECE_LENGTH)
        
    # 创建pieces目录并保存片段
    pieces_dir = os.path.join(entity_dir, 'pieces')
    os.makedirs(pieces_dir)
        
    for i, piece in enumerate(pieces):
        piece_path = os.path.join(pieces_dir, str(i))
        with open(piece_path, 'w', encoding='utf-8') as f:
            f.write(piece)
        # 计算TF-IDF特征
    if pieces:
        features, vectorizer = compute_tfidf_features(pieces)
            
        # 保存特征矩阵
        feature_path = os.path.join(entity_dir, 'feature.npy')
        np.save(feature_path, features)
            
        # 保存向量化器
        if vectorizer is not None:
            vectorizer_path = os.path.join(entity_dir, 'vectorizer.pkl')
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(vectorizer, f)
        
    # 写入数据库
    current_time = str(util_current_time())
    insert_sql = """
    INSERT INTO knowledgeentity (keGUID, keFileType, keName, keCreateTime, keAbstract) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_sql, (ke_guid, file_type, ke_name, current_time, ke_abstract))
    
    return jsonify({'code': 0, 'msg': '知识实体创建成功', 'keGUID': ke_guid})
        


@app.route('/api/knowledge/search', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def search_knowledge_entities(cursor):
    '''
    - API功能：搜索知识实体
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 请求参数：
      - `keyword`（`str`，搜索关键词）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
      - `entities`（`list`，搜索到的知识实体列表）
    '''
    try:
        data = request.json
        keyword = data.get('keyword')


        if keyword:
            # 搜索包含关键词的实体
            search_sql = """
            SELECT keId, keGUID, keFileType, keName, keCreateTime, keAbstract 
            FROM knowledgeentity 
            WHERE keName LIKE %s
            ORDER BY keCreateTime DESC
            """
            cursor.execute(search_sql, (f'%{keyword}%',))
        else:
            # 获取所有实体
            search_sql = """
            SELECT keId, keGUID, keFileType, keName, keCreateTime, keAbstract 
            FROM knowledgeentity 
            ORDER BY keCreateTime DESC
            """
            cursor.execute(search_sql)

        results = cursor.fetchall()
        entities = []
        
        for row in results:
            entities.append({
                'keId': row['keId'],
                'keGUID': row['keGUID'],
                'keFileType': row['keFileType'],
                'keName': row['keName'],
                'keCreateTime': row['keCreateTime'],
                'keAbstract': row['keAbstract']
            })
        return jsonify({'code': 0, 'msg': '搜索成功', 'entities': entities})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '搜索失败：' + str(e)})


@app.route('/api/knowledge/download/<int:ke_id>', methods=['GET', 'POST'])
@getCursor(conn_pool)
def download_knowledge_entity(cursor, ke_id):
    '''
    - API功能：下载知识实体文件，公开资料无需登录即可下载
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 请求参数：
      - `ke_id`（`int`，知识实体ID）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
      - `file`（`file`，下载的文件（触发浏览器直接下载））
    '''
    try:
        # 获取实体信息
        query_sql = "SELECT keGUID, keName, keFileType FROM knowledgeentity WHERE keId = %s"
        cursor.execute(query_sql, (ke_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'code': 1, 'msg': '知识实体不存在'})

        ke_guid, ke_name, ke_file_type = result['keGUID'], result['keName'], result['keFileType']

        # 构建文件路径
        file_path = os.path.join(DATA_DIR, 'knowledge', ke_guid, 'file')
        info_print(file_path)
        
        if not os.path.exists(file_path):
            return jsonify({'code': 1, 'msg': '文件不存在'})
        
        # 根据文件类型确定扩展名
        extension_map = {
            'text/plain': '.txt',
            'application/pdf': '.pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'application/vnd.ms-powerpoint': '.ppt'
        }
        
        extension = extension_map.get(ke_file_type, '')
        download_name = f"{ke_name}{extension}"
        
        return send_file(file_path, as_attachment=True, download_name=download_name)
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '下载失败：' + str(e)})


@app.route('/api/knowledge/favorite', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def favorite_knowledge_entity(cursor):
    '''
    - API功能：收藏知识实体
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 请求参数：
      - `keId`（`int`，知识实体ID）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
    '''
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        ke_id = data.get('keId')
        
        if not ke_id:
            return jsonify({'code': 1, 'msg': '参数不完整'})
        
        # 检查是否已收藏
        check_sql = "SELECT recId FROM usercollectionke WHERE userId = %s AND keId = %s"
        cursor.execute(check_sql, (user_id, ke_id))
        
        if cursor.fetchone():
            return jsonify({'code': 1, 'msg': '已经收藏过该知识实体'})
        
        # 添加收藏
        insert_sql = "INSERT INTO usercollectionke (userId, keId) VALUES (%s, %s)"
        cursor.execute(insert_sql, (user_id, ke_id))
        
        return jsonify({'code': 0, 'msg': '收藏成功'})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '收藏失败：' + str(e)})


@app.route('/api/knowledge/favorites', methods=['GET'])
@jwt_required()
@getCursor(conn_pool)
def get_user_favorites(cursor):
    '''
    - API功能：获取用户收藏的知识实体
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 请求参数：
      - `userId`（`int`，用户ID）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
      - `favorites`（`list`，用户收藏的知识实体列表）
    '''
    try:
        user_id = get_jwt_identity()
        
        # 获取用户收藏的知识实体
        query_sql = """
        SELECT ke.keId, ke.keGUID, ke.keFileType, ke.keName, ke.keCreateTime, ke.keAbstract
        FROM usercollectionke uc
        JOIN knowledgeentity ke ON uc.keId = ke.keId
        WHERE uc.userId = %s
        ORDER BY uc.recId DESC
        """
        cursor.execute(query_sql, (user_id,))
        results = cursor.fetchall()
        
        favorites = []
        for row in results:
            favorites.append({
                'keId': row['keId'],
                'keGUID': row['keGUID'],
                'keFileType': row['keFileType'],
                'keName': row['keName'],
                'keCreateTime': row['keCreateTime'],
                'keAbstract': row['keAbstract']
            })
        
        return jsonify({'code': 0, 'msg': '获取成功', 'favorites': favorites})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '获取失败：' + str(e)})


@app.route('/api/knowledge/search_pieces', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def search_knowledge_pieces(cursor):
    '''
    - API功能：使用搜索算法搜索知识实体片段
    - 负责人：杜宇（与Copilot人机协作编辑）
    - 输入参数：
      - `keId`（`int`，知识实体ID）
      - `queryText`（`str`，查询文本）
      - `topK`（`int`，返回前K个结果，默认为3）
    - 响应参数：
      - `code`（`int`，响应状态，`0`=成功，`1`=失败）
      - `msg`（`str`，提示信息）
      - `results`（`list`，搜索结果列表）
    '''
    try:
        data = request.get_json()
        ke_id = data.get('keId')
        query_text = data.get('queryText')
        top_k = data.get('topK', 3)
        
        if not ke_id or not query_text:
            return jsonify({'code': 1, 'msg': '参数不完整'})
        
        # 获取知识实体GUID
        query_sql = "SELECT keGUID FROM knowledgeentity WHERE keId = %s"
        cursor.execute(query_sql, (ke_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'code': 1, 'msg': '知识实体不存在'})
        
        ke_guid = result['keGUID']
          # 构建实体目录路径
        entity_dir = os.path.join(DATA_DIR, 'knowledge', ke_guid)
        feature_path = os.path.join(entity_dir, 'feature.npy')
        vectorizer_path = os.path.join(entity_dir, 'vectorizer.pkl')
        pieces_dir = os.path.join(entity_dir, 'pieces')
        
        if not os.path.exists(feature_path) or not os.path.exists(vectorizer_path) or not os.path.exists(pieces_dir):
            return jsonify({'code': 1, 'msg': '知识实体数据不完整'})
        
        # 加载TF-IDF特征
        features = np.load(feature_path)
        
        # 加载向量化器
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        # 加载文本片段（用于返回内容）
        pieces = []
        piece_files = sorted([f for f in os.listdir(pieces_dir) if f.isdigit()], key=int)
        
        for piece_file in piece_files:
            piece_path = os.path.join(pieces_dir, piece_file)
            with open(piece_path, 'r', encoding='utf-8') as f:
                pieces.append(f.read())
        
        # 搜索相似片段
        search_results = search_similar_pieces(query_text, features, vectorizer, top_k)
        
        # 添加片段内容到结果中
        results = []
        for result in search_results:
            piece_index = result['piece_index']
            if piece_index < len(pieces):
                results.append({
                    'piece_index': piece_index,
                    'content': pieces[piece_index],
                    'similarity': result['similarity']
                })
        
        return jsonify({'code': 0, 'msg': '搜索成功', 'results': results})

    except Exception as e:
        return jsonify({'code': 1, 'msg': '搜索失败：' + str(e)})


# 病历管理相关API
@app.route('/api/getMedicalRecords', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_medical_records(cursor):
    '''
    - API功能：获取用户相关的病历列表
    - 负责人：杜宇
    - 请求参数：无
    - 响应参数：code, msg, medicalRecords
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `medicalRecords`: 病历列表（`list`，包含病历信息）
    '''
    try:
        user_id = get_jwt_identity()
        
        # 获取用户类型
        cursor.execute(f"SELECT userType FROM userinfo WHERE userId='{user_id}'")
        user_result = cursor.fetchall()
        if not user_result:
            return jsonify({'code': 1, 'msg': '用户不存在'})
        
        user_type = int(user_result[0]['userType'])
        
        # 根据用户类型获取相应的病历
        if user_type == 1:  # 医师
            cursor.execute(f"SELECT * FROM medicalrecord WHERE medrecDoctorId='{user_id}' ORDER BY medrecCreateTime DESC")
        else:  # 患者
            cursor.execute(f"SELECT * FROM medicalrecord WHERE medrecPatientId='{user_id}' ORDER BY medrecCreateTime DESC")
        
        records = cursor.fetchall()
        
        # 获取每个病历的相关用户信息
        medical_records = []
        for record in records:
            # 获取患者信息
            cursor.execute(f"SELECT userName FROM userinfo WHERE userId='{record['medrecPatientId']}'")
            patient_info = cursor.fetchone()
            patient_name = patient_info['userName'] if patient_info else '未知患者'
            
            # 获取医师信息
            cursor.execute(f"SELECT userName FROM userinfo WHERE userId='{record['medrecDoctorId']}'")
            doctor_info = cursor.fetchone()
            doctor_name = doctor_info['userName'] if doctor_info else '未知医师'
            
            medical_records.append({
                'medrecId': record['medrecId'],
                'medrecCreateTime': record['medrecCreateTime'],
                'medrecModifyTime': record['medrecModifyTime'],
                'medrecPatientId': record['medrecPatientId'],
                'medrecDoctorId': record['medrecDoctorId'],
                'medrecAbstract': record['medrecAbstract'],
                'medrecState': record['medrecState'],
                'patientName': patient_name,
                'doctorName': doctor_name
            })
        
        return jsonify({'code': 0, 'msg': '获取成功', 'medicalRecords': medical_records})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '获取失败：' + str(e)})


@app.route('/api/getMedicalRecord', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def get_medical_record(cursor):
    '''
    - API功能：获取指定病历详情
    - 负责人：杜宇
    - 请求参数：medrecId
      - `medrecId`: 病历ID（`int`）
    - 响应参数：code, msg, medicalRecord
      - `code`: 执行状态（`int`，`0`=获取成功，`1`=获取失败）
      - `msg`: 自然语言提示信息（`str`）
      - `medicalRecord`: 病历详情（`dict`）
    '''
    try:
        user_id = get_jwt_identity()
        user_data = request.json
        medrec_id = user_data.get('medrecId')
        
        if medrec_id is None:
            return jsonify({'code': 1, 'msg': '病历ID不可读取'})
        
        # 获取病历信息
        cursor.execute(f"SELECT * FROM medicalrecord WHERE medrecId='{medrec_id}'")
        record = cursor.fetchone()
        
        if not record:
            return jsonify({'code': 1, 'msg': '病历不存在'})
          # 检查权限：只有患者本人和负责医师可以查看
        if user_id != record['medrecPatientId'] and user_id != record['medrecDoctorId']:
            return jsonify({'code': 2, 'msg': '您无权查看此病历'})
        
        # 获取患者信息
        cursor.execute(f"SELECT userName FROM userinfo WHERE userId='{record['medrecPatientId']}'")
        patient_info = cursor.fetchone()
        patient_name = patient_info['userName'] if patient_info else '未知患者'
        
        # 获取医师信息
        cursor.execute(f"SELECT userName FROM userinfo WHERE userId='{record['medrecDoctorId']}'")
        doctor_info = cursor.fetchone()
        doctor_name = doctor_info['userName'] if doctor_info else '未知医师'
        
        medical_record = {
            'medrecId': record['medrecId'],
            'medrecCreateTime': record['medrecCreateTime'],
            'medrecModifyTime': record['medrecModifyTime'],
            'medrecPatientId': record['medrecPatientId'],
            'medrecDoctorId': record['medrecDoctorId'],
            'medrecAbstract': record['medrecAbstract'],
            'medrecState': record['medrecState'],
            'medrecContent': record['medrecContent'],
            'patientName': patient_name,
            'doctorName': doctor_name
        }
        
        return jsonify({'code': 0, 'msg': '获取成功', 'medicalRecord': medical_record})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '获取失败：' + str(e)})


@app.route('/api/createMedicalRecord', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def create_medical_record(cursor):
    '''
    - API功能：创建病历（仅医师可用）
    - 负责人：杜宇
    - 请求参数：medrecPatientId, medrecAbstract, medrecState, medrecContent
      - `medrecPatientId`: 患者ID（`int`）
      - `medrecAbstract`: 病历概要（`str`）
      - `medrecState`: 病历状态（`str`）
      - `medrecContent`: 病历内容（`str`，Markdown格式）
    - 响应参数：code, msg, medrecId
      - `code`: 执行状态（`int`，`0`=创建成功，`1`=创建失败）
      - `msg`: 自然语言提示信息（`str`）
      - `medrecId`: 新创建的病历ID（`int`）
    '''
    try:
        user_id = get_jwt_identity()
        user_data = request.json
        
        # 检查用户是否为医师
        cursor.execute(f"SELECT userType FROM userinfo WHERE userId='{user_id}'")
        user_result = cursor.fetchone()
        if not user_result or int(user_result['userType']) != 1:
            return jsonify({'code': 1, 'msg': '只有医师可以创建病历'})
        
        medrec_patient_id = user_data.get('medrecPatientId')
        medrec_abstract = user_data.get('medrecAbstract')
        medrec_state = user_data.get('medrecState')
        medrec_content = user_data.get('medrecContent')
        
        if not all([medrec_patient_id, medrec_abstract, medrec_state, medrec_content]):
            return jsonify({'code': 1, 'msg': '请填写完整的病历信息'})
        
        # 检查患者是否存在
        cursor.execute(f"SELECT userId FROM userinfo WHERE userId='{medrec_patient_id}' AND userType='0'")
        patient_result = cursor.fetchone()
        if not patient_result:
            return jsonify({'code': 1, 'msg': '指定的患者不存在'})
        
        create_time = util_current_time()
        
        # 插入新病历
        cursor.execute(f"""
            INSERT INTO medicalrecord (medrecCreateTime, medrecModifyTime, medrecPatientId, medrecDoctorId, medrecAbstract, medrecState, medrecContent)
            VALUES ('{create_time}', '{create_time}', '{medrec_patient_id}', '{user_id}', '{medrec_abstract}', '{medrec_state}', '{medrec_content}')
        """)
        
        # 获取新创建的病历ID
        cursor.execute("SELECT LAST_INSERT_ID() as medrecId")
        result = cursor.fetchone()
        medrec_id = result['medrecId']
        
        return jsonify({'code': 0, 'msg': '病历创建成功', 'medrecId': medrec_id})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '创建失败：' + str(e)})


@app.route('/api/updateMedicalRecord', methods=['POST'])
@jwt_required()
@getCursor(conn_pool)
def update_medical_record(cursor):
    '''
    - API功能：更新病历（仅负责医师可用）
    - 负责人：杜宇
    - 请求参数：medrecId, medrecAbstract, medrecState, medrecContent
      - `medrecId`: 病历ID（`int`）
      - `medrecAbstract`: 病历概要（`str`）
      - `medrecState`: 病历状态（`str`）
      - `medrecContent`: 病历内容（`str`，Markdown格式）
    - 响应参数：code, msg
      - `code`: 执行状态（`int`，`0`=更新成功，`1`=更新失败）
      - `msg`: 自然语言提示信息（`str`）
    '''
    try:
        user_id = get_jwt_identity()
        user_data = request.json
        
        medrec_id = user_data.get('medrecId')
        medrec_abstract = user_data.get('medrecAbstract')
        medrec_state = user_data.get('medrecState')
        medrec_content = user_data.get('medrecContent')
        
        if not all([medrec_id, medrec_abstract, medrec_state, medrec_content]):
            return jsonify({'code': 1, 'msg': '请填写完整的病历信息'})
        
        # 检查病历是否存在以及权限
        cursor.execute(f"SELECT medrecDoctorId FROM medicalrecord WHERE medrecId='{medrec_id}'")
        record_result = cursor.fetchone()
        if not record_result:
            return jsonify({'code': 1, 'msg': '病历不存在'})
        
        if user_id != record_result['medrecDoctorId']:
            return jsonify({'code': 1, 'msg': '只有负责医师可以修改病历'})
        
        modify_time = util_current_time()
        
        # 更新病历
        cursor.execute(f"UPDATE medicalrecord SET medrecModifyTime='{modify_time}', medrecAbstract='{medrec_abstract}', medrecState='{medrec_state}', medrecContent='{medrec_content}' WHERE medrecId='{medrec_id}' ")
        
        return jsonify({'code': 0, 'msg': '病历更新成功'})
        
    except Exception as e:
        return jsonify({'code': 1, 'msg': '更新失败：' + str(e)})


if __name__ == '__main__':
    info_print(f"正在启动后端服务(Port:{PORT};Host:{HOST})")
    if MODE == 'prod':
        info_print("运行模式：生产环境")
        http_server = WSGIServer((HOST, PORT), app)
        http_server.serve_forever()
    else:
        info_print("运行模式：开发环境，有性能损耗", level="warning")
        app.run(debug=True, port=PORT, host=HOST)
    
