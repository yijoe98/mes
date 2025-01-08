<template>
    <div class="production-tracking flex w-5/6 max-h-max flex-col text-left mx-6 mt-3 gap-3">
        <h1 class="text-blue-950 font-extrabold">Production Tracking</h1>
        <div class="production-record">
            <div class="header flex flex-row h-min justify-between items-center">
                <h2 class="text-xl font-semibold mt-3 mb-4 flex">Production Records</h2>
                <div class="flex flex-row gap-3 justify-between items-center">
                    <form class="search-container flex flex-row h-1/2">
                        <div class="input-wrapper">
                        <input
                            v-model="recordSearch"
                            placeholder="Search Batch ID"
                            class="search-input"
                        />
                            <img src="../assets/icon/icon-search.svg" class="search-icon" />
                        </div>
                    </form>
                    <div @click="openAddProductionModal()" class="cursor-pointer bg-blue-500 px-4 py-2 text-white rounded hover:bg-blue-600">Add Records</div>
                </div>
                
            </div>
            
            <table class="table-auto w-full border-collapse border border-gray-300">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Batch ID</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Qty</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Production Line No.</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" colspan="2">Raw Material Required</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" colspan="2">Raw Material Warehouse</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" colspan="2">Production Line</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" colspan="2">Product Warehouse</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Delivery Date</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Action</th>
                    </tr>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-4 py-2 text-center">Raw Material</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Qty</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Entry</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Exit</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Entry</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Exit</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Entry</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Exit</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="record in filteredRecords" :key="record.batchId">
                        <!-- First row with batch-level details -->
                        <tr class="hover:bg-gray-100">
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.batchId }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.qty }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.productionLine }}
                            </td>

                            <!-- First raw material -->
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ record.rawMaterials[0].rawMaterial }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ record.rawMaterials[0].qtyRequired }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ record.rawMaterials[0].warehouseEntry }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ record.rawMaterials[0].warehouseExit }}
                            </td>

                            <!-- Batch-specific columns -->
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.productionStart }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.productionEnd }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.productEntry }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.productExit }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center" :rowspan="record.rawMaterials.length">
                                {{ record.deliveryDate }}
                            </td>
                            <td class="border border-gray-300 px-2 py-2 text-center" :rowspan="record.rawMaterials.length">
                                <button class="px-2 py-2 bg-green-500 text-white rounded hover:bg-green-600 mr-2" @click="openRecordModal(record)">Update</button>
                                <button class="px-2 py-2 bg-red-500 text-white rounded hover:bg-red-600" @click="deleteRecord(record.batchId)">Delete</button>
                            </td>
                        </tr>

                        <!-- Additional rows for remaining raw materials -->
                        <tr v-for="(rawMaterial, index) in record.rawMaterials.slice(1)" :key="index" class="hover:bg-gray-100">
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ rawMaterial.rawMaterial }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ rawMaterial.qtyRequired }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ rawMaterial.warehouseEntry }}
                            </td>
                            <td class="border border-gray-300 px-4 py-2 text-center">
                                {{ rawMaterial.warehouseExit }}
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
        <div class="production-schedule">
            <div class="header flex flex-row h-min justify-between items-center">
                <h2 class="text-xl font-semibold mt-3 mb-4 flex">Production Schedule</h2>
                <form class="search-container flex flex-row h-1/2">
                    <div class="input-wrapper">
                    <input
                        v-model="scheduleSearch"
                        placeholder="Search Batch ID"
                        class="search-input"
                    />
                        <img src="../assets/icon/icon-search.svg" class="search-icon" />
                    </div>
                </form>
            </div>
            <table class="table-auto w-full border-collapse border border-gray-300 mb-3">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Batch ID</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Qty</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Production Line</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Machine</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" colspan="2">Schedule</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Status</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Remarks</th>
                        <th class="border border-gray-300 px-4 py-2 text-center" rowspan="2">Action</th>
                    </tr>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-4 py-2 text-center">Start Time</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">End Time</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in filteredScheduleRecords" :key="record.batchId" class="hover:bg-gray-100">
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.batchId }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.qty }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.productionLine }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.machine }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.productionStart }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.productionEnd }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.status }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.remarks }}</td>
                        <td class="border border-gray-300 px-2 py-2 text-center">
                            <button class="px-2 py-2 bg-green-500 text-white rounded hover:bg-green-600 mr-2" @click="openProductionLineModal(record)">Update</button>
                            <button class="px-2 py-2 bg-red-500 text-white rounded hover:bg-red-600">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!--Production Record Modal-->
        <div
            v-if="isRecordModalOpen"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
        >
            <div class="bg-white rounded-lg shadow p-6 w-2/3">
                <h2 class="text-xl font-semibold mb-4">Update Record</h2>
                <form @submit.prevent="saveRecord">
                    <!-- Batch ID, Quantity, Production Line, and Status -->
                    <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block font-semibold">Batch ID</label>
                        <input
                        type="text"
                        v-model="currentRecord.batchId"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Quantity</label>
                        <input
                        type="number"
                        v-model="currentRecord.qty"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production Line</label>
                        <input
                        type="text"
                        v-model="currentRecord.productionLine"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Status</label>
                        <input
                        type="text"
                        v-model="currentRecord.status"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Raw Materials Table -->
                    <div class="mt-4">
                    <h3 class="text-lg font-semibold mb-2">Raw Materials</h3>
                    <table class="w-full table-auto">
                        <thead>
                        <tr>
                            <th class="border px-4 py-2">Raw Material</th>
                            <th class="border px-4 py-2">Qty Required</th>
                            <th class="border px-4 py-2">Warehouse Entry</th>
                            <th class="border px-4 py-2">Warehouse Exit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(rawMaterial, index) in currentRecord.rawMaterials" :key="index">
                            <td>
                            <input
                                type="text"
                                v-model="rawMaterial.rawMaterial"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="number"
                                v-model="rawMaterial.qtyRequired"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="date"
                                v-model="rawMaterial.warehouseEntry"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="date"
                                v-model="rawMaterial.warehouseExit"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                                <button type="button" @click="removeRawMaterial(index)" class="px-2 py-1 text-red-500">Remove</button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    <button type="button" @click="addRawMaterial" class="mt-2 px-2 py-1 bg-green-500 text-white rounded">Add Raw Material</button>
                    </div>

                    <!-- Production and Product Dates -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Production Entry</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionStart"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production Exit</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionEnd"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Product Entry</label>
                        <input
                        type="date"
                        v-model="currentRecord.productEntry"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Product Exit</label>
                        <input
                        type="date"
                        v-model="currentRecord.productExit"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Delivery Date, Machine, and Remarks -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Delivery Date</label>
                        <input
                        type="date"
                        v-model="currentRecord.deliveryDate"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Machine</label>
                        <input
                        type="text"
                        v-model="currentRecord.machine"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Save and Cancel Buttons -->
                    <div class="mt-4 text-right">
                    <button
                        type="button"
                        class="px-4 py-2 bg-gray-500 text-white rounded mr-2"
                        @click="closeRecordModal"
                    >
                        Cancel
                    </button>
                    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
                        Save
                    </button>
                    </div>
                </form>
            </div>
        </div>

        <!--Production Schedule Modal-->
        <div
            v-if="isProductionLineModalOpen"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
        >
            <div class="bg-white rounded-lg shadow p-6 w-2/3">
                <h2 class="text-xl font-semibold mb-4">Update Production Line</h2>
                <form @submit.prevent="saveRecord">
                    <!-- Batch ID, Quantity, Production Line, and Status -->
                    <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block font-semibold">Batch ID</label>
                        <input
                        type="text"
                        v-model="currentRecord.batchId"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Quantity</label>
                        <input
                        type="number"
                        v-model="currentRecord.qty"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production Line</label>
                        <input
                        type="text"
                        v-model="currentRecord.productionLine"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Machine</label>
                        <input
                        type="text"
                        v-model="currentRecord.machine"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    </div>

                    <!-- Production Start and End Dates -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Production Start</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionStart"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production End</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionEnd"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    </div>

                    <!-- Status and Remarks -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Status</label>
                        <input
                        type="text"
                        v-model="currentRecord.status"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Remarks</label>
                        <input
                        type="text"
                        v-model="currentRecord.remarks"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Save and Cancel Buttons -->
                    <div class="mt-4 text-right">
                    <button
                        type="button"
                        class="px-4 py-2 bg-gray-500 text-white rounded mr-2"
                        @click="closeProductionLineModal"
                    >
                        Cancel
                    </button>
                    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded" @click="saveProductionLine">
                        Save
                    </button>
                    </div>
                </form>
            </div>
        </div>


        <!--Add production record modal-->
        <div
            v-if="isAddRecordModalOpen"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
        >
            <div class="bg-white rounded-lg shadow p-6 w-2/3">
                <h2 class="text-xl font-semibold mb-4">Update Record</h2>
                <form @submit.prevent="saveRecord">
                    <!-- Batch ID, Quantity, Production Line, and Status -->
                    <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block font-semibold">Batch ID</label>
                        <input
                        type="text"
                        v-model="currentRecord.batchId"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Quantity</label>
                        <input
                        type="number"
                        v-model="currentRecord.qty"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production Line</label>
                        <input
                        type="text"
                        v-model="currentRecord.productionLine"
                        class="w-full border rounded p-2"
                        required
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Status</label>
                        <input
                        type="text"
                        v-model="currentRecord.status"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Raw Materials Table -->
                    <div class="mt-4">
                    <h3 class="text-lg font-semibold mb-2">Raw Materials</h3>
                    <table class="w-full table-auto">
                        <thead>
                        <tr>
                            <th class="border px-4 py-2">Raw Material</th>
                            <th class="border px-4 py-2">Qty Required</th>
                            <th class="border px-4 py-2">Warehouse Entry</th>
                            <th class="border px-4 py-2">Warehouse Exit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(rawMaterial, index) in currentRecord.rawMaterials" :key="index">
                            <td>
                            <input
                                type="text"
                                v-model="rawMaterial.rawMaterial"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="number"
                                v-model="rawMaterial.qtyRequired"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="date"
                                v-model="rawMaterial.warehouseEntry"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                            <input
                                type="date"
                                v-model="rawMaterial.warehouseExit"
                                class="w-full border rounded p-2"
                                required
                            />
                            </td>
                            <td>
                                <button type="button" @click="removeRawMaterial(index)" class="px-2 py-1 text-red-500">Remove</button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    <button type="button" @click="addRawMaterial" class="mt-2 px-4 py-2 bg-green-500 text-white rounded">Add Raw Material</button>
                    </div>

                    <!-- Production and Product Dates -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Production Entry</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionStart"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Production Exit</label>
                        <input
                        type="date"
                        v-model="currentRecord.productionEnd"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Product Entry</label>
                        <input
                        type="date"
                        v-model="currentRecord.productEntry"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Product Exit</label>
                        <input
                        type="date"
                        v-model="currentRecord.productExit"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Delivery Date, Machine, and Remarks -->
                    <div class="grid grid-cols-2 gap-4 mt-4">
                    <div>
                        <label class="block font-semibold">Delivery Date</label>
                        <input
                        type="date"
                        v-model="currentRecord.deliveryDate"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    <div>
                        <label class="block font-semibold">Machine</label>
                        <input
                        type="text"
                        v-model="currentRecord.machine"
                        class="w-full border rounded p-2"
                        />
                    </div>
                    </div>

                    <!-- Save and Cancel Buttons -->
                    <div class="mt-4 text-right">
                    <button
                        type="button"
                        class="px-4 py-2 bg-gray-500 text-white rounded mr-2"
                        @click="closeRecordModal"
                    >
                        Cancel
                    </button>
                    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
                        Save
                    </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
