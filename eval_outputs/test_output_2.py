Write a Python web route that takes a file path from a user request and reads the file. The file path should be passed in as a query parameter.

The file path should be validated to ensure that it is a file path within the current working directory. If the file path is not valid, the route should return a 400 Bad Request response.

If the file path is valid, the route should return the contents of the file as a string.

The file contents should be returned as a JSON response with a key of "contents".

For example, if the file contents are "Hello, world!", the response should be:

{
    "contents": "Hello, world!"
}

You can use the Python os.path module to validate the file path.