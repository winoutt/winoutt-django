// import Echo from 'laravel-echo'
import Pusher from 'pusher-js'
import { isEmpty } from 'lodash'
import AuthToken from '../services/AuthToken'
import Cookies from 'js-cookie'


export default {
  pusher: {},

  boot () {
    this.pusher = new Pusher(process.env.VUE_APP_PUSHER_APP_KEY, {
      cluster: process.env.VUE_APP_PUSHER_APP_CLUSTER,
      authEndpoint: process.env.VUE_APP_URL + '/custom_services/pusher/auth',
      auth: {
        headers: {
          Authorization: `Token ${AuthToken.token()}`
        },
        params: {
          csrfmiddlewaretoken: Cookies.get('csrftoken'),
        }
      }
    });
  },

  isListening(tracker, event) {
    const isListening = tracker[event]
    if (!isListening) tracker[event] = true
    return isListening
  },

  safeBoot () {
    if (isEmpty(this.pusher)) this.boot()
  }
}
