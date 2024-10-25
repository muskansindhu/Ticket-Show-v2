<template>
  <div>
    <br />
    <br />
    <div class="text-center">
      <h6>
        Welcome to Ticket-Show, your one stop destination for booking shows.
      </h6>
    </div>
    <div class="row justify-content-center">
      <div class="col-md-10" v-for="(theater, index) in theaters" :key="index">
        <br />
        <div class="card mb-3">
          <div class="card-header d-flex justify-content-between">
            <div class="d-flex justify-content-between align-items-baseline">
              <div>
                <h5 class="card-title">{{ theater.theater_name }},</h5>
              </div>
              &nbsp;
              <div>
                <h6>{{ theater.location }},</h6>
              </div>
              &nbsp;
              <div>
                <h6><strong>Capacity:</strong> {{ theater.capacity }}</h6>
              </div>
            </div>

            <div class="buttons"></div>
          </div>
          <div>
            <div class="card-body">
              <!-- Show cards -->
              <div class="row" v-if="theater.shows && theater.shows.length > 0">
                <div
                  class="col-md-4"
                  v-for="(show, showIndex) in theater.shows"
                  :key="showIndex"
                >
                  <div class="card mb-3">
                    <div class="card-body text-center">
                      <div>
                        <img
                          :src="posterImg(show.show_name)"
                          alt="Image"
                          class="card-img-top w-100"
                          style="max-height: 400px; max-width: 100%"
                        />
                      </div>
                      <h6 class="card-title">{{ show.show_name }}</h6>
                      <p class="card-text">
                        <strong>Show Time:</strong> {{ show.time }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <p v-else>No shows available for this theater.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "PreviewPage",
  data() {
    return {
      theaters: [],
      formData: {
        theater_name: "",
        location: "",
        capacity: "",
      },
    };
  },
  methods: {
    async getTheater() {
      const path = "http://127.0.0.1:1234/vue/all/theater";
      try {
        const response = await axios.get(path);
        this.theaters = response.data.theaters;
        this.loadShowsForTheaters();
      } catch (error) {
        console.error("Error fetching theaters:", error);
      }
    },

    async getShowsForTheater(theater) {
      const path = `http://127.0.0.1:1234/vue/theater/${theater.roll}/show`;
      try {
        const response = await axios.get(path);
        this.$set(theater, "shows", response.data.show);
      } catch (error) {
        console.error(
          `Error fetching shows for theater ${theater.roll}:`,
          error
        );
      }
    },

    async addTheaterForm() {
      try {
        const formData = new FormData();
        formData.append("theater_name", this.formData.theater_name);
        formData.append("location", this.formData.location);
        formData.append("capacity", this.formData.capacity);

        const response = await axios.post(
          "http://127.0.0.1:1234/vue/theater",
          formData
        );

        console.log(response);
        this.getTheater();
      } catch (error) {
        console.error("AxiosError:", error);

        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred. Theater was not added.");
      }
    },

    loadShowsForTheaters() {
      for (const theater of this.theaters) {
        this.getShowsForTheater(theater);
      }
    },

    initForm() {
      this.formData.theater_name = "";
      this.formData.location = "";
      this.formData.capacity = "";
    },

    onSubmit(e) {
      e.preventDefault();
      this.$refs.theaterModal.hide();
      const payload = {
        theater_name: this.formData.theater_name,
        location: this.formData.location,
        capacity: this.formData.capacity,
      };
      this.addTheaterForm(payload);
    },
    posterImg(showName) {
      return `http://127.0.0.1:1234/static/img/Posters/${showName}.webp`;
    },
  },
  async created() {
    await this.getTheater();
  },
};
</script>
