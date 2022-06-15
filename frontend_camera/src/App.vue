<template>
  <div class="app-container">
    <CameraScreen
      v-if="shouldShowCamera"
      :raceId="raceId"
      @goBack="goBack"
    />

    <RaceSelectScreen v-else @select="setRaceId"/>
  </div>
</template>

<script>
import RaceSelectScreen from 'components/RaceSelectScreen';
import CameraScreen from 'components/CameraScreen';


export default {

  components: {
    RaceSelectScreen,
    CameraScreen,
  },


  data: () => ({
    raceId: undefined,
    shouldShowCamera: false,
  }),


  methods: {

    setRaceId(id) {
      this.raceId = id;
      window.location.hash = this.raceId;
      if (this.raceId) {
        this.shouldShowCamera = true;
      }
    },


    goBack() {
      this.shouldShowCamera = false;
    },

  },


  created() {
    this.setRaceId(window.location.hash.slice(1));
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

.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  box-sizing: border-box;

  .btn {
    padding: 20px;
    background-color: #858585;
    color: white;
    width: 100%;
    display: flex;
    border: 0;
    border-radius: 15px;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    font-size: 20px;
    margin-top: 10px;

    &.submit {
      background-color: #697cb3;
    }
  }

  select {
    padding: 20px;
    border: solid 1px #858585;
    background-color: white;
    color: #1d1d1f;
    width: 100%;
    display: flex;
    border-radius: 15px;
    font-size: 20px;
    margin-top: 10px;
  }
}
</style>
