<template>
  <div id="app">
    <SentimentAnalyzer />
  </div>
</template>

<script>
import SentimentAnalyzer from './components/SentimentAnalyzer.vue';

export default {
  name: 'App',
  components: {
    SentimentAnalyzer
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

body {
  font-family: 'Inter', 'Segoe UI', sans-serif;
  background-color: #0f172a;
  color: #f8fafc;
}

#app {
  width: 100%;
  min-height: 100vh;
}
</style>