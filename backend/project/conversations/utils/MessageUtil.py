from project.conversations.models import Message

from project.conversations.utils import ChatUtil, ChatArchiveUtil

def get_message_type():
    pass

def get_message_or_exception(message_id):
    message = Message.objects.filter(message_id=message_id)
    if message.exists():
        return message.first()
    raise Exception("Message not found.")

# Read Message Helper Functions

def has_user_access_to_message(user, message):
    if message.chat.user == user or message.chat.user_connection == user:
        return True
    return False

def read_message(user, message_id):
    message = get_message_or_exception(message_id)
    if not has_user_access_to_message(user, message):
        raise Exception("You don't have permission to access this message.")
    return message

# Paginate Messages Helper Functions

def paginate(user, chat_id):
    if not ChatUtil.is_chat_exist(user, chat_id):
        raise Exception("Chat not found")
    return Message.objects.filter(chat=chat_id).order_by('-message_id')

# Unreads Message Count Helper Functions

def get_unreads_message_count(chats, user):
    archived_chats_ids = ChatArchiveUtil.get_all_archived_chats(user).values_list('chat', flat=True)
    unreads_message_count = Message.objects.filter(chat__in=chats, status__in=['delivered', 'sent']).exclude(user=user, chat__in=archived_chats_ids).count()
    return unreads_message_count

def get_unreads_message_count_from_user(user):
    chats = ChatUtil.get_all_chats(user).values_list('chat_id', flat=True)
    unreads_message_count = get_unreads_message_count(chats, user)
    return unreads_message_count


def get_message_receiver(message):
    return message.chat.user_connection if message.chat.user == message.user else message.chat.user
