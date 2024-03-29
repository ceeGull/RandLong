# ;Version 3.2
import os.path

from PF import *


class ShowTime:
    """
    SHARGS (Show Time Kwargs)
    --------------------------
    debug_mode (Prints information)
        0 = Off
        1 = Lists
    """

    def __init__(self, file, **shargs):
        # SHARGS
        self.debug_mode = shargs.get("debug_mode", 0)
        # FILE
        self.file = open(file, "r+")
        self.filename = file
        # INT
        self.show_data_len = 0
        # LIST
        self.show_data = []
        self.priority_users = []  # ;Priority Users mainly can call <MUST>
        self.contents = self.file.read().split("\n")
        # DICT
        self.dbg_data = {}
        # DATETIME
        self.run_date = f"{datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
        # CODE
        if os.path.exists(file) is True:
            self.file_watched = open(f"{file[:file.index('.')]}_watched.txt", "a")
        else:
            self.file_watched = open(f"{file[:file.index('.')]}_watched.txt", "w+")
            p(f"Created {file}_watched.txt")

        if os.path.exists(f"{file[:file.index('.')]}_user_suggestion.txt") is True:
            self.file_user_suggested = open(f"{file[:file.index('.')]}_user_suggestion.txt", "r+")
            self.suggested_data = self.file_user_suggested.read().split("\n")
        else:
            self.file_user_suggested = open(f"{file[:file.index('.')]}_user_suggestion.txt", "w+")
            p(f"Created '{file[:file.index('.')]}_user_suggestion.txt'")
        self.file_watched.write(f"\n==========================\nStart Date: {self.run_date}\nEnd Date:\n==============================================\n")
        if os.path.exists("priority_users.txt"):
            self.priority_file = open(f"priority_users.txt", "r")
            for user in self.priority_file.read().split("\n"):
                if user != "":
                    self.priority_users.append(user)
            self.priority_file.close()
        else:
            self.priority_file = open(f"priority_users.txt", "w+").close()

        for suggestion in self.contents:
            if suggestion not in ["", "\n", " "]:
                data = suggestion.split(" | ")
                self.show_data.append([data[0], data[1]])
                self.show_data_len += 1

    def remove_from_list(self, refer, var, svar):
        # CODE
        svar.append(var)  # ;Puts referred var in a list
        refer.remove(var)  # ;Removes the var from the list

    def list_data(self, **options):
        # OPTIONS
        list_data_get = options.get("search", None)
        # CODE
        if self.debug_mode == 1:
            p("\t| DEBUG LIST DATA\n\t---------------------------------------------")
            for list_data in vars(self):
                if type(vars(self)[list_data]) is list or type(vars(self)[list_data]) is dict:
                    if list_data_get is None:
                        p(f"\t|\t{list_data}: {vars(self)[list_data]}")
                    else:
                        list_data_get_alternative_listing = options.get("use_alt_list", True)
                        if list_data == list_data_get:
                            if list_data_get_alternative_listing is True:
                                p(f"\t|\t{list_data}")
                                for nested_data in vars(self)[list_data]:
                                    p(f"\t|\t|\t{nested_data}: {vars(self)[list_data][nested_data]}")
                            else:
                                p(f"\t|\t{list_data}: {vars(self)[list_data]}")
            p("\t---------------------------------------------\n-------------------------------------------------")

    def save_to_counter_file_from_list(self, main_list, main_list_unknowns):
        # CODE
        with open(f"{self.filename[:self.filename.index('.')]}_user_suggestion.txt", "r") as counter_file:  # ;Opens the counter file (it should be FILE_user_suggestion.txt)
            counter_file_contents = counter_file.read()
            counter_file_table = counter_file_contents.split("\n")  # ;Converts string to list
            user_table = {}  # ;Usernames with counters
            for user in counter_file_table:  # ;Loops through the converted string
                if user not in ["", "\n", " "]:  # ;Filters unneeded content such as lines with just spaces, empty newlines and empty strings
                    user_data = user.split(": ")
                    user_table.update({user_data[0]: int(user_data[1])})

            for username in main_list:  # ;Loops through the usernames list
                if username in user_table.keys():  # ;Checks if the 'username' is in the 'user_table', if not skip this and put it in 'unknown_usernames'
                    user_table[username] += 1
                    counter_file_contents = counter_file_contents.replace(f"{username}: {user_table[username] - 1}\n", f"{username}: {user_table[username]}\n")
                else:
                    if username not in main_list_unknowns:  # ;Checks if the 'username' is in 'unknown_users', if not add it, this is only executed when the 'username' is not in the 'user_table'
                        main_list_unknowns.append(username)  # ;Add 'username' to 'unknown_users' list
                        counter_file_contents += f"{username}: 1\n"  # ;Add 'username' with the value of 1 to the 'counter_file_contents'
                        user_table.update({username: 1})  # ;Update the 'user_table' by adding the unknown username to the list with the value of 1
            write = counter_file_contents  # ;Transfer string to a new string
            counter_file.close()
        with open(f"{self.filename[:self.filename.index('.')]}_user_suggestion.txt", "w+") as new_data:  # ;Opens the 'FILE_user_suggestion.txt' with write access with updating functions (should clear the contents of the file)
            new_data.write(write)
            new_data.close()
        self.file.close()
        self.file_watched.close()
        self.file_user_suggested.close()

    def fill_end_date(self):
        with open(f"{self.filename[:self.filename.index('.')]}_watched.txt", "r") as history_file:
            history_data = history_file.read()
            history = history_data.split("\n")
            lnRepo = {}
            endDateRepo = []
            lc = 0  # ;Character Count
            ln = 0  # ;Line Number
            isTimeDataDone = False
            for a in range(len(history)):
                current_info = {}
                lc += len(str(history[a] + "\n").encode("utf-8"))
                isOldVersion = False  # ;True when the items contain usernames and movie only
                if not a + 4 >= len(history):
                    if history[a] == "==========================":
                        if history[a + 2] == "==========================" or history[a + 1].__contains__("Start Date"):
                            start_data = history[a:a + 3]
                            date = start_data[1]
                            date_name = ""
                            if history[a + 1].__contains__("Start Date: "):
                                start_data = history[a:a + 4]
                                start_date_location = lc + len(start_data[1])
                                start_date_location_list = ln + 1
                                end_date_location = lc + len(start_data[1] + start_data[2])
                                end_date_location_list = ln + 2
                                for date_dat in range(len(date[len("Start Date: "):])):
                                    date_dat_l = date[len("Start Date: ") + date_dat]
                                    if date_dat_l == "-":
                                        date_name += "_"
                                    elif date_dat_l == ":":
                                        date_name += "_"
                                    elif date_dat_l.isspace():
                                        date_name += "-"
                                    else:
                                        date_name += date_dat_l
                                # ;                               0   1                    2                         3                  4                       5
                                current_info.update({"location": [lc, start_date_location, start_date_location_list, end_date_location, end_date_location_list, ln], "isOld": isOldVersion, "suggestions": []})
                                endDateRepo.append(current_info["location"][2])
                            else:
                                isOldVersion = True
                                for date_dat in range(len(date)):
                                    date_dat_l = date[date_dat]
                                    if date_dat_l == "-":
                                        date_name += "_"
                                    elif date_dat_l == ":":
                                        date_name += "_"
                                    elif date_dat_l.isspace():
                                        date_name += "-"
                                    else:
                                        date_name += date_dat_l
                                current_info.update({"location": [lc, lc + len(date)], "isOld": isOldVersion, "suggestions": []})
                            lnRepo.update({date_name: current_info})
                            isTimeDataDone = True
                    elif history[a].__contains__("|") and isTimeDataDone:
                        if history[a].__contains__("<") and history[a].__contains__(">"):
                            if "suggestions" in lnRepo[date_name].keys():
                                lnRepo[date_name]["suggestions"].append(history[a])
                        elif "suggestions" in lnRepo[date_name].keys():
                            lnRepo[date_name]["suggestions"].append(history[a])
                    ln += 1
            history[lnRepo[date_name]["location"][4]] += f" {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
            lnRepo[date_name].update({"endDate": datetime.now().strftime('%Y-%m-%d %I:%M %p')})
            with open(f"{self.filename[:self.filename.index('.')]}_watched.txt", "w+") as history_file:
                for data in history:
                    history_file.write(data + "\n")

    def run(self):
        # LIST
        watched_shows_list = []  # ; Finished movies list
        usernames = []  # ;User list without counter
        unknown_users = []  # ;Names that aren't in the counter file go here
        # DICT
        user_data_dict = {}  # ;Counters
        while len(self.show_data) != 0:  # ;Continuous loop that will only stop when the entries on the show_data list is 0
            if self.debug_mode == 1:
                self.dbg_data.update({
                    "watched_shows_list": watched_shows_list,
                    "usernames": usernames,
                    "user_data_dict": user_data_dict,
                    "unknown_users": unknown_users
                })
            elif 'dbg_data' in vars(self).keys():
                del self.dbg_data  # ;Removes 'self.dbg_data' from this class since self.debug_mode isn't 1

            first = self.show_data[0]  # ;Points to the first thing on the list
            p(f"\nSeries: {first[0]}\nSuggested By: {first[1]}\n")  # ;Shows selected show/series with whom suggested it
            command = input("Done watching? ")  # ;Waits for confirmation from user if the show one/more are watching is done
            p("-------------------------------------------------")

            if first[1] not in user_data_dict:
                user_data_dict.update({first[1]: 1})
            else:
                user_data_dict[first[1]] += 1
            usernames.append(first[1])

            if command in ["e", "E"]:  # ;If the input equals 'e', then start quit program sequence
                if randint(1, 100000) == 2 / 100000:  # ;Added a little fun to the mix
                    p("The cycle is broken! :D")
                self.remove_from_list(self.show_data, first, watched_shows_list)
                self.file_watched.write(f"{first[0]} | {first[1]} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")
                p(f"\nShows watched: {len(watched_shows_list)}\n\nWatched Shows: {watched_shows_list}")  # ;Shows current information
                self.save_to_counter_file_from_list(usernames, unknown_users)
                self.file_watched.close()
                self.fill_end_date()
                break

            self.list_data(search="dbg_data", use_alt_list=True)

            self.remove_from_list(self.show_data, first, watched_shows_list)
            self.file_watched.write(f"{first[0]} | {first[1]} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")  # ;Saves the watched show/series with the user whom suggested it in a file for referrence
            p(f"\nShows watched: {len(watched_shows_list)}\n\nWatched Shows: {watched_shows_list}\n\nShows: {self.show_data}")  # ;Shows current information
            p("-------------------------------------------------")

            if len(self.show_data) == 0:
                p(f"Show List is empty\nSaving Usernames to {self.filename[:self.filename.index('.')]}_user_suggestion.txt")
                self.save_to_counter_file_from_list(usernames, unknown_users)
                self.fill_end_date()
                break


