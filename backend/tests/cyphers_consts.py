from backend.utils.schemas import User, Hobby, RequestUser, RequestHobby

TEST_USER_1_REQUEST = RequestUser(**{
    "name": "user1",
    "first_name": "user",
    "last_name": "one",
    "nickname": "one1", })
TEST_USER_1 = User(**TEST_USER_1_REQUEST.dict(), id=0)

TEST_USER_2_REQUEST = RequestUser(**{"name": "user2",
                                     "first_name": "user",
                                     "last_name": "two",
                                     "nickname": "two2"})
TEST_USER_2 = User(**TEST_USER_2_REQUEST.dict(), id=1)

TEST_USER_3_REQUEST = RequestUser(**{"name": "user3",
                                     "first_name": "user",
                                     "last_name": "three",
                                     "nickname": "None"})
TEST_USER_3 = User(**TEST_USER_3_REQUEST.dict(), id=2)

TEST_USER_4_REQUEST = RequestUser(**{"name": "user4",
                                     "first_name": "user",
                                     "last_name": "four",
                                     "nickname": "four4"})
TEST_USER_4 = User(**TEST_USER_4_REQUEST.dict(), id=3)

TEST_USER_5_REQUEST = RequestUser(**{"name": "user5",
                                     "first_name": "user",
                                     "last_name": "five",
                                     "nickname": "five5"})
TEST_USER_5 = User(**TEST_USER_5_REQUEST.dict(), id=7)

TEST_HOBBY_1_REQUEST = RequestHobby(**{"name": "hobby1",
                                       "description": "one"})
TEST_HOBBY_1 = Hobby(**TEST_HOBBY_1_REQUEST.dict(), id=4)

TEST_HOBBY_2_REQUEST = RequestHobby(**{"name": "hobby2",
                                       "description": "two"})
TEST_HOBBY_2 = Hobby(**TEST_HOBBY_2_REQUEST.dict(), id=5)

TEST_HOBBY_3_REQUEST = RequestHobby(**{"name": "hobby3",
                                       "description": "three"})
TEST_HOBBY_3 = Hobby(**TEST_HOBBY_3_REQUEST.dict(), id=6)

TEST_HOBBY_4_REQUEST = RequestHobby(**{"name": "hobby4",
                                       "description": "four"})
TEST_HOBBY_4 = Hobby(**TEST_HOBBY_4_REQUEST.dict(), id=8)

TEST_RELATION_1 = (0, 6)  # (id:0) - [INTERESTED] -> (id:6)
TEST_RELATION_2 = (0, 5)  # (id:0) - [INTERESTED] -> (id:5)
TEST_RELATION_3 = (1, 5)  # (id:1) - [INTERESTED] -> (id:5)
TEST_RELATION_4 = (2, 6)  # (id:2) - [INTERESTED] -> (id:6)
TEST_RELATION_5 = (3, 4)  # (id:3) - [INTERESTED] -> (id:4)

USERS_TO_ADD = [TEST_USER_1_REQUEST, TEST_USER_2_REQUEST, TEST_USER_3_REQUEST, TEST_USER_4_REQUEST]
HOBBIES_TO_ADD = [TEST_HOBBY_1_REQUEST, TEST_HOBBY_2_REQUEST, TEST_HOBBY_3_REQUEST]

RELATIONS_TO_ADD = [TEST_RELATION_1, TEST_RELATION_2, TEST_RELATION_3, TEST_RELATION_4, TEST_RELATION_5]
