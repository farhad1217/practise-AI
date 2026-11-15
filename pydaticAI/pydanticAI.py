from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, field_validator, model_validator, Field, computed_field
from rich import print
load_dotenv()

class MovieDetail(BaseModel):
    name: str = Field(description="movie name")
    release_date: int = Field(description="movie release date. if no movie found fill with -1")
    cast: list[str] = Field(description="movie cast name")
    budget: float = Field(description="total budjet of the movie", strict=True)
    box_office: float = Field(description="box office of the movie", strict=True)
    movie_type: str = Field(description="movie after release 1999 is modern else classic")

    @field_validator("name")
    @classmethod
    def upper_name(cls, value:str)->str:
        return value.upper()

    @model_validator(mode="after")
    def movieType(self)->"MovieDetail":
        if self.release_date >= 2000 and self.movie_type.lower() == "classic":
            raise ValueError("movie will be modern")
        if self.release_date < 2000 and self.movie_type.lower() == "modern":
            raise ValueError("movie will be classic")
        return self


    @computed_field
    @property
    def netProfit(self)->float:
        net_profit = self.box_office - self.budget
        return net_profit

model = init_chat_model("google_genai:gemini-3.1-flash-lite")
messages = [SystemMessage(content="you are a movie support assistan. fill the model with each movie your are asked about")]

structure_output = model.with_structured_output(MovieDetail)
print("Ask any movie related question. Type exit to quit.")
while True:
    prompt = input("YOU: ")
    if prompt.lower() == "exit":
        break
    messages.append(HumanMessage(prompt))
    result = structure_output.invoke(messages)
    if result.release_date == -1:
        print("Movie not found!")
    else:
        print(result)
    messages.append(AIMessage(content="Movie not found!"))

print(messages)