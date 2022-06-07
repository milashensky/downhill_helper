<template>
  <table class="bracket">
    <tbody>
      <tr
        v-for="contestant in bracket"
        :key="contestant.position"
        :style="{ order: contestant.qualification_number }"
      >
        <td class="quali-number">
          {{contestant.qualification_number}}
        </td>
        <td class="contestant-name">
          <span v-if="contestant.helmet_number">№ {{contestant.helmet_number}}: </span>
          <span>{{contestant.contestant_name}}</span>
        </td>
        <td  class="position">
          {{contestant.position}}
        </td>
      </tr>
    </tbody>
  </table>
</template>
<script>
export default {
  props: {
    bracket: {
      type: Array,
      isRequired: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.bracket {
  margin-bottom: 20px;

  tbody {
    display: flex;
    flex-direction: column;
    text-align: start;

    td,
    th {
      white-space: nowrap;
      padding: 5px;
      padding-right: 10px
    }

    tr {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      white-space: nowrap;

      .position,
      .quali-number {
        width: 30px;
      }

      .contestant-name {
        flex-grow: 1;
      }
    }
  }
}
</style>
