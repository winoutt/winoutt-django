import Http from './Http'

export default {
  update (data) {
    return Http.put('users/api/settings', data)
  }
}
