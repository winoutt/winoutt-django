<template lang="pug">
  .post-footer
    .actions.d-flex.justify-content-between
      .d-flex
        .star.d-flex.align-items-end.mr-3(
          @click="star()"
          :class="starClass"
        )
          Icon.icon-star-active(name="star-active" v-if="post.is_starred")
          Icon.icon-star(name="star" v-else)
          span.count.cursor-pointer(
            v-if="post.is_user && post.stars_count"
            @click="openStarredModal()"
            data-toggle="tooltip"
            data-placement="top"
            title="Only you can see the total number of stars on your post."
          ) {{ Humanize.count(post.stars_count) }}
        .comment.d-flex.align-items-end.mr-3.cursor-pointer(@click="toggleComments()")
          Icon.icon-chat.cursor-pointer(name="chat")
          span.count(v-if="post.comments_count") {{ Humanize.count(post.comments_count) }}
        .share
          Icon.icon-share.cursor-pointer(name="share" @click.native="share()")
      .favorite(:class="favoriteClass" @click="toggleFavorite()")
        Icon.icon-bookmark.cursor-pointer(v-if="post.is_favorited" name="bookmark-active")
        Icon.icon-bookmark.cursor-pointer(v-else name="bookmark")
    .post-coments
      .new-comment.position-relative.mt-4(v-if="hasAuth")
        Textarea.comment-box(
          :autosize="true"
          placeholder="Add a comment or use @ to reply someone."
          rows="1"
          @input="suggestUsers()"
          class="mb-1"
          padding="8px 14px"
          :preventEnter="true"
          v-model="comment"
          :ref="`comment-${post.post_id}`"
          @enter="createComment()"
          @escape="clearMentionBox()"
          @focusOut="clearMentionBox()"
        )
        CommentMentionbox(:users="suggestedUsers" @choose="addMention")
      .comments-wrapper.mt-4(v-if="comments.length")
        h6.font-weight-bold.comments-heading Comments
        .comments-list.scroll.pr-1(:id="`comments-${post.post_id}-wrapper`")
          div(:id="`comments-${post.post_id}`")
            Comment(
              v-for="comment in comments"
              :key="comment.comment_id"
              :comment="comment"
            )
</template>

<script lang="ts">
import Vue from 'vue';
import { isEmpty, debounce } from 'lodash';
import v from 'voca';

import PostModalService from '../../services/ModalServices/PostModalService';
import PostState from '../../State/PostState';
import CommentRequest from '../../Request/CommentRequest';
import StarRequest from '../../Request/StarRequest';
import PostStarRequest from '../../Request/PostStarRequest';
import Mention from '../../services/Mention';
import UserState from '../../State/UserState';
import CommentScroll from '../../Scroll/CommentScroll';
import CommentMentionRequest from '../../Request/CommentMentionRequest';
import AuthToken from '../../services/AuthToken';
import Tooltip from '../../services/Tooltip';
import Autosize from '../../services/Autosize';
import FavoriteRequest from '../../Request/FavoriteRequest';

import Icon from '../Icon.vue';
import Textarea from '../Textarea.vue';
import CommentMentionbox from '../comment/CommentMentionbox.vue';
import Comment from '../comment/Comment.vue';

export default Vue.extend({
  props: ['post'],
  components: {
    Icon,
    Textarea,
    CommentMentionbox,
    Comment
  },

  data() {
    return {
      comment: '',
      reference: `comment-mention-${this.post.post_id}`
    };
  },

  computed: {
    hasAuth() {
      return AuthToken.has();
    },
    comments() {
      return PostState.collectComments(this.post.post_id);
    },
    suggestedUsers() {
      const commentMentions = UserState.collectCommentMentions();
      const isPostCommentMentions =
        commentMentions.post_id === this.post.post_id;
      return isPostCommentMentions ? commentMentions.data : [];
    },
    starClass() {
      return {
        'text-primary': this.post.is_starred,
        'cursor-pointer': !this.post.is_user
      };
    },
    favoriteClass() {
      return {
        active: this.post.is_favorited
      };
    }
  },

  methods: {
    share() {
      PostState.replacePost(this.post);
      PostModalService.share().open();
    },
    suggestUsers: debounce(async function () {
      const isMention = Mention.isLastWordIsMention(this.comment);
      if (!isMention)
        return UserState.replaceCommentMentions(this.post.post_id, []);
      const term = Mention.getTerm(this.comment);
      isEmpty(term)
        ? await CommentMentionRequest.suggestions(this.post.post_id)
        : await CommentMentionRequest.searchSuggestions(
            this.post.post_id,
            term
          );
    }, 300),
    async toggleComments() {
      if (this.comments.length) {
        PostState.replaceComments(this.post.post_id, []);
        CommentScroll.paginate.leave(this.post.post_id);
      } else {
        const comments = await CommentRequest.paginate({
          postId: this.post.post_id
        });
        if (isEmpty(comments)) return;
        CommentScroll.paginate.listen(this.post.post_id);
      }
    },
    star() {
      if (this.post.is_user) return;
      if (this.post.is_starred)
        StarRequest.delete({ postId: this.post.post_id });
      else StarRequest.create({ postId: this.post.post_id });
    },
    addMention(user) {
      const lastMention = Mention.lastMention(this.comment);
      if (lastMention === '@') {
        this.comment = v.reverse(
          v.replace(
            v.reverse(this.comment),
            '@',
            v.reverse(`@${user.username} `)
          )
        );
      } else
        this.comment = v.replace(
          this.comment,
          lastMention,
          `@${user.username} `
        );
      UserState.replaceCommentMentions(this.post.post_id, []);
      this.$refs[`comment-${this.post.post_id}`].$el.children[0].focus();
    },
    async createComment() {
      const content = v.trim(this.comment);
      await CommentRequest.create({ post: this.post.post_id, content });
      this.comment = '';
      this.$nextTick(() => Autosize.reset());
    },
    clearMentionBox() {
      setTimeout(() => {
        UserState.replaceCommentMentions(this.post.post_id, []);
      }, 300);
    },
    async openStarredModal() {
      await PostStarRequest.paginate(this.post.post_id);
      PostState.replaceStarredModal(this.post);
      PostModalService.starred().open();
    },
    toggleFavorite() {
      if (this.post.is_favorited) {
        FavoriteRequest.delete(this.post.post_id);
        const isFavoritePage = this.$route.name === 'Favorites';
        if (isFavoritePage) PostState.pullPost(this.post.post_id);
      } else {
        FavoriteRequest.create({ postId: this.post.post_id });
      }
    }
  },

  mounted() {
    Tooltip.boot();
  }
});
</script>

<style lang="sass" scoped>
@import '../../assets/sass/variables'

.post-footer
  .actions
    .icon-star, .icon-star-active
      width: 21px
      height: 21px
    .icon-chat
      width: 18px
      height: 18px
    .icon-share
      width: 22px
      height: 16px
    .count
      line-height: 1
      font-size: 0.813rem
      margin-left: 6px
    .favorite
      .icon-bookmark
        width: 14px
        height: 20px
      &.active .icon-bookmark
        fill: $primary
  .post-coments
    .comment-box
      min-height: 38px
    .comments-wrapper
      .comments-heading
        font-size: 0.9375rem
        margin-bottom: 9px
      .comments-list
        max-height: 256px
    .view-more
      font-size: 0.75rem
</style>
