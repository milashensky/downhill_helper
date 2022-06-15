<template>
  <form @submit.prevent="submit" class="form">
    <label for="raceId">
      Enter Race Id:
      <input
        v-model="raceId"
        type="number"
        id="raceId"
      >
    </label>

    <label for="sensorMark">
      Sensor mark:
      <select name="sensorMark" id="sensorMark" @change="setSensorMark">
        <option
          v-for="option, key in SENSOR_MARKS"
          :key="key"
          :value="key"
        >
          {{option}}
        </option>
      </select>
    </label>

    <button class="btn" type="submit">
      Select
    </button>
  </form>
</template>

<script>
import Cookies from 'js-cookie';
import { SENSOR_MARKS } from 'utils/constants';


export default {

  data: () => ({
    raceId: window.location.hash.slice(1),
    SENSOR_MARKS,
  }),


  methods: {

    submit() {
      // todo: add validation ?
      this.$emit('select', parseInt(this.raceId));
    },


    setSensorMark(event) {
      const mark = event.target.value;
      Cookies.set('sensor_mark', mark);
    },

  },

};
</script>

<style lang="scss" scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;

  label {
    padding-top: 20px;
    display: flex;
    flex-direction: column;
  }

  input {
    padding: 20px;
    border: solid 1px #858585;
    background-color: white;
    color: #1d1d1f;
    display: flex;
    border-radius: 15px;
    font-size: 20px;
    margin-top: 10px;
  }
}
</style>
