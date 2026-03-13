# Project Proposal

This project proposal has been revised to remove features that were originally proposed but cut.

## Get Started

The project is to be a discord bot to allow users to challenge each other to board games. For an initial proof-of-concept, the bot will only be capable of the [Kalah(6,4) Mancala game](https://en.wikipedia.org/wiki/Kalah), although the option will be left open to extend it to e.g. Reversi, Checkers, or Chess. 

|            | Description                                                                                                                                                                                                                                                                                                                                              | Answer |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| Tech Stack | What tech stack will you use for your final project? It is recommended to use the following technologies in this project: Python/Flask, PostgreSQL, SQLAlchemy, Heroku, Jinja, RESTful APIs, JavaScript, HTML, CSS. Depending on your idea, you might end up using WTForms and other technologies discussed in the course.                               | The planned tech stack for the bot portion of this project is a discord bot using discord.py. Games in progress will be stored on a server which the bot will connect to via an API that may be RESTful, using an SQLAlchemy database to hold state.|
| Type       | Will this be a website? A mobile app? Something else?                                                                                                                                                                                                                                                                                                    | The plan here is for this to be a discord bot |
| Goal       | What goal will your project be designed to achieve?                                                                                                                                                                                                                                                                                                      | The goal is to allow people to challenge their friends to board games |
| Users      | What kind of users will visit your app? In other words, what is the demographic of your users?                                                                                                                                                                                                                                                           | Discord users who are board game enthusiasts |
| Data       | What data do you plan on using? How are you planning on collecting your data? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. You are welcome to create your own API and populate it with data. If you are using a Python/Flask stack, you are required to create your own API. | We'll be storing data about past and in-progress games: who challenged who, when, who the winner was; we'll also be storing each move as a database row. Board states for in-progress games can be reconstructed from their move history as needed. |

# Breaking down your project

- Design the discord bot (command syntax, etc)
- Design the database schema
- Build the discord bot
- Build the back end
- Deploy back end

Things to find out:
- Can discord API get profile pictures for users?

Notes on challenges:
- Have to learn discord API/discord.py library (hardest task on the project)
- Determine how much the bot depends on its back end site
- Designing the database schema: First time designing a schema whole-cloth, starting with turning subjective information (game state) into quantified data; determine what needs to be quantified and stored and what can be reconstructed
- Deployment; my experience here is shallow but I need to learn it and it seems pretty simple from what I've done. the companies offering services to deploy on want those services used.

This project involves tasks working on both the front and back ends, but very little that's full stack in a single task. Some full-stack tasks might come up as the discord bot is developed.

The proposal here is mostly minimum must-haves. Stretch goals might include the above-mentioned other games, and a web access to records of past games and perhaps ongoing games.

## Labeling

(I didn't use this section)

Labeling is a great way to separate out your tasks and to track progress. Here’s an [example](https://github.com/hatchways/sb-capstone-example/issues) of a list of issues that have labels associated.

| Label Type    | Description                                                                                                                                                                                                                                                                                                                     | Example                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Difficulty    | Estimating the difficulty level will be helpful to determine if the project is unique and ready to be showcased as part of your portfolio - having a mix of task difficultlies will be essential.                                                                                                                               | Easy, Medium, Hard           |
| Type          | If a frontend/backend task is large at scale (for example: more than 100 additional lines or changes), it might be a good idea to separate these tasks out into their own individual task. If a feature is smaller at scale (not more than 10 files changed), labeling it as fullstack would be suitable to review all at once. | Frontend, Backend, Fullstack |
| Stretch Goals | You can also label certain tasks as stretch goals - as a nice to have, but not mandatory for completing this project.                                                                                                                                                                                                           | Must Have, Stretch Goal      |
