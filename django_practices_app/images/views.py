from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from .forms import ImageForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.info('Index view was called')
    image_list = Image.objects.all()
    context = {'image_list': image_list}
    return render(request, 'images/index.html', context)

def detail(request, image_id):
    logger.info(f'Detail view was called for image with id = {image_id}')
    try:
        image = get_object_or_404(Image, id=image_id, is_active=True)
    except Http404:
        logger.warning(f'Image with id = {image_id} not found')
        raise
    logger.info(f'Image with id = {image_id} found')
    context = {'image': image}
    return render(request, 'images/detail.html', context)

def delete(request, image_id):
    logger.info(f'Trying to delete image with id = {image_id}')
    try:
        image = get_object_or_404(Image, id=image_id)
    except Http404:
        logger.warning(f'Image with id = {image_id} can not be deleted, because not exist')
        raise
    image.delete()
    logger.info(f'Image with id = {image_id} correctly deleted')
    return redirect('images:index')

def upload(request):
    if request.method == 'POST':
        logger.info('Upload view called with POST method')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info('Image correctly saved in Database')
            return redirect('images:index')
        logger.warning('Form not validated and image not saved')
    else:
        logger.info('Upload view called with GET method')
        form = ImageForm()

    return render(request, 'images/upload.html', {'form': form})
