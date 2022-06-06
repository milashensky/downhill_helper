<template>
  <div v-if="race.name">
  </div>
  <div v-else>
    Loading...
  </div>
</template>

<script>
import { Race } from 'utils/resources';


export default {
  name: 'App',
  data: () => ({
    race: {},
  }),
  methods: {
    async getRace() {
      const slug = 'test_race';
      const race = await Race.get(slug);
      this.race = race;
    },
  },
  created() {
    this.getRace();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
