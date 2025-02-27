from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mainapp import models as mainapp_models
from mainapp.models import Courses
admin.site.register(Courses)


@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    list_filter = ('deleted', 'created', 'updated')
    ordering = ('pk',)
    search_fields = ["title", "preambule", "body"]
    list_per_page = 5
    actions = ('mark_as_delete',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = _("Mark deleted")


@admin.register(mainapp_models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "get_course_name", "num", "title", "deleted"]
    ordering = ["-course__name", "-num"]
    list_per_page = 5
    list_filter = ["course", "created", "deleted"]
    actions = ["mark_deleted"]

    def get_course_name(self, obj):
        return obj.course.name

    get_course_name.short_description = _("Course")

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _("Mark deleted")


@admin.register(mainapp_models.CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "get_courses"]
    list_select_related = True

    def get_courses(self, obj):
        return ", ".join((i.name for i in obj.course.all()))

    get_courses.short_description = _("Courses")