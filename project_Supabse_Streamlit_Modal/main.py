def create_message_generator():
    yield "hi"
    yield "there"
    yield "friend"

gen = create_message_generator()

print(next(gen))