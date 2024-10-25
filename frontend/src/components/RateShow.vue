<template>
  <div class="container mt-5 pt-5 justify-content-center">
    <div class="row">
      <div class="col-md-6 mx-auto">
        <div class="card">
          <div class="card-body text-center">
            <form @submit.prevent="submitBooking">
              <h3>Rate Show</h3>
              <input
                type="text"
                name="show_name"
                id="show_name"
                class="form-control my-4 py-2"
                placeholder="Show Name"
                v-model="formData.show_name"
                readonly
                required
              />
              <input
                type="number"
                name="rate"
                id="rate"
                max="5"
                min="1"
                class="form-control my-4 py-2"
                placeholder="Rate"
                v-model="formData.rating"
                required
              />
              <input type="submit" value="Rate Show" class="btn btn-success" />
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RateShowPage",
  data() {
    return {
      formData: {
        rating: "",
        show_name: "",
      },
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
    };
  },
  created() {
    this.populateForm();
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
        } else {
          console.error("Show data is missing or invalid");
        }
      } catch (error) {
        console.error("Error while populating form:", error);
      }
    },
    async submitBooking() {
      try {
        const bookingData = new FormData();
        bookingData.append("rating", this.formData.rating);
        if (this.userSession && this.userSession.token) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const id = this.$route.params.id;
          const response = await axios.put(
            `http://127.0.0.1:1234/vue/rate/${id}`,
            bookingData
          );
          console.log(response);
          alert("Thank you for rating the show!");
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
