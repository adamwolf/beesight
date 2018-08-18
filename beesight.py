def csv_to_todays_minutes(csv_lines):
    minutes = int(0)

    # skip first two header lines
    config = configparser.RawConfigParser()
    logger.debug ("Reading config file %s", CONFIG_FILE_NAME)
    config.read(CONFIG_FILE_NAME)
    timezone_offset = int(config.get(INSIGHT_SECTION, "utc_timezone"))

    logger.info("Parsing last four sessions from CSV:")
    # try to read the last four entries
    try:
        for l in csv_lines[2:6]:
            line = l.split(",")
            datetime_part = line[0]
            duration_part = line[1]
            activity_part = line[2]
            if "Meditation" not in activity_part:
                continue 
            d_h, d_m, d_s= duration_part.split(":")
            minutes_entry = 60 * int(d_h) + int(d_m) + (1 if int(d_s) >= 30 else 0)
            logger.info ("%s : %s minutes", datetime_part, minutes_entry)
            date_part, time_part = datetime_part.split(" ")
            date_parts = date_part.split("/")
            time_parts = time_part.split(":")
            if len(date_parts) == 3 and len(time_parts) == 3:
                m, d, y = map(int, date_parts)
                h, _, _ = map(int, time_parts)
                dt = datetime.date(y, m, d)
                if h + timezone_offset < 0:
                    dt -= datetime.timedelta(days=1)
                logger.info(dt)
                if dt == datetime.date.today():
                    minutes += int(minutes_entry)
    except IndexError:
        logger.info ("Insight session data too short: expected at least 4 entries, retrieved %s minutes from available data", minutes)
    else:
        logger.info ("File parsed successfully, %s minutes retrieved.", minutes)
    return minutes

if __name__ == "__main__":
    # get today's minutes from insight
    insight_minutes = csv_to_todays_minutes(get_insight_data())
    if insight_minutes == 0:
        logger.info("No minutes logged for today's date on InsightTimer.com")
        sys.exit()
    else:
        logger.info ("%s minutes meditated today according to InsightTimer.com", insight_minutes)

    # get dates of days meditated, from beeminder
    #beeminder_dates = beeminder_to_one_per_day(get_beeminder())
    #print "%s datapoints in beeminder" % len(beeminder_dates)

    # get today's date
    new_date = datetime.date.today()
    logger.debug ("new_date: %s", new_date)

    # create beeminder-friendly datapoints
    timestamp = datetime.datetime.today().timestamp()
    new_datapoint = {'timestamp': timestamp, 'value':insight_minutes, 'comment':"beesight+script+entry"}
    logger.debug ("new_datapoint: %s", new_datapoint)

    post_beeminder_entry(new_datapoint)
    logger.info ("Script complete, exiting.")
