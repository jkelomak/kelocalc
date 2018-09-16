# kelocalc
a simple web-API calculator

Deployed in https://kelocalc.herokuapp.com/

specification for the API:
    
Endpoint:
GET /calculus?query=[input]

input: UTF-8 with BASE64 encoding
supported operations: +, -, *, /
expression syntax according to standard mathematical conventions

output on success:
{ error: false, result: number }

on error:
{ error: true, message: string }
with HTTP error code 400

three kinds of errors: encoding error, syntax error, zero division error

NOTE: The creators python installation is quite messed up. Because of this, there are a lot of unnecessary things in the requirements. My apologies, and use caution!
