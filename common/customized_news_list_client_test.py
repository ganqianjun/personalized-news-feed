import customized_news_list_client as client

def test_basic():
    # before run this test, make sure the click log for 'user_id' exists in db
    user_id = "ganqianjun@outlook.com"
    news_description = ["FBI director nominee Christopher Wray tells Sen. Lindsey on that the Russia controversy the Russia controversy is a",
         "1o2iuoiu09 bljk2j3kj 09809adlkjfd",
         "Today, some world\u2019s biggest internet companies and activist groups are coming together to protest the rollback of net neutrality protections",
         "Trump also said he gets along 'very, very well' with PutinTrump also said he gets along 'very, very well' with Putin"]
    click_predict = client.predict_news_click(user_id, news_description)
    print click_predict
    assert 1
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
