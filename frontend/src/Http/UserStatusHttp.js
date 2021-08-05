import Http from './Http'

export default {
  update (isOnline) {
    const data = { is_online: isOnline }
    return Http.put('users/api/users/status', data)
  }
}
