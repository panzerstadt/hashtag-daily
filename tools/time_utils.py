import datetime, time


def str_2_datetime(str_in, input_format='%Y-%m-%d', timezone='JST'):
    return datetime.datetime.strptime(str_in, input_format)


def datetime_2_str(datetime_in, output_format='%Y-%m-%d'):
    return time.strftime(output_format, datetime_in.timetuple())