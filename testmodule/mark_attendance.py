from time import *
import datetime
import calendar

from sqlite3db import FPAttendanceSystemDB


def get_finger_id(fp_id):
    fp_att = FPAttendanceSystemDB()
    get_fp_id = fp_att.select_registered_fp(fp_id)

    name = get_fp_id[0]
    id_ = get_fp_id[1]
    fp_date = get_fp_id[2]
    # for data in get_fp_id:
    #     print("get id ", data)

    print("get id ", get_fp_id)

    today_name = datetime.date.today()
    day_name = calendar.day_name[today_name.weekday()]
    print("my details ", day_name)
    print("my details ", name)
    print("my details ", str(id_))
    print("my details ", fp_date)

    if fp_id >= 0 and day_name != 'Sunday':
        ## Generating TIME VALUES
        now = datetime.datetime.now()
        curr_date = datetime.date.today()
        curr_time = datetime.datetime.now().time()

        my_time_string_10 = "10:30:00"
        my_time_string_12 = "12:00:00"
        my_time_string_13 = "13:29:59"
        my_time_string_15 = "15:00:00"
        my_time_string_16 = "16:00:01"
        my_time_string_19 = "19:30:01"
        my_time_string_20 = "20:30:01"
        my_time_string_22 = "22:30:01"
        time_10 = datetime.datetime.strptime(my_time_string_10, "%H:%M:%S")
        time_12 = datetime.datetime.strptime(my_time_string_12, "%H:%M:%S")
        time_13 = datetime.datetime.strptime(my_time_string_13, "%H:%M:%S")
        time_15 = datetime.datetime.strptime(my_time_string_15, "%H:%M:%S")
        time_16 = datetime.datetime.strptime(my_time_string_16, "%H:%M:%S")
        time_19 = datetime.datetime.strptime(my_time_string_19, "%H:%M:%S")
        time_20 = datetime.datetime.strptime(my_time_string_20, "%H:%M:%S")
        time_22 = datetime.datetime.strptime(my_time_string_22, "%H:%M:%S")

        # I am supposing that the date must be the same as now
        time_10 = now.replace(hour=time_10.time().hour, minute=time_10.time().minute,
                              second=time_10.time().second, microsecond=0)
        time_12 = now.replace(hour=time_12.time().hour, minute=time_12.time().minute,
                              second=time_12.time().second, microsecond=0)
        time_13 = now.replace(hour=time_13.time().hour, minute=time_13.time().minute,
                              second=time_13.time().second, microsecond=0)
        time_15 = now.replace(hour=time_15.time().hour, minute=time_15.time().minute,
                              second=time_15.time().second, microsecond=0)
        time_16 = now.replace(hour=time_16.time().hour, minute=time_16.time().minute,
                              second=time_16.time().second, microsecond=0)
        time_19 = now.replace(hour=time_19.time().hour, minute=time_19.time().minute,
                              second=time_19.time().second, microsecond=0)
        time_20 = now.replace(hour=time_20.time().hour, minute=time_20.time().minute,
                              second=time_20.time().second, microsecond=0)
        time_22 = now.replace(hour=time_22.time().hour, minute=time_22.time().minute,
                              second=time_22.time().second, microsecond=0)

        record = fp_att.select_fp_attendance_record(fp_id=fp_id, cur_date=curr_date)
        record1 = fp_att.select_fp_attendance_all_record()

        print("record is ", record)
        print("record1 is ", record1)
        print("time 15 is ", time_15 < now > time_16)
        print("tnow ", now)
        print("time is is ", datetime.datetime.now().time())

        if record is None:
            print("here it is")
            attt = fp_att.insert_attendance(name=name, cur_date=curr_date,
                                            checkin_time=str(datetime.datetime.now().time()), fp_id=fp_id)
            print("attt", attt)

        else:
            print("No record found")

        record2 = fp_att.select_fp_attendance_status(fp_id=fp_id, cur_date=curr_date)
        checkin_status = record2[0]
        # checkout_status = record2[1]

        print("record2 is ", checkin_status)
        # print("record2 is ", checkout_status)

        if checkin_status == 'Not Marked':
            print("not mark ,..")
            if time_10 < now <= time_12:
                update = fp_att.update_attendance_status(checkin_status='Present', fp_id=fp_id, cur_date=curr_date)

                print("updated", update)
                updated_record = fp_att.select_fp_attendance_record(fp_id=fp_id, cur_date=curr_date)
                print("updated_record", updated_record)
            elif time_12 <= now <= time_13:
                fp_att.update_attendance_status(checkin_status='Late', fp_id=fp_id, cur_date=curr_date)
            elif time_13 <= now <= time_16:
                print("not mark ,..**")

                fp_att.update_attendance_status(checkin_status='Too late', fp_id=fp_id, cur_date=curr_date)

        if checkin_status == 'Present' or checkin_status == 'Late' or checkin_status == 'Too late':
            print("too late ,..")
            if time_15 < now < time_16:
                print("not mark ,.^^.")

                fp_att.update_checkout_status(checkout_status='Leave Too Early', fp_id=fp_id,
                                              cur_date=curr_date)
            if time_16 <= now <= time_19:
                fp_att.update_checkout_status(checkout_status='Leave Early', fp_id=fp_id,
                                              cur_date=curr_date)
            if time_19 <= now <= time_20:
                fp_att.update_checkout_status(checkout_status='Leave on time', fp_id=fp_id,
                                              cur_date=curr_date)
            if time_20 <= now <= time_22:
                fp_att.update_checkout_status(checkout_status='Over time', fp_id=fp_id, cur_date=curr_date)
    else:
        print("It's Sunday")

# get_finger_id(1)
