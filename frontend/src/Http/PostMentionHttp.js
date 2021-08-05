import Http from './Http'

export default {
  suggestions () {
    return Http.get('posts/api/posts/mentions/suggestions')
  },

  searchSuggestions (term) {
    return Http.get('posts/api/posts/mentions/suggestions/search', { term })
  }
}
