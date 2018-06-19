# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
docker-compose down
docker rm -f $(docker ps -aq)
docker rmi -f springprojectbase_nginx_proxy springprojectbase_backend_server springprojectbase_postgres_db
