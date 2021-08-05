import { isEmpty } from 'lodash'
import Socket from './Socket'
import UserState from '../State/UserState'
import MessageState from '../State/MessageState'
import MessageRequest from '../Request/MessageRequest'
import MessageScroll from '../Scroll/MessageScroll'
import ChatState from '../State/ChatState'
import ChatRequest from '../Request/ChatRequest'

function channel () {
  const user = UserState.collectUser()
  return `private-user.${user.id}`
}

const tracker = {
  created: false,
  delivered: false,
  read: false
}

export default {
  listen: {
    created: () => {
      if (Socket.isListening(tracker, 'created')) return
      Socket.safeBoot()
      Socket.pusher.subscribe(channel()).bind('message.created',  async data => {
        await setTimeout(async ()=>{
          const { message_id: messageId } = data
          const message = await MessageRequest.read(messageId)
          if (isEmpty(message)) return
          MessageState.addMessage(message)
          ChatState.replaceLastMessage(message)
          ChatState.moveToActive(message.chat_id)
          MessageScroll.toBottom()
          const activeChat = ChatState.collectChat()
          const isActive = activeChat.pivot &&
            (activeChat.chat_id === message.chat_id)
          if (isActive) ChatRequest.read(message.chat_id)
          else ChatRequest.markDelivered()
        },1000);
        })
    },
    delivered: () => {
      if (Socket.isListening(tracker, 'delivered')) return
      Socket.safeBoot()
      Socket.pusher.subscribe(channel()).bind('message.delivered', data => {
          const { message_id: messageId } = data
          MessageState.deliveredMessage(messageId)
        })
    },
    read: () => {
      if (Socket.isListening(tracker, 'read')) return
      Socket.safeBoot()
      Socket.pusher.subscribe(channel()).bind('message.read', data => {
          const { message_id: messageId } = data
          MessageState.readMessage(messageId)
        })
    }
  },

  leave () {
    if (Socket.pusher) {
      tracker.created = false
      tracker.delivered = false
      tracker.read = false
      Socket.pusher.unsubscribe(channel())
    }
  }
}
