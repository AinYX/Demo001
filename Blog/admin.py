from django.contrib import admin
from Blog import models


# Register your models here.
@admin.register(models.Article)
class AdminArticle(admin.ModelAdmin):
	list_display = ('title', 'category', 'status', 'topped', 'last_modified_time')
	list_editable = ('status', 'topped',)


admin.site.register(models.Category)
admin.site.register(models.About)
