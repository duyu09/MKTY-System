<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统的前端用户注册页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年01月31日 -->
<!-- 修改日期：2025年02月20日 -->
<script>
import "@/assets/css/bootstrap.min.css";
import "@/assets/js/bootstrap.bundle.min.js";
import "@/assets/js/register.js";
import { errHandle, msgHandle } from "@/utils/tools";
import { register } from "@/api/api";
export default
{
  name: "Register",
  data()
  {
    return{
      userName:'',
      userType:-1,
      userSex:-1,
      userSexPermission:true, // true=仅自己可见；false=公开
      userAge:23,
      userAgePermission:true, // true=仅自己可见；false=公开
      userFrom:'',
      userFromPermission:true, // true=仅自己可见；false=公开
      userContact:'',
      userContactPermission:true, // true=仅自己可见；false=公开
      userDescription:'',
      userImportantInfo:'',
      userImportantInfoPermission:true, // true=仅自己可见；false=公开
      userPassword:'',
      userPassword02:'',
      userAvatar:'',
      userAvatar_final:'',
      userRegisterTime:0,
      dialogRIVisible:false,
      isChecked:true,
    }
  },
  computed:{
    userSex_text(){
      if(this.userSex===0){
        return '男性';
      }
      else if(this.userSex===1){
        return '女性';
      }
      else{
        return '<未选择>';
      }
    },
    userAge_text(){
      return this.userAge + ' 周岁';
    },
    userFrom_text(){
      const user_form_str = this.userFrom;
      return user_form_str.length > 7 ? `${user_form_str.slice(0, 7)}...` : user_form_str;
    },
    userContact_text(){
      const user_contact_str = this.userContact;
      return user_contact_str.length > 14 ? `${user_contact_str.slice(0, 14)}...` : user_contact_str;
    },
    userImportantInfo_text(){
      const user_important_info_str = this.userImportantInfo;
      return user_important_info_str.length > 7 ? `${user_important_info_str.slice(0, 7)}...` : user_important_info_str;
    },
    userSexPermission_text(){
      return this.userSexPermission ? '私密' : '公开';
    },
    userSexPermission_content(){
      return (this.userSex==-1) ? '<未选择>' : this.userSex_text;
    },
    userAgePermission_text(){
      return this.userAgePermission ? '私密' : '公开';
    },
    userAgePermission_content(){
      return (this.userAge==-1 || this.userAge=="") ? '<未填写>' : this.userAge_text;
    },
    userFromPermission_text(){
      return this.userFromPermission ? '私密' : '公开';
    },
    userFromPermission_content(){
      return (this.userFrom===''||this.userFrom==null) ? '<未填写>' : this.userFrom_text;
    },
    userContactPermission_text(){
      return this.userContactPermission ? '私密' : '公开';
    },
    userContactPermission_content(){
      return this.userContact===''? '<未填写>' : this.userContact_text;
    },
    userImportantInfoPermission_text(){
      return this.userImportantInfoPermission ? '私密' : '公开';
    },
    userImportantInfoPermission_content(){
      return this.userImportantInfo==='' ? '<未填写>' : this.userImportantInfo_text;
    }
  },
  methods:
      {
        writeImgData() {
          const fileBox=this.$refs.imgSelect;
          const Img = fileBox.files[0];
          const reader = new FileReader();
          reader.onloadend = () => {
            const fileContent = reader.result; // 获取文件内容
            if(fileContent.length>10*1024*1024) {
              msgHandle("您选择的图片过大(大于10MB)，无法处理。");
              fileBox.value = '';
              return;
            }
            this.userAvatar=fileContent;
            this.$refs.imgShow.src = fileContent;
            };
            try {
              reader.readAsDataURL(Img);
              const imgShowPic = this.$refs.imgShow;
              imgShowPic.onload = () => {
                this.userAvatar_final = this.getImgDataAsBase64(this.$refs.imgShow);
                // console.log(this.userAvatar_final);
              };
            }
            catch (e) {
              msgHandle('读取头像文件失败：'+e);
              this.$refs.imgShow.src = "/images/null_avatar.jpg"
            }
        },
        getImgDataAsBase64(img) {
          const canvas = document.createElement('canvas');
          canvas.width = 200;
          canvas.height = 200;
          const ctx = canvas.getContext('2d');
          const imgWidth = img.naturalWidth;
          const imgHeight = img.naturalHeight;
          const size = Math.min(imgWidth, imgHeight); // 取宽高中较小的值作为裁剪区域的边长
          const offsetX = (imgWidth - size) / 2;
          const offsetY = (imgHeight - size) / 2;
          ctx.drawImage(img, offsetX, offsetY, size, size, 0, 0, 200, 200);
          const base64String = canvas.toDataURL('image/webp');
          return base64String;
        },
        RegFunction()
        {
          if(this.userName===''||this.userName==null)
          {
            msgHandle("注册失败：您必须设置姓名");
            return;
          }
          if(this.userType==-1)
          {
            msgHandle("注册失败：请您选择用户类型");
            return;
          }
          if(this.userSex==-1)
          {
            msgHandle("注册失败：请您选择性别");
            return;
          }
          if(isNaN(parseInt(this.userAge))){
            msgHandle('注册失败：年龄必须填写阿拉伯数字');
            return;
          }
          if(this.userAge==='' || this.userAge==null || this.userAge<0)
          {
            msgHandle("注册失败：您必须设置符合条件的年龄");
            return;
          }
          if(this.userFrom===''||this.userFrom==null)
          {
            msgHandle("注册失败：您必须您的来源地");
            return;
          }
          if(this.userContact===''||this.userContact==null)
          {
            msgHandle("注册失败：您必须设置联系方式");
            return;
          }
          if (this.userDescription.length>1024 || this.userDescription==='' || this.userDescription==null)
          {
            msgHandle("注册失败：您未填写自述或您的自述过长");
            return;
          }
          if (this.userImportantInfo.length>1024 || this.userImportantInfo==='' || this.userImportantInfo==null)
          {
            msgHandle("注册失败：您未填写重要信息或您的重要信息过长");
            return;
          }
          if(this.userAvatar==='' || this.userAvatar==null)
          {
            msgHandle('注册失败：您需要设置头像');
            return;
          }
          if(this.userPassword===''||this.userPassword==null)
          {
            msgHandle('注册失败：您必须设置密码。');
            return;
          }
          if(this.userPassword!==this.userPassword02)
          {
            msgHandle('注册失败：您两次输入的密码不一致。');
            return;
          }
          if(this.isChecked===false)
          {
            msgHandle('注册失败：您必须阅读、同意注册须知并勾选。');
            return;
          }
          const userAgePermission = this.userAgePermission ? 1 : 0;
          const userSexPermission = this.userSexPermission ? 1 : 0;
          const userFromPermission = this.userFromPermission ? 1 : 0;
          const userContactPermission = this.userContactPermission ? 1 : 0;
          const userImportantInfoPermission = this.userImportantInfoPermission ? 1 : 0;
          register(this.userName,this.userType,this.userSex,userSexPermission,this.userAge,userAgePermission,this.userFrom,userFromPermission,this.userContact,userContactPermission,this.userDescription,this.userImportantInfo,userImportantInfoPermission,this.userPassword,this.userAvatar_final)
            .then(res=>{
                if(res.data.code===0){
                  msgHandle('注册成功').then(()=>{
                    msgHandle('您的MKTY大平台账号为：'+res.data.userId+" ，可用于登录，请您牢记！");
                  });
                }
                else{
                  msgHandle('注册失败：' + res.data.msg);
                }
              })
              .catch(res=>{
                msgHandle('注册失败：'+res);
              });
        }
      },
  mounted()
  {

  }
}
</script>

