### Tips and tricks

To make sure your Docker containers are flushed and re-created between docker-compose re-runs, use those commands:
- `docker rm $(docker ps -a -q)` (removes containers that are not running)
- `docker volume rm $(docker volume ls -qf dangling=true)` (removes orphaned volumes)

To make life easier, I recommend [ctop](https://ctop.sh/) tool for overseeing container behavior and resource usage