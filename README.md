# Epic Seven Secret Shop Auto Refresher

## Demo

![Demo](videos/e7-auto-ss-demo.gif)

## Features
* Takes control of your cursor to automatically refresh the shop and buy covenant bookmarks and mystic medals
* Implements realistic mouse movements and clicks to avoid detection
* Use the UI to view statistics: the number of covenant bookmarks/mystic medals bought, skystones used, skystones per covenant bookmarks / mystic medals, time elapsed
* Settings available to control cursor speed, cursor deviation, and number of skystones used to refresh
* Automatically handles server reset, allowing you to leave it on overnight
* Easy to setup and use!

## Instructions
1. Download the E7 PC client (currently only tested on windows)
2. Download the app here: [e7-auto-ss.exe](https://github.com/timthlu/e7-auto-ss/releases/download/v1.0.0/e7-auto-ss.exe)
3. Run E7 and navigate to the secret shop
4. Run e7-auto-ss.exe **as administrator**. A UI should start up after a couple seconds.
5. Select your settings and press start! The refresher will move and resize your application and take control of your cursor.

Settings/Controls:
* Speed: cursor movement speed. *An integer >= 1*. Smaller means faster, larger means slower but smoother cursor movements. 
* Deviation: controls cursor pathing. *An integer >= 10*. Larger means wider cursor movements.
* Max # of skystones to spend: for the next looping triggered by the "Start!" button, the refresher will use at most this many skystones on refreshes, then stop automatically.
* Stopping the refresher: the refresher can be stopped at any time by pressing the "q" key on your keyboard. It will finish its current action then stop, which may take a few seconds.

Tips:
* Try not to move your cursor after pressing start. It may interfere with the pathing and may cause the refresher to miss.
* Try to have a stable internet connection. Too much buffering may interfere with the pathing and may cause the refresher to miss.
* If you are leaving the refresher on overnight, please remove the shortcut icons at the bottom of the lobby screen, as during daily server reset it may interfere with the refresher's routing past the daily login reward screens and back into the secret shop. The refresher may click an icon at the bottom of the lobby and end up someplace completely unfamiliar and execute some undefined behaviour...