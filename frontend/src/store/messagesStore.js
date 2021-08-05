import { forEach, filter, isEmpty, compact, find } from 'lodash'

export default {
  namespaced: true,
  state: {
    messages: [],
    unreadsCount: 0,
    nextPage: ''
  },

  mutations: {
    addMessage (state, message) {
      const chat = this.getters['chats/chat']
      const updateUnreads = () => {
        const activeChats = this.getters['chats/active']
        const archivedChats = this.getters['chats/archived']
        const query = chat => chat.chat_id === message.chat_id
        const activeChat = find(activeChats, chat => query(chat))
        const archivedChat = find(archivedChats, chat => query(chat))
        const chats = compact([activeChat, archivedChat])
        forEach(chats, chat => {
          return this.commit('chats/increaseUnreadsCount', chat.pivot.id)
        })
        this.commit('messages/addUnreadsCount', 1)
      }
      if (isEmpty(chat)) return updateUnreads()
      const isChat = message.chat_id === chat.chat_id
      if (isChat) {
        state.messages.push(message)
      } else updateUnreads()
      this.commit('chats/moveActiveTop', message.chat_id)
    },
    replaceMessages (state, messages) {
      state.messages = []
      this.commit('messages/pushMessages', messages)
    },
    replaceNextPage (state, nextPage) {
      state.nextPage = nextPage
    },
    pushMessages (state, messages) {
      forEach(messages, message => {
        state.messages.unshift(message)
      })
    },
    readMessages (state, chatId) {
      const messages = filter(state.messages, message => {
        const isChat = message.chat_id === chatId
        const isReceived = message.is_sent === false
        const isRead = message.status === 'read'
        return (isChat && isReceived && !isRead)
      })
      forEach(messages, message => {
        message.status = 'read'
      })
    },
    deliveredMessage (state, message_id) {
      const message = find(state.messages, { message_id })
      if (!message) return
      message.status = 'delivered'
    },
    readMessage (state, message_id) {
      const message = find(state.messages, { message_id })
      if (!message) return
      message.status = 'read'
    },
    replaceUnreadsCount (state, count) {
      state.unreadsCount = count
    },
    pullUnreadsCount (state, count) {
      const decreased = state.unreadsCount - count
      this.commit('messages/replaceUnreadsCount', decreased)
    },
    addUnreadsCount (state, count) {
      const increased = state.unreadsCount + count
      this.commit('messages/replaceUnreadsCount', increased)
    },
    pullMessages (state) {
      state.messages = []
    }
  },

  getters: {
    messages: state => state.messages,
    unreadsCount: state => state.unreadsCount,
    nextPage: state => state.nextPage
  }
}
