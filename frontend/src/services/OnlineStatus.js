import AuthToken from './AuthToken'

export default {
  listen: {
    setOffline () {
      window.onbeforeunload = function () {
        const url = `${process.env.VUE_APP_URL}/users/api/users/status`
        const body = JSON.stringify({
          is_online: false,
          authorization: `Token ${AuthToken.token()}`
        })
        navigator.sendBeacon(url, body)
      }
    }
  }
}