<template>
<div id="Register-MainDiv">
  <div class="container">
    <main>
      <div class="py-3 text-center">
        <img class="d-block mx-auto mb-4" src="/images/mkty_en_light.svg" alt="" width="550" height="120" id="logoImg">
        <div style="background-color: rgb(230,230,230); padding: 1.5rem; border-radius: 18px;">
        <h2><nobr><span style="font-family: hanwang,serif;font-size: larger;">明康慧醫&nbsp;<wbr>智慧醫療大平臺</span></nobr><wbr><nobr>&nbsp;个人账号注册</nobr></h2>
        <span class="lead" style="font-family: font01,serif;font-weight: lighter;">
          MKTY智慧医疗平台 AI新技术助力医疗行业发展 为医师减负 使患者安心！
        </span>
        </div>
      </div>
      <hr class="my-4">

      <div class="row g-5">
        <div class="col-md-7 col-lg-8">
          <h4 class="mb-3">基本信息填写</h4>
          <form class="needs-validation" novalidate>
            <div class="row g-3">

              <div class="col-sm-6">
                <label for="Name" class="form-label">您的真实姓名</label>
                <input type="text" class="form-control" id="Name" placeholder="" required v-model="userName">
                <div class="invalid-feedback">
                  您的姓名是必填项
                </div>
                <br>

                <label for="Type" class="form-label">用户类型</label>
                <select class="form-select" id="Type" required v-model="userType">
                  <option :value=-1>-请选择-</option>
                  <option :value=0>患者</option>
                  <option :value=1>医师</option>
                  <option :value=2>其他人员</option>
                </select>
                <div class="invalid-feedback">
                  您的用户类型选项是必填项
                </div>
              </div>

              <div class="col-md-4">
                <label for="Sex" class="form-label">您的性别</label>
                <select class="form-select" id="Sex" required v-model="userSex">
                  <option :value=-1>-请选择-</option>
                  <option :value=0>男</option>
                  <option :value=1>女</option>
                </select>
                <div class="invalid-feedback">
                  您的性别是必填项
                </div>
              </div>

              <div class="col-sm-4">
                <label for="Age" class="form-label">
                  <span v-if="this.userType===1">您的从医资历</span>
                  <span v-else>您的年龄</span>
                  <div class="text-muted">（阿拉伯数字）</div>
                </label>
                <div class="input-group">
                  <input type="text" class="form-control" id="Age" placeholder="" required v-model="userAge">
                  <span v-if="this.userType===1" class="input-group-text">年</span>
                  <span v-else class="input-group-text">周岁</span>
                </div>
                <div class="invalid-feedback">
                  您的年龄/资历是必填项
                </div>
                <br>
              </div>

              <div class="col-12">
                <label for="Contact" class="form-label">您的联系方式<span class="text-muted">（电话号码或电子邮箱，可用于登录，必须唯一）</span></label>
                <input type="text" class="form-control" id="Contact" placeholder="" required v-model="userContact">
                <div class="invalid-feedback">
                  您的联系方式是必填项
                </div>
              </div>

              <div class="col-12">
                <label for="From" class="form-label">来源地填写
                  <div class="text-muted" v-if="this.userType===0">（患者：请填写您所在的地区城市）</div>
                  <div class="text-muted" v-else-if="this.userType===1">（医师：请填写您所在的医疗机构名称）</div>
                </label>
                <input type="text" class="form-control" id="From" placeholder="" required v-model="userFrom">
                <div class="invalid-feedback">
                  您的来源地是必填项
                </div>
              </div>

              <div class="col-12">
                <label for="Description" class="form-label">用户自述<span class="text-muted">（1024字符内）</span></label>
                <div class="input-group">
                  <span class="input-group-text">用户<br>自述</span>
                  <textarea class="form-control" aria-label="Self Introduction" id="Description" v-model="userDescription"></textarea>
                </div>
              </div>

              <div class="col-12">
                <label for="ImportantInfo" class="form-label">
                  用户重要信息
                  <span class="text-muted">（1024字符内）</span>
                  <div class="text-muted" v-if="this.userType===0">（患者：请详细写明慢性病、过敏、家族遗传病史记录等重要信息）</div>
                  <div class="text-muted" v-else-if="this.userType===1">（医师：请填写您所在科室与擅长专业）</div>
                </label>
                <div class="input-group">
                  <span class="input-group-text">重要<br>信息</span>
                  <textarea class="form-control" aria-label="Self Introduction" id="ImportantInfo" v-model="userImportantInfo"></textarea>
                </div>
              </div>

            </div>
            <br>
            <div>
              <label for="imgSelect" class="form-label">头像设置</label>
              <div class="text-muted" style="margin-bottom: 0.75rem;">（请选择10MB以下图像，系统切分中心最大1:1部分作为头像）</div>
              <img src="/images/null_avatar.jpg" class="img-thumbnail" alt="请选择头像图片" style="width: 6rem;height: 6rem;border-radius: 0.8rem;object-fit: cover;" id="imgShow" ref="imgShow">
              <br><br>
              <div class="input-group">
                <input type="file" class="form-control" id="imgSelect" @change="writeImgData()" ref="imgSelect" aria-label="Upload" accept=".jpg,.jpeg,.png,.webp,.bmp,.gif,.ico">
              </div>  
            </div>

            <hr class="my-4">

            <h4 class="mb-3">密码设定</h4>


            <div class="col-12">
              <label for="password01" class="form-label">密码设定</label>
              <input type="password" class="form-control" id="password01" placeholder="Input Your Password" required v-model="userPassword">
              <div class="invalid-feedback">
                您必须设定密码
              </div>
              <br>

              <label for="password02" class="form-label">确认密码</label>
              <input type="password" class="form-control" id="password02" placeholder="Confirm Your Password" required v-model="userPassword02">
              <div class="invalid-feedback">
                您必须核实密码
              </div>
            </div>

            <hr class="my-4">

            <h4 class="mb-3">隐私权限设定</h4>
            <p class="text-muted">对于下列所有选项，您勾选意味着对应信息只有您自己可见，若取消勾选则可由所有已注册用户查看与检索。</p>
            <div class="form-check">
              <label class="form-check-label" for="check_sex_pm">
                您的性别信息（当前设定为：<span class="text-muted">{{ userSexPermission_content }}</span>；权限：<span class="text-muted">{{ userSexPermission_text }}</span>）
              </label>
              <input id="check_sex_pm" type="checkbox" class="form-check-input" checked v-model="userSexPermission">
            </div>

            <div class="form-check">
              <label class="form-check-label" for="check_age_pm">
                您的年龄信息（当前设定为：<span class="text-muted">{{ userAgePermission_content }}</span>；权限：<span class="text-muted">{{ userAgePermission_text }}</span>）
              </label>
              <input id="check_age_pm" type="checkbox" class="form-check-input" checked v-model="userAgePermission">
            </div>

            <div class="form-check">
              <label class="form-check-label" for="check_from_pm">
                您的来源地（当前设定为：<span class="text-muted">{{ userFromPermission_content }}</span>；权限：<span class="text-muted">{{ userFromPermission_text }}</span>）
              </label>
              <input id="check_from_pm" type="checkbox" class="form-check-input" checked v-model="userFromPermission">
            </div>

            <div class="form-check">
              <label class="form-check-label" for="check_contact_pm">
                您的联系方式（当前设定为：<span class="text-muted">{{ userContactPermission_content }}</span>；权限：<span class="text-muted">{{ userContactPermission_text }}</span>）
              </label>
              <input id="check_contact_pm" type="checkbox" class="form-check-input" checked v-model="userContactPermission">
            </div>

            <div class="form-check">
              <label class="form-check-label" for="check_important_pm">
                您的重要信息（当前设定为：<span class="text-muted">{{ userImportantInfoPermission_content }}</span>；权限：<span class="text-muted">{{ userImportantInfoPermission_text }}</span>）
              </label>
              <input id="check_important_pm" type="checkbox" class="form-check-input" checked v-model="userImportantInfoPermission">
            </div>

            <hr class="my-4">
            <h4 class="mb-3">用户承诺</h4>

            <div class="form-check">
              <label class="form-check-label" for="checkXY">
                您已充分阅读
                <a @click="dialogRIVisible = true;" style="color: #007bff;cursor: pointer;text-decoration: underline;">
                  《注册须知》
                </a>
                全文，并充分理解及同意其中的全部内容。
              </label>
              <input type="checkbox" class="form-check-input" id="checkXY" required checked v-model="isChecked">
            </div>

            <hr class="my-4">

          </form>
          <button class="w-100 btn btn-primary btn-lg" @click="RegFunction()">注册账号</button>
        </div>
      </div>
    </main>
    <footer class="my-5 pt-5 text-muted text-center text-small" style="padding-bottom: 2rem;">
      <p class="mb-1">&copy; 2023~2025 DU Yu (MKTY Developer)</p>
    </footer>
  </div>
