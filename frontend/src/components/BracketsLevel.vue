<template>
  <div class="brackets-level">
    <RaceBracket
      v-for="(bracket, key) in brackets"
      :key="key"
      :bracket="bracket"
    />
  </div>
</template>
<script>
import RaceBracket from 'components/RaceBracket';


export default {
  components: {
    RaceBracket,
  },
  props: {
    brackets: {
      type: Object,
      isRequired: true,
    },
  },
};
</script>

<style lang="scss">
.brackets-level {
  display: flex;
  flex-direction: column;
  margin-right: 40px;
  justify-content: center;
}
</style>
