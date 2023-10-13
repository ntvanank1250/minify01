from fastapi import FastAPI, HTTPException,Query
from fastapi.responses import FileResponse
import requests
import configparser
from cssmin import cssmin
from jsmin import jsmin
from PIL import Image
from io import BytesIO
import uvicorn
from utils import *
import sys

config = configparser.ConfigParser()
config.read('info.ini')
my_path = config.get('local', 'path')
server = config.get('server', 'url') + ":" + config.get('server', 'port')

app = FastAPI()

@app.get("/minify_css")
async def minify_css(css_uri: str):
    css_request_uri = server + css_uri
    file_path = my_path + css_uri

    response = requests.get(css_request_uri)
    css = response.text
    minified_css = cssmin(css)
    with open(file_path, "w+") as file:
        file.write(minified_css)
    return FileResponse(file_path, media_type="text/css")

@app.get("/minify_js")
async def minify_js(js_uri: str):
    js_request_uri = server + js_uri
    file_path = my_path + js_uri

    response = requests.get(js_request_uri)
    js = response.text
    minified_js = jsmin(js)
    with open(file_path, "w+") as file:
        file.write(minified_js)
    return FileResponse(file_path, media_type="application/javascript")

@app.get("/minify_img")
async def minify_img(input_image_uri: str):
    input_image__request_uri = server + input_image_uri
    list_img = input_image_uri.split(".")
    list_img[-1] = "webp"
    output_image = '.'.join(list_img)
    output_image_path =my_path + output_image
    response = requests.get(input_image__request_uri)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(output_image_path, "WebP", quality=80)
        print("Hình ảnh đã được lưu dưới dạng WebP với chất lượng 70 thành công.")
        return FileResponse(output_image_path, media_type="image/webp") 
    else:
        print("Không thể tải xuống hình ảnh. Mã trạng thái:", response.status_code)

@app.get("/minify/")
async def minify_img(param: str = Query(...)):
    print(param)
    response = requests.get(param)
    content = response.text
    size_before = sys.getsizeof(content)
    name_file = param.split('/')[-1]
    print("Dung lượng truoc minify:", size_before, "bytes")

    if is_css(param):
        print("CSS")
        minified = cssmin(content)
        # file_path = "/home/hieudd/Code/minify01/static/css/" +name_file
        file_path = "/home/hieudd/minify/static/css/" +name_file

        write_file(file_path=file_path,minified=minified)
        return FileResponse(file_path, media_type="text/css")
    elif is_js(param):
        print("JS")
        minified = jsmin(content)
        # file_path = "/home/hieudd/Code/minify01/static/js/" +name_file
        file_path = "/home/hieudd/minify/static/js/" +name_file

        write_file(file_path=file_path,minified=minified)
        return FileResponse(file_path, media_type="application/javascript")
    elif is_image(param):
        print("IMAGE")
        # file_path = "/home/hieudd/Code/minify01/static/images/" +name_file
        file_path = "/home/hieudd/minify/static/images/" +name_file

        image = Image.open(BytesIO(response.content))
        image.save(file_path, "WebP", quality=80)
        print("Hình ảnh đã được lưu dưới dạng WebP với chất lượng 70 thành công.")
        return FileResponse(file_path, media_type="image/webp") 

def write_file(file_path,minified):
    with open(file_path, "w+") as file:
        file.write(minified)
    size_after = sys.getsizeof(minified)
    print("Dung lượng sau minify:", size_after, "bytes")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
