from django.contrib import admin
from main.models import Posts
from main.models import Authors
from main.models import Comments
from main.models import Friends
from main.models import Follows

admin.site.register(Posts)
admin.site.register(Authors)
admin.site.register(Comments)
admin.site.register(Friends)
admin.site.register(Follows)
