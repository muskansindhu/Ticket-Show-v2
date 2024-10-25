<template>
  <div class="container py-4 py-xl-5">
    <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-3">
      <div class="col-md-12 col-xl-12">
        <div>
          <div class="row">
            <div
              class="btn-group"
              role="group"
              style="
                padding-top: 15px;
                padding-left: 30px;
                padding-bottom: 15px;
              "
            >
              <button
                class="text-center btn btn-success btn-lg me-2 disabled"
                type="submit"
                v-if="this.success"
              >
                Successfully Exported!
              </button>
              <button
                class="text-center btn btn-success btn-sm me-2"
                type="submit"
                v-else
                @click="export_data"
              >
                Email Data as CSV
              </button>
            </div>
            <br />
          </div>
          <div class="py-4 d-flex">
            <div>
              <h4>{{ this.theaterData.theater_name }}'s Analytics</h4>
              <p>
                The chart below shows the number of seats booked for every show
                in
                {{ this.theaterData.theater_name }}.
              </p>
            </div>
          </div>
          <img
            alt="Analytics Image"
            class="rounded img-fluid d-block w-100 border border-dark rounded"
            style="height: 100%; object-fit: cover"
            :src="compSeatsBookedImg"
          />
          <br />
          <br />
          <div>
            <p>
              The chart below shows the ratings received by every show in
              {{ this.theaterData.theater_name }}.
            </p>
          </div>
        </div>
        <br />
        <img
          alt="Analytics Image"
          class="rounded img-fluid d-block w-100 border border-dark rounded"
          style="height: 40%; object-fit: cover"
          :src="compRatingImg"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AnalyticsView",

  data() {
    return {
      theater: this.$route.params.id,
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      success: false,
      theaterData: null,
    };
  },
  methods: {
    async fetchData() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;
        const theater_id = this.$route.params.id;
        await axios

          .get(`http://127.0.0.1:1234/vue/analytics/${theater_id}`)
          .catch(() => {
            // console.log(error);
          });
      }
      this.success = false;
      this.$forceUpdate();
    },
    async fetchTheaterData() {
      try {
        if (this.userSession) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const theater_id = this.$route.params.id;

          const response = await axios.get(
            `http://127.0.0.1:1234/vue/theater/${theater_id}`
          );
          this.theaterData = response.data.theater;
        }
      } catch (error) {
        console.error("Error fetching theater:", error);
      }
    },
    export_data() {
      if (this.userSession) {
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.userSession.token}`;
        const theater_id = this.$route.params.id;
        axios
          .get(`http://127.0.0.1:1234/vue/analytics/export_data/${theater_id}`)
          .catch(() => {
            // console.log(error);
          });

        this.success = true;
      }
    },
  },
  computed: {
    compSeatsBookedImg() {
      return (
        "http://127.0.0.1:1234/static/img/Analytics/" +
        this.theaterData.theater_name +
        "/Seats Booked.png"
      );
    },
    compRatingImg() {
      return (
        "http://127.0.0.1:1234/static/img/Analytics/" +
        this.theaterData.theater_name +
        "/Rating.png"
      );
    },
  },
  async beforeMount() {
    this.fetchData();
  },
  mounted() {
    document.title = "Analytics";
  },
  created() {
    this.fetchTheaterData();
    const isFirstVisit = localStorage.getItem("firstVisit") !== "true";

    if (isFirstVisit) {
      localStorage.setItem("firstVisit", "true");
      location.reload();
    }
  },
};
</script>
