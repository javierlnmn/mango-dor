from django.db import models

class Nationality(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} ({self.code})'

    class Meta:
        verbose_name_plural = 'Nationalities'

class Gender(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} ({self.code})'

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    nationality = models.ManyToManyField(Nationality)
    description = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    linkedin_profile = models.URLField(max_length=200, null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)
    
    @property
    def nationalities(self):
        return ", ".join(nationality.name for nationality in self.nationality.all())
    
    @property
    def main_image(self):
        for image in self.images.all():
            if image.main_image:
                return image
        return None

    def __str__(self):
        return f'{self.name} {self.surname}, {self.age}'
    

class CandidateImage(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='candidate_images/')
    main_image = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        
        if not self.main_image:

            main_image = CandidateImage.objects.filter(
                candidate=self.candidate,
                main_image=True
            ).exclude(
                id=self.id
            )

            if not main_image:
                self.main_image = True
                        
        else:

            main_images = CandidateImage.objects.filter(
                main_image=True
            ).exclude(
                id=self.id
            )

            super(CandidateImage, self).save(*args, **kwargs)
            
            for image in main_images:
                image.main_image = False
                image.save()

            return
        
        super(CandidateImage, self).save(*args, **kwargs)


    def __str__(self):
        return f"Image for {self.candidate.name} {self.candidate.surname}"