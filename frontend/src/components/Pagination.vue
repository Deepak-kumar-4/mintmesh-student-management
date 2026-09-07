<script setup>
const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['change']);

function goPrevious() {
  if (props.currentPage > 1) {
    emit('change', props.currentPage - 1);
  }
}

function goNext() {
  if (props.currentPage < props.totalPages) {
    emit('change', props.currentPage + 1);
  }
}
</script>

<template>
  <div class="flex items-center justify-center gap-4 font-sans text-sm">
    <button
      type="button"
      :disabled="currentPage <= 1"
      class="rounded border border-ink-soft/20 px-3 py-1.5 transition-colors"
      :class="
        currentPage <= 1
          ? 'cursor-not-allowed text-ink-soft/40'
          : 'text-ink hover:bg-paper'
      "
      @click="goPrevious"
    >
      Previous
    </button>
    <span class="text-ink-soft">Page {{ currentPage }} of {{ Math.max(totalPages, 1) }}</span>
    <button
      type="button"
      :disabled="currentPage >= totalPages"
      class="rounded border border-ink-soft/20 px-3 py-1.5 transition-colors"
      :class="
        currentPage >= totalPages
          ? 'cursor-not-allowed text-ink-soft/40'
          : 'text-ink hover:bg-paper'
      "
      @click="goNext"
    >
      Next
    </button>
  </div>
</template>
