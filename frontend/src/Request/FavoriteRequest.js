import { isEmpty } from 'lodash';
import FavoriteHttp from '../Http/FavoriteHttp';
import PostState from '../State/PostState';
import Alert from '../services/Alert';
import AuthToken from '../services/AuthToken';
import IntendedRedirect from '../services/IntendedRedirect';

const FavoriteRequest = {
  async create(data) {
    if (!AuthToken.has()) return IntendedRedirect.post(data.postId);
    const { isFavorited } = await FavoriteHttp.create(data);
    if (!isFavorited) return;
    PostState.markFavorited(data.postId);
    Alert.action.success('Added to Favorites', 'Undo', function () {
      FavoriteRequest.delete(data.postId);
    });
  },

  async paginate(nextPage = false) {
    if (nextPage === null) return;
    const posts = await FavoriteHttp.paginate(nextPage);
    if (isEmpty(posts)) return;
    if (nextPage) PostState.pushPosts(posts.results);
    else PostState.replacePosts(posts.results);
    PostState.replaceNextPage(posts.next);
    return posts;
  },

  async delete(postId) {
    const { isDeleted } = await FavoriteHttp.delete(postId);
    if (!isDeleted) return;
    PostState.removeFavorited(postId);
    Alert.action.success('Removed from Favorites', 'Undo', function () {
      FavoriteRequest.create({ postId });
    });
  }
};

export default FavoriteRequest;
