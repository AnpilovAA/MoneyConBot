def add_button_back(func):
    def wrapper(*args, **kwargs):
        all_args = [*args]

        back_button = (str('Back'), str('Back'))

        if len(all_args[0][0]) > 1:

            all_args.append(back_button)
            create_inline_buttons = func(*all_args)

            return create_inline_buttons
        else:
            return func(*args, **kwargs)

    return wrapper
