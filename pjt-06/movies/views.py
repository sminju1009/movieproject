from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Movie, Comment, Recomment
from .forms import MovieForm, CommentForm, RecommentForm

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    recomment_form = RecommentForm()
    recomments = movie.recomment_set.all()
    context = {
        'movie': movie,
        'comment_form': comment_form,
        'comments': comments,
        'recomment_form': recomment_form,
        'recomments': recomments,
    }
    return render(request, 'movies/detail.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)

@login_required
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user==movie.user:
        movie.delete()
    return redirect('movies:index')

@login_required
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user:
        if request.method=='POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid:
                form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm(instance=movie)
    else:
        return redirect('movies:index')
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)


@login_required
def comments_create(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie': movie,
        'comment_form': comment_form,
    }
    return render(request, 'movies/detail.html', context)


@login_required
def comments_delete(request, movie_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')


@login_required
def create_recomments(request, movie_pk, comment_pk):
    movie = Movie.objects.get(pk=movie_pk)
    comment = Comment.objects.get(pk=comment_pk)
    recomment_form = RecommentForm(request.POST)
    if recomment_form.is_valid():
        recomment = recomment_form.save(commit=False)
        recomment.movie = movie
        recomment.user = request.user
        recomment.comment = comment
        recomment.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie': movie,
        'comment': comment,
        'recomment_form': recomment_form,
    }
    return render(request, 'movies:detail', context)


@login_required
def recomments_delete(request, movie_pk, comment_pk, recomment_pk):
    recomment = Recomment.objects.get(pk=recomment_pk)
    if request.user == recomment.user:
        recomment.delete()
    return redirect('movies:detail', movie_pk)