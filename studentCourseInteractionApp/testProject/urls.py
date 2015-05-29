from django.conf.urls import patterns, include, url
from testProject import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.courses, name='index'),
    #url(r'^state/', views.state),
    url(r'^courses/all_courses/', views.courses),
    url(r'^courses/view_course/(?P<course_id>.+)$', views.specifiedCourse),
    url(r'^courses/view_student/(?P<course_id>.+)&(?P<student_id>.+)$', views.specifiedCourse)
    #url(r'^$', 'testProject.views.home', name='home'),
    # url(r'^testProject/', include('testProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
