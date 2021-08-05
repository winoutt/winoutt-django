import Http from './Http'

export default {
  create (data) {
    return Http.post('users/api/unfollows', data)
  },

  delete (connectionId) {
    return Http.delete(`users/api/unfollows/${connectionId}`)
  }
}
