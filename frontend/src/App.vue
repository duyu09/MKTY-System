<script>
import { RouterLink, RouterView } from 'vue-router';
import MainView from "./components/MainView.vue";
export default
{
  components:
  {
    "MainView":MainView,
  },

}
</script>

<template>
  <RouterView></RouterView>
</template>

<style>
@font-face
{
  font-family: cons;
  src: url("../src/assets/fonts/consola.woff2");
}
pre > code
{
  font-family: cons !important;
  margin-top: 0.5rem !important;
  margin-bottom: 0.5rem !important;
  padding-top: 0.5rem !important;
  padding-bottom: 0.5rem !important;
  padding-left: 0.75rem !important;
  border-radius: 4px;
  font-size: 0.85em;
}
code
{
  font-family: cons !important;
}
</style>
