<script setup>
import { ref } from 'vue';
import StudentList from './components/StudentList.vue';
import StudentForm from './components/StudentForm.vue';
import ConfirmDialog from './components/ConfirmDialog.vue';
import { deleteStudent } from './services/api.js';

const studentListRef = ref(null);
const panel = ref(null); // null | { mode: 'create' } | { mode: 'edit', student } | { mode: 'delete', student }
const actionError = ref('');

function openCreate() {
  actionError.value = '';
  panel.value = { mode: 'create' };
}

function openEdit(student) {
  actionError.value = '';
  panel.value = { mode: 'edit', student };
}

function openDelete(student) {
  actionError.value = '';
  panel.value = { mode: 'delete', student };
}

function closePanel() {
  panel.value = null;
}

function handleSaved() {
  closePanel();
  studentListRef.value?.refresh();
}

async function handleConfirmDelete() {
  const student = panel.value?.student;
  if (!student) return;
  try {
    await deleteStudent(student.id);
    closePanel();
    studentListRef.value?.refresh();
  } catch (err) {
    closePanel();
    actionError.value = `Couldn't delete ${student.first_name} ${student.last_name}. Please try again.`;
  }
}
</script>

<template>
  <div class="mx-auto max-w-5xl px-6 py-10">
    <div
      v-if="actionError"
      class="mb-4 flex items-start justify-between gap-3 rounded border border-accent/30 bg-accent/10 px-4 py-3 font-sans text-sm text-accent"
    >
      <span>{{ actionError }}</span>
      <button type="button" class="font-medium" @click="actionError = ''">&times;</button>
    </div>

    <StudentList ref="studentListRef" @create="openCreate" @edit="openEdit" @delete="openDelete" />

    <StudentForm
      v-if="panel?.mode === 'create' || panel?.mode === 'edit'"
      :key="panel.mode + '-' + (panel.student?.id ?? 'new')"
      :student="panel.mode === 'edit' ? panel.student : null"
      @saved="handleSaved"
      @cancel="closePanel"
    />

    <ConfirmDialog
      v-if="panel?.mode === 'delete'"
      :message="`Delete ${panel.student.first_name} ${panel.student.last_name}? This can't be undone.`"
      @confirm="handleConfirmDelete"
      @cancel="closePanel"
    />
  </div>
</template>
