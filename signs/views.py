from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DetectionUploadForm, TrainingUploadForm
from .models import DetectionHistory, TrafficSignClass, TrainingImage
from .services.recognizer import extract_features, predict_sign


def home(request):
    return redirect("train")


def train_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_class":
            sign_class = get_object_or_404(TrafficSignClass, pk=request.POST.get("class_id"))
            sign_class.name = (request.POST.get("class_name") or "").strip() or sign_class.name
            sign_class.meaning = (request.POST.get("class_meaning") or "").strip()
            sign_class.save(update_fields=["name", "meaning"])
            messages.success(request, f"Updated class: {sign_class.name}.")
            return redirect("train")

        if action == "delete_class":
            sign_class = get_object_or_404(TrafficSignClass, pk=request.POST.get("class_id"))
            class_name = sign_class.name
            for sample in sign_class.training_images.all():
                sample.image.delete(save=False)
            sign_class.delete()
            messages.success(request, f"Deleted class: {class_name}.")
            return redirect("train")

        if action == "delete_training_image":
            sample = get_object_or_404(TrainingImage, pk=request.POST.get("sample_id"))
            sample.image.delete(save=False)
            sample.delete()
            messages.success(request, "Training image deleted.")
            return redirect("train")

        form = TrainingUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sign_class = form.cleaned_data["sign_class"]
            class_name = (form.cleaned_data.get("new_class_name") or "").strip()
            meaning = (form.cleaned_data.get("meaning") or "").strip()

            if sign_class is None:
                sign_class, _ = TrafficSignClass.objects.get_or_create(
                    name=class_name,
                    defaults={"meaning": meaning},
                )
                if not _ and meaning and sign_class.meaning != meaning:
                    sign_class.meaning = meaning
                    sign_class.save(update_fields=["meaning"])

            image_file = form.cleaned_data["image"]
            features = extract_features(image_file)
            image_file.seek(0)

            TrainingImage.objects.create(
                sign_class=sign_class,
                image=image_file,
                feature_vector=features,
            )

            messages.success(request, "Training image saved and recognizer updated.")
            return redirect("train")
    else:
        form = TrainingUploadForm()

    recent_training = TrainingImage.objects.select_related("sign_class")[:8]
    classes = TrafficSignClass.objects.all()

    return render(
        request,
        "signs/train.html",
        {
            "form": form,
            "recent_training": recent_training,
            "classes": classes,
        },
    )


def detect_view(request):
    prediction = None
    history_entry = None

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete_detection":
            detection = get_object_or_404(DetectionHistory, pk=request.POST.get("detection_id"))
            detection.image.delete(save=False)
            detection.delete()
            messages.success(request, "Detection record deleted.")
            return redirect("detect")

        if action == "clear_detection_history":
            for detection in DetectionHistory.objects.all():
                detection.image.delete(save=False)
            DetectionHistory.objects.all().delete()
            messages.success(request, "All detection uploads were cleared.")
            return redirect("detect")

        form = DetectionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data["image"]
            result = predict_sign(image_file)
            image_file.seek(0)

            history_entry = DetectionHistory.objects.create(
                image=image_file,
                predicted_sign=result.sign_class,
                confidence=result.confidence,
            )
            prediction = result
    else:
        form = DetectionUploadForm()

    history = DetectionHistory.objects.select_related("predicted_sign")[:10]

    return render(
        request,
        "signs/detect.html",
        {
            "form": form,
            "prediction": prediction,
            "history": history,
            "history_entry": history_entry,
        },
    )
