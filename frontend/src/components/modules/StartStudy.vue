<script>
import {convertTimeChinese, errHandle} from "../../utils/tools";
import Cookies from "js-cookie";

export default
{
  name: "StartStudy",
  data()
  {
    return{
      "userId":0,
      "studyContext":'',
      "startTime":0,
      "length":60,
      "encourage":'',
      "nowTimeString":'null',
    }
  },
  mounted()
  {
    setInterval(()=>{
      this.startTime=Date.now();
      this.nowTimeString=convertTimeChinese(Date.now());
    },400);
    const aimContext=Cookies.get('AimContext');
    if(aimContext!==''&&aimContext!==undefined&&aimContext!==null)
    {
      this.studyContext=aimContext;
    }
  },
  methods:
      {
        start()
        {
          if(this.studyContext===''||this.encourage==='')
          {
            errHandle('自习内容以及鼓励自我的语言不能不写哦！');
            return;
          }
          Cookies.set('studyStatus',true);
          Cookies.set('studyStartTime',this.startTime);
          Cookies.set('studyLength',this.length);
          Cookies.set('studyLeftTimeUnix',this.length*60*1000);
          Cookies.set('studyEncourage',this.encourage);
          Cookies.set('studyContext',this.studyContext);
          this.$router.push('/StudyRoom');
        }

      }
}
</script>

<template>
<div id="ss-mainDiv">
  <div id="ss-div01">
    <div id="ss-div02">
      <div id="ss-div03">
        <span><nobr>欢迎来到ILP</nobr><wbr><nobr>大平台云自习室</nobr></span>
        <div id="ss-div04">
          <div class="ss-itemDiv">
            <span>{{ nowTimeString }}</span>
          </div>
          <div class="ss-itemDiv">
              请设置本次自习的时长：<el-input-number v-model="length" :step="5" :min="10" :max="300" /> 分钟
          </div>
          <div class="ss-itemDiv">
            请设置本次自习的内容：<el-input v-model="studyContext" placeholder="自习内容" clearable input-style="max-width:42.5%;" />
          </div>
          <div class="ss-itemDiv">
            说几句话鼓励一下自己！<el-input v-model="encourage" placeholder="加油哦！一定要专注，认真，细致！" clearable input-style="max-width:42.5%" />
          </div>
          <div class="ss-itemDiv">
            <el-button type="success" @click="start()">开始自习吧！</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
@font-face {
  font-family: xinwei02;
  src:url('/fonts/xinwei.woff');
}
@font-face {
  font-family: HPHS;
  src:url('/fonts/HPHS.woff');
}
#ss-mainDiv
{
  height: 100%;
  width:100%;
}
#ss-div01
{
  height: 100%;
  width:100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
#ss-div02
{
  width: 80%;
  height: calc(0.72 * 100vh);
  background-image: url("/images/10.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  border-radius: 24px;
  box-shadow: 0 0 0.8rem 0.4rem rgba(0,0,0,0.5);
}
#ss-div03
{
  text-align: center;
  font-family: xinwei02, serif;
  font-size: 2.25rem;
  margin-top: 0.75rem;
}
#ss-div04
{
  font-size: 1.2rem;
  font-family: HPHS, serif;
}
.ss-itemDiv
{
  margin-top: 1.25rem;
}
</style>