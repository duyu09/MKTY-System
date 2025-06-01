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
            title: '明康慧医智慧医疗系统 - 用户信息'
          },
          component: () => import('@/components/modules/PersonalPage.vue'),
        },
        {
          path: 'PsyChat',
          name: 'PsyChat',
          meta: {
            title: '明康慧医 - 智慧医疗问答'
          },
          component: () => import('@/components/modules/PsyChat.vue'),
        },
        {
          path: 'PsyChatDM',
          name: 'PsyChatDM',
          meta: {
            title: '明康慧医 - AI智能体讨论解答疑问'
          },
          component: () => import('@/components/modules/PsyChatDM.vue'),
        },
        {
          path: 'Forum',
          name: 'Forum',
          meta: {
            title: 'MKTY专属医学与诊疗论坛平台'
          },
          component: () => import('@/components/modules/Forum.vue'),
        },
        {
          path: 'Resources',
          name: 'Resources',
          meta: {
            title: 'ILP大平台资源中心'
          },
          component: () => import('@/components/modules/Resources.vue'),
        },
        {
          path: 'ForumInner',
          name: 'ForumInner',
          meta: {
            title: 'MKTY专属医学与诊疗论坛平台'
          },
          component: () => import('@/components/modules/ForumInner.vue'),
        },
        {
          path: 'ImportantList',
          name: 'ImportantList',
          meta: {
            title: '重要事项清单 - 明康慧医系统'
          },
          component: () => import('@/components/modules/ImportantList.vue'),
        },
        {
          path: 'KnowledgeOverview',
          name: 'KnowledgeOverview',
          meta: {
            title: '知识库管理 - 明康慧医系统'
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
        title: '明康慧医智慧医疗系统 - 用户登录'
      },
      component: () => import('@/components/modules/Login.vue'),
    },
    {
      path:'/LoginMobile',
      name:'LoginMobile',
      meta: {
        title: '明康慧医智慧医疗系统 - 用户登录'
      },
      component: () => import('@/components/modules/LoginMobile.vue'),
    },
    {
      path:'/Register',
      name:'Register',
      meta: {
        title: '明康慧医智慧医疗系统 - 用户注册'
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
