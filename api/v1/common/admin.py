from django.contrib import admin

from .models import User,Profile,Property,PropertyDocuments,PropertyImages,Soldproperties,Ratings,Soldproperties,Invoice,Transactions,KycDocuments
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(KycDocuments)
admin.site.register(Property)
admin.site.register(PropertyDocuments)
admin.site.register(PropertyImages)
admin.site.register(Soldproperties)
admin.site.register(Ratings)
admin.site.register(Invoice)
admin.site.register(Transactions)
