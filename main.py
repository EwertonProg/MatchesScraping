from fastapi import FastAPI

from hltv_controller import HltvController
from match import has_brazilian_team

app = FastAPI()
hltvController = HltvController()


@app.get("/hltv/all-games")
async def get_all_csgo_games():
    return hltvController.get_all_games()


@app.get("/hltv/all-br-games")
async def get_all_br_csgo_games():
    matches = hltvController.get_all_games()
    matches = filter(has_brazilian_team, matches)
    return list(matches)


@app.get("/hltv/all-today-games")
async def get_all_today_br_csgo_games():
    return hltvController.get_all_today_games()


@app.get("/hltv/all-today-br-games")
async def get_all_today_br_csgo_games():
    matches = hltvController.get_all_today_games()
    matches = filter(has_brazilian_team, [] if matches is None else matches)
    return list(matches)