class MovieNight:
    """
    Optionals
    --------------------------
    debug_mode
        0 = Off <-- Default
        1 = Lists
    """

    def __init__(self, file, **options):
        # OPTIONS
        self.debug_mode = options.get("debug_mode", 0)
        self.debug_priority_users_autoskip_input = options.get("priority_users_autoskip_input", False)
        # FILE
        self.file = open(file, "r+")
        self.filename = file
        # INT
        self.movie_data_len = 0
        # LIST
        self.movie_data = []
        self.priority_users = []  # ;Priority Users mainly can call <MUST>
        self.contents = self.file.read().split("\n")
        # DICT
        self.dbg_data = {}
        # DATETIME
        self.run_date = f"{datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
        # CODE
        if os.path.exists(file):
            self.file_watched = open(f"{file[:file.index('.')]}_watched.txt", "a")
        else:
            self.file_watched = open(f"{file[:file.index('.')]}_watched.txt", "w+")
            p(f"Created {file}_watched.txt")

        if os.path.exists(f"{file[:file.index('.')]}_user_suggestion.txt"):
            self.file_user_suggested = open(f"{file[:file.index('.')]}_user_suggestion.txt", "r+")
            self.suggested_data = self.file_user_suggested.read().split("\n")
        else:
            self.file_user_suggested = open(f"{file[:file.index('.')]}_user_suggestion.txt", "w+")
            p(f"Created '{file[:file.index('.')]}_user_suggestion.txt'")
        self.file_watched.write(f"\n==========================\nStart Date: {self.run_date}\nEnd Date:\n==========================\n")

        if os.path.exists("priority_users.txt"):
            self.priority_file = open(f"priority_users.txt", "r")
            for user in self.priority_file.read().split("\n"):
                if user != "":
                    self.priority_users.append(user)
            self.priority_file.close()
        else:
            self.priority_file = open(f"priority_users.txt", "w+").close()

        for suggestion in self.contents:
            if suggestion not in ["", "\n", " "]:
                data = suggestion.split(" | ")
                self.movie_data.append([data[0], data[1]])
                self.movie_data_len += 1

    def remove_from_list(self, refer, var, saver):
        saver.append(var)  # ;Puts watched movie in watched_movies_list
        refer.remove(var)  # ;Removes currently picked movie from the mutable_movies_list

    def list_data(self, **options):
        # OPTIONS
        list_data_get = options.get("search", None)
        # CODE
        if self.debug_mode == 1:
            p("\t| DEBUG LIST DATA\n\t---------------------------------------------")
            for list_data in vars(self):
                if type(vars(self)[list_data]) is list or type(vars(self)[list_data]) is dict:
                    if list_data_get is None:
                        p(f"\t|\t{list_data}: {vars(self)[list_data]}")
                    else:
                        list_data_get_alternative_listing = options.get("use_alt_list", True)
                        if list_data == list_data_get:
                            if list_data_get_alternative_listing is True:
                                p(f"\t|\t{list_data}")
                                for nested_data in vars(self)[list_data]:
                                    p(f"\t|\t|\t{nested_data}: {vars(self)[list_data][nested_data]}")
                            else:
                                p(f"\t|\t{list_data}: {vars(self)[list_data]}")
            p("\t---------------------------------------------\n-------------------------------------------------")

    def fill_end_date(self):
        with open(f"{self.filename[:self.filename.index('.')]}_watched.txt", "r") as history_file:
            history_data = history_file.read()
            history = history_data.split("\n")
            lnRepo = {}
            endDateRepo = []
            lc = 0  # ;Character Count
            ln = 0  # ;Line Number
            isTimeDataDone = False
            for a in range(len(history)):
                current_info = {}
                lc += len(str(history[a] + "\n").encode("utf-8"))
                isOldVersion = False  # ;True when the items contain usernames and movie only
                if not a + 4 >= len(history):
                    if history[a] == "==========================":
                        if history[a + 2] == "==========================" or history[a + 1].__contains__("Start Date"):
                            start_data = history[a:a + 3]
                            date = start_data[1]
                            date_name = ""
                            if history[a + 1].__contains__("Start Date: "):
                                start_data = history[a:a + 4]
                                start_date_location = lc + len(start_data[1])
                                start_date_location_list = ln + 1
                                end_date_location = lc + len(start_data[1] + start_data[2])
                                end_date_location_list = ln + 2
                                for date_dat in range(len(date[len("Start Date: "):])):
                                    date_dat_l = date[len("Start Date: ") + date_dat]
                                    if date_dat_l == "-":
                                        date_name += "_"
                                    elif date_dat_l == ":":
                                        date_name += "_"
                                    elif date_dat_l.isspace():
                                        date_name += "-"
                                    else:
                                        date_name += date_dat_l
                                # ;                               0   1                    2                         3                  4                       5
                                current_info.update({"location": [lc, start_date_location, start_date_location_list, end_date_location, end_date_location_list, ln], "isOld": isOldVersion, "suggestions": []})
                                endDateRepo.append(current_info["location"][2])
                            else:
                                isOldVersion = True
                                for date_dat in range(len(date)):
                                    date_dat_l = date[date_dat]
                                    if date_dat_l == "-":
                                        date_name += "_"
                                    elif date_dat_l == ":":
                                        date_name += "_"
                                    elif date_dat_l.isspace():
                                        date_name += "-"
                                    else:
                                        date_name += date_dat_l
                                current_info.update({"location": [lc, lc + len(date)], "isOld": isOldVersion, "suggestions": []})
                            lnRepo.update({date_name: current_info})
                            isTimeDataDone = True
                    elif history[a].__contains__("|") and isTimeDataDone:
                        if history[a].__contains__("<") and history[a].__contains__(">"):
                            if "suggestions" in lnRepo[date_name].keys():
                                lnRepo[date_name]["suggestions"].append(history[a])
                        elif "suggestions" in lnRepo[date_name].keys():
                            lnRepo[date_name]["suggestions"].append(history[a])
                    ln += 1
            history[lnRepo[date_name]["location"][4]] += f" {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
            lnRepo[date_name].update({"endDate": datetime.now().strftime('%Y-%m-%d %I:%M %p')})
            with open(f"{self.filename[:self.filename.index('.')]}_watched.txt", "w+") as history_file:
                for data in history:
                    history_file.write(data + "\n")

    def save_to_counter_file_from_list(self, main_list, main_list_unknowns):
        # CODE
        with open(f"{self.filename[:self.filename.index('.')]}_user_suggestion.txt", "r") as counter_file:  # ;Opens the counter file (it should be FILE_user_suggestion.txt)
            counter_file_contents = counter_file.read()
            counter_file_table = counter_file_contents.split("\n")  # ;Converts string to list
            user_table = {}  # ;Usernames with counters
            for user in counter_file_table:  # ;Loops through the converted string
                if user not in ["", "\n", " "]:  # ;Filters unneeded content such as lines with just spaces, empty newlines and empty strings
                    user_data = user.split(": ")
                    user_table.update({user_data[0]: int(user_data[1])})

            for username in main_list:  # ;Loops through the usernames list
                if username in user_table.keys():  # ;Checks if the 'username' is in the 'user_table', if not skip this and put it in 'unknown_usernames'
                    user_table[username] += 1
                    counter_file_contents = counter_file_contents.replace(f"{username}: {user_table[username] - 1}\n", f"{username}: {user_table[username]}\n")
                else:
                    if username not in main_list_unknowns:  # ;Checks if the 'username' is in 'unknown_users', if not add it, this is only executed when the 'username' is not in the 'user_table'
                        main_list_unknowns.append(username)  # ;Add 'username' to 'unknown_users' list
                        counter_file_contents += f"{username}: 1\n"  # ;Add 'username' with the value of 1 to the 'counter_file_contents'
                        user_table.update({username: 1})  # ;Update the 'user_table' by adding the unknown username to the list with the value of 1
            write = counter_file_contents  # ;Transfer string to a new string
            counter_file.close()
        with open(f"{self.filename[:self.filename.index('.')]}_user_suggestion.txt", "w+") as new_data:  # ;Opens the 'FILE_user_suggestion.txt' with write access with updating functions (should clear the contents of the file)
            new_data.write(write)
            new_data.close()
        self.file.close()
        self.file_watched.close()
        self.file_user_suggested.close()

    def roll_dice(self):
        # LIST
        watched_movies_list = []  # ;Finished movies list
        usernames = []  # ;User list without counter (it's literally 'watched_movies_list' without the movie being added)
        unknown_users = []  # ;Names that aren't in the counter file go here
        priority_failed_attempts = []
        # DICT
        user_data_dict = {}  # ;Counters
        # CODE
        p("Checking for called priorities")
        if len(self.priority_users) != 0:
            for i in range(len(self.movie_data)+1): # ;Act as an updater, because there is a bug where it skips the next suggestion since that the suggestion got removed
                for suggestion in self.movie_data:
                    suggestion_s = suggestion[0].split("^")  # ; Splitted
                    movie_raw = suggestion[0]
                    user = suggestion[1]
                    if user in self.priority_users:
                        if len(suggestion_s) > 1:
                            if suggestion_s[-1] == "":
                                suggestion_s.pop(-1)
                            flags = suggestion_s[1]
                            movie = suggestion_s[0]
                            if movie[-1].isspace():
                                suggestion_s[0] = movie[:-1]
                                movie = suggestion_s[0]
                            if flags in ["PRIORITY", "MUST", "MUST_WATCH"] and movie_raw not in [x[0] for x in watched_movies_list]: # ;skips a suggestion that's already been looped over
                                if self.debug_mode == 1:
                                    self.dbg_data({
                                        "watched_movies_list": watched_movies_list,
                                        "usernames": usernames,
                                        "user_data_dict": user_data_dict,
                                        "unknown_users": unknown_users
                                    })
                                elif 'dbg_data' in vars(self).keys():
                                    del self.dbg_data
                                makeBox(f"Movie Picked: '{movie}'\nSuggested By: {user}")
                                makeBox(f"Tagged as: {flags}")
                                if self.debug_priority_users_autoskip_input is False:
                                    command = input("Is movie done? ")
                                else:
                                    command = ""
                                p("-------------------------------------------------")
                                if user not in user_data_dict:
                                    user_data_dict.update({user: 1})
                                else:
                                    user_data_dict[user] += 1
                                usernames.append(user)
                                if command in ["e", "E"]:  # ;If the input equals 'e', then start quit program sequence
                                    p("The cycle is broken! :D", cond=randint(1, 100000), value=2 / 100000)
                                    self.remove_from_list(self.movie_data, suggestion, watched_movies_list)
                                    self.file_watched.write(f"{movie_raw} | {user} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")  # ;Save the watched movie with whom suggested it in a file for referrence
                                    p(f"\nMovies watched: {len(watched_movies_list)}\nWatched Movies: {watched_movies_list}\nMovie List: {self.movie_data}\n")  # ;Shows current information
                                    p(f"Saving Suggestion counters to {self.filename[:self.filename.index('.')]}_user_suggestion.txt")
                                    self.save_to_counter_file_from_list(usernames, unknown_users)
                                    self.file_watched.close()
                                    self.fill_end_date()
                                    exit()
                                self.list_data(search="dbg_data", use_alt_list=True)
                                self.remove_from_list(self.movie_data, suggestion, watched_movies_list)
                                self.file_watched.write(f"{movie_raw} | {user} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")  # ;Save the watched movie with whom suggested it in a file for referrence
                                p(f"\nMovies watched: {len(watched_movies_list)}\n\nWatched Movies: {watched_movies_list}\n\nMovie List: {self.movie_data}\n")  # ;Shows current information
                                p("-------------------------------------------------")
                                if len(self.movie_data) == 0:
                                    p(f"Show List is empty\nSaving Suggestion counters to {self.filename[:self.filename.index('.')]}_user_suggestion.txt")
                                    self.save_to_counter_file_from_list(usernames, unknown_users)
                                    self.fill_end_date()
                                    exit()
                    elif len(suggestion_s) > 1:
                        if suggestion_s[-1] == "":
                            suggestion_s.pop(-1)
                        flags = suggestion_s[1]
                        if flags in ["PRIORITY", "MUST", "MUST_WATCH"] and self.movie_data[self.movie_data.index(suggestion)] not in priority_failed_attempts:
                            if suggestion_s[-1].isspace():
                                suggestion_s[0] = suggestion_s[:-1]
                            priority_failed_attempts.append(self.movie_data[self.movie_data.index(suggestion)])
                            self.movie_data[self.movie_data.index(suggestion)][0] = suggestion_s[0]
                            p(f'"{user}" has attempted to call the priority command when they do not have the permission to')
        del priority_failed_attempts
        p("Done with priority calls\n")
        while len(self.movie_data) != 0:  # ;Continuous loop that will only stop when the entries on the 'show_data' list is 0
            if self.debug_mode == 1:
                self.dbg_data({
                    "watched_movies_list": watched_movies_list,
                    "usernames": usernames,
                    "user_data_dict": user_data_dict,
                    "unknown_users": unknown_users
                })
            elif 'dbg_data' in vars(self).keys():
                del self.dbg_data

            pick = choice(self.movie_data)  # ;Chooses movie randomly
            pick_movie = pick[0]  # ;Movie
            pick_suggested_by = pick[1]  # ;Gets the user who suggested the movie
            p(f"Movie Picked '{pick_movie}'\nSuggested By: {pick_suggested_by}\n")  # ;Chooses movie randomly and shows who suggested it with when it was picked
            command = input("Is movie done? ")  # ;Waits for confirmation from user if the show one/more are watching is done
            p("-------------------------------------------------")

            if pick_suggested_by not in user_data_dict:
                user_data_dict.update({pick_suggested_by: 1})
            else:
                user_data_dict[pick_suggested_by] += 1
            usernames.append(pick_suggested_by)

            if command in ["e", "E"]:  # ;If the input equals 'e', then start quit program sequence
                p("The cycle is broken! :D", cond=randint(1, 100000), value=2 / 100000)
                self.remove_from_list(self.movie_data, pick, watched_movies_list)
                self.file_watched.write(f"{pick_movie} | {pick_suggested_by} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")  # ;Save the watched movie with whom suggested it in a file for referrence
                p(f"\nMovies watched: {len(watched_movies_list)}\nWatched Movies: {watched_movies_list}\nMovie List: {self.movie_data}\n")  # ;Shows current information
                p(f"Saving Suggestion counters to {self.filename[:self.filename.index('.')]}_user_suggestion.txt")
                self.save_to_counter_file_from_list(usernames, unknown_users)
                self.file_watched.close()
                self.fill_end_date()
                break

            self.list_data(search="dbg_data", use_alt_list=True)

            self.remove_from_list(self.movie_data, pick, watched_movies_list)
            self.file_watched.write(f"{pick_movie} | {pick_suggested_by} <{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")  # ;Save the watched movie with whom suggested it in a file for referrence
            p(f"\nMovies watched: {len(watched_movies_list)}\n\nWatched Movies: {watched_movies_list}\n\nMovie List: {self.movie_data}\n")  # ;Shows current information
            p("-------------------------------------------------")

            if len(self.movie_data) == 0:
                p(f"Show List is empty\nSaving Suggestion counters to {self.filename[:self.filename.index('.')]}_user_suggestion.txt")
                self.save_to_counter_file_from_list(usernames, unknown_users)
                self.fill_end_date()
                break
