from flask import Flask, request, make_response, jsonify, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from urllib.parse import unquote
from fake_useragent import UserAgent

import requests
import time
from rembg import remove, new_session

from io import BytesIO
from PIL import Image

import os


app = Flask(__name__)

limiter = Limiter(key_func=get_remote_address, app=app, default_limits=[])

CORS(app)


@app.route("/")
@limiter.exempt
def hello():
    return "API is working!"


@app.route("/share/<cid>")
@limiter.exempt
def share(cid):
    return (
        '<html><head><meta name="twitter:card" content="summary_large_image" /><meta property="og:url" content="https://'
        + cid
        + '.ipfs.nftstorage.link" /><meta property="og:title" content="Kwentize yourself" /><meta property="og:description" content="Kwentize yourself with our tool." /><meta property="og:image" content="https://'
        + cid
        + '.ipfs.nftstorage.link" /></head><body>redirecting to image..</body><script>setTimeout(function(){ window.location.href = "https://'
        + cid
        + '.ipfs.nftstorage.link"; }, 200)</script></html>'
    )


@app.route("/remove", methods=["POST", "OPTIONS"])
@limiter.exempt
def remove_bg():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json_data = request.json
        now = str(time.time())
        url = json_data["url"]
        data = requests.get(url).content
        file_extension = url.split(".")[-1]  # Extract file extension from URL
        input_path = f"./origin/{now}.{file_extension}"

        # Save the downloaded image
        with open(input_path, "wb") as f:
            f.write(data)

        output_path = f"./static/{now}.png"  # Output always as PNG

        res = {}
        res["result"] = f"{now}.png"

        with open(input_path, "rb") as i:
            with open(output_path, "wb") as o:
                input_data = i.read()
                model_name = "u2net_human_seg"
                session = new_session(model_name)
                output = remove(input_data, session=session)
                o.write(output)

        # Delete the input file after processing
        os.remove(input_path)

        return jsonify(res)
    else:
        return "Content-Type not supported!"


@app.route("/remove-bg-2", methods=["POST", "OPTIONS"])
@limiter.limit(
    "4 per day",
    key_func=lambda: request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr),
)
def remove_bg2():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.json
        now = str(time.time())
        url = json["url"]
        data = requests.get(url).content
        f = open("./origin/" + now + ".jpg", "wb")
        f.write(data)
        f.close()
        res = {}
        res["result"] = now + ".png"

        input_path = "./origin/" + now + ".jpg"
        output_path = "./static/" + now + ".png"

        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": open(input_path, "rb")},
            data={"size": "auto"},
            headers={"X-Api-Key": "N7ofK6rsQTtk3oKPbpDM3dV3"},
        )
        if response.status_code == requests.codes.ok:
            with open(output_path, "wb") as out:
                out.write(response.content)
                return jsonify(res)
        else:
            print("Error:", response.status_code, response.text)
            return response.text
    else:
        return "Content-Type not supported!"
    
