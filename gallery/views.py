from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
import cloudinary.uploader


# ========== ALBUM VIEWS ==========

class AlbumListView(LoginRequiredMixin, ListView):
    """Display all albums owned by the logged-in user."""
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 12
    login_url = 'login'
    
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    """Create a new album."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Album created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})


class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Display album details and its photos."""
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the album owner."""
        album = self.get_object()
        return album.owner == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['photo_form'] = PhotoForm(user=self.request.user)
        return context


class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an album."""
    model = Album
    form_class = AlbumForm
    template_name = 'gallery/album_form.html'
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the album owner."""
        album = self.get_object()
        return album.owner == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Album updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete an album."""
    model = Album
    template_name = 'gallery/album_confirm_delete.html'
    success_url = reverse_lazy('album_list')
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the album owner."""
        album = self.get_object()
        return album.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Album deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ========== PHOTO VIEWS ==========

class PhotoCreateView(LoginRequiredMixin, CreateView):
    """Create a new photo in an album."""
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'
    login_url = 'login'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Verify user owns the selected album
        album = form.instance.album
        if album.owner != self.request.user:
            messages.error(self.request, 'You do not have permission to add photos to this album.')
            return self.form_invalid(form)
        messages.success(self.request, 'Photo uploaded successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a photo."""
    model = Photo
    form_class = PhotoForm
    template_name = 'gallery/photo_form.html'
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the photo owner."""
        photo = self.get_object()
        return photo.owner == self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Photo updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a photo from an album."""
    model = Photo
    template_name = 'gallery/photo_confirm_delete.html'
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the photo owner."""
        photo = self.get_object()
        return photo.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        photo = self.get_object()
        album_pk = photo.album.pk
        
        # Delete from Cloudinary if image exists
        if photo.image:
            try:
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception as e:
                print(f"Cloudinary deletion failed: {e}")
        
        messages.success(request, 'Photo deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})


class PhotoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Display a single photo in detail."""
    model = Photo
    template_name = 'gallery/photo_detail.html'
    context_object_name = 'photo'
    login_url = 'login'
    
    def test_func(self):
        """Ensure user is the photo owner or album owner."""
        photo = self.get_object()
        return photo.owner == self.request.user or photo.album.owner == self.request.user


# ========== LEGACY COMPATIBILITY VIEW (for backward compatibility) ==========

@login_required(login_url='login')
def gallery_view(request):
    """Legacy view - redirects to album list."""
    return redirect('album_list')