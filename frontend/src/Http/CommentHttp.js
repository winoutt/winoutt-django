import Http from './Http'

export default {
  create (data) {
    return Http.post('posts/api/comments', data)
  },

  delete (id) {
    return Http.delete(`posts/api/comments/${id}`)
  },

  paginate (data, nextPage = null) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get(`posts/api/comments/${data.postId}/paginate`)
  }
}
