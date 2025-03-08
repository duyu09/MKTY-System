<script>
import { Position } from "@element-plus/icons-vue";
import { Search } from "@element-plus/icons-vue";
import Cookies from 'js-cookie'
import {showForum} from "../../api/api";
import {errHandle} from "../../utils/tools";

export default
{
  name: "ForumOverview.vue",
  components:
      {
        'Position':Position,
        'Search':Search,
      },
  data()
  {
    return{
      Search:Search,
      ForumData:[],
      ForumData_Temp:[],
      SearchBoxContext:'',
      currentPage:1,
      pageSize:4,
      SelectId:0,
    }
  },
  mounted()
  {
    const userId=Cookies.get('userId');
    let ForumA=[];
    showForum(userId).then(res=>{
      //console.log(res);
      let ForumJ=res.data.data;
      for(const i in ForumJ)
      {
        let item={'id':0,'name':'null','classify':'null','time':'1970-01-01 08:00:00'};
        item.id=ForumJ[i].id;
        item.name=ForumJ[i].name;
        if(ForumJ[i].attrib===0) { item.classify='其他类'; }
        else if(ForumJ[i].attrib===1) { item.classify='学术类'; }
        else if(ForumJ[i].attrib===2) { item.classify='技术类'; }
        else { item.classify='生活类'; }
        ForumA.push(item);
      }
      ForumA.sort((a,b)=>{ return a.id-b.id; });
      this.ForumData_Temp=ForumA;
      this.ForumData=this.ForumData_Temp;
    }).catch(res=>{
      errHandle('拉取论坛列表失败：'+res);
    });
  },
  methods:
      {
        SearchBoxChange()
        {
          var fd_temp=[];
          this.currentPage=1;
          this.ForumData_Temp.forEach((item) =>
              {
                if(item.name.includes(this.SearchBoxContext)||item.classify.includes(this.SearchBoxContext))
                {
                  fd_temp.push(item);
                }
              }
          );
          this.ForumData=fd_temp;
        },
        ClickForum()
        {
          const id=this.SelectId;
          Cookies.set('ForumId',id);
          this.$router.push("/main/ForumInner"); //跳转到论坛内部页面，并读取cookie.
        }

      }
}
</script>

<template>
<div id="ForumOverview-MainDiv">
  <div id="ForumOverview-SearchBoxDiv">
    <el-input
        v-model="SearchBoxContext"
        class="w-50 m-2"
        placeholder="搜索您感兴趣的论坛"
        :suffix-icon="Search"
        input-style="background-color: rgb(240,240,240);"
        @keyup="SearchBoxChange()"
    />
  </div>
  <div style="overflow: auto;">
  <div class="ForumOverview-TableItem"
       v-for="item in ForumData.slice((currentPage-1)*pageSize,currentPage*pageSize)"
  >
    <div class="ForumOverview-TableItemLeft">
      <div class="ForumOverview-TableItemNameLabel">
        论坛名称:<el-icon id="ForumOverview-Pos02"><Position /></el-icon>
      </div>
      <div class="ForumOverview-TableItemName" @click="()=>{this.SelectId=item.id;this.ClickForum();}">
        <el-icon id="ForumOverview-Pos01"><Position /></el-icon>{{ item.name }}
      </div>
    </div>
    <div class="ForumOverview-TableItemRight">
      <div><span style="font-weight: bolder;">论坛编号：</span><br class="ForumOverview-Br01">{{ item.id }}</div>
      <div><span style="font-weight: bolder;">所属类别：</span><br class="ForumOverview-Br01">{{ item.classify }}</div>
      <div><span style="font-weight: bolder;">等级：</span><br class="ForumOverview-Br01">优质论坛</div>
    </div>
  </div>
  </div>


  <div style="margin-top: 2rem;text-align: right;margin-left: 1rem;padding-bottom: 2.25rem;">
    <el-pagination background layout="prev, pager, next"
                   :total=this.ForumData.length
                   v-model:page-size="pageSize"
                   v-model:current-page="currentPage"
    />
  </div>

</div>
</template>

<style scoped>
@font-face
{
  font-family: ubuntu;
  src: url("../../assets/fonts/ubuntu.woff2");
}
#ForumOverview-MainDiv
{
  font-family: none,sans-serif;
}
#ForumOverview-SearchBoxDiv
{
  width: 50%;
}
#ForumOverview-Pos01
{
  display: inline;
}
#ForumOverview-Pos02
{
  display: none;
}
.ForumOverview-Br01
{
  display: none;
}
.ForumOverview-TableItem
{
  display: flex;
  font-size: 1rem;
  padding-left: 1rem;
  padding-top: 1rem;
  padding-bottom: 0.75rem;
  box-shadow: 0 4px 7px rgba(0, 0, 0, 0.2);
}
.ForumOverview-TableItem:hover
{
  background-color: rgb(243,243,243);
}
.ForumOverview-TableItemLeft
{
  width: 60%;
}
.ForumOverview-TableItemRight
{
  color: #555555;
  font-family: ubuntu;
  font-size: 0.875rem;

}
.ForumOverview-TableItemNameLabel
{
  padding-bottom: 0.25rem;
  font-family: HPHS,serif;
  color: #555555;
}
.ForumOverview-TableItemName
{
  font-size: 1.5rem;
  display: flex;
  justify-content: left;
  align-items: center;
  font-family: font01,serif;
}
.ForumOverview-TableItemName:hover
{
  color: blue;
  font-style: italic;
  cursor: pointer;
}
@media screen and (max-width: 40rem)
{
  #ForumOverview-SearchBoxDiv
  {
    width: 85%;
  }
  #ForumOverview-Pos01
  {
    display: none;
  }
  #ForumOverview-Pos02
  {
    display: inline;
  }
  .ForumOverview-TableItemName
  {
    font-size: 1.25rem;
  }
  .ForumOverview-TableItemNameLabel
  {
    display: flex;
    justify-content: left;
    align-items: center;
  }
  .ForumOverview-TableItemRight
  {
    font-size: 0.5rem;
  }
  .ForumOverview-Br01
  {
    display: inline;
  }
}
</style>