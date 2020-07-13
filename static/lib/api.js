import { APP_KEY } from "../key/appKey.js";

const API_HOST = "https://api.themoviedb.org/3";

export const getPopularMovieAPI = () => {
  return fetch(
    `${API_HOST}/discover/movie?sort_by=popularity.desc&api_key=${APP_KEY}&language=ko-KR`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }
  ).then(response => response.json());
};

export const getGenresAPI = () => {
  return fetch(
    `${API_HOST}/genre/movie/list?api_key=${APP_KEY}&language=ko-KR`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }
  ).then(response => response.json());
};

export const getGenreContentsAPI = (genre, date) => {
  return fetch(
    `${API_HOST}/discover/movie?with_genres=${
      genre.id
    }&primary_release_year=${date.getFullYear()}&api_key=${APP_KEY}&language=ko-KR`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }
  ).then(response => response.json());
};
