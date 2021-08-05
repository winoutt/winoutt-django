import {
  forEach,
  findIndex,
  find,
  compact,
  size,
  uniqBy,
  isMatch
} from 'lodash';

/**
 * Initial bootstrap comments.
 * Posts not includes comments property by default.
 * Here is the fix for posts to bind comments intials structure.
 * @param {Object} post
 * @returns {undefined}
 */
function bootstrapComments(post) {
  post.comments = { data: [], nextPage: '' };
}

function findAll(state, post_id) {
  const posts = find(state.posts, { post_id });
  const post = isMatch(state.post, { post_id }) ? state.post : null;
  return compact([posts, post]);
}

function findAllAndUpdate(state, id, updates) {
  const updatables = findAll(state, id);
  forEach(updatables, (post) => {
    forEach(updates, (value, key) => {
      post[key] = value;
    });
  });
}

export default {
  namespaced: true,
  state: {
    posts: [],
    starredModal: {},
    post: {
      comments: {
        data: [],
        nextPage: ''
      }
    },
    nextPage: '',
    hasNew: false,
    articleEditor: {
      cover: '',
      title: '',
      content: '',
      quillEditor: null
    }
  },

  mutations: {
    addPost(state, post) {
      const exists = find(state.posts, { post_id: post.post_id });
      if (exists) return;
      bootstrapComments(post);
      state.posts.unshift(post);
    },
    addComment(state, comment) {
      const { post_id: post_id } = comment;
      const posts = find(state.posts, { post_id });
      const post = isMatch(state.post, { post_id }) ? state.post : null;
      const addables = compact([posts, post]);
      forEach(addables, (post) => {
        const existingCommentIndex = findIndex(post.comments.data, {
          id: comment.id
        });
        if (existingCommentIndex === -1) {
          post.comments.data.unshift(comment);
          post.comments_count++;
        }
      });
    },
    replacePosts(state, posts) {
      state.posts = [];
      this.commit('posts/pushPosts', posts);
    },
    replacePost(state, post) {
      bootstrapComments(post);
      state.post = post;
    },
    replaceNextPage(state, nextPage) {
      state.nextPage = nextPage;
    },
    replaceHasNew(state, hasNew) {
      state.hasNew = hasNew;
    },
    replaceStarredModal(state, post) {
      state.starredModal = post;
    },
    pushPosts(state, posts) {
      forEach(posts, (post) => {
        bootstrapComments(post);
        state.posts.push(post);
      });
    },
    pushComments(state, payload) {
      const { id, comments } = payload;
      const posts = find(state.posts, { post_id: id });
      const post = isMatch(state.post, { post_id: id }) ? state.post : null;
      const pushables = compact([posts, post]);
      forEach(pushables, (post) => {
        forEach(comments, (comment) => post.comments.data.push(comment));
      });
    },
    amendPost(state, post) {
      const { post_id } = post;
      bootstrapComments(post);
      const index = findIndex(state.posts, { post_id });
      state.posts.splice(index, 1, post);
      if (isMatch(state.post, { post_id })) state.post = post;
    },
    pullPost(state, post_id) {
      const posts = find(state.posts, { post_id });
      if (posts) {
        const index = findIndex(state.posts, { post_id });
        state.posts.splice(index, 1);
      }
      if (isMatch(state.post, { post_id })) {
        state.post = {};
        bootstrapComments(state.post);
      }
    },
    pullComment(state, comment_id) {
      function pull(post) {
        const index = findIndex(post.comments.data, { comment_id });
        post.comments.data.splice(index, 1);
        post.comments_count--;
      }
      const posts = find(state.posts, (post) => {
        return size(post) && find(post.comments.data, { comment_id });
      });
      const post = find(state.post.comments.data, { comment_id }) ? state.post : null;
      const pullables = compact([posts, post]);
      forEach(pullables, (post) => pull(post));
    },
    markFavorited(state, id) {
      findAllAndUpdate(state, id, { is_favorited: true });
    },
    removeFavorited(state, id) {
      findAllAndUpdate(state, id, { is_favorited: false });
    },
    addStar(state, id) {
      const updatables = findAll(state, id);
      forEach(updatables, (post) => {
        post.stars_count++;
        post.is_starred = true;
      });
    },
    pullStar(state, id) {
      const updatables = findAll(state, id);
      forEach(updatables, (post) => {
        post.stars_count--;
        post.is_starred = false;
      });
    },
    markPollVoted(state, data) {
      const { poll_id: pollId, choice_id: choiceId } = data;
      const posts = find(state.posts, (post) => {
        return post.poll && post.poll.id === pollId;
      });
      function post() {
        const isPost = state.post.poll && state.post.poll.id === pollId;
        return isPost ? state.post : null;
      }
      const markables = compact([posts, post()]);
      forEach(markables, (post) => {
        post.poll.is_voted = true;
        const choice = find(post.poll.choices, { id: choiceId });
        if (choice) choice.is_voted = true;
      });
    },
    replaceCommentNextPage(state, payload) {
      const { id, nextPage } = payload;
      const post = find(state.posts, { id });
      if (post) post.comments.nextPage = nextPage;
    },
    replaceComments(state, payload) {
      const { id, comments } = payload;
      const posts = find(state.posts, { post_id: id });
      const post = isMatch(state.post, { post_id: id }) ? state.post : null;
      const replaceables = compact([posts, post]);
      forEach(replaceables, (post) => {
        post.comments.data = comments;
      });
    },
    upvoteComment(state, comment) {
      const { comment_id: commentId, post_id: postId } = comment;
      const posts = find(state.posts, { post_id: postId });
      const post = isMatch(state.post, { post_id: postId }) ? state.post : null;
      const updatables = uniqBy(compact([posts, post]), 'id');
      forEach(updatables, (post) => {
        const { data: comments } = post.comments;
        const comment = find(comments, { comment_id: commentId });
        if (comment) {
          comment.is_voted = true;
          comment.votes_count++;
        }
      });
    },
    unvoteComment(state, comment) {
      const { comment_id: commentId, post_id: postId } = comment;
      const posts = find(state.posts, { post_id: postId });
      const post = isMatch(state.post, { post_id: postId }) ? state.post : null;
      const updatables = uniqBy(compact([posts, post]), 'id');
      forEach(updatables, (post) => {
        const { data: comments } = post.comments;
        const comment = find(comments, { comment_id: commentId });
        if (comment) {
          comment.is_voted = false;
          comment.votes_count--;
        }
      });
    },
    replaceArticleEditorCover(state, cover) {
      state.articleEditor.cover = cover;
    },
    replaceArticleEditorTitle(state, title) {
      state.articleEditor.title = title;
    },
    replaceArticleEditorContent(state, content) {
      state.articleEditor.content = content;
    },
    replaceArticleEditorQuillEditor(state, editor) {
      state.articleEditor.quillEditor = editor;
    },
    clearArticleEditor(state) {
      state.articleEditor.cover = '';
      state.articleEditor.title = '';
      state.articleEditor.content = '';
    }
  },

  getters: {
    posts: (state) => state.posts,
    post: (state) => state.post,
    starredModal: (state) => state.starredModal,
    hasNew: (state) => state.hasNew,
    nextPage: (state) => state.nextPage,
    articleEditorCover: (state) => state.articleEditor.cover,
    articleEditorTitle: (state) => state.articleEditor.title,
    articleEditorContent: (state) => state.articleEditor.content,
    articleEditorQuillEditor: (state) => state.articleEditor.quillEditor,
    collectCommentNextPage(state) {
      return (id) => {
        const post = find(state.posts, { id });
        return post ? post.comments.nextPage : null;
      };
    },
    collectComments(state) {
      return (post_id) => {
        const posts = find(state.posts, { post_id });
        const post = isMatch(state.post, { post_id }) ? state.post : null;
        const collatable = post || posts;
        if (collatable) return collatable.comments.data;
      };
    }
  }
};
