### Liine Take Home 

__Python is preferred, but if you feel unable to complete it using python, use whatever programming language you feel most comfortable in.__

Build an API with an endpoint which takes a single parameter, a datetime string, and returns a list of restaurant names which are open on that date and time. You are provided a dataset in the form of a CSV file of restaurant names and a human-readable, string-formatted list of open hours. Store this data in whatever way you think is best. Optimized solutions are great, but correct solutions are more important. Make sure whatever solution you come up with can account for restaurants with hours not included in the examples given in the CSV. Please include all tests you think are needed.

## API

Input
    - takes a single param
    - param is a datetime string (24hr format): YYYY-MM-DDThh:mm
    
Return
    - comma-separated list of restaurants, e.g. {"restaurants": ["Beasley's Chicken + Honey", "Garland"]}
    - account for restaurants with hours not included in the examples given in the CSV

### Assumptions:
* If a day of the week is not listed, the restaurant is closed on that day
* All times are local — don’t worry about timezone-awareness
* The CSV file will be well-formed, assume all names and hours are correct

### Want bonus points? Here are a few things we would really like to see:
1. A Dockerfile and the ability to run this in a container

If you have any questions, let me know. Use git to track your progress, and push your solution to a github repository (public or if private just give me access @sharpmoose)
