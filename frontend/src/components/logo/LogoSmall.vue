<template lang="pug">
  .logo
    router-link(:to="{ name: 'Landing' }")
      img(src=`${process.env.VUE_APP_BASE_URL}/assets/Logo.svg` alt="winoutt" :class="imgClass")
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: ['fullWidth'],
  computed: {
    imgClass () {
      return { 'full-width': this.fullWidth }
    }
  }
})
</script>

<style lang="sass" scoped>
img
  width: 123px
  height: auto
  &.full-width
    width: 100%
</style>
