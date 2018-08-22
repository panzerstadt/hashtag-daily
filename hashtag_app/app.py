from flask import Flask, request, jsonify
from tools.baseutils import textify
import time, datetime, pytz
import schedule
from threading import Thread

from tools.twitter_api import get_top_trends_from_twitter, get_top_hashtags_from_twitter
from tools.db_utils import make_db, load_db, update_db
from tools.time_utils import datetime_2_str, str_2_datetime

# pretty interface
from flasgger import Swagger

application = Flask(__name__)
swagger = Swagger(application)
application.config.update(JSON_AS_ASCII=False,
                          JSONIFY_PRETTYPRINT_REGULAR=True)

start_time = time.time()
update_start = time.time()
time_format_full_no_timezone = '%Y-%m-%d %H:%M:%S'
jp_timezone = pytz.timezone('Asia/Tokyo')

DATABASE_PATH = './db/daily_database.json'
DATABASE_STRUCTURE = {
    "trends": {
        "include_hashtags": {
            "timestamp": '1999-01-01 00:00:00',
            "initial_timestamp": datetime_2_str(datetime.datetime.now(), output_format=time_format_full_no_timezone),
            "content": []
        },
        "exclude_hashtags": {
            "timestamp": '1999-01-01 00:00:00',
            "initial_timestamp": datetime_2_str(datetime.datetime.now(), output_format=time_format_full_no_timezone),
            "content": []
        }
    },
    "hashtags": {
        "timestamp": '1999-01-01 00:00:00',
        "initial_timestamp": datetime_2_str(datetime.datetime.now(), output_format=time_format_full_no_timezone),
        "content": []
    }
}

REFRESH_MINS = 15


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def get_twitter_trends():
    print("Elapsed time: " + str(time.time() - start_time))
    print('calling twitter API to get trends')

    get_top_trends_from_twitter(country='Japan', cache_duration_mins=REFRESH_MINS-1)

    pass


def get_twitter_extended_hashtags():
    print("Elapsed time: " + str(time.time() - start_time))
    print('calling twitter API to build hashtags')

    get_top_hashtags_from_twitter(country='Japan', cache_duration_mins=REFRESH_MINS-1)


def get_updates_from_twitter():
    update_start = time.time()

    get_twitter_trends()
    #get_twitter_extended_hashtags()

    print("total update time took: {} seconds".format(str(time.time() - update_start)))



# only POST
@application.route('/', methods=['GET'])
def daily():
    print("time since app start: {} minutes".format(str((time.time() - start_time) / 60)))
    print("time since last update: {} minutes".format(str((time.time() - update_start) / 60)))

    full_db = load_db(database_path=DATABASE_PATH)

    #print(full_db)

    return "hello {}".format('WAIT')


@application.route('/twitter/hashtags')
def hashtags_twitter_only():
    """
        get list of latest tweets, locations, sentiment, and time
        ---
        parameters:
          - name: location
            in: query
            type: string
            required: true
            default: osaka
        responses:
          200:
            description: returns a json list of tweets
            schema:
              id: predictionGet
              properties:
                results:
                  type: json
                  default: setosa
                status:
                  type: number
                  default: 200
    """
    print("time since app start: {} minutes".format(str((time.time() - start_time) / 60)))
    print("time since last update: {} minutes".format(str((time.time() - update_start) / 60)))

    full_db = load_db(database_path=DATABASE_PATH)

    direct_hashtags_from_trends = full_db['trends']['include_hashtags']['content']

    output = []
    for t in direct_hashtags_from_trends:
        output.append(t['label'])

    output_str = '<br />'.join(output)
    return textify(output_str)


@application.route('/db', methods=['GET'])
def all():
    full_db = load_db(database_path=DATABASE_PATH)

    db_init_timestamp = str_2_datetime(full_db['trends']['include_hashtags']['initial_timestamp'], input_format=time_format_full_no_timezone)
    db_init_timestamp = db_init_timestamp.astimezone(tz=jp_timezone)
    db_update_timestamp = str_2_datetime(full_db['trends']['include_hashtags']['timestamp'], input_format=time_format_full_no_timezone)
    db_update_timestamp = db_update_timestamp.astimezone(tz=jp_timezone)

    print("time since app start: {:.2f} minutes".format((time.time() - start_time) / 60))
    print("time since database init: {:.2f} hours".format((datetime.datetime.now(tz=jp_timezone) - db_init_timestamp).seconds/3600))
    print("time since last update: {:.2f} minutes".format((datetime.datetime.now(tz=jp_timezone) - db_update_timestamp).seconds/60))

    return jsonify(full_db)


if __name__ == '__main__':
    make_db(DATABASE_STRUCTURE, debug=True)
    get_updates_from_twitter()

    schedule.every(REFRESH_MINS).minutes.do(get_updates_from_twitter)
    t = Thread(target=run_schedule)
    t.start()
    print("Start time: " + str(start_time))
    application.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    print('a flask app is initiated at {0}'.format(application.instance_path))


