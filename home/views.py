from django.shortcuts import render
from .models import Departure, Delivery

# Create your views here.
def home(request):
    return render(request,'home.html')


# def services(request):
#     departure_cities = Departure.objects.all()
#     delivery_cities = Delivery.objects.all()
#     return render(request, 'services.html',
#                   {'departure_cities': departure_cities, 'delivery_cities': delivery_cities})


from django.shortcuts import render, redirect
from .models import Departure, Delivery, UserInput

def services(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_type = request.POST.get('product_type')
        departure_id = request.POST.get('departure')
        delivery_id = request.POST.get('delivery')

        # Retrieve Departure and Delivery objects
        departure_city = Departure.objects.get(pk=departure_id)
        delivery_city = Delivery.objects.get(pk=delivery_id)

        # Create UserInput instance
        user_input = UserInput.objects.create(
            user=user,
            name=name,
            email=email,
            product_type=product_type,
            departure=departure_city,
            delivery=delivery_city
        )
        user_input.save()

        # Redirect to a success page or render another template
        return redirect('home:home')  # You need to define the URL name for the success page in your urlpatterns

    else:
        departure_cities = Departure.objects.all()
        delivery_cities = Delivery.objects.all()
        return render(request, 'services.html',
                      {'departure_cities': departure_cities, 'delivery_cities': delivery_cities})




