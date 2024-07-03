from django.http import JsonResponse, HttpResponseNotAllowed
from .models import PostgresModel
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def postgres_crud(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({'error': 'Field "name" is required'}, status=400)

            obj = PostgresModel.objects.create(name=name)
            return JsonResponse({'id': obj.id, 'name': obj.name}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    elif request.method == 'GET':
        data = list(PostgresModel.objects.values())
        return JsonResponse(data, safe=False)


@csrf_exempt
def postgres_detail(request, pk):
    try:
        obj = PostgresModel.objects.get(pk=pk)
    except PostgresModel.DoesNotExist:
        return JsonResponse({'error': f'Object with id {pk} not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({'id': obj.id, 'name': obj.name})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({'error': 'Field "name" is required'}, status=400)

            obj.name = name
            obj.save()
            return JsonResponse({'id': obj.id, 'name': obj.name})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

    elif request.method == 'DELETE':
        try:
            obj.delete()
            return JsonResponse({'message': 'Object deleted successfully!'})

        except PostgresModel.DoesNotExist:
            return JsonResponse({'error': f'Object with id {pk} not found'}, status=404)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])