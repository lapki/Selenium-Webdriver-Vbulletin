# Selenium-Webdriver-Vbulletin
A Selenium script using Webdriver to perform browser actions on a vbulletin website headlessly

# To-Do

I initially wrote this script with a few websites in mind and some aspects of their layout that reoccurred repeatedly were hardcoded into the script. 

For example, I would specify which iframe index to use for submitting a post when I encountered a website that used iframes for their post forms (Most used iframes but some did not). In the future I will have to edit the script to automatically locate the correct iframe, and until then I have hardcoded an index for the iframe in this version of the script.

I rewrote this script somewhat to make it more "general" because there are many vbulletin websites spannng several versions, and I will have to continue to debug this iteration of the script.
