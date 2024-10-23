# Liine Cooks - API app by SJlawson

> A line cook is a kitchen staff member who works at a specific station in a restaurant kitchen, preparing and cooking food.  
*"Liine Cooks"* is a play on words and the name of this fancy restaurant info app!  


- Dependencies are recent versions of
    - git
    - docker
    - docker-compose

## Get and deploy
  
- clone the git repo
- IMPORTANT Rename and edit the file `env` to `.env`
    - Note that the password kept in this file is very silly and should never be used
    - Note that .env is ignored by git
    - This file could be replaces by a secrets manager offered by a cloud provider (i.e. aws secrets manager)
- run `docker-compose up`
- You should be able to see this README at [http://0.0.0.0:8000/](http://0.0.0.0:8000/)
- To test the API, send GET requests to http://0.0.0.0:8000/api/hours?datetime=YYYY-MM-DDTHH:MM 
- Request time format is 24-hour, but response shows meridian 
- Example request that returns data:
    - [http://0.0.0.0:8000/api/hours?datetime=2024-10-22T13:36](http://0.0.0.0:8000/api/hours?datetime=2024-10-22T13:36)
    - shows all restaurants: [http://0.0.0.0:8000/api/](http://0.0.0.0:8000/api/)

## Django admin setup
The app can be managed with Django's admin ui. To use it, you will need to create a super user with:  
`docker exec -it take-home_django_1 python manage.py createsuperuser`  
and enter the necessary fields.  

Once a user has been created, login at:  
[http://0.0.0.0:8000/admin


## Data Loader
- This Django management command is meant to simulate a simple batch ETL pipeline from a hypothetical S3 mounted bucket.
- The loader is setup to run automatically as a service in `docker-compose.yml`
- Locally, use the docker exec command:  `docker exec -it take-home_django_1 python manage.py load_restaurant_data /s3_mount/restaurants.csv`
    - the above command *should* run automatically
    
## Tests
- Yes, we have tests!!
- Run tests with: `docker exec -it take-home_django_1 python manage.py test`
- They also run on launch, so you should see the following as the containers start:  

>
```
testing_1      | Creating test database for alias 'default'...
testing_1      | Found 7 test(s).
take-home_data_loader_1 exited with code 0
testing_1      | System check identified no issues (0 silenced).
testing_1      | .......
testing_1      | ----------------------------------------------------------------------
testing_1      | Ran 7 tests in 0.025s
testing_1      | 
testing_1      | OK
testing_1      | Destroying test database for alias 'default'...
```


