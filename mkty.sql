-- Copyright (c) 2024~2025 DuYu (202103180009@stu.qlu.edu.cn), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences).
-- 该文件为“明康慧医MKTY”智慧医疗系统的数据库DDL文件（SQL建表语句）。该文件为MKTY系统的重要组成部分。
-- 创建日期：2025/01/21
-- 修改日期：2025/01/22

-- 创建数据库 mkty
CREATE DATABASE IF NOT EXISTS mkty;

-- 选择数据库
USE mkty;

-- 1. 用户信息表
CREATE TABLE IF NOT EXISTS userInfo (
    userId BIGINT NOT NULL COMMENT '用户ID，每个用户的唯一编码，注册时随机生成。',
    userCiphertext TEXT NOT NULL COMMENT '用户密码的加密值。',
    userType TEXT NOT NULL COMMENT '用户类型: 0 - 患者, 1 - 医师, 2 - 其他。',
    userName TEXT NOT NULL COMMENT '用户姓名。',
    userSex BOOLEAN NOT NULL COMMENT '用户性别: True - 男性, False - 女性。',
    userAge TEXT NOT NULL COMMENT '用户年龄，以文本存储。',
    userContact TEXT NOT NULL COMMENT '用户联系方式，电话号码或邮箱。',
    userDescription TEXT COMMENT '用户自述，限制字数1024字符。',
    userFrom TEXT NOT NULL COMMENT '用户来源地，患者填写城市，医师填写机构名称。',
    patientImportantInfo TEXT COMMENT '患者特有信息，慢性病、过敏、家族遗传病史记录等。',
    doctorImportantInfo TEXT COMMENT '医师特有信息，科室与擅长专业。',
    userAvatarId TEXT COMMENT '用户头像ID，头像ID为GUID。',
    PRIMARY KEY (userId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';

-- 2. 电子病历表
CREATE TABLE IF NOT EXISTS medicalRecord (
    medrecId BIGINT AUTO_INCREMENT NOT NULL COMMENT '病历ID，每个电子病历唯一编码。',
    medrecCreateTime TEXT NOT NULL COMMENT '病历创建时间，Unix时间戳，精确到秒，服务器时间。',
    medrecModifyTime TEXT NOT NULL COMMENT '病历修改时间，Unix时间戳，精确到秒，服务器时间。',
    medrecPatientId BIGINT NOT NULL COMMENT '病历所属患者ID。',
    medrecMainDoctorId BIGINT NOT NULL COMMENT '病历主要负责人（医师）ID。',
    medrecMinorDoctorId BIGINT COMMENT '病历其他负责人（医师）ID。',
    medrecAbstract TEXT COMMENT '病历概要，简洁描述病历。',
    medrecState TEXT NOT NULL COMMENT '病历状态: 0 - 正常生效，1 - 痊愈无效，2 - 慢性病优先级降低。',
    medrecRight TEXT NOT NULL COMMENT '病历权限: 0 - 仅患者与医师可见，1 - 公开可检索。',
    medrecEigenVector JSON COMMENT '病历特征值，存储病历的TF-IDF与BigBird特征。',
    medrecResList JSON COMMENT '病历资源列表，存储病历中上传的资源ID。',
    PRIMARY KEY (medrecId),
    FOREIGN KEY (medrecPatientId) REFERENCES userInfo(userId) ON DELETE CASCADE,
    FOREIGN KEY (medrecMainDoctorId) REFERENCES userInfo(userId) ON DELETE CASCADE,
    FOREIGN KEY (medrecMinorDoctorId) REFERENCES userInfo(userId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电子病历表';

-- 3. 知识实体表
CREATE TABLE IF NOT EXISTS knowledgeEntity (
    keId BIGINT AUTO_INCREMENT NOT NULL COMMENT '知识实体ID，唯一标识知识库实体。',
    keFileType TEXT NOT NULL COMMENT '知识实体源文件类型，文件的MIME格式。',
    keName TEXT NOT NULL COMMENT '知识实体名称，展示时的标题。',
    keCreateTime TEXT NOT NULL COMMENT '上传时间，Unix时间戳，精确到秒，服务器时间。',
    keAbstract TEXT COMMENT '知识实体概要。',
    isKeMultimodal BOOLEAN NOT NULL COMMENT '是否为多模态实体，True=是。',
    keTextEigenVectors JSON COMMENT '知识实体各文本特征。',
    keResList JSON COMMENT '知识实体资源列表，解析出的资源ID。',
    PRIMARY KEY (keId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='知识实体表';

-- 4. 资源表
CREATE TABLE IF NOT EXISTS resource (
    resourceId BIGINT AUTO_INCREMENT NOT NULL COMMENT '资源ID，唯一标识资源。',
    resourcePath TEXT NOT NULL COMMENT '资源存储路径，相对于服务器存储根目录。',
    resourceParentType TEXT NOT NULL COMMENT '资源归属类型: 0 - 病历，1 - 知识库。',
    resourceParentId BIGINT NOT NULL COMMENT '资源归属ID，病历ID或知识库ID。',
    resourcePermission BOOLEAN NOT NULL COMMENT '资源权限: True - 仅限病历患者与医师可见，False - 公开。',
    resourceType TEXT NOT NULL COMMENT '资源类型，如 audio/mp3。',
    resourceEigenVector JSON COMMENT '资源特征值，存储CLIP图像特征。',
    PRIMARY KEY (resourceId),
    FOREIGN KEY (resourceParentId) REFERENCES medicalRecord(medrecId) ON DELETE CASCADE,
    FOREIGN KEY (resourceParentId) REFERENCES knowledgeEntity(keId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='资源表';

-- 5. 论坛列表
CREATE TABLE IF NOT EXISTS forumSummary (
    forumId BIGINT AUTO_INCREMENT NOT NULL COMMENT '论坛ID，唯一标识一个论坛。',
    forumName TEXT NOT NULL COMMENT '论坛名称。',
    forumType BOOLEAN NOT NULL COMMENT '论坛类型: True - 疾病论坛, False - 医学知识论坛。',
    forumCreateTime TEXT NOT NULL COMMENT '论坛创建时间，Unix时间戳，精确到秒，服务器时间。',
    PRIMARY KEY (forumId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='论坛列表';

-- 6. 论坛内容表（帖子）
CREATE TABLE IF NOT EXISTS forumContent (
    postId BIGINT AUTO_INCREMENT NOT NULL COMMENT '帖子ID，唯一标识一个帖子。',
    postCreateTime TEXT NOT NULL COMMENT '帖子发布时间，Unix时间戳，精确到秒，服务器时间。',
    postPosterId BIGINT NOT NULL COMMENT '发帖者的用户ID。',
    postForumId BIGINT NOT NULL COMMENT '帖子所属论坛ID。',
    postContent TEXT NOT NULL COMMENT '帖子具体内容。',
    postPraiseNumber INT DEFAULT 0 COMMENT '帖子被点赞的数量。',
    PRIMARY KEY (postId),
    FOREIGN KEY (postPosterId) REFERENCES userInfo(userId) ON DELETE CASCADE,
    FOREIGN KEY (postForumId) REFERENCES forumSummary(forumId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='论坛内容表（帖子）';

-- 7. 用户收藏的知识实体表
CREATE TABLE IF NOT EXISTS userCollectionKe (
    recId BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID，唯一标识一条收藏记录。',
    userId BIGINT NOT NULL COMMENT '用户ID，表示该记录关于哪位用户。',
    keId BIGINT NOT NULL COMMENT '知识实体ID，表示用户收藏的知识实体。',
    FOREIGN KEY (userId) REFERENCES userInfo(userId) ON DELETE CASCADE,
    FOREIGN KEY (keId) REFERENCES knowledgeEntity(keId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户收藏的知识实体表';

-- 8. 大模型问答历史记录表
CREATE TABLE IF NOT EXISTS LlmHistory (
    sessionId BIGINT AUTO_INCREMENT NOT NULL COMMENT '会话ID，唯一标识一个会话。',
    isSessionDM BOOLEAN NOT NULL COMMENT '会话是否启用大模型“讨论”机制。',
    sessionSaveTime TEXT NOT NULL COMMENT '会话保存时间，Unix时间戳，精确到秒，服务器时间。',
    sessionUserId BIGINT NOT NULL COMMENT '会话所属用户ID。',
    sessionContent JSON NOT NULL COMMENT '会话内容，存储JSON格式。',
    PRIMARY KEY (sessionId),
    FOREIGN KEY (sessionUserId) REFERENCES userInfo(userId) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='大模型问答历史记录表';
