<template>
    <div class="side-bar w-1/6 min-h-full">
        <h1>MES</h1>
        <div class="container min-w-full min-h-svh">
            <router-link
            to="/"
            class="container-item min-w-full px-6 py-3"
            :class="{ 'selected': route.name === 'Dashboard' }"
            >
                <p>Dashboard</p>
            </router-link>
            <router-link 
            to="/production"
            class="container-item min-w-full px-6 py-3"
            :class="{ 'selected': route.name === 'Production' }"
            >
                <p>Production Tracking</p>
            </router-link>
            <router-link 
            to="/quality"
            class="container-item min-w-full px-6 py-3"
            :class="{ 'selected': route.name === 'Quality' }"
            >
                <p>Quality Control</p>
            </router-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

//data
const route = useRoute();


</script>