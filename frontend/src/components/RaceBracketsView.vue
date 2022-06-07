<template>
  <div class="race-brackets">
    <BracketsLevel
      v-for="(brackets, key) in bracketsByLevel"
      :key="key"
      :brackets="brackets"
    />
  </div>
</template>
<script>
import BracketsLevel from 'components/BracketsLevel';
import { Brackets } from 'utils/resources';
import prepareBrackets from 'utils/prepare-brackets';


export default {
  components: {
    BracketsLevel,
  },
  props: {
    type: {
      type: Number,
      isRequired: true,
    },
    raceSlug: {
      type: String,
      isRequired: true,
    },
  },
  data: () => ({
    bracketsByLevel: {},
  }),
  methods: {
    async getBrackets() {
      const brackets = await Brackets.get(this.raceSlug, this.type);
      this.bracketsByLevel = prepareBrackets(brackets);
    },
  },
  created() {
    this.getBrackets();
  },
};
</script>

<style lang="scss" scoped>
.race-brackets {
  display: flex;
  flex-direction: row;
  overflow-x: auto;
}
</style>
