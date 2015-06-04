from django.shortcuts import render_to_response
from models import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import re
import datetime
import copy
from datetime import timedelta
import pymongo
import pdb

connection = pymongo.MongoClient('localhost',27017)
db = connection.mongo
collection = db.modulestore.find() 

    
    
#print item.definition

# Global variables
itemsPerProblem = 3

def index(request):

    auth_user_list = auth_user.objects.all().order_by('id')

    extra_context = {"auth_user": auth_user_list}

    #return HttpResponse("Hello World!")
    return render_to_response("testProject/index.html", extra_context)

"""
#
# old code
#

def state(request):

    studentId = 6

    # in order to get records of all students
    # studentModule = courseware_studentmodule.objects.all()

    # in order to get records of a student with particular student_id
    # and the module_type is 'Problem'
    studentModule = courseware_studentmodule.objects.filter(
            student_id = studentId
        ).filter(
            module_type = 'Problem'
        )

    problems = []

    for row in studentModule:

        state = json.loads(row.state)
        attempts = 0
        #search in the state JSON array if there were attempts performed on
        #the current problem
        for key, value in state.iteritems ():
            if key == "attempts":

                attempts = value
                # checking if the student attempted to solve the problem
                if attempts > 0:
                    problem = {}
                    # problem is an associative array that stores values and keys (instead of indexes)
                    problem["problem_code"] = row.module_id
                    problem["attempts"] = attempts
                    problem["grade"] = int ( row.grade / row.max_grade * 100 )
                    problem["time_took"] = row.modified - row.created

                    problems.append(problem)

    extra_context = { "student_id": studentId,
                      "student_state": problems}

    return render_to_response("testProject/state.html", extra_context)
"""
def courses(request):

    # print "-----------------"

    studentModule = courseware_studentmodule.objects.filter(
            module_type = 'Problem'
        )

    courses = []

    for row in studentModule:

        course_id = row.course_id

        if not any(course_id in s for s in courses):

            courses.append(course_id)

    extra_context = { "courses": courses }

    return render_to_response("testProject/courses.html", extra_context)