def overlay_images(foreground_image, background_path="assets/frame_img.png"):
    try:
        # Open the background image
        background = Image.open(background_path)

        # Open the foreground image from bytes
        foreground = Image.open(BytesIO(foreground_image))

        # Resize foreground image to fit background
        foreground.thumbnail((background.width // 2, background.height // 2))

        # Calculate position to place the foreground image at the center of background
        x = (background.width - foreground.width) // 2
        y = (background.height - foreground.height) // 2

        # Paste the foreground image onto the background
        background.paste(foreground, (x, y), foreground)

        # Save the result to a BytesIO object
        output = BytesIO()
        background.save(output, format='PNG')
        output.seek(0)

        return output.getvalue()

    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route("/overlay", methods=["POST"])
def overlay():
    try:
        # Check if the request contains a file named 'foreground'
        if 'foreground' not in request.files:
            return jsonify({"error": "Foreground image not provided"}), 400
        
        # Read the foreground image bytes from the request
        foreground_image = request.files['foreground'].read()

        # Call overlay_images function to overlay the images
        result_image_bytes = overlay_images(foreground_image)

        # Check if the overlaying was successful
        if result_image_bytes is None:
            return jsonify({"error": "Failed to overlay images"}), 500

        # Return the resulting image as a response
        return send_file(BytesIO(result_image_bytes), mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/remove_and_overlay", methods=["POST"])
def remove_and_overlay():
    try:
        address_encoded = request.args.get("custody_address")
        username_encoded = request.args.get("username")
        pfp_url_encoded = request.args.get("pfp_url")

        address = unquote(address_encoded)
        username = unquote(username_encoded)
        pfp_url = unquote(pfp_url_encoded)

        print("Address:", address)
        print("Username:", username)
        print("PFP URL:", pfp_url)

        if not (username and address):
            return jsonify({"error": "Username and address must be provided"}), 400

        now = str(time.time())
   
        file_extension = "png"
        input_path = f"./origin/{now}.{file_extension}"
        output_path = f"./static/{username}_{address}_{now}.png"  # Output always as PNG

        print("Input Path:", input_path)
        print("Output Path:", output_path)

        # try:
        #     response = requests.get(pfp_url)
        #     response.raise_for_status()  # Raise an error for bad status codes
        #     data = response.content
        # except requests.exceptions.RequestException as e:
        #     print("Error fetching image:", e)
        try:

            data = fetch_image(pfp_url)
        except Exception as e:
            print("Error fetching image:", e)

        print("Data Length:", len(data))

        try:
            background_image_filename = f"background_{now}.{file_extension}"
            background_image_path = os.path.join("static", background_image_filename)
            with open(background_image_path, "wb") as f:
                f.write(data)

            # Remove background from the provided image
            background_removed_image_bytes = remove_background_from_image(data)
        except Exception as e:
            print("Error saving image:", e)


        if background_removed_image_bytes is None:
            return jsonify({"error": "Failed to remove background from image"}), 500

        # Overlay the background removed image on top of a background
        result_image_bytes = overlay_images(background_removed_image_bytes)
        os.remove(background_image_path)

        with open(output_path, "wb") as f:
            f.write(result_image_bytes)

        if result_image_bytes is None:
            return jsonify({"error": "Failed to overlay images"}), 500

        # # Return the resulting image as a response
        # return send_file(BytesIO(result_image_bytes), mimetype='image/png')

        # Return the filename of the resulting image
        return jsonify({"filename": output_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def fetch_image(webpage_url):
    # Create a fake user agent
    user_agent = UserAgent().random

    # Set headers to simulate a web browser
    headers = {'User-Agent': user_agent}

    # Send a GET request to the URL with headers
    response = requests.get(webpage_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content of the response (the image) to a file
        print("Image downloaded successfully.")
        return response.content

    else:
        print("Failed to download the image. Status code:", response.status_code)




@app.route("/download_file", methods=["POST"])
def download_file():
    print("tried to download")
    try:
        # Get the username from the POST request data
        username_encoded = request.args.get("username")
        username = unquote(username_encoded)

        # Check if the username exists
        if username:
            # Get the static folder path
            static_folder_path = os.path.join(os.getcwd(), 'static')

            # Find files starting with the username
            matching_files = [file for file in os.listdir(static_folder_path) if file.startswith(username + '_')]

            # Sort the files by timestamp
            sorted_files = sorted(matching_files, key=lambda x: float(x.split('_')[-1].split('.')[0]), reverse=True)

            # Check if any files matched the criteria
            if sorted_files:
                # Get the latest file
                latest_file = sorted_files[0]

                # Get the full path of the file
                file_path = os.path.join(static_folder_path, latest_file)

                # Return the file for download
                return send_file(file_path, as_attachment=True)
            else:
                return jsonify({"error": f"No files found for username '{username}'"}), 404
        else:
            return jsonify({"error": "Username not provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def remove_background_from_image(foreground_image_bytes):
    try:
        # Prepare data for removing background
        now = str(time.time())
        input_path = "./origin/" + now + ".png"
        output_path = "./static/" + now + ".png"

        # Write the provided foreground image bytes to a file
        with open(input_path, "wb") as f:
            f.write(foreground_image_bytes)

        # Remove background from the image
        with open(input_path, "rb") as i:
            with open(output_path, "wb") as o:
                input_image_bytes = i.read()
                model_name = "u2net_human_seg"
                session = new_session(model_name)
                output_image_bytes = remove(input_image_bytes, session=session)
                o.write(output_image_bytes)
        
        # Delete the input file after processing
        os.remove(input_path)

        # Read the resulting image bytes
        with open(output_path, "rb") as f:
            result_image_bytes = f.read()

        os.remove(output_path)

        return result_image_bytes

    except Exception as e:
        print(f"Error: {e}")
        return None

def overlay_images(foreground_image_bytes, background_path="assets/frame_img.png"):
    try:
        # Open the background image
        background = Image.open(background_path)

        # Open the foreground image from bytes
        foreground = Image.open(BytesIO(foreground_image_bytes))

        # Resize foreground image to fit background
        foreground.thumbnail((background.width // 2, background.height // 2))

        # Calculate position to place the foreground image at the center of background
        x = (background.width - foreground.width) // 2
        y = (background.height - foreground.height) // 2

        # Paste the foreground image onto the background
        background.paste(foreground, (x, y), foreground)

        # Return the resulting image bytes
        with BytesIO() as output_buffer:
            background.save(output_buffer, format='PNG')
            return output_buffer.getvalue()

    except Exception as e:
        print(f"Error: {e}")
        return None
    