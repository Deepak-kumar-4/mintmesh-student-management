<script setup>
import { onMounted, onBeforeUnmount } from 'vue';

defineProps({
  message: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['confirm', 'cancel']);

function handleKeydown(event) {
  if (event.key === 'Escape') {
    emit('cancel');
  }
}

onMounted(() => window.addEventListener('keydown', handleKeydown));
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeydown));
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-ink/50 p-4 font-sans"
    @click.self="$emit('cancel')"
  >
    <div class="w-full max-w-sm rounded-md bg-white p-6 shadow-xl">
      <p class="text-sm text-ink">{{ message }}</p>
      <div class="mt-6 flex justify-end gap-3">
        <button
          type="button"
          class="rounded border border-ink-soft/30 px-4 py-2 text-sm text-ink hover:bg-paper"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
        <button
          type="button"
          class="rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:opacity-90"
          @click="$emit('confirm')"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>
