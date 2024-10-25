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
                      <p class="card-text">
                        <strong>Available Seats:</strong>
                        {{
                          availableSeats(theater.capacity, show.seats_booked)
                        }}
                      </p>
                      <template
                        v-if="
                          availableSeats(theater.capacity, show.seats_booked) >
                          0
                        "
                      >
                        <a
                          :href="'/show/' + show.roll + '/booking'"
                          class="btn btn-outline-success btn-sm"
                        >
                          Book now
                        </a>
                      </template>
                      <template v-else>
                        <button class="btn btn-outline-danger btn-sm" disabled>
                          Housefull
                        </button>
                      </template>
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
  name: "UserDashPage",
  data() {
    return {
      theaters: [],
      formData: {
        theater_name: "",
        location: "",
        capacity: "",
      },
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
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

    loadShowsForTheaters() {
      for (const theater of this.theaters) {
        this.getShowsForTheater(theater);
      }
    },
    posterImg(showName) {
      return `http://127.0.0.1:1234/static/img/Posters/${showName}.webp`;
    },
    availableSeats(theaterCapacity, showSeatsBooked) {
      return theaterCapacity - showSeatsBooked;
    },
  },
  async created() {
    await this.getTheater();
  },
};
</script>
