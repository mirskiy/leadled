#!/usr/bin/env python3
from Adafruit_Raspberry_Pi_Python_Code.Adafruit_PWM_Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from datetime import datetime, timezone, timedelta
import pytz

ALARMTIMES_FILENAME = 'alarmTimes.txt'
ALARMED_FILENAME = 'alarmed.txt'

# TODO should we use pytz utc instead of timezone.utc
# NOTE make sure everything is done in one timezone!
# prolly utc, but think about stuff like alarm reset
# ex we set an alarm for 23 est at 19, will it get deleted at 20 (utc 0)?

if __name__ == '__main__':
    # Time
    est_tz = pytz.timezone('US/Eastern')
    dt_now_utc = datetime.now(timezone.utc)
    time_now_est = dt_now_utc.astimezone(est_tz).time()

    with open(ALARMED_FILENAME, 'r') as f:
        alarmed_list = []
        for line in f:
            alarmed_list.append(line.strip())

    with open('alarmTimes.txt', 'r') as f:
        for line in f:
            line = line.split('#')[0].strip()   # get everything up to #
            if line == '':      # if blank or comment (possibly with whitespace before)
                continue        # skip

            print(line)
            split_line = line.split()
            time_str = split_line[0]
            set_vals = split_line[1:]
            assert len(set_vals) == 4        # Make sure we have just r, g, b, w

            dt = datetime.strptime(time_str, '%H:%M').replace(tzinfo=timezone.utc)
            time = dt.time()   # TODO shouldn't this be est time? the file is in est times...
            dt_after = dt + timedelta(0, 600, 0)        # TODO terrible naming
            time_after = dt_after.time()

            if line in alarmed_list:    # if we have already alarmed
                continue                # skip

            # !!TODO fix this. its a hack so we can set alarms for the next day
            if time_now_est < time or time_now_est > time_after:      # if we are before or more than 10 mins after alarm time
                print("\tpending")
                continue                       # skip 

            print('alarm! now %s for %s' % (time_now_est, time))
            pwm = PWM(0x70)     # TODO this resets the colors!
            for ch, val in enumerate(set_vals):
                pwm.setPWM(ch, 0, int(val))
                pwm.setPWM(ch+4, 0, int(val))

            alarmed_list.append(line)       # TODO document and think. same alarm twice won't be triggered, but different vals will
            with open(ALARMED_FILENAME, 'a') as alarmed_f:
                output_line= "%s\t# activated %s" % (line, dt_now_utc)		# TODO if we add a comment, the line comparison check fails above
                print(line, file=alarmed_f)