@import "@/assets/scss/index.scss"
</style>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';

//data
const recordSearch = ref('');
const scheduleSearch = ref('');
const isRecordModalOpen = ref(false);
const isProductionLineModalOpen = ref(false);
const currentRecord = ref<Record<string, any> | null>(null);
const records = ref<Record<string, any> | null>(null);
const isAddRecordModalOpen = ref(false);

const filteredRecords = computed(() =>
    records.value?.filter((record) =>
        record.batchId.toLowerCase().includes(recordSearch.value.toLowerCase())
    )
);

const filteredScheduleRecords = computed(() =>
    records.value?.filter((record) =>
        record.batchId.toLowerCase().includes(scheduleSearch.value.toLowerCase())
    )
);

const openRecordModal = (record: Record<string, any> | null) => {
      currentRecord.value = record || { batchId: "", qty: 0, productionLine: "", status: "" };
      isRecordModalOpen.value = true;
    };

const closeRecordModal = () => {
    isRecordModalOpen.value = false;
    isAddRecordModalOpen.value=false;
    currentRecord.value = null;
};

const addRawMaterial = () => {
    if (!currentRecord.value?.rawMaterials) {
        currentRecord.value.rawMaterials = [];
    }
        currentRecord.value?.rawMaterials.push({
        rawMaterial: "",
        qtyRequired: 0,
        warehouseEntry: "",
        warehouseExit: "",
    });
};

