import Socket from './Socket'
import TeamState from '../State/TeamState'
import UserState from '../State/UserState'
import PostState from '../State/PostState'
import PostRequest from '../Request/PostRequest'

function channel () {
  const team = TeamState.collectTeam()
  return `private-team.${team.id}`
}

const tracker = {
  created: false
}

export default {
  listen: {
    created () {
      if (Socket.isListening(tracker, 'created')) return
      Socket.safeBoot()
      Socket.pusher.subscribe(channel()).bind('post.created', async data => {
          const { post_id: postId } = data
          const post = await PostRequest.read(postId, false)
          const user = UserState.collectUser()
          const isUserPost = post.user_id === user.id
          if (isUserPost) return
          PostState.addPost(post)
          PostState.replaceHasNew(true)
        })
    }
  },
  leave () {
    if (Socket.pusher) {
      tracker.created = false
      Socket.pusher.unsubscribe(channel())
    }
  }
}
