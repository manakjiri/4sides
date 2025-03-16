<template>
  <div class="greetings">
    <h1>Four-sides model</h1>
    <p>
      <a href="https://en.wikipedia.org/wiki/Four-sides_model">The four-sides model</a> (also known
      as communication square or four-ears model) is a communication model postulated in 1981 by
      German psychologist Friedemann Schulz von Thun. According to this model every message has four
      facets though not the same emphasis might be put on each. The four sides of the message are
      <mark class="factual">fact</mark>, <mark class="revealing">self-disclosure</mark>,
      <mark class="relationship">social relationship</mark> between sender and receiver, and
      <mark class="appeal">wish or want</mark>
    </p>
    <p>
      This tool uses an LLM to attempt to distill out each layer of a message. Enter a sentence, and
      watch it being broken down into its four aspects. Adjust wording to see how emphasis shifts!
    </p>
    <em style="font-size: 0.8rem">
      Note: The first response might be slower when the model is initializing. If there is a lot of
      traffic, the response time might be slower in general.
    </em>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

p {
  margin-bottom: 1rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
