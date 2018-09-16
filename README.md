# kelocalc
a simple web-API calculator

Deployed in 
Web

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
