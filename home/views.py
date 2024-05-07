from django.shortcuts import render,redirect,get_object_or_404
from .models import Departure, Delivery
from django.views.generic import TemplateView,CreateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from .utils import train_model, make_prediction



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

from datetime import timedelta
from django.utils import timezone

class MyShipment(TemplateView):
    template_name="shipments.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch UserInput objects for the current user
        user_inputs = UserInput.objects.filter(user=self.request.user.id)
        print(user_inputs)
        # Calculate difference in days for each UserInput object
        for user_input in user_inputs:
            try:
                current_time = timezone.now()
                print("Current Time:", current_time)
                print(user_input.date)
                difference =  current_time - user_input.date
                print('diff',difference.days)
                
                prediction = round(float(user_input.prediction))
                
                # print(prediction)
                a =prediction - int(difference.days) 
                user_input.prediction = a
                
                expected_delivery_date = user_input.date + timedelta(days=prediction)
                print(expected_delivery_date)
                user_input.expected_date=expected_delivery_date
                user_input.save()
            except:
                print("Prediction does not exist")
        context["data"] = user_inputs
        context["ship"] = Predict.objects.filter(user=self.request.user.id)
        return context


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
    print(user)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_type = request.POST.get('product_type')
        departure_id = request.POST.get('departure')
        delivery_id = request.POST.get('delivery')
       
        departure_city = Departure.objects.get(pk=departure_id)
        delivery_city = Delivery.objects.get(pk=delivery_id)
        feed=Feedback.objects.all()

        user_input = UserInput.objects.create(
            user=user,
            name=name,
            email=email,
            product_type=product_type,
            departure=departure_city,
            delivery=delivery_city,   
        )
        user_input.save()

        return redirect('home:ship')  
    else:
        departure_cities = Departure.objects.all()
        delivery_cities = Delivery.objects.all()
        feed = Feedback.objects.all()
        return render(request, 'home.html',{'departure_cities': departure_cities, 'delivery_cities': delivery_cities,'feed':feed,'user':user})


# def services(request):
#     departure_cities = Departure.objects.all()
#     delivery_cities = Delivery.objects.all()
#     return render(request, 'services.html',
#                   {'departure_cities': departure_cities, 'delivery_cities': delivery_cities})


def services(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_type = request.POST.get('product_type')
        departure_id = request.POST.get('departure')
        delivery_id = request.POST.get('delivery')

        departure_city = Departure.objects.get(pk=departure_id)
        delivery_city = Delivery.objects.get(pk=delivery_id)

        user_input = UserInput.objects.create(
            user=user,
            name=name,
            email=email,
            product_type=product_type,
            departure=departure_city,
            delivery=delivery_city
        )
        user_input.save()
        return redirect('home:home')     
    else:
        departure_cities = Departure.objects.all()
        delivery_cities = Delivery.objects.all()
        return render(request, 'services.html',{'departure_cities': departure_cities, 'delivery_cities': delivery_cities})



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

    obj.prediction = prediction[0]

    # Save the object
    obj.save()

    return redirect('home:ship')
    # elif request.method == "GET":
    #     # Handle GET requests here, render a template or return a redirect
    #     return redirect('home:home')  # Redirect to some other view or URL

from django.http import HttpResponse

def track_shipments(request, **kwargs):
    # if request.method == 'POST':
        # try:
            id = kwargs.get('pk')
            
            print(id)
            shipments = UserInput.objects.get(id=id)
            print(shipments)
            days = Predict.objects.get(shipment=id)
            total = int(round(float(days.prediction))) / 4
            
            if shipments.prediction == total * 4:
                shipments.status = 'Order Confirmed'
            elif shipments.prediction == total * 3:
                shipments.status = 'Processing'
            elif shipments.prediction == total * 2:
                shipments.status = 'Shipped'
            elif shipments.prediction == total:
                shipments.status == 'Out for delivery'
            elif shipments.prediction == 0:
                shipments.status = 'Delivered'
                
            shipments.save()
            return render(request, 'tracking.html', {'shipments': shipments})
        
    #     except (UserInput.DoesNotExist, Predict.DoesNotExist) as e:
    #         return HttpResponse("Shipment or Prediction not found.")
    
    # return render(request, 'tracking.html')


