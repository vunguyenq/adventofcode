# Code repository for coding challenge adventofcode2021  
This repository contains code and puzzle inputs for Advent of Code 2021: https://adventofcode.com/2021

Run make on a BASH shell to create code template for each day challenge.  
  
Create new day code:  
```make create dayname="01 DayTitle"```
  
Delete day code:  
```make delete day=01```   
  
If there is more than 1 test case, sepearte test cases in file <code>input_testxx.txt</code> with <code>#####INPUT_SEPERATOR#####</code>.  
Example - <code>input_test01.txt</code> with 3 test cases:  
```
1 2  
3 4
#####INPUT_SEPERATOR#####
5 6  
7 8
#####INPUT_SEPERATOR#####
9 10 
11 12
```
