from random import shuffle, randint, sample
from itertools import combinations
from queue import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
            return 0
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
            return 0
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)
            return 1

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        if numUsers <= avgFriendships:
            print("WARNING: Number of users must be greater than average friendships")
            return

        # Add users
        for user in range(numUsers):
            self.addUser(user)
        #####################
        # Original Create friendships
        #####################
        # possible_friendships = list(combinations(range(1, numUsers+1), 2))
        # shuffle(possible_friendships)
        # for num in range((numUsers*avgFriendships)//2):
        #     friendship = possible_friendships[num]
        #     self.addFriendship(friendship[0], friendship[1])

        #########################################
        # Refactor for adding friendships stretch
        #########################################
        # numFriends = 0
        # while numFriends < numUsers*avgFriendships//2:
        #     friends_added = self.addFriendship(
        #         randint(1, numUsers), randint(1, numUsers))
        #     numFriends += friends_added

        #########################################
        # Refactor adding friendships for fun
        #########################################
        numFriends = 0
        possible_choices = set(range(1, numUsers+1))
        already_friends = {}
        for user in self.users:
            # set self equal to max user
            # ie friend 1 = 100 only 99 choices for friend 1
            # friend 1 can't be friends with self so we set it to 100
            already_friends[user] = {user: numUsers}
        numFriendships = numUsers*avgFriendships//2
        while numFriends < numFriendships:
            print('test', already_friends)
            # pull first friend from friends not maxed on friends
            friend1 = sample(possible_choices, 1)[0]
            # Set number of possibilities for friend 2
            # number of users - length of already friends with user
            # ie. friend 100 cant be friends with self possible choices = 1-99
            second_friend_number_of_choices = numUsers - \
                len(already_friends[friend1])
            # pick random number from choices for friend 2
            friend2 = randint(1, second_friend_number_of_choices)
            # if friend2 already friends with friend 1 retrieve alternate value
            if already_friends[friend1].get(friend2):
                # ie friend1 = 1 and friend2 = 1.
                # retrieves and sets friend2 to 100
                friend2 = already_friends[friend1].get(friend2)
                print('friend', friend2, friend1)
                # add friendship
                addFriend = self.addFriendship(friend1, friend2)
                numFriends += addFriend
                # since we remove one choice from second friend number of choices we need to reset the number we took to second friend number of choices
                # ie friend2 => 1 => 100 but now needs to be set to 99
                already_friends[friend1][friend2] = second_friend_number_of_choices
                already_friends[friend2][friend1] = numUsers - \
                    len(already_friends[friend2])
            # if friend1 not already friends with friend2
            else:
                print('friend', friend2, friend1)
                addFriend = self.addFriendship(friend1, friend2)
                numFriends += addFriend
                already_friends[friend1][friend2] = second_friend_number_of_choices
                already_friends[friend2][friend1] = numUsers - \
                    len(already_friends[friend2])

            # remove friends from list of possible choices when maxed on friends
            print('num of friends', friend1, len(already_friends[friend1]), friend2, len(
                already_friends[friend2]))
            if len(already_friends[friend1]) == numUsers:
                possible_choices.remove(friend1)
                print('choice', possible_choices)
            if len(already_friends[friend2]) == numUsers:
                possible_choices.remove(friend2)
                print('choice', possible_choices)

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        queue = Queue()
        queue.put([userID])
        while not queue.empty():
            path = queue.get()
            node = path[-1]
            if node not in visited:
                visited[node] = path
                for next_friend in self.friendships[node]:
                    queue.put(path + [next_friend])
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(3, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
    # testing question 2 of part 3 below
    # test = SocialGraph()
    # test.populateGraph(1000, 5)
    # test_connections = test.getAllSocialPaths(1)
    # print(len(test_connections))
    # degree_of_sep = []
    # for key in test_connections:
    #     degree_of_sep.append(len(test_connections[key]))
    # print(sum(degree_of_sep)/len(degree_of_sep))
