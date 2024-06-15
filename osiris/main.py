from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from osiris import settings
from osiris.core.logger_setup import setup_logging
from osiris.services.auth_service.api import router as auth_router
from osiris.services.auth_service.auth_service import AuthService

TEMPLATES = Jinja2Templates(directory=settings.templates_dir)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield
    # Clean up the ML models and release the resources


app = FastAPI(title="Recipe API", openapi_url="/openapi.json", lifespan=lifespan, loglevel="debug")
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

api_router = APIRouter()
api_router.include_router(auth_router)

logger = logging.getLogger("custom")

@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

@api_router.get("/sign_in", status_code=200)
def sign_in(request: Request, service: AuthService = Depends()) -> dict:
    """
    Root GET
    """
    access_token = request.cookies.get(settings.auth_service_cookie_name)
    try:
        # ToDo Bearer access_token= - dirty hack!
        if access_token is not None and access_token.startswith("Bearer"):
            access_token = access_token.removeprefix("Bearer").strip()
            logger.info(access_token)
            service.validate_token(access_token)
            return RedirectResponse(f"/chat")

    except ValidationError:
        pass

    return TEMPLATES.TemplateResponse(
        "MainOsiris.html",
        {"request": request},
    )


@api_router.get("/sign_up", status_code=200)
def sign_in(request: Request, service: AuthService = Depends()) -> dict:
    """
    Root GET
    """
    access_token = request.cookies.get(settings.auth_service_cookie_name)
    try:
        # ToDo Bearer access_token= - dirty hack!
        if access_token is not None and access_token.startswith("Bearer"):
            access_token = access_token.removeprefix("Bearer").strip()
            logger.info(access_token)
            service.validate_token(access_token)
            return RedirectResponse(f"/chat")

    except ValidationError:
        pass

    return TEMPLATES.TemplateResponse(
        "RegistrationOsiris.html",
        {"request": request},
    )



#@api_router.get("/csrftoken/")
#async def get_csrf_token(csrf_protect:CsrfProtect = Depends()):
#	response = JSONResponse(status_code=200, content={'csrf_token':'cookie'})
#	csrf_protect.set_csrf_cookie(response)
#	return response

#@app.get("/document/{item_id}")
#async def read_document(item_id: int):
#	async with Session() as session:
#		result = await session.execute(select(Document).filter(Document.id == item_id))
#		document: Document = result.one()[0]
#	return document.as_dict()
#
#@app.post("/document/", response_class=JSONResponse)
#async def write_document(new_document: NewDocument, request: Request, csrf_protect:CsrfProtect = Depends()):
#	csrf_protect.validate_csrf_in_cookies(request)
#	async with Session() as session:
#		async with session.begin():
#			document = Document(name=new_document.name, bodytext=new_document.body, tags=",".join(new_document.tags))
#			session.add(document)
#	return JSONResponse(status_code=200, content=document.as_dict())

#@app.exception_handler(CsrfProtectError)
#def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
#  return JSONResponse(status_code=exc.status_code, content={ 'detail':  exc.message })



app.include_router(api_router)

if __name__ == "__main__":
    # TODO: migration mechanism?
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")