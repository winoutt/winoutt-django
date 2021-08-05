import Http from './Http'

export default {
  update () {
    return Http.put('users/api/sessions')
  }
}
