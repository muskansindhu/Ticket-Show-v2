<template>
  <div class="container mt-5 pt-5 justify-content-center">
    <div class="row">
      <div class="col-md-6 mx-auto">
        <div class="card">
          <div class="card-body">
            <h2>{{ register ? "Sign up" : "Log in" }}</h2>
            <form @submit.prevent="register ? registerOn() : login()">
              <div>
                <input
                  type="text"
                  name="username"
                  id="username"
                  class="form-control my-4 py-2"
                  placeholder="Username"
                  v-model="username"
                  required
                />
              </div>
              <div v-if="register">
                <input
                  type="text"
                  name="email"
                  id="email"
                  class="form-control my-4 py-2"
                  placeholder="Email"
                  v-model="email"
                  required
                />
              </div>
              <div>
                <input
                  type="password"
                  name="password"
                  id="password"
                  class="form-control my-4 py-2"
                  placeholder="Password"
                  minlength="4"
                  v-model="password"
                  required
                />
              </div>
              <div class="mb-3">
                <!-- Dropdown to select user or admin registration -->
                <select v-model="role" class="form-select">
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div class="mb-3">
                <button
                  class="btn btn-success d-block w-100"
                  type="submit"
                  :disabled="register && !isEmail(email)"
                >
                  {{ register ? "Register" : "Login" }}
                </button>
              </div>
              <p class="text-muted">
                {{ register ? "Have an account?" : "Not a member?" }}
                <a @click="state" href="#">
                  {{ register ? "Log in" : "Register" }}
                </a>
              </p>
            </form>
            <div class="card-text alert alert-danger" v-if="error">
              {{ msg }}
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
  name: "LoginView",
  data() {
    return {
      userSession: JSON.parse(localStorage.getItem("userSession")) || null,
      register: false,
      username: "",
      email: "",
      password: "",
      role: "user",
      token: "",
      exp: "",
      msg: "",
      error: false,
    };
  },
  methods: {
    isEmail(str) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(str);
    },
    click() {
      if (this.role === "admin") {
        this.$router.push("/admin/dash");
        this.$router.go();
      } else {
        this.$router.push("/user/dash");
        this.$router.go();
      }
    },
    state() {
      this.error = false;
      this.register = !this.register;
    },
    async registerOn() {
      if (
        this.isEmail(this.email) &&
        this.username.trim() &&
        this.password.length > 3
      ) {
        try {
          const formData = new FormData();
          formData.append("username", this.username);
          formData.append("email", this.email);
          formData.append("password", this.password);

          const response = await axios.post(
            `http://127.0.0.1:1234/vue/${this.role}`,
            formData
          );

          if ("error" in response.data) {
            throw new Error(response.data.error_msg);
          }

          this.token = response.data.token;
          this.exp = response.data.exp;

          this.userSession = {
            token: this.token,
            exp: this.exp,
            role: this.role,
          };

          localStorage.setItem("userSession", JSON.stringify(this.userSession));
          this.click();
        } catch (error) {
          this.error = true;
          this.msg = error.message;
        }
      } else {
        this.msg = "Fields not filled properly";
        this.error = true;
      }
    },
    async login() {
      try {
        let loginEndpoint = "";

        if (this.role === "user") {
          loginEndpoint = "http://127.0.0.1:1234/vue/user/login";
        } else if (this.role === "admin") {
          loginEndpoint = "http://127.0.0.1:1234/vue/admin/login";
        }

        if (!loginEndpoint) {
          throw new Error("Invalid role selected");
        }

        const response = await axios.post(loginEndpoint, {
          username: this.username,
          password: this.password,
        });

        if ("error" in response.data) {
          throw new Error(response.data.error_msg);
        }
        this.token = response.data.token;
        this.exp = response.data.exp;

        this.userSession = {
          token: this.token,
          exp: this.exp,
          role: this.role,
        };

        localStorage.setItem("userSession", JSON.stringify(this.userSession));

        if (this.role === "admin") {
          this.redirectToAdminDash();
        } else {
          this.redirectToUserDash();
        }
        //window.location.reload();
        this.$router.go();
      } catch (error) {
        this.error = true;
        this.errorMsg = error.message;
      }
    },
    redirectToAdminDash() {
      this.$router.push("/admin/dash");
    },

    redirectToUserDash() {
      this.$router.push("/user/dash");
    },
  },
  mounted() {
    document.title = this.register ? "Register" : "Login";
  },
};
</script>
