import Http from './Http'

export default {
  login (data) {
    return Http.post('users/api/auth/login', data)
  },

  logout () {
    return Http.post('users/api/auth/logout')
  },

  register (data) {
    return Http.post('users/api/auth/register', data)
  },

  user () {
    return Http.get('users/api/auth/user')
  }
}
