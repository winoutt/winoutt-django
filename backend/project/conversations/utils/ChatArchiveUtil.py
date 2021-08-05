from project.conversations.models import ChatArchive


def create(user, chat):
    return ChatArchive.objects.create(user=user, chat=chat)


def is_exist(user, chat):
    return ChatArchive.objects.filter(user=user, chat=chat).exists()


def delete_archive_chat(user, chat):
    return ChatArchive.objects.get(user=user, chat=chat).delete()


def get_all_archived_chats(user):
    return ChatArchive.objects.filter(user=user)


def delete_archived_chats(chat):
    archived_chats = ChatArchive.objects.filter(chat=chat)
    for archived_chat in archived_chats:
        archived_chat.delete()