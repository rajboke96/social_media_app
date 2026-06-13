import strawberry
from social_media_app.schemas import Country, City, State

@strawberry.type
class UserType:
    username: str
    role: str
    
@strawberry.type
class Token:
    access_token: str
    token_type: str

@strawberry.type
class CountryType:
    id: int
    name: str|None
    country_code: str|None

    @staticmethod
    def from_db(info: strawberry.Info, db_country:Country)->"CountryType":
        return CountryType(
            id=db_country.id,
            name=db_country.country,
            country_code=db_country.country_code
        )
    
    @staticmethod
    def get(info: strawberry.Info, id):
        db=info.context.db
        db_city=db.query(Country).filter(Country.id==id).first()
        if db_city:
            return db_city

@strawberry.type
class StateType:
    id: int
    name: str|None
    state_code: str|None
    country: CountryType|None

    @staticmethod
    def get(info: strawberry.Info, id):
        db=info.context.db
        db_city=db.query(State).filter(State.id==id).first()
        if db_city:
            return db_city

    @staticmethod
    def from_db(info: strawberry.Info, db_state:State)->"StateType":
        return StateType(
            id=db_state.id,
            name=db_state.state,
            state_code=db_state.state_code,
            country=CountryType.from_db(CountryType.get(info.context.db, db_state.country_id)) if db_state.country_id else None
        )

@strawberry.type
class CityType:
    id: int
    name: str|None
    city_code: str|None
    state: StateType|None

    @staticmethod
    def get(info: strawberry.Info, id):
        db=info.context.db
        db_city=db.query(City).filter(City.id==id).first()
        if db_city:
            return db_city
        
    @staticmethod
    def from_db(info: strawberry.Info, db_state:City)->"CityType":
        return CityType(
            id=db_state.id,
            name=db_state.state,
            state_code=db_state.state_code,
            state=StateType.from_db(StateType.get(info.context.db, db_state.state_id)) if db_state.state_id else None
        )