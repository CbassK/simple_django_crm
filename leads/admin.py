from django.contrib import admin
from .models import (
    User,
    UserProfile,
    Agent,
    Lead
)

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)
