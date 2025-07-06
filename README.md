<p align="center">
  </a>
  <br />
</p>
<div align="center">
  <h1>
    Stytch LLM agent starter kit
  </h1>
  <p>LangChain app with a Stytch-powered auth and user management flows</p>
</div>

This repo includes a fully built sample LLM application, Explain Like I'm Five. Explain Like I'm Five was originally built on top of Stytch's React Quickstart example application, which can be found [here](https://stytch.com/docs/b2b/quickstarts/react).

## App dependencies

```bash
git clone https://github.com/lilybarrett/langchain-stytch-agent-starter.git
```

To run the example locally, you need to:

1. Sign up for a Stytch account and create a Stytch B2B Project in your [**Stytch Dashboard**](https://stytch.com/dashboard).
2. Open up the application in your code editor. You should notice we have both `frontend` and `backend` subdirectories. Each one includes an `.env.example` file with some sample variables.
3. Please copy the values for each sub-directory’s `.env.example` file into a new `.env.local` file.

```bash
$ cp frontend/.env.example frontend/.env.local
$ cp backend/.env.example backend/.env.local
```

Open each `.env.local` in the text editor of your choice. Set the environment variables using the `project_id`, `secret`, and `public_token` found on [API Keys](https://stytch.com/dashboard/api-keys).

## Configuring your Stytch project

To allow the Stytch SDK to run on your frontend, you'll also need to:

1. Enable frontend SDKs in **Test** in your [**Stytch Dashboard here**](https://stytch.com/dashboard/sdk-configuration).
2. Add the domain your application will run on ([`http://localhost:5173/`](http://localhost:5173/)) to the list of **Domains** under **Authorized applications**.
3. For Email Magic Links, you must also specify a redirect URL under **Redirect URLs** to authenticate the token. Because our app uses Vite, whose default port is [http://localhost:5173/](http://localhost:5173/authenticate), please set your redirect URL for magic links to http://localhost:5173/authenticate. Set this as the **DEFAULT** for **Login, Signup, Invite, Reset Password and Discovery** types.
4. Enable the **Create organizations** toggle under **Enabled methods**. This isn't required, but this setting will allow users to create new [**Organization**](https://stytch.com/docs/resources/glossary#organization)s directly from our SDK.
5. Enable the **Member actions & permissions** toggle under **Enabled methods.** We’ll need this for RBAC purposes.

## Running the app

1. In one terminal tab, run the following commands to install your frontend dependencies and boot up the React application:

```bash
$ cd langchain-stytch-code-agent-starter
$ cd frontend
$ npm install
$ npm run dev
```

2. In another terminal tab, please run the following to create a virtual env, install Python dependencies, and load the FastAPI application:

```bash
$ source venv/bin/activate
$ python -m venv venv
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

Load up http://localhost:5173/ in your browser of choice and poke around.

## Learn more

To learn more about Stytch and LangChain, check out the following resources:

- [LangChain docs](https://python.langchain.com/docs/introduction/)
- [Stytch B2B basics](https://stytch.com/docs/b2b/guides/what-is-stytch-b2b-auth)
- [Stytch: Role-Based Access Control Overview](https://stytch.com/docs/b2b/guides/rbac/overview)
- [Stytch: Python Quickstart](https://stytch.com/docs/b2b/quickstarts/python)
- [Stytch: React Quickstart](https://stytch.com/docs/b2b/quickstarts/react)
