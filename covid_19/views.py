from django.shortcuts import render
from django.views.generic import TemplateView
from campaign.models import VaccineCampaign
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        campaigns = VaccineCampaign.objects.all().order_by('-campaign_name')
        # reviews = Review.objects.all()
       
        p = Paginator(campaigns,3) 
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number) 
        totalpage = page_obj.paginator.num_pages
        # lastpage = page_obj.paginator.num_pages 

        context = {
            # "campaigns":campaigns, 
            # "reviews": reviews,
            # 'totalpage': totalpage,
            'page_obj': page_obj,
            'totalPagelist': [n+1 for n in range(totalpage)]
        }
        return render(request, self.template_name, context)

def about(request):
    return render(request, "about_us.html")

def info(request):
    return render(request, "info.html")




######################################################################################
# def index(request):
# 	campaigns = VaccineCampaign.objects.all() # fetching all post objects from database
# 	p = Paginator(campaigns, 2) # creating a paginator object
# 	# getting the desired page number from url
# 	page_number = request.GET.get('page')
# 	try:
# 		page_obj = p.get_page(page_number) # returns the desired page object
        
# 	except PageNotAnInteger:
# 		# if page_number is not an integer then assign the first page
# 		page_obj = p.page(1)
# 	except EmptyPage:
# 		# if page is empty then return last page
# 		page_obj = p.page(p.num_pages)
# 	context = {
#         'page_obj': page_obj,
#         'totalPagelist': [n+1 for n in range(p.num_pages)]
#         }
# 	# sending the page object to index.html
# 	return render(request, 'index.html', context)



# class HomeView(TemplateView):
#     template_name = 'index.html'
#     paginate_by = 2

#     def get(self, request, *args, **kwargs):
#         campaigns = VaccineCampaign.objects.all().order_by('-campaign_name')
#         paginator = Paginator(campaigns, self.paginate_by)
        
#         page_number = request.GET.get('page')
#         try:
#             page_obj = paginator.page(page_number)
#         except EmptyPage:
#             # If page is out of range, deliver last page of results
#             page_obj = paginator.page(paginator.num_pages)

#         context = {
#             'page_obj': page_obj,
#             'totalPagelist': [n+1 for n in range(paginator.num_pages)]
#         }
#         return render(request, self.template_name, context)
