<template>
  <div>
    <br />
    <br />
    <div class="col-md-12 text-center">
      <button type="button" class="btn btn-success" v-b-modal.theater-modal>
        Add Theater
      </button>
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

            <div class="buttons">
              <a
                :href="'/admin/' + theater.roll + '/add-show'"
                class="btn btn-outline-success btn-sm"
              >
                Add Show
              </a>
              &nbsp;
              <a
                :href="'/theater/' + theater.roll + '/analytics'"
                class="btn btn-outline-warning btn-sm"
              >
                Analytics
              </a>
              &nbsp;
              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="deleteTheater(theater.roll)"
              >
                Delete Theater
              </button>
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
                      <a
                        :href="'/admin/' + show.roll + '/edit-show'"
                        class="btn btn-info btn-sm"
                      >
                        Actions
                      </a>
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

    <!-- Add Theater Model -->
    <b-modal
      ref="theaterModal"
      id="theater-modal"
      title="Add a Theater"
      hide-backdrop
      hide-footer
    >
      <b-form class="w-100">
        <b-form-group id="theater_name" label-for="theater_name_input">
          <b-form-input
            id="theater_name_input"
            type="text"
            v-model="formData.theater_name"
            placeholder="Enter Theater Name"
            required
          >
          </b-form-input>
          <br />
        </b-form-group>
        <b-form-group id="location" label-for="location_input">
          <b-form-input
            id="location_input"
            type="text"
            v-model="formData.location"
            placeholder="Enter Theater Location"
            required
          >
          </b-form-input>
        </b-form-group>
        <br />
        <b-form-group id="capacity" label-for="capacity_input">
          <b-form-input
            id="capacity_input"
            type="number"
            v-model="formData.capacity"
            placeholder="Enter Theater Capacity"
            required
          >
          </b-form-input>
        </b-form-group>
        <br />
        <div class="text-center">
          <b-button type="submit" variant="success" @click="onSubmit"
            >Submit</b-button
          >
        </div>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminDashPage",
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

    async addTheaterForm() {
      try {
        if (this.userSession && this.userSession.token) {
          // Set the Authorization header with the JWT token
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const formData = new FormData();
          formData.append("theater_name", this.formData.theater_name);
          formData.append("location", this.formData.location);
          formData.append("capacity", this.formData.capacity);

          const response = await axios.post(
            "http://127.0.0.1:1234/vue/theater",
            formData
          );
          console.log("User Token:", this.userSession.token);
          console.log(response);
          this.getTheater();
        } else {
          // Handle the case where the user is not authenticated
          console.error("User is not authenticated.");
          // You can redirect to the login page or show an error message here
        }
      } catch (error) {
        console.error("AxiosError:", error);
        console.log(this.userSession.token);

        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred. Theater was not added.");
      }
    },
    deleteTheater(theater_id) {
      try {
        if (this.userSession && this.userSession.token) {
          // Set the Authorization header with the JWT token
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const response = axios.delete(
            `http://127.0.0.1:1234/vue/theater/${theater_id}`
          );
          console.log(response);
          alert("Theater deleted Successfully");
          this.getTheater();
        } else {
          // Handle the case where the user is not authenticated
          console.error("User is not authenticated.");
          // You can redirect to the login page or show an error message here
        }
      } catch (error) {
        console.error("AxiosError:", error);
        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred. Theater was not deleted.");
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
    await this.loadShowsForTheaters();
    const fetchData = async () => {
      try {
        await this.getTheater();
        await this.loadShowsForTheaters();
      } catch (error) {
        console.error("Error fetching theaters:", error);
      }
    };
    fetchData();

    setInterval(fetchData, 60000);
  },
};
</script>
