# DCM PROCESSOR
A dicom processing library setup with docker containers

## DEPENDENCIES
1. Docker & Docker Compose

## Getting up and running
1. open the `.env` file with any text editor and set the `BASEDIR` variable to a folder which will be used a a base for mounting docker volumes
2. build and pull docker images with `bash build.sh` [Run with `sudo` if needed]
3. run docker containers with `bash run.sh`

## Containers in this library
1. orthanc    : The orthanc server which servers as an intermedairy between dicom providers and our services.
2. scheduler  : The flask based service for scheduling jobs in our service registry
3. worker     : A worker container which executes the scheduled tasks.
4. dashboard  : A dashboard for RQ workers. Which shows the state of scheduled jobs


## Scaling up workers
You can scale the number of workers by pass the argument `--scale worker=N` where `N` is the number of instances you want.


## Preparing your own service
A service consist of two parts
1. An entry in the services `registry`
2. An entry in the service `modules`

### Service entry in the registry
A service entry in the registry is basically a folder which contains a `settings.json` file and a python file.
The json file defines the job associated with the service and the python file provides a callback function whose return value determines when a job is to be run.
- The `settings.json` file can either be an object or an array of objects with the following fields:
    `jobName` :  [string,required] the name of the job, this should be unique from other service jobs
    `worker` : [string,required] name of the function to be run as the worker, this should be a full function name. (see section below for details.)
    `callback` : [string,required] name of the function which determines if a job should be scheduled for the current dicom processing or not. (see section below for details.)
    `dependsOn` : [string/list,optional] name(s) of jobs which the current service job depends on. this will make sure that those jobs run successfully before this job runs.
    `priority` : [string,optional] the priority level assigned to this job. if not specified a default priority is assigned.
    `timeout` : [string/number,optional] the RQ queuing timeout default is 1 hour.
    `params`: [object,optional] this is an object with additional parameters that will be sent to the worker function.
    `sortPosition` : [number,optional] this is a sorting variable which is used to sort the order in which jobs are scheduled (Note: independent jobs are however scheduled before dependent jobs)
    `description` : [string,optional] this is a description for this current job. Its not used in any operation but only for third parties to have an idea what your service does.

- The python file should contain the `callback` function(s) you stated in the `settings.json` file
- For an example check the `temp` service folder in the `services` folder.