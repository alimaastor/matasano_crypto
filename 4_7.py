
import os

def main():
    import re
    import mechanize
    from mechanize import Browser

    br = Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Ignore robots.txt
    br.set_handle_robots( False )
    # Google demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]

    # Retrieve the Google home page, saving the response
    br.open( "http://localhost:8080/upload" )
    br._factory.is_html = True
    print br.response().read()
    print br.response().code

    # Select the search box and search for 'foo'
    br.select_form( 'uploadFile' )
    filename = os.path.join('data', '4_7_data.txt')
    br.form.add_file(open(filename), 'text/plain', filename)

    # Get the search results
    try:
        br.submit()
    except Exception:
        print '500'
    else:
        print '200'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement and break HMAC-SHA1 with an artificial timing leak - Challenge 31 (Set 4) of Matasano Crypto Challenge.')

    main()
