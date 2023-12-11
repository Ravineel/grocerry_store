<template>
  <Bar
    id="my-chart-id"
    :options="chartOptions"
    :data="chartData"
    v-if="chart_loaded"
  />
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { onMounted } from "vue";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "BarChart",
  components: { Bar },
  props: {
    chartType: {
      type: String,
      default: "manager",
    },
  },

  data() {
    return {
      chartData: {},
      chart_loaded: false,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        height: 300,
      },
    };
  },

  beforeMount() {
    if (this.chartType === "manager") {
      this.$store.dispatch("user/getManagerChartData").then((data) => {
        if (!sessionStorage.getItem("isAuthenticated")) {
          this.$router.push("/login");
        } else if (this.$store.getters["user/error"]) {
          this.$toast.error(this.$store.getters["user/error"]);
        }

        this.chartData = {
          labels: ["Total Manager", "Active Manager", "Inactive Manager"],
          datasets: [
            {
              label: "Manager",
              backgroundColor: [
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(255, 99, 132, 0.2)",
              ],
              borderColor: [
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(255, 99, 132, 1)",
              ],
              borderWidth: 1,
              data: [
                data.total_managers_count,
                data.active_managers_count,
                data.inactive_managers_count,
              ],
            },
          ],
        };
        this.chart_loaded = true;
      });
    } else if (this.chartType === "user") {
      this.$store.dispatch("user/getDataCount").then((data) => {
        if (!sessionStorage.getItem("isAuthenticated")) {
          this.$router.push("/login");
        } else if (this.$store.getters["user/error"]) {
          this.$toast.error(this.$store.getters["user/error"]);
        }
        this.chartData = {
          labels: [
            "Total User",
            "Total Products",
            "Total Categories,",
            "Total Orders",
          ],
          datasets: [
            {
              label: "counts",
              backgroundColor: [
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(255, 99, 132, 0.2)",
                "rgba(153, 102, 255, 0.2)",
              ],
              borderColor: [
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(255, 99, 132, 1)",
                "rgba(153, 102, 255, 1)",
              ],
              borderWidth: 1,
              data: [
                data.total_users,
                data.total_products,
                data.total_categories,
                data.total_orders,
              ],
            },
          ],
        };
        this.chart_loaded = true;
      });
    }
  },
};
</script>
