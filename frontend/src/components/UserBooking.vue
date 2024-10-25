<template>
  <div>
    <br />
    <br />
    <div class="row">
      <div
        class="col-md-10 mx-auto"
        v-for="(booking, index) in bookings"
        :key="index"
      >
        <!-- Booking Card -->
        <div class="card mb-3">
          <div class="card-body">
            <!-- Display Booking Information -->
            <h5 class="card-title">Booking {{ index + 1 }}</h5>
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <p class="card-text">
                  <strong>Show Name:</strong>
                  {{ getShowName(booking.show_id) }} <br />
                  <strong>Show Rating:</strong>
                  {{ getShowRating(booking.show_id) }} <br />
                  <strong>Tickets Booked:</strong> {{ booking.tickets_booked }}
                </p>
              </div>
              <a
                :href="'/rate/' + booking.show_id + '/show'"
                class="btn btn-outline-success"
              >
                Rate Show
              </a>
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
  name: "UserBookingPage",
  data() {
    return {
      bookings: [],
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      showData: {}, // Use an object to store show data by show_id
    };
  },

  methods: {
    async fetchUserBooking() {
      try {
        if (this.userSession && this.userSession.token) {
          // Set the Authorization header with the JWT token
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const response = await axios.get(
            "http://127.0.0.1:1234/vue/user/bookings"
          );
          this.bookings = response.data.bookings;
          console.log(this.bookings);

          for (const booking of this.bookings) {
            await this.fetchShowfromBooking(booking.show_id);
          }
        }
      } catch (error) {
        console.error("Error fetching bookings:", error);
      }
    },
    async fetchShowfromBooking(show_id) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:1234/vue/theater/show/${show_id}`
        );
        const showData = response.data;

        // Use the show_id as the key to store show data
        this.$set(this.showData, show_id, showData);
      } catch (error) {
        console.error(
          `Error fetching show data for show_id ${show_id}:`,
          error
        );
      }
    },
    getShowName(show_id) {
      const show = this.showData[show_id];
      return show ? show.show_name : "N/A";
    },
    getShowRating(show_id) {
      const show = this.showData[show_id];
      return show ? show.rating : "N/A";
    },
  },

  async created() {
    await this.fetchUserBooking();
  },
};
</script>
