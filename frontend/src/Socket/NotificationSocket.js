import { isEmpty } from 'lodash'
import Socket from './Socket'
import UserState from '../State/UserState'
import NotificationState from '../State/NotificationState'
import NotificationRequest from '../Request/NotificationRequest'
import Page from '../services/Page'

function channel () {
  const user = UserState.collectUser()
  return `private-user.${user.id}`
}

const tracker = {
  created: false
}

export default {
  listen: {
    created: () => {
      if (Socket.isListening(tracker, 'created')) return
      Socket.safeBoot()

      Socket.pusher.subscribe(channel()).bind('notification.created',  async data => {
        await setTimeout(async ()=>{
          const { notification_id: notificationId } = data
          const notification = await NotificationRequest.read(notificationId)
          if (isEmpty(notification)) return
          const isConnectionRequest = notification.notification_type === 'connection_request'
          if (isConnectionRequest) {
            NotificationState.addConnectionRequest(notification)
          } else {
            NotificationState.addNotification(notification)
          }
          NotificationState.incrementUnreadsCount()
        },1000)
      });
    }
  },

  leave () {
    if (Socket.pusher) {
      tracker.created = false
      Socket.pusher.unsubscribe(channel())
    }
  }
}
