# locoMail
A simple smtp server that can be used for testing

## Motivation
As a developer in many ocassions you will require to send emails. It is a pain to either modify the code so that
the emails are directed to your account or use a special mailserver set by someone in the office that will forward
all the emails to "developers@whatever.com".

Not only this is messy and dirty, it is a total overhead.

I am trying to solve this.

## How does it works
Essentially it extends the SMTPServer object in python, when a new mail is received it is stored into a simple
sqlite3 database. The reason to store the mails (and even the attachments!) into a database is that it is fairly
simple to search for them afterwards.

## How do I run it.
The easiest way is to use docker, either run it directly

```bash
docker run --rm --name loco-mail -it -p -p 10000:5000 -p 25:25 loco-mail
```

Or via docker-compose

```bash
docker-compose up
```

You will need to expose ports 10000 and 25. Of course port 25 is the SMTP server, port 10000 is the web interface
to check any new emails.

If you prefer not to run docker, simply run the python script directly

```bash
cd src
python3 locoServer.py
```

Note that you will need to install the following libraries

```bash
requests
gevent
flask
```

You can install them with pip3

```bash
pip3 install requests gevent flask
```