<template lang="pug">
  a.content-link-preview.d-flex.rounded.border.mb-1.bg-white(:href="customLinkPreview.url" target="_blank")
    .preview-image
      img.rounded-left(:src="customLinkPreview.image")
    .details
      .title.text-truncate.font-weight-bold {{ customLinkPreview.title }}
      .description.text-truncate {{ customLinkPreview.description }}
      small.url.text-truncate {{ customLinkPreview.url }}
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: ['linkPreview'],
  computed:{
    customLinkPreview(){
      return this.linkPreview[0]
    }
  }
})
</script>

<style lang="sass" scoped>
.content-link-preview
  .preview-image, img
    width: 59px
    height: 59px
    object-fit: cover
  .details
    display: grid
    padding: 6px 10px
    .title
      margin-bottom: -5px
    .description
      font-size: 0.813rem
      margin-bottom: -2px
  &:hover
    color: inherit
</style>
