from project.users.models import Note


def get_notes(user):
    return Note.objects.filter(user=user).order_by('-note_id')


def get_archived_notes(user):
    return Note.raw_objects.filter(user=user, deleted_at__isnull=False).order_by('-note_id')


def get_note_or_exception(note_id, user):
    note = Note.objects.filter(user=user, note_id=note_id)
    if note.exists():
        return note.first()
    raise Exception("Unable to update the note.")


def get_archived_note_or_exception(note_id, user):
    note = Note.raw_objects.filter(user=user, note_id=note_id, deleted_at__isnull=False)
    if note.exists():
        return note.first()
    raise Exception("Unable to unarchived the note.")



def force_delete_note(note_id, user):
    note = Note.objects.filter(user=user, note_id=note_id)
    if not note.exists():
        note = Note.raw_objects.filter(user=user, note_id=note_id, deleted_at__isnull=False)
        if not note.exists():
            raise Exception("Note not found.")
    note.first().hard_delete()
       

def force_delete_blank_note(user):
    notes = Note.raw_objects.filter(user=user, content__isnull=True)
    if not notes.exists():
        raise Exception("Blank Notes not found.")
    for note in notes:
        note.hard_delete()