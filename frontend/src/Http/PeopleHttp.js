import Http from './Http'

export default {
  mayknow () {
    return Http.get('users/api/people/mayknow')
  },

  paginate (nextPage) {
    const baseUrl = 'users/api/people/paginate'
    const url = nextPage ? `${baseUrl}/${nextPage}` : baseUrl
    return Http.get(url)
  },

  search (params) {
    return Http.get('urls/api/people/search', params)
  }
}
