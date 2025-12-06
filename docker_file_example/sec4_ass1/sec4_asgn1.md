  GNU nano 6.2                                                 assignment1.md                                                          
# assignemnt1: Manage multiple continer

# answer:
docker container run --name nginx_local -d -p 8080:80 nginx:latest

docker container run --name mysql_local -e MYSQL_RANDOM_ROOT_PASSWORD=YES -d -p 3306:3306 mysql

docker container run --name apache_server -d -p 8080:80 httpd


# to stop 
docker container stop $(docker container ps -q)

# to delete everything 
docker system prune -a -f




