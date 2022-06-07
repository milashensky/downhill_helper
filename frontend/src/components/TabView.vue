<template>
  <div class="tab-view">
    <div v-if="activeTab == 'open'" class="tab-content">
      <RaceBracketsView :type="RACE_TYPES.open" :raceSlug="raceSlug" />
    </div>

    <div v-else-if="activeTab == 'amateurs'" class="tab-content">
      <RaceBracketsView :type="RACE_TYPES.amateurs" :raceSlug="raceSlug" />
    </div>

    <div v-else-if="activeTab == 'masters'" class="tab-content">
      <RaceBracketsView :type="RACE_TYPES.masters" :raceSlug="raceSlug" />
    </div>
    <div v-else class="tab-content">
      <QualificationView :raceSlug="raceSlug" />
    </div>
  </div>
</template>
<script>
import QualificationView from 'components/QualificationView';
import RaceBracketsView from 'components/RaceBracketsView';
import { RACE_TYPES } from 'utils/constants';


export default {
  props: ['activeTab', 'raceSlug'],
  components: {
    QualificationView,
    RaceBracketsView,
  },
  data: () => ({
    RACE_TYPES,
  }),
};
</script>
<style lang="scss" scoped>
.tab-view {
  padding-top: 40px;

  .tab-content {
    display: flex;
    justify-content: center;
  }
}
</style>
