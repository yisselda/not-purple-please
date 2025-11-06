# Slack Theme Generator
Generates a slack theme from an image.
Pertinent images like logos work well.

[Preview the generated themes from the SlackableThemes project](https://github.com/yisselda/SlackableThemes)

### Install dependencies
You will need pipenv, you can install it with Homebrew: `brew install pipenv`
On macOS, install the OpenSSL-linked Python before creating the virtualenv:
```
$ brew install python@3.12
$ pipenv --python /opt/homebrew/bin/python3.12
```
```
$ pipenv install
```

### Update dependencies
```
$ pipenv update
```

### Add and install a dependency
```
$ pipenv install my-dependency
```

### Start the server
```
$ export FLASK_APP=controller.py
$ pipenv run flask run
```

### Run the tests
```
$ pipenv run python -m unittest
```

### Lint and format
```
$ pipenv run lint
$ pipenv run format
```
`pipenv run format` runs `isort --profile black` followed by `black` to keep imports and formatting consistent.

### Security audit
```
$ pipenv run pip-audit
```
`pipenv check` is deprecated; use `pip-audit` instead to scan the current environment and resolve any reported issues (for example by upgrading `pip` when prompted).

### Start a virtual environment terminal
```
$ pipenv shell
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