</div>
<el-dialog v-model="dialogRIVisible" title="明康慧医MKTY智慧医疗系统账号注册须知" width="75%">
  <div style="height: 39vh; overflow-y: auto;overflow-x: auto;"><br>
  欢迎您注册使用明康慧医MKTY智慧医疗系统！<br>
  在注册账号并使用本系统之前，请您务必仔细阅读并充分理解本《账号注册须知》（以下简称“须知”）。您点击“注册账号”按钮，即视为您已阅读、理解并同意接受本须知的全部内容。<br>
  <hr class="my-4">
  <b>一、必要说明</b><br><br>
  1. 明康慧医MKTY智慧医疗系统（以下简称“本系统”）为个人毕业设计项目原型，旨在进行学术研究和技术演示，<b>并非正式发布的商业产品。</b><br>
  2. 本系统功能有限，目前仅用于毕业设计答辩和演示，<b>暂不适用于任何实际的医疗场景。</b><br>
  3. 开发者对“本系统不存在漏洞、错误及不完善之处”<b>不做保证。</b><br><br>
  <b>二、责任免除</b><br><br>
  1. 开发者声明：本人作为明康慧医MKTY智慧医疗系统的开发者，仅为完成齐鲁工业大学(山东省科学院)计算机科学与技术学部2025届毕业设计而开发此系统，不承担任何与用户使用本系统相关的责任。<br>
  2. 用户责任：用户应自行承担使用本系统所产生的一切后果，包括但不限于：<br>
  &nbsp;&nbsp;* 因系统漏洞、错误或不完善导致的任何损失；<br>
  &nbsp;&nbsp;* 因用户操作不当导致的任何损失；<br>
  &nbsp;&nbsp;* 因用户违反本须知导致的任何损失。<br>
  3. 免责范围：开发者不对以下情况承担任何责任：<br>
  &nbsp;&nbsp;* 用户因使用本系统而遭受的任何直接或间接损失；<br>
  &nbsp;&nbsp;* 用户因使用本系统而导致的任何人身伤害或财产损失；<br>
  &nbsp;&nbsp;* 用户因使用本系统而侵犯任何第三方权益。<br>
  <br>
  <b>三、其他条款</b><br><br>
  1. 本须知最终解释权归开发者所有。<br>
  2. 本须知自本系统开源之日起生效。<br>
  请您务必谨慎考虑并自行承担风险后再决定是否注册使用本系统。<br>
  <br>
  <b>开发者：杜宇</b> (英语：DU Yu；越南语：Đỗ Vũ)，齐鲁工业大学(山东省科学院)计算机科学与技术学部2025届本科毕业生<br>
  <b>生效日期：2025年02月03日</b><br>
  <b>电子邮箱：202103180009@stu.qlu.edu.cn</b><br>
  <hr class="my-4"><br>
  </div>
  <br>
  <el-button type="primary" @click="dialogRIVisible = false;isChecked = true;">已完整阅读并同意</el-button>
