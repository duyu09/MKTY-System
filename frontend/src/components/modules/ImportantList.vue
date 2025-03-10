<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统重要事项清单页面Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年03月10日 -->
<!-- 修改日期：2025年03月10日 -->
<script>
import ListHeader from "./ListHeader.vue";
import { ChatDotRound } from "@element-plus/icons-vue";
import { Clock } from "@element-plus/icons-vue";
import { InfoFilled } from "@element-plus/icons-vue";
import { Aim } from "@element-plus/icons-vue";

import { addFlag, deleteFlag, getToken, showFlag } from "@/api/api";
import { convertTime, errHandle, successHandle } from "@/utils/tools";

export default
{
  name: "ImportantList",
  components:
      {
        "ListHeader":ListHeader,
        "ChatDotRound":ChatDotRound,
        "Clock":Clock,
        "InfoFilled":InfoFilled,
        "Aim":Aim,
      },
  data()
  {
    return{
      userId:0,
      addAimDialogTableVisible:false,
      checkAimDialogTableVisible:false,
      deleteAimDialogTableVisible:false,
      comeTrueAimDialogTableVisible:false,
      comeTrueAimDialogTableContext:'',
      checkAimDialogTableContext:'',
      deleteAimDialogTableContext:'',
      deleteAimDialogTableId:0,
      addAimContext:'',
      Aims_Arr:[
        {"id":0,"context":"测试语句","time":"null"},
      ],
      loading:true,
    }
  },
  methods:
      {
        addAim(context)
        {
          if(context===''||context===undefined||context===null)
          {
            errHandle('您不能添加一个没有内容地目标哦！');
            return;
          }
          addFlag(this.userId,context).then(res=>{
            if(res.data.code===0)
            {
              successHandle('你已成功添加一个目标，祝你早日实现目标！');
              this.addAimDialogTableVisible = false;
              setTimeout(()=>{this.$router.go(0);},1234);
            }
            else { errHandle('添加目标失败。'); }
          }).catch(res=>{
            errHandle('添加目标失败：'+res);
          });
        },
        deleteAim(id)
        {
          deleteFlag(this.userId,id).then(res=>{
            if(res.data.code===0)
            {
              successHandle('移除目标项成功。');
              this.deleteAimDialogTableVisible=false;
              setTimeout(()=>{
                this.$router.go(0);
              },1234);
            }
            else
            {
              errHandle('移除目标项失败！');
              return;
            }
          }).catch(res=>{
            errHandle('移除目标项失败：'+res);
            return;
          });
        },
        comeTrueAim()
        {
          Cookies.set('AimContext',this.comeTrueAimDialogTableContext);
          this.$router.push('/main/StartStudy');
        }
      },
  mounted()
  {
    const userId=Cookies.get('userId');
    this.userId=userId;
    if(this.userId===0||this.userId===undefined||this.userId===null)
    {
      errHandle('您尚未登录或您的登录状态已过期。');
      return;
    }
    showFlag(userId,userId).then(res=>{
      const rCode=res.data.code;
      const rData=res.data.data;
      if(rCode!==0)
      {
        errHandle('未能成功拉取你的目标清单。');
        return;
      }
      let outArr=[];
      for(const i in rData)
      {
        let item={"id":0,"context":"null","time":"null"};
        item.id=rData[i].id;
        item.context=rData[i].context;
        item.time=convertTime(rData[i].time);
        outArr.push(item);
      }
      this.Aims_Arr=outArr;
      this.loading=false;

    }).catch(res=>{
      errHandle('拉取目标清单失败：'+res);
      this.loading=false;
      return;
    });

  }
}
</script>

<template>
  <div id="Aims-MainDiv">
    <div id="Aims-HeaderDiv">
      <ListHeader></ListHeader>
    </div>
    <div id="Aims-Div01">
      <div id="Aims-Div02">
        <div id="Aims-Div05">
          <div id="Aims-Div07">
          <span id="Aims-Span01">
            <el-icon><InfoFilled /></el-icon>
            我的目标数量：
            {{ Aims_Arr.length }}个目标有待完成。
          </span>
            <span id="Aims-Span02">
