from django import forms

from store.models import ProductReview
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model=ProductReview
        fields=["title","product_image","review_text","rating"]
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter review title'}),
            'product_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'review_text':forms.Textarea(attrs={'class':'form-control','placeholder':'write your review','rows':4}),
            'rating':forms.NumberInput(attrs={'class':'form-control','min':1,'max':5})
        }




    # Validation for the 'title' field
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required.")
        if len(title) < 4:
            raise forms.ValidationError("Title must be at least 4 characters long.")
        return title

    # Validation for the 'product_image' field
    def clean_product_image(self):
        product_image = self.cleaned_data.get('product_image')
        if product_image:
            if product_image.size > 100 * 1024 * 1024:  # Limit file size to 100MB
                raise forms.ValidationError("Image file size should not exceed 100MB.")
            if not product_image.content_type.startswith('image/'):
                raise forms.ValidationError("Only image files are allowed.")
        return product_image

    # Validation for the 'review_text' field
    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if not review_text:
            raise forms.ValidationError("Review text is required.")
        if len(review_text) < 10:
            raise forms.ValidationError("Review text must be at least 10 characters long.")
        return review_text

    # Validation for the 'rating' field
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    # Validation for the entire form
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        review_text = cleaned_data.get('review_text')

        if title and review_text:
            # Example of a cross-field validation
            if "bad" in review_text.lower() and "great" in title.lower():
                raise forms.ValidationError(
                    "Title and review text seem to contradict each other. Please revise your review."
                )
        return cleaned_data