import Http from './Http'

export default {
  create (commentId) {
    return Http.post(`posts/api/comments/${commentId}/votes`)
  },

  delete (commentId) {
    return Http.delete(`posts/api/comments/${commentId}/votes`)
  }
}
