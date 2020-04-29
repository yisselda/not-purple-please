# Slack Theme Generator
Generates a slack theme from an image.
Pertinent images like logos work well.

[Preview the generated themes from the SlackableThemes project](https://github.com/yisselda/SlackableThemes)

### Install dependencies
You will need pipenv, you can install it with Homebrew: `brew install pipenv`
```
pipenv install
```

### Create a virtual environment
```
$ python3 -m venv venv
```

### Start your virtual environment
```
$ pipenv shell
```

### Update dependencies


### Install dependencies


### Start the server
```
$ export FLASK_APP=controller.py
$ flask run
```

### Run the tests
```
$ python -m unittest
```

### Production URL
https://gen-slack-theme.herokuapp.com/

### Endpoint to generate a Slack Theme from an image:
```
POST https://gen-slack-theme.herokuapp.com/create-theme
Content-type: multipart/form-data
```

⚠️ Allowed file formats are `'png', 'jpg', 'jpeg', 'gif'`

### Interesting Reads📚
- [The Science of Color Contrast](https://medium.muz.li/the-science-of-color-contrast-an-expert-designers-guide-33e84c41d156)