const removeRawMaterial = (index: number) => {
    currentRecord.value?.rawMaterials.splice(index, 1);
};

const serializeRecord = (record: any) => {
  const serializeDate = (date: Date | string | null) =>
    date ? new Date(date).toISOString() : null;

  const serializeInspectionDetails = (details: any[]) =>
    details.map((detail) => ({
      ...detail,
    }));

  const serializeRawMaterials = (materials: any[]) =>
    materials.map((material) => ({
      ...material,
      warehouseEntry: serializeDate(material.warehouseEntry),
      warehouseExit: serializeDate(material.warehouseExit),
    }));

  return {
    ...record,
    inspectionDate: serializeDate(record.inspectionDate),
    productionStart: serializeDate(record.productionStart),
    productionEnd: serializeDate(record.productionEnd),
    productEntry: serializeDate(record.productEntry),
    productExit: serializeDate(record.productExit),
    deliveryDate: serializeDate(record.deliveryDate),
    rawMaterials: serializeRawMaterials(record.rawMaterials),
    inspectionDetails: serializeInspectionDetails(record.inspectionDetails),
  };
};

const saveRecord = async () => {
  if (currentRecord.value) {
    try {
      const serializedRecord = serializeRecord(currentRecord.value);

      const response = await fetch(
        `http://127.0.0.1:8000/update_record/${currentRecord.value.batchId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(serializedRecord),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update the record');
      }

      alert('Record updated successfully!');
      closeRecordModal();
    } catch (error) {
      console.error('Error updating record:', error);
      alert(`Failed to update record: ${error.message}`);
    }
  }
};

const openAddProductionModal = () => {
    isAddRecordModalOpen.value = true;
    currentRecord.value = {};  // Initialize currentRecord if it's null
    currentRecord.value.batchId = `B${String(records.value?.length +1).padStart(3, '0')}`;
};

const openProductionLineModal = (record: Record<string, any> | null) => {
    currentRecord.value = record || { batchId: "", qty: 0, productionLine: "", status: "" };
    isProductionLineModalOpen.value = true;
};

const closeProductionLineModal = () => {
    isProductionLineModalOpen.value = false;
    currentRecord.value = null;
};

const saveProductionLine = async() => {
    if (currentRecord.value) {
    try {
      const serializedRecord = serializeRecord(currentRecord.value);

      const response = await fetch(
        `http://127.0.0.1:8000/update_record/${currentRecord.value.batchId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(serializedRecord),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update the record');
      }

      alert('Record updated successfully!');
      closeProductionLineModal();
    } catch (error) {
      console.error('Error updating record:', error);
      alert(`Failed to update record: ${error.message}`);
    }
  }
};

const deleteRecord = async (batchId) => {
    try {
        // Send a DELETE request to the API with the batchId
        const response = await fetch(`http://127.0.0.1:8000/delete_record/${batchId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Check if the response is OK (status 200)
        if (response.ok) {
            const data = await response.json();
            alert(data.message);  // Show success message
           
            records.value = records.value.filter(record => record.batchId !== batchId);
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to delete the record');
        }
    } catch (error) {
        console.error('Error deleting record:', error);
        alert(`Failed to delete record: ${error.message}`);
    }
};


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