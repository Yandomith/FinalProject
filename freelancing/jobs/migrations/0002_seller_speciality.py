# Generated by Django 5.0.6 on 2024-06-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='speciality',
            field=models.CharField(choices=[('Computer systems manager', 'Computer systems manager'), ('Data analyst', 'Data analyst'), ('Data scientist', 'Data scientist'), ('Database administrator', 'Database administrator'), ('Digital marketing specialist', 'Digital marketing specialist'), ('Full stack developer', 'Full stack developer'), ('Graphic designer', 'Graphic designer'), ('IT consultant', 'IT consultant'), ('Network administrator', 'Network administrator'), ('Software engineer', 'Software engineer'), ('Web developer', 'Web developer'), ('Data analyst', 'Data analyst'), ('UX/UI designer', 'UX/UI designer'), ('Java developer', 'Java developer'), ('Python developer', 'Python developer'), ('Cybersecurity specialist', 'Cybersecurity specialist'), ('Artificial intelligence engineer', 'Artificial intelligence engineer'), ('Machine learning engineer', 'Machine learning engineer'), ('Help desk support specialist', 'Help desk support specialist'), ('Customer service representative', 'Customer service representative'), ('Salesforce developer', 'Salesforce developer'), ('Game Developer', 'Game Developer'), ('Animator', 'Animator'), ('3D modeler', '3D modeler'), ('Video Editor', 'Video Editor'), ('Student(amateur)', 'Student(amateur)')], default='Amateur(Learning)', max_length=50),
        ),
    ]
