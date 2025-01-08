<template>
  <div class="flex flex-row min-w-full min-h-svh">
    <SideBar />
    <router-view/>
  </div>
</template>

<style lang="scss">
@import "./assets/scss/index.scss"
</style>

<script setup>
import SideBar from "@/components/SideBar.vue" ;
</script>
