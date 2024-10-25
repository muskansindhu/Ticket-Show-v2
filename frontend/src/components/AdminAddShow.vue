<template>
  <div>
    <div class="container mt-5 pt-5 justify-content-center">
      <div class="row">
        <div class="col-md-6 mx-auto">
          <div class="card">
            <div class="card-body text-center">
              <h3>Add Show</h3>
              <form>
                <input
                  type="text"
                  name="show_name"
                  id="show_name"
                  class="form-control my-4 py-2"
                  placeholder="Show Name"
                  v-model="formData.show_name"
                  required
                />
                <input type="hidden" name="venue_id" />
                <input
                  type="number"
                  min="0"
                  max="5"
                  name="rating"
                  id="rating"
                  class="form-control my-4 py-2"
                  placeholder="Ratings"
                  v-model="formData.rating"
                  required
                />
                <input
                  type="text"
                  name="tags"
                  id="tags"
                  class="form-control my-4 py-2"
                  placeholder="Tags"
                  v-model="formData.tags"
                  required
                />
                <input
                  type="text"
                  name="time"
                  id="time"
                  class="form-control my-4 py-2"
                  placeholder="Time"
                  v-model="formData.time"
                  required
                />
                <input
                  type="number"
                  min="0"
                  name="price"
                  id="price"
                  class="form-control my-4 py-2"
                  placeholder="Price"
                  v-model="formData.price"
                  required
                />

                <label for="poster">Choose a poster for your show:</label>
                <input
                  type="file"
                  name="poster"
                  id="poster"
                  class="form-control my-4 py-2"
                  placeholder="Show Poster"
                  @change="handleFileUpload"
                  required
                />

                <input
                  type="submit"
                  value="Submit"
                  class="btn btn-success"
                  @click="addShowForm"
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
  name: "AdminAddShowPage",
  data() {
    return {
      formData: {
        show_name: "",
        price: "",
        tags: "",
        time: "",
        rating: "",
        theater_id: "",
        poster: null,
      },
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
    };
  },
  methods: {
    async addShowForm() {
      try {
        if (this.userSession && this.userSession.token) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const theater_id = this.$route.params.id;
          const formData = new FormData();
          formData.append("show_name", this.formData.show_name);
          formData.append("time", this.formData.time);
          formData.append("tags", this.formData.tags);
          formData.append("price", this.formData.price);
          formData.append("rating", this.formData.rating);
          formData.append("poster", this.formData.poster);
          formData.append("theater_id", theater_id);
          console.log(formData);
          const response = await axios.post(
            "http://127.0.0.1:1234/vue/show",
            formData
          );
          console.log(response);
          alert(" Show was added successfully.");
        } else {
          console.error("User is not authenticated.");
        }
      } catch (error) {
        console.error("AxiosError:", error);

        if (error.response) {
          console.error("Response Data:", error.response.data);
        } else {
          console.error("Network Error:", error.message);
        }
        alert("Oops! An error occurred. Show was not added.");
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0]; // Get the first selected file
      this.formData.poster = file; // Assign the file to 'formData.poster'
    },
  },
};
</script>
