<template>
    <div class="bg-white shadow-md rounded-lg p-4 border border-gray-200">
        <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-700">{{ title }}</h3>
            <img :src="icon" alt="Icon" class="h-8 w-8"/>
        </div>
        <p class="text-3xl font-bold text-gray-900 mt-4">{{ value }}</p>
        <p class="text-sm text-gray-500">{{ description }}</p>
    </div>
</template>
  
<script setup>
import { defineProps } from "vue";

const props = defineProps({
    title: String,
    value: [String, Number],
    description: String,
    icon: String
})
</script>

<style lang="scss">
@import "@/assets/scss/component.scss"
</style>