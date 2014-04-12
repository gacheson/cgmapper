# cgmapper

A fork of cgminer2rrd by vitaminmoo. This repo provides an easy-to-use tool for sending and receiving commands and data from the cgminer (or, preferably, sgminer) API, across multiple cards, and writing it to CSV files. It's been developed on Linux, and may or may not work on other platforms.

## Requirements

* `python2.7`
* `pip` for installing `scipy`
* `R` and `ggplot2`
* `cgminer` or `sgminer` (`sgminer` is preferable as it has more precision on the MHS API endpoint)
* The API enabled for the above (add `"api-listen" : true,` `"api-allow" : "W:127.0.0.1",` `"api-port" : "4028",` to your cgminer config file)

## Usage

Since this fork is repurposed for a single task, there is only one use for it:

1. Actively fiddling with overclock settings while writing data to a CSV for later processing with `R`

## Overclock Tuning

To generate a heatmap of your core/mem clock hashrate output for each card:

1. Be aware of your cards' stable range of core and memory clock settings
2. Customize the top of clocks.py to specify these settings
3. Run `./clocks.py` and wait (may take up to several days)
4. If `./clocks.py` crashes or you have to stop it, just restart it when you can - it won't retry settings that it has already tried (limited, see `.clocks.py` for more info)
5. Once `./clocks.py` has finished, generate a graph with `R --no-save < clocks.R`
