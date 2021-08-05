import Http from './Http'

export default {
  create (data) {
    return Http.post('posts/api/poll/votes', data)
  }
}
