// Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences)
// 该文件为“明康慧医MKTY”智慧医疗系统前端路由配置文件。该文件为MKTY系统的重要组成部分。
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect:'/Login'
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('@/components/MainView.vue'),
      children:[
        {
          path: 'MultimodalDiagnosis',
          name: 'MultimodalDiagnosis',
          component: () => import('@/components/modules/MultimodalDiagnosis.vue'),
          meta: {
            title: '智能多模态诊断 - 明康慧医智慧医疗系统'
          }
        },
        {
          path: 'PersonalPage',
          name: 'PersonalPage',
          meta: {
            title: '用户信息 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/PersonalPage.vue'),
        },
        {
          path: 'PsyChat',
          name: 'PsyChat',
          meta: {
            title: '智慧医疗问答 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/PsyChat.vue'),
        },
        {
          path: 'PsyChatDM',
          name: 'PsyChatDM',
          meta: {
            title: 'AI智能体讨论解答疑问 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/PsyChatDM.vue'),
        },
        {
          path: 'Forum',
          name: 'Forum',
          meta: {
            title: 'MKTY专属医学与诊疗论坛平台 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/Forum.vue'),
        },
        {
          path: 'MedicalRecordOverview',
          name: 'MedicalRecordOverview',
          meta: {
            title: '病历概览 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/MedicalRecordOverview.vue'),
        },
        {
          path: 'MedicalRecordInner',
          name: 'MedicalRecordInner',
          meta: {
            title: '病历详情 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/MedicalRecordInner.vue'),
        },
        {
          path: 'ForumInner',
          name: 'ForumInner',
          meta: {
            title: 'MKTY专属医学与诊疗论坛平台 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/ForumInner.vue'),
        },
        {
          path: 'ImportantList',
          name: 'ImportantList',
          meta: {
            title: '重要事项清单 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/ImportantList.vue'),
        },
        {
          path: 'KnowledgeOverview',
          name: 'KnowledgeOverview',
          meta: {
            title: '知识库管理 - 明康慧医智慧医疗系统'
          },
          component: () => import('@/components/modules/KnowledgeOverview.vue'),
        },
        {
          path: 'HomePage',
          name: 'PersonPage',
          meta: {
            title: '欢迎使用明康慧医系统'
          },
          component: () => import('@/components/modules/HomePage.vue'),
        },

      ]
    },
    {
      path:'/Login',
      name:'Login',
      meta: {
        title: '用户登录 - 明康慧医智慧医疗系统'
      },
      component: () => import('@/components/modules/Login.vue'),
    },
    {
      path:'/LoginMobile',
      name:'LoginMobile',
      meta: {
        title: '用户登录 - 明康慧医智慧医疗系统'
      },
      component: () => import('@/components/modules/LoginMobile.vue'),
    },
    {
      path:'/Register',
      name:'Register',
      meta: {
        title: '用户注册 - 明康慧医智慧医疗系统'
      },
      component: () => import('@/components/modules/Register.vue'),
    },
    {
      path:'/:catchAll(.*)',
      name:'NotFound',
      meta: {
        title: '404 - 明康慧医智慧医疗系统'
      },
      component: ()=>import('@/components/modules/NotFound.vue'),
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  };
  next();
});
router.afterEach((to, from, next) => {
  if (to.path === '/Register' && from.path !== '/') {
    console.log(to.path, from.path)
    //location.reload()
  };
});

export default router;
