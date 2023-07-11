import poe

client = None


def set_token(token):
    global client
    if client:
        del client
        client = None
    client = poe.Client(token)


def clear_context(current_bot_code):
    client.send_chat_break(current_bot_code)


def get_reply_stream(current_bot_code, prompt):
    prev_text = ""
    for chunk in client.send_message(current_bot_code, prompt):
        prev_text += chunk["text_new"]
        yield False, prev_text
    yield True, prev_text


def purge_conversation(current_bot_code, count=1):
    client.purge_conversation(current_bot_code, count)
