# ClassUCLA
This is a class check and enroll program for myUCLA. 

in directory /app/

it has all the information that you need for watching a class. All one needs to do is to edit the json file.

the other file is to find detailed class information. 

It can scan through all the classes' detailed information and output an excel, csv(or pd DataFrame)

Now it supports
* subject
* course number
* title
* website
* status
* waitlist*status
* days
* time
* location
* units
*  instructor
*  final_exam_day
*  final_exam_weekday
*  final_exam_time
*  final_exam_avail
*  grade_type
*  restriction
*  impacted
*  individual*studies
*  level
*  *requisite*//TODO
*  course*description
*  class description
*  GE requirement
*  writingII requirement
*  diversity requirement
*  class notes

To look for specific set of classes, just enter class id in scrapy.py by ./scrapy.py
and to get all available detailed class website, just run ./get_available_webiste.py
