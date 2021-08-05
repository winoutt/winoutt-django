import Http from './Http'

export default {
  create (data) {
    return Http.post('posts/api/stars', data)
  },

  delete (data) {
    return Http.delete(`posts/api/stars/${data.postId}`)
  }
}
