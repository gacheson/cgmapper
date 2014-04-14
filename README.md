# cgmapper

A fork of cgminer2rrd by vitaminmoo. This repo provides an easy-to-use tool for overclocking and recording hashrate output via the cgminer API, for one or more cards, and writing it to file for later use. Once it's done, it will have found and set the optimal clock speeds for each card. There is also the option of generating heatmaps to help visualize the hashrate output. It's been developed on Linux to be cross-platform, however it may or may not work on other platforms (currently untested).

## Requirements

* `python2.7`
* `pip` for installing `scipy`
* `R` and `ggplot2` to generate heatmaps
* `cgminer` or `sgminer` (`sgminer` is preferable as it has more precision on the MHS API endpoint)
* `cgminer` API is enabled (add `"api-listen" : true,` `"api-allow" : "W:127.0.0.1",` `"api-port" : "4028",` to your .conf file, or to your .bat file use *`--command argument`* instead)
* make sure you have disabled or removed `gpu-mem` `gpu-engine` `auto-gpu` and their respective settings

## Usage

cgmapper only does one thing (at which it's pretty good at):

>Finding and setting the optimal clock speeds, for one or more cards, while writing data to file for later use with `R`

If you want to specify more than one card, in clocks.py:

`card = '0,1,2,..'`

Each card can have its own core clock range, memory clock range, and core/memory step values ~~or they can have a single value for each that is applied to all~~:

`core_min = '900,1000,1100,..'`

~~`core_min = '900'`~~

cgmapper's gpu identifiers are linked to cgminer. If the card you want to use is `GPU 1` in cgminer, it will be `card = '1'` in cgmapper.

Additionally, there are more options that you can set which are briefly commented on in clocks.py *`# comments are preceded by a hash mark`*.

## Overclock Tuning

To find your cards' optimal clock speeds:

1. Make sure cgminer is running
2. Be aware of your cards' stable range of core and memory clock speeds
3. Customize the top of clocks.py to specify this range
4. Run `./clocks.py` and wait (may take up to several days)
5. If `./clocks.py` crashes or you have to stop it, just restart it when you can - it won't retry settings that it has already tried
6. Once `./clocks.py` has finished, the cards' optimal clock speeds will have been set for you
7. Optionally, you can generate heatmaps with `R --no-save < clocks.R`
