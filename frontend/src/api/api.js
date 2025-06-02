/*
 - Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)
 - 该文件为“明康慧医MKTY”智慧医疗系统API JS文件。该文件为MKTY系统的重要组成部分。
 - 创建日期：2025年02月22日
 - 修改日期：2025年04月06日
*/
import axios from "axios";
import Cookies from 'js-cookie';
import { errHandle, msgHandle } from "@/utils/tools";
const baseURL='http://localhost:5555/api';
export
{
    loginVerification, register, setToken, getToken, removeToken, setCookie, getCookie, removeCookie, convertBlobToBase64,
    getUserAvatar, getUserInfo, modifyUserInfo, modifyUserAvatar, modifyUserPassword, getMailList, getMailList_Reverse, 
    deleteMailItem, addMailItem, multimodalDiagnosisSubmitTask, multimodalDiagnosisGetStatus, getCurrentTime,
    getImportantList, addImportantItem, deleteImportantItem, finishImportantItem, llmInferenceGetStatus, llmInferenceSubmitTask, 
    saveLlmSession, getLlmSession, getLlmSessionList, deleteLlmSession, addForum, getForumList, deleteForum, 
    modifyForumType, sendPost, getPostList, getPostContent, praisePost, deletePost, getForumInfo, exportChatToPDF, sendEmail,
    tsbbModelSubmitTask, tsbbInferenceGetStatus, 
    
    // 知识库管理相关API
    createKnowledgeEntity, searchKnowledgeEntities, downloadKnowledgeEntity, favoriteKnowledgeEntity, getUserFavorites, searchKnowledgePieces,

    setUserInformation, updataInformation, setAvatar, addFlag, showFlag, deleteFlag, showOrg, deleteOrg, creatForum, createOrg, releaseItem, showForum, showItem, deleteItem, showPsy, signIn, readSignInContext, readStudyRoom, startStudy, readStudyStatus, dredgePsy, skillTest, upvote, upload, showFile, downloadFile, getMusicList
}

function convertBlobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result);
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
}

function setCookie(key, value){
    Cookies.set(key, value);
}

function getCookie(key){
    return Cookies.get(key);
}

// 写入token到cookie,成功返回0，失败返回1.
function setToken(token)
{
    if(token==undefined){
        errHandle("身份验证出现了错误。");
        return 1;
    }
    else{
        Cookies.set("token",token);
        return 0;
    }
}

// 从cookie里删除键key
function removeCookie(key){
    Cookies.remove(key);
}

function removeToken(){
    Cookies.remove("token");
}

// 从cookie里读取token, 成功返回token,失败弹窗，并跳转至登录页。
function getToken()
{
    const token=Cookies.get("token");
    if(token==undefined || token==""){
        errHandle("您尚未登录或您的登录状态已过期。");
        // msgHandle("您尚未登录或您的登录状态已过期。");
        setTimeout(()=>{},1500);
        //跳转至登录页面。
        window.location.href = "/Login";
        return undefined;
    }
    else return "Bearer " + token;
}

// 01.用户登录
function loginVerification(userLoginKey, userLoginKeyType, userPassword)
{
    return axios.post(baseURL+'/loginVerification',{
        'userLoginKey': userLoginKey,
        'userLoginKeyType': userLoginKeyType,
        'userPassword': userPassword
    });
};

// 02.用户注册
function register(userName, userType, userSex, userSexPermission, userAge, userAgePermission, userFrom, userFromPermission, userContact, userContactPermission, userDescription, userImportantInfo, userImportantInfoPermission, userPassword, userAvatar)
{
    return axios.post(baseURL+'/register',{
        'userName': userName,
        'userType': userType,
        'userSex': userSex,
        'userSexPermission': userSexPermission,
        'userAge': userAge,
        'userAgePermission': userAgePermission,
        'userFrom': userFrom,
        'userFromPermission': userFromPermission,
        'userContact': userContact,
        'userContactPermission': userContactPermission,
        'userDescription': userDescription,
        'userImportantInfo': userImportantInfo,
        'userImportantInfoPermission': userImportantInfoPermission,
        'userPassword': userPassword,
        'userAvatar': userAvatar
    });
}

// 03.获取用户头像
function getUserAvatar(aimUserId)
{
    return axios.post(baseURL+'/getUserAvatar',{
        'userId': aimUserId,
    },{headers: {'Authorization': getToken()}})
}

// 04.获取用户基本信息
function getUserInfo(aimUserId) {
    return axios.post(baseURL+'/getUserInfo',{
        'userId': aimUserId
    },{headers: {'Authorization': getToken()}});
}

