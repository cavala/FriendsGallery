# Flask + Python + MongoDB + AWS S3 +  Okta Hosted Login

This application shows  you how to use Flask to log in to your application with an Okta Hosted Login page.  The login is achieved through the [authorization code flow](https://developer.okta.com/authentication-guide/implementing-authentication/auth-code), where the user is redirected to the Okta-Hosted login page.  After the user authenticates, they are redirected back to the application with an access code that is then exchanged for an access token.

> Requires Python version 3.6.0 or higher.

## Prerequisites

Before running this sample, you will need the following:

* An Okta Developer Account, you can sign up for one at https://developer.okta.com/signup/.
* An Okta Application configured for Web mode. You can create one from the Okta Developer Console, and you can find instructions [here][OIDC WEB Setup Instructions].  When following the wizard, use the default properties.  They are designed to work with our sample applications.

## Running This Example

To run this application, you first need to clone this repo:

```bash
git clone git@github.com:cavala/FriendsGallery.git
```

Then install dependencies:

```bash
pip install -r requirements.txt
```


Start the app server:

```
python main.py
```

Now navigate to http://localhost:8080 in your browser.

If you see a home page that prompts you to log in, then things are working! Clicking the **Log in** button will redirect you to the Okta hosted sign-in page.

You can log in with the same account that you created when signing up for your Developer Org. You can also use a known username and password from your Okta Directory.

**Note:** If you are currently using your Developer Console, you already have a Single Sign-On (SSO) session for your Org. You will be automatically logged into your application as the same user that is using the Developer Console. You may want to use an incognito tab to test the flow from a blank slate.

[OIDC Web Setup Instructions]: https://developer.okta.com/authentication-guide/implementing-authentication/auth-code#1-setting-up-your-application
