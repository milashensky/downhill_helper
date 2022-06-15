<template>
  <div class="container">
    <ul class="crossings" v-show="!selected">
      <li
        class="crossing"
        v-for="item, key in detected"
        :key="key"
        @click="select(key)"
      >
        <span>Detection at {{item.time}}</span>
        <span
          class="delete"
          @click.stop="$emit('deleteCrossing', key)"
        />
      </li>
    </ul>

    <SelectedDetectionModal
      v-if="selected"
      :selected="selected"
      @close="selectedKey = undefined"
      @remove="$emit('deleteCrossing', selectedKey)"
    />
  </div>
</template>

<script>
import SelectedDetectionModal from 'components/SelectedDetectionModal';


export default {

  components: {
    SelectedDetectionModal,
  },


  props: {
    detected: {
      type: Object,
    },
  },


  data: () => ({
    selectedKey: undefined,
  }),


  computed: {

    selected() {
      if (!this.selectedKey) {
        return null;
      }
      return this.detected[this.selectedKey];
    },

  },


  methods: {

    select(key) {
      this.selectedKey = key;
    },

  },

};
</script>

<style lang="scss" scoped>
.container {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding-top: 10vh;
  z-index: 100;

  .crossings {
    padding: 0;
    margin: 0;
    max-height: 80vh;
    overflow-y: auto;
    list-style: none;
    background-color: #ffffff85;
    border-radius: 5px;

    .crossing {
      padding: 20px 10px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;

      &:not(:last-child) {
        border-bottom: solid 1px #b1b1b1;
      }

      .delete {
        width: 20px;
        height: 20px;
        display: block;
        flex-shrink: 0;
        position: relative;
        z-index: 900;

        &::before,
        &::after {
          content: '';
          position: absolute;
          width: 28px;
          height: 4px;
          background-color: red;
          top: 0;
        }

        &::before {
          left: 0;
          transform: rotate(45deg);
          transform-origin: left;
        }
        &::after {
          right: 0;
          transform: rotate(-45deg);
          transform-origin: right;
        }
      }
    }
  }

}
</style>
