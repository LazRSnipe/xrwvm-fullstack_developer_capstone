from django.contrib import admin
from .models import CarMake, CarModel  # Correct import for CarMake and CarModel

# CarModelInline to display CarModel in CarMake Admin
class CarModelInline(admin.TabularInline):  # You can use admin.StackedInline as well
    model = CarModel
    extra = 1  # Controls the number of empty forms displayed by default

# CarModelAdmin class (optional, if you want custom admin configuration for CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  # Fields to display in the list view
    search_fields = ('name', 'car_make__name')  # Enable search by model name and car make
    list_filter = ('car_make', 'type', 'year')  # Enable filters for make, type, and year

# CarMakeAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to display in the list view
    search_fields = ('name',)  # Enable search by car make name
    inlines = [CarModelInline]  # Display related CarModel instances inline under CarMake

# Registering models with their corresponding admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)  # Optional: Only if you need to customize CarModel in the admin
