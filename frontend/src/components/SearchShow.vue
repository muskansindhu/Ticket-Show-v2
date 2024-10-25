<template>
  <div class="row g-0">
    <div class="col-md-6 order-first order-md-last" style="min-height: 250px">
      <div class="text-white p-4 p-md-5">
        <h2 class="fw-bold text-white mb-3">{{ show.show_name }}</h2>
        <p class="mb-2">Time: {{ show.time }}</p>
        <p class="mb-2">Price: {{ show.price }}</p>
        <p class="mb-2">Tags: {{ show.tags }}</p>
        <p class="mb-2">Seats Booked: {{ show.seats_booked }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchShowPage",
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
};
</script>
