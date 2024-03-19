# Warpcast Frame Kwentize API

This Flask application provides endpoints for various image processing tasks such as removing backgrounds, overlaying images, and generating social media sharing metadata.

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AsparAugustus/kwentize-frame
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Flask application:**
    ```bash
    python3 app.py
    ```

## Endpoints

### 1. `/remove`

This endpoint accepts a JSON payload containing the URL of an image, downloads the image, removes its background, and returns the processed image.

- **Method:** POST
- **Payload:**
    ```json
    {
        "url": "https://example.com/image.jpg"
    }
    ```


### 3. `/overlay`

This endpoint overlays a provided foreground image on a background image.

- **Method:** POST
- **Payload:** Form-data with `foreground` file

### 4. `/remove_and_overlay`

This endpoint combines background removal and image overlaying functionalities. It accepts parameters such as username, address, and profile picture URL, removes the background from the profile picture, overlays it on a background, and returns the resulting image.

- **Method:** POST
- **Payload:**
    ```json
    {
        "custody_address": "123 Main St",
        "username": "user123",
        "pfp_url": "https://example.com/profile_pic.jpg"
    }
    ```

### 5. `/remove_and_overlay_test`

Similar to `/remove_and_overlay`, but this endpoint is for testing purposes.

- **Method:** POST
- **Payload:**
    ```json
    {
        "custody_address": "123 Main St",
        "username": "user123",
        "pfp_url": "https://example.com/profile_pic.jpg"
    }
    ```

## Additional Notes

- CORS headers are enabled to allow cross-origin requests.
- Rate limiting is applied to certain endpoints to prevent abuse.
- The code also includes functions for writing logs and serving static files.

Feel free to explore and modify the code as needed.