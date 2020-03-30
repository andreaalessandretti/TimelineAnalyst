<div style="text-align:center"><img src="mlogo.png" height=300/></div>

**Early identification** and **social distancing** are _essential_ to reduce the spread of the virus.

* What can we do if we are tested positive?
* How do we know if we are already infected?
* How can we improve social distancing and reduce the spread of the virus?

**TimelineAnalyst** allows you to:
* Check if you crossed in the past a person that was tested positive using your data from Google Map Timeline;
* Identify the places with and high risk of infection for **people** to avoid them and **governments** to apply ad-hoc measures.

**[TimelineAnalyst](https://devpost.com/software/timelineanalyst)** was developed for the hackathon [#CodeVsCovid19](https://codevscovid19.devpost.com/).

## Dependences
**TimelineAnalyst** requires [Python](https://www.python.org/) and [Flask](https://flask.palletsprojects.com/en/1.1.x/) to be installed.
## Getting started!
See the video '2 min Pitch + DEMO (5 min)' below that illustrates how to setup and use TimelineAnalyst.

Main commands:
* **Start the TimelineAnalyst server**
```
python server.py
```
* **TimelineAnalyst client submits a timeline of an infected person**
```
python3 client.py nickname 1 <history length in days> <path to timeline zip file> <server address>
```
where '<path to timeline zip file>' is the path to the Google Map Timeline file (get yours [here](https://takeout.google.com/settings/takeout/custom/location_history), '<history length in days>' specify the length of your past timeline to be considered as infected, and '<server address>' is the link to the TimelineAnalyst server.

* **Check the timeline of a person**          
```
python3 client.py nickname 0 <history length in days> <path to timeline zip file> <server address>
```
* **Request the list of places visited by infected people**   
```
python3 client.py <server address>
```

## Videos
* 2 min Pitch:

[![ ](http://img.youtube.com/vi/59xqVFVcyfY/0.jpg)](http://www.youtube.com/watch?v=59xqVFVcyfY)

* 2 min Pitch + DEMO (5 min)

[![ ](http://img.youtube.com/vi/sEH6_WzLkY4/0.jpg)](http://www.youtube.com/watch?v=sEH6_WzLkY4)
