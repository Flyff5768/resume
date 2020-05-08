import json

# .py
import Spades_Team.line.line_notify_message as line_notify
import Spades_Team.database.db_mongodb as my_mongodb
# pip
import pandas as pd







def main():


    my_mongodb.connect_mongodb("spades", "place")
    my_mongodb.mongodb_summary()

    df = pd.DataFrame(my_mongodb.mongodb_find())

    print(df)





if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')