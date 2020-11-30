# CinemApp-back

Aplicacion desarrollada en Python 3.8, su fin es la de comprar entradas de cine y recibir un código QR como comprobante para entrar al cine

![1](img/python.png)

---

## Aplicación

Utliza Python 3.8 junto con Flask y para el despliegue utiliza Unicorn, para manejar si API REST se maneja una colección de Postman con ejemplos

## Proxy a Themoviedb

El proyecto hace proxy a la API de la pagina [themoviedb](https://www.themoviedb.org/), la documentación de la API esta [aquí](https://developers.themoviedb.org/3/getting-started/introduction)

* Un ejemplo seria el siguiente:
[https://utn-2020-2c-desa-mobile.herokuapp.com/proxy/v1/themoviedb/movie/550](https://utn-2020-2c-desa-mobile.herokuapp.com/proxy/v1/themoviedb/movie/550)

Todo lo que halla luego de `/proxy/v1/themoviedb` es lo que se envia a la API agregandole un query param para la *apikey* y otra para el idioma

---

## Heroku

Está desplegado en Heroku para que sea simple de usar, el link esta [aquí](https://utn-2020-2c-desa-mobile.herokuapp.com/)

## Git Actions

Se lo utiliza para hacer un despliegue automatizado al mergear contra master, su archivo de configuración es el siguiente: `./.github/workflows/python-publish.yml`

---

## Autores

Githubs:

* [Brian Lobo](https://github.com/brianwolf)
* [Ezequiel Xifre](https://github.com/e-xifre)
* [Dante Castelluccio](https://github.com/DanteCaste)

## Facultad

Desarrollo de aplicaciones móviles 2C-2020 UTN-FRBA

![1](img/utn.jpg)
