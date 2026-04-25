from django.db import models


class TrafficSignClass(models.Model):
    name = models.CharField(max_length=120, unique=True)
    meaning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TrainingImage(models.Model):
    sign_class = models.ForeignKey(
        TrafficSignClass,
        related_name="training_images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="training_images/")
    feature_vector = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class DetectionHistory(models.Model):
    image = models.ImageField(upload_to="detection_images/")
    predicted_sign = models.ForeignKey(
        TrafficSignClass,
        related_name="detections",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
