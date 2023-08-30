# Credentials
In most cases, authentication needs to happen in order to interact with project management software suites.  This interaction can use certificates, API keys, or simple username/password combinations.  In order to store these credentials, {{projectName}} comes with a keyring authenticator.  This will allow credentials to be stored in the OS's keyring.  For Windows, that will be the Credential Manager.  For other OS's, the keyring can vary based on implementations.

## Storing Credentials
Before using the credentials, they need to be stored in the appropriate keyring.  Storing credentials in a keyring typically requires a service name, username, and password.  When storing the credentials, multiple entries may be created in the keyring.  For example, simple username and password combinations will require two entries &dash;&dash; one for the username and one for the password.  The service name will vary based on the purpose for the credentials.  Credentials for JIRA will use **jira** for the service name.  Let's look at an example.

```
>>> import keyring
>>> keyring.set_password('jira', 'username', 'myjirausername')
>>> keyring.get_password('jira', 'username')
'myjirausername'
>>> keyring.set_password('jira', 'password', 'myjirapassword')
>>> keyring.get_password('jira', 'username')
'myjirauserpassword'
```

This code sets and retrieves the credentials just as an example.  All you need to do is set the credentials and the authenticator will handle reading them.  Your OS may have other ways to interface with its keyring.  This is just one way to do it.

The available values for the usernames portion of the keyring entries are 'username', 'password', 'api_key', and 'certificate'.