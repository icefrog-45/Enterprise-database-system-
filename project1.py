import sqlite3
import time
import random
import string
from datetime import date
import getpass
import sys
import getopt
import math
import numbers

connection = None
cursor = None

class Post:
    def __init__(self, pid, pdate, title, body, poster):
        self.pid = pid
        self.pdate = pdate
        self.title = title
        self.body = body
        self.poster = poster
    def get_pid(self):
        return self.pid
    def get_pdate(self):
        return self.pdate
    def get_title(self):
        return self.title
    def get_body(self):
        return self.body
    def get_poster(self):
        return self.poster

class User:
    def __init__(self, uid, name, pwd, city, crdate, privileged):
        self.uid = uid
        self.name = name
        self.pwd = pwd
        self.city = city
        self.crdate = crdate
        self.privileged = privileged



    def get_privileged(self):
        return self.privileged

    def postQuestion(self):
        #creates a question post
        #gets: title, body
        #auto gen: pid, pdate, poster
        #returns True when completed

        #set up connection
        global connection, cursor

        print("Type 'back' to return to the previous page")

        #get all pid in system
        cursor.execute('SELECT pid FROM posts')
        all_pid = cursor.fetchall()

        pid_lst = []
        for a_pid in all_pid:
            pid_lst.append(a_pid[0])

        #generate a random pid
        #double check if pid is unique
        unique_pid = False
        while not unique_pid:
            pid = get_random(4)
            if pid not in pid_lst:
                unique_pid = True

        pdate = date.today()
        poster = self.uid

        #ask for title
        title = input("Enter a title for your post: ")
        if title.lower() == 'back':
            return False

        #ask for body text
        text = input("Enter a question:\n")
        if text.lower() == 'back':
            return False

        #add question post to tables:
        # - posts
        # - questions
        cursor.execute("""
            INSERT INTO posts (pid, pdate, title, body, poster)
            VALUES (:pid, :pdate, :title, :body, :poster);""",
            {'pid': pid, 'pdate': pdate, 'title': title, 'body': text, 'poster': poster}
            )
        cursor.execute("""
            INSERT INTO questions (pid, theaid)
            VALUES (:pid, :theaid);""",
            {'pid': pid, 'theaid': None}
            )
        connection.commit()
        print("You just post a question!")
        return True

    def postAnswer(self, qid):
        #creates an answer post
        #gets: title, body
        #auto gen: pid, pdate, poster
        #returns True when completed

        #set up connection
        global connection, cursor


        print("Type 'back' to return to the previous page")

        #check if the post is a question,
        #if not, return to previous page with an error message
        cursor.execute('SELECT pid FROM questions WHERE pid=:qid;', {'qid':qid},)
        selected_question = cursor.fetchone()
        if selected_question == None:
            print("You can only post an answer to a question!\n")
            return False

        #get all pid in system
        cursor.execute('SELECT pid FROM posts')
        all_pid = cursor.fetchall()

        pid_lst = []
        for a_pid in all_pid:
            pid_lst.append(a_pid[0])

        #generate a random pid
        #double check if pid is unique
        unique_pid = False
        while not unique_pid:
            pid = get_random(4)
            if pid not in pid_lst:
                unique_pid = True

        pdate = date.today()
        poster = self.uid

        #ask for title
        title = input("Enter a title for your post: ")
        if title.lower() == 'back':
            return False

        #ask for body text
        text = input("Enter an answer:\n")
        if text.lower() == 'back':
            return False

        #add answer post to tables:
        # - posts
        # - answer
        cursor.execute("""
            INSERT INTO posts (pid, pdate, title, body, poster)
            VALUES (:pid, :pdate, :title, :body, :poster);""",
            {'pid': pid, 'pdate': pdate, 'title': title, 'body': text, 'poster': poster}
            )
        cursor.execute("""
            INSERT INTO answers (pid, qid)
            VALUES (:pid, :theaid);""",
            {'pid': qid, 'theaid': pid}
            )
        connection.commit()
        return True

    def vote(self, pid):
        #increase the vote number
        #gets:pid
        #auto gen: vdate
        #returns True when completed

        #set up connection
        global connection, cursor


        vdate = date.today()
        user = self.uid

        #get all pid in db
        cursor.execute('SELECT pid FROM votes;')
        all_pidwithvote = cursor.fetchall()

        #check if user already make the vote on the post
        cursor.execute('SELECT uid FROM votes WHERE pid=:pid;', {'pid' : pid},)
        user_vote = cursor.fetchone()
        if user_vote != None:
            print("You've already voted on this post!\n")
            connection.commit()
            return False
        else:
            print("Type 'back' to return to the previous page: ")
            choice = input("Do you want to vote for this post:(Y/N) ")
            if choice=='y' or choice=='Y':
                #get all vno
                cursor.execute('SELECT vno FROM votes ;')
                all_uno = cursor.fetchall()

                #generate a random pid
                #double check if pid is unique
                unique_vno = False
                while not unique_vno:
                    vno = get_random(4)
                    if vno not in all_uno:
                        unique_vno = True


                #add the user vote history into db
                cursor.execute('INSERT INTO votes (pid, vno, vdate, uid) VALUES (?,?,?,?);',(pid,vno,vdate,user))
                print("You just voted on the post!")
                connection.commit()
                return True
            else:
                connection.commit()
                return False


    def markAccepted(self, pid):
        #input pid: post id (answer be selected)
        ##returns True when completed

        #set up connection
        global connection, cursor
        c = connection.cursor()

        #get pid of the question
        cursor.execute('SELECT qid from answers where pid=:pid;', {'pid':pid},)
        question_id=cursor.fetchone()
        if question_id == None:
            print("A question post cannot be marked as an accepted answer!\n")
            return False

        #get accepted answer of question
        cursor.execute('SELECT theaid from questions where pid=:pid;', {'pid':pid},)
        ans=cursor.fetchone()

        #no accepted answer
        if ans == None:
            a=input("Do you want to set selected post as accepted answer?: (Y/N)")
            if a=='y' or a=='Y':
                cursor.execute("UPDATE questions SET theaid=:pid WHERE pid=:qid;", {'qid':question_id[0], 'pid':pid},)
                print("Post {} has now been marked as the accepted answer of question post {}!\n".format(pid, question_id[0]))
                connection.commit()
                return True
            else:
                connection.commit()
                return False

        #if selected post is an accepted answer
        elif pid in ans:
            print("The selected post is already an accepted answer")
            connection.commit()
            return False

        else:
            b=input("The selected post already had an accepted answer, do you want to change it?")
            if b=='y' or b=='Y':
                cursor.execute("UPDATE questions SET theaid=:pid WHERE pid=:qid;", {'pid':pid, 'qid':question_id[0]},)
                connection.commit()
                return True
            else:
                connection.commit()
                return False



    def giveBadge(self, pid):
        global connection, cursor

        #get badgename
        badgeName = input("Enter a badge name: ")
        bdate = str(date.today())

        cursor.execute("""SELECT bname FROM badges;""")
        bnames = cursor.fetchall()

        bnames_lst = []
        for name in bnames:
            bnames_lst.append(name[0])

        while badgeName not in bnames_lst:
            badgeName = input("No such a badge! Please enter another badge:\n")

        cursor.execute("""SELECT u.uid, u.bdate FROM ubadges u, posts p WHERE p.pid = ? AND u.uid = p.poster AND u.bname LIKE ?;""", (pid,badgeName))
        results = cursor.fetchall()

        if bdate in results[:, 1]:
            # there is already a badge with the same name given to the poster
            print("The same badge has already been given to the poster today.")
            return
        else:
            # give the badge to the poster
            # find the exact bname
            cursor.execute("""SELECT bname FROM ubadges WHERE bname LIKE """  + badgeName + """;""")
            bname = cursor.fetchone()[0]
            # find the poster
            cursor.execute("""SELECT poster FROM posts WHERE pid = ?;""", (pid,))
            poster = cursor.fetchone()[0]
            cursor.execute("""INSERT INTO ubadges VALUES (?, ?, ?);""", (poster, pdate, bname,))
            connection.commit()
        return

    def addTag(self, pid):
        #creates a tage
        #gets: tags
        #returns

        #set up connection
        global connection, cursor
        c = connection.cursor()

        print("Type 'back' to return to the previous page")
        #ask for tag
        tag = input("Enter the tag for your post: ")

        if tag.lower() == 'back':
            return False

        cursor.execute('SELECT tag FROM tags')
        tags = cursor.fetchall()

        #check if tag already exit
        already_exit = 1

        if tag not in tags:
          already_exit=0

        #if tag already exits
        if already_exit:
          print("the tag already exit")
          cursor.commit()
          return False

        else:
          cursor.execute('INSERT INTO tags VALUES (?,?);', pid,tag)
          connection.commit()
          return True


    def edit(self, pid):
        global connection, cursor

        if_title = input("Would you like to edit the title? (y/n)\n")
        while if_title != "y" and if_title != "n":
            print("Invalid input!")
            if_title = input("Would you like to edit the title? (y/n)\n")
        if if_title == "y":
            #ask for title
            title = input("Enter a new title for the post: ")
            if title.lower() == 'back':
                return False
        elif if_title == "n":
            # retrieve the previous title
            cursor.execute("SELECT title FROM posts WHERE pid = ?;", (pid,))
            title = cursor.fetchall()[0][0]

        if_body = input("Would you like to edit the body? (y/n)\n")
        while if_body != "y" and if_body != "n":
            print("Invalid input!")
            if_body = input("Would you like to edit the body? (y/n)\n")
        if if_body == "y":
            #ask for body text
            text = input("Enter a new post body: \n")
            if text.lower() == 'back':
                return False
        elif if_title == "n":
            # retrieve the previous body
            cursor.execute("""SELECT body FROM posts WHERE pid = ?;""", (pid,))
            body = cursor.fetchall()[0][0]

        # add edited post to tables:
        # - posts
        # - questions
        cursor.execute("""
            UPDATE posts
            SET title =""",
            {'pid': pid, 'pdate': pdate, 'title': title, 'body': body, 'poster': poster}
            )
        connection.commit()
        return


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    #cursor.execute(' PRAGMA foreign_keys=ON; ')

    #read in data from a file
    #file = open(sys.argv[1])   THIS WILL BE USED IN THE FINAL COPY
    file = open("testdata2.txt")  # THIS IS FOR TESTING ONLY
    file = file.read()
    cursor.executescript(file)
    connection.commit()
    return


