from django.contrib import admin
from nbsap.models import *

admin.site.register(Scale)

admin.site.register(AichiGoal)
admin.site.register(AichiTarget)
admin.site.register(AichiIndicator)

admin.site.register(NationalAction)
admin.site.register(NationalObjective)
admin.site.register(EuAction)
admin.site.register(EuTarget)
