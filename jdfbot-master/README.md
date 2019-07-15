
This repository contains the bots for the «J'arrête de Fumer» smoking cessation
program.

## Development setup

1. Create a virtual environment if not already existing:

   python -m venv venv

2. Activate the virtual environment:

   source ./venv/bin/activate

3. The first time install the Python dependencies with:

   pip install -r dev-requirements.txt

   Later on update the required dependencies with:

   pip-sync

4. Install `pre-commit` to check for some issues before committing:

   pre-commit install

5. Create a `.env` file in project root and specify the following environment variables:

   FLASK_APP=`jdfbots/__init__.py`
   > Specifies where the flask app can be found and is necessary in order to initialize or upgrade the database in the next step.

   SERVER_URL=`…`

   > Is used in the chatbots to specify the path to pictures and other static resources that are served to the user. Since Facebook requires that the webhook uses HTTPS protocol we need to use a dynamic DNS service in order to expose the chatbots and static resources. To do so we used [localtunnel][] which provides an easy way to share our local webservice using HTTPS.

   JDF_PAGE_TOKENS=`…`

   > _`{PageID}:{MessengerAPItoken};`_

   > The page tokens contain the Facebook page id together with the messenger api access token. Information on where to get it is found [here. ](#markdown-header-tokens) Multiple page tokens can be specified, separated by a __`;`__ semicolon.

   JDF_VERIFY_TOKEN=`…`

   > The verification token is a user generated token used for authentication purpose between the webhook and Facebook's platform. More information can be found [here](https://developers.facebook.com/docs/messenger-platform/getting-started/webhook-setup/).

6. Initialize the local SQLite database:

   flask db upgrade

7. Run the bots:

   python -m jdfbots

## Production setup

1.  Install [docker][] and [docker-compose][].

2.  Enter facebook tokens in `.env`:

    JDF_PAGE_TOKENS=…
    JDF_VERIFY_TOKEN=…

3.  Start the services with [docker-compose][]:

    docker-compose up

4.  After a schema update of the database, a manual upgrade is required:

    docker exec -it jdfbots bash
    flask db upgrade

5.  Add the following line **before** the last rule in
    `/var/lib/postgresql/data/pg_hba.conf` in the container `jdfbots-db` and
    restart it afterward (or find a way to run `pg_ctl reload` ;-):

        host all all samenet trust

[docker]: https://www.docker.com/
[docker-compose]: https://docs.docker.com/compose/install/
[localtunnel]: https://localtunnel.github.io/www/

## Tokens

Tokens can be obtained through [the facebook developer
platform][facebook-developer]. The page tokens generated from the web interface are short-living ones. They can be extended to long-living ones by doing an API call, see [this answer][extend-token]. An helper for doing it with VSCode is using the file [extend.http](extend.http).

[facebook-developer]: https://developers.facebook.com/
[extend-token]: https://stackoverflow.com/questions/10467272/get-long-live-access-token-from-facebook

## TODOs

- [ ] Be sure that when a button is pressed twice in a MultipleChoice questions,
      it is not accepted by the next question.
- [ ] Propose different thanks messages for cigarettes tracker
- [ ] Kill switch (setting bot in maintenance mode if something goes wrong)
- [ ] Notifications system (email / telegram) in case of Python Exception

## Links

- [«J'arrête de Fumer» project page](https://c4science.ch/project/view/1964/)
