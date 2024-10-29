# "Liine Cooks" project

> "A chef de partie, station chef or line cook is a chef in charge of a particular area of production in a restaurant."  
  -Sophie Brickman (September 12, 2010). "How French Laundry's chefs reach for the stars". San Francisco Chronicle.  


"Liine Cooks" is a play on words and the name of this fancy restaurant info API service!

## Overview: 

*Primary Purpose:* Create an application that ingests data from a csv file and makes it query-able through a REST API.  

*Secondary Purpose:* Demonstrate use of Django and DRF with a standard DBMS, Postgresql, data ingestion, and cross-platform, automated deployment using docker-compose.  


*From project description that was emailed:*
> Build an API with an endpoint which takes a single parameter, a datetime string, and returns a list of restaurant names which are open on that date and time. You are provided a dataset in the form of a CSV file of restaurant names and a human-readable, string-formatted list of open hours. Store this data in whatever way you think is best. Optimized solutions are great, but correct solutions are more important. Make sure whatever solution you come up with can account for restaurants with hours not included in the examples given in the CSV. Please include all tests you think are needed.

*Input*
    - takes a single param
    - param is a datetime string (24hr format): YYYY-MM-DDThh:mm
    
*Return*
    - List of restaurants
    - Format is not specified, but DRF can provide a lot of flexibility. A simple modification of `RestaurantHourSerializer` can change the output from the API.
    - account for restaurants with hours not included in the examples given in the CSV


Start with the project's purpose. This helps everyone stay on the same page from the beginning.

## Process: 

### API development (start with the end!)
1. Research multiple effective ways of handling business hours
   - settled on a commonly used method for the models - Two models/tables:
       - Restaurant: holds restaurant name and a PK
       - RestaurantHour: 
           - foreign key to Restaurant
           - weekday: enumerated integer choice, 0-6 with 0 being 'Mon' and 6 as 'Sun'
           - open_time and close_time: TimeField from Django model class library
2. Declare models to Django admin so data can be entered manually for development of the API
3. Setup serializer for DRF to read the datetime string from url query and filter RestaurantHour model based on query
4. Make getters in serializer to format the response values as needed

### Ingestion / quasi-ETL process

1. Experiment with parsing strategies
   - tried regex at first, but it didn't take long to realize that approach was more computationally complex
   - split sets of days & hours on '/' 
   - For each set:
       - get string index of first numeral
       - get days section which may include multiple ranges, or single days split by comma
       - covert char days to numeric 0-6

## Challenges and Solutions: 

### Day & Time parsing
The first problem was parsing the day/time formats because each had two. Days could be a range (Mon-Fri), individual days (Mon, Wed, Fri), and could be inter-mixed and seperated by comma. Time formats are 12hr, but only include minutes if they aren't right on the hour.  

I differentiated the weekday formats just with a condition (`if "-" in day_split`).   
Multiple formats for time parsing can be approached with a try-except (`ValueError`).  

I could have also handled it with an alternative time library like `Arrow` or `dateutil`, but I opted for a lighter-weight solution rather than adding a whole library to only eliminate two lines of code.  
 
### Open past midnight!

I noticed a more difficult problem with restaurants that were open past midnight. Customers may think of 1AM as part of the day they just lived through, but computers consider that the following day.  

The solution I came up with was to determine the existence of a 'open at or past midnight' case `end_time < start_time`, and in those cases we create a new entry of hours for that restaurant with an opening time of 00:00 and closing at the given closing time with the weekday incremented to the next, while the original set of hours is changed to close on the orinigal given day at 11:59PM  

This solution successfully enabled queries for restaurants that opened at, for example, 5PM and closed at 12:30AM  

### Deployment

This application requires multiple services:
1. Django app
2. Postgres database
3. Migrations for schema/models
4. A data ingestion process
5. Tests 
6. A separate web server for static files (icons, js, css) used by DRF's automated API docs and the Django admin interface

In the context of this POC, Docker compose offers easy configuration and orchestration of these containers and services.  
In a true production environment, one might be able to use this containerized solution, but OpenTofu/Terraform might offer scalability options (like adding a cache layer)

## Result summary

The API application, *Liine Cooks*, is capable of demostrating data ingestion, testing, and deployment of a Django/DRF API application.  
The postgres database can scale well on it's own, or the DB connection string can be updated to use an external service such as AWS RDS (which I usually recommend).  


In general, I'm pleased with the resulting API service. For scaling I would add a caching layer most likely using the `django-redis` package. Other alternatives worth considering are RabbitMQ or, if the app were to be deployed on AWS we might use SQS/SNS.  


If the data ingestion were to be scaled up to a full ETL process, it could be triggered as a batch process with Celery Beat, or moved to an AWS Glue job, triggered with EventBridge, AWS Lambda, and S3 (note that a pseudo-S3 mount is used in this POC).  