#LOGIN PAGE: SIGN IN, SIGN OUT
##############################################################################
def intro():
    #print introduction
    #ask user to login or sign up
    print("Hello!")

    valid_input = False
    while not valid_input:
        action = input("To sign in to an existing account, type 'signin'\n"
                       "To sign up for a new account, type 'signup'\n"
                       "To close program, type 'exit' \n")
        if action.lower() == "signin":
            return 1
        elif action.lower() == "signup":
            return 2
        elif action.lower() == "exit":
            print("...adios :)")
            quit()
        else:
            print("Invalid input!")


def sign_in():
    #sign in a pre-existing user

    #set up connection
    global connection, cursor
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    #separate pages
    print('-'*50 + "\n")

    print("Type 'back' to return to the previous page")

    #ask user for user id and password
    while True:
        username = input("Please enter your username: ")
        #user wants to go back to the start
        if username.lower() == "back":
                    return 0
        else:
            password = getpass.getpass()

        #query for userID
        #should only give one row because userID is unique
        cursor.execute('SELECT * FROM users WHERE uid = :uname AND pwd = :pw;',
                  { 'uname': username, 'pw': password },)
        row = cursor.fetchone()

        if row == None:
            print("Invalid username or password!\n")
        #found user in database
        elif (username in row) and (password in row):

            #check if user is a privileged user
            is_privileged = cursor.execute('SELECT * FROM privileged WHERE uid = :uname',
                                      {'uname': username}).fetchone()

            if is_privileged != None:
                if username in is_privileged:
                    #create privileged User class object then return
                    priv_user = User(row['uid'], row['name'], row['pwd'], row['city'], row['crdate'], True)
                    return priv_user

            #create regular User class object then return
            reg_user = User(row['uid'], row['name'], row['pwd'], row['city'], row['crdate'], False)
            return reg_user

        connection.commit()


