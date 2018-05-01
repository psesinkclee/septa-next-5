# septa-next-5

This script uses Septa's open train hackathon data to parse the status of trains for specific route or routes on the Regional Rail. Data is used to draw a time board with the next 5 trains on that route/direction that mimics the look of Septa's status boards. This script can be scheduled so that a machine always has a current board image for display or messaging.


## config setup

### [TrainRouteInformation] 
#### departureStation
Enter your departure station ID below from the following options Station IDs can be found here:
https://transitfeeds.com/p/septa/262/latest/stops
example: Jefferson Station is '90006'

#### boundDirection
Train direction is either 'Northbound' or 'Southbound'
The directions are not geographical references, but a reference to the old Reading and Pennsy Railroads. The key to understanding the
direction is by using Suburban Station as a starting point: Any trains that that move eastbound towards
Market East are all considered Northbound; trains going from Suburban to 30th St are all Southbound. The 'path' field describes more
accurately the path of travel along the various branches.

#### trainDestination
Enter the train line destination. This may not be the name of the stop you are, but is the final destination of that line.  Ensure
that the destination station is correct for the line(s) you are interested in. You can enter multiple destinations by adding a comma
(see example in config file). Here is a list of possible train destination stations:
'Airport', 'Bryn Mawr''Chestnut H East', 'Chestnut H West', 'Cynwyd', 'Doylestown', 'Elwyn, ''Fox Chase', 'Glenside', 'Lansdale',
'Marcus Hook', 'Malvern', 'Norristown', 'Newark', 'Norristown TC', 'Elwyn', 'Paoli', 'Suburban Station', 'Thorndale', 'Trenton',
'Warminster', 'West Trenton', 'Wilmington'

#### trainLineName
Enter the name of the train line.  This will be used as the header of the train time image that is created.

&nbsp;
### [TrueTypeFontFile] 
#### TTF
Enter the filepathe to the true type font file (TTF) below.  You can find TTFs online for most standard fonts for free.