// 05.修改用户基本信息（不包括密码修改与头像更换）
function modifyUserInfo(userName, userType, userSex, userSexPermission, userAge, userAgePermission, userFrom, userFromPermission, userContact, userContactPermission, userDescription, userImportantInfo, userImportantInfoPermission)
{
    return axios.post(baseURL+'/modifyUserInfo',{
        'userName': userName,
        'userType': userType,
        'userSex': userSex,
        'userSexPermission': userSexPermission,
        'userAge': userAge,
        'userAgePermission': userAgePermission,
        'userFrom': userFrom,
        'userFromPermission': userFromPermission,
        'userContact': userContact,
        'userContactPermission': userContactPermission,
        'userDescription': userDescription,
        'userImportantInfo': userImportantInfo,
        'userImportantInfoPermission': userImportantInfoPermission
    },{headers: {'Authorization': getToken()}});
}

// 06.修改用户头像
function modifyUserAvatar(userAvatar)
{
    return axios.post(baseURL+'/modifyUserAvatar',{
        'userAvatar': userAvatar
    },{headers: {'Authorization': getToken()}});
}

// 07.修改用户密码
function modifyUserPassword(userOldPassword, userNewPassword)
{
    return axios.post(baseURL+'/modifyUserPassword',{
        'userOldPassword': userOldPassword,
        'userNewPassword': userNewPassword
    },{headers: {'Authorization': getToken()}});
}

// 08. 获取留言列表（读取别人发给自己的留言）
function getMailList()
{
    return axios.post(baseURL+'/getMailList',{
        'mode': 1,
    },{headers: {'Authorization': getToken()}});
}

// 09. 获取留言列表（读取自己发给别人的留言）
function getMailList_Reverse()
{
    return axios.post(baseURL+'/getMailList',{
        'mode': 0,
    },{headers: {'Authorization': getToken()}});
}

// 10. 删除留言
function deleteMailItem(mailItemId)
{
    return axios.post(baseURL+'/deleteMailItem',{
        'mailItemId': mailItemId,
    },{headers: {'Authorization': getToken()}});
}

// 11. 发送留言
function addMailItem(mailItemContent, mailItemReceiverUserId)
{
    return axios.post(baseURL+'/addMailItem',{
        'mailItemContent': mailItemContent,
        'mailItemReceiverUserId': mailItemReceiverUserId
    },{headers: {'Authorization': getToken()}});

}

// 12. 多模态辅诊-提交任务
function multimodalDiagnosisSubmitTask(language, texts, imageBase64)
{
    return axios.post(baseURL+'/multimodalDiagnosisSubmitTask',{
        'language': language,
        'texts': texts,
        'imageBase64': imageBase64
    },{headers: {'Authorization': getToken()}});
}

// 13. 多模态辅诊-查询任务状态
function multimodalDiagnosisGetStatus(taskId)
{
    return axios.post(baseURL+'/multimodalDiagnosisGetStatus',{
        'taskId': taskId
    },{headers: {'Authorization': getToken()}});
}


// 14. 获取服务器当前时间戳（以秒为单位，Unix时间戳）
function getCurrentTime() 
{
    return axios.post(baseURL+'/getCurrentTime');
}


// 15. 获取用户医疗事项列表
function getImportantList()
{
    return axios.post(baseURL+'/getImportantList',{
    },{headers: {'Authorization': getToken()}});
}

// 16. 添加诊疗事项
function addImportantItem(listItemContent, listItemTimeMode, listItemTimeWeek, listItemStartTime, listItemEndTime, listItemPriority, listItemIsFinished)
{
    return axios.post(baseURL+'/addImportantItem',{
        'listItemContent': listItemContent,
        'listItemTimeMode': listItemTimeMode,
        'listItemTimeWeek': listItemTimeWeek,
        'listItemStartTime': listItemStartTime,
        'listItemEndTime': listItemEndTime,
        'listItemPriority': listItemPriority,
        'listItemIsFinished': listItemIsFinished
    },{headers: {'Authorization': getToken()}});
}

// 17. 删除诊疗事项
function deleteImportantItem(listItemId)
{
    return axios.post(baseURL+'/deleteImportantItem',{
        'listItemId': listItemId
    },{headers: {'Authorization': getToken()}});
}

// 18. 标记医疗事项是否完成
function finishImportantItem(listItemId, listItemIsFinished)
{
    return axios.post(baseURL+'/finishImportantItem',{
        'listItemId': listItemId,
        'listItemIsFinished': listItemIsFinished
    },{headers: {'Authorization': getToken()}});
}

