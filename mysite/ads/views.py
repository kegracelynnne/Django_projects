from django.views import View
from ads.models import Ad, Comment, Fav
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from ads.forms import CreateForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q


class AdListView(OwnerListView):
    # model = Ad
    # By convention:
    # template_name = "ads/article_list.html"
    model = Ad
    template_name = "ads/ad_list.html"

    # def get(self, request) :
    #     ad_list = Ad.objects.all()
    #     favorites = list()
    #     if request.user.is_authenticated:
    #         # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
    #         rows = request.user.favorite_ads.values('id')
    #         # favorites = [2, 4, ...] using list comprehension
    #         favorites = [ row['id'] for row in rows ]
    #     ctx = {'ad_list' : ad_list, 'favorites': favorites}
    #     return render(request, self.template_name, ctx)

    def get(self, request) :
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__in=[strval]), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else :
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)


        ctx = {'ad_list' : ad_list, 'favorites' : favorites, 'search': strval}
        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     # List the fields to copy from the Ad model to the Ad form
#     fields = ['title', 'price', 'text', 'tags']
#     template_name = 'ads/ad_form.html'

# class AdUpdateView(OwnerUpdateView):
#     model = Ad
#     fields = ['title', 'text', 'tags']
#     # This would make more sense
#     # fields_exclude = ['owner', 'created_at', 'updated_at']
#     template_name = 'ads/ad_form.html'

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"
    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])

def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        ad = Fav(user=request.user, ad=t)
        try:
            ad.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            ad = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()