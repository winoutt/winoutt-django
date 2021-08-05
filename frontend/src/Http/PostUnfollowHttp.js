import Http from './Http'

export default {
  create (postId) {
    return Http.post(`posts/api/posts/${postId}/unfollows`)
  },

  delete (postId) {
    return Http.delete(`posts/api/posts/${postId}/unfollows`)
  }
}
