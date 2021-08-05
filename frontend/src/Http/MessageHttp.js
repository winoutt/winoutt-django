import Http from './Http'

export default {
  read (messageId) {
    return Http.get(`conversations/api/messages/${messageId}`)
  },

  create (data) {
    return Http.post('conversations/api/messages', data)
  },

  paginate (chatId, nextPage = false) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get(`conversations/api/messages/${chatId}/paginate`)
  },

  unreadsCount () {
    return Http.get('conversations/api/messages/unreads/count')
  }
}