<!--            {{ Aims_Attrib }}-->
<!--            这里可能要写已完成目标数量-->
          </span>
          </div>
        </div>

      </div>
      <div id="Aims-Div03">
        <div id="Aims-ItemsDiv" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
          <div id="Aims-Div10">
            <div class="Aims-Class-Div11" v-for="item in Aims_Arr">
              <div class="Aims-Class-Div16">
                目标内容：
                <span style="font-weight: bolder;" @click="this.checkAimDialogTableContext=item.context;checkAimDialogTableVisible=true;">
                  {{ item.context }}
                </span>
              </div>
              <div class="Aims-Class-Div17">
                创建时间：{{ item.time }}
                <span class="Aims-Class-Span03">
                  <span class="Aims-Class-Span04" @click="comeTrueAimDialogTableContext=item.context;comeTrueAimDialogTableVisible=true;">去实现目标</span>&nbsp;
                  <span class="Aims-Class-Span04" @click="deleteAimDialogTableId=item.id;deleteAimDialogTableContext=item.context;deleteAimDialogTableVisible=true;">已达成目标</span>&nbsp;
                </span>
              </div>
            </div>
          </div>
        </div>

        <el-dialog v-model="checkAimDialogTableVisible" title="查看目标">
          <el-form>
            <el-form-item>
              目标具体内容：<span style="font-weight: bolder;">
              {{ this.checkAimDialogTableContext }}
            </span>
            </el-form-item>
          </el-form>
          <template #footer>
                    <span class="dialog-footer">
                      <el-button type="primary" @click="checkAimDialogTableVisible = false">
                        确定
                      </el-button>
                    </span>
          </template>
        </el-dialog>

        <el-dialog v-model="deleteAimDialogTableVisible" title="移除已实现的目标">
          <el-form>
            <el-form-item>
              你选择的目标内容是：<span style="font-weight: bolder;">
              {{ this.deleteAimDialogTableContext }}
            </span>
            </el-form-item>
            <el-form-item>
              你完成它了吗？如果已经完成，请从目标清单中去掉它吧！清单减少一项，知识增加十分！
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="deleteAimDialogTableVisible=false;">取消</el-button>
              <el-button type="primary" @click="deleteAim(this.deleteAimDialogTableId)">
                删除目标项
              </el-button>
            </span>
          </template>
        </el-dialog>


        <el-dialog v-model="comeTrueAimDialogTableVisible" title="实现目标">
          <el-form>
            <el-form-item>
              你选择的目标内容是：<span style="font-weight: bolder;">
              {{ this.comeTrueAimDialogTableContext }}
            </span>
            </el-form-item>
            <el-form-item>
              你即将前往ILP专属云自习室去学习，以完成该项目标。
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="comeTrueAimDialogTableVisible=false;">取消</el-button>
              <el-button type="primary" @click="comeTrueAim()">
                去自习室学习
              </el-button>
            </span>
          </template>
        </el-dialog>


      </div>

      <div id="Aims-Div18">
        <div id="Aims-Div19">
          <div id="Aims-Div20">
            <div id="PsyChat-Div06">
              <div id="PsyChat-Div07">
<!--                <input id="PsyChat-InputBox01" placeholder="尽情提问吧" v-model="Aims_Context" @keyup.enter="PsyChat_Send()" />-->
                <div id="PsyChat-SendButtonDiv" @click="()=>{this.addAimDialogTableVisible=true;}">
                  <el-icon><Aim /></el-icon>&nbsp;<span class="PsyChat-Span02">添加目标</span>
                </div>

                <el-dialog v-model="addAimDialogTableVisible" title="添加目标">
                  <el-form>
                    <el-form-item>
                      添加一个目标，请坚定信心 坚持不懈地完成它！
                    </el-form-item>
                    <el-form-item>
                      目标描述：<el-input v-model="addAimContext" placeholder="请写下待完成目标地具体内容" />
                    </el-form-item>
                  </el-form>
                  <template #footer>
                    <span class="dialog-footer">
                      <el-button @click="addAimDialogTableVisible = false;">取消</el-button>
                      <el-button type="primary" @click="addAim(this.addAimContext);">
                        确定添加
                      </el-button>
                    </span>
                  </template>
                </el-dialog>

              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
