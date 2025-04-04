# About this project

## Description

**Disclaimer: This project is still heavily work in progress. So it will not work as expected and may not work completely in some areas**

This project is my implementation of a Cloud Storage System, where you can set up a Device as your host and connect to it via the PyDrive Application for file transfer. The end goal of this project is, that a user is able to self-host a their own Cloud Storage Drive Service.

## Usage description
When calling the script we have currently the options between these commands:

| command       | usage                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------|
| init          | The init function has to be run in order to use PyDrive as it initialises the local database     |
| target add    | This command is used to add a new Drive target that you want to be able to access                |
| target remove | This command will remove a added target that has been formerly added                             |
| target list   | This command will display all the targets that you have initialised currently                    |
| target switch | Via this command you will be able to switch your PyDrive target you want to access               |

## How does the project work?

The application uses a local database to store crucial data needed to connect. Sensitive data get's will be stored salted and hashed in the database. On access request you will have to enter a password which you will be able to set on creation of the database entry via the "pydrive target add <location>" command.