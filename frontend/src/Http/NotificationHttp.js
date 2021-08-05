import Http from './Http'

export default {
  paginate (nextPage = null) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get('notifications/api/notifications/paginate')
  },

  read (notificationId) {
    return Http.get(`notifications/api/notifications/${notificationId}`)
  },

  markRead (id) {
    return Http.put(`notifications/api/notifications/${id}/read`)
  },

  markAllRead () {
    return Http.post('notifications/api/notifications/read/all')
  },

  unreadsCount () {
    return Http.get('notifications/api/notifications/unreads/count')
  },

  connectionRequest: {
    list () {
      return Http.get('notifications/api/notifications/connection-requests')
    }
  }
}
