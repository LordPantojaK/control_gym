import datetime
#import django.utils.timezone
from django.db import models, transaction, IntegrityError
from django.contrib import admin
from django.utils import timezone 
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
# Create your models here.

class Noticia(models.Model):
	autor = models.ForeignKey('auth.User')
	titulo = models.CharField(max_length=200)
	descripcion = models.TextField()
	fecha = models.DateTimeField(
		default = timezone.now)
	publicacion_fecha = models.DateTimeField(
		blank=True, null=True)
	def publicacion(self):
		self.publicacion_fecha = timezone.now()
		self.save()
	
	def __str__(self):
		return 'Publicada por %s con titulo %s el dia %s'%(self.autor, self.titulo,self.fecha)	

class Sucursal(models.Model):
	nombre = models.CharField(max_length=50)
	direccion = models.CharField(max_length=80)
	class Meta:
		ordering=["nombre"]
		verbose_name_plural ="Sucursales"
	def __str__(self):
		return u"%s the sucursal" % (self.nombre)
		
class Salon(models.Model):
	plaza = models.OneToOneField(Sucursal, primary_key=True)
	servicio_de_maquinas = models.BooleanField()
	servicio_de_nutricion = models.BooleanField()
	servicio_de_clase = models.BooleanField()
	class Meta:
		ordering=["plaza"]
		verbose_name_plural ="Salones"
	def __str__(self):
		return u"%s the salon" % (self.plaza.nombre)

class Membrecia(models.Model):
	aplica_en = models.ForeignKey(Salon)
	nombre = models.CharField(max_length=30)	
	precio = models.FloatField(default=0.0)
	def __str__(self):
		return u"%s por membrecia tipo %s y aplica en %s"%(self.precio, self.nombre ,self.aplica_en.plaza)			

class Miembro(models.Model):
	nombre = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	sexo = models.CharField(max_length=1,choices=(('M','Mujer'),('H','Hombre'),))
	telefono = models.CharField(max_length=10)
	correo = models.EmailField(blank=True, verbose_name='e-mail')
	domicilio = models.CharField(max_length=60)
	fecha_de_nacimimiento = models.DateField()
	salon = models.ForeignKey(Salon)
	mebrecia = models.ForeignKey(Membrecia)
	#foto = models.ImageField(upload_to = 'fotos')
	def __str__(self):
		return u"%s es miembro en %s" % (self.nombre, self.salon)	
		
class Profesor(models.Model):
	salon = models.ForeignKey(Salon)
	nombre = models.CharField(max_length=30)
	apellidos = models.CharField(max_length=40)
	telefono = models.CharField(max_length=10)
	correo = models.EmailField(blank=True, verbose_name='e-mail')
	ciudad = models.CharField(max_length=60)
	#foto = models.ImageField(upload_to = 'fotos')
	class Meta:
		ordering=["salon"]
		verbose_name_plural ="Profesores"
	def __str__(self):
		return u"%s es miembro en %s" % (self.nombre, self.salon)
		
class Clase(models.Model):
	salon = models.ForeignKey(Salon)
	nombre = models.CharField(max_length=40)
	descripcion = models.CharField(max_length=100)
	Horario = (
		('LyM', (('1', 'Lunes y Miercoles \'Matutino\''), ('2', 'Lunes y Miercoles \'Vespertino\''),)
		),
		('MyJ', (('1', 'Martes y Jueves \'Matutino\''), ('2', 'Martes y Jueves \'Vespertino\''),)
		),
		('VyS', (('1', 'Viernes y Sabado \'Matutino\''),('2', 'Viernes y Sabado \'Vespertino\''),)
		),
	)
	horario=models.CharField(max_length=50, choices=Horario)
	comienza=models.TimeField(default='00:00')
	termina=models.TimeField(default='00:00')
	profesor = models.ForeignKey(Profesor)
	miembros = models.ManyToManyField(Miembro)
	def __str__(self):
		return u'La clase de %s  impartida por %s'%(self.nombre, self.profesor.nombre)
		
class Pago(models.Model):
	Realizado_por = models.ForeignKey('auth.User')
	cliente = models.ForeignKey(Miembro, on_delete=models.CASCADE)
	precio = models.ForeignKey(Membrecia)
	fecha_de_pago = models.DateTimeField(
		default = timezone.now)
	fecha_de_vencimiento = models.DateTimeField(
		default = timezone.now() + datetime.timedelta(days=31))
	class Meta:
		ordering=["fecha_de_vencimiento"]
		
	def __str__(self):
		return 'El cliente %s pago %s y tiene vigencia desde %s hasta %s'%(self.cliente.nombre, self.precio, self.fecha_de_pago,self.fecha_de_vencimiento)