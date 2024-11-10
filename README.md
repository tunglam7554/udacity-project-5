# Casting Agency Project

## Project Motivation
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process

The Casting Agency has three main roles:
- Casting Assistant - Has the ability to view actors and movies.
- Casting Director - All permissions a Casting Director should have. Also adds the ability to approve or reject an actor request.
- Executive Producer - Has all permissions a Casting Director should have. Also adds the ability to add or delete an actor from the database.

## Installing Dependencies
1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```pip install -r requirements.txt ```

4. **Set up database** - With Postgres running, restore a database using follow commands:
    ```
    createdb capstone
    psql capstone < capstone.psql
    ```

5. **Configuring database path** - In order to run the application, you will need to set the following environment variables:
    ```
    export DATABASE_URL=postgresql://localhost:5432/capstone
    export FLASK_APP=app.py
    export FLASK_ENV=development
    ```
    Or you can config in config.py file.
6. **Auth0** - In order to use the Auth0 service, you will need to create an account and configure the application. Follow the [instructions](https://auth0.com/docs/quickstart
    Then set the envirement variables:
    ```
    export AUTH0_DOMAIN=dev-cpow2e2hthall7yb.us.auth0.com
    export API_AUDIENCE=capstone
    export ALGORITHMS=RS256
    ```
    Or you can config in config.py file.
6. **Run the application** - With all the environment variables set, you can run the application using the following command:
    ```
    flask run
    ```
## Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```
      

The API will return the following error types:
- 400 - Bad Request
- 404 - Resource Not Found
- 405 - Method Not Allowed

## Endpoints:
1.  `GET /movies` - Returns a list of movies.
    - Require permission: `get:movies`
    - Example: `curl http://127.0.0.1:5000/movies`
    - Output:
        ```json
        {
            "movies": [
                {
                "actors": [
                    {
                    "age": 43,
                    "gender": "Male",
                    "id": 1,
                    "name": "Chris Evans"
                    }
                ],
                "id": 1,
                "release_date": "Mon, 11 Nov 2024 00:00:00 GMT",
                "title": "Avenger Endgame"
                }
            ],
            "success": true
        }
        ```

2. `POST /movies` - Creates a new movie.
    - Require permission: `post:movie`
    - Require title, release_date in the request body.
    - Example: `curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -d '{"title": "Avenger Endgame", "release_date": "2024-10-10"}'`
    - Output:
        ```json
        {
            "message": "Movie created",
            "movie": {
                "id": 2,
                "release_date": "2024-10-10",
                "title": "Avenger Endgame"
            },
            "success": true
        }
        ```
        
3. `PATCH /movies/<int:movie_id>` - Update a movie.
    - Require permission: `patch:movie`
    - Requrie movie_id
    - Respone 404 error if movie_id not found
    - Example: `curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Content-Type: application/json" -d '{"title": "Avenger Endgame", "release_date": "2024-11-10"}'`
    - Output:
        ```json
        {
            "message": "Movie updated",
            "movie": {
                "id": 1,
                "release_date": "2024-11-10",
                "title": "Avenger Endgame"
            },
            "success": true
        }
        ```

4. `DELETE /movies/<int:movie_id>` - delete a movie.
    - Require permission: `delete:movie`
    - Requrie movie_id
    - Respone 404 error if movie_id not found
    - Example: `curl -X DELETE http://127.0.0.1:5000/movies/1`
    - Output:
        ```json
        {
            "message": "Movie deleted",
            "success": true
        }
        ```

5. `GET /actors` - Returns a list of actors.
    - Require permission: `get:actors`
    - Example: `curl http://127.0.0.1:5000/actors`
    - Output:
        ```json
        {
            "actors": [
                {
                    "age": 43,
                    "gender": "Male",
                    "id": 1,
                    "name": "Chris Evans"
                }
            ],
            "success": true
        }
        ```
6. `POST /actors` - Creates a new actor.
    - Require permission: `post:actor`
    - Require name, age and gender in the request body.
    - Example: `curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -d '{"name": "John Cena", "age": 47, "gender": "Male"}'`
    - Output:
        ```json
        {
            "actor": {
                "age": 47,
                "gender": "Male",
                "id": 2,
                "movie_id": null,
                "name": "John Cena"
            },
            "message": "Actor created",
            "success": true
        }
        ```

7. `PATCH /actors/<int:actor_id>` - Update a actor.
    - Require permission: `patch:actor`
    - Requrie actor_id
    - Respone 404 error if actor_id not found
    - Example: `curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -d '{"name": "John Cena", "age": 47, "gender": "Male"}'`
    - Output:
        ```json
        {
            "actor": {
                "age": 47,
                "gender": "Male",
                "id": 2,
                "movie_id": null,
                "name": "John Cena"
            },
            "message": "Actor created",
            "success": true
        }
        ```

8. `DELETE /actors/<int:actor_id>` - delete a actor.
    - Require permission: `delete:actor`
    - Requrie actor_id
    - Respone 404 error if actor_id not found
    - Example: `curl -X DELETE http://127.0.0.1:5000/actors/1`
    - Output:
        ```json
        {
            "message": "Actor deleted",
            "success": true
        }
        ```

