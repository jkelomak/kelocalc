# kelocalc
a simple web-API calculator, Deployed in https://kelocalc.herokuapp.com/
    
Endpoint:
GET /calculus?query=[input]

input: UTF-8 with BASE64 encoding
supported operations: +, -, *, /

The query syntax must follow standard mathematical conventions


The API returns:
on success:
{ error: false, result: number }

on error:
{ error: true, message: string }
with HTTP error code 400

The three kinds of errors are: encoding error, syntax error, zero division error

NOTE: The creator's python installation is quite messed up. Because of this, there are a lot of unnecessary things in the requirements. My apologies, and use caution!
