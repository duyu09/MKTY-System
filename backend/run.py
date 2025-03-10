'''
- 文件描述：明康慧医MKTY智慧医疗系统后端服务
- 负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：run.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from util import util_file2base64, util_base642file, util_uuid, util_current_time, info_print, start_print, getDataBaseConnectionPool, getCursor
from util import util_encrypt_password, util_verify_password, RpcClient
from gevent.pywsgi import WSGIServer

# 全局变量配置
MODE = 'dev'  # 运行模式（dev=开发模式，prod=生产模式）
DATA_DIR = r'./data/'  # 数据文件夹
AVATAR_FORMAT = '.webp'  # 头像文件格式
VERSION = 'v1.1.0'  # 版本号
PORT = 5000  # 后端服务端口
HOST = '0.0.0.0'  # 后端服务主机地址
STRONG_PASSWORD = 'DUYU09'  # 强密码，用于加密token
MD_MQ_CONNECTION_PARAMETERS = {  # 多模态辅诊端MQ连接参数
    'host': 'localhost',
    'port': 5672,
    'heartbeat': 0
}
MD_QUEUE_NAME = 'modest_model_inference'  # 多模态辅诊端MQ队列名称

# 程序启动，首先打印必要信息
start_print(VERSION)
info_print("正在初始化后端服务")

# 建立数据库连接池
conn_pool = getDataBaseConnectionPool(host='localhost', user='root', password='', database='mkty_02', pool_size=5, pool_name="mkty")

# 通过MQ与多模态智能辅诊端建立连接
md_rpc_client = RpcClient(MD_MQ_CONNECTION_PARAMETERS, MD_QUEUE_NAME)


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
    - 请求参数：
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
    



if __name__ == '__main__':
    info_print(f"正在启动后端服务(Port:{PORT};Host:{HOST})")
    if MODE == 'prod':
        info_print("运行模式：生产环境")
        http_server = WSGIServer((HOST, PORT), app)
        http_server.serve_forever()
    else:
        info_print("运行模式：开发环境，有性能损耗", level="warning")
        app.run(debug=True, port=PORT, host=HOST)
    