@font-face
{
  font-family: HPHS;
  src: url("../../assets/fonts/HPHS.woff");
}
#Aims-HeaderDiv
{
  width: 100%;
}
#Aims-MainDiv
{
  width: 100%;
  display: flex;
  flex-direction: column;
}
#Aims-Div01
{
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
}
#Aims-Div02
{
  font-family: HPHS, serif;
  height: 2rem;
  box-shadow: 0 0 0.8rem 0.25rem rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
}
#Aims-Div03
{
  display: flex;
  justify-content: center;
  height: calc(99.85vh - 9rem);
}
#Aims-Div04
{
  display: flex;
  align-items: center;
  height: 100%;
  margin-left: 1.75rem;
  font-size: 1.25rem;
}
#Aims-Div05
{
  height: 100%;
  margin-left: 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
#Aims-Div06
{
  font-size: 1.25rem;
}
#Aims-Div07
{
  font-size: 1rem;
  margin-top: 0.35rem;
  display: flex;
  align-items: center;
}
#Aims-Div08
{
  flex-grow: 1;
  text-align: right;
  margin-right: 2rem;
}
#Aims-Div09
{

}
#Aims-Div10
{
  display: flex;
  align-items:center;
  flex-direction: column;
}
.Aims-Class-Div11
{
  box-shadow: 0 5px 5px -5px #888888;
  width: 92.5%;
  min-height: 4.5rem;
}
.Aims-Class-Div11:hover
{
  background-color: rgba(240,240,240,1);
}
.Aims-Class-Div12
{
  display: flex;
  margin-top: 0.75rem;
}
.Aims-Class-Div13
{
  background-color: #3d93ff;
  height: 2.75rem;
  width: 2.75rem;
  border-radius: 2rem;
}
.Aims-Class-Div14
{
  margin-left: 1rem;
}
.Aims-Class-Div15
{
  color: #555555;
  font-size: 0.85rem;
  margin-top: 0.1rem;
}
.Aims-Class-Div16
{
  margin-left: 0.25rem;
  margin-top: 0.75rem;
  cursor: pointer;
}
.Aims-Class-Div16:hover
{
  /*font-weight: bolder;*/
  color: darkblue;
}
.Aims-Class-Div17
{
  margin-left: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.75rem;
}
#Aims-Div18
{
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 1.5rem;
  width:100%;
}
#Aims-Div19
{
  width: 90%;
}
#Aims-Div20
{

}
#Aims-Span01
{
  display: flex;
  align-items: center;
}
#Aims-Span02
{
  display: flex;
  align-items: center;
  margin-left: 1rem;
}
.Aims-Class-Span02
{
  font-weight: bolder;
  font-size: 1rem;
}
.Aims-Class-Span03
{
  left:90%;
  position: sticky;
  cursor: pointer;
}
.Aims-Class-Span04:hover
{
  color: darkblue;
  font-weight: bolder;
}
#Aims-ItemsDiv
{
  background-color:white;
  width: 90%;
  margin-top: 1.25rem;
  border-radius: 20px 20px 0 0;
  overflow: auto;
}
#PsyChat-Div06
{
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}
#PsyChat-Div07
{
  box-shadow: 0 0 0.8rem 0.075rem rgba(0,0,0,0.5);
  background-color: rgba(255,255,255,0.8);
  width:7.5rem;
  height: 2.5rem;
  border-radius: 15px;
  padding: 0.15rem 0.05rem;
  display: flex;
  margin-top: 1rem;
  justify-content: center;
}
#Aims-Image01
{
  border-radius: 4px;
  height: 3rem;
  width: 3rem;
  background-size: cover;
  box-shadow: 0 0.35rem 0.35rem 0 rgba(0,0,0,0.5);
}
.Aims-Class-Image02
{
  height: 100%;
  width:100%;
  border-radius: 10rem;
}
#PsyChat-InputBox01
{
  background-color: transparent;
  border: none;
  outline: none;
  width:85%;
  height: 100%;
  font-size: 1rem;
  text-indent: 0.75rem;
  font-family: HPHS, serif;
}
#PsyChat-InputBox01:focus
{
  border: none;
  outline: none;
}
#PsyChat-SendButtonDiv
{
  background-color: rgba(255,165,0,0.2);
  box-shadow: 0 0 0.35rem 0.05rem rgba(0,0,0,0.4);
  width: 95%;
  margin-top: 0.1rem;
  margin-bottom: 0.1rem;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
#PsyChat-SendButtonDiv:hover
{
  background-color: rgba(255,165,0,0.333);
}
#PsyChat-SendButtonDiv:active
{
  background-color: rgba(255,165,0,0.45);
}
.PsyChat-Span02
{
  cursor: pointer;
}
#Aims-ItemsDiv::-webkit-scrollbar
{
  display: none;
}

@media screen and (max-width: 40rem)
{
  #Aims-Div09
  {
    display: none;
  }


  /*#PsyChat-Span02 {*/
  /*  display: none;*/
  /*}*/

  #PsyChat-SendButtonDiv {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 0;
  }

  #PsyChat-Div07 {
    margin-bottom: 2rem;
  }
}
</style>