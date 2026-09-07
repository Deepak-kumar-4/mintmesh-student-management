<script setup>
import { reactive, ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { createStudent, updateStudent } from '../services/api.js';

const props = defineProps({
  student: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['saved', 'cancel']);

const isEditMode = computed(() => props.student !== null);

const form = reactive({
  first_name: props.student?.first_name ?? '',
  last_name: props.student?.last_name ?? '',
  email: props.student?.email ?? '',
  date_of_birth: props.student?.date_of_birth ?? '',
  enrollment_status: props.student?.enrollment_status ?? 'active',
});

const errors = reactive({
  first_name: '',
  last_name: '',
  email: '',
  date_of_birth: '',
  enrollment_status: '',
});

const saving = ref(false);
const bannerError = ref('');
const visible = ref(false);
let pendingSavedData = null;

onMounted(() => {
  visible.value = true;
  window.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
});

function handleKeydown(event) {
  if (event.key === 'Escape') {
    requestClose();
  }
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function todayISO() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function validate() {
  errors.first_name = form.first_name.trim() ? '' : 'First name is required';
  errors.last_name = form.last_name.trim() ? '' : 'Last name is required';
  errors.email = EMAIL_PATTERN.test(form.email) ? '' : 'Enter a valid email address';

  if (!form.date_of_birth) {
    errors.date_of_birth = 'Date of birth is required';
  } else if (form.date_of_birth >= todayISO()) {
    errors.date_of_birth = "Date of birth can't be in the future";
  } else {
    errors.date_of_birth = '';
  }

  errors.enrollment_status = form.enrollment_status ? '' : 'Enrollment status is required';

  return (
    !errors.first_name &&
    !errors.last_name &&
    !errors.email &&
    !errors.date_of_birth &&
    !errors.enrollment_status
  );
}

async function handleSubmit() {
  bannerError.value = '';
  if (!validate()) return;

  saving.value = true;
  try {
    const payload = {
      first_name: form.first_name.trim(),
      last_name: form.last_name.trim(),
      email: form.email.trim(),
      date_of_birth: form.date_of_birth,
      enrollment_status: form.enrollment_status,
    };
    const response = isEditMode.value
      ? await updateStudent(props.student.id, payload)
      : await createStudent(payload);
    pendingSavedData = response.data;
    requestClose();
  } catch (err) {
    if (err.response?.status === 409) {
      errors.email = 'This email is already registered to another student';
    } else {
      bannerError.value = "Couldn't save this student record. Please try again.";
    }
  } finally {
    saving.value = false;
  }
}

function requestClose() {
  visible.value = false;
}

function handleAfterLeave() {
  if (pendingSavedData) {
    emit('saved', pendingSavedData);
    pendingSavedData = null;
  } else {
    emit('cancel');
  }
}
</script>

<template>
  <Transition
    enter-active-class="transition-opacity duration-300 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-200 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="visible" class="fixed inset-0 z-40 bg-ink/50" @click="requestClose"></div>
  </Transition>

  <Transition
    enter-active-class="transition-transform duration-300 ease-out"
    enter-from-class="translate-x-full"
    enter-to-class="translate-x-0"
    leave-active-class="transition-transform duration-200 ease-in"
    leave-from-class="translate-x-0"
    leave-to-class="translate-x-full"
    @after-leave="handleAfterLeave"
  >
    <aside
      v-if="visible"
      class="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col bg-white shadow-xl"
    >
      <div class="flex items-center justify-between border-b border-ink-soft/20 px-6 py-4">
        <h2 class="font-display text-xl font-semibold text-ink">
          {{ isEditMode ? 'Edit Student Record' : 'New Student Record' }}
        </h2>
        <button
          type="button"
          class="font-sans text-ink-soft hover:text-ink"
          aria-label="Close"
          @click="requestClose"
        >
          &times;
        </button>
      </div>

      <div
        v-if="bannerError"
        class="mx-6 mt-4 flex items-start justify-between gap-3 rounded border border-accent/30 bg-accent/10 px-4 py-3 font-sans text-sm text-accent"
      >
        <span>{{ bannerError }}</span>
        <button type="button" class="font-medium" @click="bannerError = ''">&times;</button>
      </div>

      <form class="flex flex-1 flex-col overflow-hidden font-sans" @submit.prevent="handleSubmit">
        <div class="flex-1 space-y-4 overflow-y-auto px-6 py-4 text-sm">
          <div>
            <label class="mb-1 block font-medium text-ink" for="first_name">First name</label>
            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              class="w-full rounded border px-3 py-2 text-ink"
              :class="errors.first_name ? 'border-accent' : 'border-ink-soft/30'"
            />
            <p v-if="errors.first_name" class="mt-1 text-xs text-accent">{{ errors.first_name }}</p>
          </div>

          <div>
            <label class="mb-1 block font-medium text-ink" for="last_name">Last name</label>
            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              class="w-full rounded border px-3 py-2 text-ink"
              :class="errors.last_name ? 'border-accent' : 'border-ink-soft/30'"
            />
            <p v-if="errors.last_name" class="mt-1 text-xs text-accent">{{ errors.last_name }}</p>
          </div>

          <div>
            <label class="mb-1 block font-medium text-ink" for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="w-full rounded border px-3 py-2 text-ink"
              :class="errors.email ? 'border-accent' : 'border-ink-soft/30'"
            />
            <p v-if="errors.email" class="mt-1 text-xs text-accent">{{ errors.email }}</p>
          </div>

          <div>
            <label class="mb-1 block font-medium text-ink" for="date_of_birth">Date of birth</label>
            <input
              id="date_of_birth"
              v-model="form.date_of_birth"
              type="date"
              class="w-full rounded border px-3 py-2 text-ink"
              :class="errors.date_of_birth ? 'border-accent' : 'border-ink-soft/30'"
            />
            <p v-if="errors.date_of_birth" class="mt-1 text-xs text-accent">{{ errors.date_of_birth }}</p>
          </div>

          <div>
            <label class="mb-1 block font-medium text-ink" for="enrollment_status">Enrollment status</label>
            <select
              id="enrollment_status"
              v-model="form.enrollment_status"
              class="w-full rounded border bg-white px-3 py-2 text-ink"
              :class="errors.enrollment_status ? 'border-accent' : 'border-ink-soft/30'"
            >
              <option value="active">Active</option>
              <option value="graduated">Graduated</option>
              <option value="dropped">Dropped</option>
            </select>
            <p v-if="errors.enrollment_status" class="mt-1 text-xs text-accent">
              {{ errors.enrollment_status }}
            </p>
          </div>
        </div>

        <div class="flex justify-end gap-3 border-t border-ink-soft/20 px-6 py-4">
          <button
            type="button"
            class="rounded border border-ink-soft/30 px-4 py-2 text-sm text-ink hover:bg-paper"
            @click="requestClose"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ saving ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </form>
    </aside>
  </Transition>
</template>
