import Http from './Http'

export default {
  suggestions (postId) {
    return Http.get('posts/api/comments/mentions/suggestions', { post: postId })
  },

  searchSuggestions (postId, term) {
    const params = { post: postId, term }
    return Http.get('posts/api/comments/mentions/suggestions/search', params)
  }
}
