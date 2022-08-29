# Marine App

Marine App is an application which contains data for a maritime data intelligence company.
The Api has been developed with Fast Api and User Interface with VueJs.

## Usage

This project contains docker-compose.yml to help you set up easily without requiring to install
dependencies to run the application only need to run the following

```sh
$ docker-compose up --build -d 
```

## Database Schema

### Vessel Position

This is the model where we store the vessel positions of our app.
Fields :
* vessel_id = this is the id of a vessel
* latitude = this is latitude of the vessel. Latitude can be between -90 to 90.
* longitude = this is longitude of the vessel. Longitude can be between -180 to 180.
* position_time = this is the time when the coordinates have been sent to the system. 
Time has the following format : `%Y-%m-%d %H:%M:%S.%f` e.g. `2017-11-10 05:43:07.000000`

## Api Collection

Apis of the project is:

### Ingest Vessel Position

* Url: `localhost:8002/vessel-position/`
* Method: `POST`
* Body : `{'vessel_id':1,'latitude':30.323,'longitude':32.3','position_time':'2017-11-10 05:43:07.000000'}`
* Response : `{'vessel_id':1,'latitude':30.323,'longitude':32.3,'position_time':'2017-11-10 05:43:07.000000'}`

There is validation for correct range of `longitude` and `latitude`.
Also, i have made a validation for impossible travels. I assume that a vessel can travel up to 0.5 kilometers
per minute, so we make proper calculations and validation based on the last entry of this vessel in our DB.
If the entry is above proper threshold it will return proper error message.

### Retrieve Vessel Positions

* Url: `localhost:8002/vessel-position/`
* Method: `GET`
* QueryParams :
    * `skip` (optional) : you can define how many of the entries you would like to skip 
    * `limit` (optional) : with this param you can define how many vessel positions the api can return. 
  Default number is 100
    * Response :
      ```json
      {
        "number_of_pages": 20,
        "total_vessel_position": 30000,
        "data": [
            {
              'vessel_id':1,
              'latitude':30.323,
              'longitude':32.3,
              'position_time':'2017-11-10 05:43:07.000000'
            }
        ]
      }
      ```


## Local Development setup instructions

### Install pyenv with python 3.10.4

* Install prerequisite packages https://github.com/pyenv/pyenv/wiki#:~:text=Suggested%20build%20environment
* Install pyenv : git clone https://github.com/pyenv/pyenv.git ~/.pyenv
* Set pynenv in
  bash https://github.com/pyenv/pyenv#:~:text=make%20%2DC%20src-,Configure%20your%20shell%27s%20environment%20for%20Pyenv,-Note%3A%20The%20below
* Download python pyenv install 3.10.4

More details : https://github.com/pyenv/pyenv

### Install Poetry and start projects new virtual env

* Download poetry and install : curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py |
  python3 - configure your current shell run `source $HOME/.poetry/env`
  *Set python 3.10.4 as default inside project folder `poetry env use ~/.pyenv/versions/3.10.4/bin/python`
* Create virtual env for project. Inside in project directory run `poetry shell`
* Install dependencies `poetry install`

More details :  https://python-poetry.org/

### Run tests

* I have created a script which run the tests which is in following path `marine-be/scripts/test.sh`

The  script can be found
here : https://github.com/dtagkalos93/marine-app/blob/main/marine-be/scripts/test.sh \ 

#### Note : This scripts should be run from the backend folder otherwise the script will not find poetry. 

### Run auto-farmat and linting

* I have created a script which scan all the code and fix issues with formatting and linting 
`marine-be/scripts/project-formating.sh`

The  script can be found
here : https://github.com/dtagkalos93/marine-app/blob/main/marine-be/scripts/project-formating.sh

### Import Test Data

Also i have created two scripts to ingest test data. 
* The first one will ingest vessel positions as it found in the file. So many of the
vessel positions is no ingested due to validation of impossible travel and because the file is unordered 
for position time. This script can be found in `marine-be/scripts/populdate_data.sh`
* the second one will order vessel positions based on position time from lower to higher and will ingest 
them to database `marine-be/scripts/populdate_ordered_data.sh` 

The commands can be found
here : https://github.com/dtagkalos93/marine-app/blob/main/marine-be/scripts/populate_data.sh \
https://github.com/dtagkalos93/marine-app/blob/main/marine-be/scripts/populate_ordered_data.sh

### User Interface

I have also created a UserInterface which can displays the vessel positions.
![](/Users/dtagkalos/Desktop/Screenshot 2022-08-29 at 6.28.47 PM.png)

### Notes

* Due to M1 architecture Docker probably will fail with the following message `Unable to connect to PostgreSQL server: SCRAM authentication requires libpq version 10 or above.`.
The solution that is proposed is before run any of the scripts or build the docker image to run the following command
`export DOCKER_DEFAULT_PLATFORM=linux/amd64`

More details here : https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem

* If i have more time i would like to add to project a security authentication. For example JWT Token.
* Because I misunderstood the statement regarding the user interface and I realized it the last moment 
the api I have created is not exactly what should be implemented according to the user interface that have been asked.
My Api is a general api which returns all the vessel positions that exists in the database ordered by position time and paginated.
If we would like to be more accurate i should have created a endpoint which have the following response:
```json
[
  {
    "vessel_id":1234,
    "vessel_positions": [
      {
        'latitude':30.323,
        'longitude':32.3,
        'position_time':'2017-11-10 05:43:07.000000'
      },
      {
        'latitude': 30.323,
        'longitude': 32.3,
        'position_time': '2017-11-10 05:43:07.000000'
      },
      ...
    ]
  }
  ...
]
```

So this response is grouping vessel positions based on vessel_ids.
Also, i don't have the experience to create a more complicated UI which can display the vessel trips in sea.
Most of my experience is as backend engineer and i have never written Vue Js in the past. 

* Last but not least, i would like to have more time to find a better way for travel validation probably my validation 
is only an assumption and based on some research i made on the internet. Another solution that it comes is my mind is to 
make an external call to Google Maps API and find a way to see if the location is a land or sea but i did not have the
time to deep in the Google Maps API Documentation and find out if it is a proper call.