<template>
  <div>
    <div class="container mt-5 pt-5 justify-content-center">
      <div class="row">
        <div class="col-md-6 mx-auto">
          <div class="card">
            <div class="card-body text-center">
              <h3>Edit Show</h3>
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
                <!--
                  <label for="poster">Choose a poster for your show:</label>
                  <input
                    type="file"
                    name="poster"
                    id="poster"
                    class="form-control my-4 py-2"
                    placeholder="Show Poster"
                    required
                  />
                  -->
                <button
                  type="button"
                  class="btn btn-outline-success"
                  @click="editShowForm"
                >
                  Edit
                </button>
                &nbsp;
                <button
                  type="button"
                  class="btn btn-outline-danger"
                  @click="deleteShow"
                >
                  Delete
                </button>
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
  name: "AdminEditShowPage",
  data() {
    return {
      formData: {
        show_name: null,
        price: null,
        tags: null,
        time: null,
        rating: null,
        show_id: null,
      },
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
    };
  },
  methods: {
    async editShowForm() {
      try {
        if (this.userSession && this.userSession.token) {
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const formData = new FormData();
          const show_id = this.$route.params.id;
          formData.append("show_name", this.formData.show_name);
          formData.append("time", this.formData.time);
          formData.append("tags", this.formData.tags);
          formData.append("price", this.formData.price);
          formData.append("rating", this.formData.rating);
          formData.append("show_id", show_id);
          console.log(formData);

          // Send the formData to the server for updating
          const response = await axios.put(
            "http://127.0.0.1:1234/vue/show",
            formData
          );

          // Update this.formData with the new values from the form fields
          this.formData.show_name = formData.get("show_name");
          this.formData.time = formData.get("time");
          this.formData.tags = formData.get("tags");
          this.formData.price = formData.get("price");
          this.formData.rating = formData.get("rating");

          alert(" Show was updated successfully.");
          console.log(response);
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
        alert("Oops! An error occurred. Show was not edited.");
      }
    },
    deleteShow() {
      try {
        if (this.userSession && this.userSession.token) {
          // Set the Authorization header with the JWT token
          axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${this.userSession.token}`;
          const show_id = this.$route.params.id;
          const response = axios.delete(
            `http://127.0.0.1:1234/vue/show/${show_id}`
          );
          console.log(response);
          alert("Show deleted Successfully");
          this.$router.push({ name: "admin-dash" });
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
        alert("Oops! An error occurred. Show was not deleted.");
      }
    },
  },
  created() {
    const id = this.$route.params.id;
    axios
      .get(`http://127.0.0.1:1234/vue/theater/show/${id}`)
      .then((response) => {
        const showData = response.data;
        this.formData.show_name = showData.show_name;
        this.formData.time = showData.time;
        this.formData.tags = showData.tags;
        this.formData.price = showData.price;
        this.formData.rating = showData.rating;
        this.formData.show_id = showData.show_id;
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
};
</script>
