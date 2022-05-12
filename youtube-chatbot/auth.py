from google_auth_oauthlib.flow import InstalledAppFlow, Flow

client_id = '495894690747-n8pnqqh99rpuqgc3kf0kcbbjof9tr4t9.apps.googleusercontent.com'
client_secret = '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'


def Oauth(filename):
    flow = InstalledAppFlow.from_client_secrets_file(
        filename,
        scopes=['openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/youtube',
                'https://www.googleapis.com/auth/youtube.force-ssl']
    )

    flow.run_local_server()
    return flow
