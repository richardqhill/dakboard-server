# dakboard

This is a personal server for our dakboard family calendar.

It provides an API to access:
- a "count up" timer for last bottle based on pre-exisiting data populated from huckleberry
- battery/range of our tesla

This is not meant to be scalable but it is meant to be secure.

This keeps teslamate access strictly limited to local network. 
The publicly accessible web server only exposes non-input GET endpoints that return non-sensitive data.

TODO:
- change auth from username/pass to something else
- gunicorn WSGI server