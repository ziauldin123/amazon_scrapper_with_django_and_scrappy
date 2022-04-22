from http import HTTPStatus
from urllib.parse import urlparse
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from scrapyd_api import ScrapydAPI
from main.models import ScrapyItem
from scrapper import *

scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False

    return True


class SchedulingError(Exception):
    def __str__(self):
        return 'scheduling error'

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    try:
        amazon = Scraper()
        amazon.search("huggies")
    except Exception as e:
        print(e)
    if request.method == 'POST':

        try:
            amazon = Scraper()
            amazon.search("huggies")
        except SchedulingError as e:
            return JsonResponse(
                {'error': e},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
    elif request.method == 'GET':
        try:
            task_id = request.GET.get('task_id', None)
        except ValueError as e:
            return JsonResponse(
                {'error': e},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            unique_id = request.GET.get('unique_id', None)[:-1]
        except ValueError as e:
            return JsonResponse(
                {'error': e},
                status=HTTPStatus.BAD_REQUEST
            )
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                item = ScrapyItem.objects.filter(unique_id=unique_id)
                if not item:
                    return JsonResponse(
                        {'error': 'There is no data'},
                        status=HTTPStatus.NOT_FOUND
                    )
                dict_list = []
                for i in list(item):
                    dict_data = {
                        'url': i.url,
                        'title': i.title,
                        'contents': i.contents,
                        'published_date': i.published_date.strftime('%Y-%m-%d %H:%M'),
                        'views': i.views,
                        'recommends': i.recommends,
                        'date': i.date.strftime('%Y-%m-%d %H:%M')
                    }
                    dict_list.append(dict_data)
                data = {'data': dict_list}
                return JsonResponse(data)
            except Exception as e:
                return JsonResponse(
                    {'error': str(e)},
                )
        else:
            return JsonResponse({'status': status})


def show_data(request):
    category = request.GET.get('category', None)
    item = ScrapyItem.objects.filter(category=category)
    if not item:
        return JsonResponse(
            {'error': 'There is no data in database'},
            status=HTTPStatus.NOT_FOUND
        )
    dict_list = []
    for i in list(item):
        dict_data = {
            'url': i.url,
            'title': i.title,
            'contents': i.contents,
            'published_date': i.published_date.strftime('%Y-%m-%d %H:%M'),
            'views': i.views,
            'recommends': i.recommends,
            'date': i.date.strftime('%Y-%m-%d %H:%M')
        }
        dict_list.append(dict_data)
    data = {'data': dict_list}
    return JsonResponse(data)
