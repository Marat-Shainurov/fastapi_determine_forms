# General description
fastapi_determine_forms is a fastapi project created for storing form templates and getting the most suitable one 
by passing the request form with field_name-field_value pairs. \

Main stack and tools: FastAPI, MongoDB, Pydantic, pytest.

# Install and usage
1. Clone the project https://github.com/Marat-Shainurov/fastapi_determine_forms.

2. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

3. Read the project's documentation (swagger or redoc):
   - http://localhost:8000/docs/
   - http://localhost:8000/redoc/

4. Go to the main page on your browser http://localhost:8000/docs and start working with the app's endpoints.
   - /get_form
   - /create_form_template
   - /get_form_templates_list
   - /retrieve_form_template/{form_name}
   - /put_form_template/{form_name}
   - /delete_form_template/{form_name}

# Testing
1. All the tests are run during the docker startup process (run_tests.sh). \
   Run tests manually:
   - docker-compose exec app pytest -vv
