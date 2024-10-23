# Liine Cooks - API app by SJlawson

> A line cook is a kitchen staff member who works at a specific station in a restaurant kitchen, preparing and cooking food.  
*"Liine Cooks"* is a play on words and the name of this fancy restaurant info app!  


- Dependencies are recent versions of
    - git
    - docker
    - docker-compose

## Get and deploy
  
- clone the git repo
- run `docker-compose up`
- To test the API, send GET requests to http://0.0.0.0:8000/api/hours?datetime=YYYY-MM-DDTHH:MM 
- Request time format is 24-hour, but response shows meridian 
- Example request that returns data:
  - [http://0.0.0.0:8000/api/hours?datetime=2024-10-22T13:36](http://0.0.0.0:8000/api/hours?datetime=2024-10-22T13:36)


## Data Loader
- This Django management command is meant to simulate a simple batch ETL pipeline from a hypothetical S3 mounted bucket.
- The loader is setup to run automatically as a service in `docker-compose.yml`
- Locally, use the docker exec command:  `docker exec -it take-home_django_1 python manage.py load_restaurant_data /s3_mount/restaurants.csv`


