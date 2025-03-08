<script>
import { Position } from "@element-plus/icons-vue";
import { Search } from "@element-plus/icons-vue";
import Cookies from 'js-cookie'
import {showOrg} from "../../api/api";
import {convertTime, errHandle} from "../../utils/tools";

export default
{
  name: "JoinOrg",
  components:
      {
        'Position':Position,
        'Search':Search,
      },
  data()
  {
    return{
      userId:0,
      Search:Search,
      OrgData:[],
      OrgData_Temp:[],
      SearchBoxContext:'',
      currentPage:1,
      pageSize:4,
      SelectId:0,
      dialogFormVisible:false,
      SelectedId:-1,
      SelectedName:'',
      SelectedRecruitment:'',
      loading:true,
      Items_Arr:[
          "公告内容01","公告内容02","公告内容03",
      ],
    }
  },
  mounted()
  {
    this.userId=Cookies.get('userId');
    showOrg(this.userId).then(res=>{
      const co=res.data.code;
      if(co!==0)
      {
        console.log(co);
        errHandle('错误：您未登录或因其他原因导致无法拉取学生组织信息表');
        return;
      }
      const orgJ=res.data.data;
      const orgA=[];
      for(const i02 in orgJ)
      {
        const i =orgJ[i02];
        let item={'id':0,'name':'null','classify':'null','time':'1970年01月01日','context':'null','recruitment':'null'};
        item.id=i.id;
        item.name=i.name;
        item.recruitment=i.recruitment;
        if(i.attrib===0) { item.classify='学生会';}
        else if(i.attrib===1) { item.classify='技术与学术类';}
        else if(i.attrib===2) { item.classify='创业类';}
        else {item.classify='文娱兴趣类';}
        item.time=convertTime(i.time);
        item.context=i.context;
        orgA.push(item);
      }
      //console.log(orgA);
      orgA.sort((a,b)=>{return a.id-b.id;});
      this.OrgData_Temp=orgA;
      this.OrgData=this.OrgData_Temp;
      //
      this.loading=false;
    }).catch(res=>{
      errHandle('拉取学生组织信息失败：'+res);
    });

  },
  methods:
      {
        SearchBoxChange()
        {
          var fd_temp=[];
          this.currentPage=1;
          this.OrgData_Temp.forEach((item) =>
              {
                if(item.name.includes(this.SearchBoxContext)||item.classify.includes(this.SearchBoxContext))
                {
                  fd_temp.push(item);
                }
              }
          );
          this.OrgData=fd_temp;
        },
        ClickOrg(id,name,recruitment)
        {
          this.SelectedId=id;
          this.SelectedName=name;
          this.SelectedRecruitment=recruitment;
          this.dialogFormVisible=true;
        }

      }
}
</script>

<template>
  <div id="OrgOverview-MainDiv" v-loading="loading" element-loading-text="加载中..." element-loading-background="rgba(0, 0, 0, 0.2)">
    <div>
      <el-input
          v-model="SearchBoxContext"
          class="w-50 m-2"
          placeholder="搜索您感兴趣的学生组织"
          :suffix-icon="Search"
          style="width: 50%;"
          @keyup="SearchBoxChange()"
      />
    </div>
    <div class="OrgOverview-TableItem"
         v-for="item in OrgData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
    >
      <div class="OrgOverview-TableItemLeft">
        <div class="OrgOverview-TableItemNameLabel">学生组织名称:</div>
        <div class="OrgOverview-TableItemName" @click="()=>{this.ClickOrg(item.id,item.name,item.recruitment);}">
          <el-popover
              placement="top-start"
              title="社团简介"
              :width="200"
              trigger="hover"
              :content="item.context"
          >
            <template #reference>
              <div>
                <el-icon><Position /></el-icon>
                {{ item.name }}
              </div>
            </template>
          </el-popover>
        </div>
      </div>
      <div class="OrgOverview-TableItemRight">
        <div><b>组织编号：</b>{{ item.id }}</div>
        <div><b>所属类别：</b>{{ item.classify }}</div>
        <div><b>创建时间：</b>{{ item.time }}</div>
      </div>
    </div>


    <div style="margin-top: 2rem;text-align: right;margin-left: 1rem;">
      <el-pagination background layout="prev, pager, next"
                     :total=this.OrgData.length
                     v-model:page-size="pageSize"
                     v-model:current-page="currentPage"
      />
    </div>



<!--    <el-button text @click="dialogFormVisible = true">-->
<!--      open a Form nested Dialog-->
<!--    </el-button>-->

    <el-dialog v-model="dialogFormVisible" title="纳新详细信息">
      <el-card class="box-card" style="max-height: 16rem;overflow: auto;">
        <template #header>
          <div class="card-header">
            <span><b>{{ SelectedName }}</b>&nbsp;讨论与纳新公告区:</span>
            <el-button class="button" text>申请加入该组织</el-button> <!-- 在此处使用SelectedId, 写加入组织逻辑。 -->
          </div>
        </template>
<!--        <div v-for="o in 50" :key="o" class="text item">{{ 'List item ' + o }}</div>-->
        <div>
          {{ SelectedRecruitment }}
        </div>
      </el-card>
      <br>
<!--      <el-input v-model="input" placeholder="参与讨论 或 发布公告" />-->
<!--      <br><br>-->
<!--      <el-button type="success" round>发布消息</el-button>-->
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false" type="primary">关闭</el-button>
      </span>
      </template>
    </el-dialog>


  </div>
</template>

<style scoped>
@font-face
{
  font-family: ubuntu;
  src: url("../../assets/fonts/ubuntu.woff2");
}
#OrgOverview-MainDiv
{
  font-family: none,sans-serif;
}
.OrgOverview-TableItem
{
  display: flex;
  font-size: 1rem;
  padding-left: 1rem;
  padding-top: 1rem;
  padding-bottom: 0.75rem;
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.2);
}
.OrgOverview-TableItemLeft
{
  width: 60%;

}
.OrgOverview-TableItemRight
{
  color: #555555;
  font-family: ubuntu;
  font-size: 0.875rem;

}
.OrgOverview-TableItemNameLabel
{
  padding-bottom: 0.25rem;
  font-family: HPHS,serif;
  color: #555555;
}
.OrgOverview-TableItemName
{
  font-size: 1.5rem;
  display: flex;
  justify-content: left;
  align-items: center;
  font-family: font01,serif;
}
.OrgOverview-TableItemName:hover
{
  color: blue;
  font-style: italic;
  cursor: pointer;
}
</style>