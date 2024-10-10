import os.path
from contextlib import asynccontextmanager
from typing import List, Annotated

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Field, Session, select

home_dir = os.path.expanduser('~')
db_path = os.path.join(home_dir, ".yoda", 'yoda.sqlite3')

connect_args = {"check_same_thread": False}
engine = create_engine(f'sqlite:///{db_path}', connect_args=connect_args)


class Plugin(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: str
    config_data: str
    is_enabled: bool


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create the database and tables before we start listening for requests
    create_db_and_tables()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/plugins", response_model=List[Plugin])
async def get_plugin_list(session: SessionDep):
    plugins = session.exec(select(Plugin)).all()
    return plugins


@app.post("/plugins", response_model=Plugin)
async def create_plugin(plugin: Plugin, session: SessionDep):
    plugin_validated = Plugin.model_validate(plugin)
    session.add(plugin_validated)
    session.commit()
    session.refresh(plugin_validated)
    return plugin_validated


@app.get("/plugins/{plugin_name}", response_model=Plugin)
async def get_plugin_details(plugin_name: str, session: SessionDep):
    plugin = session.get(Plugin, plugin_name)
    return plugin


@app.put("/plugins/{plugin_name}", response_model=Plugin)
async def update_plugin(plugin_name: str, updated_plugin: Plugin, session: SessionDep):
    current_plugin = session.get(Plugin, plugin_name) or Plugin(name=plugin_name)
    current_plugin.description = updated_plugin.description
    current_plugin.config_data = updated_plugin.config_data
    current_plugin.is_enabled = updated_plugin.is_enabled
    session.add(current_plugin)
    session.commit()
    session.refresh(current_plugin)
    return current_plugin


@app.delete("/plugins/{plugin_name}")
async def delete_plugin(plugin_name: str, session: SessionDep):
    plugin = session.get(Plugin, plugin_name)
    session.delete(plugin)
    session.commit()
    return {"message": "Plugin deleted successfully"}
