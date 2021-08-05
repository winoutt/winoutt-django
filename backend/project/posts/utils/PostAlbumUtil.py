from project.posts.models import PostAlbum

def create(post, photos):
    for photo in photos:
        PostAlbum.objects.create(post=post, photo=photo, photo_original=photo)


def get_post_album(post):
    return PostAlbum.objects.filter(post=post)