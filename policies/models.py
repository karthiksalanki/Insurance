from django.db import models
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date,datetime
from insurance import settings
from django.core.mail import send_mail


class Policy(models.Model):
    POLICY_CHOICES = [
        ('ICICI Life', 'ICICI Life'),
        ('Max Life', 'Max Life'),
        ('HDFC Life', 'HDFC Life'),
    ]
    POLICY_STATUS_CHOICES = [
        ('Requirements Awaited', 'Requirements Awaited'),
        ('Requirements Closed', 'Requirements Closed'),
        ('Underwriting', 'Underwriting'),
        ('Policy Issued', 'Policy Issued'),
        ('Policy Rejected', 'Policy Rejected'),
    ]
    MEDICAL_TYPE_CHOICES = [
        ('Tele Medicals', 'Tele Medicals'),
        ('Physical Medicals', 'Physical Medicals'),
    ]
    MEDICAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Waiting for Report', 'Waiting for Report'),
        ('Done', 'Done'),
    ]

    policy_name = models.CharField(max_length=50, choices=POLICY_CHOICES)
    application_number = models.CharField(max_length=100, validators=[RegexValidator(regex='^[a-zA-Z0-9]*$')], unique=True)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(regex='^[0-9]{10}$')])
    date_of_birth = models.DateField()
    policy_cover = models.PositiveIntegerField(validators=[MinValueValidator(2500000), MaxValueValidator(50000000)])
    policy_status = models.CharField(max_length=50, choices=POLICY_STATUS_CHOICES)
    policy_number = models.CharField(max_length=100, blank=True, null=True)
    medical_type = models.CharField(max_length=50, choices=MEDICAL_TYPE_CHOICES, blank=True, null=True)
    medical_status = models.CharField(max_length=50, choices=MEDICAL_STATUS_CHOICES, blank=True, null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # To send Email
        if self.policy_status == 'Policy Issued' and not self.policy_number:
            raise ValidationError('Policy number is required when the policy is issued.')
        elif self.policy_status == 'Policy Issued' and self.policy_number:
            subject = 'Your Insurance Policy Has Been Issued'
            message = f'Dear {self.customer_name},\n\nYour policy has been successfully issued. Your policy number is {self.policy_number}.\n\nThank you for choosing our services.\n\nBest regards,\nDitto Insurance'
            from_email = "Ditto Insurance"
            recipient_list = [self.email]
            send_mail(subject, message, from_email, recipient_list)
        
        # To check medical type and status
        if self.policy_name in ['Max Life', 'HDFC Life'] and (not self.medical_type or not self.medical_status):
                raise ValidationError('Medical type and status are required for Max Life and HDFC Life.')
        elif self.policy_name == 'ICICI Life' and (self.medical_type and self.medical_status):
                raise ValidationError('Medical type and status are not required for ICICI Life.')
        if self.policy_name == 'Max Life' and self.remarks:
             raise ValidationError('Remarks not required for Max Life.')

        # To check age
        if self.date_of_birth:
            today = date.today()
            dob = self.date_of_birth
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18 or age > 99:
                raise ValidationError('Age should be between 18 and 99 years.')

        # To check for remarks
        if self.policy_name in ['ICICI Life', 'HDFC Life'] and not self.remarks:
            raise ValidationError('Remarks is required for ICICI Life and HDFC Life.')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'

class Comment(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='comments')   # we can use ManyToManyField(but complicated)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



