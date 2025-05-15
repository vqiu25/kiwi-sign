# Kiwi Sign

<p align="center">
  <img width="450" alt="ray-tracer" src="https://github.com/user-attachments/assets/555c8a4d-794b-493c-8f97-4e70effa2cad">
</p>

## About

Kiwi Sign is a project developed for the DEVS Hackathon 2024. It utilises an ML model to recognise and interpret New Zealand Sign Language. The app features a "SignDex" (akin to a PokeDex), which records new signs when they are first observed. The SignDex is organised into categories such as Greetings, Numbers, etc.

## Features
* A dataset containing 100 images for each sign. These signs included:
  * **Alphabet**: A, B, C
  * **Numbers**: 1 - 9
  * **Days of the Week**: Monday - Sunday
  * **Greetings**: Hello, Goodbye, Thank you
  * **Terms**: Mountain, Marae, Food
* An ML model that can provide live translation from NZSL to English and Te Reo
* A SignDex, which records all hand signs recognised by the user

## Video

https://github.com/user-attachments/assets/3e283cd4-6b90-45d8-88b6-e0869671aa15

## Acknowledgements

This project was made possible by the efforts of:
* Eason Jin,
* Noah Hagar-Dent,
* Isabel Body, and
* Seif Farah

## To run the app

First `cd` into `client`, then run `python3 app.py`. This will create a Flask server, which can be used to access Kiwi Sign.
