from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='eliminado',
            field=models.BooleanField(default=False, verbose_name='Eliminado'),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='eliminado_en',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Eliminado en'),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='eliminado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimientos_eliminados', to=settings.AUTH_USER_MODEL, verbose_name='Eliminado por'),
        ),
    ]
