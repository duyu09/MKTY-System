'''
- 文件描述：明康慧医MKTY智慧医疗系统后台管理系统后端服务
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：app.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot辅助编写，人机合作完成。
'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import jwt
import time

app = Flask(__name__)

# 管理员账号配置
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
JWT_SECRET = "your-secret-key"  # 用于JWT加密的密钥

# 配置CORS
# CORS(app, resources={
#     r"/*": {
#         "origins": ["http://localhost:8080"],
#         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization"],
#         "supports_credentials": True
#     }
# })
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mkty_02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 用户信息模型
class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    userId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    userCiphertext = db.Column(db.Text, nullable=False)
    userName = db.Column(db.Text, nullable=False)
    userType = db.Column(db.Text, nullable=False)
    userSex = db.Column(db.Boolean, nullable=False)
    userSexPermission = db.Column(db.Boolean, nullable=False)
    userAge = db.Column(db.Text, nullable=False)
    userAgePermission = db.Column(db.Boolean, nullable=False)
    userFrom = db.Column(db.Text, nullable=False)
    userFromPermission = db.Column(db.Boolean, nullable=False)
    userContact = db.Column(db.Text, nullable=False)
    userContactPermission = db.Column(db.Boolean, nullable=False)
    userDescription = db.Column(db.Text)
    patientImportantInfo = db.Column(db.Text)
    doctorImportantInfo = db.Column(db.Text)
    userImportantInfoPermission = db.Column(db.Boolean, nullable=False)
    userAvatarId = db.Column(db.Text)
    userRegisterTime = db.Column(db.BigInteger, nullable=False)

# 病历模型
class MedicalRecord(db.Model):
    __tablename__ = 'medicalrecord'
    medrecId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    medrecCreateTime = db.Column(db.Text, nullable=False)
    medrecModifyTime = db.Column(db.Text, nullable=False)
    medrecPatientId = db.Column(db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    medrecDoctorId = db.Column(db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    medrecAbstract = db.Column(db.Text)
    medrecState = db.Column(db.Text, nullable=False)
    medrecContent = db.Column(db.Text, nullable=False)

    patient = db.relationship('UserInfo', foreign_keys=[medrecPatientId])
    doctor = db.relationship('UserInfo', foreign_keys=[medrecDoctorId])

# 知识实体模型
class KnowledgeEntity(db.Model):
    __tablename__ = 'knowledgeentity'
    keId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    keGUID = db.Column(db.Text, nullable=False)
    keFileType = db.Column(db.Text, nullable=False)
    keName = db.Column(db.Text, nullable=False)
    keCreateTime = db.Column(db.Text, nullable=False)
    keAbstract = db.Column(db.Text)

# 论坛模型
class ForumSummary(db.Model):
    __tablename__ = 'forumsummary'
    forumId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    forumCreator = db.Column(db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    forumName = db.Column(db.Text, nullable=False)
    forumType = db.Column(db.Boolean, nullable=False)
    forumCreateTime = db.Column(db.Text, nullable=False)
    forumPermission = db.Column(db.Boolean, nullable=False)
    forumStatus = db.Column(db.Integer, nullable=False)

    creator = db.relationship('UserInfo', foreign_keys=[forumCreator])

class ForumContent(db.Model):
    __tablename__ = 'forumcontent'
    postId = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    postCreateTime = db.Column(db.Text, nullable=False)
    postPosterId = db.Column(db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    postForumId = db.Column(db.BigInteger, db.ForeignKey('forumsummary.forumId'), nullable=False)
    postContent = db.Column(db.JSON, nullable=False)
    postPraiseNumber = db.Column(db.Integer, default=0)
    postStatus = db.Column(db.Integer, nullable=False)

    poster = db.relationship('UserInfo', foreign_keys=[postPosterId])
    forum = db.relationship('ForumSummary', foreign_keys=[postForumId])

# 留言模型
class Message(db.Model):
    __tablename__ = 'mailitem'
    messageId = db.Column('mailItemId', db.BigInteger, primary_key=True, autoincrement=True)
    messageSenderId = db.Column('mailFromUserId', db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    messageReceiverId = db.Column('mailToUserId', db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    messageContent = db.Column('mailItemContent', db.Text, nullable=False)
    messageStatus = db.Column('mailItemStatus', db.Integer, nullable=False)
    messageCreateTime = db.Column('mailItemSendTime', db.BigInteger, nullable=False)

    sender = db.relationship('UserInfo', foreign_keys=[messageSenderId])
    receiver = db.relationship('UserInfo', foreign_keys=[messageReceiverId])

# 大模型对话模型
class Chat(db.Model):
    __tablename__ = 'llmhistory'
    chatId = db.Column('sessionId', db.BigInteger, primary_key=True, autoincrement=True)
    chatUserId = db.Column('sessionUserId', db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    chatContent = db.Column('sessionContent', db.JSON, nullable=False)
    chatStatus = db.Column('isSessionDM', db.Boolean, nullable=False)
    chatCreateTime = db.Column('sessionSaveTime', db.Text, nullable=False)

    user = db.relationship('UserInfo', foreign_keys=[chatUserId])

# 重要事项清单模型
class Todo(db.Model):
    __tablename__ = 'importantlist'
    todoId = db.Column('listItemId', db.BigInteger, primary_key=True, autoincrement=True)
    todoUserId = db.Column('userId', db.BigInteger, db.ForeignKey('userinfo.userId'), nullable=False)
    todoContent = db.Column('listItemContent', db.Text, nullable=False)
    todoPriority = db.Column('listItemPriority', db.Integer, nullable=False)
    todoStatus = db.Column('listItemStatus', db.Integer, nullable=False)
    todoCreateTime = db.Column('listItemStartTime', db.BigInteger, nullable=False)
    todoEndTime = db.Column('listItemEndTime', db.BigInteger, nullable=False)
    todoIsFinished = db.Column('listItemIsFinished', db.Integer, nullable=False)
    todoTimeMode = db.Column('listItemTimeMode', db.Integer, nullable=False)
    todoTimeWeek = db.Column('listItemTimeWeek', db.Integer, nullable=False)

    user = db.relationship('UserInfo', foreign_keys=[todoUserId])

# 登录路由
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # 生成JWT token
        token = jwt.encode({
            'username': username,
            'exp': time.time() + 24 * 60 * 60  # 24小时过期
        }, JWT_SECRET, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'message': '登录成功'
        })
    else:
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401

# 用户管理路由
@app.route('/api/users', methods=['GET'])
def get_users():
    users = UserInfo.query.all()
    return jsonify([{
        'userId': user.userId,
        'userName': user.userName,
        'userType': user.userType,
        'userSex': user.userSex,
        'userAge': user.userAge,
        'userFrom': user.userFrom,
        'userContact': user.userContact,
        'userDescription': user.userDescription,
        'userRegisterTime': user.userRegisterTime
    } for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserInfo.query.get_or_404(user_id)
    return jsonify({
        'userId': user.userId,
        'userName': user.userName,
        'userType': user.userType,
        'userSex': user.userSex,
        'userAge': user.userAge,
        'userFrom': user.userFrom,
        'userContact': user.userContact,
        'userDescription': user.userDescription,
        'userRegisterTime': user.userRegisterTime
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = UserInfo(
        userCiphertext=data['userCiphertext'],
        userName=data['userName'],
        userType=data['userType'],
        userSex=data['userSex'],
        userSexPermission=data['userSexPermission'],
        userAge=data['userAge'],
        userAgePermission=data['userAgePermission'],
        userFrom=data['userFrom'],
        userFromPermission=data['userFromPermission'],
        userContact=data['userContact'],
        userContactPermission=data['userContactPermission'],
        userDescription=data.get('userDescription'),
        patientImportantInfo=data.get('patientImportantInfo'),
        doctorImportantInfo=data.get('doctorImportantInfo'),
        userImportantInfoPermission=data['userImportantInfoPermission'],
        userAvatarId=data.get('userAvatarId'),
        userRegisterTime=int(datetime.now().timestamp())
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'userId': new_user.userId})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = UserInfo.query.get_or_404(user_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserInfo.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# 病历管理路由
@app.route('/api/medical-records', methods=['GET'])
def get_medical_records():
    records = MedicalRecord.query.all()
    return jsonify([{
        'medrecId': record.medrecId,
        'medrecCreateTime': record.medrecCreateTime,
        'medrecModifyTime': record.medrecModifyTime,
        'medrecPatientId': record.medrecPatientId,
        'medrecDoctorId': record.medrecDoctorId,
        'medrecAbstract': record.medrecAbstract,
        'medrecState': record.medrecState,
        'medrecContent': record.medrecContent,
        'patientName': record.patient.userName if record.patient else None,
        'doctorName': record.doctor.userName if record.doctor else None
    } for record in records])

@app.route('/api/medical-records/<int:record_id>', methods=['GET'])
def get_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify({
        'medrecId': record.medrecId,
        'medrecCreateTime': record.medrecCreateTime,
        'medrecModifyTime': record.medrecModifyTime,
        'medrecPatientId': record.medrecPatientId,
        'medrecDoctorId': record.medrecDoctorId,
        'medrecAbstract': record.medrecAbstract,
        'medrecState': record.medrecState,
        'medrecContent': record.medrecContent,
        'patientName': record.patient.userName if record.patient else None,
        'doctorName': record.doctor.userName if record.doctor else None
    })

@app.route('/api/medical-records', methods=['POST'])
def create_medical_record():
    data = request.json
    current_time = str(int(datetime.now().timestamp()))
    new_record = MedicalRecord(
        medrecCreateTime=current_time,
        medrecModifyTime=current_time,
        medrecPatientId=data['medrecPatientId'],
        medrecDoctorId=data['medrecDoctorId'],
        medrecAbstract=data.get('medrecAbstract'),
        medrecState=data['medrecState'],
        medrecContent=data['medrecContent']
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Medical record created successfully', 'medrecId': new_record.medrecId})

@app.route('/api/medical-records/<int:record_id>', methods=['PUT'])
def update_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(record, key):
            setattr(record, key, value)
    
    record.medrecModifyTime = str(int(datetime.now().timestamp()))
    db.session.commit()
    return jsonify({'message': 'Medical record updated successfully'})

@app.route('/api/medical-records/<int:record_id>', methods=['DELETE'])
def delete_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Medical record deleted successfully'})

# 知识库管理路由
@app.route('/api/knowledge', methods=['GET'])
def get_knowledge_entities():
    entities = KnowledgeEntity.query.all()
    return jsonify([{
        'keId': entity.keId,
        'keGUID': entity.keGUID,
        'keFileType': entity.keFileType,
        'keName': entity.keName,
        'keCreateTime': entity.keCreateTime,
        'keAbstract': entity.keAbstract
    } for entity in entities])

@app.route('/api/knowledge/<int:entity_id>', methods=['GET'])
def get_knowledge_entity(entity_id):
    entity = KnowledgeEntity.query.get_or_404(entity_id)
    return jsonify({
        'keId': entity.keId,
        'keGUID': entity.keGUID,
        'keFileType': entity.keFileType,
        'keName': entity.keName,
        'keCreateTime': entity.keCreateTime,
        'keAbstract': entity.keAbstract
    })

@app.route('/api/knowledge', methods=['POST'])
def create_knowledge_entity():
    data = request.json
    import uuid
    new_entity = KnowledgeEntity(
        keGUID=data.get('keGUID', str(uuid.uuid4())),
        keFileType=data['keFileType'],
        keName=data['keName'],
        keCreateTime=str(int(datetime.now().timestamp())),
        keAbstract=data.get('keAbstract')
    )
    db.session.add(new_entity)
    db.session.commit()
    return jsonify({'message': 'Knowledge entity created successfully', 'keId': new_entity.keId})

@app.route('/api/knowledge/<int:entity_id>', methods=['PUT'])
def update_knowledge_entity(entity_id):
    entity = KnowledgeEntity.query.get_or_404(entity_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(entity, key):
            setattr(entity, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Knowledge entity updated successfully'})

@app.route('/api/knowledge/<int:entity_id>', methods=['DELETE'])
def delete_knowledge_entity(entity_id):
    entity = KnowledgeEntity.query.get_or_404(entity_id)
    db.session.delete(entity)
    db.session.commit()
    return jsonify({'message': 'Knowledge entity deleted successfully'})

# 论坛管理路由
@app.route('/api/forums', methods=['GET'])
def get_forums():
    forums = ForumSummary.query.all()
    return jsonify([{
        'forumId': forum.forumId,
        'forumCreator': forum.forumCreator,
        'forumName': forum.forumName,
        'forumType': forum.forumType,
        'forumCreateTime': forum.forumCreateTime,
        'forumPermission': forum.forumPermission,
        'forumStatus': forum.forumStatus,
        'creatorName': forum.creator.userName if forum.creator else None
    } for forum in forums])

@app.route('/api/forums/<int:forum_id>', methods=['GET'])
def get_forum(forum_id):
    forum = ForumSummary.query.get_or_404(forum_id)
    return jsonify({
        'forumId': forum.forumId,
        'forumCreator': forum.forumCreator,
        'forumName': forum.forumName,
        'forumType': forum.forumType,
        'forumCreateTime': forum.forumCreateTime,
        'forumPermission': forum.forumPermission,
        'forumStatus': forum.forumStatus,
        'creatorName': forum.creator.userName if forum.creator else None
    })

@app.route('/api/forums', methods=['POST'])
def create_forum():
    data = request.json
    new_forum = ForumSummary(
        forumCreator=data['forumCreator'],
        forumName=data['forumName'],
        forumType=data['forumType'],
        forumCreateTime=str(int(datetime.now().timestamp())),
        forumPermission=data['forumPermission'],
        forumStatus=data['forumStatus']
    )
    db.session.add(new_forum)
    db.session.commit()
    return jsonify({'message': 'Forum created successfully', 'forumId': new_forum.forumId})

@app.route('/api/forums/<int:forum_id>', methods=['PUT'])
def update_forum(forum_id):
    forum = ForumSummary.query.get_or_404(forum_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(forum, key):
            setattr(forum, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Forum updated successfully'})

@app.route('/api/forums/<int:forum_id>', methods=['DELETE'])
def delete_forum(forum_id):
    forum = ForumSummary.query.get_or_404(forum_id)
    db.session.delete(forum)
    db.session.commit()
    return jsonify({'message': 'Forum deleted successfully'})

# 论坛帖子路由
@app.route('/api/forum-posts', methods=['GET'])
def get_forum_posts():
    posts = ForumContent.query.all()
    return jsonify([{
        'postId': post.postId,
        'postCreateTime': post.postCreateTime,
        'postPosterId': post.postPosterId,
        'postForumId': post.postForumId,
        'postContent': post.postContent,
        'postPraiseNumber': post.postPraiseNumber,
        'postStatus': post.postStatus,
        'posterName': post.poster.userName if post.poster else None,
        'forumName': post.forum.forumName if post.forum else None
    } for post in posts])

@app.route('/api/forum-posts/<int:post_id>', methods=['GET'])
def get_forum_post(post_id):
    post = ForumContent.query.get_or_404(post_id)
    return jsonify({
        'postId': post.postId,
        'postCreateTime': post.postCreateTime,
        'postPosterId': post.postPosterId,
        'postForumId': post.postForumId,
        'postContent': post.postContent,
        'postPraiseNumber': post.postPraiseNumber,
        'postStatus': post.postStatus,
        'posterName': post.poster.userName if post.poster else None,
        'forumName': post.forum.forumName if post.forum else None
    })

@app.route('/api/forum-posts', methods=['POST'])
def create_forum_post():
    data = request.json
    new_post = ForumContent(
        postCreateTime=str(int(datetime.now().timestamp())),
        postPosterId=data['postPosterId'],
        postForumId=data['postForumId'],
        postContent=data['postContent'],
        postPraiseNumber=0,
        postStatus=data['postStatus']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Forum post created successfully', 'postId': new_post.postId})

@app.route('/api/forum-posts/<int:post_id>', methods=['PUT'])
def update_forum_post(post_id):
    post = ForumContent.query.get_or_404(post_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(post, key):
            setattr(post, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Forum post updated successfully'})

@app.route('/api/forum-posts/<int:post_id>', methods=['DELETE'])
def delete_forum_post(post_id):
    post = ForumContent.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Forum post deleted successfully'})

# 留言管理路由
@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        'messageId': message.messageId,
        'messageSenderId': message.messageSenderId,
        'messageReceiverId': message.messageReceiverId,
        'messageContent': message.messageContent,
        'messageStatus': message.messageStatus,
        'messageCreateTime': message.messageCreateTime,
        'senderName': UserInfo.query.get(message.messageSenderId).userName,
        'receiverName': UserInfo.query.get(message.messageReceiverId).userName
    } for message in messages])

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(
        messageSenderId=data['messageSenderId'],
        messageReceiverId=data['messageReceiverId'],
        messageContent=data['messageContent'],
        messageStatus=data['messageStatus'],
        messageCreateTime=int(datetime.now().timestamp())
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created successfully'})

@app.route('/api/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.json
    message.messageContent = data['messageContent']
    message.messageStatus = data['messageStatus']
    db.session.commit()
    return jsonify({'message': 'Message updated successfully'})

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})

# 大模型对话路由
@app.route('/api/chats', methods=['GET'])
def get_chats():
    chats = Chat.query.all()
    return jsonify([{
        'chatId': chat.chatId,
        'chatUserId': chat.chatUserId,
        'chatContent': chat.chatContent,
        'chatStatus': chat.chatStatus,
        'chatCreateTime': chat.chatCreateTime,
        'userName': UserInfo.query.get(chat.chatUserId).userName
    } for chat in chats])

@app.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.json
    new_chat = Chat(
        chatUserId=data['chatUserId'],
        chatContent=data['chatContent'],
        chatStatus=data['chatStatus'],
        chatCreateTime=int(datetime.now().timestamp())
    )
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'message': 'Chat created successfully'})

@app.route('/api/chats/<int:chat_id>', methods=['PUT'])
def update_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    data = request.json
    chat.chatContent = data['chatContent']
    chat.chatStatus = data['chatStatus']
    db.session.commit()
    return jsonify({'message': 'Chat updated successfully'})

@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({'message': 'Chat deleted successfully'})

# 重要事项清单路由
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{
        'todoId': todo.todoId,
        'todoUserId': todo.todoUserId,
        'todoContent': todo.todoContent,
        'todoPriority': todo.todoPriority,
        'todoStatus': todo.todoStatus,
        'todoCreateTime': todo.todoCreateTime,
        'userName': UserInfo.query.get(todo.todoUserId).userName
    } for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(
        todoUserId=data['todoUserId'],
        todoContent=data['todoContent'],
        todoPriority=data['todoPriority'],
        todoStatus=data['todoStatus'],
        todoCreateTime=int(datetime.now().timestamp())
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'})

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.json
    todo.todoContent = data['todoContent']
    todo.todoPriority = data['todoPriority']
    todo.todoStatus = data['todoStatus']
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        # 创建所有数据库表
        db.create_all()
    app.run(debug=True)
    
