# time_tracker  
**INFO**  
Script to see how i spent my time when i am learning how to code  
This runs only on linux see reqirements.txt for dependencies

**DONE**
+ integrated with firebase to store activiti titles and time

**TODO**  
- flask web page to get data from firebase
- fancy charts with charts.js


**DB structure**
activities (collection)    
 |-------->date1 (document)    
 |          |--->activity1(window_title) (collection)    
 |          |       |--->title    
 |          |       |--->time(increment this)    
 |          |       |    
 |          |--->activity2(window_title)    
 |          |       |--->title    
 |          |       |--->time(increment this)    
 |          |       |    
 |          |--->activity3(window_title)    
 |          |       |--->title    
 |          |       |--->time(increment this)    
 |          |           
 |          |           
 |-------->date2    
 |          |--->activity1(window_title)    
 |          |       |--->title    
 |          |       |--->time(increment this)    
 |          |           
 |-------->date3    
 |          |--->activity1(window_title)    
 |          |       |--->title    
 |          |       |--->time(increment this)    
 |          |       |    

