from django import forms

from .models import TrafficSignClass


class TrainingUploadForm(forms.Form):
    sign_class = forms.ModelChoiceField(
        queryset=TrafficSignClass.objects.all(),
        required=False,
        empty_label="Choose existing sign class",
    )
    new_class_name = forms.CharField(max_length=120, required=False)
    meaning = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
    image = forms.ImageField()

    def clean(self):
        cleaned_data = super().clean()
        sign_class = cleaned_data.get("sign_class")
        new_class_name = (cleaned_data.get("new_class_name") or "").strip()
        meaning = (cleaned_data.get("meaning") or "").strip()

        if not sign_class and not new_class_name:
            raise forms.ValidationError(
                "Select an existing class or provide a new class name."
            )

        if new_class_name and not meaning:
            raise forms.ValidationError(
                "Provide meaning when creating a new class."
            )

        return cleaned_data


class DetectionUploadForm(forms.Form):
    image = forms.ImageField()
