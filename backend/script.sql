-- Copyright (c) 2024~2025 DuYu (202103180009@stu.qlu.edu.cn), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences).
-- 该文件为“明康慧医MKTY”智慧医疗系统的数据库DDL文件（SQL建表语句）。该文件为MKTY系统的重要组成部分。
-- 该文件由DataGrip IDE生成
-- 创建日期：2025/01/21
-- 修改日期：2025/04/14

-- 创建数据库 mkty
CREATE DATABASE IF NOT EXISTS mkty;

-- 选择数据库
USE mkty;

create table knowledgeentity
(
	keId bigint auto_increment comment '知识实体ID，唯一标识知识库实体。'
		primary key,
	keGUID text not null comment '知识实体GUID，用于命名知识实体存储目录。',
	keFileType text not null comment '知识实体源文件类型，文件的MIME格式。',
	keName text not null comment '知识实体名称，展示时的标题。',
	keCreateTime text not null comment '上传时间，Unix时间戳，精确到秒，服务器时间。',
	keAbstract text null comment '知识实体概要。'
)
comment '知识实体表' charset=utf8mb3;

create table userinfo
(
	userId bigint auto_increment comment '用户ID，每个用户的唯一编码，注册时随机生成。'
		primary key,
	userCiphertext text not null comment '用户密码的加密值。',
	userName text not null comment '用户姓名。',
	userType text not null comment '用户类型: 0 - 患者, 1 - 医师, 2 - 其他。',
	userSex tinyint(1) not null comment '用户性别: True - 男性, False - 女性。',
	userSexPermission tinyint(1) not null comment '用户性别查看权限，0=公开；1=仅自己可见',
	userAge text not null comment '用户年龄，以文本存储。',
	userAgePermission tinyint(1) not null comment '用户年龄查看权限，0=公开；1=仅自己可见',
	userFrom text not null comment '用户来源地，患者填写城市，医师填写机构名称。',
	userFromPermission tinyint(1) not null comment '用户来源地查看权限，0=公开；1=仅自己可见',
	userContact text not null comment '用户联系方式，电话号码或邮箱。',
	userContactPermission tinyint(1) not null comment '用户联系方式查看权限，0=公开；1=仅自己可见',
	userDescription text null comment '用户自述，限制字数1024字符。',
	patientImportantInfo text null comment '患者特有信息，慢性病、过敏、家族遗传病史记录等。',
	doctorImportantInfo text null comment '医师特有信息，科室与擅长专业。',
	userImportantInfoPermission tinyint(1) not null comment '用户重要信息查看权限，0=公开；1=仅自己可见',
	userAvatarId text null comment '用户头像ID，头像ID为GUID。',
	userRegisterTime bigint not null comment '用户注册时间（服务器时间，以秒为单位的Unix时间戳）'
)
comment '用户信息表' charset=utf8mb3;

create table forumsummary
(
	forumId bigint auto_increment comment '论坛ID，唯一标识一个论坛。'
		primary key,
	forumCreator bigint not null comment '论坛创建者userId',
	forumName text not null comment '论坛名称。',
	forumType tinyint(1) not null comment '论坛类型: 0=医学知识论坛；1=疾病论坛。',
	forumCreateTime text not null comment '论坛创建时间，Unix时间戳，精确到秒，服务器时间。',
	forumPermission tinyint(1) not null comment '论坛权限，0=不限人员类型；1=仅限医师创建、参与；2=仅限患者创建、参与',
	forumStatus int not null comment '论坛状态：0=正常；1=已被删除；2=其他情况',
	constraint forumsummary_userinfo_userId_fk
		foreign key (forumCreator) references userinfo (userId)
)
comment '论坛列表' charset=utf8mb3;

create table forumcontent
(
	postId bigint auto_increment comment '帖子ID，唯一标识一个帖子。'
		primary key,
	postCreateTime text not null comment '帖子发布时间，Unix时间戳，精确到秒，服务器时间。',
	postPosterId bigint not null comment '发帖者的用户ID。',
	postForumId bigint not null comment '帖子所属论坛ID。',
	postContent json not null comment '帖子具体内容（images字段：值为一个数组，里面存有各图像的GUID字符串，规定所有图像为webp格式；content字段：帖子文本字符串）',
	postPraiseNumber int default 0 null comment '帖子被点赞的数量。',
	postStatus int not null comment '帖子状态（0=正常；1=被删除；2=其他情况）',
	constraint forumcontent_ibfk_1
		foreign key (postPosterId) references userinfo (userId)
			on delete cascade,
	constraint forumcontent_ibfk_2
		foreign key (postForumId) references forumsummary (forumId)
			on delete cascade
)
comment '论坛内容表（帖子）' charset=utf8mb3;

create index postForumId
	on forumcontent (postForumId);

create index postPosterId
	on forumcontent (postPosterId);

create table importantlist
(
	listItemId bigint auto_increment comment '清单项id'
		primary key,
	userId bigint not null comment '该项所属的userId',
	listItemContent text not null comment '医疗事项内容',
	listItemStartTime bigint not null comment '（一次性事项的）事项开始时间（秒为单位Unix时间戳）',
	listItemEndTime bigint not null comment '（一次性事项的）事项结束时间（秒为单位Unix时间戳）',
	listItemPriority tinyint not null comment '事项优先级（0=正常；1=非常重要）',
	listItemStatus tinyint not null comment '事项状态（0=正常；1=删除；2=其他）',
	listItemIsFinished tinyint not null comment '事项是否完成（0=未完成；1=已完成）',
	listItemTimeMode tinyint not null comment '事项的时间模式（0=一次性事项；1=周期性事项【每周的某天】；2=不声明时间）',
	listItemTimeWeek tinyint not null comment '（周期性事项的）星期【1=星期一；7=星期日】',
	constraint importantlist_userinfo_userId_fk
		foreign key (userId) references userinfo (userId)
)
comment '重要事项清单表';

