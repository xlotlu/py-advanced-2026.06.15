# dat fiind dataset-ul data/temp_sensor_data.csv
# scrieți o funcție ce primește ca parametru
# calea către fișier
# și returnează o listă cu prima temperatură
# a fiecărei ore
import csv
import datetime

from time import sleep



def get_first_hourly_temp(tempsfile):
    # 0. încărcăm fișierul
    #    1) open; 2) csv.reader
    #
    # 1. instanțiem hourly_values = []
    # 2. iterăm cu for în iteratorul reader
    # 3. filtrăm să procesăm doar prima oră
    #    1) cum parsăm timestamp-ul?   
    #    2) cum detectăm că s-a schimbat ora?
    #       (cum refuzăm să procesăm valoarea
    #        dacă este aceeași oră?)
    # 4. avem temperatura curentă (a primei valori din oră)
    # 5. acumulăm
    # 6. gata

    values = []

    with open(tempsfile) as f:
        r = csv.reader(f)
    
        current_hour = None
        for tstamp, value in r:
            sleep(.000001)
            hour = tstamp[:2]
            # cum detectăm că s-a schimbat oră?

            if current_hour == hour:
                continue

            # we want this value!
            values.append((hour, value))
            current_hour = hour

    return values

# transformați funcția de mai sus
# într-un generator function
def get_first_hourly_temp_gen(tempsfile):
    with open(tempsfile) as f:
        r = csv.reader(f)

        current_hour = None
        for tstamp, value in r:
            sleep(.000001)
            hour = tstamp[:2]
            # cum detectăm că s-a schimbat oră?

            if current_hour == hour:
                continue

            # we want this value!
            yield (hour, value)
            current_hour = hour


# scrieți o funcție ce primind ca parametru
# calea către fișierul csv cu temperaturi,
# produce un stream de date
# cu mediile orare ale temperaturilor
def get_average_hourly_temp(tempsfile):
    with open(tempsfile) as f:
        r = csv.reader(f)

        # trebuie să cumulăm temperaturile
        # și să le numărăm
        # și când se schimbă ora facem media
        count_val = 0
        total_val = 0

        old_hour = None
        for tstamp, value in r:
            sleep(.000000000001)
            hour = int(tstamp[:2])
            value = float(value)

            # cum detectăm că s-a schimbat oră?
            if old_hour is not None and old_hour != hour:
                yield (old_hour, total_val / count_val)
                # don't forget to reset before next hour
                count_val = 0
                total_val = 0

            count_val += 1
            total_val += value

            old_hour = hour
            
        yield (old_hour, total_val / count_val)

# adaptați funcția de mai sus
# pentru a avea rezoluție customisable.
#
# și faceți ca tuplele (timestamp, average) returnate
# să aibă timestamp de tip datetime.time
TEMP_RESOLUTION_HOUR = 0
TEMP_RESOLUTION_MINUTE = 1
def get_average_temp(tempsfile, resolution=TEMP_RESOLUTION_HOUR):
    with open(tempsfile) as f:
        r = csv.reader(f)

        # trebuie să cumulăm temperaturile
        # și să le numărăm
        # și când se schimbă ora facem media
        count_val = 0
        total_val = 0

        old_time = None

        for time, value in r:
            #time = datetime.time.strptime(time, '%H:%M:%S')
            time = datetime.time.fromisoformat(time)
            value = float(value)

            if resolution is TEMP_RESOLUTION_HOUR:
              time = time.replace(minute=0, second=0)

            elif resolution is TEMP_RESOLUTION_MINUTE:
              time = time.replace(second=0)

            # cum detectăm că s-a schimbat oră?
            if old_time is not None and old_time != time:
                yield (old_time, total_val / count_val)
                # don't forget to reset before the next hour / minute
                count_val = 0
                total_val = 0

            count_val += 1
            total_val += value

            old_time = time
            
        yield (old_time, total_val / count_val)