def sign_up():
    #create new user
    #get: uid, name, pwd, city
    #auto generate crdate
    #privileged = False

    #set up connection
    global connection, cursor

    #get all uid in system
    cursor.execute('SELECT uid FROM users')
    all_uid = cursor.fetchall()
    uid_list = []
    for a_uid in all_uid:
        uid_list.append(a_uid[0])

    #separate pages
    print('-'*50 + "\n")

    print("Type 'back' to return to the previous page")

    #get user info
    name = input("Please enter a name (This is your public name): ")
    #user wants to go back to the start
    if name.lower() == "back":
                return 0

    city = input("Please enter your city: ")
    #user wants to go back to the start
    if city.lower() == "back":
                return 0

    crdate = date.today()

    #validate uid
    valid_uid = False
    uid = ''
    while not valid_uid:
        uid = input("Please enter a username (must be 4 characters long): ")

        if len(uid) > 4:
            #error if greater than 4 char
            print("Username is too long!\n")
        elif len(uid) < 4:
            #error if less than 4 char
            print("Username is too short!\n")
        elif uid in uid_list:
            #check for UNIQUE uid
            print("Username is already taken!\n")
        elif uid.lower() == 'back':
            #return to login page
            return 0
        else:
            valid_uid = True

    #confirm pass
    pass_confirmed = False
    pwd = ''
    while not pass_confirmed:
        print("Please enter a suitable password")
        pwd = getpass.getpass()

        if pwd.lower() == 'back':
            #return to login page
            return 0
        else:
            print("Please re-enter your password")
            confirm = getpass.getpass()

            if pwd == confirm:
                #confirm match
                pass_confirmed = True
            else:
                print("Passwords don't match!")

    #insert into users table
    cursor.execute("""
        INSERT INTO users (uid, name, pwd, city, crdate)
        VALUES (:uid, :name, :pwd, :city, :crdate);""",
        {'uid': uid, 'name': name, 'pwd': pwd, 'city': city, 'crdate': crdate}
        )
    connection.commit()

    #create regular User class object
    reg_user = User(uid, name, pwd, city, crdate, False)
    return reg_user

