from django.db import models
from django.contrib.gis.db import models as gis_models
from cities.models import Region, Country, City
from multiselectfield.db.fields import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

GENDERS = (('GF', 'Genderfluid / Genderqueer'),
           ('NB', 'Non-binary'),
           ('2S', '2-Spirit'),
           ('F', 'Woman'),
           ('M', 'Man'),
           ('T', 'Trans'))

ETHNICITIES = (('AAPI', 'Asian or Pacific Islander'),
               ('B', 'Black'),
               ('L', 'Hispanic or Latinx'),
               ('I', 'Indigenous, Aboriginal, Native, Inuit, or Métis'),
               ('M', 'Multiracial or Biracial'),
               ('W', 'White'),
               ('OTH', 'A race/ethnicity not listed here'))

DISABILITIES = (('W', 'I use a wheelchair or other mobility aid'),
                ('I', 'I have an intellectual disability'),
                ('A', 'I am on the autism spectrum'),
                ('M', 'I have a mental illness'),
                ('V', 'I am vision-impaired or blind'),
                ('D', 'I am hard of hearing or deaf'),
                ('A', 'Able-bodied (no disability)'),
                ('OTH', 'Other disability not listed here'))


class DemographicSurvey(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = gis_models.PointField(null=True, blank=True)

    class IncomeBracket(models.TextChoices):
        LT_25 = 'LT_25', _('Less than $25,000 USD'),
        GT_25 = 'GT_25', _('$25,000 - $50,000 USD'),
        GT_50 = 'GT_50', _('$50,000 - $100,000 USD'),
        GT_100 = 'GT_100', _('$100,000 - $200,000 USD'),
        GT_200 = 'GT_200', _('$200,000 - $500,000 USD'),
        GT_500 = 'GT_500', _('More than $500,000 USD')

    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = MultiSelectField(choices=GENDERS, null=True, blank=True)
    income = models.CharField(max_length=6, choices=IncomeBracket.choices, default=None, null=True, blank=True)
    ethnicity = MultiSelectField(choices=ETHNICITIES, null=True, blank=True)
    disability = MultiSelectField(choices=DISABILITIES, null=True, blank=True)
    minutes_per_day_outside = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1440)])
    safe_rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    comment_experience = models.TextField(max_length=5000)


class Review(models.Model):
    # All the Review fields we will need from the survey here
    minutes_per_day = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1440)])
    score = models.PositiveSmallIntegerField()
    location = gis_models.PointField()
    comment = models.TextField(max_length=5000)

    class Meta:
        abstract = True


class TransitReview(Review):
    station_id = models.PositiveIntegerField()


class BikeReview(Review):
    safety = models.PositiveSmallIntegerField()
    noise = models.PositiveSmallIntegerField()


class CarReview(Review):
    traffic = models.PositiveSmallIntegerField()
    road_quality = models.PositiveSmallIntegerField()
