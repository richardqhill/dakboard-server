# dakboard

This is a personal server for our dakboard family calendar.

It provides an API to access:
- a "count up" timer for last bottle based on pre-exisiting data populated from huckleberry
- battery/range of our tesla
- temp/humidity from switchbot sensors

This is not meant to be scalable but it is meant to be secure.

This keeps teslamate access strictly limited to local network. 
The publicly accessible web server only exposes non-input GET endpoints that return non-sensitive data.

---

This also hosts an instance of mediawiki. In docker-compose.yml, comment out the volume link for LocalSettings.php on first start.

```
docker-compose up
```

Navigate to http://localhost/mw-config/index.php and complete the initial setup.
