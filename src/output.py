

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Classe(models.Model):
    nom_classe = models.CharField(primary_key=True, max_length=30)

    class Meta:
        
        db_table = 'classe'
        
class Model(models.Model):
    nom_model = models.CharField(primary_key=True, max_length=20)

    class Meta:
        
        db_table = 'model'        


class Historique(models.Model):
    id_histo = models.AutoField(primary_key=True)
    date_pred = models.DateField()
    classe_predit = models.ForeignKey(Classe,models.DO_NOTHING,related_name='classe_preditfk', db_column='classe_predit')
    precision = models.DecimalField(max_digits=5, decimal_places=2)
    classe_correcte = models.ForeignKey(Classe, models.DO_NOTHING,related_name='classe_correctefk', db_column='classe_correcte', blank=True, null=True)
    path = models.CharField(max_length=100)
    model = models.ForeignKey('Model', models.DO_NOTHING, db_column='model')

    class Meta:
        
        db_table = 'historique'
        
        
# INSERT INTO classe
# VALUES ('tarte_pomme'),('carpaccio_boeuf'),('bibimbap'),('cupcakes'),('foie_gras'),('frites'),('autre'),
# ('pain_a_l''ail'),('omelette'),('pizza'),('rouleaux_printemps'),('spaghetti_carbonara'),('gateau_framboise')
# ON CONFLICT DO NOTHING;
# INSERT INTO model
# VALUES ('model3'),('model11')
# ON CONFLICT DO NOTHING;

# SELECT setval('public.historique_id_histo_seq', 0, true);
# TRUNCATE TABLE historique;