def specifiedCourse(request, course_id, student_id = None):

    if request.method == 'POST' or student_id != None:# If the form has been submitted...

        student_ids = {student_id}
        problem_ids = request.POST.getlist('problem_ids')
        #hidden fields
        course_students = request.POST.getlist('students')
        course_id = request.POST.get('course_id') or course_id


        # in case student_ids array is empty, using all students enrolled in course
        if not student_ids:
            student_ids = re.findall('\d+', course_students[0])

        # student_states stores student's interaction with different problems
        student_states = []

        # a matrix and a vector that will be used for prediction
        matrixX = []
        vectorY = []
        # creating the structure of matrixX
        dataForMatrix = courseware_studentmodule.objects.filter(
            course_id = course_id
        ).filter(
            module_type = 'Problem'
        )

        allCourseProblems = []
        for row in dataForMatrix:
            if not any(row.module_id in s for s in enumerate(allCourseProblems)):
                allCourseProblems.append(row.module_id)

        # creating data structure to send to the prediction algorithm
        for studentId in student_ids:
            # matrixXrow is one row of matrixX
            # item at index 0 is a student id
            matrixXrow = []
            matrixXrow.append(studentId)

            for i in range(0,len(allCourseProblems)):
                for j in range(0,itemsPerProblem):
                    matrixXrow.append(0)

            # last item in matrixXrow is the final grade

            # getting times of all course components (courses, chapters, sequentials, problems)
            studentModule = courseware_studentmodule.objects.filter(
                        course_id = course_id
                    ).filter(
                        student_id = studentId
                    ).filter(
                        module_type = "problem"
                    )

            
            # sum of all grades (will be used to calculate final grade)
            sumGrades = 0
            
            for row in studentModule:
            
                # check if current problem_id is in passed problem_ids array
                if any(row.module_id in s for s in enumerate(problem_ids)) or not problem_ids:

                    state = json.loads(row.state)
                    attempts = 0
                    #search in the state JSON array if there were attempts performed on
                    #the current problem
                    for key, value in state.iteritems ():
                        if key == "attempts":

                            attempts = value
                            # checking if the student attempted to solve the problem
                            if attempts > 0:
                                # find index where to insert data in matrixXrow
                                problemItem = allCourseProblems.index(row.module_id)
                                gradeIndex = problemItem * itemsPerProblem + 1
                                attemptsIndex = problemItem * itemsPerProblem + 2
                                timeTookIndex = problemItem * itemsPerProblem + 3

                                matrixXrow[gradeIndex] = int ( row.grade / row.max_grade * 100 )
                                matrixXrow[attemptsIndex] = attempts
                                matrixXrow[timeTookIndex] = (row.modified - row.created).total_seconds()

                                sumGrades += int ( row.grade / row.max_grade * 100 )                 
            # adding final course grade
            matrixXrow.append(sumGrades / len(allCourseProblems))
            # adding current student row to matrix
            matrixX.append(matrixXrow)
            

        '''
        # structure of matrixX:
        [
            [| student id | problem 1 grade | problem 1 time taken | problem 1 attempts | problem 2 grade | ... | final course grade |],
            [| student id | problem 1 grade | problem 1 time taken | problem 1 attempts | problem 2 grade | ... | final course grade |]
        ]
        '''
        '''
        # This is how matrixX will look like for 2 students and 5 course problems:
        [
            [u'5', 0, 1, 13, 100, 5, 33, 0, 0, 0, 100, 3, 27, 0, 0, 40],
            [u'8', 100, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 1, 40]
        ]
        '''

        # creating data structure to send to the view


        
        for studentId in student_ids:
            
            # getting times of all course components (courses, chapters, sequentials, problems)
            timesModule = courseware_studentmodule.objects.filter(
                        course_id = course_id
                    ).filter(
                        student_id = studentId
                    )

            courseModules = []
            for row in timesModule:
                moduleRow = {}
                moduleRow["module_type"] = row.module_type
                moduleRow["module_id"] = row.module_id
                moduleRow["created"] = row.created
               
                courseModules.append(moduleRow)
            
            # sorting by times
            courseModules.sort(key=lambda x: x["created"])

            # finding lowest created time
            lowestTime = courseModules[0]["created"]
            for module in courseModules:
                if lowestTime > module["created"]:
                    lowestTime = module["created"]

            chapters = []
            chapCounter = 0

            # creating an array of chapters
            for module in courseModules:
                if module["module_type"] == "chapter":
                    chapter = {}
                    chapter["module_id"] = module["module_id"].split("/chapter/", 1)[1]
            

                    if chapCounter == 0:
                        chapter["created"] = lowestTime
                        chapCounter = 1
                    else:
                        chapter["created"] = module["created"]

                    chapter["sequentials"] = []
                    chapters.append(chapter)
                    
            coursed = []
            # replacing module_id with the Module name
            for i in range(0, len(chapters)):
                for j in collection:
                    if chapters[i]["module_id"] == j["_id"]["name"]:
                        chapters[i]["module_id"] = j["metadata"]["display_name"]
                collection.rewind()
            #print chapters             
            for course in studentModule: 
                #print course 
                if course == "course_id":
                    coursed.append(course)
            #print coursed    
            for i in range(0, len(chapters)):

                sequentials = []
                seqCounter = 0


                for module in courseModules:
                    if module["module_type"] == "sequential" and chapters[i]["created"] <= module["created"]:
                        if i + 1 == len(chapters) or chapters[i+1]["created"] > module["created"]:
                            sequential = {}
                            sequential["module_id"] = module["module_id"].split("/sequential/", 1)[1]
                            if seqCounter == 0:
                                sequential["created"] = lowestTime
                                seqCounter = 1
                            else:
                                sequential["created"] = module["created"]

                            sequential["problems"] = []
                            sequentials.append(sequential)

                chapters[i]["sequentials"] = sequentials
                

            # in order to get records of all students
            # studentModule = courseware_studentmodule.objects.all()

            # in order to get records of a student with particular student_id
            # and the module_type is 'Problem'
            studentModule = courseware_studentmodule.objects.filter(
                    course_id = course_id
                ).filter(
                    module_type = 'Problem'
                ).filter(
                    student_id = studentId
                )

            problems = []
            attemptsArr = []
            gradeArr = []
            timeTookArr = []
            student_chapters = []

            for row in studentModule:

                # check if current problem_id is in passed problem_ids array
                if any(row.module_id in s for s in enumerate(problem_ids)) or not problem_ids:

                    state = json.loads(row.state)
                    attempts = 0
                    #search in the state JSON array if there were attempts performed on
                    #the current problem
                    for key, value in state.iteritems ():
                        if key == "attempts":

                            attempts = value
                            # checking if the student attempted to solve the problem
                            if attempts > 0:
                                problem = {}

                                # problem is an associative array that stores values and keys (instead of indexes)
                                problem["problem_code"] = row.module_id.split("/problem/", 1)[1]
                                problem["attempts"] = attempts
                                attemptsArr.append(attempts)
                                problem["grade"] = int ( row.grade / row.max_grade * 100 )
                                gradeArr.append(problem["grade"])
                                problem["time_took"] = row.modified - row.created
                                timeTookArr.append(problem["time_took"])

                                problems.append(problem)

                                student_chapters = chapters
                                for chapter in student_chapters:
                                    sequentials = chapter["sequentials"]
                                    for i in range(0,len(sequentials)):

                                        if sequentials[i]["created"] <= row.created:
                                            if i + 1 == len(sequentials) or sequentials[i+1]["created"] > row.created:

                                                sequentials[i]["problems"].append(problem)

            student_state = {}
            student_state["student_id"] = studentId
            student_state["problems"] = problems
            student_state["chapters"] = student_chapters
            if len(student_chapters) > 0:
                # claculating averages of attempts, grades, and time took
                student_state["avg_attempts"] = float(sum(attemptsArr)) / float(len(attemptsArr))
                student_state["avg_grade"] = sum(gradeArr) / len(gradeArr)
                student_state["avg_time_took"] = sum(timeTookArr, datetime.timedelta(0)) / len(timeTookArr)
                # adding all problems current student tackled
                student_states.append(student_state)

        extra_context = { "student_ids": student_ids,
                          "student_states": student_states}

        return render_to_response("testProject/result.html", extra_context)

    else:

        studentModule = courseware_studentmodule.objects.filter(
                module_type = 'Problem'
            ).filter(
                course_id = course_id
            )

        students = []
        added_problem_ids = []
        problems = []

        for row in studentModule:

            # checking is a gradable problem
            if row.max_grade >= 0:

                # students enrolled on the course
                student_id = row.student_id

                # checking that there are no repetitions
                if not any(student_id in s for s in enumerate(students)):

                    students.append(student_id)

                if not any(row.module_id in s for s in enumerate(added_problem_ids)) and row.max_grade > 0:
                    added_problem_ids.append(row.module_id)
                    # information about gradable problems in the course
                    problem = {}
                    problem["problem_id"] = row.module_id
                    problem["max_grade"] = row.max_grade

                    problems.append(problem)
        """
        # testing long list of students
        for i in range(0,100):
            students.append(i)
        """
        extra_context = { "course_id": course_id,
                          "students": students,
                          "problems": problems}

        return render_to_response("testProject/courses/view_course.html", extra_context,
                               context_instance=RequestContext(request))