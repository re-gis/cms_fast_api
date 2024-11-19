from fastapi import FastAPI
from cms.auth.views import router as auth_router
from cms.projects.views import router as projects_router
from cms.volunteers.views import router as volunteers_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(volunteers_router, prefix="/volunteers", tags=["Volunteers"])
