<template>
    <div>
      <canvas ref="chartCanvas" class="w-full h-64"></canvas>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, defineProps } from "vue";
import { Chart, LinearScale, CategoryScale, BarElement, BarController, Title, Tooltip, Legend } from "chart.js";

// Register required Chart.js components
Chart.register(LinearScale, CategoryScale, BarElement, BarController, Title, Tooltip, Legend);

const props = defineProps({
    chartData: Object,
    chartOptions: Object
});

// Refs
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

// Methods
const createChart = () => {
    if (chartCanvas.value) {
        chartInstance = new Chart(chartCanvas.value, {
        type: "bar", // Bar chart type
        data: props.chartData,
        options: props.chartOptions,
        });
    }
};

const destroyChart = () => {
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
};

// Watch for changes in chartData and recreate the chart
watch(
    () => props.chartData,
    () => {
        destroyChart();
        createChart();
    },
    { deep: true }
);

onMounted(() => {
    createChart();
    });
  </script>
  