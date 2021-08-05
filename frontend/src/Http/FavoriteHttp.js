import Http from './Http';

export default {
  create(data) {
    return Http.post('posts/api/favorites', data);
  },

  paginate(nextPage = false) {
    if (nextPage) return Http.paginate(nextPage);
    return Http.get('posts/api/favorites/paginate');
  },

  delete(postId) {
    return Http.delete(`posts/api/favorites/${postId}`);
  }
};
