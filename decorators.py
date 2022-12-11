def add_button_back(func):
    def wrapper(*args, **kwargs):
        all_args = [*args]
        back_button = (str('Back'), str('Back'))
        if len(all_args[0][0]) > 1:
            all_args.append(back_button)
            f = func(*all_args)
            return f
        else:
            return func(*args, **kwargs)
    return wrapper
