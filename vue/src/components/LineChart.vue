<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, defineProps } from "vue";
import { Chart, ChartData, ChartOptions, LineController, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from "chart.js";

// Register required Chart.js components
Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend);

const props = defineProps(['chartData', 'chartOptions']);

// Refs
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

// Methods
const createChart = () => {
if (chartCanvas.value) {
    chartInstance = new Chart(chartCanvas.value, {
    type: "line",
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

// Lifecycle hook
onMounted(() => {
createChart();
});
</script>
