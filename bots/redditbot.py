import sys
import time
import praw
import re
import requests

reddit = praw.Reddit(
    user_agent="configreddit",
    client_id="hvytENVlQMoGTw",
    client_secret="61_QrgDy8ws96r1wk85GMuuXWjDN8A",
    username="Bibibobot",
    password="86trpWj*edMr@R.",
)

# Legt das Muster [Buchstaben]-[Zahlen] fest
code_pattern = re.compile(r'((.|\s|^)([a-zA-Z]{3}|[a-zA-Z]{4}|[a-zA-Z]{5})-[0-9]{3})|([hH][eE][yY][zZ][oO]-[0-9]{'
                          r'4})|(1[pP][oO][nN][dD][oO] [0-9]{6}_[0-9]{3})|([cC][aA][rR][iI][bB][bB][eE][aA][nN][cC]['
                          r'oO][mM] [0-9]{6}-[0-9]{3})')


def post(info_dict):
    '''
    Generates a Reddit-conform comment containing all codes and their infomation

    Parameters
    ----------
    info_dict: dict
    dict of codes paired with the comment they were found in
    '''
    subreddit = reddit.subreddit("javbot")
    localtime = time.asctime(time.localtime(time.time()))
    ausgabe = ""
    # generiert ausgabe
    z = 1
    for code in info_dict:
        jav_link = "www.javmost.com/" + code
        r = requests.get(jav_link.replace('www', 'https://www'))
        if str(type(info_dict[code])) == "<class 'praw.models.reddit.submission.Submission'>":
            link = "www.reddit.com/r/" + info_dict[code].subreddit.display_name + "/comments/" + info_dict[
                code].id + "/"
        else:
            link = "www.reddit.com/r/" + info_dict[code].subreddit.display_name + "/comments/" + info_dict[
                code].submission.id + "/_/" + info_dict[code].id + "/"
        if r.status_code == 404:
            ausgabe = ausgabe + str(z) + ".: " + code + " r/" + info_dict[
                code].subreddit.display_name + "\n \n" + link + "\n \n"
        else:
            ausgabe = ausgabe + str(z) + ".: " + code + " r/" + info_dict[
                code].subreddit.display_name + "\n \n" + link + "\n \n" + jav_link + "\n \n"
        z += 1
    # subreddit.submit(title=str(localtime), selftext=ausgabe)
    print(ausgabe)


def code_extraktion(potential_codes):
    '''
    Extracts the raw codes from the string it has been found in

    Parameters
    ----------
    potential_codes: list
    list of potential codes

    Returns
    -------
    sauce_dirty: list
    list of actual codes
    '''
    sauce_dirty = list()
    for i in potential_codes:
        if str(type(i)) == "<class 'praw.models.reddit.submission.Submission'>":
            txt = i.title
        else:
            txt = i.body
        compiled = code_pattern.search(txt)
        sauce_dirty.append(compiled.group(0))
    return sauce_dirty


def code_cleaner(sauce_dirty):
    '''
    Cleans up the codes

    Parameters
    ----------
    sauce_dirty: list
    list of dirty codes

    Returns
    -------
    sauce_clean: list
    list of cleaned codes
    '''
    not_allowed_chars = ".[]{}!$%&/()?*+#'"
    sauce = list()
    sauce_clean = list()
    for i in sauce_dirty:
        txt = i.upper()
        txt = txt.replace(' ','-')
        txt = txt.replace(not_allowed_chars, '')
        sauce_clean.append(txt)
    return sauce_clean


def process_comments(potential_codes):
    codes = code_extraktion(potential_codes)
    clean_codes = code_cleaner(codes)
    info_dict = dict(zip(clean_codes, potential_codes))
    return info_dict


def comment_crawler(subreddit_list):
    """
    Takes a list subreddits and iterates through top-of-day posts.
    Posts are checked if they match a code-pattern and further cleaned up by code_extraktion code_cleaner and process_comments

    Parameters
    ----------
    subreddit_list: list
        list of subreddits

    Returns
    -------
    info_dict:
        a dictionary of JAV-codes paired with the comment they were found in
    """
    potential_codes = list()
    # Iteriere durch Subreddit Liste, nimmt die Top-Posts fuer weitere Bearbeitung
    for curr_subreddit in subreddit_list:
        top_posts = curr_subreddit.top(time_filter="day", limit=10)
        # Iteriere durch die Top-Posts
        for curr_post in top_posts:
            curr_post.comments.replace_more()
            # durchlauft alle kommentare und prueft, ob das Muster enthalten ist
            for comment in curr_post.comments.list():
                if code_pattern.match(comment.body):
                    potential_codes.append(comment)
            if code_pattern.match(curr_post.title):
                potential_codes.append(curr_post)
    info_dict = process_comments(potential_codes)
    return info_dict


def Main(args=None):
    with open('subreddits.txt') as lines:
        subreddits = lines.read().split()
    subreddit_list = [reddit.subreddit(i) for i in subreddits]
    results = comment_crawler(subreddit_list)
    if "posten" in args:
        post(results)
    return results


if __name__ == "__main__":
    Main(sys.argv)
