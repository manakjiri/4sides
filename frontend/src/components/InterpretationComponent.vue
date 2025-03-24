<script setup lang="ts">
import { ref, watch, computed } from 'vue'

const MIN_MESSAGE_LENGTH = 5
const MAX_MESSAGE_LENGTH = 256

enum InterpretationLevel {
  FACTUAL = 'factual',
  REVEALING = 'revealing',
  RELATIONSHIP = 'relationship',
  APPEAL = 'appeal',
}

interface UserInputInterpretation {
  level: InterpretationLevel
  message: string
  interpretation: string
}

const values = ref<{ [id: string]: UserInputInterpretation | null }>({
  [InterpretationLevel.FACTUAL]: null,
  [InterpretationLevel.REVEALING]: null,
  [InterpretationLevel.RELATIONSHIP]: null,
  [InterpretationLevel.APPEAL]: null,
})

const url = 'wss://sides.manakjiri.cz/api/ws'
const ws = ref<WebSocket | null>(null)

function connect() {
  console.log('Connecting to', url)
  ws.value = new WebSocket(url)

  ws.value.onopen = () => {
    console.log('Connected to server')
  }

  ws.value.onclose = () => {
    console.log('Disconnected from server')
    ws.value = null
    setTimeout(function () {
      connect()
    }, 5000)
  }

  ws.value.onerror = (event) => {
    console.error('Websocket error:', event)
    ws.value?.close()
  }

  ws.value.onmessage = (event) => {
    const intr: UserInputInterpretation = JSON.parse(event.data)
    if (!!actual_message.value) {
      values.value[intr.level] = intr
    }
  }
}

connect()

const message = ref<string>('')
const actual_message = ref<string>('')
watch(message, (new_message) => {
  new_message = new_message.trim()
  if (!new_message || new_message.length < MIN_MESSAGE_LENGTH) {
    actual_message.value = ''
    for (const level of Object.values(InterpretationLevel)) {
      values.value[level] = null
    }
  } else if (new_message.length >= MIN_MESSAGE_LENGTH) {
    if (new_message.length > MAX_MESSAGE_LENGTH) {
      new_message = new_message.slice(0, MAX_MESSAGE_LENGTH)
    }
    actual_message.value = new_message
    ws.value?.send(new_message)
  }
})

const isLoading = computed(() => {
  return (level: InterpretationLevel) => {
    if (!actual_message.value) {
      return false
    }
    return values.value[level]?.message !== actual_message.value
  }
})

function capitalizeFirstLetter(val: string): string {
  return String(val).charAt(0).toUpperCase() + String(val).slice(1)
}
</script>

<template>
  <input
    type="text"
    placeholder="Start typing a message you want interpreted"
    v-model="message"
    class="wide-input"
    @input="message = message.slice(0, MAX_MESSAGE_LENGTH)"
  />
  <section class="interpretations-section">
    <div
      v-for="level in Object.values(InterpretationLevel)"
      :key="level"
      :class="['interpretation-box', level.toLowerCase()]"
    >
      <h3>
        {{ capitalizeFirstLetter(level.toString()) }}
        <div v-if="isLoading(level)" class="loading">Loading...</div>
      </h3>
      {{ values[level]?.interpretation }}
    </div>
  </section>
</template>

<style scoped>
.wide-input {
  width: 100%;
  max-width: 200ch;
  padding: 1rem;
  margin-bottom: 2rem;
  margin-top: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  transition:
    border-color 0.3s,
    background-color 0.3s;
}

.wide-input:focus {
  border-color: var(--color-border-hover);
  background-color: var(--color-background);
  outline: none;
}

.interpretation-box {
  width: 100%;
  max-width: 200ch;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  color: var(--color-text);
  text-align: left;
}

.loading {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text);
  float: right;
}
</style>
