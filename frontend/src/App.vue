<template>
  <div v-if="race.name" class="container" :style="{ backgroundImage: `url(/media${race.background_image_url})` }">
    <div v-if="hasTabs" class="race-container">

      <TabsList
        :race="race"
        :activeTab="activeTab"
        @change="setTab"
      />

      <TabView
        :raceSlug="raceSlug"
        :activeTab="activeTab"
      />
    </div>
    <div v-else>
      Coming soon...
    </div>
  </div>
  <div v-else>
    Loading...
  </div>
</template>

<script>
import { Race } from 'utils/resources';
import TabsList from 'components/TabsList';
import TabView from 'components/TabView';


export default {
  components: {
    TabsList,
    TabView,
  },
  data: () => ({
    race: {},
    activeTab: window.location.hash.slice(1) || 'qualification',
  }),
  methods: {
    setTab(tab) {
      window.location.hash = tab;
      this.activeTab = tab;
    },
    async getRace() {
      const race = await Race.get(this.raceSlug);
      this.race = race;
    },
  },
  computed: {
    raceSlug() {
      return window.location.pathname.split('/').filter(Boolean).pop();
    },
    hasTabs() {
      return this.race.is_qualification_open
        || this.race.has_masters
        || this.race.has_open
        || this.race.has_amateurs;
    },
  },
  created() {
    this.getRace();
  },
};
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

body {
  font-family: -apple-system, Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #1d1d1f;
  margin: 0;
  font-size: 17px;
  font-weight: 400;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
  padding: 10px;
  box-sizing: border-box;

  &:before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    pointer-events: none;
    opacity: .5;
    background-color: #fff;
    z-index: 1;
  }

  .race-container {
    z-index: 2;
    display: flex;
    flex-direction: column;
    max-width: 980px;
    width: 100%;
    padding-top: 5vh;
  }
}
</style>
