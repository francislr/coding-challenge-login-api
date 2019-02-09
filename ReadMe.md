# TLM Ninja login API Coding challenge

My take on the TLM Ninja Coding Challenge 🐱‍👤

## Installation

* Create and activate a Python Virtual Environment
* Install dependencies from `requirements.txt`<br>
  `pip install -r requirements.txt`
* Copy `therewasanattempt/settings.py.dist` to `therewasanattempt/settings.py`
* Edit `therewasanattempt/settings.py`
  * By default, the `SECRET_KEY` setting is taken from the `APP_SECRET` environment variable
* Run the usual Django setup commands:
  * `python manage.py migrate`
  * `python manage.py createsuperuser`

## Project structure

<dl>
  <dt><i>therewasanattempt/</i></dt>
  <dd>Django project directory</dd>
</dl>

# The Challenge

Your mission: Create and deploy a `django` application exposing a REST API that will provide details on _login attempts_.
Example details would be IP Address, Region, success and failure attempts count, anything else you think that sounds interesting.

## Requirements

### Backend

- [ ] Expose a REST API
- [ ] Have a way to authenticate with the API
- [ ] Write unit tests to validate API behaviour

### Frontend

- [ ] Have a frontend app, page or django view to login and consume the API
- [ ] List login attempts with details

### The Rules

- [ ] Deployed applicaton must be used on a secure connection (https)
- [ ] Code must be open source
- [ ] There must be a license for the code (of your choice)
- [ ] You must use `git` (you can fork this repo or create a new one)
- [ ] Commit messages should follow [the seven rules of a great Git commit message](https://chris.beams.io/posts/git-commit/)
- [ ] Your project should follow [12 factor](https://12factor.net/) principles

### Deliverable

- [ ] Link to git repository
- [ ] Url to live application
- [ ] Credentials so we can try your application

### Advices

* **Try to design and implement your solution as you would do for real production code.** Show us how you create clean, maintainable code that does awesome stuff. Build something that we'd be happy to contribute to. This is not a programming contest where dirty hacks win the game.
* Feel free to add more features!
* Documentation and maintainability is a plus.
* **Don't you forget those unit tests.**
* We don’t want to know if you can do exactly as asked (or everybody would have the same result). We want to know what you bring to the table when working on a project, what is your secret sauce. More features? Best solution? Thinking outside the box?
* Make sure you apply security good practices. Ninjas hide their secrets because pirates will find them.

