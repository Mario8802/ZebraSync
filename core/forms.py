from django import forms


class ZipUploadForm(forms.Form):
    src_zip = forms.FileField(label="Upload ZIP to Synchronize")

    def clean_src_zip(self):
        file = self.cleaned_data["src_zip"]
        if not file.name.lower().endswith(".zip"):
            raise forms.ValidationError("Only .zip files are allowed.")
        return file
# test