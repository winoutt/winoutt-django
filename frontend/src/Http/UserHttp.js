import Http from './Http'

export default {
  read (username) {
    return Http.get(`users/api/users/${username}`)
  },

  edit (data) {
    return Http.put('users/api/users', data)
  },

  delete (data) {
    return Http.post('users/api/users', data)
  },

  posts (username, nextPage = null) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get(`users/api/users/${username}/posts`)
  }
}
