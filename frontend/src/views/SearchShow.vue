<template>
  <div class="container" style="padding-top: 44px">
    <div
      class="bg-dark border rounded border-0 border-dark overflow-hidden"
      style="padding-bottom: 0px; margin-bottom: 64px"
    >
      <div class="p-md-3" v-if="this.boolShows">
        <p class="fw-bold text-white mb-2">
          Shows found for the search term are as follows:
        </p>
      </div>
      <div v-if="this.boolShows">
        <div v-for="show in this.compShows" :key="show.roll">
          <SearchShowPage :show="show"></SearchShowPage>
        </div>
      </div>
      <div class="p-md-3" v-if="!this.boolShows">
        <p class="fw-bold text-white mb-3">
          No shows found for the search term
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import SearchShowPage from "@/components/SearchShow.vue";
import axios from "axios";

export default {
  name: "SearchShowView",
  components: { SearchShowPage },
  props: {
    term: String,
  },
  data() {
    return {
      shows: [],
    };
  },
  created() {
    this.fetchSearchResults(this.term);
  },
  methods: {
    async fetchSearchResults(term) {
      const response = await axios.get(
        `http://127.0.0.1:1234/vue/searchShows/${term}`
      );
      this.shows = response.data.shows;
    },
    async beforeMount() {
      await this.fetchShowData(); // Call the fetchShowData method
    },
  },
  computed: {
    boolShows() {
      if (this.shows) {
        return this.shows.length > 0;
      }
      return false;
    },
    compShows() {
      return this.shows;
    },
  },
};
</script>
