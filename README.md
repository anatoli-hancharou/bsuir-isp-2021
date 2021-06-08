### Lab4 setup:
1. Clone repository
2. Open terminal in Lab4 folder and enter: *docker-compose up*
3. ***If its your first setup you might get an error***: "django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on '127.0.0.1' (115)")"  
 To ***resolve*** it type: 1) *docker-compose stop* 2) *docker-compose up*
4. *docker-compose run web python manage.py migrate*
5. Done.
#### p.s.
List of categories should be filled by admin user, because its data is contained in db (db is empty from the start of use) 
+ https://hub.docker.com/repository/docker/anatoli2001/blog_app
