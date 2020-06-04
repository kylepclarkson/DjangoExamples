from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import ImageCreationForm

@login_required
def image_create(request):

    if request.method == 'POST':

        form = ImageCreationForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # Create new image (without saving to database using commit=False)
            new_item = form.save(commit=False)
            # assign item to current user
            new_item.user = request.user
            # Save to database.
            new_item.save()

            messages.success(request, 'Image added successfully')

            # redirect user to URL of new image
            return redirect(new_item.get_absolute_url())

    else:
        form = ImageCreationForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})

# @login_required
# @require_POST
# def image_like(request):
#     image_id = request.POST.get('id')
#     action = request.POST.get('action')
#
#     if image_id and action:
#         try:
#             image = Image.objects.get(id='image_id')
