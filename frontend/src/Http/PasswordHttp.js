import Http from './Http'

export default {
  reset (data) {
    return Http.post('passwords/reset', data) // api url not implemented
  },

  update (data) {
    return Http.patch('passwords/update', data) // api url not implemented
  },

  change (data) {
    return Http.put('users/api/passwords', data)
  }
}
