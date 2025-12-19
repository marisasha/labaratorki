from .start import router as start_router
from .get_weather import router as weather_router
from .get_humindity import router as humindity_router
from .get_wind import router as wind_router

all_routers = [
    start_router,
    weather_router,
    humindity_router,
    wind_router
]