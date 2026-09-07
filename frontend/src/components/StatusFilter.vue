<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(['change']);

const options = [
  { label: 'All', value: null },
  { label: 'Active', value: 'active' },
  { label: 'Graduated', value: 'graduated' },
  { label: 'Dropped', value: 'dropped' },
];

function select(value) {
  if (value !== props.modelValue) {
    emit('change', value);
  }
}
</script>

<template>
  <div class="inline-flex rounded-md border border-ink-soft/20 bg-white p-1 font-sans text-sm">
    <button
      v-for="option in options"
      :key="option.label"
      type="button"
      class="rounded px-3 py-1.5 transition-colors"
      :class="
        modelValue === option.value
          ? 'bg-accent text-white'
          : 'text-ink-soft hover:bg-paper hover:text-ink'
      "
      @click="select(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>