// 19. 提交大语言模型(MKTY-3B-Chat)推理任务
function llmInferenceSubmitTask(context, prompt)
{
    return axios.post(baseURL+'/llmInferenceSubmitTask',{
        'context': context,
        'prompt': prompt
    },{headers: {'Authorization': getToken()}});
}

// 20. 获取大语言模型推理任务状态
function llmInferenceGetStatus(taskId)
{
    return axios.post(baseURL+'/llmInferenceGetStatus',{
        'taskId': taskId
    },{headers: {'Authorization': getToken()}});
}

// 21. 保存MKTY大语言模型会话
function saveLlmSession(sessionId, sessionContent, isSessionDM)
{
    return axios.post(baseURL+'/saveLlmSession',{
        'sessionId': sessionId,
        'sessionContent': sessionContent,
        'isSessionDM': isSessionDM
    },{headers: {'Authorization': getToken()}});
}

// 22. 获取指定ID的MKTY大语言模型会话内容
function getLlmSession(sessionId)
{
    return axios.post(baseURL+'/getLlmSession',{
       'sessionId': sessionId
    },{headers: {'Authorization': getToken()}});
}

// 23. 获取指定用户的MKTY大语言模型会话列表
function getLlmSessionList(isSessionDM)
{
    return axios.post(baseURL+'/getLlmSessionList',{
      'isSessionDM': isSessionDM
    },{headers: {'Authorization': getToken()}});
}

// 24. 删除指定ID的MKTY大语言模型会话（数据库级真删除）
function deleteLlmSession(sessionId)
{
    return axios.post(baseURL+'/deleteLlmSession',{
      'sessionId': sessionId
    },{headers: {'Authorization': getToken()}});
}

// 25. 创建论坛（论坛列表的“增”操作）
function addForum(forumName, forumType, forumPermission)
{
    return axios.post(baseURL+'/addForum',{
        'forumName': forumName,
        'forumType': forumType,
        'forumPermission': forumPermission
    },{headers: {'Authorization': getToken()}}); 
}

// 26. 获取论坛列表（论坛列表的“查”操作）
function getForumList(forumType, forumPermission)
{
    return axios.post(baseURL+'/getForumList',{
        'forumType': forumType,
        'forumPermission': forumPermission
    },{headers: {'Authorization': getToken()}});
} 

// 27. 修改论坛类型（论坛列表的“改”操作）
function modifyForumType(forumId, forumType)
{
    return axios.post(baseURL+'/modifyForumType',{
        'forumId': forumId,
        'forumType': forumType
    },{headers: {'Authorization': getToken()}});
}

// 28. 删除论坛（论坛列表的“删”操作）
function deleteForum(forumId)
{
    return axios.post(baseURL+'/deleteForum',{
        'forumId': forumId
    },{headers: {'Authorization': getToken()}});
}

// 29. 在论坛发布帖子
function sendPost(forumId, postContent, postImagesBase64List)
{
    return axios.post(baseURL+'/sendPost',{
        'forumId': forumId,
        'postContent': postContent,
        'postImagesBase64List': postImagesBase64List
    },{headers: {'Authorization': getToken()}});
}

// 30. 获取指定论坛的帖子列表
function getPostList(forumId)
{
    return axios.post(baseURL+'/getPostList',{
        'forumId': forumId
    },{headers: {'Authorization': getToken()}});
}

// 31. 获取指定帖子ID的具体内容
function getPostContent(postId)
{
    return axios.post(baseURL+'/getPostContent',{
        'postId': postId
    },{headers: {'Authorization': getToken()}});
}

// 32. 给指定帖子点赞
function praisePost(postId)
{
    return axios.post(baseURL+'/praisePost',{
        'postId': postId
    },{headers: {'Authorization': getToken()}});
}

// 33. 删除帖子
function deletePost(postId)
{
    return axios.post(baseURL+'/deletePost',{
        'postId': postId
    },{headers: {'Authorization': getToken()}});
}

// 34. 获取指定Id的论坛信息元数据
function getForumInfo(forumId)
{
    return axios.post(baseURL+'/getForumInfo',{
        'forumId': forumId
    },{headers: {'Authorization': getToken()}});
}

// 35. 导出聊天记录到PDF
function exportChatToPDF(sessionId)
{
    return axios.post(baseURL+'/exportChatToPDF',{
        'sessionId': sessionId
    },{headers: {'Authorization': getToken()}, responseType: 'blob'});
}

