### About:

* The model calculates probability of car accident by borough in London
(probabilities provided as scaled anomaly score by 
 [isolation forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html))

* Feature used:
    - Historical weather data
    - Road surface condition (historical)
    - Road class (motorway etc.)
    - Road type (one way street, dual carriageway etc.)
    - Speed limit
    - Junction control
    - Light condition
    - some others.

* For what?
    - predicting car accidents probability can be used for
    optimization of schedules of city services (ambulance or police)
    - there is possibility to integrate this model in city services
    automated systems, responsible for scheduling

* What else to do?
    - Averaging by boroughs is very rough guess. It's possible to 
    predict probabilities for every part of road in the city, but you 
    need much more calculation resources.
    - Tune model and try another models
    - Use more historical data as features
    
* Visit [our github](https://github.com/tazizov/car_accidents_app)
    
   
     

    
         