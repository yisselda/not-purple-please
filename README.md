# Slack Theme Generator
Generate a slack theme from an image.
Pertinent images like logos work well.

[Preview the generated themes from the SlackableThemes project](https://github.com/yisselda/SlackableThemes)

### Start your virtual environment
```
$ source venv/bin/activate
```

### Start the server
```
$ export FLASK_APP=controller.py
$ flask run
```

### Production URL
https://gen-slack-theme.herokuapp.com/

### Endpoint to generate a Slack Theme from an image:
```
POST https://gen-slack-theme.herokuapp.com/create-theme
Content-type: multipart/form-data
```

⚠️ allowed file formats: 'png', 'jpg', 'jpeg', 'gif'
