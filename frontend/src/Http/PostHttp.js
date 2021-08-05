import Http from './Http'

export default {
  create (data) {
    return Http.post('posts/api/posts', data)
  },

  delete (id) {
    return Http.delete(`posts/api/posts/${id}`)
  },

  read (id) {
    return Http.get(`posts/api/posts/${id}`)
  },

  top () {
    return Http.get('posts/api/posts/top')
  }
}