// 36. 发送邮件
function sendEmail(content, receiver, subject)
{
    return axios.post(baseURL+'/sendEmail',{
        'content': content,
        'receiver': receiver,
        'subject': subject
    },{headers: {'Authorization': getToken()}});
}

// 37. 提交判敛任务或时序预测模型推理任务
function tsbbModelSubmitTask(taskType, taskLanguage, taskData)
{
    return axios.post(baseURL+'/tsbbModelSubmitTask',{
        'taskType': taskType,
        'taskLanguage': taskLanguage,
        'taskData': taskData
    },{headers: {'Authorization': getToken()}});
}

// 38. 判敛/时序预测任务状态查询
function tsbbInferenceGetStatus(taskId)
{
    return axios.post(baseURL+'/tsbbInferenceGetStatus',{
        'taskId': taskId
    },{headers: {'Authorization': getToken()}});
}














//04.注册用户基本信息
function setUserInformation(userName,userNickname,userSex,userSchool,userMajor,userSelfIntroduction,userPassword,userAvatar) {
    return axios.post(baseURL+'/setUserInformation',{
        "userName": userName,
        "userNickname": userNickname,
        "userSex": userSex,
        "userSchool": userSchool,
        "userMajor": userMajor,
        "userSelfIntroduction": userSelfIntroduction,
        "userPassword": userPassword,
        "userAvatar": userAvatar,
        "userRegisterTime": Date.now()
    });
    
}

//04-02.修改用户的基本信息
function updataInformation(userId,userName,userNickname,userSex,userSchool,userMajor,userSelfIntroduction,userPassword)
{
    return axios.post(baseURL+'/updataInformation',{
        "userId":userId,
        "userName": userName,
        "userNickname": userNickname,
        "userSex": userSex,
        "userSchool": userSchool,
        "userMajor": userMajor,
        "userSelfIntroduction": userSelfIntroduction,
        "userPassword": userPassword
    },{headers:{'Authorization':getToken()}});
}

//05.设置用户头像
function setAvatar(userId,imgData) {
    return axios.post(baseURL+'/setAvatar',{
        "userId":userId,
        "imgData":imgData
    },{headers:{'Authorization':getToken()}})
}


//08.添加目标
function addFlag(userId,context) {
    return axios.post(baseURL+'/addFlag',{
        "userId":userId,
        "context":context
    },{headers:{'Authorization':getToken()}})
}

//09.展示目标
function showFlag(userId,aimUserId)
{
    return axios.post(baseURL+'/showFlag',{
        'userId':userId,
        'aimUserId':aimUserId
    },{headers:{'Authorization':getToken()}})
}

//10.删除目标
function deleteFlag(userId,id)
{
    return axios.post(baseURL+'/deleteFlag',{
        'userId':userId,
        'id':id
    },{headers:{'Authorization':getToken()}})
}

//11.12.13

//14.学生组织列表
function showOrg(userId)
{
    return axios.post(baseURL+'/showOrg',{
        'userId':userId
    },{headers:{'Authorization':getToken()}})
}

//15.删除组织
function deleteOrg(userId,Id)
{
    return axios.post(baseURL+'/deleteOrg',{
        'userId':userId,
        'Id':Id
    },{headers:{'Authorization':getToken()}})
}

//16.创建论坛
function creatForum(userId,name,attrib)
{
    return axios.post(baseURL+'/creatForum',{
        'userId':userId,
        'name':name,
        'attrib':attrib
    },{headers:{'Authorization':getToken()}});
}

//16-02.创建组织
function createOrg(userId,orgAttrib,orgName,orgDescription,orgRecruitment)
{
    return axios.post(baseURL+'/creatOrg',{
        'userId':userId,
        "orgAttrib": orgAttrib,
        "orgName": orgName,
        "orgDescription": orgDescription,
        "orgRecruitment":orgRecruitment,
        "orgAddTime":Date.now()
    },{headers:{'Authorization':getToken()}});
}

//17.发布帖子或纳新信息
function releaseItem(userId,forumId,context)
{
    return axios.post(baseURL+'/releaseItem',{
        'userId':userId,
        'forumId':forumId,
        'context':context,
    },{headers:{'Authorization':getToken()}})
}

//18.展示论坛列表
function showForum(userId)
{
    return axios.post(baseURL+'/showForum',{
        'userId':userId
    },{headers:{'Authorization':getToken()}})
}

//19.帖子与纳新项目表
function showItem(forumId)
{
    return axios.post(baseURL+'/showItem',{
        "forumId":forumId,
    },{headers:{'Authorization':getToken()}})
}

