-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mkty_02
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `forumcontent`
--

DROP TABLE IF EXISTS `forumcontent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forumcontent` (
  `postId` bigint NOT NULL AUTO_INCREMENT COMMENT '帖子ID，唯一标识一个帖子。',
  `postCreateTime` text NOT NULL COMMENT '帖子发布时间，Unix时间戳，精确到秒，服务器时间。',
  `postPosterId` bigint NOT NULL COMMENT '发帖者的用户ID。',
  `postForumId` bigint NOT NULL COMMENT '帖子所属论坛ID。',
  `postContent` json NOT NULL COMMENT '帖子具体内容（images字段：值为一个数组，里面存有各图像的GUID字符串，规定所有图像为webp格式；content字段：帖子文本字符串）',
  `postPraiseNumber` int DEFAULT '0' COMMENT '帖子被点赞的数量。',
  `postStatus` int NOT NULL COMMENT '帖子状态（0=正常；1=被删除；2=其他情况）',
  PRIMARY KEY (`postId`),
  KEY `postForumId` (`postForumId`),
  KEY `postPosterId` (`postPosterId`),
  CONSTRAINT `forumcontent_ibfk_1` FOREIGN KEY (`postPosterId`) REFERENCES `userinfo` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `forumcontent_ibfk_2` FOREIGN KEY (`postForumId`) REFERENCES `forumsummary` (`forumId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3 COMMENT='论坛内容表（帖子）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forumcontent`
--

LOCK TABLES `forumcontent` WRITE;
/*!40000 ALTER TABLE `forumcontent` DISABLE KEYS */;
INSERT INTO `forumcontent` VALUES (1,'1744932622',8,3,'{\"images\": \"\", \"content\": \"小托尼有迪克吗？\"}',0,0),(2,'1744932789',8,3,'{\"images\": \"6c9b2132-199a-463e-9761-fdf2441af1dd\", \"content\": \"02_小托尼有迪克吗？\"}',0,1),(4,'1744932622',8,4,'{\"images\": \"6c9b2132-199a-463e-9761-fdf2441af1dd$^6c9b2132-199a-463e-9761-fdf2441af1dd\", \"content\": \"小托尼有迪克吗？\"}',937,0),(5,'1744932622',8,4,'{\"images\": \"\", \"content\": \"小托尼有迪克吗？\"}',0,1),(6,'1744932623',9,4,'{\"images\": \"\", \"content\": \"当然是没有了！\"}',939,0),(7,'1744932624',9,4,'{\"images\": \"\", \"content\": \"当然是没有了！\"}',933,0),(8,'1745606510',8,3,'{\"images\": \"293524c3-edc2-47e1-b9dd-e69dcc25715e$^fec6e10c-446c-42bc-b906-9a980c12b483\", \"content\": \"03_小托尼有迪克吗？\"}',1,0),(9,'1745606929',8,4,'{\"images\": \"8dd56703-22cb-4da3-9e80-f4e1fbba6c1a\", \"content\": \"测试帖子\"}',0,1),(10,'1745607109',8,4,'{\"images\": \"\", \"content\": \"测试帖子。\"}',0,0),(11,'1745607157',8,4,'{\"images\": \"fe76bdd0-c5ca-404c-b342-d1fb3b9da21c$^3cb3f12f-6c25-40d9-a9e5-ca0fb0e90c96$^2f7f28c8-b73e-4c14-b4db-677945068d5b\", \"content\": \"测试图片帖子。\"}',0,0),(12,'1745661656',8,3,'{\"images\": \"d0525573-1487-4292-948f-fe39ee49263c$^c88876d0-dbc1-4c17-ac4a-4b35b81571b3$^0b8aa47e-48f3-486b-a15d-f4edaff192d0\", \"content\": \"来！看看小迪克托尼的帅照！\"}',4,0),(13,'1745661692',8,3,'{\"images\": \"674c9b01-2950-457c-b4ee-75d490eea4b5$^192665e1-c641-4f4e-b29f-526a40aa00d9\", \"content\": \"你好！\"}',0,1),(14,'1745681778',8,3,'{\"images\": \"3b38c8a7-278f-4324-bc84-14dd3094aed4$^b0ad123c-548e-4057-b6d6-55023050372b\", \"content\": \"Q.T. 又出新歌了！来听听！\"}',0,1),(15,'1745682984',8,3,'{\"images\": \"f49a733d-28fe-4853-8297-9cd549ff1670$^c77d58cd-ef9a-4417-b76d-7a8527a944f6\", \"content\": \" Q.T. 又出新歌了！赶紧来听听！\"}',7,1),(16,'1745744214',8,3,'{\"images\": \"a1975716-a739-49e5-9bfe-3cf0bf1f4f0a$^75255507-cced-4843-924b-9267db47cffd$^f4dba4ae-54db-41c9-b08b-1301e5cb08af\", \"content\": \"上传图片测试。\"}',0,0),(17,'1746615289',8,3,'{\"images\": \"1a2a3cc2-4668-466d-becb-8a5771cbd3f3$^e2566930-3ea0-435d-839b-5f94f94337cd\", \"content\": \"难道常挤眼就能防近视吗？不应该少看手机吗？\"}',2,0),(18,'1746632552',8,2,'{\"images\": \"fc975a87-b55f-4960-8be1-f6ba17684703\", \"content\": \"简直！不忍直视！是吧？\"}',0,0),(19,'1746632876',9,7,'{\"images\": \"ea41abee-3e88-43f8-b1b4-4cc608a744c1$^2e528a55-cffc-4e8e-a50e-bcc0de6445d0$^971adc0d-da05-4bb4-b584-e38f03f83e27\", \"content\": \"我是Nodickny，中文名诺迪克尼。\"}',6,0),(20,'1746632976',8,7,'{\"images\": \"\", \"content\": \"回复：@Нодикнй：迪克尼先生，你为啥起这个名字呢？\"}',4,0),(21,'1746720618',9,3,'{\"images\": \"242a1df1-3f25-44fc-ad5c-9aabe0a994a0$^196804f5-7487-48cd-b08d-a3631edd7c85$^82d57598-b76f-4f32-8129-5dccfeae265c\", \"content\": \"快来看一看Quỳnh Trang！摘掉眼镜就是好看！\"}',16,0),(22,'1746721479',8,7,'{\"images\": \"c95e2c01-2536-400e-abd3-fcaa73b21d64\", \"content\": \"回复：@Quỳnh Trang：快说快说！！！\"}',0,0),(23,'1746782255',8,3,'{\"images\": \"030ec0b3-2981-4d1a-b794-ecf6c0c341c7\", \"content\": \"哎呦我去！\"}',8,0),(24,'1747528541',9,8,'{\"images\": \"\", \"content\": \"脱发中一般脂溢性脱发比较容易治疗。\"}',0,0),(25,'1747528857',2,8,'{\"images\": \"39c25bac-0452-46ad-bdfe-c07ccbe1149d$^9fc0b6e3-ec56-4c23-8acf-a68384caa4c1\", \"content\": \"回复：@Нодикнй：嗯嗯确实！你看我就痊愈了。\"}',0,0),(26,'1749024753',8,3,'{\"images\": \"de5e5e87-47d7-4182-9074-090890af6370$^a345fc7c-a53d-4026-9a87-6e2855d042c7\", \"content\": \"测试帖子\"}',13,0);
/*!40000 ALTER TABLE `forumcontent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forumsummary`
--

DROP TABLE IF EXISTS `forumsummary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forumsummary` (
  `forumId` bigint NOT NULL AUTO_INCREMENT COMMENT '论坛ID，唯一标识一个论坛。',
  `forumCreator` bigint NOT NULL COMMENT '论坛创建者userId',
  `forumName` text NOT NULL COMMENT '论坛名称。',
  `forumType` tinyint(1) NOT NULL COMMENT '论坛类型: 0=医学知识论坛；1=疾病论坛。',
  `forumCreateTime` text NOT NULL COMMENT '论坛创建时间，Unix时间戳，精确到秒，服务器时间。',
  `forumPermission` tinyint(1) NOT NULL COMMENT '论坛权限，0=不限人员类型；1=仅限医师创建、参与；2=仅限患者创建、参与',
  `forumStatus` int NOT NULL COMMENT '论坛状态：0=正常；1=已被删除；2=其他情况',
  PRIMARY KEY (`forumId`),
  KEY `forumsummary_userinfo_userId_fk` (`forumCreator`),
  CONSTRAINT `forumsummary_userinfo_userId_fk` FOREIGN KEY (`forumCreator`) REFERENCES `userinfo` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COMMENT='论坛列表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forumsummary`
--

LOCK TABLES `forumsummary` WRITE;
/*!40000 ALTER TABLE `forumsummary` DISABLE KEYS */;
INSERT INTO `forumsummary` VALUES (2,3,'骨质疏松症讨论区',1,'0',0,0),(3,8,'近视防控论坛',1,'1744759363',1,0),(4,8,'老年人保健综合',0,'1744759363',2,0),(5,8,'Nodickny相关探讨',1,'1744759363',2,1),(6,8,'测试疾病论坛03',1,'1745432300',2,0),(7,8,'高血压预防',1,'1745432472',0,0),(8,8,'脱发医学问题研讨',0,'1747528478',0,0);
/*!40000 ALTER TABLE `forumsummary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `importantlist`
--

DROP TABLE IF EXISTS `importantlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `importantlist` (
  `listItemId` bigint NOT NULL AUTO_INCREMENT COMMENT '清单项id',
  `userId` bigint NOT NULL COMMENT '该项所属的userId',
  `listItemContent` text NOT NULL COMMENT '医疗事项内容',
  `listItemStartTime` bigint NOT NULL COMMENT '（一次性事项的）事项开始时间（秒为单位Unix时间戳）',
  `listItemEndTime` bigint NOT NULL COMMENT '（一次性事项的）事项结束时间（秒为单位Unix时间戳）',
  `listItemPriority` tinyint NOT NULL COMMENT '事项优先级（0=正常；1=非常重要）',
  `listItemStatus` tinyint NOT NULL COMMENT '事项状态（0=正常；1=删除；2=其他）',
  `listItemIsFinished` tinyint NOT NULL COMMENT '事项是否完成（0=未完成；1=已完成）',
  `listItemTimeMode` tinyint NOT NULL COMMENT '事项的时间模式（0=一次性事项；1=周期性事项【每周的某天】；2=不声明时间）',
  `listItemTimeWeek` tinyint NOT NULL COMMENT '（周期性事项的）星期【1=星期一；7=星期日】',
  PRIMARY KEY (`listItemId`),
  KEY `importantlist_userinfo_userId_fk` (`userId`),
  CONSTRAINT `importantlist_userinfo_userId_fk` FOREIGN KEY (`userId`) REFERENCES `userinfo` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='重要事项清单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importantlist`
--

LOCK TABLES `importantlist` WRITE;
/*!40000 ALTER TABLE `importantlist` DISABLE KEYS */;
INSERT INTO `importantlist` VALUES (1,8,'每周三上午10点进行康复训练',1739718610,1739818610,1,1,1,1,3),(2,8,'每周三上午10点进行康复训练',0,0,1,1,0,1,3),(3,8,'每周三上午10点进行康复训练',1739718610,1739818610,1,1,1,1,6),(4,8,'每周三上午10点进行康复训练',1749718610,1759818610,0,1,1,0,3),(5,8,'本周每天用活络油按摩关节',1742918400,1745942400,0,0,1,0,0),(6,8,'晚上十点吃清开灵',0,0,1,0,1,1,4),(7,6,'晚上十点吃清开灵',1743343167,1743343227,1,0,0,0,0),(8,8,'一天三次吃厄贝沙坦降压药',1743782400,1746288000,1,0,1,0,0);
/*!40000 ALTER TABLE `importantlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledgeentity`
--

DROP TABLE IF EXISTS `knowledgeentity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledgeentity` (
  `keId` bigint NOT NULL AUTO_INCREMENT COMMENT '知识实体ID，唯一标识知识库实体。',
  `keGUID` text NOT NULL COMMENT '知识实体GUID，用于命名知识实体存储目录。',
  `keFileType` text NOT NULL COMMENT '知识实体源文件类型，文件的拓展名。',
  `keName` text NOT NULL COMMENT '知识实体名称，展示时的标题。',
  `keCreateTime` text NOT NULL COMMENT '上传时间，Unix时间戳，精确到秒，服务器时间。',
  `keAbstract` text COMMENT '知识实体概要。',
  PRIMARY KEY (`keId`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3 COMMENT='知识实体表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledgeentity`
--

LOCK TABLES `knowledgeentity` WRITE;
/*!40000 ALTER TABLE `knowledgeentity` DISABLE KEYS */;
INSERT INTO `knowledgeentity` VALUES (4,'2d13a3b3-0b0f-43c0-979b-39639c37a6b4','application/pdf','医疗美容','1748738147','一本讲述医美行业概论的书籍'),(5,'57f863af-f1bf-447a-b10e-809b6e9e25f5','application/pdf','耳科学','1748769949','耳鼻喉科医师必备书籍'),(6,'a4f41bcd-39e5-44cb-8d2a-7c38ebae101f','application/pdf','国人健康手机号','1748771844','胡大一医生著作，能防止心血管疾病的手机号'),(7,'24724d07-a388-47bc-aa3f-dd42721cde73','application/pdf','内科学','1748771892','内科和全科医师必备书籍'),(8,'f28c6248-d0b6-44d2-9949-ff9d62fc3ba7','application/pdf','医学科学导论','1748772094','医学学生的入门书'),(9,'e0507ba2-de0b-44f6-861e-8d4e308dabd0','application/pdf','中医大科普','1748772119','面向百姓，科普中医'),(10,'361c1167-6fa1-45d9-be09-8f6b43b0a2ed','application/pdf','医疗美容','1748772145','一本讲述医美行业概论的书籍'),(11,'ebd23a20-a847-4fa0-9e6f-be32238b4bb4','application/vnd.openxmlformats-officedocument.wordprocessingml.document','耳科学','1748784413','耳鼻喉科医师必备书籍');
/*!40000 ALTER TABLE `knowledgeentity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `llmhistory`
--

DROP TABLE IF EXISTS `llmhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `llmhistory` (
  `sessionId` bigint NOT NULL AUTO_INCREMENT COMMENT '会话ID，唯一标识一个会话。',
  `isSessionDM` tinyint(1) NOT NULL COMMENT '会话是否启用大模型“讨论”机制。',
  `sessionSaveTime` text NOT NULL COMMENT '会话保存时间，Unix时间戳，精确到秒，服务器时间。',
  `sessionUserId` bigint NOT NULL COMMENT '会话所属用户ID。',
  `sessionContent` json NOT NULL COMMENT '会话内容，存储JSON格式。',
  PRIMARY KEY (`sessionId`),
  KEY `sessionUserId` (`sessionUserId`),
  CONSTRAINT `llmhistory_ibfk_1` FOREIGN KEY (`sessionUserId`) REFERENCES `userinfo` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3 COMMENT='大模型问答历史记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `llmhistory`
--

LOCK TABLES `llmhistory` WRITE;
/*!40000 ALTER TABLE `llmhistory` DISABLE KEYS */;
INSERT INTO `llmhistory` VALUES (1,0,'1743880042',8,'[{\"role\": \"assistant\", \"content\": \"你好，我是MKTY明康慧医大模型，我将为您解决医疗相关问题。\"}, {\"role\": \"user\", \"content\": \"一般局限性神经性皮炎传染吗？\"}, {\"role\": \"assistant\", \"content\": \"<p>补钙</p>\\n\"}]'),(2,0,'1743880754',8,'[{\"role\": \"assistant\", \"content\": \"你好，我是MKTY明康慧医大模型，我将为您解决医疗相关问题。\"}, {\"role\": \"user\", \"content\": \"用三个字介绍骨质疏松症。\"}, {\"role\": \"assistant\", \"content\": \"<p>脆、疏、裂</p>\\n\"}, {\"role\": \"user\", \"content\": \"请简单回答骨质疏松是否由缺钙导致。\"}, {\"role\": \"assistant\", \"content\": \"<p> <strong>明康慧医</strong> MKTY回答：<strong>是的</strong>，骨质疏松通常是由缺钙引起的。缺乏足够的钙和维生素D会导致骨质流失，从而引发骨质疏松症。此外，长期的不良生活习惯，如吸烟、饮酒、缺乏运动等也会增加患骨质疏松的风险。因此，建议您保持均衡的饮食，多摄入富含钙和维生素D的食物，并适当进行体育锻炼以维持骨骼健康。如果您有任何疑虑或需要更详细的建议，请咨询医生或营养师。</p>\\n\"}, {\"role\": \"user\", \"content\": \"谢谢你！\"}, {\"role\": \"assistant\", \"content\": \"<p>不客气，如果还有其他问题，欢迎随时向我提问！</p>\\n\"}]'),(4,0,'1743889388',8,'[{\"role\": \"assistant\", \"content\": \"你好，我是MKTY明康慧医大模型，我将为您解决医疗相关问题。\"}, {\"role\": \"user\", \"content\": \"红斑狼疮的发病机制是什么？\"}, {\"role\": \"assistant\", \"content\": \"<p>系统性红斑狼疮（Systemic lupus erythematosus，简称SLE）是一种主要由免疫系统异常激活，而攻击自身组织导致的慢性弥漫性结缔组织病。此病的具体病因尚不明确，但可能与遗传、环境因素与雌激素有关。长期的阳光曝晒、特定药物使用、感染、以及口服雌激素均可能诱发系统性红斑狼疮症状加重。此病易发于育龄女性，尤其是10到40岁的人群，女性发病率明显高于男性，约9:1。</p>\\n\"}]'),(5,0,'1745759091',8,'[{\"role\": \"assistant\", \"content\": \"你好，我是MKTY明康慧医大模型，我将为您解决医疗相关问题。\"}, {\"role\": \"user\", \"content\": \"有哪些常见的降压药？\"}, {\"role\": \"assistant\", \"content\": \"<p>补钙、抗骨吸收、促骨形成。</p>\\n\"}]'),(9,0,'1748531920',8,'[{\"role\": \"assistant\", \"content\": \"你好，我是MKTY明康慧医大模型，我将为您解决医疗相关问题。\"}, {\"role\": \"user\", \"content\": \"做个自我介绍。\"}, {\"role\": \"assistant\", \"content\": \"<p>好的，请问您是哪个学校的呢？我是 <strong>明康慧医</strong> 大模型（ <strong>MKTY</strong> Healthcare LLM），由齐鲁工业大学（山东省科学院）的 <strong>杜宇</strong> 同学（No.202103180009，<a href=\\\"https://github.com/duyu09\\\">https://github.com/duyu09</a>, @duyu09）利用海量医学领域文本微调得到。我被用于明康慧医系统（英语：Minh Khoe Tue Y System），指导医学领域的诊断、治疗和药方开具。</p>\\n\"}]'),(15,1,'1749058363',8,'[\"请深入研究骨质疏松症的发病原因及治疗方法。\", {\"title\": \"第1轮 智能体1讨论\", \"content\": \"<p> <strong>明康慧医</strong> MKTY大模型回答：骨质疏松症是一种常见的骨骼疾病，主要表现为骨量减少和骨结构的破坏，导致骨骼脆弱易碎，容易发生骨折。其发病原因主要包括以下几点：</p>\\n<ol>\\n<li><p>遗传因素：遗传基因对骨质疏松症的发生有重要的影响。</p>\\n</li>\\n<li><p>年龄增长：随着年龄的增长，人体内的激素水平会发生变化，特别是雌激素和睾酮的水平下降，这会导致骨质流失加快。</p>\\n</li>\\n<li><p>营养不良：钙、磷、维生素D等营养素的缺乏或摄入不足，也会增加骨质疏松症的风险。</p>\\n</li>\\n<li><p>缺乏运动：长期缺乏运动会导致肌肉力量下降，从而增加骨折的风险。</p>\\n</li>\\n<li><p>其他因素：如吸烟、过量饮酒、某些药物（如皮质类固醇）的使用等，也可能会增加骨质疏松症的风险。</p>\\n</li>\\n</ol>\\n<p>针对骨质疏松症的治疗，主要有以下几种方法：</p>\\n<ol>\\n<li><p>药物治疗：常用的药物包括双磷酸盐类药物、降钙素、雌激素、选择性雌激素受体调节剂等。</p>\\n</li>\\n<li><p>运动疗法：适当的运动可以帮助增强骨骼密度，预防骨折。推荐的运动包括负重运动、抗阻运动等。</p>\\n</li>\\n<li><p>饮食调整：保证足够的钙和维生素D的摄入，可以促进骨骼健康。</p>\\n</li>\\n<li><p>生活方式调整：戒烟、限酒、保持健康的体重等，也可以帮助预防骨质疏松症。</p>\\n</li>\\n</ol>\\n<p>总之，骨质疏松症是一种需要综合治疗的疾病，患者应根据自身情况，选择合适的治疗方案，并在医生的指导下进行治疗。</p>\\n\"}, {\"title\": \"第1轮 智能体2讨论\", \"content\": \"<p> <strong>明康慧医</strong> MKTY大模型回答：骨质疏松症是一种常见的骨骼疾病，其发病原因主要包括遗传因素、年龄增长、缺乏运动、营养不良、激素水平下降等。治疗方法主要包括药物治疗、物理治疗和生活方式改变。药物治疗包括抗骨质疏松药物、钙剂、维生素D等。物理治疗可以采用理疗、按摩等方式缓解疼痛。生活方式改变则需要加强锻炼、保持健康的饮食习惯、避免过度饮酒和吸烟等不良习惯。此外，定期进行骨密度检测也是非常重要的，以便及时发现和处理骨质疏松症。</p>\\n\"}, {\"title\": \"第1轮 主持人总结\", \"content\": \"我支持 **明康慧医** MKTY大模型的第2个观点。骨质疏松症的主要发病原因是激素水平下降，特别是雌激素和睾酮的水平下降，这会导致骨质流失加快。此外，遗传因素、年龄增长、缺乏运动、营养不良等因素也会增加骨质疏松症的风险。治疗方法主要包括药物治疗、物理治疗和生活方式改变。药物治疗包括抗骨质疏松药物、钙剂、维生素D等。物理治疗可以采用理疗、按摩等方式缓解疼痛。生活方式改变则需要加强锻炼、保持健康的饮食习惯、避免过度饮酒和吸烟等不良习惯。此外，定期进行骨密度检测也是非常重要的，以便及时发现和处理骨质疏松症。\"}, {\"title\": \"第2轮 智能体1讨论\", \"content\": \"<p> <strong>明康慧医</strong> MKTY大模型回答：骨质疏松症是一种常见的骨骼疾病，主要表现为骨量减少和骨结构的破坏，导致骨骼脆弱易碎，容易发生骨折。其发病原因主要包括以下几点：</p>\\n<ol>\\n<li><p>遗传因素：遗传基因对骨质疏松症的发生有重要的影响。</p>\\n</li>\\n<li><p>年龄增长：随着年龄的增长，人体内的激素水平会发生变化，特别是雌激素和睾酮的水平下降，这会导致骨质流失加快。</p>\\n</li>\\n<li><p>营养不良：钙、磷、维生素D等营养素的缺乏或摄入不足，也会增加骨质疏松症的风险。</p>\\n</li>\\n<li><p>缺乏运动：长期缺乏运动会导致肌肉力量下降，从而增加骨折的风险。</p>\\n</li>\\n<li><p>其他因素：如吸烟、过量饮酒、某些药物（如皮质类固醇）的使用等，也可能会增加骨质疏松症的风险。</p>\\n</li>\\n</ol>\\n<p>针对骨质疏松症的治疗，主要有以下几种方法：</p>\\n<ol>\\n<li><p>药物治疗：常用的药物包括双磷酸盐类药物、降钙素、雌激素、选择性雌激素受体调节剂等。</p>\\n</li>\\n<li><p>运动疗法：适当的运动可以帮助增强骨骼密度，预防骨折。推荐的运动包括负重运动、抗阻运动等。</p>\\n</li>\\n<li><p>饮食调整：保证足够的钙和维生素D的摄入，可以促进骨骼健康。</p>\\n</li>\\n<li><p>生活方式调整：戒烟、限酒、保持健康的体重等，也可以帮助预防骨质疏松症。</p>\\n</li>\\n</ol>\\n<p>总之，骨质疏松症是一种需要综合治疗的疾病，患者应根据自身情况，选择合适的治疗方案，并在医生的指导下进行治疗。</p>\\n\"}, {\"title\": \"第2轮 智能体2讨论\", \"content\": \"<p> <strong>明康慧医</strong> MKTY大模型回答：骨质疏松症是一种常见的骨骼疾病，其发病原因主要包括遗传因素、年龄增长、缺乏运动、营养不良、激素水平下降等。治疗方法主要包括药物治疗、物理治疗和生活方式改变。药物治疗包括抗骨质疏松药物、钙剂、维生素D等。物理治疗可以采用理疗、按摩等方式缓解疼痛。生活方式改变则需要加强锻炼、保持健康的饮食习惯、避免过度饮酒和吸烟等不良习惯。此外，定期进行骨密度检测也是非常重要的，以便及时发现和处理骨质疏松症。</p>\\n\"}, {\"title\": \"第2轮 主持人总结\", \"content\": \"我支持 **明康慧医** MKTY大模型的第1个观点。骨质疏松症是一种常见的骨骼疾病，其发病原因主要包括遗传因素、年龄增长、缺乏运动、营养不良、激素水平下降等。治疗方法主要包括药物治疗、物理治疗和生活方式改变。药物治疗包括抗骨质疏松药物、钙剂、维生素D等。物理治疗可以采用理疗、按摩等方式缓解疼痛。生活方式改变则需要加强锻炼、保持健康的饮食习惯、避免过度饮酒和吸烟等不良习惯。此外，定期进行骨密度检测也是非常重要的，以便及时发现和处理骨质疏松症。\"}, {\"title\": \"判敛结果：讨论不收敛（79.26%）\", \"content\": \"智能体讨论结束，若干智能体未达成共识，最后一轮收敛指标：0.792571896533174（约为79.26%），小于您设置的阈值。\"}]');
/*!40000 ALTER TABLE `llmhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailitem`
--

DROP TABLE IF EXISTS `mailitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mailitem` (
  `mailItemId` bigint NOT NULL AUTO_INCREMENT COMMENT '留言信息Id',
  `mailFromUserId` bigint NOT NULL COMMENT '留言者用户Id',
  `mailToUserId` bigint NOT NULL COMMENT '被留言者UserId',
  `mailItemContent` text NOT NULL COMMENT '留言信息文本内容',
  `mailItemStatus` int NOT NULL COMMENT '留言条目状态；0=正常；1=被删除；2=其他',
  `mailItemSendTime` bigint NOT NULL COMMENT '留言条目发送时间，以秒为单位的Unix时间戳',
  PRIMARY KEY (`mailItemId`),
  KEY `mailitem_userinfo_userId_fk` (`mailToUserId`),
  KEY `mailitem_userinfo_userId_fk2` (`mailFromUserId`),
  CONSTRAINT `mailitem_userinfo_userId_fk2` FOREIGN KEY (`mailFromUserId`) REFERENCES `userinfo` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户留言表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailitem`
--

LOCK TABLES `mailitem` WRITE;
/*!40000 ALTER TABLE `mailitem` DISABLE KEYS */;
INSERT INTO `mailitem` VALUES (1,2,8,'这里是MKTY智慧医疗系统',0,1740156315),(2,3,8,'Xin chào, làm thế nào để phòng ngừa loãng xương?',0,1740156338),(3,4,8,'Hiểu Ngữ，你的账单快来拿！',0,1740156340),(4,6,8,'这个MKTY智慧医疗系统真不错',0,1740156340),(6,8,2,'你好！这是测试语句。',1,1740156315),(7,8,3,'你好！这是测试语句。',0,1740156315),(8,8,4,'你好！这是测试语句。',1,1740156315),(9,8,6,'嗨！',1,1740848256),(10,8,6,'我的天啊！\n你太可爱了！',0,1740848469),(11,8,7,'局限性神经性皮炎抹卤米松软膏治疗',0,1741018981),(12,8,6,'哎哟哟你太可爱了吧！',0,1741536746),(13,8,7,'一般腿疼是怎么回事啊？',0,1742637125),(14,8,7,'测试留言01',0,1743800738),(15,8,9,'你的中文名叫啥？',0,1745481135),(16,7,6,'如果天生就是高度近视，那么手术可以治疗吗？',0,1748843712);
/*!40000 ALTER TABLE `mailitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicalrecord`
--

DROP TABLE IF EXISTS `medicalrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicalrecord` (
  `medrecId` bigint NOT NULL AUTO_INCREMENT COMMENT '病历ID，每个电子病历唯一编码。',
  `medrecCreateTime` text NOT NULL COMMENT '病历创建时间，Unix时间戳，精确到秒，服务器时间。',
  `medrecModifyTime` text NOT NULL COMMENT '病历修改时间，Unix时间戳，精确到秒，服务器时间。',
  `medrecPatientId` bigint NOT NULL COMMENT '病历所属患者ID。',
  `medrecDoctorId` bigint NOT NULL COMMENT '病历负责人（医师）ID。',
  `medrecAbstract` text COMMENT '病历概要，简洁描述病历。',
  `medrecState` text NOT NULL COMMENT '病历状态: 0 - 正常生效，1 - 痊愈无效，2 - 慢性病优先级降低。',
  `medrecContent` text NOT NULL COMMENT '病历内容，Markdown格式。',
  PRIMARY KEY (`medrecId`),
  KEY `medrecMainDoctorId` (`medrecDoctorId`),
  KEY `medrecPatientId` (`medrecPatientId`),
  CONSTRAINT `medicalrecord_ibfk_1` FOREIGN KEY (`medrecPatientId`) REFERENCES `userinfo` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `medicalrecord_ibfk_2` FOREIGN KEY (`medrecDoctorId`) REFERENCES `userinfo` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COMMENT='电子病历表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicalrecord`
--

LOCK TABLES `medicalrecord` WRITE;
/*!40000 ALTER TABLE `medicalrecord` DISABLE KEYS */;
INSERT INTO `medicalrecord` VALUES (1,'1748970187','1748971182',7,8,'测试','1','rrewreew'),(2,'1748975264','1749046360',7,8,'骨质疏松症','0','# 骨质疏松症\n\n### 基本信息\n- **姓名**：Vuong Du Huyen\n- **性别**：女  \n- **年龄**：68岁  \n- **主诉**：腰背部疼痛2年，加重伴身高缩短3cm  \n\n### 现病史\n- 近2年无诱因腰背痛，久坐/负重后加重  \n- 无外伤史，1年前曾发生桡骨远端骨折（跌倒后）  \n- 日常活动受限，未规范治疗  \n\n### 危险因素\n- 绝经年龄：50岁  \n- 长期低钙饮食  \n- 少晒太阳  \n- 母亲有髋部骨折史  \n\n### 检查\n- **骨密度（DXA）**：L1-L4 T值 -3.2，股骨颈 T值 -2.8  \n- **X线**：腰椎多椎体楔形变  \n- **实验室**：血钙磷正常，25-OH-VitD 18 ng/ml（↓）  \n\n### 诊断\n原发性骨质疏松症（严重）  \n');
/*!40000 ALTER TABLE `medicalrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usercollectionke`
--

DROP TABLE IF EXISTS `usercollectionke`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usercollectionke` (
  `recId` bigint NOT NULL AUTO_INCREMENT COMMENT '记录ID，唯一标识一条收藏记录。',
  `userId` bigint NOT NULL COMMENT '用户ID，表示该记录关于哪位用户。',
  `keId` bigint NOT NULL COMMENT '知识实体ID，表示用户收藏的知识实体。',
  PRIMARY KEY (`recId`),
  KEY `keId` (`keId`),
  KEY `userId` (`userId`),
  CONSTRAINT `usercollectionke_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `userinfo` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `usercollectionke_ibfk_2` FOREIGN KEY (`keId`) REFERENCES `knowledgeentity` (`keId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COMMENT='用户收藏的知识实体表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usercollectionke`
--

LOCK TABLES `usercollectionke` WRITE;
/*!40000 ALTER TABLE `usercollectionke` DISABLE KEYS */;
INSERT INTO `usercollectionke` VALUES (2,8,4),(3,8,5),(4,8,10),(5,8,9),(6,8,11);
/*!40000 ALTER TABLE `usercollectionke` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userinfo` (
  `userId` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID，每个用户的唯一编码，注册时随机生成。',
  `userCiphertext` text NOT NULL COMMENT '用户密码的加密值。',
  `userName` text NOT NULL COMMENT '用户姓名。',
  `userType` text NOT NULL COMMENT '用户类型: 0 - 患者, 1 - 医师, 2 - 其他。',
  `userSex` tinyint(1) NOT NULL COMMENT '用户性别: True - 男性, False - 女性。',
  `userSexPermission` tinyint(1) NOT NULL COMMENT '用户性别查看权限，0=公开；1=仅自己可见',
  `userAge` text NOT NULL COMMENT '用户年龄，以文本存储。',
  `userAgePermission` tinyint(1) NOT NULL COMMENT '用户年龄查看权限，0=公开；1=仅自己可见',
  `userFrom` text NOT NULL COMMENT '用户来源地，患者填写城市，医师填写机构名称。',
  `userFromPermission` tinyint(1) NOT NULL COMMENT '用户来源地查看权限，0=公开；1=仅自己可见',
  `userContact` text NOT NULL COMMENT '用户联系方式，电话号码或邮箱。',
  `userContactPermission` tinyint(1) NOT NULL COMMENT '用户联系方式查看权限，0=公开；1=仅自己可见',
  `userDescription` text COMMENT '用户自述，限制字数1024字符。',
  `patientImportantInfo` text COMMENT '患者特有信息，慢性病、过敏、家族遗传病史记录等。',
  `doctorImportantInfo` text COMMENT '医师特有信息，科室与擅长专业。',
  `userImportantInfoPermission` tinyint(1) NOT NULL COMMENT '用户重要信息查看权限，0=公开；1=仅自己可见',
  `userAvatarId` text COMMENT '用户头像ID，头像ID为GUID。',
  `userRegisterTime` bigint NOT NULL COMMENT '用户注册时间（服务器时间，以秒为单位的Unix时间戳）',
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COMMENT='用户信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinfo`
--

LOCK TABLES `userinfo` WRITE;
/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
INSERT INTO `userinfo` VALUES (1,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Quynh Trang 01','0',1,0,'28',1,'Tuy Hoa, Phu Yen, Viet Nam.',0,'nocont_02',1,'暂无','暂无','暂无',0,'c18fed32-8539-44af-9856-19c59a58ab3c',1739718610),(2,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Nguyen Thuy Trang','0',1,0,'28',1,'Việt Nam',0,'nocont_03',1,'暂无','暂无','暂无',0,'a84ca57a-fe4e-4415-9de5-633103efe51b',0),(3,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Du Yu','1',0,1,'23',1,'山东省济南市',1,'202103180009@stu.qlu.edu.cn',1,'我是杜宇！','全科','全科',1,'a4cee919-47ba-4656-9d47-128c3b8eb4ec',0),(4,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Du Yu','1',0,0,'23',0,'山东省济南市',1,'202103180009@test_01',1,'我是杜宇，大佬一枚','全科医师','全科医师',1,'f0c2f99f-9e31-4e67-ae89-acf7520b4176',1739718610),(5,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Du Yu','1',0,1,'23',1,'山东省济南市',1,'all_test',1,'我是杜宇，大佬一枚','全科医师','全科医师',1,'e904e3e2-9404-4af0-abca-1e2c5ff7094a',1739724987),(6,'$argon2id$v=19$m=65536,t=3,p=4$0IfTpnUjOsZ+WyKfK0gc2A$SztOUFVuCtHsTvb+ZaABkKBQdW5TbemYLDVLQhKdAu0','Quynh Trang','1',1,0,'28',0,'越南社会主义共和国 富安省 绥和市',0,'qt',1,'Em la Quynh Trang, Mot de thuong con gai.','我是小琼庄，可爱的小琼庄！','我是小琼庄，可爱的小琼庄！',0,'08a73583-aa0b-4e06-9174-bb5d121322d4',1739958202),(7,'$argon2id$v=19$m=65536,t=3,p=4$DVwrJenwmDQUqgyepcnDfw$nolevPIWh+SgfUpZywNUXTbIaU8SxnnVXBf2PSNm0w8','Vuong Du Tuyen','0',1,0,'23',1,'越南社会主义共和国 西贡 (胡志明市)',0,'w',1,'我更可爱！','暂无重要信息。','暂无重要信息。',0,'927660de-0138-476e-a63d-4e778ae248c1',1740082921),(8,'$argon2id$v=19$m=65536,t=3,p=4$UQdEStJvxl6193tRRpu66g$e5JAHNhiA3mFf+osCt34Zn0MyK1U3wqt28cKjWUCX3k','Ly Hieu Ngu','1',0,0,'22',1,'中国 山东省 德州市',1,'test',0,'我是 Lý Hiểu Ngữ，你也可以叫我 Li Xiaoyu 或 Нодикнй，来自中华人民共和国山东省德州市，我是无所不能的小dễ thương Tony，啥病都会看！','我是 Lý Hiểu Ngữ，你也可以叫我 Li Xiaoyu 或 Нодикнй，来自中华人民共和国山东省德州市，我是无所不能的小dễ thương Tony，啥病都会看！','我是 Lý Hiểu Ngữ，你也可以叫我 Li Xiaoyu 或 Нодикнй，来自中华人民共和国山东省德州市，我是无所不能的小dễ thương Tony，啥病都会看！',0,'b842b7e9-ed1d-4651-a62f-c33da03a2a6d',1740156011),(9,'$argon2id$v=19$m=65536,t=3,p=4$YZH895OCrwKXz9WZEYMxfQ$C7C9kBWUvgi0beBRZAHIGXq2fTLlOK/N28ehF6NNapM','Нодикнй','0',0,0,'23',0,'越南社會主義共和國 富安省 綏和市',0,'lxy',0,'我是Нодикный','我是Нодикный','我是Нодикный',0,'e7920405-7b1d-4ef9-8dac-4c49cd9140f4',1745480901);
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-13 21:50:38
