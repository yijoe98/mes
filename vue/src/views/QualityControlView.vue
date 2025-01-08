<template>
    <div class="quality-control flex w-5/6 max-h-max flex-col text-left mx-6 mt-3 gap-3">
        <h1 class="text-blue-950 font-extrabold">Quality Control</h1>
        <div>
            <div class="header flex flex-row h-min justify-between items-center">
                <h2 class="text-xl font-semibold mt-3 mb-4 flex">Quality Control Tracker</h2>
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
            </div>
            <table class="table-auto w-full border-collapse border border-gray-300">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-4 py-2 text-center">Batch ID</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Inspection Date</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Inspector Name</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Status</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Remarks</th>
                        <th class="border border-gray-300 px-4 py-2 text-center">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in filteredRecords" :key="record.batchId" class="hover:bg-gray-100">
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.batchId }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.inspectionDate }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.inspectorName }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.inspectionStatus }}</td>
                        <td class="border border-gray-300 px-4 py-2 text-center">{{ record.inspectionRemarks }}</td>
                        <td class="border border-gray-300 px-2 py-2 text-center flex flex-row gap-2 justify-center items-center">
                            <button
                            class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                            @click="openBatchModal(record)"
                            >
                            View
                            </button>
                            <button
                            class="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
                            @click="openBatchEditModal(record)"
                            >
                            Update
                            </button>
                            <button
                            class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                            @click="deleteBatch(record.batchId)"
                            >
                            Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
    
            <!-- View Batch Modal -->
            <div v-if="isViewModalOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
                <div class="bg-white rounded-lg p-6 w-fit">
                    <h2 class="text-2xl font-bold mb-4">Batch {{ selectedRecord.batchId }} Quality Control</h2>
                    <table class="table-auto w-full border-collapse border border-gray-300">
                        <thead>
                            <tr class="bg-gray-100">
                                <th class="border border-gray-300 px-4 py-2 text-center">Inspection ID</th>
                                <th class="border border-gray-300 px-4 py-2 text-center">Status</th>
                                <th class="border border-gray-300 px-4 py-2 text-center">Remarks</th>
                                <th class="border border-gray-300 px-4 py-2 text-center">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                            v-for="inspection in selectedRecord.inspectionDetails"
                            :key="inspection.inspectionID"
                            class="hover:bg-gray-100"
                            >
                                <td class="border border-gray-300 px-4 py-2 text-center">{{ inspection.inspectionID }}</td>
                                <td class="border border-gray-300 px-4 py-2 text-center">{{ inspection.status }}</td>
                                <td class="border border-gray-300 px-4 py-2 text-center">{{ inspection.remarks }}</td>
                                <td class="border border-gray-300 px-4 py-2 text-center">
                                    <button
                                    class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 mr-2"
                                    @click="openInspectionEditModal(selectedRecord, inspection)"
                                    >
                                    Edit
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="flex justify-end mt-4">
                        <button class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 mr-2" @click="closeBatchModal">
                            Close
                        </button>
                        <button class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600" @click="generateReport(selectedRecord)">
                            Generate Report
                        </button>
                    </div>
                </div>
            </div>
    
            <!-- Edit Batch Modal -->
            <div v-if="isBatchEditModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div class="bg-white rounded-lg shadow p-6 w-1/3">
                    <h2 class="text-xl font-bold mb-4">Edit Batch Details</h2>
                    <form @submit.prevent="updateBatch">
                        <div class="grid grid-cols-2 gap-4">
                            <label class="block mb-2 font-semibold">Batch ID:</label>
                            <input v-model="selectedRecord.batchId" class="w-full border rounded p-2" disabled />

                            <label class="block mb-2 font-semibold">Inspector Name:</label>
                            <input v-model="selectedRecord.inspectorName" class="w-full border rounded p-2" />

                            <label class="block mb-2 font-semibold">Inspection Date:</label>
                            <input type="date" v-model="selectedRecord.inspectionDate" class="w-full border rounded p-2" />

                            <label class="block mb-2 font-semibold">Status:</label>
                            <input v-model="selectedRecord.inspectionStatus" class="w-full border rounded p-2" />

                            <label class="block mb-2 font-semibold">Remarks:</label>
                            <textarea v-model="selectedRecord.inspectionRemarks" class="w-full border rounded p-2"></textarea>
                        </div>
                        <div class="mt-4 text-right">
                            <button class="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 mr-2" @click="closeBatchEditModal">
                                Cancel
                            </button>
                            <button class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600" type="submit" @click="updateBatchDetails">
                                Save
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Edit Inspection Modal -->
            <div v-if="isInspectionEditModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white rounded-lg shadow p-6 w-1/3">
                    <h2 class="text-xl font-bold mb-4">Edit Inspection Details</h2>
                    <form @submit.prevent="updateBatch">
                        <div class="grid grid-cols-2 gap-4">
                            <label class="block mb-2 font-semibold">Inspection ID:</label>
                            <input v-model="selectedInspection.inspectionID" class="w-full border rounded p-2"  disabled />
                            <label class="block mb-2 font-semibold">Status:</label>
                            <input v-model="selectedInspection.status" class="w-full border rounded p-2"  />
                            <label class="block mb-2 font-semibold">Remarks:</label>
                            <textarea v-model="selectedInspection.remarks" class="w-full border rounded p-2" ></textarea>
                        </div>
                        
                        <div class="mt-4 text-right">
                            <button class="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 mr-2" @click="closeInspectionEditModal">
                            Cancel
                            </button>
                            <button class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600" type="submit" @click="updateInspectionDetails">
                            Save
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Report Modal -->
            <div v-if="isReportModalOpen" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
                <div class="bg-white rounded-lg p-6 w-fit">
                    <h2 class="text-2xl font-bold mb-4">Batch {{ reportData.batchId }} Quality Control Report</h2>
                    <table class="table-auto w-full border-collapse border border-gray-300">
                        <tbody>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Batch ID</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.batchId }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Inspection Date</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.inspectionDate }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Inspector Name</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.inspectorName }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Total Quantity</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.totalQty }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Defective Quantity</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.defectQty }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Defect Rate</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.defectRate }}</td>
                            </tr>
                            <tr>
                                <th class="border border-gray-300 px-4 py-2 text-left">Status</th>
                                <td class="border border-gray-300 px-4 py-2">{{ reportData.status }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="flex justify-end mt-4">
                        <button class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600" @click="closeReportModal">
                            Close
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>
  

<style lang="scss">
@import "@/assets/scss/index.scss"
</style>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Data
const recordSearch = ref('');

// State
const isViewModalOpen = ref(false);
const isInspectionEditModalOpen = ref(false);
const isBatchEditModalOpen = ref(false);
const selectedRecord = ref<Record<string, any> | null>(null);
const selectedInspection = ref<Record<string, any> | null>(null);
const isReportModalOpen = ref(false);
const reportData = ref<Record<string, any> | null>(null);
const records = ref<Record<string, any> | null>(null);

// Computed
const filteredRecords = computed(() =>
    records.value?.filter((record) =>
        record.batchId.toLowerCase().includes(recordSearch.value.toLowerCase())
    )
);

// Methods
const openBatchModal = (record: Record<string, any>) => {
    selectedRecord.value = { ...record };
    isViewModalOpen.value = true;
};

const closeBatchModal = () => {
    selectedRecord.value = null;
    isViewModalOpen.value = false;
};

const openBatchEditModal = (record: Record<string, any>) => {
    selectedRecord.value = { ...record };
    isBatchEditModalOpen.value = true;
};

const closeBatchEditModal = () => {
    selectedRecord.value = null;
    isBatchEditModalOpen.value = false;
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

const updateBatchDetails = async() => {
    if (selectedRecord.value) {
        try {
            const serializedRecord = serializeRecord(selectedRecord.value);

            const response = await fetch(
                `http://127.0.0.1:8000/update_record/${selectedRecord.value.batchId}`,
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
            closeBatchEditModal();
            } catch (error) {
            console.error('Error updating record:', error);
            alert(`Failed to update record: ${error.message}`);
        }
    }
    
};

const openInspectionEditModal = (record: Record<string, any>, inspection: Record<string, any>) => {
    selectedRecord.value = { ...record };
    selectedInspection.value = { ...inspection };
    isInspectionEditModalOpen.value = true;
};

const closeInspectionEditModal = () => {
    selectedInspection.value = null;
    isInspectionEditModalOpen.value = false;
    isViewModalOpen.value = false;
};

const updateInspectionDetails = async () => {
    const inspectionIndex = selectedRecord.value?.inspectionDetails.findIndex(
        (inspection) => inspection.inspectionID === selectedInspection.value?.inspectionID
    );

    if (inspectionIndex !== -1) {
        // Update the status and remarks in the selectedRecord
        selectedRecord.value.inspectionDetails[inspectionIndex].status = selectedInspection.value?.status;
        selectedRecord.value.inspectionDetails[inspectionIndex].remarks = selectedInspection.value?.remarks;
    } else {
        alert('Inspection not found!');
        return;
    }

    try {
        const serializedRecord = serializeRecord(selectedRecord.value);

        // Step 3: Send the updated record to the API
        const response = await fetch(
            `http://127.0.0.1:8000/update_record/${selectedRecord.value.batchId}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(serializedRecord),
            }
        );

        // Step 4: Handle the response from the API
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to update the record');
        }

        // Success: Notify the user and close the modal
        alert('Record updated successfully!');
        closeInspectionEditModal();
    } catch (error) {
        console.error('Error updating record:', error);
        alert(`Failed to update record: ${error.message}`);
    }
};

const deleteBatch = async (batchId) => {
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

const generateReport = (record: Record<string, any>) => {
    reportData.value = {
        batchId: record.batchId,
        inspectionDate: record.inspectionDate,
        inspectorName: record.inspectorName,
        totalQty: record.qty,
        defectQty: record.defectQty,
        defectRate: ((record.defectQty / record.qty) * 100).toFixed(2) + '%',
        status: record.status,
    };
    isReportModalOpen.value = true;
};

const closeReportModal = () => {
    isReportModalOpen.value = false;
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