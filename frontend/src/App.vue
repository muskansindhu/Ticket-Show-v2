<template>
  <div>
    <nav class="navbar navbar-dark navbar-expand-md sticky-top bg-dark py-1">
      <div class="container">
        <div class="navbar-brand d-flex align-items-center">
          <strong>Ticket Show</strong>
        </div>
        <ul class="navbar-nav ms-auto">
          <li
            class="nav-item"
            v-if="userInSession && userSession.role === 'admin'"
          >
            <div
              class="nav-link active d-flex justify-content-between align-items-center"
            >
              <router-link class="nav-link active" to="/admin/dash">
                Dashboard
              </router-link>
              <div class="nav-link active">
                <li class="nav-item">
                  <input
                    class="form-control mr-sm-2"
                    input
                    v-model="searchTerm"
                    @keyup.enter="search"
                    placeholder="Search Shows"
                    required
                  />
                </li>
              </div>
              <div class="nav-link active" v-if="showGoBackButton">
                <button class="btn btn-secondary" @click="goBack">
                  Go Back
                </button>
              </div>
              <div class="nav-link active" @click="logout">
                <button class="btn btn-danger">Log out</button>
              </div>
            </div>
          </li>
          <li
            class="nav-item"
            v-else-if="userInSession && userSession.role === 'user'"
          >
            <div
              class="nav-link active d-flex justify-content-between align-items-center"
            >
              <router-link class="nav-link active" to="/user/dash">
                Dashboard
              </router-link>
              <router-link class="nav-link active" to="/user/booking">
                Bookings
              </router-link>
              <div class="nav-link active">
                <li class="nav-item">
                  <input
                    class="form-control mr-sm-2"
                    input
                    v-model="searchTerm"
                    @keyup.enter="search"
                    placeholder="Search Shows"
                    required
                  />
                </li>
              </div>
              <div class="nav-link active" v-if="showGoBackButton">
                <button class="btn btn-secondary" @click="goBack">
                  Go Back
                </button>
              </div>
              <div class="nav-link active" @click="logout">
                <button class="btn btn-danger">Log out</button>
              </div>
            </div>
          </li>
          <li class="nav-item" v-else>
            <div
              class="nav-link active d-flex justify-content-between align-items-center"
            >
              <router-link class="nav-link active" to="/"> Home </router-link>
              <router-link class="nav-link active" to="/login">
                <button class="btn btn-success">Log in</button>
              </router-link>
            </div>
          </li>
        </ul>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      user: null,
      searchTerm: "",
      searchResults: [],
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("userSession");
      this.userSession = null;
      this.$router.push({ name: "login" });
    },
    async search() {
      this.$router.push(`/search/${this.searchTerm}`);
    },
    goBack() {
      // Go back to the previous page in history
      this.$router.go(-1);
    },
  },
  computed: {
    userInSession() {
      return this.userSession !== null;
    },
    showGoBackButton() {
      const currentPath = this.$route.path;
      return (
        currentPath !== "/admin/dash" &&
        currentPath !== "/user/dash" &&
        ((this.userInSession && this.userSession.role === "admin") ||
          (this.userInSession && this.userSession.role === "user"))
      );
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 10px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
nav .navbar-brand {
  color: #42b983;
}
</style>
