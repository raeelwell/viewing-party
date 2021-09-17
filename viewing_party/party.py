
#initialize/create movie to add to list

def create_movie(movie_title, genre, rating):
    if movie_title and genre and rating:
        movie_dict = {
        "title" : movie_title,
        "genre" : genre,
        "rating" : rating}
        return movie_dict
    else:
        return None

#add a movie to watchlist
#user_data is a dictionary with "watched" key and a list of dictionaries of each movie as the value
#movie is the dictionary of movies made in create_movie
#add movie to user_data list

def add_to_watched(user_data, movie):
    user_data["watched"].append(movie)
    return user_data

def add_to_watchlist(user_data, movie):
    user_data["watchlist"].append(movie)
    return user_data

def watch_movie(user_data, title):
    watchlist = user_data["watchlist"]
    for movie in watchlist:
        if movie["title"] == title:
            title = movie
    if title in user_data["watchlist"]:
        user_data["watchlist"].remove(title)
        user_data["watched"].append(title)
            
    return user_data

def get_watched_avg_rating(user_data):
    watched = user_data["watched"]
    sum=0
    count=0
    if watched == []:
        print(watched)
        return 0.0
    else:
        for movie in watched:
            sum+=movie["rating"]
            count+=1
        avg=sum/count
        return avg


##to get the most watched genre from the dict inside user_list
##make a dict of each genre key with value set to 1
##increment value each time genre repeats
##return key with highest value count

def get_most_watched_genre(user_data):
    watched = user_data["watched"]
    if watched == []:
        return None
    else:
        genre_dict={}
        for movie in watched:
            if movie["genre"] not in genre_dict:
                genre_dict[movie["genre"]] = 1
            if movie["genre"] in genre_dict:
                genre_dict[movie["genre"]] += 1
        most_watched_genre = max(genre_dict, key=genre_dict.get)

        return most_watched_genre


##takes user_data which is a dictionary with keys: 'watched' and 'friends' 
##the value of 'watched' is a list of dictionaries with 'title' and movie title as key and value
##the value of 'friends' is a list of dictionaries with 'watched' as keys with the values being a list of movie dicts
##return a list of dictionaries - movies that the user has watched but friends have not watched

##return movies value to a set for both user and friends (mult. friends in one)
##run difference between sets

def get_unique_watched(user_data):
    user_watched=set()
    friends_watched=set()
    for movie in user_data["watched"]:
        user_watched.add(movie["title"])
    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            friends_watched.add(movie["title"])
    unique_watched=user_watched.difference(friends_watched)

    result_list=[]

    for movie in unique_watched:
        for user_watched_movie in user_data["watched"]:
            if movie in user_watched_movie["title"]:
                result_list.append(user_watched_movie)

    return result_list


def get_friends_unique_watched(user_data):
    user_watched=set()
    friends_watched=set()
    for movie in user_data["watched"]:
        user_watched.add(movie["title"])
    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            friends_watched.add(movie["title"])
    unique_watched=friends_watched.difference(user_watched)

    temp_list=[]
    result_list=[]

    for movie in unique_watched:
        for friend in user_data["friends"]:
            for friend_watched_movie in friend["watched"]:
                if movie in friend_watched_movie["title"]:
                    temp_list.append(friend_watched_movie)
    
    for i in range(0, len(temp_list)):
        if temp_list[i] not in temp_list[i+1:]:
            result_list.append(temp_list[i])
            
    return result_list


##Wave 4

##user_data is a dictionary with an entry with key "subscriptions". Value is which services user has
##also has key "watched". Value is movies user has watched
##also has key "friends". Value has a key "watched" which contains value of a dictionary representing a movie
##friends -> watched -> dictionary has title and host as keys, and movie title and service as values, respectively
##get movie recommendations based on movies the user has NOT seen and friends HAVE seen, that also has same subscriptions

##use get_friends_unique_watched

def get_available_recs(user_data):
    unique_watched=get_friends_unique_watched(user_data)
    movie_rec=[]

    for unique_movie in unique_watched:
        if unique_movie["host"] in user_data["subscriptions"]:
            movie_rec.append(unique_movie)
    return movie_rec


##counts the user's most watched genre
##recommends movies friends have seen that are in the genre that the user hasn't seen

def get_new_rec_by_genre(user_data):
    genre=get_most_watched_genre(user_data)

    unique_watched=get_friends_unique_watched(user_data)
    rec_list=[]

    for unique_movie in unique_watched:
        if unique_movie["genre"] == genre:
            rec_list.append(unique_movie)    
    return rec_list


#user_data has field: favorites
#value of favorites is list of movie dictionaries
#generate list of recommended movies if it is in user's favorites and none of user's friends have seen it
#return list

def get_rec_from_favorites(user_data):
    unique_watched=get_unique_watched(user_data)

    rec_list=[]

    for favorite in user_data["favorites"]:
        if favorite in unique_watched:
            rec_list.append(favorite)

    return rec_list