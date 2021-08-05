import Http from './Http'

export default {
  archive (id) {
    return Http.delete(`conversations/api/chats/${id}/archive`)
  },

  unarchive (id) {
    return Http.post(`conversations/api/chats/${id}/unarchive`)
  },

  paginate (nextPage = null) {
    const baseUrl = 'conversations/api/chats/paginate'
    const url = nextPage || baseUrl
    return Http.get(url)
  },

  archived (nextPage = null) {
    const baseUrl = 'conversations/api/chats/archived'
    const url = nextPage ? `${baseUrl}/${nextPage}` : baseUrl
    return Http.get(url)
  },

  search (params) {
    return Http.get('conversations/api/chats/search', params)
  },

  read (id) {
    return Http.post(`conversations/api/chats/${id}/read`)
  },

  markDelivered () {
    return Http.post('conversations/api/chats/mark/delivered')
  },

  readFromUserId (id) {
    return Http.get(`conversations/api/chats/user/${id}`)
  }
}
