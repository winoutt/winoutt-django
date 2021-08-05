import Http from './Http'

export default {
  list () {
    return Http.get('teams/api/teams')
  },

  top () {
    return Http.get('teams/api/teams/top')
  },

  read (slug) {
    return Http.get(`teams/api/teams/${slug}`)
  },

  contributors (id) {
    return Http.get(`teams/api/teams/${id}/contributors`)
  },

  posts (id, nextPage = null) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get(`teams/api/teams/${id}/posts`)
  }
}
