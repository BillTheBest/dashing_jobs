#Dashing Jobs

Quick and dirty scripts for getting data into [Dashing](http://dashing.io). The scripts I've written so far are for displaying Ganglia, GridEngine, and Isilon data.

[Sample image of working dashboard](https://raw.githubusercontent.com/ssplatt/dashing_jobs/master/dashing_demo.png)

Widgets used in the demo image:

- [Weather](https://gist.github.com/davefp/4990174)
- [Hotness](https://gist.github.com/rowanu/6246149)
  - with [mod to allow inversed ranges](https://gist.github.com/munkius/9209839)
- Meter
- Twitter Comments, tagged #hpc
- List
- Image
- Clock

##Ganglia data

My `ganglia.rb` script runs from the `dashing_project/jobs/` folder and pulls JSON data from [Ganglia](http://ganglia.sourceforge.net/), which is running on my compute cluster. You may need to add a few lines to the `Gemfile` in the `dashing_project/` folder:

```
gem 'httparty'
gem 'addressable'
```
then run `bundle install`.

##Grid Engine data

These scripts are meant to be run via cron on the head node of a compute cluster. They call `qstat` and `qacct` then parse their output for the required data and POST it to Dashing.

##Isilon data

This script runs via cron on the first node of an Isilon cluster. It calls `isi status -q` and parses the output then ships it to Dashing.

To add your own custom lines to cron on the Isilon system:

1. check with Isilon support that this won't ruin your system. I take no respsonsibility for what you do.
1. store the script in a location like `/root/bin/isi_to_dashing.py`
1. create a file `/etc/local/crontab.local` with a regular crontab style line calling the script
1. restart cron with `killall -HUP cron`
1. check that your line from `/etc/local/crontab.local` was added to the bottom of `/etc/crontab`
