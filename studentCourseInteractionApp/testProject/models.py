from django.db import models

class student_courseenrollment(models.Model):
    id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)
    course_id = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(null=True)
    is_active = models.SmallIntegerField(max_length=1, null=True)
    mode = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'student_courseenrollment'

class auth_user(models.Model):
    id = models.IntegerField(null=False)
    email = models.TextField(null=True)

    class Meta:
        db_table = 'auth_user'

class courseware_studentmodule(models.Model):
    module_type = models.TextField(null=False)
    module_id = models.TextField(null=False)
    student_id = models.IntegerField(null=False)
    state = models.TextField(null=True)
    grade = models.DecimalField(null=True)
    created = models.DateTimeField(null=False)
    modified = models.DateTimeField(null=False)
    max_grade = models.DecimalField(null=True)
    course_id = models.TextField(null=False)

    class Meta:
        db_table = 'courseware_studentmodule'