def login():
    #main login page
    #handles all login actions:
    #  - sign in
    #  - sign out
    #typing 'back' at any page allows user to return to login page
    login_action = intro()

    while True:
        if login_action == 0:
            login_action = intro()
        elif login_action == 1:
            login_action = sign_in()
        elif login_action == 2:
            login_action = sign_up()
        elif isinstance(login_action, User):
            return login_action
        else:
            print("An error has occured, please try again.")
            login_action = 0
##############################################################################

def instructions():
    print("""
            -----------------------------------------------------
             help       show instructions
             postq      post a question
             search     search for posts
             logout     logs out of current account
             exit       exits program
             The following are post-search actions:
             (note actions with * are for privileged users only)
             answer     post an answer to a selected question post
             vote       upvote a selected post
             accept*    mark the selected answer post as the
                        accepted answer for its corresponding
                        question
             badge*     give a badge to the selected post's poster
             tag*       add a tag to the selected post
             edit*      edit the selected post
             -----------------------------------------------------
          """)



def signed_in_block(user):
    #main signed in actions block
    #asks users for what they want to do

    #separate pages
    print('-'*50 + "\n")

    print("Enter help for instructions")

    #list of post search actions
    ps_actions = ["answer", "vote", "accept", "badge", "tag", "edit"]
    selected_post = None
    is_done = False
    while not is_done:
        #ask user for what they want to do
        action = input("What would you like to do? ")

        if action.lower() == "help":
            #print instructions
            instructions()

        elif action.lower() == "exit":
            #user exits program
            print("Exiting session...\n")
            return action.lower()

        elif action.lower() == "logout":
            #go back to intro page
            print("Logged out!\n")

            #separate pages
            print('-'*50 + "\n")
            return action.lower()

        elif action.lower() == "postq":
            #post a question
            user.postQuestion()

        elif action.lower() == "search":
            #search
            selected_post = search_block()

        elif action.lower() in ps_actions:

            if isinstance(selected_post, Post):
                #if selected post is a Post object
                if action.lower() == "answer":
                    user.postAnswer(selected_post.get_pid())

                elif action.lower() == "vote":
                    user.vote(selected_post.get_pid())

                elif action.lower() == "tag":
                    if user.get_privileged():
                        user.addTag(selected_post.get_pid())
                    else:
                        print("Action only available to privileged users!\n")

                elif action.lower() == "accept":
                    if user.get_privileged():
                        user.markAccepted(selected_post.get_pid())
                    else:
                        print("Action only available to privileged users!\n")

                elif action.lower() == "badge":
                    if user.get_privileged():
                        user.giveBadge(selected_post.get_pid())
                    else:
                        print("Action only available to privileged users!\n")

                elif action.lower() == "edit":
                    if user.get_privileged():
                        user.edit(selected_post.get_pid())
                    else:
                        print("Action only available to privileged users!\n")

            else:
                #raise error if user has not searched/selected a post
                #            or if the selected post is not a Post object
                print("No post selected yet! Please search for a post first!\n")

        else:
            #raise error if user enters an action not listed
            print("Invalid action!\n")




