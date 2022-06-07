<template>
  <div class="qualification-container">
    <table class="qualification-table">
      <thead>
        <th>Name</th>
        <th>Number</th>
        <th>Best time</th>
        <th v-for="i in maxAttempts" :key="i">
          Attempt {{i}}
        </th>
      </thead>
      <tbody>
        <tr
          v-for="contestant in qualification"
          :key="contestant.contestant_id"
        >
          <td>{{contestant.contestant_name}}</td>
          <td>{{contestant.helmet_number}}</td>
          <td>{{contestant.bestTime}} sec.</td>
          <td v-for="(time, id) in contestant.times" :key="id">
            {{time}} sec.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import prepareQaulification from 'utils/prepare-qaulification';
import { Qualification } from 'utils/resources';


export default {
  props: {
    raceSlug: {
      type: String,
      isRequired: true,
    },
  },
  data: () => ({
    qualification: [],
    maxAttempts: 1,
  }),
  methods: {
    async getQualification() {
      const qualis = await Qualification.get(this.raceSlug);
      [this.qualification, this.maxAttempts] = prepareQaulification(qualis);
    },
  },
  created() {
    this.getQualification();
  },
};
</script>

<style lang="scss" scoped>
.qualification-container {
  overflow-x: auto;

  .qualification-table {
    text-align: start;

    th {
      font-weight: 500;
    }
    td,
    th {
      white-space: nowrap;
      padding: 5px;
      padding-right: 30px
    }
  }
}
</style>
