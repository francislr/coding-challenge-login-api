
def get_user_ip_address(request):
    """
    Guess the user IP address based on the X-Forwarded-For HTTP header.
    If the header is omitted, the remote address is returned.

    Discussion : https://stackoverflow.com/a/5976065

    The solution assumes a typical production setup where only one user-facing proxy is present.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')
