<template lang="pug">
.favorites
  HeadingSmall.my-3 Favorites
  .posts.mb-3.mb-sm-0(v-if="!Util.isEmpty(posts)")
    Post(v-for="post in posts" :post="post" :key="post.post_id")
  NoResults.no-results(
    v-else
    text="No favorites yet!"
    subtext="From here, you can access your favorite posts."
  )
  PostModals
</template>

<script lang="ts">
import Vue from 'vue';
import PeopleRequest from '../Request/PeopleRequest';
import HashtagRequest from '../Request/HashtagRequest';
import FavoriteRequest from '../Request/FavoriteRequest';
import PostState from '../State/PostState';
import Request from '../Request/Request';
import PostScroll from '../Scroll/PostScroll';

import HeadingSmall from '../components/heading/HeadingSmall.vue';
import Post from '../components/post/Post.vue';
import NoResults from '../components/NoResults.vue';
import PostModals from '../components/post/PostModals.vue';

export default Vue.extend({
  components: {
    HeadingSmall,
    Post,
    NoResults,
    PostModals
  },

  async beforeRouteEnter(to, from, next) {
    const requests = [
      FavoriteRequest.paginate(),
      PeopleRequest.mayknow(),
      HashtagRequest.trending()
    ];
    const { isFailed } = await Request.bulk(requests);
    if (!isFailed) next();
  },

  computed: {
    posts() {
      return PostState.collectPosts();
    }
  },

  beforeDestroy() {
    PostScroll.favorite.paginate.leave();
  },

  mounted() {
    PostScroll.favorite.paginate.listen();
  }
});
</script>
