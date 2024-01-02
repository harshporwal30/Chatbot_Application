# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 13:27:01 2023

@author: Harsh
"""

import os
import random
import re
import json
from datetime import datetime


class Chatbot:
    negative_responses = ["no", "nope", "nah",
                          "no thanks", "no thank", "sorry"]
    exit_keywords = ["bye", "exit", "quit", "goodbye", "later"]
    starter_questions = [
        "What issue are you facing? ",
        "Please tell me about the issue you're experiencing. ",
        "How can I assist you with the problem you're facing? ",
        "Looking for information about restaurants? "
    ]

    def __init__(self):
        self.qry = {
            'book table': r'.*\s*(book|booking|table|reserve).*',
            'payment': r'.*\s*(pay|payment).*',
            'modify reservation': r'.*\s*(change|modify|modification).*',
            'coupon': r'.*\s*(coupon|apply|code|redeem).*',
            'get restaurant': r'.*\s*(get|find|restaurant|place).*',
            'discount': r'.*\s*(discount|offers|offer).*',
            'cancel': r'.*\s*(Cancellation|cancel).*'
        }

    def greet(self):
        self.name = input("Enter your name: ")
        print("Hello " + self.name + "!")
        print("I am ReserveBuddy.")
        self.chat()

    def is_exit_command(self, reply):
        return reply.lower() in self.exit_keywords

    def is_negative_response(self, reply):
        return reply.lower() in self.negative_responses

    def chat(self):
        while True:
            print(random.choice(self.starter_questions))
            reply = input(
                "You: ").lower()
            if self.is_exit_command(reply):
                print("ReserveBuddy: Okay! Have a nice day.")
                break
            elif self.is_negative_response(reply):
                print("ReserveBuddy: Ok! Have a nice day.")
                break
            else:
                self.handle_category_selection(reply)

    def handle_category_selection(self, reply):
        for key, pattern in self.qry.items():
            found_match = re.match(pattern, reply)
            if found_match:
                if key == 'book table':
                    print(self.handle_reservation_query())
                    return
                elif key == 'payment':
                    print(self.payment())
                    return
                elif key == 'modify reservation':
                    print(self.modify_reservation())
                    return
                elif key == 'coupon':
                    print(self.coupon()())
                    return
                elif key == 'get restaurant':
                    print(self.get_restaurant())
                    return
                elif key == 'discount':
                    print(self.discount())
                    return
                elif key == 'cancel':
                    print(self.can_process())
                    return
        self.no_match_intent()

    def get_restaurant(self):
        print("ReserveBuddy: Sure! I can help you find information about restaurants. What is your pincode?")
        user_pincode = input("You: ")

        # Load restaurant data from the JSON file (assuming the file already exists)
        try:
            with open("restaurantdata.json", "r") as json_file:
                restaurant_data = json.load(json_file)
        except FileNotFoundError:
            return "ReserveBuddy: Restaurant data not found. Please enter some restaurant data first."

        # Check if the user's pincode exists in the data
        if "pincodes" in restaurant_data and user_pincode in restaurant_data["pincodes"]:
            print(
                f"ReserveBuddy: Here is the list of restaurants in pincode {user_pincode}:")
            for restaurant in restaurant_data["pincodes"][user_pincode]:
                print(
                    f"Name: {restaurant['name']}, Address: {restaurant['address']}, Cuisine: {restaurant['cuisine']}")
        else:
            return f"ReserveBuddy: No restaurants found for pincode {user_pincode}"

    def handle_reservation_query(self):
        print("ReserveBuddy: Great! Please choose from the following options:")
        print("1. Book a table")
        print("2. Modify a reservation")
        print("3. Know Your Reservation")
        print("4. Cancel your Reservation")
        print("Enter the number corresponding to your choice: ")

        choice = input("You: ")
        if choice == "1":
            self.book_table()
        elif choice == "2":
            print(self.modify_reservation())
        elif choice == "3":
            print(self.rev_details())
        elif choice == "4":
            print(self.cancel_rev())
        else:
            print("Invalid choice. Please select a valid option.")

    def book_table(self):
        responses = [
            "ReserveBuddy: Certainly! I can help you with that. First, let's start with your pincode.",
            "ReserveBuddy: Great! To find the perfect restaurant for you, I'll need your pincode. Could you please provide it?"
        ]
        print(random.choice(responses))
        user_pincode = input("You: ")

        with open('restaurantdata.json', 'r') as json_file:
            res_data = json.load(json_file)
            if user_pincode in res_data["pincodes"]:
                print(
                    "ReserveBuddy: Here are the list of available restaurants in your area")

                for count, res in enumerate(res_data['pincodes'][user_pincode], start=1):
                    print(
                        f"{count}. Name: {res['name']} Address: {res['address']} Cuision: {res['cuisine']}")
                print("ReserveBuddy: Select your Restaurant: ")
                inp = int(input("You: ")) - 1

                if inp < len(res_data['pincodes'][user_pincode]):
                    selected_res = res_data['pincodes'][user_pincode][inp]
                    print(
                        "ReserveBuddy: Great choice! Now, let's proceed with the reservation.")

                    print("Date for the reservation (in YYYY-MM-DD format): ")

                    date_str = input("You: ")
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        print(
                            "ReserveBuddy: Invalid date format. Please use the YYYY-MM-DD format.")
                        return
                    print(
                        "ReserveBuddy: Time for the reservation (in HH:MM format): ")
                    time = input("You: ")
                    print("ReserveBuddy: Number of people: ")
                    num_people = input("You: ")
                    booking_id_gen = str(random.randint(1002, 2905))
                    booking_id = ("B" + booking_id_gen)

                    print(
                        f"ReserveBuddy: Thank you for providing the details. Your reservation for {num_people} people at {selected_res['name']} on {date} at {time} is confirmed! Your booking_id is {booking_id}")

                    booking = {"booking_id": booking_id, "Restaurant": selected_res['name'], "name": self.name,
                               "date": date_str, "time": time, "number_of_people": num_people}

                    with open("chatbotdata.json", "a") as json_file:
                        json.dump(booking, json_file)
                        json_file.write('\n')
                    print(
                        "ReserveBuddy: Do you have any other questions or issues? (yes/no): ")
                    further_reply = input(
                        "You: ").lower()
                    if further_reply == "no":
                        print("ReserveBuddy: Okay! Have a nice day.")
                    else:
                        self.chat()

    def can_process(self):
        response = ("Canceling your reservation is a straightforward process. You have two options:\n"

                    "1. Log in to your account on our website and follow the cancellation instructions.\n"
                    "2. Simply respond with 'yes' to this message, and we'll assist you in canceling your reservation right away.")
        print(response)
        res = input("You: ").lower()
        if res == "yes":
            return (self.cancel_rev())
        else:
            return (self.chat())

    def payment(self):
        responses = [
            "ReserveBuddy: We accept various payment methods, including credit cards, debit cards, and online payment services. Your payment details are processed securely.",
            "ReserveBuddy: You can pay using different methods such as credit cards, debit cards, and online payment services. Choose the one that's most convenient for you."
        ]
        print(random.choice(responses))
        print("ReserveBuddy: Is there anything else you'd like to know or do regarding payments?: ")
        user_response = input(
            "You: ").lower()

        if re.match(r'.*\s*(gateway|transaction|failure|unable).*', user_response):
            print(
                "ReserveBuddy:  We apologize for any inconvenience. Transaction failures can occur due to issues with our payment gateway. This may be caused by connectivity problems, server errors, or temporary downtime. Please try the transaction again in a few minutes. If the issue persists, you may want to check your internet connection or contact our support team for assistance.")
            return
        elif re.match(r'.*\s*(card|decline).*', user_response):
            print("If your credit card payment is declined, it could be due to various reasons. Please ensure that there are sufficient funds in your account, and double-check that your card has not expired. Additionally, verify that the entered card details, including the CVV and expiration date, are accurate. If the problem persists, you may want to contact your bank for further assistance or try an alternative payment method.")
            return
        elif user_response == "no":
            print(
                "ReserveBuddy: Okay! If you have any more questions or need assistance later, feel free to ask.")
            return
        else:
            print(
                "ReserveBuddy: I'm not sure I understand. If you have more questions, please let me know.")

    def modify_reservation(self):
        responses = [
            "Certainly, I can assist you with that. Please provide your reservation details, and I'll help you make the necessary changes.",
            "No problem! Let's modify your reservation. Please provide the details, and we'll get it sorted for you."
        ]
        print("ReserveBuddy: " + random.choice(responses))

        found = False
        print("ReserveBuddy: Enter your Reservation ID: ")
        booking_id = input("You: ")

        with open("chatbotdata.json", "r") as json_file, open("temp.json", "w") as output_file:
            for line in json_file:
                booking = json.loads(line)
                if booking['booking_id'] == booking_id:
                    found = True

                    print("ReserveBuddy: Reservation details:")
                    print(
                        f"Your Booking ID is {booking['booking_id']}, Name: {booking['name']}, Date: {booking['date']}, Time: {booking['time']}, Number of people: {booking['number_of_people']}")
                    print(
                        "What would you like to modify?\n1. Date\n2. Time\n3. Number of People\n")
                    print("Choose an option (1/2/3): ")
                    modification = input("You: ")

                    if modification == "1":
                        print(
                            "ReserveBuddy: New Date for the reservation (in YYYY-MM-DD format): ")
                        new_date = input(
                            "You: ")
                        try:
                            new_date = datetime.strptime(
                                new_date, "%Y-%m-%d")
                            booking['date'] = new_date.strftime("%Y-%m-%d")
                        except ValueError:
                            print(
                                "ReserveBuddy: Invalid date format. Please use the YYYY-MM-DD format.")

                    elif modification == "2":
                        print(
                            "ReserveBuddy: New Time for the reservation (in HH:MM format): ")
                        new_time = input(
                            "You: ")
                        booking['time'] = new_time

                    elif modification == "3":
                        new_people = input("Number of people: ")
                        booking['number_of_people'] = new_people

                    else:
                        print("ReserveBuddy: Invalid Input.")

                    json.dump(booking, output_file)
                    output_file.write('\n')

                else:
                    json.dump(booking, output_file)
                    output_file.write('\n')

        if found:
            os.replace("temp.json", "chatbotdata.json")
            return("ReserveBuddy:: Reservation modified successfully!")

        else:
            return("ReserveBuddy: Reservation ID not found.")

    def rev_details(self):
        response = ["To assist you better, could you please provide either your phone number or booking ID associated with the reservation?",

                    "Sure, in order to retrieve your reservation details, may I have either your phone number or the booking ID?",

                    "Certainly! To pull up your reservation details, could you kindly share either your phone number or the booking ID with me?"]
        print("ReserveBuddy: " + random.choice(response))

        booking_id = input("You: ")

        with open("chatbotdata.json", "r") as json_file:
            for line in json_file:
                booking = json.loads(line)
                if booking['booking_id'] == booking_id:

                    print("ReserveBuddy: Reservation details:")
                    print(
                        f"Your Booking ID is {booking['booking_id']}, Name: {booking['name']}, Date: {booking['date']}, Time: {booking['time']}, Number of people: {booking['number_of_people']}")
                else:
                    print("ReserveBuddy: Invalid Input.")

    def cancel_rev(self):
        response = ["I'm sorry to hear that you need to cancel your reservation. To proceed, could you please provide your booking ID or the phone number associated with the reservation?",

                    "I understand that plans can change. To assist you with cancelling your reservation, may I have either your booking ID or the phone number used for the reservation?",

                    "I'm here to help with the cancellation. To proceed, could you share either your booking ID or the phone number under which the reservation was made?"]
        print("ReserveBuddy: " + random.choice(response))

        booking_id_to_cancel = input(
            "You: ")

        found = False

        with open("chatbotdata.json", "r") as json_file, open("temp.json", "w") as output_file:
            for line in json_file:
                booking = json.loads(line)
                if booking['booking_id'] == booking_id_to_cancel:
                    found = True
                    print("ReserveBuddy: Reservation details:")
                    print(
                        f"Booking ID: {booking['booking_id']}, Name: {booking['name']}, Date: {booking['date']}, Time: {booking['time']}, Number of people: {booking['number_of_people']}")
                    print(
                        "Are you sure you want to cancel this reservation? (yes/no): ")

                    confirmation = input(
                        "You: ").lower()

                    if confirmation == "yes":
                        print("ReserveBuddy: Reservation canceled successfully!")
                    else:
                        print("ReserveBuddy: Reservation cancellation aborted.")
                else:
                    json.dump(booking, output_file)
                    output_file.write('\n')

        if not found:
            print("ReserveBuddy: Reservation ID not found.")

        os.replace("temp.json", "chatbotdata.json")

    def discount(self):
        response = ("Yes, we do offer discounts and coupons for table bookings! We regularly run promotions to provide our customers with special offers. You can check our website or promotional emails for the latest discounts and coupon codes.")
        return response

    def coupon(self):
        response = (
            "To apply a discount code to your reservation, follow these steps:\n"
            "1. During the booking process, look for the 'Promo Code' or 'Discount Code' field.\n"
            "2. Enter the code exactly as provided, ensuring there are no extra spaces.\n"
            "3. Click 'Apply' or 'Submit' to validate the code.\n"
            "4. The discount will be reflected in your total amount.\n"
            "Please note that some codes may have expiration dates or specific terms, so be sure to check the details when applying."
        )
        return response

    def no_match_intent(self):
        responses = ["I don't understand.\n", "I'm not sure I understand.\n"]
        print("ReserveBuddy: " + random.choice(responses))


reservebuddy = Chatbot()
reservebuddy.greet()
