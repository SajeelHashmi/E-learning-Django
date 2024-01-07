# Ilm Ghar
Important to use the hls stream you must at this point manually run the ffmpeg command after uploading a lecture
navigate to the media folder 
go to lecture videos and run the command
 ffmpeg -i fileName.mp4 -c:v h264 -c:a aac -hls_time 10 -hls_list_size 0 lectureName_lectureId/output.m3u8

## Prerequisites

- [Python](https://www.python.org/) (3.x recommended)
- [Node.js](https://nodejs.org/) (for frontend development)
- [npm](https://www.npmjs.com/) (Node.js package manager)

## Backend Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/SajeelHashmi/E-learning-Django
    ```

2. Navigate to the project folder:

    ```bash
    cd your-repository
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations:

    ```bash
    python manage.py migrate
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

   The backend should now be running at [http://localhost:8000/](http://localhost:8000/).

## Frontend Setup

1. Navigate to the frontend folder:

    ```bash
    cd frontend
    ```

2. Initialize npm (if not already done):

    ```bash
    npm init
    ```

    Follow the prompts to create a `package.json` file.

3. Install frontend dependencies:

    ```bash
    npm install
    ```

4. Run the development server:

    ```bash
    npm start
    ```

   The frontend development server should now be running at [http://localhost:3000/](http://localhost:3000/).


