from django.http import JsonResponse, HttpResponseNotAllowed
from .models import MongoModel
from bson import ObjectId
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def mongo_crud(request):
    if request.method == 'GET':
        data = list(MongoModel.objects.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({'error': 'Field "name" is required'}, status=400)

            obj = MongoModel.objects.create(name=name)
            return JsonResponse({'id': str(obj._id), 'name': obj.name}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def mongo_detail(request, id):
    try:
        obj = MongoModel.objects.get(_id=ObjectId(id))
    except MongoModel.DoesNotExist:
        return JsonResponse({'error': f'Object with id {id} not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': str(obj._id), 'name': obj.name})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            obj.name = name
            obj.save()
            return JsonResponse({'id': str(obj._id), 'name': obj.name})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

    elif request.method == 'DELETE':
        try:
            obj.delete()
            return JsonResponse({'message': 'Object deleted successfully!'})

        except MongoModel.DoesNotExist:
            return JsonResponse({'error': f'Object with id {id} not found'}, status=404)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
