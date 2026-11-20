def fetch(session, url):
    # The requests library drops the Authorization header when a redirect changes the host,
    # so follow redirects by hand.
    resp = session.get(url, allow_redirects=False)
    while resp.is_redirect:
        resp = session.get(resp.headers["Location"], allow_redirects=False)
    return resp
