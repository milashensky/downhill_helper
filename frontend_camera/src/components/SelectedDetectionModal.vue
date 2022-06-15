<template>
  <div class="container">
    <div class="modal">
      <canvas ref="canvas" />
      <button type="button" class="btn submit" @click="submit">Submit</button>
      <button type="button" class="btn" @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { SensorSignal } from 'utils/resources';
import { SENSOR_MARKS } from 'utils/constants';


export default {

  props: {
    selected: {
      type: Object,
      required: true,
    },
  },


  methods: {

    async submit() {
      const sensorMark = Cookies.get('sensor_mark') || SENSOR_MARKS.start;
      const data = {
        race_id: window.location.hash.slice(1),
        signal_registered_at: this.selected.time,
        sensor_mark: sensorMark,
      };
      await SensorSignal.post(data);
      this.$emit('remove');
    },

  },


  mounted() {
    const context = this.$refs.canvas.getContext('2d');
    context.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
    this.$refs.canvas.width = this.selected.crossingFrame.width;
    this.$refs.canvas.height = this.selected.crossingFrame.height;
    context.putImageData(this.selected.crossingFrame, 0, 0);
  },

};
</script>

<style lang="scss" scoped>
.container {
  margin: 10px;
  position: absolute;
  z-index: 900;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .modal {
    margin-top: 5vh;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
    background-color: #ffffff85;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>
