#Spark Demo - DDoS

*Includes the demo for Apache Spark + InterSystems Cache.*

NOTE - THE CODE IS NOT OPERATIONAL

This was intended as a demo for InterSystems Cache integrated into Spark, but instead I decided to not use the product and explore some other ML models that aren't neural nets (namely, time-propagating GMMs).

The data is streamed from 1.usa.gov, a website that tracks all clicks around the world that are in the .gov domain (along with other info, like referral pages and geographical coordinates), processed, and sent to a GMM model that will "detect" a potential DDoS attack, inferred from expected normal behavior.

Since I believe that ML visualization is a long-neglected topic, I also included in Dashboard.py a simulation for the clicks, and how they are processed by the GMM.


## Setup

- Run DataProcessor.py and select the features you want from one of the training sets (set<somenumber>.json)
- Run GMMTrainer.py, selecting a value for NUM_GAUSSIANS (the initial number of Gaussians that the clustering + error correcting algorithm will work with). GMMTrainer.py uses Occam's Razor to spit out the smallest number of Gaussians that also minimize the error.
- Run Dashboard.py.

## TODO

- Make this thing operational. I'm super swamped so I'll take any collabs!
- It will be nice if we did a time-propagating GMM (and more believable)


(c) Adrian deWynter, 2017
