import Http from './Http'

export default {
  all (params) {
    return Http.get('users/api/search/all', params)
  }
}
