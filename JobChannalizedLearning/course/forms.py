from django import forms
from course.models import Catogaries, Course

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Catogaries
        fields = ['name', 'category_image']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['featured_image', 'video_file', 'zip_file','title', 'description', 'status']

# class ZipUploadForm(forms.Form):
#     zip_file = forms.FileField(label='Select a zip file', help_text='Max. 50 MB', widget=forms.ClearableFileInput(attrs={'multiple': True}))