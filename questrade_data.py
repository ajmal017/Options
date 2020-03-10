import questradeapi as qapi

refresh_token = input('Refresh Token: ')
sess = qapi.Session(refresh_token)