//20.删除帖子或纳新信息
function deleteItem(userId,Id)
{
    return axios.post(baseURL+'/deleteItem',{
        'userId':userId,
        'Id':Id
    },{headers:{'Authorization':getToken()}})
}

//21.心理焦虑疏导模块
// function () {
//
// }

//22.心理疏导使用记录
function showPsy(userId)
{
    return axios.post(baseURL+'/showPsy',{
        'userId':userId
    },{headers:{'Authorization':getToken()}})
}

//23.略

//24.用户签到
function signIn(userId,context)
{
    return axios.post(baseURL+'/signIn',{
        'userId':userId,
        'context':context
    },{headers:{'Authorization':getToken()}})
}

//25.读取签到状态
function readSignInContext(userId)
{
    return axios.post(baseURL+'/readSignInContext',{
        'userId':userId
    },{headers:{'Authorization':getToken()}})
}

//26.读取自习楼状况
function readStudyRoom(userId,floor)
{
    axios.post(baseURL+'/readStudyRoom',{
        'userId':userId,
        'floor':floor
    },{headers:{'Authorization':getToken()}})
}

//27.开始自习
function startStudy(floor,site,startTime,context,encourage,length)
{
    return axios.post(baseURL+'/startStudy',{
        "floor": floor,
        "site": site,
        "startTime": startTime,
        "context": context,
        "encourage": encourage,
        "length": length
    },{headers:{'Authorization':getToken()}})
}

//28.读取自习状态或强制结束自习
function readStudyStatus(userId,operation)
{
    return axios.post(baseURL+'/readStudyStatus',{
        "userId":userId,
        "operation":operation
    },{headers:{'Authorization':getToken()}});
}

//psy小智同学机器人
function dredgePsy(userId,inputContext)
{
    return axios.post(baseURL+'/dredgePsy',{
        "inputContext":inputContext
    },{headers:{'Authorization':getToken()}});
}

//技术与能力检测模块
function skillTest(userId,workMode,expectSalary,expectCity,expectJob,inputContext)
{
    return axios.post(baseURL+'/skillTest',{
        "userId":userId,
        "workMode":workMode,
        "expectSalary":expectSalary,
        "expectCity":expectCity,
        "expectJob":expectJob,
        "inputContext":inputContext
    },{headers:{'Authorization':getToken()}});
}

//评论点赞
function upvote(userId,id)
{
    return axios.post(baseURL+'/upvote',{
        "userId":userId,
        "id":id
    },{headers:{'Authorization':getToken()}})
}

//上传资源
function upload(formData)
{
    return axios.post(baseURL+'/upload',formData,
        {headers:{'Authorization':getToken(),'content-type':'multipart/form-data'}});
}

//获取资源列表
function showFile(userId)
{
    return axios.post(baseURL+'/showFile',{
        "userId":userId
    },{headers:{'Authorization':getToken()}});

}

//下载资源
function downloadFile(id)
{
    window.location=baseURL+'/download?id='+id;
}

//从AutumnFish获取音乐信息JSON
function getMusicList(context)
{
    return axios.get('https://autumnfish.cn/search?keywords='+context);
}










// 知识库管理相关API函数

// 创建知识实体
function createKnowledgeEntity(keName, keAbstract, fileContent, fileType) {
    return axios.post(baseURL + '/knowledge/create', {
        keName: keName,
        keAbstract: keAbstract,
        fileContent: fileContent,
        fileType: fileType
    }, {headers: {'Authorization': getToken()}});
}

// 搜索知识实体
function searchKnowledgeEntities(keyword) {
    return axios.post(baseURL + '/knowledge/search', {
        keyword: keyword
    }, {
        headers: {
            'Authorization': getToken()
        }
    });
}

// 下载知识实体文件
function downloadKnowledgeEntity(keId) {
    const token = getToken();
    window.open(baseURL + '/knowledge/download/' + keId + '?token=' + token, '_blank');
}

// 收藏知识实体
function favoriteKnowledgeEntity(keId) {
    return axios.post(baseURL + '/knowledge/favorite', {
        keId: keId
    }, {
        headers: {
            'Authorization': getToken()
        }
    });
}

// 获取用户收藏的知识实体
function getUserFavorites() {
    return axios.get(baseURL + '/knowledge/favorites', {
        headers: {
            'Authorization': getToken()
        }
    });
}

// 搜索知识实体片段
function searchKnowledgePieces(keId, queryText, topK = 3) {
    return axios.post(baseURL + '/knowledge/search_pieces', {
        keId: keId,
        queryText: queryText,
        topK: topK
    }, {
        headers: {
            'Authorization': getToken()
        }
    });
}