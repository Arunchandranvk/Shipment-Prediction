from django.shortcuts import render
from .models import Departure, Delivery
from django.views.generic import TemplateView,CreateView
from .models import *
from .forms import *
from django.urls import reverse_lazy


# class FeedCreateView(CreateView):
#     template_name="feedback.html"
#     model=Feedback
#     form_class=FeedForm
#     success_url=reverse_lazy('home:home')

def FeedCreateView(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        
    
        # Create UserInput instance
        user_input = Feedback.objects.create(
            user=user,
            Name=name,
          
            message=message
        )
        user_input.save()

        # Redirect to a success page or render another template
        return redirect('home:feed')  # You need to define the URL name for the success page in your urlpatterns

    else:
        
        return render(request, 'feedback.html')
    return render(request,'feedback.html')


class MyShipment(TemplateView):
    template_name="shipments.html"
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)     
        context["data"]=UserInput.objects.filter(user=self.request.user.id)
        context["ship"]=Predict.objects.filter(user=self.request.user.id)
        return context
    
from django.http import JsonResponse

def update_days(request,**kwargs):
    if request.method == 'POST':
        days_left = int(request.POST.get('daysLeft'))
        # Update the days in the database here

        # For example:
        id=kwargs.get("pk")
        obj = UserInput.objects.get(pk=id)
        obj.prediction = days_left
        obj.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

# Create your views here.
def home(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_type = request.POST.get('product_type')
        departure_id = request.POST.get('departure')
        delivery_id = request.POST.get('delivery')
        img = request.POST.get('img')

        # Retrieve Departure and Delivery objects
        departure_city = Departure.objects.get(pk=departure_id)
        delivery_city = Delivery.objects.get(pk=delivery_id)
        feed=Feedback.objects.all()

        # Create UserInput instance
        user_input = UserInput.objects.create(
            user=user,
            name=name,
            email=email,
            product_type=product_type,
            departure=departure_city,
            delivery=delivery_city,
            img=img,
           
        )
        user_input.save()

        # Redirect to a success page or render another template
        return redirect('home:home')  # You need to define the URL name for the success page in your urlpatterns

    else:
        departure_cities = Departure.objects.all()
        delivery_cities = Delivery.objects.all()
        feed = Feedback.objects.all()
        return render(request, 'home.html',
                      {'departure_cities': departure_cities, 'delivery_cities': delivery_cities,'feed':feed})
    # return render(request,'home.html')


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






from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .utils import train_model, make_prediction

# Train the model and save it as a global variable
model, scaler = train_model()

def predict(request, **kwargs):
    # if request.method == "POST":
    id = kwargs.get("pk")
    print(id)
    data = UserInput.objects.get(id=id)
    print(data)
    print(data.departure.latitude)
    input_data = [
        data.departure.latitude, data.departure.longitude,
        data.delivery.latitude, data.delivery.longitude,
        data.weather_conditions, data.multiple_deliveries,
        data.festival
    ]
    prediction = make_prediction(model, scaler, input_data)

    feed =Predict(prediction = prediction[0],user=data.user.id,shipment=id)
    feed.save()
    print(prediction)
    obj = get_object_or_404(UserInput, pk=data.id)

    # Predict the value
    # predicted_value = predict_value()

    # Add the predicted value to the corresponding row
    pred=prediction-18
    obj.prediction = pred[0]

    # Save the object
    obj.save()

    return redirect('home:home')
    # elif request.method == "GET":
    #     # Handle GET requests here, render a template or return a redirect
    #     return redirect('home:home')  # Redirect to some other view or URL

