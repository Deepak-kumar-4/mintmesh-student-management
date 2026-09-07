<script setup>
import { ref, computed, watch } from 'vue';
import { getStudents } from '../services/api.js';
import StatusFilter from './StatusFilter.vue';
import Pagination from './Pagination.vue';

defineEmits(['edit', 'delete']);

const PAGE_SIZE = 10;

const students = ref([]);
const total = ref(0);
const page = ref(1);
const status = ref(null);
const loading = ref(false);
const error = ref(false);

const totalPages = computed(() => Math.ceil(total.value / PAGE_SIZE));

const STATUS_STYLES = {
  active: { text: 'text-status-active', border: 'border-l-status-active' },
  graduated: { text: 'text-status-graduated', border: 'border-l-status-graduated' },
  dropped: { text: 'text-status-dropped', border: 'border-l-status-dropped' },
};

function statusTextClass(value) {
  return STATUS_STYLES[value]?.text ?? '';
}

function statusBorderClass(value) {
  return STATUS_STYLES[value]?.border ?? '';
}

function capitalize(value) {
  return value ? value.charAt(0).toUpperCase() + value.slice(1) : '';
}

async function fetchStudents() {
  loading.value = true;
  error.value = false;
  try {
    const response = await getStudents({
      page: page.value,
      pageSize: PAGE_SIZE,
      enrollmentStatus: status.value,
    });
    students.value = response.data.items;
    total.value = response.data.total;
  } catch (err) {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

function handleFilterChange(value) {
  status.value = value;
  page.value = 1;
}

function handlePageChange(newPage) {
  page.value = newPage;
}

function clearFilter() {
  status.value = null;
  page.value = 1;
}

watch([page, status], fetchStudents, { immediate: true });
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="font-display text-3xl font-semibold text-ink">Student Records</h1>
      <StatusFilter :model-value="status" @change="handleFilterChange" />
    </div>

    <div v-if="error" class="flex flex-col items-center gap-3 rounded-md border border-ink-soft/20 bg-white py-16 font-sans">
      <p class="text-ink-soft">Couldn't load student records.</p>
      <button
        type="button"
        class="rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:opacity-90"
        @click="fetchStudents"
      >
        Retry
      </button>
    </div>

    <div
      v-else-if="!loading && students.length === 0"
      class="flex flex-col items-center gap-3 rounded-md border border-ink-soft/20 bg-white py-16 font-sans"
    >
      <p class="text-ink-soft">No students match this filter.</p>
      <button
        type="button"
        class="rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:opacity-90"
        @click="clearFilter"
      >
        Clear filter
      </button>
    </div>

    <template v-else>
      <div class="overflow-x-auto rounded-md border border-ink-soft/20 bg-white">
        <table class="w-full text-left font-sans text-sm">
          <thead>
            <tr class="border-b border-ink-soft/20 text-ink-soft">
              <th class="px-4 py-3 font-medium">Name</th>
              <th class="px-4 py-3 font-medium">Email</th>
              <th class="px-4 py-3 font-medium">Status</th>
              <th class="px-4 py-3 font-medium">Date of Birth</th>
              <th class="px-4 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody v-if="loading">
            <tr v-for="n in 5" :key="`skeleton-${n}`" class="border-b border-b-ink-soft/10">
              <td class="px-4 py-3"><div class="h-4 w-32 animate-pulse rounded bg-ink-soft/15"></div></td>
              <td class="px-4 py-3"><div class="h-4 w-40 animate-pulse rounded bg-ink-soft/15"></div></td>
              <td class="px-4 py-3"><div class="h-4 w-20 animate-pulse rounded bg-ink-soft/15"></div></td>
              <td class="px-4 py-3"><div class="h-4 w-24 animate-pulse rounded bg-ink-soft/15"></div></td>
              <td class="px-4 py-3"><div class="h-4 w-16 animate-pulse rounded bg-ink-soft/15"></div></td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr
              v-for="student in students"
              :key="student.id"
              class="border-b border-b-ink-soft/10 border-l-4"
              :class="statusBorderClass(student.enrollment_status)"
            >
              <td class="px-4 py-3 text-ink">{{ student.first_name }} {{ student.last_name }}</td>
              <td class="px-4 py-3 text-ink">{{ student.email }}</td>
              <td class="px-4 py-3 font-medium" :class="statusTextClass(student.enrollment_status)">
                {{ capitalize(student.enrollment_status) }}
              </td>
              <td class="px-4 py-3 text-ink">{{ student.date_of_birth }}</td>
              <td class="px-4 py-3">
                <button
                  type="button"
                  class="mr-3 text-accent hover:underline"
                  @click="$emit('edit', student)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  class="text-ink-soft hover:text-accent hover:underline"
                  @click="$emit('delete', student)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <Pagination
        v-if="!loading"
        class="mt-4"
        :current-page="page"
        :total-pages="totalPages"
        @change="handlePageChange"
      />
    </template>
  </div>
</template>
