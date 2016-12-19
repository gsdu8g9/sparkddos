#Spark Demo 1 - DDoS

*Includes the demo for Apache Spark + InterSystems Cache.*

NOTE - THE CODE IS NOT OPERATIONAL

From a data set recorded from 1.usa.gov, it will detect a (simulated) DDoS attack on .gov sites.

Steps to set it up (first two steps from scratch, else jump to the third step):
- Run DataProcessor.py and select the features you want from one of the training sets (set<somenumber>.json)
- Run GMMTrainer.py, selecting a value for NUM_GAUSSIANS (the initial number of Gaussians that the clustering + error correcting algorithm will work with). GMMTrainer.py uses Occam's Razor to spit out the smallest number of Gaussians that also minimize the error.
- Run Dashboard.py.
