from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

@app.get('/', tags = ['home'] )

def home():
    return "Hello World"

@app.get('/movies', tags = ['movies'] )

def get_movies():
    return movies

@app.post('/movies', tags = ['movies'])

def create_movie (id: int = Body(), 
                  title: str= Body(), 
                  overview: str = Body(), 
                  year: int = Body(), 
                  rating: float = Body(), 
                  category: str = Body()):
    movies.append ({
        'id': id,
        'title': title,
        'overview': overview,
       ' year': year,
       'rating': rating,
       'category': category
})
    return movies

@app.put('/movies/{id}', tags = ['movies'])

def update_movie (id: int,
                  title: str= Body(), 
                  overview: str = Body(), 
                  year: int = Body(), 
                  rating: float = Body(), 
                  category: str = Body()
):
    for movie in movies :
        if movie ['id'] == id:
            movie ['title'] = title
            movie ['overview'] = overview
            movie ['year'] = year
            movie ['rating'] = rating
            movie ['category'] = category
    return movies

@app.delete('/movies/{id}', tags = ['movies'])

def delete_movie(id: int):
    for movie in movies :
        if movie ['id'] == id:
            movies.remove(movie)
    return movies