<template>
  <div>
    <div v-for="(value, key) in showSaleData" :key="key">
      <p>{{ key }}: {{ value }}</p>
    </div>
    <div v-if="graphFilePath">
      <img :src="graphFilePath + '?v=' + new Date().getTime()" alt="Graph" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminSummaryView",
  data() {
    return {
      admin: null,
      showSaleData: {},
      graphFilePath: null,
    };
  },
  mounted() {
    if (this.userSession && this.userSession.token) {
      // Set the Authorization header with the JWT token
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${this.userSession.token}`;

      axios
        .get("http://127.0.0.1:1234/vue/summary")
        .then((response) => {
          this.admin = response.data.admin;
          this.showSaleData = response.data.showSaleData;
          this.graphFilePath = response.data.graphFilePath;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      // Handle the case where the user is not authenticated
      console.error("User is not authenticated.");
      // You can redirect to the login page or show an error message here
    }
  },
};
</script>
