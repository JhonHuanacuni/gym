from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, MembresiaViewSet, AsistenciaViewSet
from .views_dashboard import DashboardStatsView


router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'membresias', MembresiaViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),

]
