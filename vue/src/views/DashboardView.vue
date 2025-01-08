<template>
    <div class="dashboard flex w-5/6 max-h-max flex-col text-left mx-6 mt-3 gap-3">
        <h1 class="text-blue-950 font-extrabold">Dashboard</h1>
        <section class="flex grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Production Status -->
            <MetricsCard
            title="Production Progress"
            :value="`${metrics.productionProgress}%`"
            description="Completed production batches"
            :icon= "require('../assets/icon/icon-shield.svg')"
            >
            </MetricsCard>

            <!-- Production Line Status-->
            <div class="bg-white shadow-md rounded-lg p-4 border border-gray-200">
                <h3 class="text-lg font-semibold text-gray-700 mb-6">Production Line Status</h3>
                <div v-for="(production, index) in productionLine" :key="index" class="flex justify-between items-center">
                    <p class="text-m font-semibold text-black-500">{{ production.production }}</p>
                    <p v-if="production.status === 'Online'" class="text-sm text-green-500">{{ production.status }}</p>
                    <p v-else class="text-sm text-red-500">{{ production.status }}</p>
                </div>
            </div>

            <!-- Machine Utilization -->
            <MetricsCard
            title="Machine Utilization"
            :value="`${metrics.machineUtilization}%`"
            description="Average utilization of machines"
            :icon= "require('../assets/icon/icon-plus-sign-green.svg')"
            >
            </MetricsCard>

            <!-- Defect Rate -->
            <MetricsCard
            title="Defect Rate"
            :value="`${metrics.defectRate}%`"
            description="Defective units in production"
            :icon= "require('../assets/icon/icon-exclamation-triangle.svg')"
            >       
            </MetricsCard>
        </section>

        <!-- Real-Time Alerts -->
        <section class="my-6">
            <h2 class="text-xl font-bold mb-4">Real-Time Alerts</h2>
            <ul class="bg-white shadow-md rounded-lg p-4 border border-gray-200">
            <li v-for="(alert, index) in alerts" :key="index" class="mb-2">
                <p class="text-gray-700">
                <span class="font-semibold" style="color:red">{{ alert.type }}</span>: {{ alert.message }}
                </p>
                <p class="text-sm text-gray-500">{{ alert.timestamp }}</p>
            </li>
            </ul>
        </section>

        <!-- Chart Section -->
        <div class="flex flex-col mb-6">
            <h2 class="text-xl font-semibold mb-4">Production Progress</h2>
                <LineChart class="shadow-md rounded-lg p-4 border border-gray-200" :chartData="productionData"  :chartOptions="chartOptions"/>
        </div>
        <div class="flex flex-row gap-3 mb-6">
            <!-- Machine Utilization -->
            <div class="bg-white w-1/2">
                <h2 class="text-xl font-semibold mb-4">Machine Utilization</h2>
                <BarChart class="shadow-md rounded-lg p-4 border border-gray-200" :chartData="machineUtilizationData" :chartOptions="chartOptions"/>
            </div>

            <!-- Product Defect Rates -->
            <div class="bg-white w-1/2">
                <h2 class="text-xl font-semibold mb-4">Product Defect Rates</h2>
                <LineChart class="shadow-md rounded-lg p-4 border border-gray-200" :chartData="defectRatesData"  :chartOptions="chartOptions"/>
            </div>
        </div> 
        
    </div>
</template>

<style lang="scss">
@import "@/assets/scss/index.scss"
</style>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import MetricsCard from "@/components/MetricsCard.vue";
import LineChart from "@/components/LineChart.vue";
import BarChart from "@/components/BarChart.vue";

//data
const metrics = {
    productionProgress: 75,
    machineUtilization: 85,
    defectRate: 2.5,
};

const records = ref<Record<string, any> | null>(null);

const alerts = [
    { type: "Warning", message: "Machine 1 (Line 1) requires maintenance", timestamp: "2025-01-08 10:30" },
    { type: "Error", message: "Batch B004 delayed due to raw material shortage", timestamp: "2025-01-08 09:15" },
];

const machineUtilizationData = {
    labels: ['Machine 1 (Line 1)', 'Machine 2 (Line 2)'],
    datasets: [
    {
        label: 'Machine Utilization (%)',
        data: [85, 90],
        backgroundColor: '#1be21b',
    },
    ],
};

const defectRatesData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
    {
        label: 'Defect Rate (%)',
        data: [5, 3, 2, 4],
        borderColor: '#ff0000',
        fill: false,
        
    },
    ],
};

const productionData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [
    {
        label: 'Production Progress (%)',
        data: [85,80,90,65],
        borderColor: '#4552e3',
        fill: false,
        
    },
    ],
}

const chartOptions = {
    responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
        },
        scales: {
            y: {
                beginAtZero: true,
            },
    },
}

const productionLine = [
    {
        production: 'Production Line 1',
        status: 'Online'
    },
    {
        production: 'Production Line 2',
        status: 'Online'
    },
];


const fetchRecords = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/get_record`, {
            method: 'GET',  
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
        // If response is OK, parse JSON
        const data = await response.json();
        records.value = data; 

        const formatDate = (dateObj) => {
            if (dateObj) {
                const date = new Date(dateObj);
                return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
            }
            return null; // Return null if date is invalid
        };

        // Map over the records to format dates
        const formattedRecords = records.value.map((record) => {
                return {
                    ...record,
                    inspectionDate: formatDate(record.inspectionDate),
                    productionStart: formatDate(record.productionStart),
                    productionEnd: formatDate(record.productionEnd),
                    productEntry: formatDate(record.productEntry),
                    productExit: formatDate(record.productExit),
                    deliveryDate: formatDate(record.deliveryDate),
                    rawMaterials: record.rawMaterials.map((material) => ({
                        ...material,
                        warehouseEntry: formatDate(material.warehouseEntry),
                        warehouseExit: formatDate(material.warehouseExit),
                    })),
                };
            });

            // Update the records with formatted data
            records.value = formattedRecords;
        }
    } catch (error) {
        console.error('Error fetching user:', error);
        alert(`Something went wrong while fetching data: ${error.message}`);
    }
};

onMounted(async() =>{
    await fetchRecords();
})



</script>