</el-dialog>
</template>

<style scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px)
{
  .bd-placeholder-img-lg
  {
    font-size: 3.5rem;
  }

}
@media (max-width: 768px) {
  #logoImg
  {
    width: 330px;
  }
}

.b-example-divider {
  height: 3rem;
  background-color: rgba(0, 0, 0, .1);
  border: solid rgba(0, 0, 0, .15);
  border-width: 1px 0;
  box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
}

.b-example-vr {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
}

.bi {
  vertical-align: -.125em;
  fill: currentColor;
}

.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
}

.nav-scroller .nav {
  display: flex;
  flex-wrap: nowrap;
  padding-bottom: 1rem;
  margin-top: -1px;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}
@font-face {
  font-family: hanwang;
  src: url('/fonts/hanwang.woff2');
}

@font-face {
  font-family: penxingshu;
  src: url('/fonts/penxingshu.woff');
}
@font-face {
  font-family: font01;
  src: url('/fonts/font01.woff2');
}
@font-face {
  font-family: ubuntu;
  src: url('/fonts/ubuntu.woff2');
}
@font-face {
  font-family: HPHS;
  src: url('/fonts/HPHS.woff');
}

.container
{
  max-width: 960px;
}

#Register-MainDiv
{
  font-family: ubuntu,'HPHS',serif;
  background-color: rgb(248,248,248);
}
</style>
