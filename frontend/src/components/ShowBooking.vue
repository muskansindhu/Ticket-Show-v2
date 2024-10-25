<template>
  <div>
    <div class="container mt-5 pt-5 justify-content-center">
      <div class="row">
        <div class="col-md-6 mx-auto">
          <div class="card">
            <div class="card-body text-center">
              <h3>Show Booking</h3>
              <form @submit.prevent="submitBooking">
                <input
                  type="text"
                  name="show_name"
                  id="show_name"
                  placeholder="Show Name"
                  required
                  class="form-control my-4 py-2"
                  v-model="formData.show_name"
                  readonly
                />
                <input
                  type="text"
                  name="rating"
                  id="rating"
                  placeholder="Rating"
                  required
                  class="form-control my-4 py-2"
                  v-model="formData.rating"
                  readonly
                />
                <input
                  type="text"
                  name="time"
                  id="time"
                  placeholder="Time"
                  required
                  class="form-control my-4 py-2"
                  v-model="formData.time"
                  readonly
                />
                <input
                  type="number"
                  min="0"
                  step="1"
                  name="price"
                  id="price"
                  placeholder="Price"
                  required
                  class="form-control my-4 py-2"
                  v-model="formData.price"
                  readonly
                />
                <input
                  type="number"
                  min="1"
                  step="1"
                  name="tickets_booked"
                  id="tickets_booked"
                  placeholder="Number of Seats"
                  required
                  class="form-control my-4 py-2"
                  v-model="formData.tickets_booked"
                />
                <p>Total Payable Amount: {{ totalPrice }}</p>
                <input
                  type="submit"
                  value="Confirm Booking"
                  class="btn btn-success"
                />
              </form>
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
  name: "ShowBookingPage",
  data() {
    return {
      formData: {
        show_name: "",
        rating: "",
        time: "",
        price: "",
      },
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
    };
  },
  created() {
    this.populateForm();
  },
  computed: {
    totalPrice() {
      if (this.formData.tickets_booked) {
        return this.formData.price * this.formData.tickets_booked;
      } else {
        return 0;
      }
    },
  },
  methods: {
    async getShow() {
      try {
        const show_id = this.$route.params.id;
        const response = await axios.get(
          `http://127.0.0.1:1234/vue/theater/show/${show_id}`
        );
        return response.data;
      } catch (error) {
        console.error("AxiosError:", error);

        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred. Show details not available");
      }
    },

    async populateForm() {
      try {
        const show = await this.getShow();

        if (show && show.show_name) {
          this.formData.show_name = show.show_name;
          this.formData.price = show.price;
          this.formData.time = show.time;
          this.formData.rating = show.rating;
        } else {
          // Handle the case where show data is missing or invalid
          console.error("Show data is missing or invalid");
          // You might want to show an error message to the user or take other actions.
        }
      } catch (error) {
        console.error("Error while populating form:", error);
      }
    },

    async submitBooking() {
      try {
        const show_id = this.$route.params.id;
        const bookingData = new FormData();
        bookingData.append("show_id", show_id);
        bookingData.append("tickets_booked", this.formData.tickets_booked);
        if (this.userSession && this.userSession.token) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const response = await axios.post(
            "http://127.0.0.1:1234/vue/booking",
            bookingData
          );
          console.log(response);
          alert("Booking Done Succesfully.");
        }
      } catch (error) {
        console.error("AxiosError:", error);

        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred while confirming the booking.");
      }
    },
  },
};
</script>
