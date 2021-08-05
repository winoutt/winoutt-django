import Http from './Http'

export default {
  create (data) {
    return Http.post('users/api/connections', data)
  },

  accept (id) {
    return Http.post(`users/api/connections/${id}/accept`)
  },

  ignore (id) {
    return Http.post(`users/api/connections/${id}/ignore`)
  },

  mutuals (id, nextPage = null) {
    const baseUrl = `users/api/connections/${id}/mutuals?page=1`
    const url = nextPage || baseUrl
    return Http.get(url)
  },

  list (id, nextPage = null) {
    const baseUrl = `users/api/connections/${id}?page=1`
    const url = nextPage || baseUrl
    return Http.get(url)
  },

  disconnect (id) {
    return Http.post(`users/api/connections/${id}/disconnect`)
  },

  cancel (id) {
    return Http.post(`users/api/connections/${id}/cancel`)
  }
}
