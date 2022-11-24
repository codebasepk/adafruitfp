import time
from time import sleep
import datetime
import calendar
import requests

from sqlite3db import FPAttendanceSystemDB

api_post_url = "http://192.168.1.25:8000/api/post/"
api_update_status_url = "http://192.168.1.25:8000/api/changestatus/"


class MarkAttendance:
    def __init__(self) -> None:
        super().__init__()
        self.fp_att = FPAttendanceSystemDB()

    def get_finger_id(self, fp_id):

        get_fp_id = self.fp_att.select_registered_fp(fp_id)

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

            # specify time to mark attendance
            time_10 = datetime.time(10, 30, 0)
            time_12 = datetime.time(12, 00, 0)
            time_13 = datetime.time(13, 30, 0)
            time_15 = datetime.time(15, 00, 0)
            time_16 = datetime.time(16, 00, 0)
            time_19 = datetime.time(19, 30, 0)
            time_20 = datetime.time(20, 30, 0)
            time_22 = datetime.time(22, 30, 0)

            # combine the specified time with current date
            combine_10 = datetime.datetime.combine(curr_date, time_10)
            combine_12 = datetime.datetime.combine(curr_date, time_12)
            combine_13 = datetime.datetime.combine(curr_date, time_13)
            combine_15 = datetime.datetime.combine(curr_date, time_15)
            combine_16 = datetime.datetime.combine(curr_date, time_16)
            combine_19 = datetime.datetime.combine(curr_date, time_19)
            combine_20 = datetime.datetime.combine(curr_date, time_20)
            combine_22 = datetime.datetime.combine(curr_date, time_22)
            print("combine", combine_10)
            print("combine", combine_22)

            # check fp attendance table is none or not
            record = self.fp_att.select_fp_attendance_record(fp_id=fp_id, cur_date=curr_date)
            # record1 = self.fp_att.select_fp_attendance_all_record()

            print("record is ", record)
            # print("record1 is ", record1)

            if record is None:
                print("here it is")
                print(curr_time)
                # try:
                post_data = {"username": name, "checkinstatus": 'Not Marked', "currentdate": curr_date,
                             "checkintime": str(curr_time), "exitstatus": 'Not Marked',
                             "checkouttime": "", "fpid": fp_id}

                response = requests.post(api_post_url, post_data)

                print(response.status_code)
                # except requests.exceptions.HTTPError as error:
                #     print("error", error)

                if response.status_code == 201:
                    print("attendance marked successfully")
                    attt = self.fp_att.insert_attendance(name=name, cur_date=curr_date,
                                                         checkin_time=str(curr_time), fp_id=fp_id)
                    print("attt", attt)

                elif requests.exceptions.HTTPError:
                    print(response)
                sleep(1)

            else:
                print("No record found")

            # if fp attendance table contains any record get the checkin_status from table
            record2 = self.fp_att.select_fp_attendance_status(fp_id=fp_id, cur_date=curr_date)
            checkin_status = record2[0]
            # checkout_status = record2[1]

            print("record2 is ", checkin_status)
            # print("record2 is ", checkout_status)

            if checkin_status == 'Not Marked':
                print("not mark ,..")
                if combine_10 < now <= combine_12:
                    data = {"checkinstatus": "Present"}
                    self.change_in_status_api(checkin_status="Present", fp_id=fp_id, curr_date=curr_date,
                                              status_data=data)

                elif combine_12 <= now <= combine_13:
                    data = {"checkinstatus": "Late"}
                    self.change_in_status_api(checkin_status="Late", fp_id=fp_id, curr_date=curr_date,
                                              status_data=data)
                elif combine_13 <= now <= combine_16:
                    print("not mark ,..**")

                    data = {"checkinstatus": "Too Late"}
                    self.change_in_status_api(checkin_status="Too Late", fp_id=fp_id, curr_date=curr_date,
                                              status_data=data)

            if checkin_status == 'Present' or checkin_status == 'Late' or checkin_status == 'Too late':
                curr_time = str(datetime.datetime.now().time())
                print("too late ,..")
                if combine_15 < now < combine_16:
                    print("not mark ,.^^.")
                    data = {"checkouttime": curr_time, "exitstatus": "Leave Too Early"}
                    self.change_out_status_api(checkout_status="Leave Too Early", fp_id=fp_id, current_date=curr_date,
                                               status_data=data, curr_time=curr_time)
                elif combine_16 <= now <= combine_19:
                    data = {"checkouttime": curr_time, "exitstatus": "Leave Early"}
                    self.change_out_status_api(checkout_status="Leave Early", fp_id=fp_id, current_date=curr_date,
                                               status_data=data, curr_time=curr_time)
                elif combine_19 <= now <= combine_20:
                    data = {"checkouttime": curr_time, "exitstatus": "Leave on Time"}
                    self.change_out_status_api(checkout_status="Leave on Time", fp_id=fp_id, current_date=curr_date,
                                               status_data=data, curr_time=curr_time)
                elif combine_20 <= now <= combine_22:
                    data = {"checkouttime": curr_time, "exitstatus": "Overtime"}
                    self.change_out_status_api(checkout_status="Overtime", fp_id=fp_id, current_date=curr_date,
                                               status_data=data, curr_time=curr_time)
        else:
            print("It's Sunday")

    def change_in_status_api(self, checkin_status, fp_id, curr_date, status_data):
        status_response = requests.patch(api_update_status_url + str(fp_id) + "/" + str(curr_date) + "/", status_data)

        if status_response.status_code == 200:
            print("Success")
            self.fp_att.update_attendance_status(checkin_status=checkin_status, fp_id=fp_id, cur_date=curr_date)
        elif requests.exceptions.HTTPError:
            print(status_response)

    def change_out_status_api(self, checkout_status, fp_id, current_date, status_data, curr_time):
        outstatus_response = requests.patch(api_update_status_url + str(fp_id) + "/" + str(current_date) + "/",
                                            status_data)
        if outstatus_response.status_code == 200:
            self.fp_att.update_checkout_status(checkout_status=checkout_status, fp_id=fp_id,
                                               checkout_time=curr_time, cur_date=current_date)
            print("Checkout success")
        elif requests.exceptions.HTTPError:
            print(outstatus_response)

# mark_att = MarkAttendance()
# mark_att.get_finger_id(1)