#SEACH BLOCK: SEARCH USING KEYWORDS, DISPLAY RESULTS, SELECT POST
##############################################################################
def get_keywords():
    #get keywords and split them
    #if nothing was entered, raise error and ask again
    key_length = 0
    while key_length == 0:
        keywords = input("Enter a keyword or keywords separated by ',' to search: \n")
        keywords_lst = keywords.split(',')
        key_length = len(keywords_lst)

        if key_length == 0:
            print("Cannot search without entering a keyword!")

    return keywords_lst

def make_post_objects(post):
    #converts a post into a Post object
    pid = post[0]
    pdate = post[1]
    title = post[2]
    body = post[3]
    poster = post[4]

    new_post = Post(pid, pdate, title, body, poster)

    return new_post

def display_results(post_list):
    #display results, 5 per page
    #show:
    #- pid, pdate, title, body, poster
    #- votes, answers to question posts (0 if none)
    ###list should only contain 5 items at max!!!###

    border = '-'*95
    print(border)
    #maybe we can get this from cursor.description
    col_names = ["pid", "date", "title", "body", "poster", "votes", "answers"]
    print("|{:^6}|{:^12}|{:^10}|{:^30}|{:^10}|{:^4}|{:^7}".format(*col_names))
    print(border)

    #print each post
    #find a better way to do this
    for post in post_list:

        if (len(post[2]) > 10) and (len(post[3]) > 30):
            #both title and body too long
            print("|{:^6}|{:^12}|{:^7.7}...|{:^27.27}...|{:^10}|{:^4}|{:^7}".format(*post))

        elif len(post[3]) > 30:
            #long body
            print("|{:^6}|{:^12}|{:^10}|{:^27.27}...|{:^10}|{:^4}|{:^7}".format(*post))

        elif len(post[2]) > 10:
            #long title
            print("|{:^6}|{:^12}|{:^7.7}...|{:^30}|{:^10}|{:^4}|{:^7}".format(*post))

        else:
            print("|{:^6}|{:^12}|{:^10}|{:^30}|{:^10}|{:^4}|{:^7}".format(*post))
    print(border)

def split_list(lst, num):
    #split a list into sublists of length num
    new_lst = []
    for i in range(0, len(lst), num):
        new_lst.append(lst[i: i + num])
    return new_lst

