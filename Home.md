# Blog Api

## /register
* GET
```js
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 17
Content-Type: text/html; charset=utf-8
Keep-Alive: 60

<h1>Register</h1>
```
* POST
```js
# Success
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 107
Content-Type: application/json
Keep-Alive: 60

{
    "code": 0,
    "message": "success",
    "result": "{\"email\": \"aaa233@aa.com\", \"id\": 2, \"username\": \"loyo\"}"
}
# Error
HTTP/1.1 400 Bad Request
Connection: keep-alive
Content-Length: 62
Content-Type: application/json
Keep-Alive: 60

{
    "code": 1005,
    "message": "该邮箱已注册"
}
```

## /login
* GET
```
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 17
Content-Type: text/html; charset=utf-8
Keep-Alive: 60

<h1>Login</login>
```
* POST
```
# Success
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 107
Content-Type: application/json
Keep-Alive: 60

{
    "code": 0,
    "message": "success",
    "result": "{\"email\": \"aaa233@aa.com\", \"id\": 2, \"username\": \"loyo\"}"
}
# Error
HTTP/1.1 400 Bad Request
Connection: keep-alive
Content-Length: 68
Content-Type: application/json
Keep-Alive: 60

{
    "code": 1001,
    "message": "账号或密码错误"
}
```
