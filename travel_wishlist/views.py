from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


# Create your views here.
@login_required()
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save(commit=False)
        place.user = request.user
        # creating a model object from form
        if form.is_valid():  # validation against DB constraints for example, are required fields present?
            place.save()  # saves places to db
            return redirect('place_list')  # redirects to get view with name place_list- which is this same view

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by(
        'name')  # this will give a list of objects
    new_place_form = NewPlaceForm
    return render(request, 'travel_wishlist/wishlist.html',
                  {'places': places, 'new_place_form': new_place_form})


@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)  # This is a database query
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    # return redirect('places_visited')
    return redirect('place_list')  # place_list is the name of the path


@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html',
                  {'visited': visited})


@login_required()
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # return render(request, 'travel_wishlist/place_detail.html', {'place': place})

    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # instance is the model object to update with the form data

        if form.is_valid():
            form.save()  # the form represents the new information the user has entered
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # Temp error message - future version improve

        return redirect('place_details', place_pk=place_pk)

    else:  # GET place details
        # if GET request, show Place info and optional form.
        # if place is visited, show form; if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)  # Pre-populate with data form this place instance
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

    # is this a GET request (show Data + form), or a POST request (update Place object)?

    # if POST request, validate form data and update.


#  if request.method == 'POST':
#  form = TripReviewForm(request.POST, request.FILES, instance=place)


@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()

# def about(request):
# author = 'Adade'
# about = 'A website to create a list of places to visit'
# return render(request, 'travel_wishlist/about.html', {'author': author,
#  'about': about})
