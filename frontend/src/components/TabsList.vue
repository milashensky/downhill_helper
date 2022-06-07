<template>
  <div class="tabs">
    <div
      v-if="race.is_qualification_open"
      class="tab"
      :class="activeTab === 'qualification' && 'active'"
      @click="$emit('change', 'qualification')"
    >
      Qualification
    </div>
    <div
      v-if="race.has_open"
      class="tab"
      :class="activeTab === 'open' && 'active'"
      @click="$emit('change', 'open')"
    >
      Open
    </div>
    <div
      v-if="race.has_amateurs"
      class="tab"
      :class="activeTab === 'amateurs' && 'active'"
      @click="$emit('change', 'amateurs')"
    >
      Amateurs
    </div>
    <div
      v-if="race.has_masters"
      class="tab"
      :class="activeTab === 'masters' && 'active'"
      @click="$emit('change', 'masters')"
    >
      Masters
    </div>
  </div>
</template>
<script>
export default {
  props: ['race', 'activeTab'],
};
</script>
<style lang="scss">
.tabs {
  display: flex;
  justify-content: space-around;

  .tab {
    flex-grow: 1;
    border-bottom: 2px solid;
    font-weight: 500;
    border-color: transparent;
    transition: all .5s ease;
    opacity: .8;
    cursor: pointer;
    padding: 10px 5px;

    &.active {
      opacity: 1;
      border-color: #813c3a;
    }
  }
}
</style>
