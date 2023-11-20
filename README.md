# General description
fastapi_determine_forms is a fastapi project created for storing form templates and getting the most suitable one, 
by passing the request form with field_name-field_value pairs. \
Main stack and tools: FastAPI, MongoDB, Pydantic, pytest.

# Install and usage
1. Clone the project https://github.com/Marat-Shainurov/fastapi_determine_forms in your IDE.

2. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

3. Read the project's documentation (swagger):
   - http://127.0.0.1:8000/docs/

4. Go to the main page on your browser http://127.0.0.1:8000/docs and start working with the app's endpoints.
