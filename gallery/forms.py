from django import forms
from .models import Photo, Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Album Name (e.g., Summer Vacation)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Description (optional)'
            }),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'album']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Photo Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Photo Description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'album': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter albums to only show those owned by the current user
        if user:
            self.fields['album'].queryset = Album.objects.filter(owner=user)