def nav_select_post(matching_posts):
    #processes list of posts obtained from query for displaying
    #asks user to select a post
    #user can press next or back to navigate through posts (if any)

    #create pages
    #how many pages do we need
    num_pages = math.ceil(len(matching_posts)/5)
    post_pages = split_list(matching_posts, 5)

    print("Number of pages = ", num_pages)

    #print instructions
    instructions = ("To select a post, type a number from 1-5 corresponding to its order.\n",
                    "Eg. To select the second post, type '2'. \n",
                    "To navigate between pages or posts, type 'next' or 'prev'.\n",
                    "To return to main page, type 'back'.\n")
    print("".join(instructions))

    post_selected = False
    #0 = first page
    showing = 0
    #display and let user select a post
    #show 5 posts at a time
    display_results(post_pages[showing])
    while not post_selected:
        user_action = input("Enter an action: ")


        if user_action.lower() == "next":
            #if not the last page, move to the next one
            if showing < (num_pages - 1):
                showing += 1
                display_results(post_pages[showing])
            else:
                print("No more pages ahead!")
        elif user_action.lower() == "prev":
            #if not the first page, move the previous one
            if showing > 0:
                showing -= 1
                display_results(post_pages[showing])
            else:
                print("This is the first page!")
        elif user_action.lower() == "back":
            #cascade back to main page
            return user_action
        else:
            try:
                isinstance(int(user_action), numbers.Number)
                #if input is an int, check if a post is selected
                if int(user_action) <= len(post_pages[showing]):
                    #return the post selected by user
                    return post_pages[showing][int(user_action)-1]
            except:
                print("Invalid! Please try again.")


def query_for_posts(keywords):
    #takes in keywords list
    #queries for posts
    #returns a list of Post objects
    global connection, cursor
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()


    ###############################################     QUERY
    #GET POSTS
    #GET VOTES OF POSTS
    #GET NUMBER OF ANSWERS TO POSTS (if is a question post)

    search_query = """with
                      vt as (select pid, count(vno) as vc_count
                      from votes
                      group by pid),
                      ans as (select a.qid, count(a.pid) as a_count
                      from posts p, answers a
                      where a.pid = p.pid
                      group by a.qid)
                      select p.pid, p.pdate, p.title, p.body, p.poster, ifnull(vc_count, 0), ifnull(a_count, 0)
                      from posts p
                      left join vt on vt.pid = p.pid
                      left join ans on ans.qid = p.pid
                      left join tags on tags.pid = p.pid
                      where """

    for keyword in keywords:
        search_query = search_query + """ tags.tag like "%""" + keyword + """%" OR p.title like "%""" + keyword + """%" OR p.body like "%""" + keyword + """%" OR"""

    search_query = search_query.rstrip("OR")

    search_query = search_query + """ group by p.pid, p.pdate, p.title, p.body, p.poster, vc_count, a_count
                                      order by 0 """

    for keyword in keywords:
        search_query = search_query + """ + (tags.tag like "%""" + keyword + """%" OR p.title like "%""" + keyword + """%" OR p.body like "%""" + keyword + """%")"""

    search_query = search_query + """ DESC;"""

    cursor.execute(search_query)

    ################################################

    matching_posts = cursor.fetchall()

    connection.commit()

    return matching_posts  #a list of post tuples from query


def search_block():
    #this function is called when user want to search
    #handles searching and displaying results
    #returns a Post object of the post selected by the user
    #        or a string that says otherwise

    #gets a list of keywords from user to search with
    keywords = get_keywords()
    #queries posts
    matching_posts = query_for_posts(keywords)

    #if no posts found, return to main signed in block
    if len(matching_posts) == 0:
        print("No posts found")
        return

    #show posts and allow selection
    selected_post = nav_select_post(matching_posts)

    #if user enters 'back', return
    if selected_post == 'back':
        return

    #turn selected_post into a Post object
    selected_post = make_post_objects(selected_post)


    print("selected post: ", selected_post.get_pid())
    print("")

    return selected_post


##############################################################################


#POST SEARCH ACTIONS: ANSWER, VOTE, GIVE BADGE, EDIT, TAG, ACCEPT ANSWER
##############################################################################

#def answer(selected_post):
    ##allows user to post an answer to the post if it's a question post
    #global connection, cursor

    ##is it a question post



##############################################################################


def get_random(length):
    #https://pynative.com/python-generate-random-string/
    #creates a random string of a given length
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(length))
    return rand_str



def main():
    global connection, cursor

    path = "./register.db"
    connect(path)

    session_done = False
    while not session_done:
        user = login()

        print("Logged in!\n")

        #main signed in block here
        action = signed_in_block(user)

        if action == 'exit':
            print("...adios :)")
            session_done = True


    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