create table llmhistory
(
	sessionId bigint auto_increment comment '会话ID，唯一标识一个会话。'
		primary key,
	isSessionDM tinyint(1) not null comment '会话是否启用大模型“讨论”机制。',
	sessionSaveTime text not null comment '会话保存时间，Unix时间戳，精确到秒，服务器时间。',
	sessionUserId bigint not null comment '会话所属用户ID。',
	sessionContent json not null comment '会话内容，存储JSON格式。',
	constraint llmhistory_ibfk_1
		foreign key (sessionUserId) references userinfo (userId)
			on delete cascade
)
comment '大模型问答历史记录表' charset=utf8mb3;

create index sessionUserId
	on llmhistory (sessionUserId);

create table mailitem
(
	mailItemId bigint auto_increment comment '留言信息Id'
		primary key,
	mailFromUserId bigint not null comment '留言者用户Id',
	mailToUserId bigint not null comment '被留言者UserId',
	mailItemContent text not null comment '留言信息文本内容',
	mailItemStatus int not null comment '留言条目状态；0=正常；1=被删除；2=其他',
	mailItemSendTime bigint not null comment '留言条目发送时间，以秒为单位的Unix时间戳',
	constraint mailitem_userinfo_userId_fk2
		foreign key (mailFromUserId) references userinfo (userId)
)
comment '用户留言表';

create index mailitem_userinfo_userId_fk
	on mailitem (mailToUserId);

create table medicalrecord
(
	medrecId bigint auto_increment comment '病历ID，每个电子病历唯一编码。'
		primary key,
	medrecCreateTime text not null comment '病历创建时间，Unix时间戳，精确到秒，服务器时间。',
	medrecModifyTime text not null comment '病历修改时间，Unix时间戳，精确到秒，服务器时间。',
	medrecPatientId bigint not null comment '病历所属患者ID。',
	medrecMainDoctorId bigint not null comment '病历主要负责人（医师）ID。',
	medrecMinorDoctorId bigint null comment '病历其他负责人（医师）ID。',
	medrecAbstract text null comment '病历概要，简洁描述病历。',
	medrecState text not null comment '病历状态: 0 - 正常生效，1 - 痊愈无效，2 - 慢性病优先级降低。',
	medrecRight text not null comment '病历权限: 0 - 仅患者与医师可见，1 - 公开可检索。',
	medrecEigenVector json null comment '病历特征值，存储病历的TF-IDF与BigBird特征。',
	medrecResList json null comment '病历资源列表，存储病历中上传的资源ID。',
	constraint medicalrecord_ibfk_1
		foreign key (medrecPatientId) references userinfo (userId)
			on delete cascade,
	constraint medicalrecord_ibfk_2
		foreign key (medrecMainDoctorId) references userinfo (userId)
			on delete cascade,
	constraint medicalrecord_ibfk_3
		foreign key (medrecMinorDoctorId) references userinfo (userId)
			on delete cascade
)
comment '电子病历表' charset=utf8mb3;

create index medrecMainDoctorId
	on medicalrecord (medrecMainDoctorId);

create index medrecMinorDoctorId
	on medicalrecord (medrecMinorDoctorId);

create index medrecPatientId
	on medicalrecord (medrecPatientId);

create table resource
(
	resourceId bigint auto_increment comment '资源ID，唯一标识资源。'
		primary key,
	resourcePath text not null comment '资源存储路径，相对于服务器存储根目录。',
	resourceParentType text not null comment '资源归属类型: 0 - 病历，1 - 知识库。',
	resourceParentId bigint not null comment '资源归属ID，病历ID或知识库ID。',
	resourcePermission tinyint(1) not null comment '资源权限: True - 仅限病历患者与医师可见，False - 公开。',
	resourceType text not null comment '资源类型，如 audio/mp3。',
	resourceEigenVector json null comment '资源特征值，存储CLIP图像特征。',
	constraint resource_ibfk_1
		foreign key (resourceParentId) references medicalrecord (medrecId)
			on delete cascade,
	constraint resource_ibfk_2
		foreign key (resourceParentId) references knowledgeentity (keId)
			on delete cascade
)
comment '资源表' charset=utf8mb3;

create index resourceParentId
	on resource (resourceParentId);

create table usercollectionke
(
	recId bigint auto_increment comment '记录ID，唯一标识一条收藏记录。'
		primary key,
	userId bigint not null comment '用户ID，表示该记录关于哪位用户。',
	keId bigint not null comment '知识实体ID，表示用户收藏的知识实体。',
	constraint usercollectionke_ibfk_1
		foreign key (userId) references userinfo (userId)
			on delete cascade,
	constraint usercollectionke_ibfk_2
		foreign key (keId) references knowledgeentity (keId)
			on delete cascade
)
comment '用户收藏的知识实体表' charset=utf8mb3;

create index keId
	on usercollectionke (keId);

create index userId
	on usercollectionke (userId);

