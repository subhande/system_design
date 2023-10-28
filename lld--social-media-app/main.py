from __future__ import annotations
from enum import Enum
from decimal import Decimal
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Dict
from uuid import uuid4
import time

class PostType(Enum):
    TWEET: str = "tweet"
    COMMENT: str = "comment"

class LikeType(Enum):
    HEART: str = "heart"
    THUMBS_UP: str = "thumbs_up"
    THUMBS_DOWN: str = "thumbs_down"
    AWESOME: str = "awesome"
    SAD: str = "sad"

class User:
    def __init__(self, name: str, userId: str, email: str, password: str, content: str):
        self.name = name
        self.user_id = userId
        self.email = email
        self.password = password
        self.content = content

class RegisteredAccount(User):
    pass

class Like:
    def __init__(self, user: RegisteredAccount, type: PostType, likeType: LikeType):
        self.user = user
        self.type = type
        self.like_type = likeType

class Comment:
    def __init__(self, ra: RegisteredAccount, content: str, likes: List[Like]):
        self.ra = ra
        self.content = content
        self.likes = likes

    def showComment(self):
        print(self.content)

    def addLike(self, u: RegisteredAccount, likeType: LikeType):
        self.likes.append(Like(u, PostType.COMMENT, likeType))

    def removeLike(self, u: RegisteredAccount):
        # Remoive like where use of like is u
        pass

class CommentThread:
    def __init__(self, threadId: str, commentList: List[Comment]):
        self.threadId = threadId
        self.commentList = commentList

    def comments(self):
        return self.commentList
    
    def addComment(self, c: Comment):
        self.commentList.append(c)


class Tweet:
    def __init__(self, user: RegisteredAccount, contnet: str, hastags: List[str], taggedUsers: List[str], commentThread: Dict[str, CommentThread], like: List[RegisteredAccount]):
        self.tweetId = str(uuid4())
        self.user = user
        self.tweetTime = time.time()
        self.content = contnet
        self.hashtags = hastags
        self.taggedUsers = taggedUsers
        self.commentThread = commentThread
        self.likes = like

    def getContent(self):
        return self.content
    
    def comment(self, threadId: str, c: Comment):
        if threadId not in self.commentThread:
            self.commentThread[threadId] = CommentThread(str(uuid4()), [])
        self.commentThread[threadId].addComment(c)

    def addLike(self, u: RegisteredAccount, likeType: LikeType):
        self.likes.append(Like(u, PostType.TWEET, likeType))

    def removeLike(self, u: RegisteredAccount):
        # Remoive like where use of like is u
        pass

    def isCelebTweet(self):
        return self.user.isCelebrity()
    

class TimeLineWall:
    def __init__(self, tweets: List[Tweet]):
        self.tweets = tweets

    def addTweet(self, t: Tweet):
        self.tweets.append(t)

    def removeTweet(self, t: Tweet):
        self.tweets.remove(t)
    
class TimeLine(TimeLineWall):
    def showTimeline(self):
        return self.tweets
    
    def addCelebTweet(self, celebTweets: List[Tweet]):
        self.tweets.extend(celebTweets)


class Wall(TimeLineWall):
    def showWall(self):
        return self.tweets

    
    
class ContnetServer:
    subcriberList: Dict[RegisteredAccount, List[RegisteredAccount]] = {}
    celebritiesTweet: Dict[RegisteredAccount, List[Tweet]] = {}

    def getCelebPosts(self):
        return self.celebritiesTweet

    def addSubscriber(self, followee: RegisteredAccount, follower: RegisteredAccount):
        if followee not in self.subcriberList:
            self.subcriberList[followee] = []
        self.subcriberList[followee].append(follower)

    def sendMessage(self, followee: RegisteredAccount, t: Tweet):
        if not followee.isCelebrity():
            for follower in self.subcriberList[followee]:
                follower.getTimeLine().addTweet(t)

        else:
            if followee not in self.celebritiesTweet:
                self.celebritiesTweet[followee] = []
            self.celebritiesTweet[followee].append(t)

class RegisteredAccount(User):
    def __init__(self, name: str, userId: str, email: str, password: str, content: str):
        super().__init__(name, userId, email, password, content)
        
        self.followers = []
        self.following = []
        self.isCelebrity = False
        self.timeLine = TimeLine([])
        self.wall = Wall([])
        # self.contentServer = ContnetServer()

    def getTimeLine(self):
        return self.timeLine
    
    def checkCelebrity(self):
        return self.followers > 1000
        # return self.isCelebrity

    def viewTweet(self, t: Tweet):
        return t.getContent()
    
    def addTweet(self, t: Tweet):
        self.wall.addTweet(t)
        # self.contentServer.sendMessage(self, t)
    
    def postTweet(self, t: Tweet, contentServer: ContnetServer):
        self.feedwall.addTweet(t)
        contentServer.sendMessage(self, t)

    def showTimeline(self, contentServer: ContnetServer):
        self.nonCelebTweets: self.timeLine.getTweets()
        self.celebTweets = []

        for i, followee in enumerate(self.following):
            if followee.checkCelebrity():
                self.celebTweets.extend(contentServer.getCelebPosts()[i]) 
        self.nonCelebTweets.extend(self.celebrities)

    def addFollower(self,c: ContnetServer, ra: RegisteredAccount):

        self.addFollowers(ra)
        self.followers.append(ra)

    def followUser(self, c: ContnetServer, ra: RegisteredAccount):
        c.addFollower(ra, self)
    
    

