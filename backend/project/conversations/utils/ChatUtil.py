from project.conversations.models import Chat, Message
from project.users.models import User
from django.db.models import Max, Q
from project.conversations.utils import ChatArchiveUtil
from project.custom_services.PusherEvents import broad_cast_message

def user_has_chat(user, user_connection):
    chat = Chat.objects.filter(user=user, user_connection=user_connection)
    if chat.exists():
        return True
    chat = Chat.objects.filter(user_connection=user, user=user_connection)
    if chat.exists():
        return True
    return False


def initialize_chat(user, user_connection):
    if user_has_chat(user, user_connection):
        return
    Chat.objects.create(user=user, user_connection=user_connection)


def is_chat_exist(user, chat_id):
    if Chat.objects.filter(user=user, chat_id=chat_id).exists() or Chat.objects.filter(user_connection=user, chat_id=chat_id).exists():
        return True
    return False


def get_chat_or_exception(chat_id):
    return Chat.objects.get(pk=chat_id)


def get_send_chats(user):
    return Chat.objects.filter(user=user)


def get_received_chats(user):
    return Chat.objects.filter(user_connection=user)


def get_all_chats(user):
    send_chats = get_send_chats(user)
    received_chats = get_received_chats(user)
    return send_chats | received_chats


def sort_chats_by_last_message_created_at(chats):
    chats = chats.filter(chats__isnull=False)
    return chats.annotate(last_message_created_at=Max('chats__created_at')).order_by('-last_message_created_at')


def archive_chat(user, chat_id):
    if not is_chat_exist(user, chat_id):
        raise Exception("Chat not found")
    if ChatArchiveUtil.is_exist(user, chat_id):
        raise Exception("Already archived")
    ChatArchiveUtil.create(user, get_chat_or_exception(chat_id))


def unarchive_chat(user, chat_id):
    if not is_chat_exist(user, chat_id):
        raise Exception("Chat not found")
    if not ChatArchiveUtil.is_exist(user, chat_id):
        raise Exception("Already unarchived")
    ChatArchiveUtil.delete_archive_chat(user, chat_id)


def paginate(user):
    archived_chats_ids = ChatArchiveUtil.get_all_archived_chats(user).values_list('chat', flat=True)
    chats = get_all_chats(user).exclude(chat_id__in=archived_chats_ids)
    chats = sort_chats_by_last_message_created_at(chats)
    return chats


def get_archived_chats(user):
    archived_chats_ids = ChatArchiveUtil.get_all_archived_chats(user).values_list('chat', flat=True)
    chats = get_all_chats(user).filter(chat_id__in=archived_chats_ids)
    chats = sort_chats_by_last_message_created_at(chats)
    return chats


def fuzzy_search_chat(send_chats, recevive_chats, term):
    filtered_send_chats = Chat.objects.none()
    filtered_recevive_chats = Chat.objects.none()
    filtered_send_chats = send_chats.filter(Q(user_connection__first_name__trigram_similar=term) | Q(user_connection__last_name__trigram_similar=term) | Q(message__content__trigram_similar=term))
    filtered_recevive_chats = recevive_chats.filter(Q(user__first_name__trigram_similar=term) | Q(user__last_name__trigram_similar=term) | Q(message__content__trigram_similar=term))

    chats = filtered_send_chats.union(filtered_recevive_chats)
    return chats.values_list("chat_id", flat=True)


def simple_contain_chat_search(send_chats, recevive_chats, term):
    filtered_send_chats = Chat.objects.none()
    filtered_recevive_chats = Chat.objects.none()
    filtered_send_chats = send_chats.filter(Q(user_connection__first_name__icontains=term) | Q(user_connection__last_name__icontains=term) | Q(message__content__icontains=term))
    filtered_recevive_chats = recevive_chats.filter(Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term) | Q(message__content__icontains=term))

    chats = filtered_send_chats.union(filtered_recevive_chats)
    return chats.values_list("chat_id", flat=True)


def search_chat(user, term):
    archived_chats_ids = ChatArchiveUtil.get_all_archived_chats(user).values_list('chat', flat=True)

    send_chats = get_send_chats(user).exclude(chat_id__in=archived_chats_ids)
    recevive_chats = get_received_chats(user).exclude(chat_id__in=archived_chats_ids)
  

    if term is None:
        chats = send_chats | recevive_chats
        chats = sort_chats_by_last_message_created_at(chats)
        return chats

    fuzzy_chats = fuzzy_search_chat(send_chats, recevive_chats, term)
    simple_chats = simple_contain_chat_search(send_chats, recevive_chats, term)
    chats = list(fuzzy_chats) + list(simple_chats)
    chats = Chat.objects.filter(chat_id__in=chats)
    chats = sort_chats_by_last_message_created_at(chats)
    return chats


def read_chat_messages(user, chat_id):
    chat = get_chat_or_exception(chat_id)
    if chat.user != user and chat.user_connection != user:
        raise Exception("You can't read this chat")
    unread_messages = chat.message_set.filter(status__in=['sent', 'delivered']).exclude(user=user)
    update_messages_status(unread_messages, "read")


def update_messages_status(unread_messages, status):
    for message in unread_messages:
        message.status = status
        message.save()
        broad_cast_message(message.user.id, status, {"message_id": message.message_id})


def mark_messages_status_as_delivered(user):
    chats = get_all_chats(user).values_list('chat_id', flat=True)
    messages = Message.objects.filter(chat__in=chats, status="sent").exclude(user=user)
    update_messages_status(messages, "delivered")


def get_chat_from_user(user_id, user_connection_id):
    send_chat = Chat.objects.filter(user=user_id, user_connection=user_connection_id)
    receive_chat = Chat.objects.filter(user_connection=user_id, user=user_connection_id)
    chat = None
    if send_chat.exists():
        chat = send_chat.first()
    elif receive_chat.exists():
        chat = receive_chat.first()
    if chat is None:
        raise Exception("Chat not found.")
    return chat