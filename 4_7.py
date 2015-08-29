
import hashlib
import mechanize
import time

def try_signature(browser, signature):
    start_time = time.time()
    try:
        browser.open("http://localhost:8080/test?file=foo&signature={}".format(signature))
    except:
        elapsed_time = time.time() - start_time
        return elapsed_time

def get_correct_signature():
    signature = '0' * hashlib.sha1().block_size
    print 'Initial signature:', signature

    # Create browser and configure.
    browser = mechanize.Browser()
    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_robots( False )
    browser.addheaders = [('User-agent', 'Firefox')]

    # First we get the minimum processing time.
    elapsed_time = try_signature(browser, signature[:])
    print 'minimum time:', elapsed_time
    exit()

    while True:
        start_time = time.time()

        # Retrieve the page, saving the response
        br.open("http://localhost:8080/test")
        br._factory.is_html = True
        print br.response().code

        elapsed_time = time.time() - start_time

def main():
    get_correct_signature()
    
    import re

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
