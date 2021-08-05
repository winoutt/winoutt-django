import Http from './Http'

export default {
  trending () {
    return Http.get('posts/api/hashtags/trending')
  },

  posts (hashtag, nextPage = false) {
    if (nextPage) return Http.paginate(nextPage)
    return Http.get(`posts/api/hashtags/${hashtag}/posts`)
  }
}
