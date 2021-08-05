import Http from './Http'

export default {
  list () {
    return Http.get('users/api/notes')
  },

  archived () {
    return Http.get('users/api/notes/archived')
  },

  create (data) {
    return Http.post('users/api/notes', data)
  },

  edit (id, data) {
    return Http.put(`users/api/notes/${id}`, data)
  },

  archive (id) {
    return Http.delete(`users/api/notes/${id}/archive`)
  },

  unarchive (id) {
    return Http.post(`users/api/notes/${id}/unarchive`)
  },

  delete (id) {
    return Http.delete(`users/api/notes/${id}`)
  },

  deleteBlanks () {
    return Http.delete('users/api/notes/blanks')
  }
}
