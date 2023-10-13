import re
def check_type(param:str):
    list_param = param.split(".")
    if list_param[-1] == "css":
        return "css"
    elif list_param[-1] == "js":
        return "js"
    else:
        return False

def check_extension(url, extensions):
    pattern = r'\.({})$'.format('|'.join(extensions))
    match = re.search(pattern, url, re.IGNORECASE)
    return bool(match)

def is_js(url):
    extensions = ['js']
    return check_extension(url, extensions)

def is_css(url):
    extensions = ['css']
    return check_extension(url, extensions)

def is_image(url):
    extensions = ['jpg', 'jpeg', 'png', 'gif']
    return check_extension(url, extensions)
 