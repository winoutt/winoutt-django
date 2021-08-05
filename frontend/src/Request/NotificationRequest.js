import { isEmpty } from 'lodash'
import NotificationHttp from '../Http/NotificationHttp'
import NotificationState from '../State/NotificationState'

export default {
  async paginate (nextPage = false) {
    if (nextPage === null) return
    const notifications = await NotificationHttp.paginate(nextPage)
    if (isEmpty(notifications)) return
    if (nextPage) NotificationState.pushNotifications(notifications.results)
    else NotificationState.replaceNotifications(notifications.results)
    NotificationState.replaceNextPage(notifications.next)
    return notifications
  },

  async markRead (notification) {
    const { isRead } = await NotificationHttp.markRead(notification.notification_id)
    if (!isRead) return
    NotificationState.markRead(notification.notification_id)
    NotificationState.decrementUnreadsCount()
  },

  async markAllRead () {
    const { isRead } = await NotificationHttp.markAllRead()
    if (!isRead) return
    NotificationState.markAllRead()
    NotificationState.pullUnreadsCount()
  },

  async read (notificationId) {
    const notification = await NotificationHttp.read(notificationId)
    return notification
  },

  async unreadsCount () {
    const response = await NotificationHttp.unreadsCount()
    const { unreads_count: unreadsCount } = response
    if (unreadsCount) NotificationState.replaceUnreadsCount(unreadsCount)
    else NotificationState.replaceUnreadsCount(0)
  },

  connectionRequests: {
    async list () {
      const notifications = await NotificationHttp.connectionRequest.list()
      if (isEmpty(notifications)) {
        return NotificationState.replaceConnectionRequests([])
      }
      NotificationState.replaceConnectionRequests(notifications)
    }
  }
}
