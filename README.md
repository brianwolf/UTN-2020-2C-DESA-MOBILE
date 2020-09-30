# UTN Desarrollo Mobile

> Backend **python** desplegada en **heroku**

Utilizada para el tp de la materia Desarrollo Mobile

---

## Heroku

La aplicacion se encuentra desplegada en [este link](https://utn-2020-2c-desa-mobile.herokuapp.com/)

---

## Proxy a Themoviedb

El proyecto hace proxy a la API de la pagina [themoviedb](https://www.themoviedb.org/)
Documentacion de la API [aca](https://developers.themoviedb.org/3/getting-started/introduction)

- Un ejemplo seria el siguiente:
[https://utn-2020-2c-desa-mobile.herokuapp.com/proxy/v1/themoviedb/movie/550](https://utn-2020-2c-desa-mobile.herokuapp.com/proxy/v1/themoviedb/movie/550)

Todo lo que halla luego de **/proxy/v1/themoviedb** es lo que se envia a la API agregandole un query param para la *apikey* y otra para el idioma
