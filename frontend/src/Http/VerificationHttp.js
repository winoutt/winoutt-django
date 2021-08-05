import Http from './Http'

export default {
  resend (data) {
    return Http.post('users/api/verification/resend', data)
  },

  verify (data) {
    return Http.post('verification/verify', data) // urls' purpose covered by django
  }
}
