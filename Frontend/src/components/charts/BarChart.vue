<template>
  <bar-chart :data="chartData" :options="chartOptions"></bar-chart>
</template>

<script>
import { Bar, mixins } from "vue-chartjs";

export default {
  extends: Bar,
  mixins: [mixins.reactiveData],
  props: ["data", "options"],
  mounted() {
    this.renderChart(this.data, this.options);
  },
};
</script>
