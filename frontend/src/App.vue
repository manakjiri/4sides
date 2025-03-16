<script setup lang="ts">
import ExplanationComponent from './components/ExplanationComponent.vue'
import InterpretationComponent from './components/InterpretationComponent.vue'
</script>

<template>
  <header>
    <div class="wrapper">
      <ExplanationComponent />
    </div>
  </header>

  <main>
    <InterpretationComponent />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
