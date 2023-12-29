

def theme(request) -> dict:
    # Set the default mode to light
    theme: str = 'light'

    # Get the mode from the session if it exists
    if 'theme' in request.session:
        theme = request.session['theme']

    # Return the mode in the context dictionary
    return {'theme': theme}
