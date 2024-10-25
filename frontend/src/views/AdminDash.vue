<template>
  <AdminDashPage @onSubmit="onSubmit"></AdminDashPage>
</template>

<script>
import AdminDashPage from "@/components/AdminDash.vue";

export default {
  name: "AdminDashView",
  components: { AdminDashPage },
};
</script>
