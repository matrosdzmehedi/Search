from django.views.generic import FormView,TemplateView
from .forms import Myform
from .models import *
from django.db.models import Count
import urllib 
from django.http import JsonResponse
from datetime import datetime, timedelta
import json

class HomeView(FormView):
    template_name = 'home.html'
    form_class = Myform
    success_url ='/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['search_result_count'] = Search.objects.values('search_keyword').filter(search_result__isnull=False).annotate(Count('search_result')).order_by('-search_result__count')
        context['username'] = Search.objects.values('username').distinct()
        return context




class Filterview(TemplateView):
    def get(self, request, *args, **kwargs):
        search_list = []
        full_url= request.build_absolute_uri()
        url_list = full_url.split('?')[1].split('&')
        main_keyword,main_username,week = False,False,False

        

        for i in url_list:
            if 'keyword+' in i:
                x =i.split('+')[1]
                main_keyword= urllib.parse.unquote(x)
                search_list.append('keyword')  
            
            if 'uname+' in i:
                x =i.split('+')[1]
                main_username= urllib.parse.unquote(x)
                search_list.append('username')
            
            if 'week' in i: 
                search_list.append('week')
            
            if 'month' in i :
                search_list.append('month')
            
            if 'yesterday' in i:
                search_list.append('yesterday')
                
        
        if len(search_list) == 1:
            if search_list[0] == 'keyword':
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword)
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
                
            elif search_list[0] == 'username':
                search_result = Search.objects.filter(username__icontains=main_username)
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            elif search_list[0] == 'week':
                search_result = Search.objects.filter(created__gte=datetime.now()-timedelta(days=7))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            elif search_list[0] == 'month':
                search_result = Search.objects.filter(created__gte=datetime.now()-timedelta(days=30))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            elif search_list[0] == 'yesterday':
                search_result = Search.objects.filter(created__lte=datetime.now())
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
        
        if len(search_list)== 2:
            if 'keyword' in search_list and 'username' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,username__icontains=main_username)
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'keyword' in search_list and 'week' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,created__gte=datetime.now()-timedelta(days=7))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'username' in search_list and 'week' in search_list:
                search_result = Search.objects.filter(username__icontains=main_username,created__gte=datetime.now()-timedelta(days=7))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'keyword' in search_list and 'month' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,created__gte=datetime.now()-timedelta(days=30))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'username' in search_list and 'month' in search_list:
                search_result = Search.objects.filter(username__icontains=main_username,created__gte=datetime.now()-timedelta(days=30))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'keyword' in search_list and 'yesterday' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,created__lte=datetime.now())
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'username' in search_list and 'yesterday' in search_list:
                search_result = Search.objects.filter(username__icontains=main_username,created__lte=datetime.now())
                data = search_result.values()
                return JsonResponse(list(data), safe=False)

        if len(search_list)== 3:
            if 'keyword' in search_list and 'username' in search_list and 'week' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,username__icontains=main_username,created__gte=datetime.now()-timedelta(days=7))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'keyword' in search_list and 'username' in search_list and 'month' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,username__icontains=main_username,created__gte=datetime.now()-timedelta(days=30))
                data = search_result.values()
                return JsonResponse(list(data), safe=False)
            
            if 'keyword' in search_list and 'username' in search_list and 'yesterday' in search_list:
                search_result = Search.objects.filter(search_keyword__icontains=main_keyword,username__icontains=main_username,created__lte=datetime.now())
                data = search_result.values()
                return JsonResponse(list(data), safe=False)



    def post(self,request,*args,**kwargs):
        
        json_data = json.loads(request.body)
        start,end=json_data['from'],json_data['to']
        search_result = Search.objects.filter(created__gte=start,created__lte=end)
        data = search_result.values()
        return JsonResponse(list(data), safe=False)

    